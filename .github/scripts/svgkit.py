"""Shared drawing helpers for the profile SVGs.

Static text is converted to vector outlines so it looks the same everywhere
(GitHub serves README images without web fonts). Text that changes, such as the
hero status or the stats numbers, stays a real <text> element and uses an
embedded Onest subset instead.

Fonts: Gloock and Onest, SIL Open Font License,
see .github/fonts/*-OFL.txt.
"""

import base64
import io
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / ".github" / "fonts"
OUT = ROOT / "assets"

DISPLAY = TTFont(FONTS / "Gloock-Regular.ttf")
SANS = TTFont(FONTS / "Onest-Regular.ttf")
SANS_BOLD = TTFont(FONTS / "Onest-SemiBold.ttf")

THEMES = {
    "dark": dict(
        bg="#0C1424", panel="#0F1A2E", raised="#132039", line="#22324F", dot="#1D2A42",
        glow="#2B6CD9", tick="#2A3A56", tickText="#53668A", text="#EEF3FB", muted="#93A4BF",
        faint="#5F7392", blue="#4C9AFF", blueSoft="#16305A", amber="#FFB547", green="#3DD68C",
        greenSoft="#123B2C", onBlue="#0C1424", ghost="#2E4366",
        frame="#24365A", shadow="#000000", shadowOpacity=".45", glowOpacity=".22", sheen=".05",
        shine="#FFFFFF", shineOpacity=".10", bronze="#D98A5B",
    ),
    "light": dict(
        bg="#F7F9FC", panel="#FFFFFF", raised="#EEF2F8", line="#D9E1EC", dot="#D3DCE9",
        glow="#7FB0FF", tick="#C2CDDC", tickText="#8494AD", text="#0C1424", muted="#51627C",
        faint="#8A99B0", blue="#1F6FEB", blueSoft="#DCE9FD", amber="#C27A00", green="#14955A",
        greenSoft="#D8F3E6", onBlue="#FFFFFF", ghost="#B9C8DE",
        frame="#D5DEEA", shadow="#1B2B4B", shadowOpacity=".12", glowOpacity=".20", sheen=".6",
        shine="#1F6FEB", shineOpacity=".10", bronze="#A65A2E",
    ),
}

STACK = "'Segoe UI', Helvetica, Arial, sans-serif"


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def measure(font, text, size, tracking=0.0):
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    scale = size / font["head"].unitsPerEm
    return sum(hmtx[cmap[ord(c)]][0] * scale + tracking for c in text) - (tracking if text else 0)


def text_path(font, text, size, x, y, tracking=0.0, anchor="start"):
    """SVG path data for text on baseline (x, y). anchor: start | middle | end."""
    width = measure(font, text, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(glyph_set, num)
    cursor = x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise ValueError(f"glyph missing for {ch!r}")
        glyph_set[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        cursor += hmtx[name][0] * scale + tracking
    return pen.getCommands()


def txt(font, text, size, x, y, fill, tracking=0.0, anchor="start"):
    return f'<path d="{text_path(font, text, size, x, y, tracking, anchor)}" fill="{fill}"/>'


def wrap(font, text, size, max_width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if measure(font, trial, size) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


_font_uri = None


def font_face():
    """@font-face rule with an Onest subset (Latin-1 + punctuation) as woff2."""
    global _font_uri
    if _font_uri is None:
        options = subset.Options()
        options.flavor = "woff2"  # type: ignore[assignment]
        options.layout_features = ["kern", "liga"]
        font = TTFont(FONTS / "Onest-Regular.ttf")
        sub = subset.Subsetter(options)
        sub.populate(unicodes=[*range(0x20, 0x7F), *range(0xA0, 0x100), 0x2013, 0x2014, 0x2019,
                               0x201C, 0x201D, 0x201E, 0x2022, 0x2026, 0x20AC, 0x2192])
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        _font_uri = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
    return f'@font-face {{ font-family: HeroSans; src: url({_font_uri}) format("woff2"); }}'


def live_text(text, x, y, size, fill, anchor="start", weight=400):
    return (f'<text x="{num(x)}" y="{num(y)}" font-family="HeroSans, {STACK}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>')


def chip(label, x, y, t, h=24, size=12.5, fill=None, color=None):
    """Rounded tag; returns (svg, width)."""
    w = measure(SANS_BOLD, label, size) + 20
    svg = (f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" rx="6" fill="{fill or t["raised"]}"/>'
           + txt(SANS_BOLD, label, size, x + 10, y + h / 2 + size * 0.36, color or t["muted"]))
    return svg, w


def corner_handles(x, y, w, h, t, size=8):
    s = size / 2
    return "".join(f'<rect x="{num(px - s)}" y="{num(py - s)}" width="{size}" height="{size}" fill="{t["bg"]}" stroke="{t["blue"]}" stroke-width="1.5"/>'
                   for px, py in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)])


def svg_doc(w, h, title, desc, body, style="", defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(desc)}</desc>
  <defs>{defs}</defs>
  <style>{style}</style>
  {body}
</svg>
"""


def write(name, content):
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
