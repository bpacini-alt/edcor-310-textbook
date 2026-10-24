"""Course Synthesis spread (pages 77-78) at the end of the workbook. arg: outdir"""
import sys, pathlib
from classnotes import CSS, SCRIPT, lines, foot

EXTRA = """
.syn h1 { font-size: 44px; margin-top: 4px; }
.syn .blurb { font-size: 13.4px; }
.syn .bigq { font-family: RC, sans-serif; font-weight: 700; font-size: 22px; line-height: 1.15; padding: 12px 16px 0; }
.syn .cell { padding: 4px 16px 10px; }
.syn .lookback { font-size: 12.3px; font-style: italic; color: #333; padding: 4px 16px 0; line-height: 1.4; }
"""


def box(tab, q, hint, h=None):
    style = f'style="flex:none; height:{h}in"' if h else 'style="flex:1 1 0"'
    return f'''<section class="box grow" {style}>
    <div class="bar"><div class="tab">{tab}</div></div>
    <div class="bigq">{q}</div><div class="lookback">{hint}</div>
    <div class="cell" style="flex:1; display:flex; flex-direction:column">{lines()}</div></section>'''


P1 = f'''<div class="page"><div class="frame syn">
  <h1>Course Synthesis</h1>
  <p class="blurb">You&rsquo;ve filled a whole workbook with thinking. This is where you pull it together. Before you write,
  flip back through your pages: your &ldquo;remember forever&rdquo; sentences, your &ldquo;Pick just one&rdquo; answers, your
  self-checks, and your quiz questions. Write in your own words, and take your time.</p>
  {box("LOOKING AHEAD", "Who am I becoming?", "As a disciple, a teacher, a leader, and a person. What&rsquo;s changed in how you see learners, or yourself?")}
  {box("LOOKING OUTWARD", "How will I be better because of this class?", "Think of specific people and moments: future students, your family, a calling. What will you actually do differently?")}
  {foot("Course Synthesis", 77, "")}
</div></div>'''

P2 = f'''<div class="page"><div class="frame syn">
  {box("LOOKING BACK", "What have I learned that I never want to forget?", "Choose the few ideas that still matter most to you. For each one, say why it matters and where you&rsquo;ll use it.")}
  {foot("Course Synthesis", 78, "")}
</div></div>'''

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    (out / 'synthesis.html').write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body>{P1}{P2}{SCRIPT}</body></html>")
