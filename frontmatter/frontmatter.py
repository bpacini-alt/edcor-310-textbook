"""Front pages shared by both textbooks: the cover, the table of contents, and About this book.

This file is identical in edcor-310-textbook and Econ-150-textbook. Change it in both, in
matching pull requests, the same way as the audio player. Each book keeps its own data
(titles, chapters, colors) in its own build script and passes it to render().

render(book) returns {path: html} for:
  index.html            the cover
  contents/index.html   the table of contents
  about.html            About this book (only when the book has about text)
  assets/book.css       the shared styles

Links are root-relative ("/contents/index.html"), so the pages work at any depth.

The `book` dict:
  title, subtitle, course, school, byline           strings
  footer_html                                       list of footer lines, as HTML (so a license can be a link)
  site                                              "https://learning.benjaminpacini.com"
  cover        {"src", "width", "height", "alt"}
  theme        {"accent", "accent_hover", "numeral", "badge_bg", "badge_fg", "kicker", "tint", "tint_line", "watermark"}
  (the cover's chapter picker is built from front + units; no extra data needed)
  stats        "26 chapters in 4 units · about 21 hours of reading · free and open"
  contents_sub "26 chapters in 4 units, about 21 hours of reading"
  count        "26"                                 the faint number on the contents card
  front        [{"n", "t", "s", "m", "href"}]       Before Chapter 1
  units        [{"roman", "kicker", "title", "hook", "outcomes": [(text, [clo, ...])], "chapters": [{"n", "t", "s", "m", "href"}]}]
               a chapter may also carry "divider": "The Closing Reckoning" to start a small subheading inside its unit
  back_title   "Readings and quick references"
  back         [{"n", "t", "s", "href"}]
  about        {"paras": [...], "thanks": [...]} or None
"""
import html

AUTHOR_NAME = "Benjamin Pacini"
AUTHOR_SITE = "https://benjaminpacini.com/"


def esc(s):
    return html.escape(str(s or ""), quote=True)


def _theme_style(t):
    return ("<style>:root{"
            f"--accent:{t['accent']};--accent-hover:{t['accent_hover']};--numeral:{t['numeral']};"
            f"--badge-bg:{t['badge_bg']};--badge-fg:{t['badge_fg']};--kicker:{t['kicker']};"
            f"--tint:{t['tint']};--tint-line:{t['tint_line']};--watermark:{t['watermark']};"
            "}</style>")


def _page(book, title, description, body, current=""):
    contents_attr = ' aria-current="page"' if current == "contents" else ""
    footer = "\n".join(f"    <p>{p}</p>" for p in book["footer_html"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{esc(book['site'])}{esc(book['cover']['src'])}">
<link rel="stylesheet" href="/assets/book.css">
{_theme_style(book['theme'])}
</head>
<body>
<header class="fm-top">
  <div class="fm-top-in">
    <div class="fm-crumbs">
      <a class="fm-author" href="{AUTHOR_SITE}">{AUTHOR_NAME}</a>
      <span class="fm-slash" aria-hidden="true">/</span>
      <a class="fm-book" href="/">{esc(book['title'])}</a>
    </div>
    <nav aria-label="Book"><a class="fm-contents-link" href="/contents/index.html"{contents_attr}>Contents</a></nav>
  </div>
</header>
<main class="fm-main">
{body}
</main>
<footer class="fm-foot">
  <div class="fm-foot-in">
{footer}
  </div>
</footer>
</body>
</html>
"""


def _picker(book):
    """A compact chapter picker: one native dropdown and a Go button. Phones open their own list."""
    groups = []
    if book["front"]:
        groups.append(("Before Chapter 1", book["front"]))
    for i, u in enumerate(book["units"], 1):
        groups.append((f"Unit {i} · {u['title']}", u["chapters"]))
    opts = []
    for label, items in groups:
        rows = "".join(f'<option value="{esc(c["href"])}">{esc(c["n"])}. {esc(c["t"])}</option>' for c in items)
        opts.append(f'<optgroup label="{esc(label)}">{rows}</optgroup>')
    return f"""      <form class="fm-jump" onsubmit="if(this.c.value)location.href=this.c.value;return false;">
        <label class="fm-jump-label" for="fm-jump">Jump to a chapter</label>
        <select id="fm-jump" name="c" required><option value="">Choose a chapter…</option>{''.join(opts)}</select>
        <button class="fm-jump-go" type="submit">Go</button>
      </form>"""


def _cover(book):
    c = book["cover"]
    body = f"""  <section class="fm-cover" aria-labelledby="fm-title">
    <img class="fm-cover-img" src="{esc(c['src'])}" width="{c['width']}" height="{c['height']}" alt="{esc(c['alt'])}">
    <div class="fm-cover-text">
      <p class="fm-kicker">{esc(book['course'])} · {esc(book['school'])}</p>
      <h1 class="fm-cover-title" id="fm-title">{esc(book['title'])}</h1>
      <p class="fm-cover-sub">{esc(book['subtitle'])}</p>
      <p class="fm-byline">{esc(book['byline'])}</p>
    </div>
    <div class="fm-actions">
      <a class="fm-btn" href="/contents/index.html">Table of contents</a>
{_picker(book)}
    </div>
    <p class="fm-stats">{esc(book['stats'])}</p>
  </section>"""
    return _page(book, book["title"], book["subtitle"], body)


def _rows(items, numeral_class="fm-num", with_time=True):
    out = []
    for c in items:
        if c.get("divider"):
            out.append(f'      <li class="fm-divider"><span>{esc(c["divider"])}</span></li>')
        time = f'\n        <span class="fm-time">{esc(c["m"])}</span>' if with_time and c.get("m") else ""
        sub = f'<span class="fm-row-sub">{esc(c["s"])}</span>' if c.get("s") else ""
        out.append(f"""      <li><a class="fm-row" href="{esc(c['href'])}">
        <span class="{numeral_class}">{esc(c['n'])}</span>
        <span class="fm-row-body"><span class="fm-row-title">{esc(c['t'])}</span>{sub}</span>{time}
      </a></li>""")
    return "\n".join(out)


def _contents(book):
    c = book["cover"]
    sections = []
    if book["front"]:
        sections.append(f"""  <section class="fm-panel" id="start" aria-labelledby="start-h">
    <p class="fm-label">Front matter</p>
    <h2 class="fm-panel-title" id="start-h">Before Chapter 1</h2>
    <ol class="fm-rows">
{_rows(book['front'], 'fm-num fm-num-small')}
    </ol>
  </section>""")
    for i, u in enumerate(book["units"], 1):
        hook = f'\n    <p class="fm-hook">{esc(u["hook"])}</p>' if u.get("hook") else ""
        outcomes = ""
        if u.get("outcomes"):
            def clo_tags(clos):
                return "".join(' <span class="fm-clo">' + esc(clo) + "</span>" for clo in clos)
            items = "\n".join(f"        <li>{esc(text)}{clo_tags(clos)}</li>" for text, clos in u["outcomes"])
            outcomes = f"""
    <details class="fm-outcomes">
      <summary>Unit outcomes <span>({len(u['outcomes'])})</span></summary>
      <ol>
{items}
      </ol>
    </details>"""
        sections.append(f"""  <section class="fm-panel" id="unit-{i}" aria-labelledby="unit-{i}-h">
    <div class="fm-unit-head">
      <span class="fm-badge" aria-hidden="true">{esc(u['roman'])}</span>
      <div>
        <p class="fm-label">{esc(u['kicker'])}</p>
        <h2 class="fm-panel-title" id="unit-{i}-h">{esc(u['title'])}</h2>
      </div>
    </div>{hook}{outcomes}
    <ol class="fm-rows">
{_rows(u['chapters'])}
    </ol>
  </section>""")
    body = f"""  <section class="fm-card fm-contents-card" aria-labelledby="fm-title">
    <div class="fm-watermark" aria-hidden="true">{esc(book['count'])}</div>
    <img class="fm-thumb" src="{esc(c['src'])}" width="{c['width']}" height="{c['height']}" alt="">
    <div>
      <p class="fm-kicker">Table of contents</p>
      <h1 class="fm-card-title" id="fm-title">{esc(book['title'])}</h1>
      <p class="fm-card-sub">{esc(book['contents_sub'])}</p>
    </div>
  </section>

{chr(10).join(sections)}"""
    return _page(book, f"Contents · {book['title']}", f"Table of contents for {book['title']}", body, "contents")


def _about(book):
    a = book["about"]
    paras = "\n".join(f"    <p>{esc(p)}</p>" for p in a["paras"])
    thanks = ""
    if a.get("thanks"):
        thanks = "\n    <h2 class=\"fm-about-h\">Acknowledgments</h2>\n" + "\n".join(f"    <p>{esc(p)}</p>" for p in a["thanks"])
    body = f"""  <article class="fm-card fm-about" aria-labelledby="fm-title">
    <p class="fm-kicker">Front matter</p>
    <h1 class="fm-card-title" id="fm-title">About this book</h1>
{paras}{thanks}
    <p class="fm-about-next"><a href="/contents/index.html">Back to the contents</a></p>
  </article>"""
    return _page(book, f"About this book · {book['title']}", f"About {book['title']}: how it was made, and acknowledgments", body)


def render(book):
    pages = {
        "index.html": _cover(book),
        "contents/index.html": _contents(book),
        "assets/book.css": CSS,
    }
    if book.get("about"):
        pages["about.html"] = _about(book)
    return pages


CSS = """/* Front pages shared by both textbooks (frontmatter/frontmatter.py). Each page sets the
   book's colors (--accent, --numeral, ...) in its <head>; everything else is the same. */
:root {
  --ink: #1a1a1a;
  --text: #333333;
  --muted: #5f6570;
  --soft: #6b7079;
  --line: #e8ebef;
  --paper: #ffffff;
  --ground: #f6f7f9;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color-scheme: light;
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; min-height: 100vh; display: flex; flex-direction: column; background: var(--ground); color: var(--ink); font-family: var(--serif); }
a { color: var(--accent); }
a:hover { color: var(--accent-hover); }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--tint-line); outline-offset: 3px; border-radius: 4px; }

/* Top bar: Benjamin Pacini / Book / Contents, the same on every front page */
.fm-top { background: var(--paper); border-bottom: 1px solid var(--line); }
.fm-top-in, .fm-foot-in { max-width: 880px; margin: 0 auto; padding: 12px max(16px, env(safe-area-inset-left, 0px)); }
.fm-top-in { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.fm-crumbs { display: flex; align-items: center; gap: 4px 10px; flex-wrap: wrap; min-width: 0; flex: 1; }
.fm-top nav { flex-shrink: 0; }
.fm-author { font-family: var(--sans); font-size: 13px; font-weight: 600; color: var(--muted); text-decoration: none; }
.fm-slash { color: #c3c8cf; }
.fm-book { font-size: 16px; font-weight: 700; color: var(--ink); text-decoration: none; }
.fm-contents-link { font-family: var(--sans); font-size: 14px; font-weight: 600; text-decoration: none; }
.fm-top a:hover { text-decoration: underline; }

.fm-main { flex: 1; width: 100%; max-width: 792px; margin: 0 auto; padding: 32px 16px 64px; display: flex; flex-direction: column; gap: 22px; }

/* Cover */
.fm-cover { max-width: 560px; margin: 24px auto 0; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 30px; }
.fm-cover-img { width: 290px; max-width: 72%; height: auto; border-radius: 3px 7px 7px 3px; box-shadow: 0 1px 2px rgba(0, 0, 0, .15), 0 20px 44px color-mix(in srgb, var(--accent) 32%, transparent); }
.fm-cover-text { display: flex; flex-direction: column; gap: 10px; align-items: center; }
.fm-kicker { margin: 0; font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--kicker); }
.fm-cover-title { margin: 0; font-size: clamp(32px, 7vw, 40px); font-weight: 700; line-height: 1.12; text-wrap: balance; }
.fm-cover-sub { margin: 0; font-size: 19px; font-style: italic; color: var(--muted); text-wrap: balance; }
.fm-byline { margin: 6px 0 0; font-family: var(--sans); font-size: 14.5px; color: #3d434c; }
.fm-actions { display: flex; flex-direction: column; align-items: center; gap: 14px; }
.fm-btn { display: inline-flex; align-items: center; min-height: 46px; padding: 0 22px; border-radius: 8px; background: var(--accent); border: 1px solid var(--accent); color: #ffffff; font-family: var(--sans); font-size: 15px; font-weight: 600; text-decoration: none; }
.fm-btn:hover { background: var(--accent-hover); border-color: var(--accent-hover); color: #ffffff; }
.fm-btn-quiet { background: var(--paper); color: var(--accent); }
.fm-btn-quiet:hover { background: var(--tint); color: var(--accent); }
.fm-jump { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 6px 8px; font-family: var(--sans); }
.fm-jump-label { font-size: 13px; color: var(--muted); }
.fm-jump select { min-height: 36px; max-width: min(300px, 70vw); padding: 0 8px; border: 1px solid #d5dbe2; border-radius: 6px; background: var(--paper); color: var(--ink); font: 14px var(--sans); }
.fm-jump-go { min-height: 36px; padding: 0 12px; border: 1px solid var(--accent); border-radius: 6px; background: var(--paper); color: var(--accent); font: 600 14px var(--sans); cursor: pointer; }
.fm-jump-go:hover { background: var(--tint); }
.fm-jump select:focus-visible, .fm-jump-go:focus-visible { outline: 3px solid var(--tint-line); outline-offset: 2px; }
.fm-stats { margin: 0; padding-top: 16px; border-top: 1px solid #e3e7ec; font-family: var(--sans); font-size: 13px; line-height: 1.6; color: var(--muted); }

/* Contents title card, after the chapters' title cards */
.fm-card { position: relative; overflow: hidden; background: var(--paper); border-top: 4px solid var(--accent); border-radius: 0 0 10px 10px; box-shadow: 0 1px 6px rgba(0, 0, 0, .06); padding: 30px 28px; }
.fm-contents-card { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; }
.fm-card > *:not(.fm-watermark) { position: relative; }
.fm-watermark { position: absolute; right: -6px; top: -26px; font-size: 170px; font-weight: 700; line-height: 1; color: var(--watermark); user-select: none; pointer-events: none; }
.fm-thumb { width: 72px; height: auto; border-radius: 2px 4px 4px 2px; box-shadow: 0 1px 2px rgba(0, 0, 0, .15), 0 6px 14px color-mix(in srgb, var(--accent) 30%, transparent); }
.fm-contents-card .fm-kicker { margin-bottom: 6px; }
.fm-card-title { margin: 0 0 6px; font-size: clamp(26px, 5vw, 32px); font-weight: 700; line-height: 1.15; }
.fm-card-sub { margin: 0; font-size: 16px; font-style: italic; color: var(--muted); }

/* Contents panels */
.fm-panel { background: var(--paper); border-radius: 10px; box-shadow: 0 1px 6px rgba(0, 0, 0, .06); padding: 24px 28px 8px; scroll-margin-top: 16px; }
.fm-label { margin: 0 0 4px; font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--soft); }
.fm-panel-title { margin: 0 0 12px; font-size: 23px; font-weight: 700; line-height: 1.2; }
.fm-unit-head { display: flex; gap: 14px; align-items: center; margin-bottom: 12px; }
.fm-unit-head .fm-panel-title { margin: 0; }
.fm-badge { flex-shrink: 0; width: 38px; height: 38px; border-radius: 50%; background: var(--badge-bg); color: var(--badge-fg); font-size: 14px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; }
.fm-hook { margin: 0 0 14px; font-size: 15.5px; line-height: 1.7; color: var(--text); max-width: 62ch; }
.fm-outcomes { margin: 0 0 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--ground); }
.fm-outcomes summary { cursor: pointer; padding: 10px 14px; font-family: var(--sans); font-size: 13.5px; font-weight: 600; color: var(--accent); }
.fm-outcomes summary span { color: var(--soft); font-weight: 500; }
.fm-outcomes ol { margin: 0; padding: 0 16px 12px 34px; }
.fm-outcomes li { font-size: 14.5px; line-height: 1.65; padding: 4px 0; }
.fm-clo { display: inline-block; font-family: var(--sans); font-size: 10px; font-weight: 700; letter-spacing: .05em; color: var(--accent); background: var(--tint); border: 1px solid var(--tint-line); border-radius: 4px; padding: 1px 7px; white-space: nowrap; }

.fm-rows { list-style: none; margin: 0 -12px; padding: 0; }
.fm-rows li { border-top: 1px solid var(--line); }
.fm-rows li.fm-divider { padding: 16px 12px 6px; }
.fm-divider span { font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--kicker); }
.fm-row { display: grid; grid-template-columns: 44px minmax(0, 1fr) auto; gap: 14px; align-items: baseline; padding: 14px 12px; text-decoration: none; color: var(--ink); border-radius: 8px; }
.fm-row:hover { background: var(--tint); color: var(--ink); }
.fm-num { font-size: 22px; font-weight: 700; line-height: 1; color: var(--numeral); text-align: right; font-variant-numeric: tabular-nums; }
.fm-num-small { font-size: 18px; font-weight: 400; font-style: italic; }
.fm-row-body { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.fm-row-title { font-size: 17px; font-weight: 700; line-height: 1.3; }
.fm-row-sub { font-size: 14.5px; font-style: italic; color: var(--muted); line-height: 1.45; }
.fm-time { font-family: var(--sans); font-size: 12.5px; color: var(--soft); white-space: nowrap; font-variant-numeric: tabular-nums; }

/* About this book */
.fm-about p { font-size: 16px; line-height: 1.8; color: var(--text); margin: 0 0 1rem; max-width: 65ch; }
.fm-about .fm-kicker { margin-bottom: 8px; }
.fm-about .fm-card-title { margin-bottom: 18px; }
.fm-about-h { margin: 28px 0 10px; padding-bottom: 6px; border-bottom: 1px solid var(--line); font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--soft); }
.fm-about .fm-about-next { margin: 24px 0 0; font-family: var(--sans); font-size: 14px; font-weight: 600; }

.fm-foot { background: var(--paper); border-top: 1px solid var(--line); }
.fm-foot-in { padding-block: 18px 22px; font-family: var(--sans); font-size: 12.5px; line-height: 1.6; color: var(--muted); }
.fm-foot-in p { margin: 0 0 4px; }

@media (max-width: 600px) {
  .fm-main { padding-top: 24px; }
  .fm-cover { margin-top: 8px; gap: 24px; }
  .fm-cover-img { width: 220px; }
  .fm-card { padding: 24px 20px; }
  .fm-watermark { font-size: 130px; top: -18px; }
  .fm-panel { padding: 20px 18px 6px; }
  .fm-rows { margin: 0 -8px; }
  .fm-row { grid-template-columns: 30px minmax(0, 1fr); gap: 10px; padding: 12px 8px; }
  .fm-time { grid-column: 2; margin-top: -2px; }
}
"""
