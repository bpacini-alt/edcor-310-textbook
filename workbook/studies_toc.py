"""99 Studies pages and the blue Table of Contents. arg: outdir"""
import sys, pathlib
from classnotes import CSS, SCRIPT, WEEKS, lines, pg_for, foot, BLANK_W

H = pathlib.Path(__file__).parent
EXTRA = """
.blurb.st { padding: 0 0.2in; }
.colhead { font-weight: 700; font-size: 12.5px; text-align: center; line-height: 1.3; min-height: 33px; }
.bar .title { flex: 1; display: flex; align-items: flex-end; gap: 6px; font-weight: 700; font-size: 12.5px; padding: 0 16px 0 18px; }
.bar .title i { flex: 1; border-bottom: 1px solid #555; height: 1px; margin-bottom: 4px; }
.lhead { display: flex; align-items: center; gap: 18px; padding: 4px 2px 2px; }
.lhead .code { border: 1.6px solid #111; padding: 3px 12px 2px; font-family: RC, sans-serif; font-size: 26px; letter-spacing: .5px; }
.lhead .code b { font-weight: 400; color: #8a8a8a; }
.lhead .sep { width: 1.5px; height: 44px; background: #111; }
.lhead .nm { font-family: RC, sans-serif; font-weight: 700; font-size: 21px; line-height: 1.1; }
.lhead .nm span { display: block; font-weight: 400; font-size: 15px; color: #444; letter-spacing: 1.5px; }
.ruled { flex: 1; display: flex; flex-direction: column; }
"""


def head(title):
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}{EXTRA}</style></head><body>"


def footer(label, pg, week=None):
    wk = '' if week is None else f'Week: <span class="fill">{week}</span>'
    return f'<footer><div>{label}</div><div class="mid">{pg}</div><div>{wk}</div></footer>'


def studies(week):
    pg = pg_for('99', week) if week else ''
    boxes = ''
    for n in (1, 2, 3):
        cols = ''.join(f'<div class="cell"><div class="colhead">{h}</div>{lines()}</div>' for h in (
            'Key take-aways for teachers:', 'Implications for life,<br>if applicable?', 'Gospel connections,<br>if applicable?'))
        boxes += f'''<section class="box grow" style="flex:1 1 0"><div class="bar"><div class="tab">STUDY {n}</div>
          <div class="title">Title:<i></i></div></div>
          <div class="cols" style="grid-template-columns:1fr 1fr 1fr">{cols}</div></section>'''
    return f'''<div class="page"><div class="frame">
  <h1>99 Studies Frayer Model</h1>
  <p class="blurb st">Each week, you will have 9 studies to choose from. Select three of those studies. Then fill out
  the Frayer model below. Study 1 is the first study you chose to read about, Study 2 the second, and so on.
  You are encouraged to process <b>more</b> than this, but this much processing is required for class.
  <b>Bring this with you to class, too!</b></p>
  {boxes}
  {foot("99 Studies", pg, f"Week {week}" if week else BLANK_W)}
</div></div>'''


TOC_CSS = """
.toc { width: 8.5in; height: 11in; background: #006eb6; color: #fff; padding: 0.55in 0.62in 0; font-family: Lato, sans-serif; }
.toc .code { display: inline-block; border: 2px solid rgba(255,255,255,.85); padding: 3px 14px 2px; font-family: RC, sans-serif; font-size: 24px; letter-spacing: .5px; }
.toc .code b { font-weight: 400; color: #8fc8f0; }
.toc h1 { text-align: left; color: #fff; font-size: 56px; margin: 12px 0 26px; }
.toc table { width: 100%; border-collapse: collapse; }
.toc th { font-family: RC, sans-serif; font-weight: 700; font-size: 15px; letter-spacing: 1.2px; text-transform: uppercase; text-align: center; padding: 0 4px 10px; vertical-align: bottom; line-height: 1.2; border-bottom: 1.5px solid rgba(255,255,255,.85); }
.toc th.wk, .toc td.wk { text-align: left; }
.toc th.none { border: none; }
.toc th.group { font-size: 13px; letter-spacing: 2px; padding-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,.6); }
.toc td { text-align: center; font-size: 17px; padding: 8px 4px 7px; border-bottom: 1px solid rgba(255,255,255,.3); font-variant-numeric: tabular-nums; }
.toc td.wk { font-family: RC, sans-serif; font-weight: 700; font-size: 19px; }
.toc .gs { display: flex; flex-wrap: nowrap; gap: 6px 16px; align-items: baseline; font-size: 14px; white-space: nowrap; margin: -10px 0 22px; padding: 10px 0 12px; border-top: 1px solid rgba(255,255,255,.5); border-bottom: 1px solid rgba(255,255,255,.5); }
.toc .gs b { font-family: RC, sans-serif; font-size: 13.5px; letter-spacing: 1.2px; text-transform: uppercase; margin-right: 6px; }
.toc .gs i { font-style: normal; opacity: .8; margin-left: 4px; }
.toc .note { font-size: 13.5px; margin-top: 12px; opacity: .9; }
.toc .lined { display: flex; align-items: baseline; gap: 10px; margin-top: 26px; font-size: 19px; }
.toc .lined b { font-family: RC, sans-serif; font-weight: 700; }
.toc .lined .dots { flex: 1; border-bottom: 2px dotted rgba(255,255,255,.75); transform: translateY(-5px); }
"""


def toc():
    rows = ''.join(f'<tr><td class="wk">Week {w}</td><td>{pg_for("notes", w, 1)}</td><td>{pg_for("notes", w, 2)}</td><td>{pg_for("99", w) if w > 1 else "&ndash;"}</td><td>{pg_for("potw", w) if w > 1 else "&ndash;"}</td></tr>' for w in WEEKS)
    return f'''<div class="page toc"><div class="code">EDCOR <b>310</b></div><h1>Table of Contents</h1><div class="gs"><b>Getting Started</b><span>How to Use This Workbook <i>i</i></span><span>Reading an APA Citation <i>ii</i></span><span>Example Class Notes <i>iii&ndash;iv</i></span></div>
<table><tr><th class="none"></th><th colspan="2" class="group">Class Notes</th><th class="none"></th><th class="none"></th></tr>
<tr><th class="wk">Week</th><th>Day 1</th><th>Day 2</th><th>99 Studies</th><th>Paper of<br>the Week</th></tr>{rows}</table>
<p class="note">Numbers are page numbers. Class notes are front and back.</p>
<div class="lined"><b>Course Synthesis</b><span class="dots"></span><span>Pg. 77</span></div></div>'''


if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    (out / 'studies.html').write_text(head('99 Studies') + ''.join(studies(w) for w in WEEKS[1:]) + SCRIPT + '</body></html>')
    (out / 'studies_master.html').write_text(head('99 Studies') + studies('') + SCRIPT + '</body></html>')
    t = head('Contents').replace('</style>', TOC_CSS + '</style>')
    (out / 'toc.html').write_text(t + toc() + SCRIPT + '</body></html>')
