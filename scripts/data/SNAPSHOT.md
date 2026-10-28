# Inputs of `sheets.build(P, S, out_dir)`

## `P` - `profile.json`, the owner's own content (edit by hand)

| field | meaning |
|---|---|
| `handle`, `title` | "kazii", "The Builder" |
| `github`, `linkedin` | the two outward links |
| `intro` | the paragraph under the title sheet |
| `principles[]` | three `{name, text}` working principles, keyed 1-3 on the specification sheet |
| `flagships[]` | the six projects drawn on the assemblies sheet; each needs a drawing in `sheets.DRAW` and logos in `sheets.FLAG_LOGOS` |
| `project_groups[]` | all projects in groups A-E: `{letter, name, projects: [{name, url, stack, note}]}`; item numbers run across groups |
| `toolbox[]` | `{group, tools: [[label, logo file in logos/ or null]]}`; null draws the LLM-as-judge scales glyph |
| `politicas_figures` | the figures in the parts-list table, with their source line |
| `vr[]` | `{file, project, kind, caption, title?, sub?}`; on the VR sheet `title` names a plate (default: the project) and `sub` is the line under it (default: the project's stack) |
| `vr_sheet` | the two `vr[]` files the VR sheet inlines from `images/vr/`, left then right; the README links the left one's project |

## `S` - the snapshot, built from the GitHub GraphQL API by `update_readme.snapshot()`

| field | meaning |
|---|---|
| `fetched_at` | ISO time of the fetch; the date drives "last push" ages and the footer |
| `contributions.total_last_year` | contributions in the last 365 days |
| `contributions.current_streak_days` | consecutive days up to today with a contribution |
| `contributions.weeks[][]` | 53 weeks of 7 `{date, count}` days, Sunday first; the first week may be partial |
| `repos.public_count`, `repos.pushed_last_30_days` | public non-fork repos, and how many were pushed in 30 days |
| `repos.language_mix_by_code_size[]` | `{language, percent}` by bytes of code, markup and build glue excluded |
| `repos.items[]` | `{name, url, description, pushed_at, primary_language}`, newest push first, the profile repo excluded |

`python scripts/update_readme.py --snapshot FILE --out DIR` replays a saved snapshot instead of
fetching, which is how a change to the drawings can be checked without a token.

## `logos/` - Simple Icons 15.21.0, CC0 (`LICENSE-simple-icons.md`)

Simple Icons has no C# mark, so C# is drawn with `dotnet.svg`.
