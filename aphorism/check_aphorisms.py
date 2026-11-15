"""Check the Key aphorism boxes in a book's chapter pages.

Shared by both textbooks (EDCOR 310 and Econ 150); identical in both repositories.
Each build runs it on its chapter folder. It only warns; it never stops a build.

  python3 aphorism/check_aphorisms.py etb-live

Warns when:
  - a box's label isn't "Key aphorism" (one line) or "Key aphorisms" (a list of several);
  - a line in a chapter's end-of-chapter recap doesn't match any aphorism card in that chapter;
  - a chapter carries its own copy of the aphorism box styles (they live in aphorism/etb-aphorism.css).
"""
import html
import re
import sys
from pathlib import Path

LABEL = re.compile(r'<div class="etb-aphorism-label">(.*?)</div>', re.S)
CARD = re.compile(r'<div class="etb-aphorism-label">[^<]*</div>\s*<p class="etb-aphorism-line">(.*?)</p>', re.S)
RECAP = re.compile(r'<div class="etb-aphorism-label">([^<]*)</div>\s*<ol class="etb-aphorism-ol">(.*?)</ol>', re.S)
OWN_STYLES = re.compile(r'\.etb-aphorism(?:-label|-line|-sub|-ol)?\s*\{')


def text(fragment):
    t = html.unescape(re.sub(r"<[^>]+>", "", fragment))
    return re.sub(r"\s+", " ", t).strip().replace("’", "'")


def check(folder):
    warnings = []
    for page in sorted(Path(folder).glob("*.html")):
        s = page.read_text(encoding="utf-8")
        if "etb-aphorism-label" not in s:
            continue
        name = page.name
        for label in LABEL.findall(s):
            if text(label) not in ("Key aphorism", "Key aphorisms"):
                warnings.append(f'{name}: label "{text(label)}" should be "Key aphorism" or "Key aphorisms"')
        cards = {text(c) for c in CARD.findall(s)}
        for label, items in RECAP.findall(s):
            lines = [text(li) for li in re.findall(r"<li>(.*?)</li>", items, re.S)]
            if len(lines) > 1 and text(label) != "Key aphorisms":
                warnings.append(f'{name}: a recap of {len(lines)} lines should be labeled "Key aphorisms"')
            for line in lines:
                if line not in cards:
                    warnings.append(f'{name}: recap line "{line[:70]}" doesn\'t match any aphorism card in the chapter')
        styles = "".join(re.findall(r"(?is)<style[^>]*>(.*?)</style>", s))
        if OWN_STYLES.search(styles):
            warnings.append(f"{name}: carries its own aphorism styles; remove them (they live in aphorism/etb-aphorism.css)")
    return warnings


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "etb-live"
    found = check(folder)
    if found:
        print("Aphorism check (warnings only):")
        for w in found:
            print("  - " + w)
    else:
        print("Aphorism check: no problems found.")
