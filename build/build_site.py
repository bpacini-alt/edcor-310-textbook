"""Build the website into site/.

Reads the chapter snapshot in etb-live/ (manifest.json plus each page's HTML)
and writes:
  site/index.html            the cover
  site/contents/index.html   the table of contents
  site/about.html            About this book
  site/assets/book.css       styles for those three pages
  (all four from frontmatter/frontmatter.py, shared with Econ 150)
  site/<chapter>.html        every chapter, unit page, and supplement, wrapped as a full page
  site/joy-of-learning.html  the Joy of Learning reading menu (from menus/joy-of-learning.json)

Run from the repo root:  python3 build/build_site.py
"""
import html
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "frontmatter"))
import frontmatter  # noqa: E402  (shared with Econ 150)
SRC = ROOT / "etb-live"
OUT = ROOT / "site"

BOOK = {
    "title": "The Science of Learning",
    "subtitle": "An Evidence-Based Approach to Educational Psychology",
    "course": "EDCOR 310",
    "school": "Brigham Young University–Idaho",
    "authors": ["Benjamin Pacini", "Mayleigh Barth"],
    "year": "2026",
    "license": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
    "cover_design": "Kennadee Cuff",
    "etb": "https://books.byui.edu/science_of_learning",
    "site": "https://learning.benjaminpacini.com",
    "cover_alt": "Book cover: a smiling baby plays with a wooden toy train beneath a sketched light bulb.",
    "about": [
        "What began as a classroom project to enhance student learning in educational psychology and human development has grown over three years into a rigorous, collaborative textbook. This volume integrates student writing, generative AI assistance, and faculty oversight into a free educational resource.",
        "Ultimately, the authors and editors maintain full responsibility for the accuracy and integrity of the content herein.",
    ],
    "thanks": [
        "Special thanks are due to teaching assistants Skylar Quinton, Sarah Wilkin, Emma Canann, Jalene Rushton, Andres Rodriguez, Kennedee Cuff, and Shannon Steele for their extensive editorial and formatting contributions. Emerald Davis also provided volunteer hours to support this project. We also acknowledge the generations of students whose iterative feedback improved this text. All graphics were created by BYU-Idaho students using Canva Premium or are used by permission.",
    ],
}

WORDS_PER_MINUTE = 230
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment or ""))).strip()


def esc(s):
    return html.escape(s, quote=True)


def first_match(pattern, source):
    m = re.search(pattern, source, re.S)
    return text(m.group(1)) if m else ""


def reading_minutes(page_html):
    """The chapter's own estimate from its title card ("~ 50 min read").

    Falls back to a word-count estimate only for a chapter whose title card states none.
    """
    meta = re.search(r'class="etb-title-meta"[^>]*>(.*?)</div>', page_html, re.S)
    stated = re.search(r"~\s*(\d+)\s*min read", text(meta.group(1))) if meta else None
    if stated:
        return int(stated.group(1))
    body = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", page_html, flags=re.S)
    return max(1, round(len(text(body).split()) / WORDS_PER_MINUTE))


def sentences(paragraph, n):
    parts = re.split(r"(?<=[.!?])\s+", paragraph)
    return " ".join(parts[:n])


def load_book():
    manifest = json.loads((SRC / "manifest.json").read_text())["chapters"]
    units, chapters, supplements = [], [], []
    by_id = {}
    for entry in manifest:
        page = (SRC / entry["file"]).read_text()
        title = html.unescape(entry["title"])
        if title.startswith("Part "):
            start = page.find('class="etb-uo-intro"')
            end = page.find('class="etb-uo-list"', start)
            intro = [text(p) for p in re.findall(r"<p>(.*?)</p>", page[start:end], re.S)]
            outcomes = []
            for item in re.findall(r'class="etb-uo-text">(.*?)</div>', page, re.S):
                clos = re.findall(r'etb-uo-clo">(.*?)<', item)
                outcomes.append((text(re.sub(r'<span class="etb-uo-clo">.*?</span>', "", item, flags=re.S)), [text(c) for c in clos]))
            label = first_match(r'etb-title-unit">(.*?)</div>', page)          # "Unit 1 · Intro to Psychology"
            number, _, name = label.partition("·")
            unit = {"id": entry["id"], "label": number.strip(), "name": name.strip() or title.split(":", 1)[-1].strip(),
                    "roman": ROMAN[len(units)], "intro": [p for p in intro if p], "outcomes": outcomes, "chapters": []}
            units.append(unit)
            by_id[entry["id"]] = unit
        elif title.startswith("Chapter "):
            m = re.match(r"Chapter\s+(\d+):?\s*(.*)", title)
            # manifest.json lists pages in book order; a chapter belongs to the Part page before it.
            chapters.append({"num": int(m.group(1)), "title": m.group(2).strip(), "parent": units[-1]["id"],
                             "sub": first_match(r'class="etb-title-sub"[^>]*>(.*?)</p>', page),
                             "minutes": reading_minutes(page), "href": entry["file"]})
        elif title.startswith("Supplemental"):
            supplements.append({"title": title.split(":", 1)[-1].strip(), "href": entry["file"]})
    for ch in chapters:
        by_id[ch["parent"]]["chapters"].append(ch)
    return units, chapters, supplements


def names(people):
    return people[0] if len(people) == 1 else ", ".join(people[:-1]) + (" and " if len(people) == 2 else ", and ") + people[-1]


def chapter_range(unit):
    nums = [c["num"] for c in unit["chapters"]]
    return f"Chapters {min(nums)}–{max(nums)}" if len(nums) > 1 else f"Chapter {nums[0]}"


# The cover, contents, and About pages come from frontmatter/frontmatter.py, which is
# shared with Econ 150. This book supplies its own data and colors here.
THEME = {
    "accent": "#145d90", "accent_hover": "#0f4a73", "numeral": "#48749f",
    "badge_bg": "#145d90", "badge_fg": "#ffffff", "kicker": "#145d90",
    "tint": "#eef4fb", "tint_line": "#b8cfe0", "watermark": "#eef3f8",
}


def front_pages(units, chapters, supplements):
    hours = round(sum(c["minutes"] for c in chapters) / 60)
    back = []
    back_roman = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
    for i, s in enumerate(supplements):
        back.append({"n": back_roman[i], "t": s["title"], "s": "Quick reference", "href": "/" + s["href"]})
    book = {
        "title": BOOK["title"], "subtitle": BOOK["subtitle"], "course": BOOK["course"], "school": BOOK["school"],
        "byline": names(BOOK["authors"]), "site": BOOK["site"],
        "footer_html": [
            f'© {BOOK["year"]} {esc(names(BOOK["authors"]))}. Licensed <a href="{BOOK["license"][1]}">{BOOK["license"][0]}</a>. Cover design by {esc(BOOK["cover_design"])}.',
            f'{esc(BOOK["course"])} · {esc(BOOK["school"])}',
        ],
        "cover": {"src": "/assets/cover.jpg", "width": COVER_SIZE[0], "height": COVER_SIZE[1], "alt": BOOK["cover_alt"]},
        "theme": THEME,
        "stats": f"{len(chapters)} chapters in {len(units)} units · about {hours} hours of reading · free and open",
        "contents_sub": f"{len(chapters)} chapters in {len(units)} units, about {hours} hours of reading",
        "count": str(len(chapters)),
        "front": [
            {"n": "i", "t": "About this book", "s": "How the book was made, and acknowledgments", "m": "", "href": "/about.html"},
            {"n": "ii", "t": "How to Get the Most Out of This Book", "s": "How to study, practice, and use this book well", "m": "", "href": "/how-to-get-the-most-out-of-this-book.html"},
            {"n": "iii", "t": "Joy of Learning", "s": "The reading menu", "m": "", "href": "/joy-of-learning.html"}
        ],
        "units": [{
            "roman": u["roman"], "kicker": f"{u['label']} · {chapter_range(u)}", "title": u["name"],
            "hook": sentences(u["intro"][0], 2) if u["intro"] else "",
            "outcomes": u["outcomes"],
            "chapters": [{"n": str(c["num"]), "t": c["title"], "s": c["sub"], "m": f"{c['minutes']} min", "href": "/" + c["href"]}
                         for c in u["chapters"]],
        } for u in units],
        "back_title": "Readings and quick references",
        "back": back,
        "about": {"paras": BOOK["about"], "thanks": BOOK["thanks"]},
    }
    return frontmatter.render(book)


COVER_SIZE = (600, 926)


def build_cover():
    """Web-sized copy of the cover.

    build/cover-web.png is the EdTechBooks cover with the old books.byui.edu address removed;
    the untouched original stays in etb-live/cover.png.
    """
    global COVER_SIZE
    src = ROOT / "build" / "cover-web.png"
    im = Image.open(src if src.exists() else SRC / "cover.png").convert("RGB")
    w = 600
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    COVER_SIZE = im.size
    im.save(OUT / "assets" / "cover.jpg", "JPEG", quality=84, optimize=True, progressive=True)


# The floating Previous / Contents / Next bar at the bottom of each page: the same look as Econ 150's.
NAV_CSS = """
.etb-nav { position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000; background: rgba(255,255,255,.97); border-top: 1px solid #dce3ea; box-shadow: 0 -1px 5px rgba(26,58,92,.12); backdrop-filter: blur(8px); font-family: Arial, sans-serif; }
body { padding-bottom: 60px; }
.etb-nav-inner { max-width: 740px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 8px 12px; }
.etb-nav a, .etb-nav span { display: inline-flex; align-items: center; justify-content: center; min-height: 34px; padding: 0 11px; border: 1px solid #d6e0e8; border-radius: 6px; color: #1a3a5c; background: #fff; font-size: 12px; font-weight: 700; text-decoration: none; white-space: nowrap; }
.etb-nav a:hover, .etb-nav a:focus { background: #eef4fb; border-color: #9aaebe; outline: none; }
.etb-nav a:focus-visible { outline: 3px solid #8fb3d9; outline-offset: 2px; }
.etb-nav .etb-nav-home { border-color: #1a3a5c; background: #1a3a5c; color: #fff; }
.etb-nav .etb-nav-home:hover, .etb-nav .etb-nav-home:focus { background: #274e70; color: #fff; }
.etb-nav .etb-nav-disabled { color: #aab4bd; background: #f7f9fb; border-color: #e5eaee; }
/* When the audio player is open, it docks just above this bar instead of covering it. */
body:has(.etb-nav) .etb-ap { bottom: 51px; }
@media (max-width: 620px) { .etb-nav-inner { padding: 7px 8px; gap: 6px; } .etb-nav a, .etb-nav span { min-height: 32px; padding: 0 8px; font-size: 11px; } }
"""


def nav_bar(prev, nxt):
    """prev and nxt are manifest entries (or None at the ends of the book)."""
    def link(entry, text):
        if not entry:
            return f'<span class="etb-nav-disabled" aria-disabled="true">{text}</span>'
        label = esc(html.unescape(entry["title"]))
        return f'<a href="/{esc(entry["file"])}" aria-label="Go to {label}">{text}</a>'
    return ('<nav class="etb-nav" aria-label="Chapter navigation"><div class="etb-nav-inner">'
            f'{link(prev, "← Previous")}'
            '<a class="etb-nav-home" href="/contents/index.html" aria-label="Table of contents">Contents</a>'
            f'{link(nxt, "Next →")}</div></nav>')


def wrap_chapter_page(title, fragment, nav="", source_path=""):
    """Wrap a captured EdTechBooks fragment as a complete site page."""
    fragment = fragment.replace(
        "https://books.byui.edu/science_of_learning/sup1",
        "/sup1.html",
    )
    # Images keep their EdTechBooks paths (/images/content_images/...). The files are
    # in etb-live/images/ and publish_chapters() copies them into site/images/.
    edit_link = ""
    if source_path and fragment.strip():
        edit_path = urllib.parse.quote("etb-live/" + source_path, safe="/")
        edit_link = f'<a href="/editor/?book=science-of-learning&amp;path={edit_path}">Edit</a>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · The Science of Learning</title>
<link rel="stylesheet" href="/assets/etb-audio.css">
<style>
html {{ background: #f6f7f9; }}
body {{ margin: 0; }}
.etb-site-nav {{ background: #fff; border-bottom: 1px solid #e8ebef; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
.etb-site-nav-in {{ max-width: 740px; margin: 0 auto; padding: .8rem 1rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }}
.etb-site-nav a {{ color: #1a3a5c; text-decoration: none; font-size: 13px; font-weight: 600; }}
.etb-site-nav a:hover {{ text-decoration: underline; }}
.etb-site-nav-title {{ color: #1a1a1a !important; font-family: Georgia, "Times New Roman", serif; font-size: 15px !important; }}
.etb-site-nav-links {{ display: flex; gap: 1rem; }}
.etb {{ overflow-x: clip; }}
{NAV_CSS.strip()}
</style>
</head>
<body>
<header class="etb-site-nav">
  <div class="etb-site-nav-in">
    <a class="etb-site-nav-title" href="/index.html">The Science of Learning</a>
    <nav class="etb-site-nav-links" aria-label="Book navigation">
      <a href="/contents/index.html">Contents</a>
      <a href="/index.html">Home</a>
      {edit_link}
    </nav>
  </div>
</header>
<main>
{fragment}
</main>
{nav}
<script src="/assets/report.js" data-book="EDCOR 310" defer></script>
<script src="/assets/etb-audio.js"></script>
</body>
</html>
"""


# Drafts for review: pages in etb-live/ that are published at their own address but are
# not in manifest.json, so they stay out of the contents and the Previous / Next sequence.
# Share the link directly. When a draft is approved, it replaces its chapter's file and
# its entry here is removed.
DRAFTS = {
    "chapter16a.html": ("Chapter 16 (draft): Agency and Determinism", "chapter16.html"),
}

DRAFT_BANNER = """<div style="background:#fff8e6;border-bottom:1px solid #e8c96a;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;font-size:13px;color:#5a3d00;">
  <div style="max-width:740px;margin:0 auto;padding:.6rem 1rem;"><strong>Draft for review.</strong> This version is not yet part of the book. <a href="/{current}" style="color:#7a5000;">See the current chapter</a>.</div>
</div>"""


def publish_drafts():
    for name, (title, current) in DRAFTS.items():
        source = SRC / name
        if not source.exists():
            continue
        fragment = DRAFT_BANNER.format(current=esc(current)) + source.read_text(encoding="utf-8")
        page = wrap_chapter_page(title, fragment, nav_bar(None, None))
        page = page.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
        (OUT / name).write_text(page, encoding="utf-8")


def publish_chapters():
    (OUT / "editor").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "editor" / "index.html", OUT / "editor" / "index.html")

    for name in ("reading-ratings-demo.html", "bang-for-buck.html"):
        demo = SRC / name
        if demo.exists():
            shutil.copyfile(demo, OUT / name)

    manifest = json.loads((SRC / "manifest.json").read_text())["chapters"]
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    for name in ("etb-audio.js", "etb-audio.css"):
        (OUT / "assets" / name).write_text(
            (ROOT / "audio" / "player" / name).read_text(),
            encoding="utf-8",
        )
    # The Report a problem button; feedback/report.js is the one place to edit it.
    (OUT / "assets" / "report.js").write_text((ROOT / "feedback" / "report.js").read_text(), encoding="utf-8")
    # The chapters' images, copied from EdTechBooks into etb-live/images/ so the site doesn't depend on it.
    if (SRC / "images").is_dir():
        shutil.copytree(SRC / "images", OUT / "images", dirs_exist_ok=True)
    # Previous / Next run through the numbered chapters in book order. Unit pages and
    # supplements get the bar too, with only the Contents button active.
    sequence = [e for e in manifest if html.unescape(e["title"]).startswith("Chapter ")]
    position = {e["file"]: i for i, e in enumerate(sequence)}
    style_losses = []
    for entry in manifest:
        title = html.unescape(entry["title"])
        fragment = (SRC / entry["file"]).read_text(encoding="utf-8")
        i = position.get(entry["file"])
        prev = sequence[i - 1] if i is not None and i > 0 else None
        nxt = sequence[i + 1] if i is not None and i + 1 < len(sequence) else None
        page = wrap_chapter_page(title, fragment, nav_bar(prev, nxt), entry["file"])
        # Safety check: a rebuild should never strip styles from a published page. If the
        # source in etb-live/ has fewer <style> blocks than the page students see, leave the
        # published page alone and stop, so nobody commits a page that lost its styling.
        out = OUT / entry["file"]
        if out.exists():
            before = len(re.findall(r"<style\b", out.read_text(encoding="utf-8"), flags=re.I))
            after = len(re.findall(r"<style\b", page, flags=re.I))
            if after < before:
                style_losses.append(f"{entry['file']}: published page has {before} style blocks; "
                                    f"the rebuilt page would have {after}")
                continue
        out.write_text(page, encoding="utf-8")
    if style_losses:
        sys.exit("STOPPED: rebuilding would remove styles from these pages, so they were left as they are:\n  "
                 + "\n  ".join(style_losses)
                 + "\nCopy the missing <style> blocks into the page's etb-live/ file and build again. "
                   "If you removed a style on purpose, delete the page from site/ first.")

def publish_menu():
    """The Joy of Learning reading menu. menus/joy-of-learning.json is the one place to edit it."""
    import subprocess
    import sys
    subprocess.run(
        [sys.executable, str(ROOT / "menus" / "build_menu.py"),
         str(ROOT / "menus" / "joy-of-learning.json"), str(OUT / "joy-of-learning.html")],
        check=True,
    )


def main():
    units, chapters, supplements = load_book()
    (OUT / "contents").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    build_cover()
    publish_chapters()
    publish_drafts()
    publish_menu()
    for path, content in front_pages(units, chapters, supplements).items():
        (OUT / path).write_text(content)
    print(f"{len(units)} units, {len(chapters)} chapters, {len(supplements)} supplements")
    for u in units:
        print(f"  {u['label']}: {u['name']} | {chapter_range(u)} | {len(u['outcomes'])} outcomes | intro paras {len(u['intro'])}")


if __name__ == "__main__":
    main()
