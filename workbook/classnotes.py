"""Generate the EDCOR 310 class-notes organizer as HTML (one or many front/back sets)."""
import sys, pathlib

HERE = pathlib.Path(__file__).parent
FONT = HERE / "node_modules/@fontsource/lato/files"
RCF = HERE / "node_modules/@fontsource/roboto-condensed/files"
KF = HERE / "node_modules/@fontsource/kalam/files"

WEEKS = list(range(1, 14))   # weeks 1-13; 99 Studies / Paper of the Week start in week 2


UNIT_END = {4: 1, 7: 2, 10: 3, 13: 4}   # a Unit Review follows these weeks


def layout():
    """Every numbered page in order, as (pdf, page index, key). Drives page numbers and build order.
    Week 1 is class notes only; later weeks add 99 Studies and Paper of the Week; a two-page
    Unit Review follows weeks 4, 7, 10, and 13; the Course Synthesis closes the book.
    Every section has an even page count, and the purpose page after the cover shifts the book by one,
    so each two-page section opens as a facing spread (A on the left, B on the right)."""
    seq = []
    for w in WEEKS:
        for d in (1, 2):
            for b in (False, True):
                seq.append(("classnotes", 4 * (w - 1) + (d - 1) * 2 + b, ("notes", w, d, b)))
        if w > 1:
            seq += [("studies", w - 2, ("99", w)), ("paper_of_week", w - 2, ("potw", w))]
        if w in UNIT_END:
            u = UNIT_END[w]
            seq += [("review", 2 * (u - 1) + k, ("review", u, k)) for k in (0, 1)]
    seq += [("synthesis", k, ("synth", k)) for k in (0, 1)]
    return seq


PAGE = {key: n for n, (_, _, key) in enumerate(layout(), 1)}


def pg_for(kind, week, day=1, back=False):
    if kind == "notes":
        return PAGE[("notes", week, day, bool(back))]
    return PAGE[(kind, week)]


def foot(label, pg, right):
    return f'<footer><div>{label}</div><div class="mid">{pg}</div><div>{right}</div></footer>'


BLANK_WD = 'Week <span class="fill short"></span>&nbsp;&middot;&nbsp; Day <span class="fill short"></span>'
BLANK_W = 'Week <span class="fill short"></span>'

CSS = f"""
@font-face {{ font-family: Lato; font-weight: 400; src: url('{FONT}/lato-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 400; font-style: italic; src: url('{FONT}/lato-latin-400-italic.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 700; src: url('{FONT}/lato-latin-700-normal.woff2'); }}
@font-face {{ font-family: RC; font-weight: 400; src: url('{RCF}/roboto-condensed-latin-400-normal.woff2'); }}
@font-face {{ font-family: RC; font-weight: 700; src: url('{RCF}/roboto-condensed-latin-700-normal.woff2'); }}
@font-face {{ font-family: Kalam; font-weight: 400; src: url('{KF}/kalam-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 900; src: url('{FONT}/lato-latin-900-normal.woff2'); }}
@page {{ size: 8.5in 11in; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #fff; }}
body {{ font-family: Lato, sans-serif; color: #111; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 8.5in; height: 11in; padding: 0.16in; page-break-after: always; break-after: page; overflow: hidden; }}
.frame {{ border: 1.3px solid #333; height: 100%; padding: 0.2in 0.28in 0.12in; display: flex; flex-direction: column; gap: 0.13in; }}

h1 {{ text-align: center; font-family: RC, sans-serif; font-weight: 700; font-size: 40px; letter-spacing: 0; line-height: 1; margin-top: 2px; }}
.blurb {{ font-size: 12.6px; line-height: 1.42; padding: 0 0.1in; margin-top: -2px; }}
.blurb b {{ font-weight: 700; }}

.box {{ border: 1.8px solid #111; border-radius: 11px; display: flex; flex-direction: column; overflow: hidden; }}
.box.grow {{ flex: 1 1 auto; min-height: 0; }}
.bar {{ display: flex; align-items: center; border-bottom: 1.5px solid #111; min-height: 30px; }}
.tab {{ background: #111; color: #fff; font-family: RC, sans-serif; font-weight: 700; font-size: 15.5px; letter-spacing: 0.9px; padding: 6px 16px 6px 14px; border-radius: 0 0 10px 0; align-self: stretch; display: flex; align-items: center; }}
.bar .hint {{ font-size: 11.5px; font-style: italic; color: #333; padding-left: 14px; flex: 1; }}
.bar .date {{ font-size: 12.5px; font-weight: 700; padding-right: 14px; }}
.bar .date span {{ display: inline-block; width: 1.25in; border-bottom: 1.2px solid #111; margin-left: 4px; }}

.cols {{ display: grid; flex: 1 1 auto; min-height: 0; }}
.cell {{ padding: 8px 12px 6px; display: flex; flex-direction: column; min-height: 0; }}
.cell + .cell {{ border-left: 1.3px solid #111; }}
.row {{ display: grid; border-top: 1.3px solid #111; }}
.row:first-child {{ border-top: none; }}
.q {{ font-weight: 700; font-size: 12.5px; line-height: 1.3; }}
.q small {{ display: block; font-weight: 400; font-style: italic; font-size: 11px; color: #333; margin-top: 1px; }}
.lines {{ flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }}
.dotgrid {{ flex: 1 1 auto; margin: 8px 0 2px; background-image: radial-gradient(circle, #7a7a7a 0 1.15px, transparent 1.5px); background-size: 25px 25px; background-position: 0 0; }}
.lines {{ position: relative; }}
.tq {{ flex: 1 1 0; display: flex; flex-direction: column; min-height: 0; margin-top: 8px; }}
.tq + .tq {{ border-top: 1px dashed #999; padding-top: 6px; }}
.tql {{ font-family: RC, sans-serif; font-weight: 700; font-size: 11.5px; letter-spacing: .8px; text-transform: uppercase; color: #555; }}
.tqq {{ flex: 2.2 1 0; display: flex; flex-direction: column; min-height: 0; }}
.tqa {{ flex: 1 1 0; display: flex; flex-direction: column; min-height: 0; }}
.hw {{ position: absolute; left: 3px; right: 2px; top: 3px; font-family: Kalam, cursive; font-size: 15.5px; line-height: 25px; color: #1d3f73; white-space: pre-line; }}
.hwf {{ font-family: Kalam, cursive; color: #1d3f73; }}
.checks span.on::before {{ content: ""; background: #1d3f73; box-shadow: inset 0 0 0 2px #fff; }}
.checks.round span.on::before {{ content: ""; background: radial-gradient(circle, #1d3f73 0 3px, transparent 3.5px); }}
.rate {{ display: grid; grid-template-columns: 1fr repeat(5, 30px); align-items: center; row-gap: 3px; padding: 6px 14px 8px; font-size: 12.3px; }}
.rate .lab {{ font-weight: 700; }}
.rate .sc {{ white-space: nowrap; font-family: RC, sans-serif; font-size: 10.5px; color: #444; text-align: center; }}
.rate .o {{ width: 15px; height: 15px; border: 1.3px solid #111; border-radius: 50%; justify-self: center; position: relative; font-family: RC, sans-serif; font-size: 9px; line-height: 13px; text-align: center; color: #555; }}
.rate .o.on {{ border-color: #1d3f73; background: radial-gradient(circle, #1d3f73 0 4.5px, transparent 5px); color: transparent; }}
.dotgrid {{ position: relative; }}
.tag {{ display: inline-block; vertical-align: middle; margin-left: 12px; font-family: RC, sans-serif; font-size: 14px; letter-spacing: 2px; border: 1.6px solid #006eb6; color: #006eb6; padding: 2px 8px 1px; border-radius: 4px; position: relative; top: -4px; }}
.callout {{ position: absolute; z-index: 5; font-family: RC, sans-serif; font-size: 12px; line-height: 1.25; background: #eaf3fb; border: 1.5px solid #006eb6; color: #0b3b66; border-radius: 7px; padding: 5px 9px; box-shadow: 0 1px 0 rgba(0,0,0,.08); }}
.page {{ position: relative; }}
table.terms td .hwf {{ font-size: 16px; padding: 0 10px; display: block; line-height: 1.1; }}
.lines i {{ display: block; height: 25px; border-bottom: 1px solid #555; flex: none; }}

.checks {{ font-size: 11.5px; margin-top: 5px; display: flex; flex-wrap: wrap; gap: 4px 13px; }}
.checks span::before {{ content: ""; display: inline-block; width: 10px; height: 10px; border: 1.2px solid #111; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }}
.checks.round span::before {{ border-radius: 50%; }}

table.terms {{ width: 100%; border-collapse: collapse; flex: 1 1 auto; }}
table.terms th {{ font-size: 12.5px; font-weight: 700; text-align: left; padding: 7px 12px 5px; border-bottom: 1.3px solid #111; }}
table.terms th + th, table.terms td + td {{ border-left: 1.3px solid #111; }}
table.terms td {{ height: 31px; border-bottom: 1px solid #555; }}
table.terms tr:last-child td {{ border-bottom: none; }}
.terms-note {{ font-size: 11px; font-style: italic; color: #333; padding: 5px 12px 6px; border-top: 1.3px solid #111; }}

footer {{ display: grid; grid-template-columns: 1fr auto 1fr; align-items: baseline; font-family: RC, sans-serif; font-weight: 700; font-size: 17px; padding: 0 2px; }}
footer > div:last-child {{ text-align: right; }}
footer .mid {{ text-align: center; font-weight: 400; font-family: RC, sans-serif; font-size: 15px; line-height: 1; color: #555; letter-spacing: .5px; }}
footer .fill {{ display: inline-block; min-width: 0.85in; border-bottom: 1.3px solid #111; text-align: center; font-family: RC, sans-serif; font-weight: 700; font-size: 20px; line-height: 1; padding: 0 6px 1px; margin-left: 4px; }}
footer .fill.short {{ min-width: 0.45in; height: 18px; vertical-align: -2px; }}
"""


def lines(hw=""):
    return f'<div class="lines">{f"<div class=hw>{hw}</div>" if hw else ""}</div>'


def footer(side, week, day, ex=None):
    if ex:
        return foot("Class Notes &middot; Example", ex["pg"][0 if side == "Front" else 1], ex["when"])
    if not week:
        return foot("Class Notes", "", BLANK_WD)
    pg = pg_for("notes", week, int(day), side == "Back")
    return foot("Class Notes", pg, f"Week {week} &middot; Day {day}")


def tq(n, q="", a=""):
    """One tricky practice question: question lines, then an answer line."""
    return (f'<div class="tq"><div class="tql">Question {n}</div><div class="tqq">{lines(q)}</div>'
            f'<div class="tql">Answer</div><div class="tqa">{lines(a)}</div></div>')


def checks(opts, on=None, cls="checks", lead=""):
    items = "".join(f'<span class="{"on" if o == on else ""}">{o}</span>' for o in opts)
    return f'<div class="{cls}">{lead}{items}</div>'


def front(week, day, ex=None):
    e = ex or {}
    tag = '<span class="tag">EXAMPLE</span>' if ex else ""
    date = f'<span class="hwf" style="font-size:16px;border:none;width:auto;padding:0 6px">{e["date"]}</span>' if "date" in e else ""
    return f"""
<div class="page"><div class="frame">
  <h1>Class Notes{tag}</h1>
  <p class="blurb">Use this page in whatever way helps you learn. It doesn&rsquo;t need to be neat, and you
  don&rsquo;t have to answer every question. Skip what doesn&rsquo;t fit today. If you only do two things,
  do the <b>warm-up</b> and the <b>48-hour check</b>; those do the most for your memory. (See the example at the front of this workbook.)</p>

  <section class="box" style="height:2.05in; flex:none">
    <div class="bar"><div class="tab">BEFORE CLASS</div><div class="hint">First few minutes</div>
      <div class="date">Date:{date or '<span></span>'}</div></div>
    <div class="cols" style="grid-template-columns: 1.15fr 1fr">
      <div class="cell"><div class="q">Warm-up: Without looking, what do you remember from last class?</div>{lines(e.get("warm", ""))}</div>
      <div class="cell"><div class="q">Today&rsquo;s objective, in your own words:</div>{lines(e.get("objective", ""))}
        {checks(["Yes", "Partly", "Not yet"], e.get("got"), lead='<b style="font-weight:700">At the end, did I get there?</b>')}</div>
    </div>
  </section>

  <section class="box grow">
    <div class="bar"><div class="tab">DURING CLASS</div><div class="hint">Take notes on the right. Use the left for tricky practice questions.</div></div>
    <div class="cols" style="grid-template-columns: 2.05in 1fr">
      <div class="cell"><div class="q">Tricky practice questions<small>From your practice quizzes: ones you missed or almost missed. Write the right answer too.</small></div>
        {tq(1, e.get("q1", ""), e.get("a1", ""))}{tq(2, e.get("q2", ""), e.get("a2", ""))}</div>
      <div class="cell"><div class="q">Notes<small>Write, sketch, map, or draw. Whatever helps you remember.</small></div><div class="dotgrid">{e.get("notes", "")}</div></div>
    </div>
  </section>
  {footer("Front", week, day, ex)}
</div>{e.get("callouts_front", "")}</div>"""


def back(week, day, ex=None):
    e = ex or {}
    terms = e.get("terms", [])
    rows = "".join(f'<tr><td><span class="hwf">{t[0]}</span></td><td><span class="hwf">{t[1]}</span></td></tr>' if i < len(terms) else "<tr><td></td><td></td></tr>"
                   for i, t in enumerate(terms + [None] * (6 - len(terms))))
    rating = e.get("rating", [0, 0, 0])
    rlabels = ["make sense of today&rsquo;s ideas.", "improve my recall.", "become a better disciple, teacher, leader, or person."]
    rrows = "".join(f'<div class="lab">These notes helped me {lab}</div>' + "".join(f'<div class="o{" on" if rating[i] == k else ""}">{k}</div>' for k in range(1, 6))
                    for i, lab in enumerate(rlabels))
    h48date = f'<span class="hwf" style="font-size:16px;border:none;width:auto;padding:0 6px">{e["h48_date"]}</span>' if "h48_date" in e else ""
    return f"""
<div class="page"><div class="frame">
  <section class="box" style="flex:none">
    <div class="bar"><div class="tab">DURING CLASS</div><div class="hint">Vocab: key terms, people, and ideas to practice</div></div>
    <table class="terms">
      <colgroup><col style="width:36%"><col></colgroup>
      <tr><th>Vocab (term, person, or idea)</th><th>What it means, in my own words (or an example)</th></tr>
      {rows}
    </table>
    <div class="terms-note">To practice: cover the right column and try to explain each one out loud.</div>
  </section>

  <section class="box grow">
    <div class="bar"><div class="tab">AFTER CLASS</div><div class="hint">Last few minutes, or tonight</div></div>
    <div class="cols" style="grid-template-rows: 0.9in 1.25fr 1.45fr; grid-template-columns: 1fr">
      <div class="row" style="grid-template-columns:1fr"><div class="cell">
        <div class="q">The one idea from today I want to remember forever, in one sentence:</div>{lines(e.get("forever", ""))}</div></div>
      <div class="row" style="grid-template-columns:1fr 1fr">
        <div class="cell"><div class="q">An experience from today I want to remember:</div>{lines(e.get("experience", ""))}</div>
        <div class="cell"><div class="q">How does today connect to something earlier in the course, or to my own life?</div>{lines(e.get("connect", ""))}</div>
      </div>
      <div class="row" style="grid-template-columns:1fr 1.4fr">
        <div class="cell"><div class="q">What&rsquo;s still unclear?</div>{lines(e.get("unclear", ""))}</div>
        <div class="cell"><div class="q">Pick just one. Today helped me become a better&hellip;</div>
          {checks(["disciple", "teacher", "leader", "spouse or partner", "human"], e.get("become"), cls="checks round")}
          <div class="q" style="margin-top:5px; font-weight:400; font-style:italic; font-size:11.5px">What will I do differently?</div>{lines(e.get("differently", ""))}</div>
      </div>
    </div>
  </section>

  <section class="box" style="height:1.42in; flex:none">
    <div class="bar"><div class="tab">48-HOUR CHECK</div><div class="hint">Two days later. Cover both pages first.</div>
      <div class="date">Date:{h48date or '<span></span>'}</div></div>
    <div class="cols" style="grid-template-columns: 1fr">
      <div class="cell"><div class="q">What can I still remember? Then cover the answers on the left page and retry my tricky questions.</div>{lines(e.get("h48", ""))}</div>
    </div>
  </section>

  <section class="box" style="flex:none">
    <div class="bar"><div class="tab">SELF-CHECK</div><div class="hint">Rate yourself after the 48-hour check. Be honest; this is for you.</div></div>
    <div class="rate"><div></div><div class="sc">Not yet</div><div></div><div></div><div></div><div class="sc">Yes</div>{rrows}</div>
  </section>
  {footer("Back", week, day, ex)}
</div>{e.get("callouts_back", "")}</div>"""


SCRIPT = """
<script>
document.fonts.ready.then(() => {
  document.querySelectorAll('.lines').forEach(el => {
    const n = Math.floor((el.clientHeight - 4) / 25);
    const hw = el.querySelector('.hw');
    el.innerHTML = '<i></i>'.repeat(Math.max(n, 0));
    if (hw) el.appendChild(hw);
  });
  document.body.dataset.ready = '1';
});
</script>"""


def doc(pages, title):
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>"
            f"<style>{CSS}</style></head><body>{''.join(pages)}{SCRIPT}</body></html>")


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "classnotes_master.html").write_text(doc([front("", ""), back("", "")], "Class Notes master"))
    pages = []
    for w in WEEKS:
        for d in ("1", "2"):
            pages += [front(w, d), back(w, d)]
    (out / "classnotes.html").write_text(doc(pages, "Class Notes"))
