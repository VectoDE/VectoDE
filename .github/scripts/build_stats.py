"""Builds assets/stats-{lang}-{theme}.svg from the GitHub API.

Runs daily in .github/workflows/stats.yml. Locally:
  GH_TOKEN=$(gh auth token) uv run --with fonttools --with brotli python .github/scripts/build_stats.py
Only public data is used.
"""

import json
import math
import os
import urllib.request
from collections import Counter
from datetime import datetime, timezone

from content import AWARDS, CERTS, CODING_SINCE, LANGS, PROJECTS, STATS
from svgkit import DISPLAY, SANS, SANS_BOLD, THEMES, measure, num, svg_doc, txt, write

USER = "VectoDE"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

PALETTES = {
    "dark": ["#4C9AFF", "#FFB547", "#3DD68C", "#B48CFF", "#FF7A90", "#5FD4E8", "#5F7392"],
    "light": ["#1F6FEB", "#C27A00", "#14955A", "#7C4DDB", "#D6455E", "#1593AB", "#8A99B0"],
}


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", f"{USER}-profile-stats")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def collect():
    user = api(f"https://api.github.com/users/{USER}")
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"]]
    langs = Counter()
    for r in own:
        langs.update(api(r["languages_url"]))
    total, weeks, days = None, [], []
    if TOKEN:
        q = """query($login:String!){ user(login:$login){ contributionsCollection{ contributionCalendar{
               totalContributions weeks{ contributionDays{ contributionCount } } } } } }"""
        cal = api("https://api.github.com/graphql", {"query": q, "variables": {"login": USER}})
        cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total = cal["totalContributions"]
        weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
        days = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]
    return dict(repos=user["public_repos"], stars=sum(r["stargazers_count"] for r in own),
                followers=user["followers"], total=total, weeks=weeks, days=days, langs=langs.most_common())


def smooth(points):
    d = f"M {num(points[0][0])},{num(points[0][1])}"
    for a, b in zip(points, points[1:]):
        k = (b[0] - a[0]) * 0.5
        d += f" C {num(a[0] + k)},{num(a[1])} {num(b[0] - k)},{num(b[1])} {num(b[0])},{num(b[1])}"
    return d


def fmt_int(n, lang):
    return f"{n:,}".replace(",", "." if lang == "de" else ",")


def card(t, palette, s, lang):
    c = STATS[lang]
    W, H, M = 1280, 436, 12
    FW, FH = W - 2 * M, H - 2 * M - 8
    L, R = 44, FW - 44
    o = [f'<rect width="{FW}" height="{FH}" rx="16" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="15.5" fill="none" stroke="{t["frame"]}"/>']
    stamp = f'{c["updated"]} {datetime.now(timezone.utc).strftime(c["date_fmt"])}'
    sw = measure(SANS, stamp, 12.5) + 34
    o.append(f'<rect x="{num(R - sw)}" y="24" width="{num(sw)}" height="26" rx="13" fill="{t["raised"]}"/>')
    o.append(f'<circle class="live" cx="{num(R - sw + 14)}" cy="37" r="3.5" fill="{t["green"]}"/><circle cx="{num(R - sw + 14)}" cy="37" r="3.5" fill="{t["green"]}"/>')
    o.append(txt(SANS, stamp, 12.5, R - sw + 25, 41.5, t["muted"]))

    metrics = [(fmt_int(s["total"], lang) if s["total"] is not None else "-", c["contributions"]),
               (str(s["repos"]), c["repos"]), (str(s["stars"]), c["stars"]), (str(s["followers"]), c["followers"])]
    col = (R - L) / 4
    for i, (value, label) in enumerate(metrics):
        x = L + i * col
        o.append(f'<g class="rise" style="animation-delay:{.1 + i * .12:.2f}s">')
        if i:
            o.append(f'<path d="M{num(x - 24)} 78V146" stroke="{t["line"]}"/>')
        o.append(txt(DISPLAY, value, 50, x, 124, t["text"], tracking=-0.4))
        o.append(txt(SANS, label, 14, x, 150, t["muted"]))
        o.append("</g>")

    top, bottom = 206, 292
    o.append(txt(SANS_BOLD, c["weekly"], 13, L, top - 14, t["muted"]))
    weeks = s["weeks"] or [0] * 53
    peak = max(max(weeks), 1)
    step = (R - L) / (len(weeks) - 1)
    pts = [(L + i * step, bottom - (w / peak) * (bottom - top - 10)) for i, w in enumerate(weeks)]
    line = smooth(pts)
    o.append(f'<path d="M{L} {bottom}H{R}" stroke="{t["line"]}"/>')
    o.append(f'<path class="area" d="{line} L {R},{bottom} L {L},{bottom} Z" fill="url(#area)"/>')
    o.append(f'<path class="draw" pathLength="1" d="{line}" fill="none" stroke="{t["blue"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    i_peak = max(range(len(weeks)), key=lambda i: weeks[i])
    if weeks[i_peak]:
        px, py = pts[i_peak]
        label = f'{c["busiest"]}: {fmt_int(weeks[i_peak], lang)}'
        lw = measure(SANS_BOLD, label, 12) + 16
        lx = min(max(px - lw / 2, L), R - lw)
        o.append(f'<g class="rise" style="animation-delay:1.6s"><rect x="{num(px - 5)}" y="{num(py - 5)}" width="10" height="10" fill="{t["blue"]}"/>'
                 f'<rect x="{num(lx)}" y="{num(py - 34)}" width="{num(lw)}" height="21" rx="5" fill="{t["blue"]}"/>'
                 f'{txt(SANS_BOLD, label, 12, lx + 8, py - 19.5, t["onBlue"])}</g>')

    o.append(txt(SANS_BOLD, c["languages"], 13, L, 332, t["muted"]))
    total_bytes = sum(b for _, b in s["langs"]) or 1
    top_langs = s["langs"][:6]
    rest = total_bytes - sum(b for _, b in top_langs)
    parts = top_langs + ([(c["other"], rest)] if rest > 0 else [])
    x, segs = L, []
    for i, (_, b) in enumerate(parts):
        w = (R - L) * b / total_bytes
        segs.append(f'<rect x="{num(x)}" y="346" width="{num(w + 0.5)}" height="12" fill="{palette[min(i, len(palette) - 1)]}"/>')
        x += w
    o.append(f'<g clip-path="url(#bar)"><g class="grow">{"".join(segs)}</g></g>')
    x = L
    for i, (name, b) in enumerate(parts):
        pct = f"{b / total_bytes * 100:.1f}".replace(".", "," if lang == "de" else ".") + " %" * (lang == "de") + "%" * (lang != "de")
        o.append(f'<circle cx="{num(x + 5)}" cy="384" r="5" fill="{palette[min(i, len(palette) - 1)]}"/>')
        o.append(txt(SANS_BOLD, name, 13, x + 16, 389, t["text"]))
        nx = x + 16 + measure(SANS_BOLD, name, 13) + 6
        o.append(txt(SANS, pct, 13, nx, 389, t["muted"]))
        x = nx + measure(SANS, pct, 13) + 26

    style = """.draw { stroke-dasharray: 1; animation: draw 1.8s cubic-bezier(.65,0,.35,1) .3s backwards; }
    .area { animation: fade 1s ease-out 1.2s backwards; }
    .grow { transform-box: fill-box; transform-origin: left center; animation: grow 1.4s cubic-bezier(.2,.7,.2,1) .4s backwards; }
    .rise { animation: rise .7s ease-out backwards; }
    .live { transform-box: fill-box; transform-origin: center; animation: live 2.2s ease-out infinite; }
    @keyframes draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
    @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
    @keyframes live { 0% { opacity: .55; transform: scale(1); } 100% { opacity: 0; transform: scale(3.2); } }
    @media (prefers-reduced-motion: reduce) {
      .draw { animation: none; stroke-dashoffset: 0; } .area, .rise { animation: none; opacity: 1; }
      .grow { animation: none; transform: none; } .live { animation: none; opacity: 0; } }"""
    defs = (f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" '
            f'flood-color="{t["shadow"]}" flood-opacity="{t["shadowOpacity"]}"/></filter>'
            f'<clipPath id="bar"><rect x="{L}" y="346" width="{R - L}" height="12" rx="6"/></clipPath>'
            f'<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["blue"]}" stop-opacity=".28"/>'
            f'<stop offset="1" stop-color="{t["blue"]}" stop-opacity="0"/></linearGradient>')
    desc = f"{metrics[0][0]} {c['contributions']}, {s['repos']} {c['repos']}, {s['stars']} {c['stars']}, {s['followers']} {c['followers']}."
    return svg_doc(W, H, c["title"], desc, f'<g transform="translate({M} {M})">{"".join(o)}</g>', style, defs)


# ---------------------------------------------------------------- awards

TIERS = [("gold", 1.0), ("silver", .6), ("bronze", .3)]


def longest_streak(days):
    best = run = 0
    for count in days:
        run = run + 1 if count else 0
        best = max(best, run)
    return best


def awards(t, s, lang):
    """Medal strip built from real numbers. Tiers come from fixed thresholds per metric."""
    c = AWARDS[lang]
    W, H, M = 1280, 236, 12
    FW, FH = W - 2 * M, H - 2 * M - 8
    years = datetime.now(timezone.utc).year - CODING_SINCE
    items = [(str(years), c["years"], years, 10), (str(len(CERTS)), c["certs"], len(CERTS), 30),
             (str(longest_streak(s["days"])), c["streak"], longest_streak(s["days"]), 30),
             (str(len(s["langs"])), c["langs"], len(s["langs"]), 10),
             (str(len(PROJECTS)), c["projects"], len(PROJECTS), 8)]
    medal = {"gold": t["amber"], "silver": t["muted"], "bronze": t["bronze"]}
    o = [f'<rect width="{FW}" height="{FH}" rx="16" fill="{t["panel"]}" filter="url(#shadow)"/>',
         f'<rect x=".5" y=".5" width="{FW - 1}" height="{FH - 1}" rx="15.5" fill="none" stroke="{t["frame"]}"/>']
    col = (FW - 48) / len(items)
    for i, (value, label, n, goal) in enumerate(items):
        tier = next(name for name, share in TIERS if n >= goal * share or name == "bronze")
        color = medal[tier]
        x = 24 + i * col
        cx, cy = x + 52, FH / 2
        o.append(f'<g class="rise" style="animation-delay:{.15 + i * .14:.2f}s">')
        if i:
            o.append(f'<path d="M{num(x)} 40V{FH - 40}" stroke="{t["line"]}"/>')
        o.append(f'<circle cx="{num(cx)}" cy="{cy}" r="34" fill="{t["raised"]}"/>')
        o.append(f'<g class="spin" style="transform-origin:{num(cx)}px {cy}px">'
                 f'<circle cx="{num(cx)}" cy="{cy}" r="34" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="3 5"/></g>')
        o.append(f'<circle cx="{num(cx)}" cy="{cy}" r="25" fill="none" stroke="{color}" stroke-width="2.5"/>')
        star = " ".join(f"{num(cx + r * math.sin(math.pi * k / 5))},{num(cy - r * math.cos(math.pi * k / 5))}"
                        for k, r in zip(range(10), [11, 4.6] * 5))
        o.append(f'<polygon class="glint" points="{star}" fill="{color}" style="animation-delay:{1.4 + i * .5:.1f}s"/>')
        tx_ = cx + 52
        o.append(txt(DISPLAY, value, 44, tx_, cy + 6, t["text"]))
        o.append(txt(SANS, label, 13.5, tx_, cy + 32, t["muted"]))
        chip = c[tier]
        cw = measure(SANS_BOLD, chip, 11) + 16
        o.append(f'<rect x="{num(tx_)}" y="{cy - 58}" width="{num(cw)}" height="19" rx="9.5" fill="{color}" fill-opacity=".16"/>')
        o.append(txt(SANS_BOLD, chip, 11, tx_ + 8, cy - 44.5, color))
        o.append("</g>")
    style = """.rise { animation: rise .7s ease-out backwards; }
    .spin { animation: spin 18s linear infinite; }
    .glint { transform-box: fill-box; transform-origin: center; animation: glint 5s ease-in-out infinite; }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes glint { 0%, 80%, 100% { transform: scale(1); } 88% { transform: scale(1.25) rotate(18deg); } }
    @media (prefers-reduced-motion: reduce) { .rise { animation: none; opacity: 1; } .spin, .glint { animation: none; } }"""
    defs = (f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" '
            f'flood-color="{t["shadow"]}" flood-opacity="{t["shadowOpacity"]}"/></filter>')
    desc = "; ".join(f"{v} {label}" for v, label, _n, _g in items)
    return svg_doc(W, H, c["title"], desc, f'<g transform="translate({M} {M})">{"".join(o)}</g>', style, defs)


if __name__ == "__main__":
    stats = collect()
    for theme, t in THEMES.items():
        for lang in LANGS:
            write(f"stats-{lang}-{theme}.svg", card(t, PALETTES[theme], stats, lang))
            write(f"awards-{lang}-{theme}.svg", awards(t, stats, lang))
    print({k: v for k, v in stats.items() if k not in ("weeks", "days")})
