"""Extra profile panels in the drafting-sheet look: architecture, project cards, parts list,
build-log timeline, pulse dashboard, VR corner, toolbox stencil, civic spotlight, section dividers.

Each renderer returns an SVG string for a theme from brand.THEMES. Dynamic ones
take data from update_readme.py; the rest are static. Figures are numbered in page order
and every one carries a title block (DWG = figure number).
"""

import base64
import math
import os
from datetime import datetime, timezone
from html import escape

from brand import STYLE, THEMES, _sheet, dim, title_block, vdim

W = 1200
REV = f"{datetime.now(timezone.utc):%Y.%m}"


def _open(t, w, h, label, extra=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">',
            STYLE, extra, _sheet(t, w, h)]


def _close(o, t, h, dwg):
    o.append(title_block(t, W, h, dwg, REV))
    o.append("</svg>\n")
    return "\n".join(o)


def _title(t, text, y=64):
    return f'<text x="56" y="{y}" font-size="13" letter-spacing="3" fill="{t["accent"]}">{escape(text)}</text>'


def _arrow(t, x1, y1, x2, y2, cls="", color=None, dash=""):
    c = color or t["muted"]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path class="{cls}" d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="1.5" fill="none"{d}/>'
            f'<path d="M{x2} {y2}l-8 -4v8z" fill="{c}" transform="rotate({_ang(x1, y1, x2, y2)} {x2} {y2})"/>')


def _ang(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def _frac(points, i):
    """Fraction of a polyline's length covered up to point i (for animateMotion keyPoints)."""
    seg = [math.dist(a, b) for a, b in zip(points, points[1:])]
    return sum(seg[:i]) / sum(seg)


def _poly(points):
    return "M" + "L".join(f"{x} {y}" for x, y in points)


# --------------------------------------------------------------------------- architecture

def render_architecture(theme):
    t = THEMES[theme]
    h = 384
    o = _open(t, W, h, "Local-first architecture: your machine holds SQLite, agents propose, a human approval gate decides")
    o.append(_title(t, "FIG. 01 / LOCAL-FIRST ARCHITECTURE"))
    o.append(dim(t, 56, 856, 80, "ALL STATE LOCAL", ext=92))
    # machine boundary
    o.append(f'<rect x="56.5" y="92.5" width="800" height="196" rx="4" fill="none" stroke="{t["accent"]}" stroke-dasharray="8 6"/>')
    o.append(f'<text x="72" y="112" font-size="11" letter-spacing="2" fill="{t["accent"]}">YOUR MACHINE</text>')
    o.append(f'<text x="884" y="112" font-size="11" letter-spacing="2" fill="{t["muted"]}">OUTSIDE</text>')

    def box(x, y, w, hh, title, sub, hl=False):
        stroke = t["accent"] if hl else t["ink"]
        return (f'<rect x="{x}.5" y="{y}.5" width="{w}" height="{hh}" fill="{t["bg"]}" stroke="{stroke}" stroke-width="{1.8 if hl else 1.2}"/>'
                f'<text x="{x + w / 2}" y="{y + hh / 2 - 2}" text-anchor="middle" font-size="15" font-weight="700" fill="{t["ink"]}">{title}</text>'
                f'<text x="{x + w / 2}" y="{y + hh / 2 + 18}" text-anchor="middle" font-size="11" fill="{t["muted"]}">{sub}</text>')

    # data store (cylinder)
    cx, cy = 150, 170
    o.append(f'<path d="M{cx - 54} {cy}v70c0 14 24 22 54 22s54 -8 54 -22v-70" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.4"/>'
             f'<ellipse cx="{cx}" cy="{cy}" rx="54" ry="14" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.4"/>'
             f'<text x="{cx}" y="{cy + 50}" text-anchor="middle" font-size="15" font-weight="700" fill="{t["ink"]}">SQLite</text>'
             f'<text x="{cx}" y="{cy + 68}" text-anchor="middle" font-size="11" fill="{t["muted"]}">state + history</text>')
    o.append(box(330, 150, 150, 80, "AGENTS", "Claude Code / Ollama"))
    o.append(box(570, 150, 130, 80, "GATE", "human approves", hl=True))
    o.append(box(750, 150, 80, 80, "ACT", "apply"))
    o.append(_arrow(t, 204, 200, 330, 190, "draw"))
    o.append(_arrow(t, 480, 190, 570, 190, "draw"))
    o.append(_arrow(t, 700, 190, 750, 190, "draw", t["accent"]))
    o.append(f'<path class="draw" d="M790 230V264H150V246" fill="none" stroke="{t["muted"]}" stroke-width="1.2" stroke-dasharray="5 5"/>')
    o.append(f'<text x="470" y="258" font-size="11" fill="{t["muted"]}">result written back locally</text>')

    # Animated flow on a 6s loop: one proposal is approved at the gate, acted on and written back
    # to SQLite; a second (offset 3s) is rejected at the gate and goes no further.
    dur = "6s"
    ok = [(204, 200), (330, 190), (480, 190), (570, 190), (635, 190), (700, 190), (790, 190), (790, 264), (150, 264), (150, 246)]
    g = _frac(ok, 4)
    o.append(f'<circle r="5" fill="{t["accent"]}" opacity="0">'
             f'<animateMotion dur="{dur}" repeatCount="indefinite" path="{_poly(ok)}" calcMode="linear" keyPoints="0;{g:.3f};{g:.3f};1;1" keyTimes="0;.3;.45;.92;1"/>'
             f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.03;.9;.94;1"/></circle>')
    o.append(f'<circle cx="635" cy="190" r="0" fill="none" stroke="{t["accent"]}" stroke-width="1.5">'
             f'<animate attributeName="r" dur="{dur}" repeatCount="indefinite" values="6;6;44;44" keyTimes="0;.3;.42;1"/>'
             f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" values="0;0;.9;0;0" keyTimes="0;.299;.3;.42;1"/></circle>')
    o.append(f'<text x="635" y="142" text-anchor="middle" font-size="10" letter-spacing="2" fill="{t["accent"]}" opacity="0">APPROVED'
             f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;.31;.34;.47;.52;1"/></text>')
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="54" ry="14" fill="none" stroke="{t["accent"]}" stroke-width="2.5" opacity="0">'
             f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" values="0;0;1;0" keyTimes="0;.9;.93;1"/></ellipse>')
    no = ok[:5]
    o.append(f'<circle r="5" fill="{t["muted"]}" opacity="0">'
             f'<animateMotion dur="{dur}" begin="3s" repeatCount="indefinite" path="{_poly(no)}" calcMode="linear" keyPoints="0;1;1" keyTimes="0;.3;1"/>'
             f'<animate attributeName="opacity" dur="{dur}" begin="3s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.03;.36;.44;1"/></circle>')
    o.append(f'<text x="635" y="142" text-anchor="middle" font-size="10" letter-spacing="2" fill="{t["muted"]}" opacity="0">REJECTED'
             f'<animate attributeName="opacity" dur="{dur}" begin="3s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;.31;.34;.42;.46;1"/></text>')

    # outside: only on explicit send
    o.append(f'<rect x="884.5" y="150.5" width="260" height="80" fill="none" stroke="{t["line"]}" stroke-dasharray="4 4"/>')
    o.append(f'<text x="1014" y="186" text-anchor="middle" font-size="14" fill="{t["ink"]}">cloud / third parties</text>')
    o.append(f'<text x="1014" y="208" text-anchor="middle" font-size="11" fill="{t["muted"]}">only what you send</text>')
    o.append(f'<path d="M830 190H884" stroke="{t["accent"]}" stroke-width="1.5" stroke-dasharray="3 5"/>')
    o.append(f'<text x="857" y="180" text-anchor="middle" font-size="16" fill="{t["accent"]}">?</text>')
    o.append(f'<text x="56" y="322" font-size="11" fill="{t["muted"]}">Agents do the work, people approve it. Nothing leaves unless you send it.</text>')
    return _close(o, t, h, "01")


# --------------------------------------------------------------------------- project cards (exploded views)

# (name, one-liner, layers top to bottom as (role, label))
CARDS = [
    ("personas", "AI agent desktop app", [("UI", "REACT 19"), ("SHELL", "TAURI 2 / RUST"), ("DATA", "SQLITE")]),
    ("vibeman", "Control room for Claude Code", [("UI", "NEXT.JS 16"), ("RUN", "CLAUDE CODE x4"), ("LOCAL", "OLLAMA")]),
    ("lighttrack", "LLM observability + judge", [("UI", "DASHBOARD"), ("CORE", "RUST / JUDGE"), ("DATA", "SQLITE / PG / FS")]),
    ("pumper", "Local-first scraping service", [("API", "ONE BINARY"), ("CORE", "HTTP > BROWSER > CC"), ("DATA", "SQLITE QUEUE")]),
    ("ascent", "0-100 AI-maturity score", [("OUT", "0-100 SCORE"), ("CORE", "9 DIMENSIONS"), ("IN", "REPO EVIDENCE")]),
    ("politicas", "Czech politics accountability", [("UI", "CS / EN SITE"), ("CORE", "SCORERS"), ("DATA", "ENTITY GRAPH")]),
]


def _age(pushed, now):
    d = (now - pushed).days
    return d, ("today" if d == 0 else f"{d}d ago")


def _slab(t, cx, cy, hl):
    """One isometric layer: top face rhombus plus a 6px edge."""
    hw, hh, th = 56, 13, 6
    edge = (f'<path d="M{cx - hw} {cy}L{cx} {cy + hh}L{cx + hw} {cy}V{cy + th}L{cx} {cy + hh + th}L{cx - hw} {cy + th}Z" '
            f'fill="{t["grid_major"]}" stroke="{t["muted"]}" stroke-width="1"/>')
    top = (f'<path d="M{cx - hw} {cy}L{cx} {cy - hh}L{cx + hw} {cy}L{cx} {cy + hh}Z" fill="{t["bg"]}" '
           f'stroke="{t["accent"] if hl else t["ink"]}" stroke-width="{1.6 if hl else 1.1}"/>')
    tint = f'<path d="M{cx - hw} {cy}L{cx} {cy - hh}L{cx + hw} {cy}L{cx} {cy + hh}Z" fill="{t["accent"]}" opacity=".18"/>' if hl else ""
    return edge + top + tint


def render_cards(theme, pushed_by_name, now):
    t = THEMES[theme]
    cw, ch, gap = 360, 196, 30
    h = 88 + 2 * ch + gap + 74
    o = _open(t, W, h, "Flagship projects drawn as exploded views of their layers")
    o.append(_title(t, "FIG. 05 / FLAGSHIPS / EXPLODED VIEWS"))
    for i, (name, line, layers) in enumerate(CARDS):
        x = 56 + (i % 3) * (cw + gap - 4)
        y = 88 + (i // 3) * (ch + gap)
        p = pushed_by_name.get(name)
        days, label = _age(p, now) if p else (999, "n/a")
        dot = t["accent"] if days <= 14 else t["muted"] if days <= 90 else t["line"]
        o.append(f'<g class="fade" style="animation-delay:{i * 0.12:.2f}s">')
        o.append(f'<rect x="{x}.5" y="{y}.5" width="{cw}" height="{ch}" fill="{t["bg"]}" stroke="{t["line"]}"/>')
        o.append(f'<path d="M{x} {y + 18}V{y}H{x + 18}" fill="none" stroke="{t["accent"]}" stroke-width="2"/>')
        o.append(f'<text x="{x + 22}" y="{y + 40}" font-size="22" font-weight="700" fill="{t["ink"]}">{escape(name)}</text>')
        o.append(f'<text x="{x + 22}" y="{y + 62}" font-size="12" fill="{t["muted"]}">{escape(line)}</text>')
        lab = f"last push {label}"
        o.append(f'<circle cx="{x + cw - 16 - len(lab) * 6.6 - 10:.0f}" cy="{y + 25}" r="4" fill="{dot}"/>'
                 f'<text x="{x + cw - 16}" y="{y + 29}" text-anchor="end" font-size="11" fill="{t["muted"]}">{lab}</text>')
        o.append("</g>")
        # exploded stack: guides first, then slabs bottom-up so upper layers overlap lower ones
        sx, ys = x + 78, [y + 98, y + 132, y + 166]
        o.append(f'<path d="M{sx - 56} {ys[0]}V{ys[2]} M{sx + 56} {ys[0]}V{ys[2]} M{sx} {ys[0] + 13}V{ys[2] + 13}" '
                 f'stroke="{t["muted"]}" stroke-width=".8" stroke-dasharray="2 3" opacity=".7"/>')
        delay = .3 + i * .12
        for k in (2, 1, 0):
            shift = (1 - k) * (ys[1] - ys[0])  # collapsed onto the middle layer, then pulled apart
            anim = (f'<animateTransform attributeName="transform" type="translate" from="0 {shift}" to="0 0" '
                    f'begin="{delay:.2f}s" dur=".9s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .3 1"/>') if shift else ""
            o.append(f'<g transform="translate(0 {shift})">{_slab(t, sx, ys[k], k == 0)}{anim}</g>' if shift else _slab(t, sx, ys[k], False))
        for k, (role, lbl) in enumerate(layers):
            ly = ys[k]
            o.append(f'<g class="fade" style="animation-delay:{delay + .8:.2f}s">'
                     f'<path d="M{sx + 56} {ly}H{x + 160}" stroke="{t["muted"]}" stroke-width=".8"/><circle cx="{sx + 56}" cy="{ly}" r="2" fill="{t["muted"]}"/>'
                     f'<text x="{x + 168}" y="{ly + 4}" font-size="9" letter-spacing="1" fill="{t["muted"]}">{role} '
                     f'<tspan font-size="11" fill="{t["accent"] if k == 0 else t["ink"]}">{escape(lbl)}</tspan></text></g>')
    return _close(o, t, h, "05")


# --------------------------------------------------------------------------- parts list (assemblies)

ASSEMBLIES = [
    ("A", "AGENT PLATFORMS & DEV TOOLING", [
        ("personas", "https://github.com/xkazm04/personas", "TAURI 2 · REACT 19 · SQLITE", "Desktop app to build AI agents, wire them to tools and run teams of them"),
        ("vibeman", "https://github.com/xkazm04/vibeman", "NEXT.JS 16 · CLAUDE CODE · OLLAMA", "Project control room: up to four concurrent Claude Code sessions"),
        ("pof", "https://github.com/xkazm04/pof", "NEXT.JS · UNREAL ENGINE 5", "UE5 C++ companion: checklists, quality evals, embedded Claude Code"),
        ("ascent", "https://github.com/xkazm04/ascent", "TYPESCRIPT", "Scores how AI-native a team is, 0-100 across nine weighted dimensions"),
    ]),
    ("B", "RUST INFRASTRUCTURE", [
        ("lighttrack", "https://github.com/xkazm04/lighttrack", "RUST · SQLITE / POSTGRES / FIRESTORE", "Self-hosted LLM observability with LLM-as-judge scoring, one container"),
        ("pumper", "https://github.com/xkazm04/pumper", "RUST · SQLITE", "One-binary scraper, durable job queue, HTTP > browser > Claude Code"),
    ]),
    ("C", "HANDS-FIRST VR / META VR START 2026", [
        ("garden-vr", "https://github.com/xkazm04/garden-vr", "UNITY · META QUEST", "Two calm daily-ritual apps that grow a living garden from real habits"),
        ("mage-arena", "https://github.com/xkazm04/mage-arena", "UNREAL ENGINE 5 · META QUEST", "Seated spell duel played with your hands"),
    ]),
    ("D", "MEDIA & DATA", [
        ("gravitone", "https://github.com/xkazm04/gravitone", "PYTHON · ARM", "CPU-only TTS with voice cloning: 4.26x realtime on Graviton4"),
        ("stat-reel", "https://github.com/xkazm04/stat-reel", "TYPESCRIPT", "Licensed sports data turned into 1-3 minute data-viz videos"),
        ("systedo-case", "https://github.com/xkazm04/systedo-case", "TYPESCRIPT", "Ad intelligence on your machine: Google Ads, Sklik, Meta, TikTok"),
        ("MiSu", "https://www.youtube.com/watch?v=Kam3LOzbPoI", "PROMPT ENGINEERING", "AI-generated music album. I told it to make great music, and it does"),
    ]),
    ("E", "CIVIC & EXPERIMENTS", [
        ("politicas", "https://github.com/xkazm04/politicas", "TYPESCRIPT · CS / EN", "Czech politics: MP scoring, votes, money ties and budgets on one graph"),
        ("athena-portable", "https://github.com/xkazm04/athena-portable", "PYTHON · HACKATHON", "Personal agent that works inside your web apps and asks before it acts"),
        ("paypal", "https://github.com/xkazm04/paypal", "RUST · HACKATHON", "The Table: agent-to-agent haggling over PayPal"),
    ]),
]


def render_parts(theme):
    t = THEMES[theme]
    row = 24
    n = sum(1 + len(items) for _, _, items in ASSEMBLIES)
    top = 92
    body = top + 30
    bottom = body + n * row
    h = bottom + 92
    cols = [(72, "ITEM"), (124, "PART"), (318, "MATERIAL"), (590, "NOTE")]
    o = _open(t, W, h, "Parts list: every project grouped into sub-assemblies, with material and note")
    o.append(_title(t, "FIG. 06 / PARTS LIST"))
    o.append(f'<text x="{W - 56}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">QTY {sum(len(i) for _, _, i in ASSEMBLIES)} / links below</text>')
    o.append(f'<rect x="56.5" y="{top}.5" width="{W - 112}" height="{bottom - top}" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.2"/>')
    o.append(f'<path d="M56 {body}.5H{W - 56}" stroke="{t["ink"]}" stroke-width="1.2"/>')
    for x, label in cols:
        o.append(f'<text x="{x}" y="{top + 20}" font-size="10" letter-spacing="2" fill="{t["muted"]}">{label}</text>')
    for x, _ in cols[1:]:
        o.append(f'<path d="M{x - 12}.5 {top}V{bottom}" stroke="{t["line"]}"/>')
    y, item = body, 0
    for gi, (letter, gname, items) in enumerate(ASSEMBLIES):
        o.append(f'<rect x="57" y="{y + 1}" width="{W - 114}" height="{row - 1}" fill="{t["grid_major"]}"/>'
                 f'<text x="72" y="{y + 16}" font-size="11" font-weight="700" letter-spacing="2" fill="{t["accent"]}">{letter}</text>'
                 f'<text x="124" y="{y + 16}" font-size="10" letter-spacing="2" fill="{t["ink"]}">SUB-ASSEMBLY / {escape(gname)}</text>')
        y += row
        for name, _, material, note in items:
            item += 1
            o.append(f'<g class="fade" style="animation-delay:{item * .04:.2f}s">'
                     f'<path d="M56 {y + row}.5H{W - 56}" stroke="{t["line"]}" stroke-dasharray="2 3"/>'
                     f'<text x="72" y="{y + 16}" font-size="11" fill="{t["accent"]}">{item:02d}</text>'
                     f'<text x="124" y="{y + 16}" font-size="12" font-weight="700" fill="{t["ink"]}">{escape(name)}</text>'
                     f'<text x="318" y="{y + 16}" font-size="9" letter-spacing="1" fill="{t["muted"]}">{escape(material)}</text>'
                     f'<text x="590" y="{y + 16}" font-size="11" fill="{t["ink"]}">{escape(note)}</text></g>')
            y += row
    return _close(o, t, h, "06")


def parts_links():
    """README companion to the parts list: numbered links, one line per sub-assembly."""
    lines, item = [], 0
    for letter, _, items in ASSEMBLIES:
        links = []
        for name, url, _, _ in items:
            item += 1
            links.append(f'<a href="{url}">{item:02d} {escape(name)}</a>')
        lines.append(f"<b>{letter}</b> &nbsp;" + " · ".join(links))
    return '<p align="center"><sub>\n' + "<br/>\n".join(lines) + "\n</sub></p>"


# --------------------------------------------------------------------------- timeline

def render_timeline(theme, repos, lang_color, now):
    """repos: [(name, pushed_dt, language)] newest first."""
    t = THEMES[theme]
    h = 354
    o = _open(t, W, h, "Timeline of recent repository pushes")
    o.append(_title(t, "FIG. 04 / PUSH TIMELINE / LAST 12 MONTHS"))
    x0, x1, ay = 70, 1130, 190
    span = 365.0
    o.append(f'<path d="M{x0} {ay}H{x1}" stroke="{t["ink"]}" stroke-width="1.5"/>')
    # month ticks
    for m in range(13):
        frac = m / 12
        x = x0 + frac * (x1 - x0)
        mo = ((now.month - 12 + m - 1) % 12) + 1
        o.append(f'<path d="M{x:.0f} {ay - 6}V{ay + 6}" stroke="{t["muted"]}"/>')
        o.append(f'<text x="{x:.0f}" y="{ay + 24}" text-anchor="middle" font-size="10" fill="{t["muted"]}">{datetime(2000, mo, 1):%b}</text>')
    seen = {}
    for name, p, lang in repos:
        age = (now - p).days
        if age > span:
            continue
        x = x1 - (age / span) * (x1 - x0)
        k = int(x // 18)
        stack = seen.get(k, 0)
        seen[k] = stack + 1
        x -= (stack // 5) * 11  # wrap tall stacks into neighbouring columns
        y = ay - 14 - (stack % 5) * 13
        col = lang_color.get(lang, t["muted"])
        o.append(f'<path d="M{x:.0f} {ay}V{y}" stroke="{col}" stroke-width="1" opacity=".6"/>')
        o.append(f'<circle class="fade" style="animation-delay:{min(stack, 8) * .1:.1f}s" cx="{x:.0f}" cy="{y}" r="4.5" fill="{col}"/>')
    # newest pushes cluster on the right edge, so name them in one callout line
    recent = " · ".join(escape(n) for n, _, _ in repos[:6])
    o.append(f'<path d="M{x1} {ay + 34}V262H{x1 - 24}" stroke="{t["line"]}" fill="none"/>')
    o.append(f'<text x="{x1 - 34}" y="266" text-anchor="end" font-size="12" fill="{t["ink"]}"><tspan fill="{t["accent"]}">LATEST</tspan>  {recent}</text>')
    # legend
    langs = []
    for _, _, l in repos:
        if l not in langs:
            langs.append(l)
    lx = 56
    for l in langs[:6]:
        o.append(f'<circle cx="{lx + 5}" cy="96" r="5" fill="{lang_color.get(l, t["muted"])}"/>'
                 f'<text x="{lx + 16}" y="100" font-size="11" fill="{t["muted"]}">{escape(l)}</text>')
        lx += 30 + len(l) * 8
    o.append(f'<text x="{x1}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">{len(repos)} repos pushed</text>')
    return _close(o, t, h, "04")


# --------------------------------------------------------------------------- pulse dashboard

def render_pulse(theme, weeks, langs):
    t = THEMES[theme]
    h = 388
    o = _open(t, W, h, "Weekly contribution pulse and language donut")
    o.append(_title(t, "FIG. 03 / PULSE"))
    wk = [sum(w) for w in weeks][-26:]
    mx = max(wk) or 1
    cur = wk[-1] if wk else 0
    avg = sum(wk) / max(len(wk), 1)
    best = max(wk) if wk else 0
    active = sum(1 for w in weeks[-26:] for c in w if c)
    tiles = [("THIS WEEK", cur), ("AVG / WEEK", f"{avg:.0f}"), ("BEST WEEK", best), ("ACTIVE DAYS 26W", active)]
    for i, (lab, val) in enumerate(tiles):
        x = 56 + i * 150
        o.append(f'<path d="M{x} 100H{x + 128}" stroke="{t["line"]}"/>'
                 f'<text x="{x}" y="122" font-size="10" letter-spacing="2" fill="{t["muted"]}">{lab}</text>'
                 f'<text x="{x}" y="156" font-size="30" font-weight="700" fill="{t["ink"]}">{val}</text>')
    # bars
    bx, by, bh, bw, bg = 56, 320, 120, 18, 5
    bars_end = bx + len(wk) * (bw + bg)
    o.append(f'<path d="M{bx} {by}H{bars_end}" stroke="{t["ink"]}"/>')
    for i, v in enumerate(wk):
        hh = max(2, v / mx * bh)
        col = t["accent"] if i == len(wk) - 1 else t["heat"][3] if v >= avg else t["heat"][1]
        o.append(f'<rect class="fade" style="animation-delay:{i * .03:.2f}s" x="{bx + i * (bw + bg)}" y="{by - hh:.0f}" width="{bw}" height="{hh:.0f}" fill="{col}"/>')
    o.append(f'<path d="M{bx} {by - avg / mx * bh:.0f}H{bars_end}" stroke="{t["muted"]}" stroke-dasharray="4 4"/>')
    if best:
        o.append(vdim(t, bars_end + 18, by - bh, by, f"BEST {best}", ext=bars_end + 2))
    o.append(f'<text x="{bx}" y="{by + 20}" font-size="10" fill="{t["muted"]}">26 weeks of contributions, dashed = average</text>')
    # donut
    cx, cy, r, sw = 930, 196, 80, 26
    circ = 2 * math.pi * r
    off = 0.0
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["grid"]}" stroke-width="{sw}"/>')
    for i, (name, pct) in enumerate(langs):
        seg = circ * pct / 100
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["langs"][i]}" stroke-width="{sw}" '
                 f'stroke-dasharray="{max(seg - 2, 0.5):.1f} {circ:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        off += seg
        ly = 112 + i * 24
        o.append(f'<rect x="1040" y="{ly - 9}" width="10" height="10" fill="{t["langs"][i]}"/>'
                 f'<text x="1058" y="{ly}" font-size="12" fill="{t["ink"]}">{escape(name)} <tspan fill="{t["muted"]}">{pct:.0f}%</tspan></text>')
    o.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="12" letter-spacing="2" fill="{t["muted"]}">CODE MIX</text>')
    return _close(o, t, h, "03")


# --------------------------------------------------------------------------- VR corner (concept art)

# Downscaled art from the garden-vr and mage-arena repos, kept in assets/vr. SVGs shown
# through <img> can't load external files, so each frame is inlined as a data URI.
VR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "vr")
VR_FRAMES = [("garden-vr", "Unity / Meta Quest", "frame 01 / what to grow", "garden-01.jpg"),
             ("garden-vr", "Unity / Meta Quest", "frame 02 / sundial break", "garden-02.jpg"),
             ("mage-arena", "UE5 / Meta Quest", "storyboard / seated duel", "arena-01.jpg"),
             ("mage-arena", "UE5 / Meta Quest", "concept / unblockable", "arena-02.jpg")]


def _data_uri(name):
    with open(os.path.join(VR_DIR, name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")


def render_vr(theme):
    t = THEMES[theme]
    fw, fh = 262, 147
    y = 92
    h = y + fh + 152
    o = _open(t, W, h, "VR corner: concept frames from garden-vr and mage-arena")
    o.append(_title(t, "FIG. 07 / HANDS-FIRST VR"))
    o.append(f'<text x="{W - 56}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">CONCEPT FRAMES / Meta VR Start 2026</text>')
    for i, (name, sub, cap, img) in enumerate(VR_FRAMES):
        x = 56 + i * (fw + 30)
        o.append(f'<image class="fade" style="animation-delay:{i * .12:.2f}s" x="{x}" y="{y}" width="{fw}" height="{fh}" '
                 f'preserveAspectRatio="xMidYMid slice" href="{_data_uri(img)}"/>')
        o.append(f'<rect x="{x}.5" y="{y}.5" width="{fw}" height="{fh}" fill="none" stroke="{t["ink"]}" stroke-width="1.2"/>')
        o.append(f'<path d="M{x} {y + 16}V{y}H{x + 16}" stroke="{t["accent"]}" stroke-width="2" fill="none"/>')
        o.append(f'<text x="{x}" y="{y + fh + 26}" font-size="14" font-weight="700" fill="{t["ink"]}">{name}</text>')
        o.append(f'<text x="{x}" y="{y + fh + 44}" font-size="11" fill="{t["muted"]}">{sub}</text>')
        o.append(f'<text x="{x}" y="{y + fh + 62}" font-size="10" letter-spacing="1" fill="{t["accent"]}">{escape(cap.upper())}</text>')
    return _close(o, t, h, "07")


# --------------------------------------------------------------------------- toolbox stencil

# (category, cut-out shape, [(monogram, label, weight 1-3)]); weight sets the cut-out size.
TOOLBOX = [
    ("LANGUAGES", "circle", [("TS", "TypeScript", 3), ("Rs", "Rust", 3), ("Py", "Python", 2), ("C++", "C++", 1), ("C#", "C#", 1)]),
    ("APPS", "square", [("Re", "React 19", 3), ("Nx", "Next.js 16", 3), ("Ta", "Tauri 2", 2), ("Tw", "Tailwind v4", 2)]),
    ("DATA", "hex", [("Sq", "SQLite", 3), ("Pg", "PostgreSQL", 2), ("Fs", "Firestore", 1)]),
    ("AI", "diamond", [("CC", "Claude Code", 3), ("MC", "MCP", 2), ("LJ", "LLM-as-judge", 2), ("Ol", "Ollama", 1)]),
    ("XR", "visor", [("UE", "Unreal 5", 2), ("Un", "Unity", 2), ("MQ", "Meta Quest", 2)]),
]


def _cutout(kind, cx, cy, s, attrs):
    """Stencil hole of the given kind centred on (cx, cy); returns (svg element, half width)."""
    if kind == "circle":
        return f'<circle cx="{cx}" cy="{cy}" r="{s}" {attrs}/>', s
    if kind == "square":
        return f'<rect x="{cx - s}" y="{cy - s}" width="{2 * s}" height="{2 * s}" rx="6" {attrs}/>', s
    if kind == "hex":
        r = s * 1.1
        pts = " ".join(f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60))
        return f'<polygon points="{pts}" {attrs}/>', r
    if kind == "diamond":
        r = s * 1.25
        return f'<polygon points="{cx},{cy - r} {cx + r},{cy} {cx},{cy + r} {cx - r},{cy}" {attrs}/>', r
    rx = s * 1.4
    return f'<rect x="{cx - rx:.1f}" y="{cy - s * .75:.1f}" width="{2 * rx:.1f}" height="{s * 1.5:.1f}" rx="{s * .75:.1f}" {attrs}/>', rx


def render_toolbox(theme):
    t = THEMES[theme]
    px, py, pw = 56, 92, W - 112
    rh = 72
    ph = len(TOOLBOX) * rh + 52
    h = py + ph + 74
    o = _open(t, W, h, "Toolbox drawn as a drafting stencil: languages, apps, data, AI and XR; bigger cut-outs are used more")
    o.append(_title(t, "FIG. 09 / TOOLBOX STENCIL"))
    holes, outlines, labels = [], [], []
    for r, (cat, kind, items) in enumerate(TOOLBOX):
        cy = py + 44 + r * rh
        labels.append(f'<text x="{px + 26}" y="{cy + 4}" font-size="11" letter-spacing="2" fill="{t["accent"]}">{cat}</text>')
        for i, (mono, label, wgt) in enumerate(items):
            cx = px + 214 + i * 182
            s = 11 + 4 * wgt
            hole, half = _cutout(kind, cx, cy, s, 'fill="#000"')
            holes.append(hole)
            delay = f'style="animation-delay:{(r * 5 + i) * .04:.2f}s"'
            shade, _ = _cutout(kind, cx + 1.5, cy + 1.5, s, f'fill="none" stroke="{t["accent"]}" stroke-opacity=".4" stroke-width="1.5"')
            edge, _ = _cutout(kind, cx, cy, s, f'fill="none" stroke="{t["ink"]}" stroke-width="1.2"')
            outlines.append(f'<g class="fade" {delay}>{shade}{edge}'
                            f'<text x="{cx}" y="{cy + 4 + wgt}" text-anchor="middle" font-size="{10 + wgt}" font-weight="700" fill="{t["ink"]}">{escape(mono)}</text>'
                            f'<text x="{cx + half + 12:.0f}" y="{cy + 4}" font-size="13" font-weight="{700 if wgt == 3 else 400}" '
                            f'fill="{t["ink"] if wgt > 1 else t["muted"]}">{escape(label)}</text></g>')
    hang = (px + pw - 34, py + 30)
    holes.append(f'<circle cx="{hang[0]}" cy="{hang[1]}" r="10" fill="#000"/>')
    # translucent plate with the holes masked out, so the drafting grid shows through them
    o.append(f'<mask id="cut"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#fff"/>{"".join(holes)}</mask>')
    o.append(f'<rect x="{px}.5" y="{py}.5" width="{pw}" height="{ph}" rx="16" fill="{t["accent"]}" fill-opacity=".08" '
             f'stroke="{t["accent"]}" stroke-opacity=".55" stroke-width="1.4" mask="url(#cut)"/>')
    o.append(f'<rect x="{px + 5}.5" y="{py + 5}.5" width="{pw - 10}" height="{ph - 10}" rx="12" fill="none" stroke="{t["ink"]}" stroke-opacity=".12"/>')
    o.append(f'<circle cx="{hang[0]}" cy="{hang[1]}" r="10" fill="none" stroke="{t["ink"]}" stroke-width="1.2"/>')
    # millimetre scale along the top edge
    ticks = "".join(f"M{x} {py + 5}v{8 if (x - px) % 50 == 0 else 4}" for x in range(px + 200, px + pw - 80, 10))
    o.append(f'<path d="{ticks}" stroke="{t["muted"]}" stroke-width=".8"/>')
    o.extend(labels)
    o.extend(outlines)
    o.append(f'<text x="{px + 26}" y="{py + ph - 18}" font-size="10" letter-spacing="1" fill="{t["muted"]}">CUT-OUT SIZE = HOW OFTEN I REACH FOR IT</text>')
    return _close(o, t, h, "09")


# --------------------------------------------------------------------------- civic spotlight

# Real figures, from the politicas README (deterministic scorers, pending_review).
CIVIC = {
    "people": 7045, "mps": 207, "ballots": 406_000,
    "sweep_mps": 73, "companies": 196, "contracts": 2287, "czk_bn": 19.76, "laws": 24774,
}


def render_civic(theme):
    t = THEMES[theme]
    h = 400
    c = CIVIC
    o = _open(t, W, h, "politicas: Czech public-accountability knowledge graph in numbers")
    o.append(_title(t, "FIG. 08 / SPOTLIGHT / POLITICAS"))
    o.append(f'<text x="{W - 56}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">source: Hlidac statu, ARES, Registr smluv, psp.cz / all links pending_review</text>')
    o.append(f'<text x="56" y="112" font-size="26" font-weight="700" fill="{t["ink"]}">Follow the money, with receipts</text>')
    o.append(f'<text x="56" y="136" font-size="12" fill="{t["muted"]}">Chamber sweep: MP to company to public contract, joined on IC, human-gated.</text>')
    o.append(f'<text x="56" y="154" font-size="10" fill="{t["muted"]}">bar length is log scale; numbers are exact</text>')
    # funnel bars (log-ish scaled for readability, true values printed)
    stages = [("PEOPLE IN GRAPH", c["people"], f'{c["people"]:,}'),
              ("CURRENT MPs", c["mps"], f'{c["mps"]}'),
              ("MPs WITH COMPANY TIES", c["sweep_mps"], f'{c["sweep_mps"]}'),
              ("COMPANIES", c["companies"], f'{c["companies"]}'),
              ("PUBLIC CONTRACTS", c["contracts"], f'{c["contracts"]:,}')]
    mxl = math.log10(c["people"])
    wd = 0
    for i, (lab, v, txt) in enumerate(stages):
        y = 174 + i * 30
        wd = 520 * math.log10(v) / mxl
        col = t["accent"] if i >= 2 else t["heat"][3]
        o.append(f'<text x="56" y="{y + 12}" font-size="10" letter-spacing="1" fill="{t["muted"]}">{lab}</text>')
        o.append(f'<rect class="fade" style="animation-delay:{i * .12:.2f}s" x="250" y="{y}" width="{wd:.0f}" height="16" fill="{col}" opacity="{1 if i >= 2 else .75}"/>')
        o.append(f'<text x="{250 + wd + 8:.0f}" y="{y + 13}" font-size="13" font-weight="700" fill="{t["ink"]}">{txt}</text>')
    last = 174 + 4 * 30 + 16
    o.append(dim(t, 250, round(250 + wd), last + 22, f'{c["contracts"]:,} CONTRACTS = ~{c["czk_bn"]:.2f}B CZK', ext=last + 2))
    # big stats
    big = [(f'~{c["czk_bn"]:.2f}B', "CZK in contracts traced"), (f'{c["ballots"] // 1000}k', "roll-call ballots"), (f'{c["laws"]:,}', "laws in e-Sbirka registry")]
    for i, (v, lab) in enumerate(big):
        y = 194 + i * 40
        o.append(f'<text x="880" y="{y}" font-size="30" font-weight="700" fill="{t["accent"] if i == 0 else t["ink"]}">{v}</text>'
                 f'<text x="880" y="{y + 16}" font-size="11" fill="{t["muted"]}">{lab}</text>')
    o.append(f'<path d="M840 164V304" stroke="{t["line"]}"/>')
    return _close(o, t, h, "08")


# --------------------------------------------------------------------------- section dividers

def render_divider(theme, num, total=4):
    """Ruler strip between README sections, drawn on a transparent background so it sits on
    GitHub's page colour. num is "01".."04" or "END"."""
    t = THEMES[theme]
    w, h = W, 48
    x0, x1, y = 76, w - 150, 30
    label = "END" if num == "END" else f"§ {num}"
    right = "END OF SHEET" if num == "END" else f"SECTION {num} / {total:02d}"
    ticks = "".join(f"M{x} {y}v-{12 if (x - x0) % 120 == 0 else 7 if (x - x0) % 60 == 0 else 4}" for x in range(x0, x1 + 1, 12))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(right.lower())}">', STYLE,
         f'<text x="0" y="{y + 5}" font-size="15" font-weight="700" fill="{t["accent"]}">{label}</text>',
         f'<path class="draw" d="M{x0} {y}H{x1}" stroke="{t["muted"]}" stroke-width="1"/>',
         f'<path d="{ticks}" stroke="{t["muted"]}" stroke-width="1"/>',
         f'<text x="{w}" y="{y + 5}" text-anchor="end" font-size="11" letter-spacing="2" fill="{t["muted"]}">{right}</text>',
         # a reading-head marker sliding along the scale
         f'<g><path d="M0 {y - 16}l-5 -8h10z" fill="{t["accent"]}"/><path d="M0 {y - 16}V{y + 4}" stroke="{t["accent"]}" stroke-width="1"/>'
         f'<animateTransform attributeName="transform" type="translate" values="{x0} 0;{x1} 0;{x0} 0" dur="14s" repeatCount="indefinite" '
         f'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></g>',
         "</svg>\n"]
    return "\n".join(o)
