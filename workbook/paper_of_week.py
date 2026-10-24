"""Paper of the Week organizer, redesigned in the workbook's box/tab style. arg: outdir"""
import sys, pathlib
from classnotes import CSS, SCRIPT, WEEKS, lines, pg_for, foot, BLANK_W

EXTRA = """
.blurb.potw { font-size: 12.3px; line-height: 1.42; }
.bar .name { font-size: 12.5px; font-weight: 700; padding-right: 14px; margin-left: auto; }
.bar .name span { display: inline-block; width: 2.3in; border-bottom: 1.2px solid #111; margin-left: 4px; }
.field { display: flex; align-items: flex-end; gap: 6px; font-weight: 700; font-size: 12.5px; padding: 9px 12px 0; }
.field i { flex: 1; border-bottom: 1px solid #555; height: 1px; }
.field + .field { padding-top: 12px; }
.cell.fields { padding: 0 0 13px; }
.skel { padding: 2px 14px 11px; }
.skel .frow { display: flex; align-items: flex-end; gap: 22px; }
.skel .field { padding: 10px 0 0; }
.skel .frow.sep { margin-top: 6px; border-top: 1px dashed #bbb; }
.skel .doi { flex: 0 0 auto; display: flex; align-items: center; gap: 7px; font-weight: 700; font-size: 12.5px; padding-top: 10px; }
.skel .doi .bx { width: 13px; height: 13px; border: 1.4px solid #111; border-radius: 2px; }
.consider { font-size: 11.3px; color: #222; margin-top: 3px; line-height: 1.35; }
.consider b { font-weight: 700; }
.scale { display: flex; align-items: center; gap: 0; margin: 8px 2px 2px; font-size: 11px; font-style: italic; color: #333; }
.scale .track { flex: 1; display: flex; justify-content: space-between; align-items: center; position: relative; margin: 0 12px; }
.scale .track::before { content: ""; position: absolute; left: 6px; right: 6px; top: 50%; border-top: 1.2px solid #111; }
.scale .track span { position: relative; width: 14px; height: 14px; border: 1.3px solid #111; border-radius: 50%; background: #fff; }
.cell.tight { padding-bottom: 8px; }
"""


def page(week):
    pg = pg_for("potw", week) if week else ""
    wk = week or "&nbsp;"
    return f"""
<div class="page"><div class="frame">
  <h1>Paper of the Week</h1>
  <p class="blurb potw">This organizer helps you make sense of a hard text: a research article in education. You&rsquo;re
  encouraged to use AI (ChatGPT, Gemini, etc.) to help you understand it, and to read strategically: look at the
  headings first, skim the abstract, look up the authors. You do need to spend <b>30 minutes</b> on the reading, and
  turning this in means you did. <b>Bring it filled out to class for the jigsaw.</b></p>

  <section class="box" style="flex:none">
    <div class="bar"><div class="tab">THE PAPER</div><div class="hint">The core pieces of its APA citation, in order (see page ii)</div><div class="name">Your name:<span></span></div></div>
    <div class="skel">
      <div class="frow"><div class="field" style="flex:1">1. Author(s):<i></i></div><div class="field" style="flex:0 0 1.45in">2. Year:<i></i></div></div>
      <div class="frow"><div class="field" style="flex:1">3. Title:<i></i></div></div>
      <div class="frow"><div class="field" style="flex:1">&nbsp;<i></i></div></div>
      <div class="frow"><div class="field" style="flex:1">4. Journal:<i></i></div><div class="doi"><span class="bx"></span>I can find the DOI</div></div>
      <div class="frow sep"><div class="field" style="flex:1">Methodology (what kind of study is it?):<i></i></div></div>
    </div>
  </section>

  <section class="box" style="flex:none; height:2.42in">
    <div class="bar"><div class="tab">THE EVIDENCE</div><div class="hint">What did they find, and how much should we trust it?</div></div>
    <div class="cols" style="grid-template-rows: 1fr 0.72in; grid-template-columns: 1fr">
      <div class="row" style="grid-template-columns:1fr 1fr">
        <div class="cell"><div class="q">Statistical significance</div>
          <div class="consider">Look for: <b>p-value</b> and <b>sample size</b>. What statistical terms show up?</div>{lines()}</div>
        <div class="cell"><div class="q">Practical significance</div>
          <div class="consider">Look for: <b>effect size</b> (and its units), <b>r</b>, <b>R&sup2;</b>, <b>Cohen&rsquo;s d</b>.</div>{lines()}</div>
      </div>
      <div class="row" style="grid-template-columns:1fr"><div class="cell tight">
        <div class="q">Where does this paper sit on the hierarchy of evidence?</div>
        <div class="scale"><span>Weaker</span><div class="track"><span></span><span></span><span></span><span></span><span></span></div><span>Stronger</span>
          <span style="margin-left:18px; font-style:normal; font-weight:700; color:#111">Why?</span><i style="flex:0 0 2.3in; border-bottom:1px solid #555; height:14px; margin-left:6px"></i></div>
      </div></div>
    </div>
  </section>

  <section class="box grow">
    <div class="bar"><div class="tab">MAKING SENSE</div><div class="hint">In your own words</div></div>
    <div class="cols" style="grid-template-rows: 1.5fr 1fr 1fr; grid-template-columns: 1fr">
      <div class="row" style="grid-template-columns:1fr"><div class="cell">
        <div class="q">Synthesize: Give a very simple summary of this paper.<small>Speak to how strong the findings are and whether they matter in practice.</small></div>{lines()}</div></div>
      <div class="row" style="grid-template-columns:1fr 1fr">
        <div class="cell"><div class="q">Limitations: What are the weak spots?</div>{lines()}</div>
        <div class="cell"><div class="q">Implications for teachers:</div>{lines()}</div>
      </div>
      <div class="row" style="grid-template-columns:1fr 1fr">
        <div class="cell"><div class="q">What questions do I still have?</div>{lines()}</div>
        <div class="cell"><div class="q">Vocabulary to look up<small>Add the definitions once you look them up.</small></div>{lines()}</div>
      </div>
    </div>
  </section>
  {foot("Paper of the Week", pg, f"Week {week}" if week else BLANK_W)}
</div></div>"""


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body>"
    (out / "paper_of_week_master.html").write_text(head + page("") + SCRIPT + "</body></html>")
    (out / "paper_of_week.html").write_text(head + "".join(page(w) for w in WEEKS[1:]) + SCRIPT + "</body></html>")
