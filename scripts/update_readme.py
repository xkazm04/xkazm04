#!/usr/bin/env python3
"""Regenerate the profile's branded assets and the dynamic README sections.

- assets/header-{dark,light}.svg  drafting-sheet header (REV = current month)
- assets/stats-{dark,light}.svg   build log: contributions, heatmap, language mix
- assets/<panel>-{dark,light}.svg the figures and section dividers from panels.py
- README BUILDLOG block           most recently pushed public repos
- README PARTS block              numbered links that go with the parts-list figure

Uses only the standard library. Reads GITHUB_TOKEN from the environment.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import THEMES, render_header, render_stats  # noqa: E402
import panels  # noqa: E402

USERNAME = os.environ.get("PROFILE_USER", "xkazm04")
README = "README.md"
ASSETS = "assets"
RECENT_COUNT = 8
LANG_ORDER = ["TypeScript", "Rust", "Python", "C#", "C++", "JavaScript"]
SKIP_REPOS = {USERNAME}
DIVIDERS = ["01", "02", "03", "04", "END"]
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


def replace_block(content, name, body):
    pattern = rf"<!-- {name}:START -->.*?<!-- {name}:END -->"
    block = f"<!-- {name}:START -->\n{body}\n<!-- {name}:END -->"
    return re.sub(pattern, lambda _: block, content, flags=re.DOTALL)


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


def main():
    user = graphql(QUERY, {"login": USERNAME})["user"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]
    now = datetime.now(timezone.utc)

    def pushed(r):
        return datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00"))

    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    stats = {
        "year": now.year,
        "total": cal["totalContributions"],
        "repos": repos["totalCount"],
        "pushed_30d": sum(1 for r in repos["nodes"] if pushed(r) >= now - timedelta(days=30)),
        "streak": current_streak(days),
        "weeks": weeks,
        "week_dates": [[d["date"] for d in w["contributionDays"]] for w in cal["weeks"]],
        "langs": language_mix(repos["nodes"]),
        "updated": f"{now:%Y-%m-%d}",
    }

    os.makedirs(ASSETS, exist_ok=True)
    for theme in THEMES:
        with open(f"{ASSETS}/header-{theme}.svg", "w", encoding="utf-8", newline="\n") as f:
            f.write(render_header(theme, f"{now:%Y.%m}"))
        with open(f"{ASSETS}/stats-{theme}.svg", "w", encoding="utf-8", newline="\n") as f:
            f.write(render_stats(theme, stats))

    pushed_by_name = {r["name"]: pushed(r) for r in repos["nodes"]}
    timeline_repos = [(r["name"], pushed(r), (r["primaryLanguage"] or {}).get("name", "n/a"))
                      for r in repos["nodes"] if r["name"] not in SKIP_REPOS]
    for theme in THEMES:
        lang_color = dict(zip(LANG_ORDER, THEMES[theme]["langs"]))
        out = {
            "architecture": panels.render_architecture(theme),
            "cards": panels.render_cards(theme, pushed_by_name, now),
            "parts": panels.render_parts(theme),
            "timeline": panels.render_timeline(theme, timeline_repos, lang_color, now),
            "pulse": panels.render_pulse(theme, weeks, stats["langs"]),
            "vr": panels.render_vr(theme),
            "toolbox": panels.render_toolbox(theme),
            "civic": panels.render_civic(theme),
        }
        for num in DIVIDERS:
            out[f"divider-{num.lower()}"] = panels.render_divider(theme, num)
        for name, svg in out.items():
            with open(f"{ASSETS}/{name}-{theme}.svg", "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)

    lines = []
    shown = [r for r in repos["nodes"] if r["description"] and r["name"] not in SKIP_REPOS]
    for r in shown[:RECENT_COUNT]:
        lang = (r["primaryLanguage"] or {}).get("name", "n/a")
        lines.append(f"`{pushed(r):%Y-%m-%d}` &nbsp;**[{r['name']}]({r['url']})** &nbsp;<sub>{lang.upper()}</sub><br/>")
        lines.append(f"{r['description']}")
        lines.append("")
    buildlog = "\n".join(lines).rstrip()

    with open(README, encoding="utf-8") as f:
        content = f.read()
    content = replace_block(content, "BUILDLOG", buildlog)
    content = replace_block(content, "PARTS", panels.parts_links())
    # Bust GitHub's image cache for the regenerated SVGs.
    content = re.sub(r"(assets/[\w-]+-(?:dark|light)\.svg)(\?v=\d+)?", rf"\1?v={now:%Y%m%d}", content)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"contributions={stats['total']} repos={stats['repos']} pushed30d={stats['pushed_30d']} "
          f"streak={stats['streak']} langs={[n for n, _ in stats['langs']]}")


if __name__ == "__main__":
    main()
