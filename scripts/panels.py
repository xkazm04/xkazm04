"""Extra profile panels in the drafting-sheet look: architecture, project cards,
build-log timeline, pulse dashboard, VR corner, toolbox strip, civic spotlight.

Each renderer returns an SVG string for a theme from brand.THEMES. Dynamic ones
take data from update_readme.py; the rest are static.
"""

from datetime import datetime
from html import escape

from brand import STYLE, THEMES, _sheet

W = 1200


def _open(t, w, h, label, extra=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">',
            STYLE, extra, _sheet(t, w, h)]


def _title(t, text, y=64):
    return f'<text x="56" y="{y}" font-size="13" letter-spacing="3" fill="{t["accent"]}">{escape(text)}</text>'


def _arrow(t, x1, y1, x2, y2, cls="", color=None, dash=""):
    c = color or t["muted"]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path class="{cls}" d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="1.5" fill="none"{d}/>'
            f'<path d="M{x2} {y2}l-8 -4v8z" fill="{c}" transform="rotate({_ang(x1, y1, x2, y2)} {x2} {y2})"/>')


def _ang(x1, y1, x2, y2):
    import math
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


# --------------------------------------------------------------------------- architecture

def render_architecture(theme):
    t = THEMES[theme]
    h = 330
    o = _open(t, W, h, "Local-first architecture: your machine holds SQLite, agents propose, a human approval gate decides")
    o.append(_title(t, "FIG. 02 / LOCAL-FIRST ARCHITECTURE"))
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
    # animated token travelling the pipeline
    o.append(f'<circle r="5" fill="{t["accent"]}" class="token"><animateMotion dur="5s" repeatCount="indefinite" path="M204 200L330 190L480 190L570 190L700 190L790 190"/></circle>')
    # outside: only on explicit send
    o.append(f'<rect x="884.5" y="150.5" width="260" height="80" fill="none" stroke="{t["line"]}" stroke-dasharray="4 4"/>')
    o.append(f'<text x="1014" y="186" text-anchor="middle" font-size="14" fill="{t["ink"]}">cloud / third parties</text>')
    o.append(f'<text x="1014" y="208" text-anchor="middle" font-size="11" fill="{t["muted"]}">only what you send</text>')
    o.append(f'<path d="M830 190H884" stroke="{t["accent"]}" stroke-width="1.5" stroke-dasharray="3 5"/>')
    o.append(f'<text x="857" y="180" text-anchor="middle" font-size="16" fill="{t["accent"]}">?</text>')
    o.append(f'<text x="56" y="312" font-size="11" fill="{t["muted"]}">Agents do the work, people approve it. Nothing leaves unless you send it.</text>')
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- project cards

CARDS = [
    ("personas", "AI agent desktop app", ["TAURI 2", "REACT 19", "SQLITE"]),
    ("vibeman", "Control room for Claude Code", ["NEXT.JS 16", "OLLAMA"]),
    ("lighttrack", "LLM observability + judge", ["RUST", "SQLITE / PG"]),
    ("pumper", "Local-first scraping service", ["RUST", "SQLITE QUEUE"]),
    ("ascent", "0-100 AI-maturity score", ["TYPESCRIPT", "9 DIMENSIONS"]),
    ("politicas", "Czech politics accountability", ["TYPESCRIPT", "CS / EN"]),
]


def _age(pushed, now):
    d = (now - pushed).days
    return d, ("today" if d == 0 else f"{d}d ago")


def render_cards(theme, pushed_by_name, now):
    t = THEMES[theme]
    cw, ch, gap = 360, 150, 30
    h = 92 + 2 * ch + gap + 40
    o = _open(t, W, h, "Flagship project cards")
    o.append(_title(t, "FIG. 03 / FLAGSHIPS"))
    for i, (name, line, chips) in enumerate(CARDS):
        x = 56 + (i % 3) * (cw + gap - 4)
        y = 88 + (i // 3) * (ch + gap)
        p = pushed_by_name.get(name)
        days, label = _age(p, now) if p else (999, "n/a")
        dot = t["accent"] if days <= 14 else t["muted"] if days <= 90 else t["line"]
        o.append(f'<g class="fade" style="animation-delay:{i * 0.12:.2f}s">')
        o.append(f'<rect x="{x}.5" y="{y}.5" width="{cw}" height="{ch}" fill="{t["bg"]}" stroke="{t["line"]}"/>')
        o.append(f'<path d="M{x} {y + 18}V{y}H{x + 18}" fill="none" stroke="{t["accent"]}" stroke-width="2"/>')
        o.append(f'<text x="{x + 22}" y="{y + 44}" font-size="22" font-weight="700" fill="{t["ink"]}">{escape(name)}</text>')
        o.append(f'<text x="{x + 22}" y="{y + 70}" font-size="12" fill="{t["muted"]}">{escape(line)}</text>')
        cx = x + 22
        for c in chips:
            cwid = 9 + len(c) * 7.2
            o.append(f'<rect x="{cx}" y="{y + 88}" width="{cwid:.0f}" height="22" fill="none" stroke="{t["line"]}"/>'
                     f'<text x="{cx + 6}" y="{y + 103}" font-size="10" letter-spacing="1" fill="{t["ink"]}">{c}</text>')
            cx += cwid + 8
        o.append(f'<circle cx="{x + 26}" cy="{y + 132}" r="4" fill="{dot}"/>'
                 f'<text x="{x + 38}" y="{y + 136}" font-size="11" fill="{t["muted"]}">last push {label}</text>')
        o.append("</g>")
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- timeline

def render_timeline(theme, repos, lang_color, now):
    """repos: [(name, pushed_dt, language)] newest first."""
    t = THEMES[theme]
    h = 310
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
        if m < 13:
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
    o.append(f'<path d="M{x1} {ay + 34}V270H{x1 - 24}" stroke="{t["line"]}" fill="none"/>')
    o.append(f'<text x="{x1 - 34}" y="274" text-anchor="end" font-size="12" fill="{t["ink"]}"><tspan fill="{t["accent"]}">LATEST</tspan>  {recent}</text>')
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
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- pulse dashboard

def render_pulse(theme, weeks, langs):
    t = THEMES[theme]
    h = 360
    o = _open(t, W, h, "Weekly contribution pulse and language donut")
    o.append(_title(t, "FIG. 05 / PULSE"))
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
    o.append(f'<path d="M{bx} {by}H{bx + len(wk) * (bw + bg)}" stroke="{t["ink"]}"/>')
    for i, v in enumerate(wk):
        hh = max(2, v / mx * bh)
        col = t["accent"] if i == len(wk) - 1 else t["heat"][3] if v >= avg else t["heat"][1]
        o.append(f'<rect class="fade" style="animation-delay:{i * .03:.2f}s" x="{bx + i * (bw + bg)}" y="{by - hh:.0f}" width="{bw}" height="{hh:.0f}" fill="{col}"/>')
    o.append(f'<path d="M{bx} {by - avg / mx * bh:.0f}H{bx + len(wk) * (bw + bg)}" stroke="{t["muted"]}" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{bx}" y="{by + 20}" font-size="10" fill="{t["muted"]}">26 weeks of contributions, dashed = average</text>')
    # donut
    import math
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
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- VR corner (synthetic frames)

def _frame_garden(x, y, w, h, t, v=0):
    """Stylised calm garden: dusk sky, hills, glowing plants, floating hand rings."""
    cid = f"g{x}"
    g = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>',
         f'<linearGradient id="{cid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2A41"/><stop offset=".65" stop-color="#C2704A"/><stop offset="1" stop-color="#F4B860"/></linearGradient>',
         f'<g clip-path="url(#{cid})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{cid}s)"/>',
         f'<circle cx="{x + w * (.72 - .4 * v)}" cy="{y + h * (.48 - .1 * v)}" r="26" fill="#FBE3A8" opacity=".9"/>',
         f'<path d="M{x} {y + h * .72}Q{x + w * .3} {y + h * .52} {x + w * .55} {y + h * .70}T{x + w} {y + h * .64}V{y + h}H{x}Z" fill="#2F4A3A"/>',
         f'<path d="M{x} {y + h * .84}Q{x + w * .4} {y + h * .70} {x + w} {y + h * .82}V{y + h}H{x}Z" fill="#1F3A2C"/>']
    for i, (px, ph) in enumerate([(.18, 40), (.32, 62), (.48, 34), (.63, 70), (.80, 48)][: 5 - v]):
        bx, by = x + w * (px + .05 * v * (i % 2)), y + h * .9
        g.append(f'<path d="M{bx} {by}V{by - ph}" stroke="#7FB77E" stroke-width="2.5"/>')
        g.append(f'<circle cx="{bx}" cy="{by - ph}" r="{7 + i % 3 * 2}" fill="#F7C5D0"/><circle cx="{bx}" cy="{by - ph}" r="3" fill="#FBE3A8"/>')
    for i in range(14):
        g.append(f'<circle cx="{x + 14 + (i * 53) % (w - 28)}" cy="{y + 20 + (i * 37) % int(h * .5)}" r="1.4" fill="#FBE3A8" opacity=".8"/>')
    # hand pinch ring
    hx, hy = x + w * (.44 + .2 * v), y + h * (.56 - .12 * v)
    g.append(f'<circle cx="{hx}" cy="{hy}" r="22" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="3 4" opacity=".85"/>'
             f'<circle cx="{hx}" cy="{hy}" r="4" fill="#FFFFFF"/>')
    g.append("</g>")
    return "".join(g)


def _frame_arena(x, y, w, h, t, v=0):
    """Stylised seated duel: dark arena, glowing rune circle, spell bolts, opponent silhouette."""
    cid = f"a{x}"
    g = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>',
         f'<radialGradient id="{cid}r" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#3B1F5C"/><stop offset="1" stop-color="#0A0712"/></radialGradient>',
         f'<g clip-path="url(#{cid})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{cid}r)"/>']
    for k in range(5):
        g.append(f'<path d="M{x + k * w / 4} {y}V{y + h * .6}" stroke="#2A1844" stroke-width="10"/>')
    cx, cy = x + w / 2, y + h * .8
    for rr, op in [(100, .9), (70, .6)]:
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rr}" ry="{rr * .22}" fill="none" stroke="{"#9B6BFF" if v == 0 else "#FF7A59"}" stroke-width="1.6" opacity="{op}"/>')
    # opponent
    ox, oy = x + w * (.5 + .18 * v), y + h * (.42 + .06 * v)
    g.append(f'<path d="M{ox - 22} {oy + 50}Q{ox} {oy - 6} {ox + 22} {oy + 50}Z" fill="#05030A"/><circle cx="{ox}" cy="{oy - 8}" r="10" fill="#05030A"/>'
             f'<circle cx="{ox - 4}" cy="{oy - 9}" r="1.6" fill="#7DF9FF"/><circle cx="{ox + 4}" cy="{oy - 9}" r="1.6" fill="#7DF9FF"/>')
    # bolts
    g.append(f'<path d="M{x + w * .18} {y + h * .9}L{x + w * .38} {y + h * .62}L{x + w * .30} {y + h * .60}L{ox - 24} {oy + 20}" fill="none" stroke="#7DF9FF" stroke-width="2.5"/>')
    g.append(f'<circle cx="{x + w * .18}" cy="{y + h * .9}" r="9" fill="#7DF9FF" opacity=".35"/><circle cx="{x + w * .18}" cy="{y + h * .9}" r="4" fill="#E8FFFF"/>')
    g.append(f'<path d="M{x + w * .82} {y + h * .9}L{x + w * .66} {y + h * .66}" fill="none" stroke="#FF7A59" stroke-width="2.5" stroke-dasharray="6 4"/>')
    g.append("</g>")
    return "".join(g)


def render_vr(theme):
    t = THEMES[theme]
    h = 380
    o = _open(t, W, h, "VR corner: synthetic example frames for garden-vr and mage-arena")
    o.append(_title(t, "FIG. 06 / HANDS-FIRST VR"))
    o.append(f'<text x="{W - 56}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">SYNTHETIC FRAMES / replace with Quest captures</text>')
    fw, fh = 262, 200
    specs = [("garden-vr", "Unity / Meta Quest", "frame 01 / pinch to plant", _frame_garden),
             ("garden-vr", "Unity / Meta Quest", "frame 02 / daily ritual", _frame_garden),
             ("mage-arena", "UE5 / Meta Quest", "frame 01 / seated duel", _frame_arena),
             ("mage-arena", "UE5 / Meta Quest", "frame 02 / spell cast", _frame_arena)]
    for i, (name, sub, cap, fn) in enumerate(specs):
        x = 56 + i * (fw + 30)
        y = 92
        # offset second frame of each pair so they differ a bit
        o.append(fn(x, y, fw, fh, t, i % 2))
        o.append(f'<rect x="{x}.5" y="{y}.5" width="{fw}" height="{fh}" fill="none" stroke="{t["ink"]}" stroke-width="1.2"/>')
        o.append(f'<path d="M{x} {y + 16}V{y}H{x + 16}" stroke="{t["accent"]}" stroke-width="2" fill="none"/>')
        o.append(f'<text x="{x}" y="{y + fh + 26}" font-size="14" font-weight="700" fill="{t["ink"]}">{name}</text>')
        o.append(f'<text x="{x}" y="{y + fh + 44}" font-size="11" fill="{t["muted"]}">{sub}</text>')
        o.append(f'<text x="{x}" y="{y + fh + 62}" font-size="10" letter-spacing="1" fill="{t["accent"]}">{cap.upper()}</text>')
    o.append("</svg>\n")
    svg = "\n".join(o)
    return svg


# --------------------------------------------------------------------------- toolbox strip

TOOLBOX = [
    ("LANGUAGES", [("TS", "TypeScript"), ("Rs", "Rust"), ("Py", "Python"), ("C++", "C++"), ("C#", "C#")]),
    ("APPS", [("Re", "React 19"), ("Nx", "Next.js 16"), ("Ta", "Tauri 2"), ("Tw", "Tailwind v4")]),
    ("DATA", [("Sq", "SQLite"), ("Pg", "PostgreSQL"), ("Fs", "Firestore")]),
    ("AI", [("CC", "Claude Code"), ("MC", "MCP"), ("LJ", "LLM-as-judge"), ("Ol", "Ollama")]),
    ("XR", [("UE", "Unreal 5"), ("Un", "Unity"), ("MQ", "Meta Quest")]),
]


def render_toolbox(theme):
    t = THEMES[theme]
    rows = len(TOOLBOX)
    h = 92 + rows * 62 + 24
    o = _open(t, W, h, "Toolbox: languages, apps, data, AI and XR tools")
    o.append(_title(t, "FIG. 07 / TOOLBOX"))
    for r, (cat, items) in enumerate(TOOLBOX):
        y = 92 + r * 62
        o.append(f'<text x="56" y="{y + 32}" font-size="11" letter-spacing="2" fill="{t["muted"]}">{cat}</text>')
        for i, (mono, label) in enumerate(items):
            x = 190 + i * 190
            o.append(f'<g class="fade" style="animation-delay:{(r * 5 + i) * .04:.2f}s">'
                     f'<rect x="{x}.5" y="{y}.5" width="44" height="44" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.2"/>'
                     f'<path d="M{x} {y + 8}V{y}H{x + 8}" stroke="{t["accent"]}" stroke-width="2" fill="none"/>'
                     f'<text x="{x + 22}" y="{y + 28}" text-anchor="middle" font-size="15" font-weight="700" fill="{t["accent"]}">{escape(mono)}</text>'
                     f'<text x="{x + 56}" y="{y + 27}" font-size="13" fill="{t["ink"]}">{escape(label)}</text></g>')
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- civic spotlight

# Real figures, from the politicas README (deterministic scorers, pending_review).
CIVIC = {
    "people": 7045, "mps": 207, "ballots": 406_000,
    "sweep_mps": 73, "companies": 196, "contracts": 2287, "czk_bn": 19.76, "laws": 24774,
}


def render_civic(theme):
    t = THEMES[theme]
    h = 340
    c = CIVIC
    o = _open(t, W, h, "politicas: Czech public-accountability knowledge graph in numbers")
    o.append(_title(t, "FIG. 08 / SPOTLIGHT / POLITICAS"))
    o.append(f'<text x="{W - 56}" y="64" text-anchor="end" font-size="11" fill="{t["muted"]}">source: Hlidac statu, ARES, Registr smluv, psp.cz / all links pending_review</text>')
    o.append(f'<text x="56" y="112" font-size="26" font-weight="700" fill="{t["ink"]}">Follow the money, with receipts</text>')
    o.append(f'<text x="56" y="136" font-size="12" fill="{t["muted"]}">Chamber sweep: MP to company to public contract, joined on IC, human-gated.</text>')
    # funnel bars (log-ish scaled for readability, true values printed)
    stages = [("PEOPLE IN GRAPH", c["people"], f'{c["people"]:,}'),
              ("CURRENT MPs", c["mps"], f'{c["mps"]}'),
              ("MPs WITH COMPANY TIES", c["sweep_mps"], f'{c["sweep_mps"]}'),
              ("COMPANIES", c["companies"], f'{c["companies"]}'),
              ("PUBLIC CONTRACTS", c["contracts"], f'{c["contracts"]:,}')]
    import math
    mxl = math.log10(c["people"])
    for i, (lab, v, txt) in enumerate(stages):
        y = 170 + i * 30
        wd = 520 * math.log10(v) / mxl
        col = t["accent"] if i >= 2 else t["heat"][3]
        o.append(f'<text x="56" y="{y + 12}" font-size="10" letter-spacing="1" fill="{t["muted"]}">{lab}</text>')
        o.append(f'<rect class="fade" style="animation-delay:{i * .12:.2f}s" x="250" y="{y}" width="{wd:.0f}" height="16" fill="{col}" opacity="{1 if i >= 2 else .75}"/>')
        o.append(f'<text x="{250 + wd + 8:.0f}" y="{y + 13}" font-size="13" font-weight="700" fill="{t["ink"]}">{txt}</text>')
    o.append(f'<text x="250" y="{170 + 5 * 30 + 4}" font-size="10" fill="{t["muted"]}">bar length is log scale; numbers are exact</text>')
    # big stats
    big = [(f'~{c["czk_bn"]:.2f}B', "CZK in contracts traced"), (f'{c["ballots"] // 1000}k', "roll-call ballots"), (f'{c["laws"]:,}', "laws in e-Sbirka registry")]
    for i, (v, lab) in enumerate(big):
        y = 190 + i * 40
        o.append(f'<text x="880" y="{y}" font-size="30" font-weight="700" fill="{t["accent"] if i == 0 else t["ink"]}">{v}</text>'
                 f'<text x="880" y="{y + 16}" font-size="11" fill="{t["muted"]}">{lab}</text>')
    o.append(f'<path d="M840 160V300" stroke="{t["line"]}"/>')
    o.append("</svg>\n")
    return "\n".join(o)
