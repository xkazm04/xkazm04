<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg?v=20261014" />
  <img alt="kazii, The Builder" src="assets/header-dark.svg?v=20261014" width="100%" />
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/michalkazdan"><img src="https://img.shields.io/badge/LinkedIn-michalkazdan-F59E0B?style=flat-square&logo=linkedin&logoColor=F59E0B&labelColor=0B0D10" alt="LinkedIn" /></a>
</p>

I build local-first software: tools that run on your machine, keep your data there, and put AI agents to work on real projects. Most of it is TypeScript and Rust, with some C++ and C# when the target is a VR headset.

---

### 01 · Specification

- **Local-first by default.** State lives in SQLite on the user's machine. Nothing leaves unless they send it.
- **Agents do the work, people approve it.** Claude Code runs headless, behind gates a person controls.
- **Ship the whole thing.** Desktop app, backend, observability and the site that explains it.

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/architecture-light.svg?v=20261014" />
  <img alt="Local-first architecture: SQLite on your machine, agents, human approval gate" src="assets/architecture-dark.svg?v=20261014" width="100%" />
</picture>

---

### 02 · Build Log

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg?v=20261014" />
  <img alt="Contributions this year, contribution heatmap and language mix" src="assets/stats-dark.svg?v=20261014" width="100%" />
</picture>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/pulse-light.svg?v=20261014" />
  <img alt="Weekly contribution pulse and language mix" src="assets/pulse-dark.svg?v=20261014" width="100%" />
</picture>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/timeline-light.svg?v=20261014" />
  <img alt="Timeline of recent pushes" src="assets/timeline-dark.svg?v=20261014" width="100%" />
</picture>

<!-- BUILDLOG:START -->
`2026-10-13` &nbsp;**[athena-portable](https://github.com/xkazm04/athena-portable)** &nbsp;<sub>PYTHON</sub><br/>
Athena: a personal AI agent that works inside your web apps and asks before it acts. NVIDIA Nemotron on Nebius Token Factory red-teams her gate.

`2026-10-13` &nbsp;**[pof](https://github.com/xkazm04/pof)** &nbsp;<sub>TYPESCRIPT</sub><br/>
AI-powered companion for building Unreal Engine 5 C++ games — checklists, feature tracking, and quality evaluation from prototype to polish.

`2026-10-13` &nbsp;**[ai-registry](https://github.com/xkazm04/ai-registry)** &nbsp;<sub>JAVASCRIPT</sub><br/>
Example AI development registry - skills, practices and org memory that ascent onboards, indexes and tracks.

`2026-10-13` &nbsp;**[bp](https://github.com/xkazm04/bp)** &nbsp;<sub>TYPESCRIPT</sub><br/>
bípípí

`2026-10-13` &nbsp;**[systedo-case](https://github.com/xkazm04/systedo-case)** &nbsp;<sub>TYPESCRIPT</sub><br/>
Adamant — AI ad intelligence on your machine: measure, triage and generate ad assets across Google Ads, Sklik, Meta and TikTok.

`2026-10-13` &nbsp;**[kp](https://github.com/xkazm04/kp)** &nbsp;<sub>TYPESCRIPT</sub><br/>
open-source hiring workspace

`2026-10-13` &nbsp;**[pumper](https://github.com/xkazm04/pumper)** &nbsp;<sub>RUST</sub><br/>
Local-first scraping service — one Rust binary, durable SQLite job queue, three pluggable scrape engines (HTTP, browser, Claude Code).

`2026-10-13` &nbsp;**[garden-vr](https://github.com/xkazm04/garden-vr)** &nbsp;<sub>C#</sub><br/>
Two calm, hands-first daily-ritual apps (Unity, Meta Quest) that grow a living garden from real habits. Meta VR Start Developer Competition 2026.
<!-- BUILDLOG:END -->

---

### 03 · Assemblies

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards-light.svg?v=20261014" />
  <img alt="Flagship project cards" src="assets/cards-dark.svg?v=20261014" width="100%" />
</picture>

<table>
<tr>
<td width="50%" valign="top">

**A · Agent platforms & dev tooling**

**[personas](https://github.com/xkazm04/personas)** &nbsp;<sub>TAURI 2 · REACT 19 · SQLITE</sub><br/>
Desktop app for building AI agents, wiring them to your tools, running them on triggers and orchestrating teams of them on real software projects.

**[vibeman](https://github.com/xkazm04/vibeman)** &nbsp;<sub>NEXT.JS 16 · CLAUDE CODE · OLLAMA</sub><br/>
Project control room that runs tasks through up to four concurrent Claude Code sessions or local models.

**[pof](https://github.com/xkazm04/pof)** &nbsp;<sub>NEXT.JS · UNREAL ENGINE 5</sub><br/>
Companion for UE5 C++ games: checklists, feature tracking, quality evaluation and an embedded Claude Code terminal with domain skill packs.

**[ascent](https://github.com/xkazm04/ascent)** &nbsp;<sub>TYPESCRIPT</sub><br/>
Scores how AI-native a team's engineering is, from 0 to 100 across nine weighted dimensions, with evidence and a path to the next level.

</td>
<td width="50%" valign="top">

**B · Rust infrastructure**

**[lighttrack](https://github.com/xkazm04/lighttrack)** &nbsp;<sub>RUST · SQLITE / POSTGRES / FIRESTORE</sub><br/>
Self-hosted LLM observability with LLM-as-judge scoring. One container, your own database.

**[pumper](https://github.com/xkazm04/pumper)** &nbsp;<sub>RUST · SQLITE</sub><br/>
Scraping service in one binary with a durable job queue and three engines that escalate from HTTP to browser to Claude Code.

**C · Hands-first VR** &nbsp;<sub>META VR START 2026</sub>

<a href="https://github.com/xkazm04/garden-vr"><img src="assets/garden-vr.jpg" alt="garden-vr concept art: a glowing terrarium jar that asks what you would like to grow" width="100%" /></a>

**[garden-vr](https://github.com/xkazm04/garden-vr)** &nbsp;<sub>UNITY · META QUEST</sub><br/>
Two calm daily-ritual apps that grow a living garden from real habits.

<a href="https://github.com/xkazm04/mage-arena"><img src="assets/mage-arena.jpg" alt="mage-arena storyboard: first-person view over an arena with torches" width="100%" /></a>

**[mage-arena](https://github.com/xkazm04/mage-arena)** &nbsp;<sub>UNREAL ENGINE 5 · META QUEST</sub><br/>
Seated spell duel played with your hands.

</td>
</tr>
<tr>
<td width="50%" valign="top">

**D · Media & data**

**[gravitone](https://github.com/xkazm04/gravitone)** &nbsp;<sub>PYTHON · ARM</sub><br/>
ElevenLabs-compatible TTS with voice cloning, CPU-only: 4.26× realtime on Graviton4 at about $0.0004 per audio-minute.

**[stat-reel](https://github.com/xkazm04/stat-reel)** &nbsp;<sub>TYPESCRIPT</sub><br/>
Turns licensed sports data into 1 to 3 minute data-visualisation videos.

**[systedo-case](https://github.com/xkazm04/systedo-case)** &nbsp;<sub>TYPESCRIPT</sub><br/>
Ad intelligence on your machine across Google Ads, Sklik, Meta and TikTok.

**[MiSu](https://www.youtube.com/watch?v=Kam3LOzbPoI)** &nbsp;<sub>Prompt engineering</sub><br/>
AI generated music album. I told it to make great music...and it does

</td>
<td width="50%" valign="top">

**E · Civic & experiments**

**[politicas](https://github.com/xkazm04/politicas)** &nbsp;<sub>TYPESCRIPT · CS / EN</sub><br/>
Public-accountability platform for Czech politics: MP scoring, voting records, money ties and budgets on one entity graph.

**[athena-portable](https://github.com/xkazm04/athena-portable)** &nbsp;<sub>PYTHON · HACKATHON</sub><br/>
Personal agent that works inside your web apps and asks before it acts.

**[paypal](https://github.com/xkazm04/paypal)** &nbsp;<sub>RUST · HACKATHON</sub><br/>
The Table: agent-to-agent haggling over PayPal.

</td>
</tr>
</table>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/vr-light.svg?v=20261014" />
  <img alt="garden-vr and mage-arena example frames" src="assets/vr-dark.svg?v=20261014" width="100%" />
</picture>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/civic-light.svg?v=20261014" />
  <img alt="politicas knowledge graph in numbers" src="assets/civic-dark.svg?v=20261014" width="100%" />
</picture>


---

### 04 · Toolbox

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/toolbox-light.svg?v=20261014" />
  <img alt="Toolbox: languages, apps, data, AI, XR" src="assets/toolbox-dark.svg?v=20261014" width="100%" />
</picture>

---|---|
| **Languages** | TypeScript · Rust · Python · C++ · C# |
| **Apps** | React 19 · Next.js 16 · Tauri 2 · Tailwind v4 |
| **Data** | SQLite · PostgreSQL · Firestore |
| **AI** | Claude Code · MCP · LLM-as-judge · Ollama |
| **XR** | Unreal Engine 5 · Unity · Meta Quest |

---

<p align="center"><sub>kazii · The Builder · assets regenerated daily by GitHub Actions</sub></p>
