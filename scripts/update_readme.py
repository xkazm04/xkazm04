#!/usr/bin/env python3
"""Regenerate the profile: fetch live GitHub data, then redraw README.md and the six sheets.

The fetch is turned into a snapshot (the shape sheets.build reads; see snapshot()), and
sheets.build writes README.md and assets/{title,spec,log,assemblies,vr,toolbox}-{dark,light}.svg.
The owner's own content lives in scripts/data/profile.json.

Uses only the standard library. Reads GITHUB_TOKEN from the environment.
"""

import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheets  # noqa: E402

USERNAME = os.environ.get("PROFILE_USER", "xkazm04")
SKIP_REPOS = {USERNAME}
# Markup, config and build glue that would drown out the real languages.
NON_CODE = {"HTML", "CSS", "SCSS", "Shell", "PowerShell", "Batchfile", "Dockerfile", "NSIS",
            "Just", "HCL", "Go Template", "Makefile", "CMake", "ShaderLab", "HLSL", "PLpgSQL"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                 first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name url description pushedAt
        primaryLanguage { name }
        languages(first: 10) { edges { size node { name } } }
      }
    }
  }
}
"""


def graphql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def current_streak(days):
    today = date.today().isoformat()
    streak = 0
    for d in sorted(days, key=lambda d: d["date"], reverse=True):
        if d["date"] > today:
            continue
        if d["contributionCount"] > 0:
            streak += 1
        elif d["date"] != today:  # today may simply not have activity yet
            break
    return streak


def language_mix(repos, top=6):
    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in NON_CODE:
                sizes[name] = sizes.get(name, 0) + e["size"]
    total = sum(sizes.values()) or 1
    ranked = sorted(sizes.items(), key=lambda kv: -kv[1])
    mix = [(n, s * 100 / total) for n, s in ranked[: top - 1]]
    rest = 100 - sum(p for _, p in mix)
    if rest > 0.5:
        mix.append(("Other", rest))
    return mix


def snapshot(user, now):
    """The fetch, in the shape sheets.build reads (documented in scripts/data/SNAPSHOT.md)."""
    cal = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]

    def pushed(r):
        return datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00"))

    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return {
        "fetched_at": now.isoformat(timespec="seconds"),
        "login": USERNAME,
        "contributions": {
            "total_last_year": cal["totalContributions"],
            "current_streak_days": current_streak(days),
            "weeks": [[{"date": d["date"], "count": d["contributionCount"]} for d in w["contributionDays"]] for w in cal["weeks"]],
        },
        "repos": {
            "public_count": repos["totalCount"],
            "pushed_last_30_days": sum(1 for r in repos["nodes"] if pushed(r) >= now - timedelta(days=30)),
            "language_mix_by_code_size": [{"language": n, "percent": round(p, 1)} for n, p in language_mix(repos["nodes"])],
            "items": [{
                "name": r["name"], "url": r["url"], "description": r["description"], "pushed_at": r["pushedAt"],
                "primary_language": (r["primaryLanguage"] or {}).get("name"),
            } for r in repos["nodes"] if r["name"] not in SKIP_REPOS],
        },
    }


def main():
    """update_readme.py [--snapshot FILE] [--out DIR]: FILE replays a saved snapshot instead of fetching."""
    args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
    now = datetime.now(timezone.utc)
    if "--snapshot" in args:
        with open(args["--snapshot"], encoding="utf-8") as f:
            S = json.load(f)
    else:
        S = snapshot(graphql(QUERY, {"login": USERNAME})["user"], now)
    out = args.get("--out", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    sheets.build(sheets.load("profile.json"), S, out, version=f"{now:%Y%m%d}")
    c, r = S["contributions"], S["repos"]
    print(f"contributions={c['total_last_year']} repos={r['public_count']} pushed30d={r['pushed_last_30_days']} "
          f"streak={c['current_streak_days']} langs={[m['language'] for m in r['language_mix_by_code_size']]}")


if __name__ == "__main__":
    main()
