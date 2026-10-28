"""Drafting Sheet, Rev. B - the profile README and its six sheets.

Standard library only. build(P, S, out_dir) takes the owner's content (data/profile.json) and a
GitHub snapshot (built by update_readme.py), inlines logos from data/logos and VR art from
data/images/vr, and writes assets/*-dark.svg, assets/*-light.svg and README.md under out_dir.

Every sheet is drawn on a 1200-unit-wide viewBox shown at width="100%" in an 846 px column, so the
type floor is 1200 * 14 / 846 = 19.9 units: nothing below MIN_TYPE is ever emitted.
"""

import base64
import datetime as dt
import json
import math
import os
import re
from xml.sax.saxutils import escape

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

W = 1200
MIN_TYPE = 20
MONO = "'JetBrains Mono','SFMono-Regular',ui-monospace,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg="#0B0D10", minor="#131820", major="#1B222B", frame="#2D3540", ink="#E7E5E4",
                 muted="#8B949E", accent="#F59E0B", face_l="#141920", face_r="#1C232C", glow=0.16,
                 hatch="#5A4313"),
    "light": dict(bg="#F6F3EC", minor="#ECE6D9", major="#E0D8C7", frame="#CFC6B3", ink="#1C1917",
                  muted="#6B6459", accent="#B45309", face_l="#EDE7DA", face_r="#E2DACB", glow=0.10,
                  hatch="#E7CFA6"),
}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def logo_path(fname):
    fname = fname.split(" ")[0]
    with open(os.path.join(DATA, "logos", fname), encoding="utf-8") as f:
        return re.search(r'<path d="([^"]+)"', f.read()).group(1)


def tw(text, size, k=0.62):
    """Conservative width of monospace text."""
    return len(text) * size * k


def fmt(n):
    return f"{n:,}"


# ---------------------------------------------------------------- sheet frame

def sheet(t, h, title, body, css="", sheet_no=None, label=""):
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{escape(label)}">')
    s.append("<style>")
    s.append(f"text {{ font-family: {MONO}; }}")
    s.append(css)
    s.append("@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }")
    s.append("</style>")
    s.append("<defs>")
    s.append(f'<pattern id="minor" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{t["minor"]}" stroke-width="1"/></pattern>')
    s.append(f'<pattern id="major" width="120" height="120" patternUnits="userSpaceOnUse"><rect width="120" height="120" fill="url(#minor)"/><path d="M120 0H0V120" fill="none" stroke="{t["major"]}" stroke-width="1"/></pattern>')
    s.append(f'<radialGradient id="lamp" cx="0.72" cy="0.38" r="0.62"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>')
    s.append(f'<pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V10" stroke="{t["accent"]}" stroke-width="2.2"/></pattern>')
    s.append(f'<pattern id="hatch2" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><path d="M0 0V12" stroke="{t["ink"]}" stroke-width="1.6"/></pattern>')
    s.append(f'<pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.6" fill="{t["ink"]}"/></pattern>')
    s.append("</defs>")
    s.append(f'<rect width="{W}" height="{h}" fill="{t["bg"]}"/>')
    s.append(f'<rect width="{W}" height="{h}" fill="url(#major)"/>')
    s.append(f'<rect width="{W}" height="{h}" fill="url(#lamp)"/>')
    s.append(f'<rect x="16.5" y="16.5" width="{W - 33}" height="{h - 33}" fill="none" stroke="{t["frame"]}" stroke-width="1"/>')
    a = t["accent"]
    for x, y, dx, dy in ((16, 16, 1, 1), (W - 16, 16, -1, 1), (16, h - 16, 1, -1), (W - 16, h - 16, -1, -1)):
        s.append(f'<path d="M{x} {y + 26 * dy}V{y}H{x + 26 * dx}" fill="none" stroke="{a}" stroke-width="3"/>')
    if title:
        s.append(f'<text x="56" y="70" font-size="22" letter-spacing="4" fill="{t["muted"]}">{escape(title)}</text>')
    if sheet_no is not None:
        s.append(f'<text x="{W - 56}" y="70" font-size="22" letter-spacing="4" text-anchor="end" fill="{t["accent"]}">SHEET {sheet_no:02d} / 05</text>')
        s.append(f'<path d="M56 92H{W - 56}" stroke="{t["frame"]}" stroke-width="1"/>')
    s.extend(body)
    s.append("</svg>")
    return "\n".join(s)


def text(x, y, s, size, fill, anchor="start", weight=None, ls=None, extra=""):
    size = max(size, MIN_TYPE)
    w = f' font-weight="{weight}"' if weight else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{w}{l}{a} fill="{fill}"{extra}>{escape(s)}</text>'


def logo(fname, x, y, size, fill):
    k = size / 24
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" d="{logo_path(fname)}" fill="{fill}"/>'


def judge_glyph(x, y, size, stroke):
    k = size / 24
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" fill="none" stroke="{stroke}" stroke-width="{1.8:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3V21M6 21H18M3 7H21M12 3L12 7"/>'
            f'<path d="M5 7L2 14H8Z M19 7L16 14H22Z"/></g>')


# ---------------------------------------------------------------- isometric helpers

C30, S30 = math.cos(math.radians(30)), 0.5


class Iso:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0):
        return (self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * S30 * self.s - z * self.s)

    def poly(self, pts):
        return "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in (self.p(*q) for q in pts)) + "Z"

    def box(self, t, x, y, z, w, d, h, top=None, stroke=None, sw=1.6, top_extra=""):
        st = stroke or t["ink"]
        top_fill = top or t["bg"]
        out = [
            f'<path d="{self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)])}" fill="{t["face_l"]}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>',
            f'<path d="{self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)])}" fill="{t["face_r"]}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>',
            f'<path d="{self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)])}" fill="{top_fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"{top_extra}/>',
        ]
        return "".join(out)

    def cyl(self, t, x, y, z, r, h, stroke=None, top=None, sw=1.6):
        st = stroke or t["ink"]
        cx, cyb = self.p(x, y, z)
        _, cyt = self.p(x, y, z + h)
        rx, ry = r * self.s * 1.2247, r * self.s * 0.7071
        body = (f'<path d="M{cx - rx:.1f} {cyt:.1f}V{cyb:.1f}A{rx:.1f} {ry:.1f} 0 0 0 {cx + rx:.1f} {cyb:.1f}V{cyt:.1f}Z" '
                f'fill="{t["face_r"]}" stroke="{st}" stroke-width="{sw}"/>')
        cap = f'<ellipse cx="{cx:.1f}" cy="{cyt:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{top or t["bg"]}" stroke="{st}" stroke-width="{sw}"/>'
        return body + cap

    def line(self, a, b, stroke, sw=1.2, dash=None, extra=""):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d} fill="none"{extra}/>'


# ---------------------------------------------------------------- sheet 00: title

def sheet_title(t, P, S):
    c = S["contributions"]
    r = S["repos"]
    h = 560
    css = """
.cursor { animation: blink 1.4s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
.f1 { animation: float 7s ease-in-out infinite; }
.f3 { animation: float 7s ease-in-out -3.5s infinite; }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
.flow { animation: flow 3s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -24; } }
"""
    b = []
    b.append(text(56, 70, "SHEET 00 / PROFILE / REV B", 22, t["muted"], ls=4))
    b.append(text(W - 56, 70, "GITHUB.COM/XKAZM04", 22, t["accent"], anchor="end", ls=4))
    # name
    name = P["handle"]
    b.append(text(48, 278, name, 196, t["ink"], weight=700, extra=' textLength="540" lengthAdjust="spacing"'))
    b.append(f'<rect class="cursor" x="608" y="136" width="58" height="146" fill="{t["accent"]}"/>')
    b.append(text(60, 346, P["title"].upper(), 40, t["accent"], weight=700, ls=16))
    b.append(f'<path d="M60 372H530 M60 364V380 M530 364V380" stroke="{t["accent"]}" stroke-width="2" fill="none"/>')

    # exploded assembly: three slabs, top one lit
    iso = Iso(860, 268, 0.8)
    parts = []
    parts.append(iso.line((0, 0, -10), (0, 0, 210), t["muted"], 1.2, "6 6", ' class="flow"'))
    parts.append(iso.line((150, 0, -10), (150, 0, 210), t["muted"], 1.2, "6 6", ' class="flow"'))
    parts.append(iso.line((0, 150, -10), (0, 150, 210), t["muted"], 1.2, "6 6", ' class="flow"'))
    b.append("".join(parts))
    b.append(f'<g class="f3">{iso.box(t, 0, 0, -10, 150, 150, 26)}</g>')
    b.append(f'<g>{iso.box(t, 0, 0, 80, 150, 150, 26)}</g>')
    top = iso.box(t, 0, 0, 170, 150, 150, 26, top=t["accent"], stroke=t["accent"], sw=2)
    b.append(f'<g class="f1">{top}<path d="{iso.poly([(0, 0, 196), (150, 0, 196), (150, 150, 196), (0, 150, 196)])}" fill="url(#hatch2)" opacity="0.18"/></g>')
    # leader labels for the three slabs
    for z, lab, col in ((196, "GATE", t["accent"]), (106, "AGENTS", t["ink"]), (16, "DATA", t["ink"])):
        x0, y0 = iso.p(150, 0, z)
        b.append(f'<path d="M{x0 + 6:.0f} {y0:.0f}H{x0 + 60:.0f}" stroke="{t["muted"]}" stroke-width="1.2"/>')
        b.append(f'<circle cx="{x0 + 4:.0f}" cy="{y0:.0f}" r="4" fill="{col}"/>')
        b.append(text(x0 + 70, y0 + 8, lab, 22, col, ls=3, weight=700))

    # title block with live numbers
    y0 = 420
    cells = [
        ("CONTRIBUTIONS / 12 MO", fmt(c["total_last_year"])),
        ("CURRENT STREAK", f'{c["current_streak_days"]} DAYS'),
        ("PUBLIC REPOS", str(r["public_count"])),
        ("PUSHED / 30 DAYS", str(r["pushed_last_30_days"])),
    ]
    xs = [56, 372, 652, 900, W - 56]
    b.append(f'<rect x="56.5" y="{y0 + .5}" width="{W - 113}" height="96" fill="{t["bg"]}" stroke="{t["frame"]}" stroke-width="1.5"/>')
    for i, (lab, val) in enumerate(cells):
        x = xs[i]
        if i:
            b.append(f'<path d="M{x + .5} {y0}V{y0 + 96}" stroke="{t["frame"]}" stroke-width="1.5"/>')
        b.append(text(x + 22, y0 + 34, lab, 20, t["muted"], ls=2))
        b.append(text(x + 22, y0 + 78, val, 38, t["accent"] if i == 0 else t["ink"], weight=700))
    return sheet(t, h, None, b, css, label=f'{P["handle"]}, {P["title"]}: {fmt(c["total_last_year"])} contributions in the last year')


# ---------------------------------------------------------------- sheet 01: specification

def sheet_spec(t, P):
    h = 600
    fy = 290
    css = """
.packet { animation: travel 10s ease-in-out infinite; }
@keyframes travel {
  0%, 6% { transform: translateX(0px); opacity: 1; }
  24%, 34% { transform: translateX(254px); opacity: 1; }
  48%, 56% { transform: translateX(450px); opacity: 1; }
  70% { transform: translateX(640px); opacity: 1; }
  78%, 100% { transform: translateX(640px); opacity: 0; }
}
.gate { animation: gate 10s ease-in-out infinite; transform-origin: 740px 230px; }
@keyframes gate { 0%, 50% { transform: rotate(0deg); } 57%, 72% { transform: rotate(-72deg); } 80%, 100% { transform: rotate(0deg); } }
"""
    b = []
    a, ink, mu = t["accent"], t["ink"], t["muted"]
    # machine boundary, open where the gate is
    b.append(f'<path d="M740 230V120H56V520H740V350" fill="none" stroke="{a}" stroke-width="2" stroke-dasharray="14 10"/>')
    b.append(f'<rect x="70" y="106" width="214" height="30" fill="{t["bg"]}"/>')
    b.append(text(80, 129, "YOUR MACHINE", 22, a, weight=700, ls=4))

    # 1: SQLite drum
    iso = Iso(190, 350, 1.0)
    b.append(iso.cyl(t, 0, 0, 0, 62, 120))
    for zz in (40, 80):
        cx, cy = iso.p(0, 0, zz)
        rx, ry = 62 * 1.2247, 62 * 0.7071
        b.append(f'<path d="M{cx - rx:.1f} {cy:.1f}A{rx:.1f} {ry:.1f} 0 0 0 {cx + rx:.1f} {cy:.1f}" fill="none" stroke="{ink}" stroke-width="1.4"/>')
    lx, ly = iso.p(0, 0, 120)
    b.append(logo("sqlite.svg", lx - 22, ly - 24, 44, a))

    # 2: agent
    b.append(f'<path d="M266 {fy}H428" stroke="{mu}" stroke-width="2" stroke-dasharray="8 8"/>')
    ax, ay = 520, fy
    hexpts = " ".join(f"{ax + 92 * math.cos(math.radians(60 * k + 30)):.1f},{ay + 92 * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    b.append(f'<polygon points="{hexpts}" fill="{t["face_r"]}" stroke="{ink}" stroke-width="2"/>')
    hexin = " ".join(f"{ax + 72 * math.cos(math.radians(60 * k + 30)):.1f},{ay + 72 * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    b.append(f'<polygon points="{hexin}" fill="none" stroke="{mu}" stroke-width="1.2" stroke-dasharray="4 6"/>')
    b.append(logo("claude.svg", ax - 34, ay - 34, 68, a))
    b.append(f'<path d="M612 {fy}H726" stroke="{mu}" stroke-width="2" stroke-dasharray="8 8"/>')

    # 3: the gate in the boundary, and the person who holds it
    b.append(f'<path d="M730 230H750 M730 350H750" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<g class="gate"><path d="M740 230V350" stroke="{a}" stroke-width="8" stroke-linecap="round"/></g>')
    b.append(f'<circle cx="740" cy="230" r="8" fill="{a}"/>')
    b.append(f'<circle cx="812" cy="170" r="20" fill="none" stroke="{ink}" stroke-width="3"/><path d="M778 222Q812 184 846 222" fill="none" stroke="{ink}" stroke-width="3"/>')
    b.append(f'<path d="M812 232V264" stroke="{mu}" stroke-width="1.5" stroke-dasharray="3 4"/>')

    # 4: what ships, outside the machine
    b.append(f'<path d="M764 {fy}H896" stroke="{a}" stroke-width="2.5"/><path d="M886 {fy - 10}L900 {fy}L886 {fy + 10}" fill="none" stroke="{a}" stroke-width="2.5"/>')
    iso2 = Iso(1012, 336, 0.95)
    b.append(iso2.box(t, -60, -60, 0, 120, 120, 110, top=t["bg"], stroke=a, sw=2.2))
    b.append(f'<path d="{iso2.poly([(-60, -60, 110), (60, -60, 110), (60, 60, 110), (-60, 60, 110)])}" fill="url(#hatch)" opacity=".4"/>')

    # packet: starts inside the machine, waits for the agent, waits for the gate
    b.append(f'<g class="packet"><circle cx="270" cy="{fy}" r="9" fill="{a}"/><circle cx="270" cy="{fy}" r="18" fill="none" stroke="{a}" stroke-width="1.5" opacity=".6"/></g>')

    # labels with balloons that key the principles listed under the image
    for n, x, small, big in ((1, 190, "STATE", "IN SQLITE"), (2, 520, "AGENTS", "DO THE WORK"),
                             (None, 816, "A PERSON", "APPROVES"), (3, 1012, "SHIP", "THE WHOLE THING")):
        b.append(text(x, 452, small, 22, mu, anchor="middle", ls=3))
        b.append(text(x, 488, big, 26, ink, anchor="middle", weight=700))
        if n:
            bx = x - tw(small, 22) / 2 - 34
            b.append(f'<circle cx="{bx:.0f}" cy="445" r="18" fill="{t["bg"]}" stroke="{a}" stroke-width="2"/>')
            b.append(text(bx, 453, str(n), 22, a, anchor="middle", weight=700))
    b.append(text(W - 56, 560, "NOTHING LEAVES UNLESS A PERSON SENDS IT", 20, mu, anchor="end", ls=2))
    return sheet(t, h, "SHEET 01 / SPECIFICATION", b, css, sheet_no=1,
                 label="Specification: state in SQLite on your machine, agents do the work, a person approves what ships")


# ---------------------------------------------------------------- sheet 02: build log

def sheet_log(t, S):
    c, r = S["contributions"], S["repos"]
    weeks = c["weeks"]
    totals = [sum(d["count"] for d in w) for w in weeks]
    n = len(weeks)
    h = 720
    x0, x1 = 56, W - 56
    base = 590
    maxh = 250
    step = (x1 - x0) / n
    bw = step * 0.62
    peak = max(totals)
    pi = totals.index(peak)
    css = f"""
.scan {{ animation: scan 12s linear infinite; }}
@keyframes scan {{ from {{ transform: translateX(0px); }} to {{ transform: translateX({x1 - x0:.0f}px); }} }}
.now {{ animation: pulse 2.4s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .45; }} }}
"""
    b = []
    a, ink, mu = t["accent"], t["ink"], t["muted"]
    # display number
    b.append(text(50, 232, fmt(c["total_last_year"]), 136, ink, weight=700, ls=-4))
    b.append(text(58, 274, "CONTRIBUTIONS IN THE LAST 12 MONTHS", 22, a, ls=3))
    # right column facts
    facts = [(f'{c["current_streak_days"]}', "DAY STREAK", W - 56, a),
             (f'{r["pushed_last_30_days"]}/{r["public_count"]}', "REPOS PUSHED / 30D", W - 300, ink)]
    for v, lab, x, col in facts:
        b.append(text(x, 210, v, 64, col, anchor="end", weight=700))
        b.append(text(x, 244, lab, 20, mu, anchor="end", ls=2))

    # elevation: weekly totals as hatched columns
    cols = []
    for i, v in enumerate(totals):
        hh = max(2.0, v / peak * maxh)
        x = x0 + i * step + (step - bw) / 2
        fill = "url(#hatch)"
        cols.append(f'<rect x="{x:.1f}" y="{base - hh:.1f}" width="{bw:.1f}" height="{hh:.1f}" fill="{fill}" stroke="{a}" stroke-width="1.4"/>')
    b.extend(cols)
    # newest week, lit
    lx = x0 + (n - 1) * step + (step - bw) / 2
    lh = max(2.0, totals[-1] / peak * maxh)
    b.append(f'<rect class="now" x="{lx:.1f}" y="{base - lh:.1f}" width="{bw:.1f}" height="{lh:.1f}" fill="{a}"/>')
    # ground line + month ticks
    b.append(f'<path d="M{x0 - 8} {base}H{x1 + 8}" stroke="{ink}" stroke-width="3"/>')
    seen = set()
    last_lab_x = -999
    for i, w in enumerate(weeks):
        for d in w:
            day = dt.date.fromisoformat(d["date"])
            if day.day == 1 and (day.year, day.month) not in seen:
                seen.add((day.year, day.month))
                x = x0 + i * step
                b.append(f'<path d="M{x:.1f} {base}V{base + 12}" stroke="{mu}" stroke-width="1.5"/>')
                if x - last_lab_x > 70 and x < x1 - 30:
                    b.append(text(x + 4, base + 38, day.strftime("%b").upper(), 20, mu))
                    last_lab_x = x
    # peak dimension
    px = x0 + pi * step + step / 2
    py = base - maxh
    b.append(f'<path d="M{px:.1f} {py - 8:.1f}V{py - 40:.1f}" stroke="{ink}" stroke-width="1.4"/>')
    anchor = "end" if px > W / 2 else "start"
    tx = px - 10 if anchor == "end" else px + 10
    b.append(text(tx, py - 22, f"PEAK WEEK {fmt(peak)}", 22, ink, anchor=anchor, weight=700))
    # streak bracket
    today = dt.date.fromisoformat(weeks[-1][-1]["date"])
    start = today - dt.timedelta(days=c["current_streak_days"] - 1)
    si = next((i for i, w in enumerate(weeks) if any(dt.date.fromisoformat(d["date"]) >= start for d in w)), n - 1)
    sx = x0 + si * step
    by = base + 62
    b.append(f'<path d="M{sx:.1f} {by - 10}V{by}H{x1:.1f}V{by - 10}" fill="none" stroke="{a}" stroke-width="2"/>')
    b.append(text(sx - 12, by + 6, f'{c["current_streak_days"]}-DAY STREAK', 20, a, anchor="end", ls=2))
    # scanning plotter head
    b.append(f'<g class="scan"><path d="M{x0} {base - maxh - 12}V{base}" stroke="{a}" stroke-width="1.5" opacity=".55"/></g>')
    return sheet(t, h, "SHEET 02 / BUILD LOG", b, css, sheet_no=2,
                 label=f'Build log: {fmt(c["total_last_year"])} contributions in the last 12 months, drawn as weekly columns')


# ---------------------------------------------------------------- sheet 03: assemblies

def draw_personas(t, cx, cy):
    iso = Iso(cx, cy + 24, 1.0)
    o = []
    pts = [(-84, -14), (-14, -84), (62, 0), (0, 62)]
    for (x, y) in pts:
        o.append(iso.line((0, 0, 0), (x + 14, y + 14, 0), t["muted"], 1.6, "5 5"))
    o.append(iso.box(t, -30, -30, 0, 60, 60, 74, top=t["accent"], stroke=t["accent"], sw=2))
    for k, (x, y) in enumerate(pts):
        o.append(f'<g class="ag ag{k}">{iso.box(t, x, y, 0, 28, 28, 28)}</g>')
    return "".join(o)


def draw_vibeman(t, cx, cy):
    iso = Iso(cx - 9, cy + 30, 1.0)
    o = [iso.line((-96, 50, 0), (110, 50, 0), t["muted"], 1.4, "5 5")]
    for k in range(4):
        x = -66 + k * 44
        o.append(iso.box(t, x, -35, 0, 10, 70, 74))
        p1 = iso.p(x + 10, -20, 52)
        p2 = iso.p(x + 10, 12, 52)
        o.append(f'<path class="cur cur{k}" d="M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}" stroke="{t["accent"]}" stroke-width="4" stroke-linecap="round"/>')
        q1 = iso.p(x + 10, -20, 36)
        q2 = iso.p(x + 10, 0, 36)
        o.append(f'<path d="M{q1[0]:.1f} {q1[1]:.1f}L{q2[0]:.1f} {q2[1]:.1f}" stroke="{t["muted"]}" stroke-width="3" stroke-linecap="round"/>')
    return "".join(o)


def draw_lighttrack(t, cx, cy):
    iso = Iso(cx - 60, cy + 2, 1.0)
    o = []
    # the spot the lamp watches, then the beam, then the lamp
    sx, sy = iso.p(118, 6, 0)
    o.append(f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{44 * 1.2247:.1f}" ry="{44 * 0.7071:.1f}" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="6 5"/>')
    lx, ly = iso.p(0, 0, 90)
    a1 = (sx - 44 * 1.2247 * 0.55, sy - 44 * 0.7071 * 0.83)
    a2 = (sx + 44 * 1.2247 * 0.55, sy + 44 * 0.7071 * 0.83)
    o.append(f'<path class="beam" d="M{lx:.1f} {ly:.1f}L{a1[0]:.1f} {a1[1]:.1f}L{a2[0]:.1f} {a2[1]:.1f}Z" fill="{t["accent"]}" opacity=".24"/>')
    o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" fill="{t["accent"]}"/>')
    o.append(iso.cyl(t, 0, 0, 0, 30, 90, top=t["accent"], stroke=t["ink"]))
    return "".join(o)


def draw_pumper(t, cx, cy):
    iso = Iso(cx - 55, cy, 1.0)
    o = [iso.line((40, 6, 0), (186, 6, 0), t["muted"], 1.4, "5 5")]
    for k in range(3):
        o.append(f'<g class="job job{k}">{iso.box(t, 64 + k * 38, -10, 0, 26, 26, 26)}</g>')
    o.append(iso.cyl(t, 0, 0, 0, 34, 64))
    rx, ry = iso.p(0, 0, 64)
    o.append(f'<g class="piston"><path d="M{rx:.1f} {ry:.1f}V{ry - 36:.1f}" stroke="{t["ink"]}" stroke-width="5"/>'
             f'<ellipse cx="{rx:.1f}" cy="{ry - 36:.1f}" rx="24" ry="13" fill="{t["accent"]}" stroke="{t["accent"]}"/></g>')
    return "".join(o)


def draw_ascent(t, cx, cy):
    iso = Iso(cx, cy + 22, 1.0)
    o = []
    for k in range(9):
        last = k == 8
        o.append(iso.box(t, k * 22 - 100, -40, 0, 22, 80, 14 + k * 14,
                         top=t["accent"] if last else None, stroke=t["accent"] if last else None))
    return "".join(o)


def draw_politicas(t, cx, cy):
    iso = Iso(cx, cy + 6, 1.0)
    nodes = [(0, 0, 18), (-80, -20, 10), (-40, -80, 10), (40, -70, 10), (80, 10, 10), (40, 70, 10), (-40, 60, 10), (-100, 50, 8), (100, -60, 8)]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7), (6, 7), (3, 8), (4, 8), (2, 3), (5, 6)]
    o = []
    for i, j in edges:
        a, b_ = nodes[i], nodes[j]
        o.append(iso.line((a[0], a[1], 4), (b_[0], b_[1], 4), t["muted"], 1.6, extra=f' class="edge"'))
    for k, (x, y, r) in enumerate(nodes):
        if k == 0:
            o.append(iso.cyl(t, x, y, 0, r, 22, top=t["accent"], stroke=t["accent"]))
        else:
            o.append(iso.cyl(t, x, y, 0, r, 8))
    return "".join(o)


DRAW = {"personas": draw_personas, "vibeman": draw_vibeman, "lighttrack": draw_lighttrack,
        "pumper": draw_pumper, "ascent": draw_ascent, "politicas": draw_politicas}

FLAG_LOGOS = {
    "personas": ["tauri.svg", "react.svg", "sqlite.svg"],
    "vibeman": ["nextdotjs.svg", "claude.svg", "ollama.svg"],
    "lighttrack": ["rust.svg", "sqlite.svg", "postgresql.svg"],
    "pumper": ["rust.svg", "sqlite.svg", "claude.svg"],
    "ascent": ["typescript.svg"],
    "politicas": ["typescript.svg"],
}


def project_index(P):
    out, k = {}, 0
    for g in P["project_groups"]:
        for p in g["projects"]:
            k += 1
            out[p["name"]] = (g["letter"], k, p, g)
    return out


def sheet_assemblies(t, P, S):
    idx = project_index(P)
    pushed = {i["name"]: i["pushed_at"][:10] for i in S["repos"]["items"]}
    today = dt.date.fromisoformat(S["fetched_at"][:10])
    cw, ch = 352, 330
    gx, gy = 56, 120
    gap = (W - 2 * gx - 3 * cw) / 2
    h = gy + 2 * ch + 24 + 84
    css = """
.ag { animation: lift 6s ease-in-out infinite; }
.ag1 { animation-delay: -1.5s; } .ag2 { animation-delay: -3s; } .ag3 { animation-delay: -4.5s; }
@keyframes lift { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
.cur { animation: blink 2.4s steps(1) infinite; }
.cur1 { animation-delay: -.6s; } .cur2 { animation-delay: -1.2s; } .cur3 { animation-delay: -1.8s; }
@keyframes blink { 50% { opacity: .15; } }
.beam { animation: beam 5s ease-in-out infinite; }
@keyframes beam { 0%,100% { opacity: .22; } 50% { opacity: .42; } }
.piston { animation: piston 3.2s ease-in-out infinite; }
@keyframes piston { 0%,100% { transform: translateY(0); } 50% { transform: translateY(14px); } }
.edge { animation: edge 4s ease-in-out infinite; }
@keyframes edge { 0%,100% { opacity: 1; } 50% { opacity: .35; } }
"""
    b = []
    for k, name in enumerate(P["flagships"]):
        letter, num, p, g = idx[name]
        col, row = k % 3, k // 3
        x = gx + col * (cw + gap)
        y = gy + row * (ch + 24)
        b.append(f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{cw}" height="{ch}" fill="{t["bg"]}" stroke="{t["frame"]}" stroke-width="1.5"/>')
        b.append(f'<path d="M{x:.1f} {y + 22}V{y}H{x + 22:.1f}" fill="none" stroke="{t["accent"]}" stroke-width="3"/>')
        b.append(text(x + 22, y + 42, f"{letter}-{num:02d}", 22, t["accent"], ls=2, weight=700))
        # logos top-right
        lg = FLAG_LOGOS.get(name, [])
        for j, f in enumerate(reversed(lg)):
            b.append(logo(f, x + cw - 22 - 30 - j * 42, y + 18, 30, t["ink"]))
        b.append(DRAW[name](t, x + cw / 2, y + 160))
        b.append(f'<path d="M{x + 22:.1f} {y + ch - 74}H{x + cw - 22:.1f}" stroke="{t["frame"]}" stroke-width="1"/>')
        b.append(text(x + 22, y + ch - 28, name, 36, t["ink"], weight=700))
        d = pushed.get(name)
        if d:
            days = (today - dt.date.fromisoformat(d)).days
            lab = "TODAY" if days == 0 else f"{days}D AGO"
            dot = t["accent"] if days <= 7 else t["muted"]
            b.append(f'<circle cx="{x + cw - 22 - tw(lab, 20) - 14:.1f}" cy="{y + ch - 35}" r="5" fill="{dot}"/>')
            b.append(text(x + cw - 22, y + ch - 28, lab, 20, t["muted"], anchor="end"))
    b.append(text(W - 56, h - 44, "DOT: LAST PUSH, AMBER WITHIN 7 DAYS", 20, t["muted"], anchor="end", ls=2))
    return sheet(t, h, "SHEET 03 / ASSEMBLIES / SIX FLAGSHIPS", b, css, sheet_no=3,
                 label="Assemblies: personas, vibeman, lighttrack, pumper, ascent and politicas drawn as isometric parts")


# ---------------------------------------------------------------- sheet 04: VR plates

def sheet_vr(t, P):
    picks = P["vr_sheet"]
    vr = {v["file"]: v for v in P["vr"]}
    groups = {p["name"]: p for g in P["project_groups"] for p in g["projects"]}
    pw, ph = 528, 297
    y = 128
    h = y + ph + 150
    b = []
    for k, f in enumerate(picks):
        v = vr[f]
        x = 56 + k * (pw + (W - 112 - 2 * pw))
        with open(os.path.join(DATA, f), "rb") as fh:
            data = base64.b64encode(fh.read()).decode("ascii")
        cid = f"clip{k}"
        b.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{pw}" height="{ph}"/></clipPath>')
        b.append(f'<image href="data:image/jpeg;base64,{data}" x="{x}" y="{y}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
        b.append(f'<rect x="{x - 8.5}" y="{y - 8.5}" width="{pw + 17}" height="{ph + 17}" fill="none" stroke="{t["frame"]}" stroke-width="1.5"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="none" stroke="{t["ink"]}" stroke-width="1" opacity=".5"/>')
        b.append(f'<path d="M{x - 8} {y + 22}V{y - 8}H{x + 22}" fill="none" stroke="{t["accent"]}" stroke-width="3"/>')
        b.append(f'<path d="M{x + pw + 8} {y + ph - 22}V{y + ph + 8}H{x + pw - 22}" fill="none" stroke="{t["accent"]}" stroke-width="3"/>')
        # kind tag on the art
        kind = v["kind"].upper()
        kw = tw(kind, 20) + 28
        b.append(f'<rect x="{x + 14}" y="{y + 14}" width="{kw:.0f}" height="36" fill="{t["bg"]}" opacity=".88"/>')
        b.append(text(x + 28, y + 39, kind, 20, t["accent"], ls=1, weight=700))
        b.append(text(x, y + ph + 62, v.get("title", v["project"]), 36, t["ink"], weight=700))
        stack = v.get("sub", groups[v["project"]]["stack"])
        b.append(text(x, y + ph + 98, stack, 20, t["muted"], ls=2))
    label = " and ".join(f'{vr[f]["project"]} {vr[f]["kind"]}' for f in picks)
    return sheet(t, h, "SHEET 04 / HANDS-FIRST VR", b, "", sheet_no=4, label=f"Hands-first VR: {label}")


# ---------------------------------------------------------------- sheet 05: standard parts

def sheet_toolbox(t, P, S):
    rows = P["toolbox"]
    y0, rh = 140, 104
    h = y0 + rh * len(rows) + 150
    b = []
    for i, g in enumerate(rows):
        y = y0 + i * rh
        b.append(f'<path d="M56 {y + rh - 18}H{W - 56}" stroke="{t["frame"]}" stroke-width="1"/>')
        b.append(text(56, y + 50, g["group"].upper(), 22, t["accent"], ls=3, weight=700))
        x = 276
        for label, f in g["tools"]:
            if f:
                b.append(logo(f, x, y + 14, 48, t["ink"]))
            else:
                b.append(judge_glyph(x, y + 14, 48, t["ink"]))
            b.append(text(x + 62, y + 48, label, 24, t["ink"]))
            x += 62 + tw(label, 24, 0.6) + 30
    # material legend = language mix by code size
    mix = S["repos"]["language_mix_by_code_size"]
    y = y0 + rh * len(rows) + 10
    b.append(text(56, y + 34, "MATERIAL", 22, t["accent"], ls=3, weight=700))
    fills = ["url(#hatch)", "url(#hatch2)", "url(#dots)", t["face_r"], t["frame"], t["frame"]]
    bx, bw = 276, W - 56 - 276
    x = bx
    labels = []
    for k, m in enumerate(mix):
        w = bw * m["percent"] / 100
        b.append(f'<rect x="{x:.1f}" y="{y + 10}" width="{w:.1f}" height="30" fill="{fills[min(k, 5)]}" stroke="{t["ink"]}" stroke-width="1.2"/>')
        labels.append((x, m))
        x += w
    lx = bx
    for k, (x, m) in enumerate(labels):
        lab = f'{m["language"]} {m["percent"]:g}%'
        if k < 3:
            b.append(text(lx, y + 76, lab, 20, t["ink"] if k == 0 else t["muted"]))
            lx += tw(lab, 20) + 34
    rest = sum(m["percent"] for m in mix[3:])
    b.append(text(lx, y + 76, f"+{len(mix) - 3} more {rest:.1f}%", 20, t["muted"]))
    return sheet(t, h, "SHEET 05 / STANDARD PARTS", b, "", sheet_no=5,
                 label="Toolbox: languages, apps, data, AI and XR tools, each with its logo")


# ---------------------------------------------------------------- README

def readme(P, S, version=""):
    c, r = S["contributions"], S["repos"]
    idx = project_index(P)
    v = f"?v={version}" if version else ""  # busts GitHub's image cache when the sheets are redrawn

    def pic(name, alt, href=None):
        s = (f'<picture>\n  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg{v}" />\n'
             f'  <img alt="{escape(alt)}" src="assets/{name}-dark.svg{v}" width="100%" />\n</picture>')
        if href:
            s = f'<a href="{href}">\n{s}\n</a>'
        return s

    L = []
    L.append(pic("title", f'{P["handle"]}, {P["title"]}. {fmt(c["total_last_year"])} contributions in the last 12 months, {c["current_streak_days"]}-day streak, {r["public_count"]} public repos', P["github"]))
    L.append("")
    L.append('<p align="center">')
    L.append(f'  <a href="{P["linkedin"]}"><img src="https://img.shields.io/badge/LinkedIn-michalkazdan-F59E0B?style=flat-square&labelColor=0B0D10" alt="LinkedIn: michalkazdan" /></a>')
    L.append("</p>")
    L.append("")
    L.append(P["intro"])
    L.append("")
    L.append(pic("spec", "Specification: state in SQLite on your machine, agents do the work, a person approves what ships"))
    L.append("")
    for k, pr in enumerate(P["principles"], 1):
        L.append(f'{k}. **{pr["name"]}.** {pr["text"]}')
    L.append("")
    L.append(pic("log", f'Build log: {fmt(c["total_last_year"])} contributions in the last 12 months as weekly columns, {c["current_streak_days"]}-day streak'))
    L.append("")
    L.append("<details>")
    L.append(f'<summary><b>Latest pushes</b> &nbsp;<sub>{r["pushed_last_30_days"]} of {r["public_count"]} public repos pushed in the last 30 days</sub></summary>')
    L.append("")
    for it in r["items"][:8]:
        desc = (it["description"] or "").strip()
        lang = (it["primary_language"] or "").upper()
        line = f'`{it["pushed_at"][:10]}` &nbsp;**[{it["name"]}]({it["url"]})**'
        if lang:
            line += f" &nbsp;<sub>{lang}</sub>"
        if desc:
            line += f" &nbsp;{desc}"
        L.append(f"- {line}")
    mix = " · ".join(f'{m["language"]} {m["percent"]:g}%' for m in r["language_mix_by_code_size"])
    L.append("")
    L.append(f"Code by size: {mix}")
    L.append("")
    L.append("</details>")
    L.append("")
    L.append(pic("assemblies", "Assemblies: six flagship projects drawn as isometric parts", P["github"] + "?tab=repositories"))
    L.append("")
    for name in P["flagships"]:
        letter, num, p, g = idx[name]
        L.append(f'- <sub>{letter}-{num:02d}</sub> **[{name}]({p["url"]})** {p["note"]}. <sub>{p["stack"]}</sub>')
    L.append("")
    L.append("<details>")
    total = sum(len(g["projects"]) for g in P["project_groups"])
    L.append(f"<summary><b>Parts list</b> &nbsp;<sub>all {total} projects in {len(P['project_groups'])} sub-assemblies</sub></summary>")
    L.append("")
    for g in P["project_groups"]:
        L.append(f'**{g["letter"]} · {g["name"].replace(" Vr", " VR")}**')
        L.append("")
        for p in g["projects"]:
            _, num, _, _ = idx[p["name"]]
            L.append(f'- <sub>{g["letter"]}-{num:02d}</sub> **[{p["name"]}]({p["url"]})** {p["note"]} <sub>{p["stack"]}</sub>')
        L.append("")
    pf = P["politicas_figures"]
    L.append("**politicas in numbers**")
    L.append("")
    L.append("| people in graph | current MPs | MPs with company ties | companies | public contracts | contract value | roll-call ballots | laws in registry |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    L.append(f'| {fmt(pf["people_in_graph"])} | {pf["current_mps"]} | {pf["mps_with_company_ties"]} | {pf["companies"]} | {fmt(pf["public_contracts"])} | CZK {pf["contracts_value_czk_bn"]} bn | {fmt(pf["roll_call_ballots"])} | {fmt(pf["laws_in_registry"])} |')
    L.append("")
    L.append(f'<sub>Source: {pf["source"]}.</sub>')
    L.append("")
    L.append("</details>")
    L.append("")
    vr = {v["file"]: v for v in P["vr"]}
    left, right = (vr[f] for f in P["vr_sheet"])
    proj = idx[left["project"]][2]
    L.append(pic("vr", f'{left["project"]} {left["kind"]}: {left["caption"]}. {right["project"]} {right["kind"]}: {right["caption"]}', proj["url"]))
    L.append("")
    L.append(f'**[{proj["name"]}]({proj["url"]})** {proj["note"]}.<br/>')
    L.append(f'<sub>Left: {left["kind"]}, {left["caption"]}. Right: {right["kind"]}, {right["caption"]}.</sub>')
    L.append("")
    L.append(pic("toolbox", "Standard parts: TypeScript, Rust, Python, C++, C#, React 19, Next.js 16, Tauri 2, Tailwind v4, SQLite, PostgreSQL, Firestore, Claude Code, MCP, LLM-as-judge, Ollama, Unreal Engine 5, Unity, Meta Quest"))
    L.append("")
    L.append(f'<p align="center"><sub>{P["handle"]} · {P["title"]} · sheets regenerated daily from live GitHub data · last fetch {S["fetched_at"][:10]}</sub></p>')
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- main

def build(P, S, out_dir, version=""):
    """Write the twelve sheets to out_dir/assets and the README to out_dir/README.md."""
    assets = os.path.join(out_dir, "assets")
    os.makedirs(assets, exist_ok=True)
    builders = {
        "title": lambda t: sheet_title(t, P, S),
        "spec": lambda t: sheet_spec(t, P),
        "log": lambda t: sheet_log(t, S),
        "assemblies": lambda t: sheet_assemblies(t, P, S),
        "vr": lambda t: sheet_vr(t, P),
        "toolbox": lambda t: sheet_toolbox(t, P, S),
    }
    for name, fn in builders.items():
        for theme, t in THEMES.items():
            svg = fn(t)
            sizes = [float(x) for x in re.findall(r'font-size="([\d.]+)"', svg)]
            assert not sizes or min(sizes) >= MIN_TYPE, (name, min(sizes))
            with open(os.path.join(assets, f"{name}-{theme}.svg"), "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(readme(P, S, version))
