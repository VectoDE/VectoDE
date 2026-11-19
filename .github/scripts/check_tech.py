"""Checks every skillicons id and Simple Icons slug used in tech.py.

skillicons.dev answers an unknown id with an empty 256-byte SVG, Shields drops an
unknown logo silently. Both cases are reported here, so the README never shows a
blank tile or a badge that claims a logo it does not have.

Run: uv run python .github/scripts/check_tech.py
Exit code 1 if anything is wrong.
"""

import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

from tech import CATEGORIES, LOGOS


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "VectoDE-profile-check"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.status, res.read()


def check_icon(icon):
    status, body = fetch(f"https://skillicons.dev/icons?i={icon}")
    return icon, status == 200 and len(body) > 300


def check_logo(slug):
    status, body = fetch(f"https://img.shields.io/badge/x-242938?logo={quote(slug)}")
    return slug, status == 200 and b"<image" in body


def main():
    icons = sorted({i for _, _, items in CATEGORIES for _, i, _ in items if i})
    slugs = sorted({s for s in LOGOS.values() if s})
    with ThreadPoolExecutor(8) as pool:
        bad_icons = [i for i, ok in pool.map(check_icon, icons) if not ok]
        bad_slugs = [s for s, ok in pool.map(check_logo, slugs) if not ok]
    print(f"skillicons: {len(icons)} checked, invalid: {bad_icons or 'none'}")
    print(f"logos: {len(slugs)} checked, invalid: {bad_slugs or 'none'}")
    return 1 if bad_icons or bad_slugs else 0


if __name__ == "__main__":
    sys.exit(main())
