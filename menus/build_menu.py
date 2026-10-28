"""Build a Joy reading menu page (Joy of Learning, Joy of Econ) from its data file.

Identical copies live in both textbook repositories (menus/build_menu.py), along with
menus/joy-menu.css and menus/joy-menu.js. Change all three in both repositories in
matching pull requests. Each repository keeps its own menu data in menus/<name>.json.

Usage, from the repository root:
    python3 menus/build_menu.py menus/joy-of-learning.json site/joy-of-learning.html

The page is one self-contained file: the CSS and JS are inlined, and every reading is
written into the HTML, so the menu still works (without buttons) if the script fails.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAT_LABEL = {"watch": "Watch", "listen": "Listen", "read": "Read"}
STANCE = {"Pro-market": ("pro", "jm-stance-pro"), "Market-critique": ("crit", "jm-stance-crit")}


def esc(s):
    return html.escape(s or "", quote=True)


def entry_html(e, scope_id, titles):
    stance_key, stance_cls = STANCE.get(e.get("stance") or "", ("none", ""))
    search = " ".join(filter(None, [e["title"], e.get("topic"), e.get("stance"), e.get("hook"), e.get("blurb"), e.get("source")])).lower()
    meta = ['<span class="jm-format">%s</span>' % FORMAT_LABEL[e["format"]]]
    if e.get("topic"):
        meta.append('<span class="jm-topic">%s</span>' % esc(e["topic"]))
    if e.get("stance"):
        meta.append('<span class="jm-stance %s">%s</span>' % (stance_cls, esc(e["stance"])))
    plan = (
        '<span class="jm-plan" data-actions aria-label="Reading plan">'
        '<button type="button" class="jm-btn jm-btn-mine" data-choice="mine" aria-pressed="false" aria-label="Add to my readings" title="I’ll read this">mine</button>'
        '<button type="button" class="jm-btn jm-btn-group" data-choice="group" aria-pressed="false" aria-label="My group has it" title="My group has it">group</button>'
        '</span>'
    )
    ratings = (
        '<span class="jm-rating-cell" data-ratings>'
        '<span class="jm-rating-buttons" role="group" aria-label="Bang for buck">'
        '<button type="button" class="jm-btn jm-rating-btn" data-rating="1" aria-pressed="false" aria-label="F-tier · Replace" title="F-tier · Replace">1</button>'
        '<button type="button" class="jm-btn jm-rating-btn" data-rating="2" aria-pressed="false" aria-label="B-tier · Reconsider" title="B-tier · Reconsider">2</button>'
        '<button type="button" class="jm-btn jm-rating-btn" data-rating="3" aria-pressed="false" aria-label="A-tier · Keep" title="A-tier · Keep">3</button>'
        '<button type="button" class="jm-btn jm-rating-btn" data-rating="4" aria-pressed="false" aria-label="S-tier · Life-changing · Celebrate" title="S-tier · Life-changing · Celebrate">4</button>'
        '</span>'
        '</span>'
    )
    out = [
        '<details class="jm-entry" id="r-%s" data-id="%s" data-min="%d" data-format="%s" data-stance="%s" data-scope-id="%s" data-search="%s">'
        % (esc(e["id"]), esc(e["id"]), e["minutes"], e["format"], stance_key, scope_id, esc(search)),
        '<summary class="jm-entry-summary">',
        '<span class="jm-entry-title"><a href="%s" target="_blank" rel="noopener" title="%s">%s</a><span class="jm-sr"> (opens in a new tab)</span></span>'
        % (esc(e["url"]), esc(e["title"]), esc(e["title"])),
        '<span class="jm-entry-meta">%s</span>' % "".join(meta),
        '<span class="jm-entry-time">~%d min</span>' % e["minutes"],
        plan,
        ratings,
        '<span class="jm-entry-chevron" aria-hidden="true">+</span>',
        '<span class="jm-vote-tools" aria-label="Vote distribution controls">',
        '<button type="button" class="jm-btn jm-view-votes" aria-label="Reveal votes for this reading">Reveal</button>',
        '<span class="jm-rating-summary jm-hidden" aria-live="polite"></span>',
        '</span>',

        '</summary>',
        '<div class="jm-entry-detail">',
    ]
    blurb = esc(e.get("blurb"))
    if e.get("hook"):
        # Space inside the tag, per house style for HTML that may be pasted into editors.
        blurb = '<em class="jm-hook">%s </em>%s' % (esc(e["hook"]), blurb)
    out.append('<p class="jm-blurb">%s</p>' % blurb)
    if e.get("source"):
        out.append('<p class="jm-source">%s</p>' % esc(e["source"]))
    if e.get("alt"):
        links = " · ".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(a["url"]), esc(a["label"])) for a in e["alt"])
        out.append('<p class="jm-alt">Also available: %s</p>' % links)
    if e.get("pairs"):
        links = " · ".join('<a href="#r-%s">%s</a>' % (esc(p), esc(titles[p])) for p in e["pairs"])
        out.append('<p class="jm-pairs">Pairs with: %s</p>' % links)

    out.append('</div>')
    out.append('</details>')
    return "\n".join(out)


def hours(m):
    if m < 60:
        return "%d min" % m
    h, r = divmod(m, 60)
    return "%d hr" % h + (" %d min" % r if r else "")


def build(data):
    c = data["course"]
    # The plan meter tracks each unit. A course states its requirement per week (EDCOR 310: about an
    # hour a week, chosen from the unit's menu) or per unit (Econ 150: an hour per unit).
    per_week = c["requirement"] == "hour-per-week"
    titles = {e["id"]: e["title"] for u in data["units"] for w in u["weeks"] for e in w["entries"]}
    assert len(titles) == sum(len(w["entries"]) for u in data["units"] for w in u["weeks"]), "duplicate reading ids"
    for u in data["units"]:
        for w in u["weeks"]:
            for e in w["entries"]:
                for p in e.get("pairs", []):
                    assert p in titles, "pairs-with points at a missing id: %s -> %s" % (e["id"], p)

    scopes = []
    units_html = []
    for u in data["units"]:
        weeks_html = []
        for w in u["weeks"]:
            scope_id = u["id"]
            note = "".join('<p class="jm-note"><strong>A note. </strong>%s</p>' % esc(n) for n in w.get("notes", []))
            body = "\n".join(entry_html(e, scope_id, titles) for e in w["entries"])
            mins = sum(e["minutes"] for e in w["entries"])
            weeks_html.append(
                '<section class="jm-week" id="%s" aria-labelledby="%s-h">\n<div class="jm-week-head"><h3 id="%s-h">%s</h3><span class="jm-week-meter">%d readings · %s of options</span></div>\n%s<div class="jm-list">\n<div class="jm-list-head" aria-hidden="true"><span>Reading</span><span>Format / lens</span><span>Time</span><span>Plan</span><span>Bang for buck</span></div>\n%s\n</div>\n</section>'
                % (w["id"], w["id"], w["id"], esc(w["title"]), len(w["entries"]), hours(mins), note, body)
            )
        target = 60 * (len(u["weeks"]) if per_week else 1)
        scopes.append((u["id"], "%s (%s)" % (u["label"], hours(target))))
        uattrs = ' data-scope="%s" data-scope-label="%s" data-target="%d"' % (u["id"], esc(u["label"] + ": " + u["title"]), target)
        umeter = '<p class="jm-unit-meter" data-meter aria-live="polite"></p>'
        open_attr = " open" if not units_html else ""
        units_html.append(
            '<details class="jm-unit" id="%s"%s%s aria-labelledby="%s-h">\n<summary class="jm-unit-head"><p class="jm-unit-label">%s</p><h2 id="%s-h">%s</h2><p class="jm-unit-meta">%s</p><p class="jm-unit-blurb">%s</p>%s</summary>\n%s\n</details>'
            % (u["id"], open_attr, uattrs, u["id"], esc(u["label"]), u["id"], esc(u["title"]), esc(u["meta"]), esc(u["blurb"]), umeter, "\n".join(weeks_html))
        )

    howto = "\n".join(
        "<p><strong>%s </strong>%s</p>" % (esc(s["head"]), esc(s["body"])) if s.get("head") else "<p>%s</p>" % esc(s["body"])
        for s in data["intro"]["sections"]
    )
    units_nav = "".join('<li><a href="#%s">%s</a></li>' % (u["id"], esc(u["label"] + ": " + u["title"])) for u in data["units"])
    scope_opts = "".join('<option value="%s">%s</option>' % (sid, esc(lbl)) for sid, lbl in scopes)

    stance_row = ""
    if c.get("stanceFilter"):
        stance_row = (
            '<div class="jm-chiprow" role="group" aria-label="Viewpoint"><span>Viewpoint</span>'
            '<button type="button" class="jm-chip" data-group="stance" data-value="pro" aria-pressed="false">Pro-market</button>'
            '<button type="button" class="jm-chip" data-group="stance" data-value="crit" aria-pressed="false">Market critique</button>'
            '<button type="button" class="jm-chip" data-group="stance" data-value="none" aria-pressed="false">Other</button></div>'
        )

    appendix = ""
    if data.get("appendix"):
        a = data["appendix"]
        groups = []
        for g in a["groups"]:
            items = "".join(
                '<li><a href="%s" target="_blank" rel="noopener">%s</a> — %s</li>' % (esc(i["url"]), esc(i["title"]), esc(i["blurb"]))
                for i in g["items"]
            )
            groups.append("<h3>%s</h3><ul>%s</ul>" % (esc(g["title"]), items))
        appendix = '<details class="jm-appendix"><summary>%s</summary><p>%s</p>%s</details>' % (esc(a["title"]), esc(a["intro"]), "".join(groups))

    config = {
        "storageKey": c["storageKey"],
        "menuTitle": c["menuTitle"],
        "ratingsBook": c.get("ratingsBook"),
        "ratingsEndpoint": "/api/ratings",
    }
    css = (HERE / "joy-menu.css").read_text(encoding="utf-8")
    js = (HERE / "joy-menu.js").read_text(encoding="utf-8")
    total = len(titles)
    # The book's Report a problem button, so students can flag a dead or wrong link.
    report = ('<script src="%s" data-book="%s" defer></script>' % (esc(c["reportScript"]), esc(c["course"]))) if c.get("reportScript") else ""

    return f"""<!doctype html>
<!-- GENERATED by menus/build_menu.py from menus/{esc(c['dataFile'])}. Edit the data file and rebuild; hand edits here are overwritten. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c['menuTitle'])} · {esc(c['course'])}</title>
<meta name="description" content="{esc(c['description'])}">
<style>:root{{--acc:{c['accent']};--acc2:{c.get('accent2') or c['accent']};--ring:{c.get('ring', '#8fb3d9')};}}</style>
<style>
{css}
</style>
</head>
<body>
<header class="jm-top"><div class="jm-wrap jm-top-in">
<a class="jm-top-name" href="https://benjaminpacini.com">Benjamin Pacini</a>
<nav aria-label="Book"><a href="{esc(c['bookHome'])}">{esc(c['bookTitle'])}</a><a href="{esc(c['contents'])}">Contents</a></nav>
</div></header>
<div class="jm-bar jm-needs-js jm-hidden"><div class="jm-wrap jm-bar-in">
<label for="jm-scope">Your picks for</label>
<select id="jm-scope">{scope_opts}</select>
<div class="jm-meter"><div class="jm-meter-track" aria-hidden="true"><div class="jm-meter-fill" id="jm-meter-fill"></div></div><span class="jm-meter-text" id="jm-meter-text" aria-live="polite"></span></div>
<div class="jm-bar-actions"><button type="button" class="jm-btn jm-btn-strong" id="jm-copy">Copy my list</button><button type="button" class="jm-btn" id="jm-clear">Clear my picks</button></div>
</div></div>
<div class="jm-wrap" style="padding-top:2rem">
<section class="jm-card" aria-labelledby="jm-title">
<p class="jm-kicker">{esc(c['course'])} · Reading Menu</p>
<h1 class="jm-title" id="jm-title">{esc(c['menuTitle'])}</h1>
<p class="jm-lede">{esc(data['intro']['lede'])}</p>
<details class="jm-howto" open><summary>How this works</summary><div class="jm-howto-body">
{howto}
</div></details>
</section>
<nav aria-label="Units"><ul class="jm-units-nav">{units_nav}</ul></nav>
</div>
<main class="jm-wrap">
<section class="jm-filters jm-needs-js jm-hidden" aria-label="Find readings">
<label class="jm-sr" for="jm-search">Search the readings</label>
<input type="search" id="jm-search" placeholder="Search titles, topics, and descriptions" autocomplete="off">
<div class="jm-chiprow" role="group" aria-label="Format"><span>Format</span>
<button type="button" class="jm-chip" data-group="format" data-value="watch" aria-pressed="false">Watch</button>
<button type="button" class="jm-chip" data-group="format" data-value="listen" aria-pressed="false">Listen</button>
<button type="button" class="jm-chip" data-group="format" data-value="read" aria-pressed="false">Read</button></div>
<div class="jm-chiprow" role="group" aria-label="Length"><span>Length</span>
<button type="button" class="jm-chip" data-group="length" data-value="short" aria-pressed="false">≤10 min</button>
<button type="button" class="jm-chip" data-group="length" data-value="medium" aria-pressed="false">11–25 min</button>
<button type="button" class="jm-chip" data-group="length" data-value="long" aria-pressed="false">25+ min</button></div>
{stance_row}
<div class="jm-chiprow" role="group" aria-label="Show"><span>Show</span>
<button type="button" class="jm-chip" data-group="view" data-value="mine" aria-pressed="false">Mine only</button>
<button type="button" class="jm-chip" data-group="view" data-value="open" aria-pressed="false">Hide group</button></div>
<p class="jm-count" id="jm-count" aria-live="polite">Showing all {total} readings</p>
</section>
{chr(10).join(units_html)}
{appendix}
<div class="jm-instructor-tools"><button type="button" class="jm-btn" id="jm-reveal-all" aria-label="Reveal all votes" title="Reveal all semester votes">Reveal all votes</button></div>
<p class="jm-foot">{esc(c['menuTitle'])} · {esc(c['course'])} · Your picks are saved in this browser only. They don't reach your instructor or your group.</p>
</main>
<script type="application/json" id="jm-config">{json.dumps(config)}</script>
<script>
{js}
</script>
{report}
</body>
</html>
"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))
    data["course"]["dataFile"] = src.name
    page = build(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding="utf-8")
    n = sum(len(w["entries"]) for u in data["units"] for w in u["weeks"])
    print("%s: %d readings -> %s" % (data["course"]["menuTitle"], n, dst))


if __name__ == "__main__":
    main()
