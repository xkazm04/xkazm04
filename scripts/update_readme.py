#!/usr/bin/env python3
"""Refresh the dynamic sections of the profile README.

- STATS:   contributions this year, public repos, repos pushed in the last 30 days
- RECENT:  most recently pushed public, non-fork repos that have a description
- Cache-busts third-party stat card URLs and stamps the update time.

Uses only the standard library. Reads GITHUB_TOKEN from the environment.
"""

import json
import os
import re
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

USERNAME = os.environ.get("PROFILE_USER", "xkazm04")
README = "README.md"
RECENT_COUNT = 8
SKIP_REPOS = {USERNAME}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection { contributionCalendar { totalContributions } }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                 first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name url description pushedAt stargazerCount
        primaryLanguage { name }
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


def badge(label, value):
    enc_label = quote(label).replace("-", "--")
    value = quote(f"{value:,}" if isinstance(value, int) else str(value))
    return (
        f"![{label}](https://img.shields.io/badge/{enc_label}-{value}"
        f"-2dd4bf?style=flat-square&labelColor=0d1117)"
    )


def replace_block(content, name, body):
    pattern = rf"<!-- {name}:START -->.*?<!-- {name}:END -->"
    block = f"<!-- {name}:START -->\n{body}\n<!-- {name}:END -->"
    return re.sub(pattern, lambda _: block, content, flags=re.DOTALL)


def main():
    user = graphql(QUERY, {"login": USERNAME})["user"]
    total_contrib = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    repos = user["repositories"]
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)

    def pushed(r):
        return datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00"))

    recent_30d = sum(1 for r in repos["nodes"] if pushed(r) >= cutoff)

    stats = "\n".join([
        '<div align="center">',
        "",
        badge(f"Contributions in {now.year}", total_contrib),
        badge("Public repos", repos["totalCount"]),
        badge("Repos pushed (30d)", recent_30d),
        "",
        "</div>",
    ])

    rows = ["| Repo | Language | Pushed | About |", "|------|:--------:|:------:|-------|"]
    shown = [r for r in repos["nodes"] if r["description"] and r["name"] not in SKIP_REPOS]
    for r in shown[:RECENT_COUNT]:
        lang = (r["primaryLanguage"] or {}).get("name", "-")
        desc = r["description"].replace("|", "\\|")
        rows.append(f"| [**{r['name']}**]({r['url']}) | {lang} | {pushed(r):%Y-%m-%d} | {desc} |")
    recent = "\n".join(rows) + "\n\n<sub>Auto-updated daily by GitHub Actions.</sub>"

    with open(README, encoding="utf-8") as f:
        content = f.read()

    content = replace_block(content, "STATS", stats)
    content = replace_block(content, "RECENT", recent)

    ts = int(time.time())
    content = re.sub(r"([?&])cache=\d+", rf"\g<1>cache={ts}", content)
    content = re.sub(
        r"<!-- Last updated:.*?-->",
        f"<!-- Last updated: {now:%Y-%m-%d %H:%M:%S} UTC -->",
        content,
    )

    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"contributions={total_contrib} repos={repos['totalCount']} pushed30d={recent_30d}")


if __name__ == "__main__":
    main()
