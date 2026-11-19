"""Writes README.md (English, shown on the profile) and README.de.md (German).

Every image is a <picture> with a dark and a light source, so GitHub shows the
variant that matches the viewer's theme. GitHub cannot detect the viewer's
language, so both files carry a language switch at the top.

Run: uv run python .github/scripts/build_readme.py
"""

import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

from content import BADGES, CERTS, ISSUERS, LI_CERTS, LINKS, PROJECTS, SECTIONS, SOCIAL, SUPPORT, TEXT
from tech import BADGE_BG, BADGE_FG, CATEGORIES, CORE, LOGOS, NAMES_DE

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "certificates"
FILES = {unicodedata.normalize("NFC", f.name): f.name for f in CERT_DIR.iterdir()}
OUTPUT = {"en": "README.md", "de": "README.de.md"}
ALT_PREFIX = {"web": "Website", "linkedin": "LinkedIn", "discord": "Discord"}
LIVE_SITES = [("Tellersonne", "https://tellersonne.app"), ("VectoBeat", "https://vectobeat.uplytech.de"),
              ("UplyTech", "https://www.uplytech.de")]


def picture(dark, light, alt, width: str | None = "100%", href=None):
    size = f' width="{width}"' if width else ""
    img = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
           f'<source media="(prefers-color-scheme: light)" srcset="{light}">'
           f'<img alt="{alt}" src="{light}"{size}></picture>')
    return f'<a href="{href}">{img}</a>' if href else img


def asset(name, alt, lang=None, width="100%", href=None):
    stem = f"assets/{name}-{lang}" if lang else f"assets/{name}"
    return picture(f"{stem}-dark.svg", f"{stem}-light.svg", alt, width, href)


def section(key, lang):
    return asset(f"h-{key}", SECTIONS[key][lang][0], lang)


def md_inline(text):
    """Minimal Markdown to HTML for table cells inside raw HTML."""
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def badge(name, alt, href=None):
    """One of the generated pill badges in assets/badges."""
    return picture(f"assets/badges/{name}-dark.svg", f"assets/badges/{name}-light.svg", alt, None, href)


def pick(v, lang):
    return v[lang] if isinstance(v, dict) else v


def badge_row(key, lang):
    cells = []
    for name, _glyph, label, value, href in BADGES[key]:
        label, value = pick(label, lang), pick(value, lang)
        prefix = label or ALT_PREFIX.get(name)
        cells.append(badge(f"{name}-{lang}", f"{prefix}: {value}" if prefix else value, href))
    # three on top, the rest below, so the rows stay balanced
    return '<p align="center">\n  ' + "\n  ".join(cells[:3]) + "<br>\n  " + "\n  ".join(cells[3:]) + "\n</p>"


def brand_badges(group):
    return " ".join(badge(slug, name, href) for name, _color, slug, _fg, href in group)


def lang_switch(lang):
    en_href = LINKS["profile"] if lang == "de" else "#"
    en = asset(f"lang-en-{'on' if lang == 'en' else 'off'}", "English", width="132", href=en_href)
    de = asset(f"lang-de-{'on' if lang == 'de' else 'off'}", "Deutsch", width="132", href=OUTPUT["de"])
    return f'<p align="right">{en}{de}</p>'


def cert_tables(lang):
    tx = TEXT[lang]
    head = tx["cert_head"]
    out = []
    for gi, group in enumerate(tx["cert_groups"]):
        rows = [c for c in CERTS if c[0] == gi]
        out.append(f"<details>\n<summary><b>{group}</b> ({len(rows)})</summary>\n")
        out.append(f"| {head[0]} | {head[1]} | {head[2]} | {head[3]} |\n| --- | --- | --- | --- |")
        for _, name, issuer, (mon, year), files, verify in rows:
            name = name[lang] if isinstance(name, dict) else name
            files = [files] if isinstance(files, str) else (files or [])
            proofs = []
            for i, f in enumerate(files):
                real = FILES.get(unicodedata.normalize("NFC", f))
                if real is None:
                    raise FileNotFoundError(f)
                proofs.append(f"[{tx['proof'][0] if i == 0 else 'PMI'}](certificates/{quote(real)})")
            if verify:
                proofs.append(f"[{tx['proof'][1]}]({verify})")
            if not proofs:
                proofs.append(f"[{tx['proof'][2]}]({LI_CERTS})")
            out.append(f"| {name} | {issuer} | {tx['month'][mon]} {year} | {', '.join(proofs)} |")
        out.append("\n</details>\n")
    return "\n".join(out)


def shield(name, theme):
    """Text badge in the colours of the skillicons tiles, with a Simple Icons logo when one exists."""
    text = quote(name.replace("-", "--").replace("_", "__"), safe="")
    url = f"https://img.shields.io/badge/{text}-{BADGE_BG[theme]}?style=for-the-badge"
    slug = LOGOS.get(name)
    if slug:
        url += f"&logo={quote(slug)}&logoColor={BADGE_FG[theme]}"
    return url


def evidence(ev, tx):
    if ev is None:
        return ""
    if ev == "private":
        return f" (*{tx['private_label']}*)"
    repo = ev if "/" in ev else f"VectoDE/{ev}"
    return f" ([{repo.split('/')[1]}](https://github.com/{repo}))"


def stack(lang):
    tx = TEXT[lang]
    count = sum(len(items) for _, _, items in CATEGORIES)
    out = [tx["stack_intro"], "", f"**{tx['core_label']}:** " + " · ".join(CORE), ""]
    rows = []
    for _key, label, items in CATEGORIES:
        with_icon = [(n, i) for n, i, _ in items if i]
        icons = ""
        if with_icon:
            # a plain comma would split the srcset into several candidates, so it is encoded
            base = f"https://skillicons.dev/icons?i={'%2C'.join(i for _, i in with_icon)}&perline=13&theme="
            icons = picture(base + "dark", base + "light", ", ".join(n for n, _ in with_icon), None)
        badges = " ".join(picture(shield(n, "dark"), shield(n, "light"), n, None) for n, i, _ in items if not i)
        rows.append((f"<b>{label[lang]}</b>", "<br>".join(x for x in (icons, badges) if x)))
    out += [html_table(rows), ""]
    out += [f"<details>\n<summary><b>{tx['stack_details'].format(count=count)}</b></summary>\n", tx["stack_legend"], ""]
    for _key, label, items in CATEGORIES:
        names = NAMES_DE if lang == "de" else {}
        out.append(f"- **{label[lang]}**: " + ", ".join(names.get(n, n) + evidence(ev, tx) for n, _i, ev in items))
    out += ["\n</details>", "", tx["ideas"], ""]
    return out


def timeline_alt(tx):
    """The timeline image described in words, without Markdown links."""
    return "; ".join(f"{y}: " + re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", d) for y, d in tx["timeline_rows"])


def html_table(rows):
    lines = ["<table>"] + ["  <tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for cells in rows] + ["</table>"]
    return "\n".join(lines)


def build(lang):
    tx = TEXT[lang]
    parts = [lang_switch(lang), "",
             asset("hero", tx["hero_alt"], lang, href=LINKS["company"]), "",
             badge_row("contact", lang), badge_row("facts", lang), ""]

    parts += [section("about", lang), ""]
    for paragraph in tx["about"]:
        parts += [paragraph, ""]
    parts += [html_table([(f"<b>{k}</b>", md_inline(v)) for k, v in tx["facts"]]), ""]

    parts += [section("hire", lang), "", tx["hire_intro"], ""]
    parts += [html_table([(f"<b>{k}</b>", md_inline(v.format(count=len(CERTS), pdfs=sum(1 for c in CERTS if c[4])))) for k, v in tx["hire"]]), ""]

    parts += [section("services", lang), ""] + [f"- {s}" for s in tx["services"]] + [""]

    parts += [section("projects", lang), ""]
    for i in range(0, len(PROJECTS), 2):
        cells = [asset(f"card-{key}", f"{name}: {status[lang]}", lang, "49%", url)
                 for key, name, url, _icon, status, _text, _stack in PROJECTS[i:i + 2]]
        parts.append('<p align="center">\n  ' + "\n  ".join(cells) + "\n</p>")
    parts += ["", tx['projects_short'] + ":", ""]
    parts += [f"- [{name}]({url}): {text[lang]}" for _k, name, url, _i, _s, text, _st in PROJECTS] + [""]
    parts += ['<p align="center"><sub>' + tx["project_links"] + ": " +
              ", ".join(f'{n} <a href="{u}">{u.split("//")[1]}</a>' for n, u in LIVE_SITES) + "</sub></p>", ""]
    h = tx["smaller_head"]
    parts += [f"<details>\n<summary><b>{tx['smaller']}</b></summary>\n", f"| {h[0]} | {h[1]} | {h[2]} |", "| --- | --- | --- |"]
    parts += [f"| [{p}](https://github.com/VectoDE/{p}) | {d} | {lang_ or '-'} |" for p, d, lang_ in tx["smaller_rows"]]
    parts += ["\n</details>", ""]

    parts += [section("timeline", lang), "", asset("timeline", timeline_alt(tx), lang), ""]
    parts += [f"<details>\n<summary>{tx['timeline_text']}</summary>\n", "| | |", "| --- | --- |"]
    parts += [f"| **{y}** | {d} |" for y, d in tx["timeline_rows"]] + ["\n</details>", ""]

    parts += [section("stack", lang), ""] + stack(lang)

    issuers = " ".join(badge(f"issuer-{key}", f"{name}: {sum(1 for c in CERTS if c[2] == name)}")
                       for key, name, _glyph, _color in ISSUERS)
    parts += [section("certificates", lang), "", tx["certs_intro"].format(count=len(CERTS)), "",
              f"<p>{issuers}</p>", "", cert_tables(lang)]

    parts += [section("stats", lang), "", asset("stats", tx["stats_alt"], lang), "",
              asset("awards", tx["trophies_alt"], lang), "", f"<sub>{tx['stats_note']}</sub>", ""]

    oh = tx["org_head"]
    parts += [section("orgs", lang), "", f"| {oh[0]} | {oh[1]} |", "| --- | --- |"]
    parts += [f"| [{n}]({u}) | {d} |" for n, u, d in tx["orgs"]] + [""]

    parts += [section("links", lang), ""]
    parts += [html_table([(f"<b>{label}</b>", brand_badges(group)) for label, group in zip(tx["link_rows"], SOCIAL)]), ""]

    parts += [section("support", lang), "", tx["support"], "", f"<p>{brand_badges(SUPPORT)}</p>", ""]

    parts += [asset("footer", tx["footer_alt"], lang, href="mailto:" + LINKS["email_company"]), ""]
    views = f"https://komarev.com/ghpvc/?username=VectoDE&style=flat-square&color=1F6FEB&label={quote(tx['views'])}"
    parts += [f'<p align="center"><sub>{tx["made_by"]}</sub><br><br><img src="{views}" alt="{tx["views"]}"></p>', ""]
    return "\n".join(parts)


if __name__ == "__main__":
    for lang, name in OUTPUT.items():
        (ROOT / name).write_text(build(lang), encoding="utf-8")
    print("written:", ", ".join(OUTPUT.values()))
