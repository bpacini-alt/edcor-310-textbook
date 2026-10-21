"""Build the book's front pages (home + table of contents) into site/.

Reads the chapter snapshot in etb-live/ (manifest.json plus each page's HTML)
and writes:
  site/index.html            the landing page
  site/contents/index.html   the table of contents
  site/assets/book.css       shared styles for the book's own pages

Run from the repo root:  python3 build/build_site.py
"""
import html
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
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
                             "minutes": reading_minutes(page), "href": f"{BOOK['etb']}/{entry['short']}"})
        elif title.startswith("Supplemental"):
            supplements.append({"title": title.split(":", 1)[-1].strip(), "href": f"{BOOK['etb']}/{entry['short']}"})
    for ch in chapters:
        by_id[ch["parent"]]["chapters"].append(ch)
    return units, chapters, supplements


def page(title, body, depth, description):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{BOOK['site']}/assets/cover.jpg">
<link rel="stylesheet" href="{up}assets/book.css">
</head>
<body>
<header class="bk-top">
  <div class="bk-top-in">
    <a class="bk-top-name" href="{up}index.html">{esc(BOOK['title'])}</a>
    <nav aria-label="Book"><a href="{up}contents/index.html">Contents</a></nav>
  </div>
</header>
<main class="bk">
{body}
</main>
<footer class="bk-foot">
  <div class="bk-foot-in">
    <p>© {BOOK['year']} {esc(names(BOOK['authors']))}. Licensed <a href="{BOOK['license'][1]}">{BOOK['license'][0]}</a>. Cover design by {esc(BOOK['cover_design'])}.</p>
    <p>{esc(BOOK['course'])} · {esc(BOOK['school'])}</p>
  </div>
</footer>
</body>
</html>
"""


def names(people):
    return people[0] if len(people) == 1 else ", ".join(people[:-1]) + (" and " if len(people) == 2 else ", and ") + people[-1]


def chapter_range(unit):
    nums = [c["num"] for c in unit["chapters"]]
    return f"Chapters {min(nums)}–{max(nums)}" if len(nums) > 1 else f"Chapter {nums[0]}"


def build_home(units, chapters):
    first = min(chapters, key=lambda c: c["num"])
    cards = "\n".join(f"""    <a class="bk-unit-card" href="contents/index.html#unit-{i + 1}">
      <span class="bk-badge" aria-hidden="true">{u['roman']}</span>
      <span class="bk-kicker">{esc(u['label'])} · {esc(chapter_range(u))}</span>
      <span class="bk-unit-name">{esc(u['name'])}</span>
      <span class="bk-unit-hook">{esc(sentences(u['intro'][0], 2) if u['intro'] else '')}</span>
    </a>""" for i, u in enumerate(units))
    about = "\n".join(f"    <p>{esc(p)}</p>" for p in BOOK["about"])
    thanks = "\n".join(f"    <p>{esc(p)}</p>" for p in BOOK["thanks"])
    hours = sum(c["minutes"] for c in chapters) / 60
    body = f"""  <section class="bk-card bk-cover bk-hero">
    <img class="bk-cover-img" src="assets/cover.jpg" width="{COVER_SIZE[0]}" height="{COVER_SIZE[1]}" alt="{esc(BOOK['cover_alt'])}">
    <div class="bk-hero-text">
    <p class="bk-kicker">{esc(BOOK['course'])} · {esc(BOOK['school'])}</p>
    <h1 class="bk-title">{esc(BOOK['title'])}</h1>
    <p class="bk-sub">{esc(BOOK['subtitle'])}</p>
    <p class="bk-meta">By {esc(names(BOOK['authors']))} · {len(chapters)} chapters · about {round(hours)} hours of reading</p>
    <div class="bk-actions">
      <a class="bk-btn" href="{esc(first['href'])}">Start with Chapter {first['num']}</a>
      <a class="bk-btn bk-btn-quiet" href="contents/index.html">Table of contents</a>
    </div>
    </div>
  </section>

  <section class="bk-section" aria-labelledby="org">
    <h2 class="bk-slbl" id="org">How the book is organized</h2>
    <div class="bk-unit-grid">
{cards}
    </div>
  </section>

  <section class="bk-section bk-about" aria-labelledby="about">
    <h2 class="bk-slbl" id="about">About this book</h2>
{about}
  </section>

  <section class="bk-section bk-about bk-thanks" aria-labelledby="thanks">
    <h2 class="bk-slbl" id="thanks">Acknowledgments</h2>
{thanks}
  </section>"""
    return page(BOOK["title"], body, 0, BOOK["subtitle"])


def build_contents(units, chapters, supplements):
    blocks = []
    for i, u in enumerate(units):
        intro = "\n".join(f"      <p>{esc(p)}</p>" for p in u["intro"])
        outcomes = "\n".join(
            f"""          <li><span>{esc(o)}</span>{''.join(f' <span class="bk-clo">{esc(c)}</span>' for c in clos)}</li>"""
            for o, clos in u["outcomes"])
        rows = "\n".join(f"""      <li><a class="bk-ch" href="{esc(c['href'])}">
        <span class="bk-ch-num">{c['num']}</span>
        <span class="bk-ch-body"><span class="bk-ch-title">{esc(c['title'])}</span><span class="bk-ch-sub">{esc(c['sub'])}</span></span>
        <span class="bk-ch-time">{c['minutes']} min</span>
      </a></li>""" for c in u["chapters"])
        blocks.append(f"""  <section class="bk-unit" id="unit-{i + 1}" aria-labelledby="unit-{i + 1}-name">
    <div class="bk-unit-head">
      <span class="bk-badge" aria-hidden="true">{u['roman']}</span>
      <div>
        <p class="bk-kicker">{esc(u['label'])} · {esc(chapter_range(u))}</p>
        <h2 class="bk-unit-title" id="unit-{i + 1}-name">{esc(u['name'])}</h2>
      </div>
    </div>
    <div class="bk-unit-intro">
{intro}
    </div>
    <details class="bk-outcomes">
      <summary>Unit outcomes <span>({len(u['outcomes'])})</span></summary>
      <ol>
{outcomes}
      </ol>
    </details>
    <ol class="bk-chapters">
{rows}
    </ol>
  </section>""")
    supp = "\n".join(f"""      <li><a class="bk-ch bk-ch-supp" href="{esc(s['href'])}">
        <span class="bk-ch-num" aria-hidden="true">+</span>
        <span class="bk-ch-body"><span class="bk-ch-title">{esc(s['title'])}</span><span class="bk-ch-sub">Quick reference</span></span>
      </a></li>""" for s in supplements)
    hours = sum(c["minutes"] for c in chapters) / 60
    body = f"""  <section class="bk-card bk-cover bk-cover-small">
    <div class="bk-watermark" aria-hidden="true">{len(chapters)}</div>
    <p class="bk-kicker">Table of contents</p>
    <h1 class="bk-title">{esc(BOOK['title'])}</h1>
    <p class="bk-sub">{len(chapters)} chapters in {len(units)} units, about {round(hours)} hours of reading</p>
    <p class="bk-note">While the book finishes moving to this site, chapters open on EdTechBooks.</p>
  </section>

{chr(10).join(blocks)}

  <section class="bk-unit" aria-labelledby="supp">
    <div class="bk-unit-head">
      <div>
        <p class="bk-kicker">Reference</p>
        <h2 class="bk-unit-title" id="supp">Supplemental material</h2>
      </div>
    </div>
    <ol class="bk-chapters">
{supp}
    </ol>
  </section>"""
    return page(f"Contents · {BOOK['title']}", body, 1, f"Table of contents for {BOOK['title']}")


CSS = """/* The Science of Learning: shared styles for the book's own pages.
   Layout: one 740px reading column, matching the chapters' etb title cards.
   The chapters are a light design, so these pages commit to the same single light look. */
:root {
  --ink: #1a1a1a;
  --text: #333333;
  --muted: #6b7079;
  --faint: #9aa0a8;
  --navy: #1a3a5c;
  --navy-hover: #244d78;
  --green: #2a7a4f;
  --line: #e8ebef;
  --paper: #ffffff;
  --ground: #f6f7f9;
  --tint: #eef4fb;
  --tint-line: #b8cfe0;
  --watermark: #f0f3f8;
  --ring: #8fb3d9;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color-scheme: light;
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--serif); }
a { color: var(--navy); }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--ring); outline-offset: 3px; border-radius: 4px; }

.bk-top { background: var(--paper); border-bottom: 1px solid var(--line); }
.bk-top-in, .bk, .bk-foot-in {
  max-width: 740px; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
}
.bk-top-in { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-block: .85rem; }
.bk-top-name { font-family: var(--serif); font-weight: 700; font-size: 16px; color: var(--ink); text-decoration: none; }
.bk-top nav a { font-family: var(--sans); font-size: 14px; font-weight: 600; color: var(--navy); text-decoration: none; }
.bk-top a:hover { text-decoration: underline; }

.bk { padding-block: 2rem 3rem; display: flex; flex-direction: column; gap: 2.75rem; }

/* Title card, after the chapters' .etb-title-card */
.bk-card {
  position: relative; overflow: hidden; background: var(--paper);
  border-top: 4px solid var(--navy); border-radius: 0 0 10px 10px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, .06);
  padding: 2.5rem 2rem 2rem;
}
.bk-watermark {
  position: absolute; right: -6px; top: -26px; font-family: var(--serif);
  font-size: 170px; font-weight: 700; line-height: 1; color: var(--watermark);
  user-select: none; pointer-events: none;
}
.bk-card > *:not(.bk-watermark) { position: relative; }
.bk-kicker {
  font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: .2em;
  text-transform: uppercase; color: var(--faint); margin: 0 0 .65rem;
}
.bk-title { font-family: var(--serif); font-size: clamp(30px, 6vw, 40px); font-weight: 700; line-height: 1.15; margin: 0 0 .5rem; color: var(--ink); text-wrap: balance; }
.bk-sub { font-family: var(--serif); font-size: 18px; font-style: italic; color: var(--muted); margin: 0 0 1.25rem; text-wrap: balance; }
.bk-meta { font-family: var(--sans); font-size: 13px; line-height: 1.6; color: var(--muted); margin: 0 0 1.5rem; border-top: 1px solid var(--line); padding-top: 1rem; }
.bk-note { font-family: var(--sans); font-size: 13px; line-height: 1.55; color: var(--muted); margin: 0; border-top: 1px solid var(--line); padding-top: .9rem; }
.bk-cover-small { padding: 2rem 2rem 1.6rem; }
.bk-hero { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 2rem; align-items: center; }
.bk-hero .bk-watermark { left: auto; }
.bk-cover-img {
  display: block; width: 100%; height: auto; border-radius: 3px 6px 6px 3px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, .12), 0 8px 22px rgba(26, 58, 92, .22);
}
.bk-hero-text { min-width: 0; }
.bk-cover-small .bk-title { font-size: clamp(26px, 5vw, 32px); }

.bk-actions { display: flex; flex-wrap: wrap; gap: .65rem; }
.bk-btn {
  display: inline-block; font-family: var(--sans); font-size: 15px; font-weight: 600; text-decoration: none;
  padding: .7rem 1.15rem; border-radius: 8px; border: 1px solid var(--navy);
  background: var(--navy); color: var(--paper);
}
.bk-btn:hover { background: var(--navy-hover); border-color: var(--navy-hover); }
.bk-btn-quiet { background: var(--paper); color: var(--navy); }
.bk-btn-quiet:hover { background: var(--tint); color: var(--navy); }

/* Section label, after the chapters' .etb-slbl */
.bk-slbl {
  font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase;
  color: var(--faint); margin: 0 0 1rem; padding-bottom: 6px; border-bottom: 1px solid var(--line);
}
.bk-section { display: flex; flex-direction: column; }

.bk-badge {
  flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; background: var(--navy); color: var(--paper);
  font-family: var(--serif); font-size: 14px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center;
}

.bk-unit-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .9rem; }
.bk-unit-card {
  display: flex; flex-direction: column; gap: .45rem; text-decoration: none; color: inherit;
  background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 1.15rem 1.2rem 1.25rem;
}
.bk-unit-card:hover { border-color: var(--tint-line); box-shadow: 0 2px 10px rgba(26, 58, 92, .08); }
.bk-unit-card .bk-badge { margin-bottom: .35rem; }
.bk-unit-card .bk-kicker { margin: 0; }
.bk-unit-name { font-family: var(--serif); font-size: 19px; font-weight: 700; color: var(--ink); line-height: 1.25; }
.bk-unit-hook { font-family: var(--serif); font-size: 14.5px; line-height: 1.65; color: var(--muted); }

.bk-about p { font-size: 15.5px; line-height: 1.8; color: var(--text); margin: 0 0 1rem; max-width: 65ch; }
.bk-about p:last-child { margin: 0; }
.bk-about:not(.bk-thanks) p:last-child { font-style: italic; color: var(--muted); }

/* Contents */
.bk-unit { background: var(--paper); border-radius: 10px; box-shadow: 0 1px 6px rgba(0, 0, 0, .06); padding: 1.6rem 2rem .6rem; }
.bk-unit-head { display: flex; gap: 14px; align-items: center; margin-bottom: 1rem; }
.bk-unit-head .bk-kicker { margin: 0 0 .2rem; }
.bk-unit-title { font-family: var(--serif); font-size: 23px; font-weight: 700; line-height: 1.2; margin: 0; color: var(--ink); }
.bk-unit-intro p { font-size: 15.5px; line-height: 1.8; color: var(--text); margin: 0 0 .9rem; }
.bk-outcomes { margin: .2rem 0 1rem; border: 1px solid var(--line); border-radius: 8px; background: var(--ground); }
.bk-outcomes summary { cursor: pointer; font-family: var(--sans); font-size: 13.5px; font-weight: 600; color: var(--navy); padding: .7rem .95rem; }
.bk-outcomes summary span { color: var(--faint); font-weight: 500; }
.bk-outcomes ol { margin: 0; padding: .1rem 1.1rem .9rem 2.4rem; }
.bk-outcomes li { font-size: 14.5px; line-height: 1.7; color: var(--ink); padding: .3rem 0; }
.bk-clo {
  display: inline-block; font-family: var(--sans); font-size: 10px; font-weight: 700; letter-spacing: .05em;
  color: var(--navy); background: var(--tint); border: 1px solid var(--tint-line); border-radius: 4px; padding: 1px 7px; white-space: nowrap;
}

.bk-chapters { list-style: none; margin: 0 -1rem; padding: 0; }
.bk-chapters li + li { border-top: 1px solid var(--line); }
.bk-ch {
  display: grid; grid-template-columns: 2.6rem minmax(0, 1fr) auto; gap: .9rem; align-items: baseline;
  padding: .95rem 1rem; text-decoration: none; color: inherit; border-radius: 8px;
}
.bk-ch:hover { background: var(--tint); }
.bk-ch-num { font-family: var(--serif); font-size: 22px; font-weight: 700; color: var(--tint-line); text-align: right; font-variant-numeric: tabular-nums; line-height: 1; }
.bk-ch:hover .bk-ch-num { color: var(--navy); }
.bk-ch-body { display: flex; flex-direction: column; gap: .2rem; min-width: 0; }
.bk-ch-title { font-family: var(--serif); font-size: 17px; font-weight: 700; color: var(--ink); line-height: 1.3; }
.bk-ch-sub { font-family: var(--serif); font-size: 14.5px; font-style: italic; color: var(--muted); line-height: 1.45; }
.bk-ch-time { font-family: var(--sans); font-size: 12.5px; color: var(--faint); white-space: nowrap; font-variant-numeric: tabular-nums; }

.bk-foot { border-top: 1px solid var(--line); background: var(--paper); }
.bk-foot-in { padding-block: 1.4rem 1.8rem; font-family: var(--sans); font-size: 12.5px; line-height: 1.6; color: var(--muted); }
.bk-foot-in p { margin: 0 0 .3rem; }

@media (max-width: 600px) {
  .bk-unit-grid { grid-template-columns: minmax(0, 1fr); }
  .bk-card { padding: 2rem 1.25rem 1.6rem; }
  .bk-watermark { font-size: 130px; top: -18px; }
  .bk-hero { grid-template-columns: minmax(0, 1fr); gap: 1.4rem; }
  .bk-cover-img { width: 150px; }
  .bk-unit { padding: 1.3rem 1.25rem .4rem; }
  .bk-chapters { margin: 0 -.6rem; }
  .bk-ch { grid-template-columns: 2rem minmax(0, 1fr); gap: .7rem; padding: .85rem .6rem; }
  .bk-ch-time { grid-column: 2; margin-top: -.15rem; }
}
"""


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


def main():
    units, chapters, supplements = load_book()
    (OUT / "contents").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    build_cover()
    (OUT / "index.html").write_text(build_home(units, chapters))
    (OUT / "contents" / "index.html").write_text(build_contents(units, chapters, supplements))
    (OUT / "assets" / "book.css").write_text(CSS)
    print(f"{len(units)} units, {len(chapters)} chapters, {len(supplements)} supplements")
    for u in units:
        print(f"  {u['label']}: {u['name']} | {chapter_range(u)} | {len(u['outcomes'])} outcomes | intro paras {len(u['intro'])}")


if __name__ == "__main__":
    main()
