"""Brand palette and SVG renderers for the profile: blueprint / drafting-sheet look."""

from html import escape

FONT = "'JetBrains Mono','SFMono-Regular',ui-monospace,Menlo,Consolas,monospace"

THEMES = {
    "dark": {
        "bg": "#0B0D10",
        "grid": "#151A21",
        "grid_major": "#1E252E",
        "ink": "#E7E5E4",
        "muted": "#8B949E",
        "line": "#2D3540",
        "accent": "#F59E0B",
        "heat": ["#161B22", "#4A2F0A", "#8A5208", "#C97A06", "#F59E0B"],
        "langs": ["#F59E0B", "#E2683C", "#7DA7C9", "#D6C6A5", "#8B949E", "#5B6672"],
    },
    "light": {
        "bg": "#F6F3EC",
        "grid": "#ECE6D9",
        "grid_major": "#E0D8C7",
        "ink": "#1C1917",
        "muted": "#6B6459",
        "line": "#CFC6B3",
        "accent": "#B45309",
        "heat": ["#E8E2D4", "#F3D39B", "#E9A94A", "#C9780F", "#8A4B06"],
        "langs": ["#B45309", "#D9573A", "#3F6E94", "#A08B5B", "#6B6459", "#9AA3AD"],
    },
}

STYLE = f"""<style>
  text {{ font-family: {FONT}; }}
  .draw {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 2.6s ease-out .2s forwards; }}
  .cursor {{ animation: blink 1.1s steps(1) infinite; }}
  .fade {{ opacity: 0; animation: fade .8s ease-out forwards; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .draw, .cursor, .fade {{ animation: none; stroke-dashoffset: 0; opacity: 1; }}
  }}
</style>"""


def _sheet(t, w, h):
    """Drafting-paper background: minor/major grid, frame and corner marks."""
    marks = []
    for x, y, dx, dy in [(16, 16, 1, 1), (w - 16, 16, -1, 1), (16, h - 16, 1, -1), (w - 16, h - 16, -1, -1)]:
        marks.append(f'<path d="M{x} {y + 18 * dy}V{y}H{x + 18 * dx}" fill="none" stroke="{t["accent"]}" stroke-width="2"/>')
    return f"""<defs>
  <pattern id="minor" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width="1"/>
  </pattern>
  <pattern id="major" width="120" height="120" patternUnits="userSpaceOnUse">
    <rect width="120" height="120" fill="url(#minor)"/>
    <path d="M120 0H0V120" fill="none" stroke="{t['grid_major']}" stroke-width="1"/>
  </pattern>
</defs>
<rect width="{w}" height="{h}" fill="{t['bg']}"/>
<rect width="{w}" height="{h}" fill="url(#major)"/>
<rect x="16.5" y="16.5" width="{w - 33}" height="{h - 33}" fill="none" stroke="{t['line']}"/>
{''.join(marks)}"""


def render_header(theme, rev):
    t = THEMES[theme]
    w, h = 1200, 280
    cube = "M1010 44L1066 76V140L1010 172L954 140V76Z M954 76L1010 108L1066 76 M1010 108V172"
    hidden = "M954 140L1010 108 M1066 140L1010 108"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="kazii, The Builder">
{STYLE}
{_sheet(t, w, h)}
<text x="70" y="64" font-size="13" letter-spacing="3" fill="{t['muted']}">SHEET 01 / PROFILE</text>
<text x="66" y="156" font-size="104" font-weight="700" fill="{t['ink']}">kazii</text>
<rect class="cursor" x="366" y="80" width="46" height="80" fill="{t['accent']}"/>
<text x="72" y="206" font-size="24" letter-spacing="11" font-weight="600" fill="{t['accent']}">THE BUILDER</text>
<path class="draw" d="M72 228H430 M72 222V234 M430 222V234" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>

<path class="draw" d="{cube}" fill="none" stroke="{t['ink']}" stroke-width="1.6" stroke-linejoin="round"/>
<path class="draw" d="{hidden}" fill="none" stroke="{t['muted']}" stroke-width="1.2" stroke-dasharray="5 5"/>
<circle class="fade" cx="1010" cy="108" r="3.5" fill="{t['accent']}"/>
<path class="draw" d="M1088 44V172 M1082 44H1094 M1082 172H1094" fill="none" stroke="{t['muted']}" stroke-width="1"/>

<g class="fade">
  <rect x="764.5" y="196.5" width="400" height="64" fill="{t['bg']}" stroke="{t['line']}"/>
  <path d="M764.5 228.5H1164.5 M1044.5 196.5V260.5" stroke="{t['line']}"/>
  <text x="778" y="217" font-size="12" fill="{t['muted']}">PROJECT  <tspan fill="{t['ink']}">github.com/xkazm04</tspan></text>
  <text x="778" y="249" font-size="12" fill="{t['muted']}">FOCUS  <tspan fill="{t['ink']}">local-first AI / Rust / XR</tspan></text>
  <text x="1058" y="217" font-size="12" fill="{t['muted']}">REV  <tspan fill="{t['accent']}">{escape(rev)}</tspan></text>
  <text x="1058" y="249" font-size="12" fill="{t['muted']}">SCALE  <tspan fill="{t['ink']}">1:1</tspan></text>
</g>
</svg>
"""


def _levels(days):
    counts = sorted(c for c in days if c > 0)
    if not counts:
        return [1, 1, 1]
    q = lambda p: counts[min(len(counts) - 1, int(len(counts) * p))]
    return [q(0.25), q(0.5), q(0.75)]


def render_stats(theme, s):
    """s: year, total, repos, pushed_30d, streak, weeks (list of 7-int lists), langs [(name, pct)], updated."""
    t = THEMES[theme]
    w, h = 1200, 340
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{s["total"]:,} contributions in {s["year"]}">', STYLE, _sheet(t, w, h)]

    out.append(f'<text x="56" y="72" font-size="13" letter-spacing="3" fill="{t["accent"]}">BUILD LOG / {s["year"]}</text>')
    out.append(f'<text x="52" y="148" font-size="64" font-weight="700" fill="{t["ink"]}">{s["total"]:,}</text>')
    out.append(f'<text x="56" y="178" font-size="14" fill="{t["muted"]}">contributions this year</text>')
    for i, (label, value) in enumerate([("PUBLIC REPOS", s["repos"]), ("PUSHED 30D", s["pushed_30d"]), ("STREAK", f'{s["streak"]}d')]):
        x = 56 + i * 140
        out.append(f'<path d="M{x} 212H{x + 112}" stroke="{t["line"]}"/>')
        out.append(f'<text x="{x}" y="234" font-size="11" letter-spacing="2" fill="{t["muted"]}">{label}</text>')
        out.append(f'<text x="{x}" y="266" font-size="28" font-weight="700" fill="{t["ink"]}">{value}</text>')

    # Contribution heatmap, last 53 weeks
    weeks = s["weeks"][-53:]
    flat = [c for wk in weeks for c in wk]
    l1, l2, l3 = _levels(flat)
    x0, y0, cell, gap = 520, 64, 10, 2
    out.append(f'<text x="{x0}" y="52" font-size="11" letter-spacing="2" fill="{t["muted"]}">LAST 52 WEEKS</text>')
    for wi, wk in enumerate(weeks):
        for di, c in enumerate(wk):
            lvl = 0 if c == 0 else 1 if c <= l1 else 2 if c <= l2 else 3 if c <= l3 else 4
            out.append(f'<rect x="{x0 + wi * (cell + gap)}" y="{y0 + di * (cell + gap)}" width="{cell}" height="{cell}" rx="1.5" fill="{t["heat"][lvl]}"/>')

    # Language mix
    bar_w, bx, by = 636, x0, 196
    out.append(f'<text x="{bx}" y="{by - 12}" font-size="11" letter-spacing="2" fill="{t["muted"]}">MATERIALS (BY CODE SIZE)</text>')
    cx = bx
    for i, (name, pct) in enumerate(s["langs"]):
        seg = bar_w * pct / 100
        out.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(seg - 2, 1):.1f}" height="10" fill="{t["langs"][i]}"/>')
        cx += seg
        lx, ly = bx + (i % 3) * 212, by + 40 + (i // 3) * 26
        out.append(f'<rect x="{lx}" y="{ly - 9}" width="10" height="10" fill="{t["langs"][i]}"/>')
        out.append(f'<text x="{lx + 18}" y="{ly}" font-size="13" fill="{t["ink"]}">{escape(name)} <tspan fill="{t["muted"]}">{pct:.0f}%</tspan></text>')

    out.append(f'<text x="56" y="306" font-size="11" fill="{t["muted"]}">regenerated {escape(s["updated"])} / github.com/xkazm04</text>')
    out.append("</svg>\n")
    return "\n".join(out)
