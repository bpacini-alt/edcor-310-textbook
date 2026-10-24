"""Unit Review spreads (after Weeks 4, 7, 10, 13) and the Course Synthesis that closes the book. arg: outdir

Unit Review, front: brain dump, then top 10 (alone), top 5 (group), top 3 (alone again).
Unit Review, back: unit synthesis (teacher, disciple, leader at home / church / community, commitment).
Course Synthesis: the same questions asked about the whole course, with more room.
"""
import sys, pathlib
from classnotes import CSS, SCRIPT, lines, foot, PAGE, UNIT_END

AFTER = {u: w for w, u in UNIT_END.items()}

EXTRA = """
.rv h1 { font-size: 40px; }
.rv .blurb { font-size: 13.2px; }
.nl { flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; padding-top: 2px; }
.nl > div { flex: 1 1 0; display: flex; align-items: flex-end; gap: 7px; min-height: 22px; max-height: 34px; }
.nl b { font-family: RC, sans-serif; font-weight: 700; font-size: 13px; width: 16px; text-align: right; padding-bottom: 2px; }
.nl i { flex: 1; border-bottom: 1px solid #555; height: 1px; }
.who { font-family: RC, sans-serif; font-weight: 700; font-size: 11.5px; letter-spacing: 1px; text-transform: uppercase; color: #555; margin-bottom: 1px; }
.cell.fill { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.big .q { font-family: RC, sans-serif; font-size: 19px; line-height: 1.15; }
.big .q small { font-family: Lato, sans-serif; font-size: 11.8px; margin-top: 3px; }
"""


def nlines(n):
    return '<div class="nl">' + ''.join(f'<div><b>{k}</b><i></i></div>' for k in range(1, n + 1)) + '</div>'


def cell(q, hint="", extra=""):
    small = f"<small>{hint}</small>" if hint else ""
    return f'<div class="cell fill" {extra}><div class="q">{q}{small}</div>{lines()}</div>'


def section(tab, hint, body, style='style="flex:1 1 0"'):
    return (f'<section class="box grow" {style}><div class="bar"><div class="tab">{tab}</div>'
            f'<div class="hint">{hint}</div></div>{body}</section>')


def brain_dump(u):
    return f'''<div class="page"><div class="frame rv">
  <h1>Unit {u} Review</h1>
  <p class="blurb">List everything you learned this unit, in the shortest form you can: bullet points, fragments, terms,
  names, quick sketches. Include what you learned indirectly, too: teaching methods you saw modeled, something a classmate
  said, an idea from a friend. Start without looking at your notes, then flip back and add what you missed.</p>
  {section("BRAIN DUMP", "Everything from Unit " + str(u) + ", as fast as you can", '<div class="cell fill"><div class="dotgrid" style="margin-top:4px"></div></div>', 'style="flex:1.15 1 0"')}
  {section("ELABORATE", "Narrow it down, then talk it through",
    '<div class="cols" style="grid-template-columns:1fr 1fr">'
    '<div class="cell fill"><div class="who">On your own</div><div class="q">My top ten most meaningful things from this unit</div>' + nlines(10) + '</div>'
    '<div style="display:flex; flex-direction:column; border-left:1.3px solid #111">'
    '<div class="cell fill" style="flex:5 1 0"><div class="who">With your group</div><div class="q">Our top five</div>' + nlines(5) + '</div>'
    '<div class="cell fill" style="flex:3.6 1 0; border-top:1.3px solid #111"><div class="who">On your own again</div><div class="q">The three that matter most to me</div>' + nlines(3) + '</div>'
    '</div></div>')}
  {foot(f"Unit {u} Review", PAGE[("review", u, 0)], f"After Week {AFTER[u]}")}
</div></div>'''


def unit_synthesis(u):
    scope = "this unit"
    return f'''<div class="page"><div class="frame rv">
  <h1>Unit {u} Synthesis</h1>
  <p class="blurb">Look back at your brain dump and your top three. What difference will {scope} make in your life?</p>
  {section("TEACHER &amp; DISCIPLE", "Who am I becoming?",
    '<div class="cols" style="grid-template-columns:1fr 1fr">'
    + cell("How will I be a better teacher because of " + scope + "?")
    + cell("How will I be a better disciple?", extra='style="border-left:1.3px solid #111"') + '</div>')}
  {section("LEADER", "How will I lead better in each place?",
    '<div class="cols" style="grid-template-columns:1fr 1fr 1fr">'
    + cell("In my home")
    + cell("In the Church", extra='style="border-left:1.3px solid #111"')
    + cell("In my community", extra='style="border-left:1.3px solid #111"') + '</div>')}
  {section("MY COMMITMENT", "Make it specific enough that you could tell whether you did it",
    cell("What will I do differently because of " + scope + "?"), 'style="flex:0.8 1 0"')}
  {foot(f"Unit {u} Review", PAGE[("review", u, 1)], f"After Week {AFTER[u]}")}
</div></div>'''


def course_synthesis():
    p1 = f'''<div class="page"><div class="frame rv big">
  <h1>Course Synthesis</h1>
  <p class="blurb">This is where you pull the whole course together. Before you write, flip back through your workbook:
  your four unit reviews, your &ldquo;remember forever&rdquo; sentences, and your self-checks. Write in your own words, and take your time.</p>
  {section("TEACHER", "Think of the students you&rsquo;ll teach, in a classroom, a calling, or at home",
    cell("How will I be a better teacher because of this course?"))}
  {section("DISCIPLE", "What has this course taught you about how people learn, change, and grow?",
    cell("How will I be a better disciple because of this course?"))}
  {foot("Course Synthesis", PAGE[("synth", 0)], "")}
</div></div>'''
    p2 = f'''<div class="page"><div class="frame rv big">
  {section("LEADER", "Name real people and real situations",
    '<div style="flex:1; display:flex; flex-direction:column; min-height:0">'
    + cell("How will I be a better leader in my home?")
    + cell("In the Church?", extra='style="border-top:1.3px solid #111"')
    + cell("In my community?", extra='style="border-top:1.3px solid #111"') + '</div>', 'style="flex:1.45 1 0"')}
  {section("MY COMMITMENT", "Specific enough that you could tell, a year from now, whether you did it",
    cell("What do I commit to do differently because of this course?"))}
  {foot("Course Synthesis", PAGE[("synth", 1)], "")}
</div></div>'''
    return p1 + p2


if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body>"
    (out / 'review.html').write_text(head + ''.join(brain_dump(u) + unit_synthesis(u) for u in (1, 2, 3, 4)) + SCRIPT + '</body></html>')
    (out / 'synthesis.html').write_text(head + course_synthesis() + SCRIPT + '</body></html>')
