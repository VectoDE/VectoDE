"""Builds the profile SVGs in /assets for every language and theme.

The profile borrows the look of a vector editor: canvas, rulers, selection
frames, anchor points and an inspector panel. Content lives in content.py.

Run: uv run --with fonttools --with brotli python .github/scripts/build_assets.py
"""

import base64
import json
import math
from pathlib import Path

from content import (BADGES, CERTS, FOOTER, HERO, HERO_STACK, ISSUERS, LANG_SWITCH, LANGS, LINKS, PROJECTS,
                     SECTIONS, SOCIAL, STATUS, SUPPORT, TIMELINE, TODAY)
from svgkit import (DISPLAY, SANS, SANS_BOLD, THEMES, chip, font_face, live_text, measure, num, svg_doc,
                    txt, wrap, write)

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"
LOGO_DIR = Path(__file__).resolve().parents[1] / "brand"
LOGO = "data:image/png;base64," + base64.b64encode((LOGO_DIR / "logo-canvas.png").read_bytes()).decode()
AVATAR = "data:image/png;base64," + base64.b64encode((LOGO_DIR / "logo-avatar.png").read_bytes()).decode()
BRAND = json.loads(Path(__file__).with_name("icons.json").read_text(encoding="utf-8"))["icons"]


def pt(p):
    return f"{num(p[0])},{num(p[1])}"


def shadow(t, dy=14, blur=18):
    return (f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="140%">'
            f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="{t["shadow"]}" flood-opacity="{t["shadowOpacity"]}"/></filter>')


class Loop:
    """SMIL helpers for one looping, eased timeline."""

    def __init__(self, dur, n):
        self.dur = dur
        self.keys = ";".join(num(i / (n - 1)) for i in range(n))
        self.splines = ";".join([".45 0 .55 1"] * (n - 1))

    def attr(self, name, values):
        return (f'<animate attributeName="{name}" dur="{self.dur}" repeatCount="indefinite" calcMode="spline" '
                f'keyTimes="{self.keys}" keySplines="{self.splines}" values="{";".join(values)}"/>')

    def move(self, values):
        return (f'<animateTransform attributeName="transform" type="translate" dur="{self.dur}" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="{self.keys}" keySplines="{self.splines}" values="{";".join(values)}"/>')


# ---------------------------------------------------------------- hero

def hero(t, lang):
    c = HERO[lang]
    W, H, M = 1280, 650, 18
    FW, FH = W - 2 * M, H - 2 * M
    TOP, RULER, PANEL = 56, 24, 316
    px = FW - PANEL
    o = []

    o.append(f'<rect width="{FW}" height="{FH}" fill="{t["bg"]}"/>')
    o.append(f'<rect x="{RULER}" y="{TOP + RULER}" width="{px}" height="{FH}" fill="url(#dots)"/>')
    o.append(f'<rect width="{px}" height="{FH}" fill="url(#glow)"/>')

    # curve being reshaped by a pointer
    loop = Loop("10s", 5)
    p0, p1, p2 = (578, 548), (782, 318), (902, 496)
    c1, c4 = (676, 548), (902, 412)
    frames = []
    for angle, left, right in [(0, 96, 82), (16, 84, 104), (-12, 110, 70), (8, 92, 96), (0, 96, 82)]:
        a = math.radians(angle)
        frames.append(dict(c2=(p1[0] - math.cos(a) * left, p1[1] - math.sin(a) * left),
                           c3=(p1[0] + math.cos(a) * right, p1[1] + math.sin(a) * right)))
    ds = [f"M {pt(p0)} C {pt(c1)} {pt(f['c2'])} {pt(p1)} C {pt(f['c3'])} {pt(c4)} {pt(p2)}" for f in frames]
    o.append(f'<path d="{ds[2]}" fill="none" stroke="{t["ghost"]}" stroke-width="1.5" stroke-dasharray="4 6"/>')
    o.append(f'<path class="draw" pathLength="1" d="{ds[0]}" fill="none" stroke="{t["blue"]}" stroke-width="3" stroke-linecap="round">{loop.attr("d", ds)}</path>')
    o.append(f'<path class="pulse" pathLength="1" d="{ds[0]}" fill="none" stroke="{t["text"]}" stroke-opacity=".9" stroke-width="3" stroke-linecap="round">{loop.attr("d", ds)}</path>')

    def handle(a, key=None, fixed=None):
        if fixed:
            return (f'<line x1="{a[0]}" y1="{a[1]}" x2="{fixed[0]}" y2="{fixed[1]}" stroke="{t["amber"]}" stroke-width="1.25"/>'
                    f'<circle cx="{fixed[0]}" cy="{fixed[1]}" r="4.5" fill="{t["bg"]}" stroke="{t["amber"]}" stroke-width="1.75"/>')
        xs = [num(f[key][0]) for f in frames]
        ys = [num(f[key][1]) for f in frames]
        return (f'<line x1="{a[0]}" y1="{a[1]}" x2="{xs[0]}" y2="{ys[0]}" stroke="{t["amber"]}" stroke-width="1.25">{loop.attr("x2", xs)}{loop.attr("y2", ys)}</line>'
                f'<circle cx="{xs[0]}" cy="{ys[0]}" r="4.5" fill="{t["bg"]}" stroke="{t["amber"]}" stroke-width="1.75">{loop.attr("cx", xs)}{loop.attr("cy", ys)}</circle>')

    o += [handle(p0, fixed=c1), handle(p1, "c2"), handle(p1, "c3"), handle(p2, fixed=c4)]
    for p, filled in [(p0, False), (p1, True), (p2, False)]:
        o.append(f'<rect x="{p[0] - 5.5}" y="{p[1] - 5.5}" width="11" height="11" fill="{t["blue"] if filled else t["bg"]}" stroke="{t["blue"]}" stroke-width="1.75"/>')

    cur = [f"{num(f['c3'][0])} {num(f['c3'][1])}" for f in frames]
    lw = measure(SANS_BOLD, "Tim", 11.5) + 14
    o.append(f'<g transform="translate({cur[0]})">{loop.move(cur)}'
             f'<path d="M1 1 L1 20 L6 15 L9.5 23 L13 21.5 L9.5 13.8 L16.5 13.8 Z" fill="{t["amber"]}" stroke="{t["bg"]}" stroke-width="1.5" stroke-linejoin="round"/>'
             f'<rect x="14" y="20" width="{num(lw)}" height="19" rx="5" fill="{t["amber"]}"/>'
             f'{txt(SANS_BOLD, "Tim", 11.5, 21, 33.5, t["onBlue"])}</g>')

    # name as the selected layer
    size, tr = 104, -1
    nw = measure(DISPLAY, "Tim Hauke", size, tr)
    bx, by, pad, bh = 64, 146, 22, 128
    bw = nw + pad * 2
    tag_w = measure(SANS_BOLD, "VectoDE", 12.5) + 18
    o.append(f'<g class="fade" style="animation-delay:.1s">')
    o.append(f'<rect x="{bx}" y="{by - 29}" width="{num(tag_w)}" height="21" rx="4" fill="{t["blue"]}"/>')
    o.append(txt(SANS_BOLD, "VectoDE", 12.5, bx + 9, by - 14, t["onBlue"]))
    o.append(f'<rect x="{bx}" y="{by}" width="{num(bw)}" height="{bh}" fill="none" stroke="{t["blue"]}" stroke-width="1.25"/>')
    for hx, hy in [(bx, by), (bx + bw / 2, by), (bx + bw, by), (bx, by + bh / 2), (bx + bw, by + bh / 2),
                   (bx, by + bh), (bx + bw / 2, by + bh), (bx + bw, by + bh)]:
        o.append(f'<rect x="{num(hx - 4.5)}" y="{num(hy - 4.5)}" width="9" height="9" fill="{t["bg"]}" stroke="{t["blue"]}" stroke-width="1.25"/>')
    o.append(txt(DISPLAY, "Tim Hauke", size, bx + pad, by + 100, t["text"], tracking=tr))
    dim = f"{round(bw)} × {bh}"
    dw = measure(SANS_BOLD, dim, 11) + 14
    o.append(f'<rect x="{num(bx + bw / 2 - dw / 2)}" y="{by + bh + 9}" width="{num(dw)}" height="19" rx="4" fill="{t["blue"]}"/>')
    o.append(txt(SANS_BOLD, dim, 11, bx + bw / 2, by + bh + 22.5, t["onBlue"], anchor="middle"))
    o.append("</g>")

    # rotating role line with a text caret
    ry = 360
    o.append(f'<rect class="caret" x="{bx}" y="{ry - 25}" width="2.5" height="32" rx="1" fill="{t["blue"]}"/>')
    o.append('<g clip-path="url(#roleclip)">')
    for i, role in enumerate(c["roles"]):
        o.append(f'<g class="role" style="animation-delay:{i * 3}s">{txt(SANS_BOLD, role, 28, bx + 16, ry, t["text"], tracking=-0.2)}</g>')
    o.append("</g>")
    o.append(f'<g class="fade" style="animation-delay:.5s">')
    o.append(txt(SANS, c["intro"][0], 19, bx, 410, t["muted"]))
    o.append(txt(SANS, c["intro"][1], 19, bx, 438, t["muted"]))
    x = bx
    for label, fill, color in [("www.uplytech.de", t["blueSoft"], t["blue"]), (LINKS["email_company"], t["raised"], t["muted"]),
                               ("github.com/VectoDE", t["raised"], t["muted"])]:
        svg, w = chip(label, x, 474, t, h=30, size=13, fill=fill, color=color)
        o.append(svg)
        x += w + 10
    o.append("</g>")

    # rulers with markers that follow the pointer
    ticks = []
    o.append(f'<rect y="{TOP}" width="{px}" height="{RULER}" fill="{t["panel"]}"/>')
    o.append(f'<rect y="{TOP}" width="{RULER}" height="{FH}" fill="{t["panel"]}"/>')
    for xx in range(RULER, px, 10):
        off = xx - RULER
        ticks.append(f"M{xx} {TOP + RULER}v-{9 if off % 100 == 0 else 5 if off % 50 == 0 else 3}")
        if off % 100 == 0 and off:
            o.append(txt(SANS, str(off), 8.5, xx + 3, TOP + 10.5, t["tickText"]))
    for yy in range(TOP + RULER, FH, 10):
        off = yy - TOP - RULER
        ticks.append(f"M{RULER} {yy}h-{9 if off % 100 == 0 else 5 if off % 50 == 0 else 3}")
        if off % 100 == 0 and off:
            o.append(f'<g transform="translate(10.5 {yy - 3}) rotate(-90)">{txt(SANS, str(off), 8.5, 0, 0, t["tickText"], anchor="end")}</g>')
    o.append(f'<path d="{" ".join(ticks)} M{RULER} {TOP + RULER}H{px} M{RULER} {TOP + RULER}V{FH}" stroke="{t["tick"]}" stroke-width="1"/>')
    mx = [f"{num(f['c3'][0])} 0" for f in frames]
    my = [f"0 {num(f['c3'][1])}" for f in frames]
    o.append(f'<g transform="translate({mx[0]})">{loop.move(mx)}<rect x="-1" y="{TOP}" width="2" height="{RULER}" fill="{t["amber"]}"/></g>')
    o.append(f'<g transform="translate({my[0]})">{loop.move(my)}<rect x="0" y="-1" width="{RULER}" height="2" fill="{t["amber"]}"/></g>')
    o.append(f'<rect y="{TOP}" width="{RULER}" height="{RULER}" fill="{t["panel"]}"/>')

    # zoom indicator
    zw = measure(SANS_BOLD, c["zoom"] + "  100%", 11.5) + 20
    o.append(f'<rect x="{px - zw - 16}" y="{FH - 44}" width="{num(zw)}" height="26" rx="7" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(txt(SANS_BOLD, c["zoom"] + "  100%", 11.5, px - zw - 6, FH - 26.5, t["muted"]))

    # toolbar
    o.append(f'<rect width="{FW}" height="{TOP}" fill="{t["panel"]}"/>')
    o.append(f'<path d="M0 {TOP - .5}H{FW}" stroke="{t["line"]}"/>')
    o.append(f'<image href="{LOGO}" x="16" y="5" width="34" height="46" preserveAspectRatio="xMidYMid meet"/>')
    o.append(txt(SANS_BOLD, "VectoDE", 14.5, 60, 33, t["text"]))
    o.append(txt(SANS, "/   profile.vec", 14.5, 60 + measure(SANS_BOLD, "VectoDE", 14.5) + 10, 33, t["faint"]))
    tools_x = FW / 2 - 130
    icons = [
        f'<path d="M-5 -7 L-5 7 L-1 3.5 L1.5 9 L4 8 L1.5 2.5 L6.5 2.5 Z" fill="{t["muted"]}"/>',
        f'<path d="M-3 -8V8M3 -8V8M-8 -3H8M-8 3H8" stroke="{t["muted"]}" stroke-width="1.5"/>',
        f'<path d="M0 -8 L5 1 L0 8 L-5 1 Z M0 1 V8" fill="none" stroke="{t["onBlue"]}" stroke-width="1.5" stroke-linejoin="round"/><circle r="1.6" fill="{t["onBlue"]}"/>',
        f'<rect x="-7" y="-6" width="14" height="12" rx="1.5" fill="none" stroke="{t["muted"]}" stroke-width="1.5"/>',
        f'<circle r="7" fill="none" stroke="{t["muted"]}" stroke-width="1.5"/>',
        f'<path d="M-6 -6H6M0 -6V7" stroke="{t["muted"]}" stroke-width="1.7" stroke-linecap="round"/>',
    ]
    for i, icon in enumerate(icons):
        cx = tools_x + i * 46
        if i == 2:
            o.append(f'<rect x="{cx - 17}" y="11" width="34" height="34" rx="9" fill="{t["blue"]}"/>')
        o.append(f'<g transform="translate({num(cx)} 28)">{icon}</g>')
    o.append(f'<path d="M{num(tools_x + 5 * 46 + 30)} 18V38" stroke="{t["line"]}"/>')
    o.append(f'<path d="M{num(tools_x - 30)} 18V38" stroke="{t["line"]}"/>')
    avail = c["available"]
    aw = measure(SANS_BOLD, avail, 12.5) + 40
    lang_w = 38
    ax = FW - 18 - 34 - 12 - lang_w - 10 - aw
    o.append(f'<rect x="{num(ax)}" y="13" width="{num(aw)}" height="30" rx="15" fill="{t["greenSoft"]}"/>')
    o.append(f'<circle class="live" cx="{num(ax + 17)}" cy="28" r="4" fill="{t["green"]}"/><circle cx="{num(ax + 17)}" cy="28" r="4" fill="{t["green"]}"/>')
    o.append(txt(SANS_BOLD, avail, 12.5, ax + 29, 32.5, t["green"]))
    lx = FW - 18 - 34 - 12 - lang_w
    o.append(f'<rect x="{lx}" y="13" width="{lang_w}" height="30" rx="8" fill="{t["raised"]}"/>')
    o.append(txt(SANS_BOLD, lang.upper(), 12.5, lx + lang_w / 2, 32.5, t["muted"], anchor="middle"))
    o.append(f'<circle cx="{FW - 35}" cy="28" r="17" fill="{t["raised"]}"/>')
    o.append(f'<image href="{AVATAR}" x="{FW - 52}" y="11" width="34" height="34" clip-path="url(#avatar)"/>')
    o.append(f'<circle cx="{FW - 35}" cy="28" r="17" fill="none" stroke="{t["amber"]}" stroke-width="1.5"/>')

    # inspector
    x0, x1 = px + 24, FW - 24
    o.append(f'<rect x="{px}" y="{TOP}" width="{PANEL}" height="{FH - TOP}" fill="{t["panel"]}"/>')
    o.append(f'<path d="M{px + .5} {TOP}V{FH}" stroke="{t["line"]}"/>')
    tab1, tab2 = c["panel_tabs"]
    o.append(txt(SANS_BOLD, tab1, 13, x0, TOP + 30, t["text"]))
    o.append(f'<rect x="{x0}" y="{TOP + 41}" width="{num(measure(SANS_BOLD, tab1, 13))}" height="2" rx="1" fill="{t["blue"]}"/>')
    o.append(txt(SANS, tab2, 13, x0 + measure(SANS_BOLD, tab1, 13) + 22, TOP + 30, t["faint"]))
    y = TOP + 44
    o.append(f'<path d="M{px} {y}H{FW}" stroke="{t["line"]}"/>')
    o.append(f'<path d="M{x0} {y + 25}h10M{x0} {y + 31}h10M{x0 + 3} {y + 22}v12M{x0 + 7} {y + 22}v12" stroke="{t["blue"]}" stroke-width="1.3"/>')
    o.append(txt(SANS_BOLD, "Tim Hauke", 13.5, x0 + 20, y + 33, t["text"]))
    o.append(txt(SANS, c["layer"], 12, x1, y + 33, t["faint"], anchor="end"))
    y += 54
    o.append(f'<path d="M{px} {y}H{FW}" stroke="{t["line"]}"/>')
    o.append(txt(SANS_BOLD, c["profile_title"], 12, x0, y + 26, t["muted"]))
    y += 50
    for label, value in c["profile"]:
        o.append(txt(SANS, label, 12.5, x0, y, t["faint"]))
        o.append(txt(SANS, value, 12.5, x0 + 108, y, t["text"]))
        y += 24
    y += 6
    o.append(f'<path d="M{px} {y}H{FW}" stroke="{t["line"]}"/>')
    o.append(txt(SANS_BOLD, c["stack_title"], 12, x0, y + 26, t["muted"]))
    cx_, cy_ = x0, y + 40
    for item in HERO_STACK:
        w = measure(SANS_BOLD, item, 11.5) + 20
        if cx_ + w > x1:
            cx_, cy_ = x0, cy_ + 30
        svg, w = chip(item, cx_, cy_, t, h=23, size=11.5)
        o.append(svg)
        cx_ += w + 6
    y = cy_ + 40
    o.append(f'<path d="M{px} {y}H{FW}" stroke="{t["line"]}"/>')
    o.append(txt(SANS_BOLD, c["status_title"], 12, x0, y + 26, t["muted"]))
    o.append(f'<rect x="{x0}" y="{y + 40}" width="{x1 - x0}" height="40" rx="9" fill="{t["raised"]}" stroke="{t["line"]}"/>')
    o.append(f'<circle class="live" cx="{x0 + 19}" cy="{y + 60}" r="4.5" fill="{t["green"]}"/><circle cx="{x0 + 19}" cy="{y + 60}" r="4.5" fill="{t["green"]}"/>')
    o.append("<!-- STATUS: change the text in the next line -->")
    o.append(live_text(STATUS, x0 + 36, y + 65.5, 15, t["text"]))

    share = 100 / len(c["roles"])
    style = f"""{font_face()}
    .draw {{ stroke-dasharray: 1; animation: draw 1.8s cubic-bezier(.65,0,.35,1) .3s backwards; }}
    .pulse {{ stroke-dasharray: .08 .92; animation: run 3.4s linear infinite; }}
    .live {{ transform-box: fill-box; transform-origin: center; animation: live 2.2s ease-out infinite; }}
    .fade {{ animation: fade .8s ease-out backwards; }}
    .role {{ opacity: 0; animation: role {len(c['roles']) * 3}s cubic-bezier(.2,.7,.2,1) infinite; }}
    .caret {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes run {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes live {{ 0% {{ opacity: .55; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(3.2); }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes role {{ 0% {{ opacity: 0; transform: translateY(26px); }} {share * .12:.1f}%, {share * .82:.1f}% {{ opacity: 1; transform: none; }} {share:.1f}%, 100% {{ opacity: 0; transform: translateY(-26px); }} }}
    @keyframes blink {{ 0%, 50% {{ opacity: 1; }} 50.01%, 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .draw, .pulse, .live, .fade, .caret {{ animation: none; stroke-dashoffset: 0; opacity: 1; }}
      .pulse, .live {{ opacity: 0; }}
      .role {{ animation: none; opacity: 0; }} .role:first-child {{ opacity: 1; }}
    }}"""
    defs = f"""
    {shadow(t)}
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse" x="{RULER}" y="{TOP + RULER}"><circle cx="1" cy="1" r="1" fill="{t["dot"]}"/></pattern>
    <radialGradient id="glow" cx="0.72" cy="0.66" r="0.62"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glowOpacity"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["sheen"]}"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
    <clipPath id="avatar"><circle cx="{FW - 35}" cy="28" r="16.25"/></clipPath>
    <clipPath id="frame"><rect width="{FW}" height="{FH}" rx="18"/></clipPath>
    <clipPath id="roleclip"><rect x="{bx}" y="{ry - 34}" width="{px - bx - 40}" height="46"/></clipPath>"""
    body = (f'<g transform="translate({M} {M})">'
            f'<rect width="{FW}" height="{FH}" rx="18" fill="{t["bg"]}" filter="url(#shadow)"/>'
            f'<g clip-path="url(#frame)">\n  {chr(10).join(o)}\n  </g>'
            f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="17.5" fill="none" stroke="{t["frame"]}"/>'
            f'<rect x="1" y="1" width="{FW - 2}" height="40" rx="17" fill="url(#sheen)" pointer-events="none"/></g>')
    desc = {"en": f"Tim Hauke, founder of UplyTech and full-stack developer from Itzehoe, Germany. Currently building {STATUS}.",
            "de": f"Tim Hauke, Gründer von UplyTech und Full-Stack-Entwickler aus Itzehoe. Aktuelles Projekt: {STATUS}."}[lang]
    return svg_doc(W, H, "Tim Hauke (VectoDE)", desc, body, style, defs)


# ---------------------------------------------------------------- section headers

def header(t, title, note):
    W, H, M = 1280, 92, 8
    FW, FH = W - 2 * M, H - 2 * M - 6
    tw = measure(DISPLAY, title, 31, -0.2)
    nx = 64 + tw + 16
    nw = measure(SANS, note, 14)
    lx = nx + nw + 20
    o = [f'<rect width="{FW}" height="{FH}" rx="14" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="13.5" fill="none" stroke="{t["frame"]}"/>',
         f'<rect x="20" y="{FH / 2 - 15}" width="30" height="30" rx="8" fill="{t["blueSoft"]}"/>',
         f'<path d="M30 {FH / 2 - 3}h10M30 {FH / 2 + 3}h10M33 {FH / 2 - 7}v14M37 {FH / 2 - 7}v14" stroke="{t["blue"]}" stroke-width="1.6"/>',
         txt(DISPLAY, title, 31, 64, FH / 2 + 11, t["text"], tracking=-0.2),
         txt(SANS, note, 14, nx, FH / 2 + 5, t["faint"]),
         f'<path class="draw" pathLength="1" d="M{num(lx)} {FH / 2}H{FW - 44}" stroke="{t["line"]}" stroke-width="1.5"/>',
         f'<rect class="pop" x="{FW - 40}" y="{FH / 2 - 6}" width="12" height="12" fill="{t["blue"]}"/>']
    style = f"""
    .draw {{ stroke-dasharray: 1; animation: draw 1.4s cubic-bezier(.65,0,.35,1) .2s backwards; }}
    .pop {{ animation: pop .4s ease-out 1.4s backwards; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .draw {{ animation: none; stroke-dashoffset: 0; }} .pop {{ animation: none; opacity: 1; }} }}"""
    return svg_doc(W, H, title, title, f'<g transform="translate({M} {M})">{"".join(o)}</g>', style, shadow(t, dy=6, blur=8))


# ---------------------------------------------------------------- project icons (animated)

def icon(kind, t, cx, cy):
    b, a, g = t["blue"], t["amber"], t["green"]
    s = f'stroke="{b}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    filled = s.replace('fill="none"', f'fill="{t["blueSoft"]}"')
    if kind == "sun":
        rays = "".join(f'<path d="M0 -17V-22" transform="rotate({i * 45})"/>' for i in range(8))
        return (f'<g transform="translate({cx} {cy})"><circle r="10" {filled}/>'
                f'<g stroke="{a}" stroke-width="2.2" stroke-linecap="round">{rays}'
                f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="24s" repeatCount="indefinite"/></g></g>')
    if kind == "wave":
        bars = []
        for i, (lo, hi, dur) in enumerate([(8, 22, ".9s"), (12, 34, "1.1s"), (6, 40, ".8s"), (10, 28, "1.3s"), (6, 18, "1s")]):
            x = cx - 22 + i * 10
            bars.append(f'<rect x="{x - 2.5}" y="{cy - lo / 2}" width="5" height="{lo}" rx="2.5" fill="{b if i != 2 else a}">'
                        f'<animate attributeName="height" values="{lo};{hi};{lo}" dur="{dur}" repeatCount="indefinite"/>'
                        f'<animate attributeName="y" values="{cy - lo / 2};{cy - hi / 2};{cy - lo / 2}" dur="{dur}" repeatCount="indefinite"/></rect>')
        return "".join(bars)
    if kind == "nodes":
        pts = [(cx - 18, cy - 12), (cx + 16, cy - 16), (cx + 14, cy + 16), (cx - 14, cy + 16)]
        path = f"M{pt(pts[0])} L{pt(pts[1])} L{pt(pts[2])} L{pt(pts[3])} Z"
        return (f'<path id="np" d="{path}" stroke="{t["line"]}" stroke-width="2" fill="none"/>'
                f'<path d="M{pt(pts[0])} L{pt(pts[2])}" stroke="{t["line"]}" stroke-width="2"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{t["panel"]}" stroke="{b}" stroke-width="2.2"/>' for x, y in pts)
                + f'<circle r="3.5" fill="{a}"><animateMotion dur="4s" repeatCount="indefinite" path="{path}"/></circle>')
    if kind == "terminal":
        return (f'<rect x="{cx - 24}" y="{cy - 18}" width="48" height="36" rx="7" {s}/>'
                f'<path d="M{cx - 14} {cy - 6} L{cx - 7} {cy} L{cx - 14} {cy + 6}" {s}/>'
                f'<rect x="{cx - 2}" y="{cy + 4}" width="12" height="3" rx="1.5" fill="{a}">'
                f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    if kind == "sync":
        arc = (f'<path d="M-15 -4 A16 16 0 0 1 12 -10" {s}/><path d="M7 -15 L12 -10 L6 -6" {s}/>'
               f'<path d="M15 4 A16 16 0 0 1 -12 10" {s}/><path d="M-7 15 L-12 10 L-6 6" {s}/>')
        return (f'<g transform="translate({cx} {cy})"><g>{arc}<animateTransform attributeName="transform" type="rotate" '
                f'from="0" to="360" dur="6s" repeatCount="indefinite"/></g><circle r="3.5" fill="{a}"/></g>')
    if kind == "server":
        out = []
        for i in range(3):
            y = cy - 20 + i * 14
            out.append(f'<rect x="{cx - 22}" y="{y}" width="44" height="11" rx="3" {s}/>')
            out.append(f'<circle cx="{cx + 14}" cy="{y + 5.5}" r="2.2" fill="{g}"><animate attributeName="opacity" '
                       f'values="1;.2;1" dur="{1.2 + i * .45}s" repeatCount="indefinite"/></circle>')
            out.append(f'<path d="M{cx - 15} {y + 5.5}h10" stroke="{t["line"]}" stroke-width="2" stroke-linecap="round"/>')
        return "".join(out)
    if kind == "window":
        lines = "".join(f'<rect x="{cx - 16}" y="{cy - 2 + i * 8}" width="{w}" height="3.5" rx="1.75" fill="{t["line"]}">'
                        f'<animate attributeName="width" values="{w};{w2};{w}" dur="{d}s" repeatCount="indefinite"/></rect>'
                        for i, (w, w2, d) in enumerate([(30, 18, 3), (20, 30, 3.6), (26, 14, 4.2)]))
        return (f'<rect x="{cx - 24}" y="{cy - 20}" width="48" height="40" rx="7" {s}/>'
                f'<path d="M{cx - 24} {cy - 9}H{cx + 24}" stroke="{b}" stroke-width="2.2"/>'
                + "".join(f'<circle cx="{cx - 17 + i * 6}" cy="{cy - 14.5}" r="1.8" fill="{c}"/>' for i, c in enumerate([a, b, g]))
                + lines)
    if kind == "orbit":
        orbit = f"M{cx - 25},{cy} a25,9 0 1,0 50,0 a25,9 0 1,0 -50,0"
        return (f'<g transform="rotate(-20 {cx} {cy})"><path d="{orbit}" stroke="{t["line"]}" stroke-width="2" fill="none"/>'
                f'<circle cx="{cx}" cy="{cy}" r="10" {filled}/>'
                f'<circle r="4" fill="{a}"><animateMotion dur="5s" repeatCount="indefinite" path="{orbit}"/></circle></g>')
    return ""


# ---------------------------------------------------------------- project cards

def card(t, lang, name, status, text, stack, kind):
    W, H, M = 640, 316, 12
    FW, FH = W - 2 * M, H - 2 * M - 8
    live = status.startswith("Live")
    o = [f'<rect width="{FW}" height="{FH}" rx="16" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="15.5" fill="none" stroke="{t["frame"]}"/>',
         f'<rect x="1" y="1" width="{FW - 2}" height="30" rx="15" fill="url(#sheen)"/>']
    o.append(f'<rect x="{FW - 92}" y="22" width="68" height="68" rx="16" fill="{t["raised"]}" stroke="{t["line"]}"/>')
    o.append(icon(kind, t, FW - 58, 56))
    sw = measure(SANS_BOLD, status, 12) + (36 if live else 20)
    fill, color = (t["greenSoft"], t["green"]) if live else (t["blueSoft"], t["blue"])
    o.append(f'<rect x="28" y="28" width="{num(sw)}" height="25" rx="12.5" fill="{fill}"/>')
    if live:
        o.append(f'<circle class="live" cx="42" cy="40.5" r="3.5" fill="{color}"/><circle cx="42" cy="40.5" r="3.5" fill="{color}"/>')
    o.append(txt(SANS_BOLD, status, 12, 28 + (26 if live else 10), 44.8, color))
    o.append(txt(DISPLAY, name, 36, 28, 114, t["text"], tracking=-0.3))
    y = 150
    for line in wrap(SANS, text, 16.5, FW - 60)[:3]:
        o.append(txt(SANS, line, 16.5, 28, y, t["muted"]))
        y += 24.5
    x = 28
    for item in stack:
        svg, w = chip(item, x, FH - 52, t, h=26, size=12)
        o.append(svg)
        x += w + 7
    o.append(f'<circle cx="{FW - 44}" cy="{FH - 39}" r="17" fill="{t["raised"]}" stroke="{t["line"]}"/>')
    o.append(f'<path d="M{FW - 49} {FH - 34} L{FW - 39} {FH - 44} M{FW - 47} {FH - 44} H{FW - 39} V{FH - 36}" fill="none" stroke="{t["text"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    style = """.live { transform-box: fill-box; transform-origin: center; animation: live 2.2s ease-out infinite; }
    @keyframes live { 0% { opacity: .55; transform: scale(1); } 100% { opacity: 0; transform: scale(3.2); } }
    @media (prefers-reduced-motion: reduce) { .live { animation: none; opacity: 0; } }"""
    defs = shadow(t, dy=8, blur=10) + f'<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["sheen"]}"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
    return svg_doc(W, H, name, f"{name}. {status}. {text}", f'<g transform="translate({M} {M})">{"".join(o)}</g>', style, defs)


# ---------------------------------------------------------------- timeline

def timeline(t, lang):
    items = TIMELINE[lang]
    W, H, M = 1280, 360, 12
    FW, FH = W - 2 * M, H - 2 * M - 8
    n = len(items)
    step = (FW - 2 * 90) / (n - 1)
    xs = [90 + i * step for i in range(n)]
    ys = [266 - i * (150 / (n - 1)) for i in range(n)]
    pts = list(zip(xs, ys))
    d = f"M {pt(pts[0])}"
    for a, b in zip(pts, pts[1:]):
        k = (b[0] - a[0]) * 0.5
        d += f" C {pt((a[0] + k, a[1]))} {pt((b[0] - k, b[1]))} {pt(b)}"
    o = [f'<rect width="{FW}" height="{FH}" rx="16" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect x="1" y="1" width="{FW - 2}" height="{FH - 2}" rx="15" fill="url(#dots)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="15.5" fill="none" stroke="{t["frame"]}"/>',
         f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{t["blue"]}" stroke-width="3" stroke-linecap="round"/>',
         f'<path class="pulse" pathLength="1" d="{d}" fill="none" stroke="{t["text"]}" stroke-opacity=".9" stroke-width="3" stroke-linecap="round"/>']
    for i, ((year, lines), (x, y)) in enumerate(zip(items, pts)):
        last = i == len(items) - 1
        delay = 0.3 + i * 0.25
        o.append(f'<g class="pop" style="animation-delay:{delay:.2f}s">')
        hl = min(44, step * 0.28)
        o.append(f'<line x1="{x - hl}" y1="{y}" x2="{x + hl}" y2="{y}" stroke="{t["amber"]}" stroke-width="1.2" opacity=".75"/>')
        for hx in (x - hl, x + hl):
            o.append(f'<circle cx="{hx}" cy="{y}" r="3.5" fill="{t["panel"]}" stroke="{t["amber"]}" stroke-width="1.5"/>')
        o.append(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" fill="{t["blue"] if last else t["panel"]}" stroke="{t["blue"]}" stroke-width="2"/>')
        o.append(txt(DISPLAY, year, 27, x, y - 76, t["text"], anchor="middle"))
        o.append(txt(SANS, lines[0], 13.5, x, y - 54, t["muted"], anchor="middle"))
        o.append(txt(SANS, lines[1], 13.5, x, y - 35, t["muted"], anchor="middle"))
        o.append("</g>")
    lx, ly = xs[-1], ys[-1]
    tw = measure(SANS_BOLD, TODAY[lang], 12) + 20
    o.append(f'<g class="pop" style="animation-delay:1.9s"><rect x="{num(lx - tw / 2)}" y="{ly + 20}" width="{num(tw)}" height="22" rx="11" fill="{t["blue"]}"/>'
             f'{txt(SANS_BOLD, TODAY[lang], 12, lx, ly + 35, t["onBlue"], anchor="middle")}</g>')
    style = """.draw { stroke-dasharray: 1; animation: draw 2s cubic-bezier(.65,0,.35,1) .2s backwards; }
    .pulse { stroke-dasharray: .05 .95; stroke-dashoffset: 1; animation: run 6s linear 2.2s infinite; opacity: 0; }
    .pop { animation: pop .6s ease-out backwards; }
    @keyframes draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
    @keyframes run { 0% { stroke-dashoffset: 1; opacity: 1; } 100% { stroke-dashoffset: 0; opacity: 1; } }
    @keyframes pop { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
    @media (prefers-reduced-motion: reduce) { .draw { animation: none; stroke-dashoffset: 0; } .pop { animation: none; opacity: 1; } .pulse { display: none; } }"""
    defs = shadow(t, dy=8, blur=10) + f'<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["dot"]}"/></pattern>'
    title = {"en": f"Timeline {items[0][0]} to {items[-1][0]}", "de": f"Werdegang {items[0][0]} bis {items[-1][0]}"}[lang]
    return svg_doc(W, H, title, "; ".join(f"{y}: {' '.join(ls)}" for y, ls in items),
                   f'<g transform="translate({M} {M})">{"".join(o)}</g>', style, defs)


# ---------------------------------------------------------------- footer

def footer(t, lang):
    f = FOOTER[lang]
    W, H, M = 1280, 262, 12
    FW, FH = W - 2 * M, H - 2 * M - 8
    loop = Loop("8s", 5)
    p0, p1 = (900, 184), (1196, 62)
    c1s = [(1000, 184), (1020, 140), (970, 204), (1010, 166), (1000, 184)]
    c2s = [(1090, 62), (1070, 104), (1120, 44), (1080, 78), (1090, 62)]
    ds = [f"M {pt(p0)} C {pt(a)} {pt(b)} {pt(p1)}" for a, b in zip(c1s, c2s)]
    o = [f'<rect width="{FW}" height="{FH}" rx="16" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect width="{FW}" height="{FH}" rx="16" fill="url(#glow)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="15.5" fill="none" stroke="{t["frame"]}"/>',
         txt(DISPLAY, f["head"], 42, 44, 80, t["text"], tracking=-0.4),
         txt(SANS, f["sub"], 17, 44, 114, t["muted"])]
    o.append(txt(SANS_BOLD, f["business"], 12, 44, 152, t["faint"]))
    x = 44
    for i, mail in enumerate([LINKS["email_company"], LINKS["email"]]):
        svg, w = chip(mail, x, 162, t, h=36, size=14, fill=t["blue"] if i == 0 else t["raised"], color=t["onBlue"] if i == 0 else t["text"])
        o.append(svg)
        x += w + 10
    px_ = x + 22
    o.append(f'<path d="M{num(px_ - 12)} 146V198" stroke="{t["line"]}"/>')
    o.append(txt(SANS_BOLD, f["private"], 12, px_, 152, t["faint"]))
    svg, _ = chip(LINKS["email_private"], px_, 162, t, h=36, size=14, fill=t["greenSoft"], color=t["green"])
    o.append(svg)
    o.append(f'<path d="{ds[0]}" fill="none" stroke="{t["blue"]}" stroke-width="3" stroke-linecap="round">{loop.attr("d", ds)}</path>')
    for anchor, cs in [(p0, c1s), (p1, c2s)]:
        xs, ys = [num(c[0]) for c in cs], [num(c[1]) for c in cs]
        o.append(f'<line x1="{anchor[0]}" y1="{anchor[1]}" x2="{xs[0]}" y2="{ys[0]}" stroke="{t["amber"]}" stroke-width="1.25">{loop.attr("x2", xs)}{loop.attr("y2", ys)}</line>')
        o.append(f'<circle cx="{xs[0]}" cy="{ys[0]}" r="4.5" fill="{t["panel"]}" stroke="{t["amber"]}" stroke-width="1.75">{loop.attr("cx", xs)}{loop.attr("cy", ys)}</circle>')
    o.append(f'<rect x="{p0[0] - 5.5}" y="{p0[1] - 5.5}" width="11" height="11" fill="{t["panel"]}" stroke="{t["blue"]}" stroke-width="1.75"/>')
    o.append(f'<rect x="{p1[0] - 5.5}" y="{p1[1] - 5.5}" width="11" height="11" fill="{t["blue"]}" stroke="{t["blue"]}" stroke-width="1.75"/>')
    defs = (shadow(t, dy=8, blur=10) +
            f'<radialGradient id="glow" cx="0.85" cy="0.3" r="0.5"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glowOpacity"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>')
    desc = f'{f["head"]} {f["sub"]} {LINKS["email_company"]}, {LINKS["email"]}; {f["private"]}: {LINKS["email_private"]}'
    return svg_doc(W, H, f["head"], desc, f'<g transform="translate({M} {M})">{"".join(o)}</g>', "", defs)


# ---------------------------------------------------------------- language switch

def lang_segment(t, label, active, side):
    W, H = 132, 44
    r = 12
    x0, x1, y0, y1 = 1, W - (0 if side == "left" else 1), 4, H - 4
    if side == "left":
        d = f"M{x1} {y0} H{x0 + r} A{r} {r} 0 0 0 {x0} {y0 + r} V{y1 - r} A{r} {r} 0 0 0 {x0 + r} {y1} H{x1} Z"
    else:
        x0 = 0
        d = f"M{x0} {y0} H{x1 - r} A{r} {r} 0 0 1 {x1} {y0 + r} V{y1 - r} A{r} {r} 0 0 1 {x1 - r} {y1} H{x0} Z"
    fill = t["blue"] if active else t["panel"]
    color = t["onBlue"] if active else t["muted"]
    o = [f'<path d="{d}" fill="{fill}" stroke="{t["blue"] if active else t["frame"]}"/>']
    if active:
        o.append(f'<path d="M{W / 2 - measure(SANS_BOLD, label, 14) / 2 - 18} {H / 2} l4 4 l7 -8" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(txt(SANS_BOLD, label, 14, W / 2 + 7, H / 2 + 5, color, anchor="middle"))
    else:
        o.append(txt(SANS_BOLD, label, 14, W / 2, H / 2 + 5, color, anchor="middle"))
    return svg_doc(W, H, label, label, "".join(o))


# ---------------------------------------------------------------- badges

# Line icons on a 24 px grid, drawn as strokes.
GLYPHS = {
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 4.5l-3 15"/>',
    "building": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7.5h1.5M13.5 7.5H15M9 11.5h1.5M13.5 11.5H15M10 21v-4.5h4V21"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.6 13.3 7.5 21l4.5-2.6 4.5 2.6-1.1-7.7"/>',
    "chat": '<path d="M4 5.5h16v10.5H10l-5 4v-4H4z"/><path d="M8.5 10.5h7"/>',
}


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in c]
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def badge(t, glyph, label, value, color=None, index=0):
    """Pill badge: icon, optional muted label, value. Same type and theme as the other assets."""
    H, size = 34, 13
    live = glyph == "live"
    x = 13
    o = []
    if live:
        o.append(f'<circle class="ping" cx="{x + 7}" cy="{H / 2}" r="4" fill="{t["green"]}"/><circle cx="{x + 7}" cy="{H / 2}" r="4" fill="{t["green"]}"/>')
    elif glyph in GLYPHS:
        o.append(f'<g transform="translate({x - 1} {H / 2 - 8}) scale(.6667)" fill="none" stroke="{t["blue"]}" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>')
    else:
        fill = f"#{color}" if color and contrast(f"#{color}", t["panel"]) >= 2.4 else t["text"]
        o.append(f'<g transform="translate({x - 1} {H / 2 - 8}) scale(.6667)"><path d="{BRAND[glyph.split("-")[0]]}" fill="{fill}"/></g>')
    x += 16 + 9
    if label:
        o.append(txt(SANS, label, size, x, H / 2 + 4.6, t["muted"]))
        x += measure(SANS, label, size) + 8
        o.append(f'<path d="M{num(x - .5)} 11V23" stroke="{t["line"]}"/>')
        x += 8
    o.append(txt(SANS_BOLD, value, size, x, H / 2 + 4.6, t["green"] if live else t["text"]))
    W = math.ceil(x + measure(SANS_BOLD, value, size) + 15)
    frame = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{(H - 1) / 2}" '
             f'fill="{t["greenSoft"] if live else t["panel"]}" stroke="{t["green"] if live else t["frame"]}" '
             f'stroke-opacity="{".45" if live else "1"}"/>')
    sheen = (f'<g clip-path="url(#pill)"><rect class="sheen" x="-60" y="0" width="44" height="{H}" fill="url(#shine)" '
             f'style="animation-delay:{1.2 + index * .35:.2f}s"/></g>')
    style = f""".sheen {{ animation: sweep 7s cubic-bezier(.4,0,.2,1) infinite; }}
    .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2.2s ease-out infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(0); }} 22%, 100% {{ transform: translateX({W + 120}px); }} }}
    @keyframes ping {{ 0% {{ opacity: .55; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(3); }} }}
    {REDUCED}"""
    defs = (f'<clipPath id="pill"><rect width="{W}" height="{H}" rx="{H / 2}"/></clipPath>'
            f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["shine"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{t["shine"]}" stop-opacity="{t["shineOpacity"]}"/>'
            f'<stop offset="1" stop-color="{t["shine"]}" stop-opacity="0"/></linearGradient>')
    text = f"{label}: {value}" if label else value
    return svg_doc(W, H, text, text, frame + "".join(o) + sheen, style, defs)


def pick(v, lang):
    return v[lang] if isinstance(v, dict) else v


def badges(t, theme):
    for row in BADGES.values():
        for i, (key, glyph, label, value, _href) in enumerate(row):
            for lang in LANGS:
                write(f"badges/{key}-{lang}-{theme}.svg", badge(t, glyph, pick(label, lang), pick(value, lang), index=i))
    for group in SOCIAL + [SUPPORT]:
        for i, (name, color, slug, _fg, _href) in enumerate(group):
            write(f"badges/{slug}-{theme}.svg", badge(t, slug, None, name, color, index=i))
    for i, (key, name, glyph, color) in enumerate(ISSUERS):
        count = sum(1 for c in CERTS if c[2] == name)
        write(f"badges/issuer-{key}-{theme}.svg", badge(t, glyph, name, str(count), color, index=i))


if __name__ == "__main__":
    for theme, t in THEMES.items():
        for lang in LANGS:
            write(f"hero-{lang}-{theme}.svg", hero(t, lang))
            write(f"timeline-{lang}-{theme}.svg", timeline(t, lang))
            write(f"footer-{lang}-{theme}.svg", footer(t, lang))
            for key, texts in SECTIONS.items():
                title, note = texts[lang]
                write(f"h-{key}-{lang}-{theme}.svg", header(t, title, note.format(count=len(CERTS))))
            for key, name, _url, kind, status, text, stack in PROJECTS:
                write(f"card-{key}-{lang}-{theme}.svg", card(t, lang, name, status[lang], text[lang], stack, kind))
        for lang, label in LANG_SWITCH.items():
            side = "left" if lang == "en" else "right"
            write(f"lang-{lang}-on-{theme}.svg", lang_segment(t, label, True, side))
            write(f"lang-{lang}-off-{theme}.svg", lang_segment(t, label, False, side))
        badges(t, theme)
    print("assets written")
