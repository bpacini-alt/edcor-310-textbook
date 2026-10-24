"""Front matter: How to Use (i), Reading an APA Citation (ii), Example Class Notes (iii-iv). arg: outdir"""
import sys, pathlib
from classnotes import CSS, SCRIPT, front, back, foot

FM = """
.fm h1 { text-align: left; font-size: 44px; margin: 6px 0 2px; }
.fm .lede { font-size: 15px; line-height: 1.5; color: #222; margin-bottom: 4px; }
.fm h2 { font-family: RC, sans-serif; font-weight: 700; font-size: 21px; margin: 4px 0 6px; }
.fm p, .fm li { font-size: 14.4px; line-height: 1.5; color: #222; }
.fm ul { padding-left: 20px; }
.fm li { margin-bottom: 4px; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.card { border: 1.8px solid #111; border-radius: 11px; overflow: hidden; }
.card .tab { display: inline-flex; }
.card .in { padding: 9px 13px 11px; }
.card .when { font-family: RC, sans-serif; font-weight: 700; font-size: 13px; letter-spacing: .8px; text-transform: uppercase; color: #555; margin-bottom: 4px; }
.card p { font-size: 13.8px; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.note { border-left: 4px solid #111; padding: 4px 0 4px 14px; }
.cite { font-size: 19px; line-height: 2.5; padding: 18px 22px 10px 52px; text-indent: -30px; border: 1.8px solid #111; border-radius: 11px; }
.pt { border-bottom: 2.5px solid #111; padding-bottom: 1px; }
.n { display: inline-block; text-indent: 0; width: 20px; height: 20px; border-radius: 50%; background: #111; color: #fff; font-family: RC, sans-serif; font-weight: 700; font-size: 13px; line-height: 20px; text-align: center; vertical-align: 7px; margin: 0 3px 0 1px; }
.key { display: grid; grid-template-columns: 26px 150px 1fr; row-gap: 9px; column-gap: 8px; align-items: baseline; }
.key .n { vertical-align: 0; }
.key b { font-family: RC, sans-serif; font-size: 16px; }
.key span { font-size: 14.2px; line-height: 1.45; }
.key em { color: #555; }
.week { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border: 1.8px solid #111; border-radius: 11px; overflow: hidden; }
.week > div { padding: 12px 14px 14px; position: relative; }
.week > div + div { border-left: 1.3px solid #111; }
.week .st { font-family: RC, sans-serif; font-weight: 700; font-size: 13px; letter-spacing: 1px; color: #555; text-transform: uppercase; }
.week .ti { font-family: RC, sans-serif; font-weight: 700; font-size: 19px; margin: 2px 0 5px; }
.week p { font-size: 13.4px; line-height: 1.45; }
.spot { border: 1.8px solid #111; border-radius: 11px; padding: 14px 20px 14px; }
.spot .bad { font-size: 16px; line-height: 2.1; padding-left: 30px; text-indent: -30px; margin: 4px 0 8px; }
.ans { transform: rotate(180deg); font-size: 12.5px; color: #444; line-height: 1.45; margin-top: 6px; }
"""


def page(inner, label, pg):
    return f'<div class="page"><div class="frame fm">{inner}{foot(label, pg, "")}</div></div>'


HOW = page('''
  <h1>How to Use This Workbook</h1>
  <p class="lede">This workbook is where you think on paper. It has three kinds of pages. Each one is built to help you
  understand ideas, remember them, and use them.</p>
  <div class="cards">
    <div class="card"><div class="tab">CLASS NOTES</div><div class="in"><div class="when">Every class &middot; front and back</div>
      <p>Take notes, write your own quiz questions, and connect what you learned to your life. There&rsquo;s one for each class day.</p></div></div>
    <div class="card"><div class="tab">99 STUDIES</div><div class="in"><div class="when">Weekly, starting Week 2</div>
      <p>Pick three of the week&rsquo;s nine studies. For each one, write takeaways for teaching, for life, and gospel connections.</p></div></div>
    <div class="card"><div class="tab">PAPER OF THE WEEK</div><div class="in"><div class="when">Weekly, starting Week 2</div>
      <p>Read one research article closely. Pull out its citation, judge the evidence, and bring it to class for the jigsaw.</p></div></div>
  </div>
  <div class="two">
    <div>
      <h2>You don&rsquo;t need to fill every box</h2>
      <p>The boxes on the Class Notes pages are tools, and different days call for different tools. Use the ones that help you
      make sense of the day and leave the rest blank. A page with a few thoughtful answers beats a page full of filler.
      The example on pages iii&ndash;iv shows what that can look like.</p>
      <h2 style="margin-top:12px">Bring it to every class</h2>
      <p>You&rsquo;ll use it during class, and some days we&rsquo;ll stop and work on one box together.</p>
    </div>
    <div>
      <h2>Two habits do the most for your memory</h2>
      <ul>
        <li><b>The warm-up.</b> Before class starts, write what you remember from last time without looking. Pulling ideas out of memory makes them stick better than rereading.</li>
        <li><b>The 48-hour check.</b> Two days later, cover the page and see what you can still recall. Then answer your own quiz questions. Coming back after a gap is what makes learning last.</li>
      </ul>
      <h2 style="margin-top:12px">Rate yourself at the end</h2>
      <p>Each Class Notes page ends with a short self-check: did these notes help you make sense of the ideas, remember them,
      and grow as a disciple, teacher, and person? Be honest. It&rsquo;s for you.</p>
    </div>
  </div>
  <h2 style="margin-top:2px">Your week at a glance</h2>
  <div class="week">
    <div><div class="st">Step 1</div><div class="ti">Class Day 1</div><p>Warm-up, take notes, then answer one or two After Class prompts.</p></div>
    <div><div class="st">Step 2</div><div class="ti">Class Day 2</div><p>Same thing on a new page. Before you start, do the 48-hour check for Day 1.</p></div>
    <div><div class="st">Step 3</div><div class="ti">Before next week</div><p>Do the 48-hour check for Day 2, plus that week&rsquo;s 99 Studies and Paper of the Week.</p></div>
    <div><div class="st">Step 4</div><div class="ti">Bring it back</div><p>Bring the workbook to class. We&rsquo;ll use your pages in discussion and the jigsaw.</p></div>
  </div>
  <div style="flex:1"></div>
''', "Getting Started", "i")

APA = page('''
  <h1>Reading an APA Citation</h1>
  <p class="lede">Every research article has a citation: a short line that tells anyone exactly how to find it. Here&rsquo;s one,
  broken into its parts. Each Paper of the Week page asks you to find the first four pieces.</p>
  <div class="cite"><span class="n">1</span><span class="pt">Roediger, H. L., III, &amp; Karpicke, J. D.</span>
  <span class="n">2</span><span class="pt">(2006).</span>
  <span class="n">3</span><span class="pt">Test-enhanced learning: Taking memory tests improves long-term retention.</span>
  <span class="n">4</span><span class="pt"><i>Psychological Science</i>,</span>
  <span class="n">5</span><span class="pt"><i>17</i>(3),</span>
  <span class="n">6</span><span class="pt">249&ndash;255.</span>
  <span class="n">7</span><span class="pt">https://doi.org/10.1111/j.1467-9280.2006.01693.x</span></div>
  <div class="key">
    <span class="n">1</span><b>Author(s)</b><span>Last name, then initials. Put <b style="font-size:13.4px">&amp;</b> before the last author. <em>Find it under the title on the first page.</em></span>
    <span class="n">2</span><b>Year</b><span>In parentheses, followed by a period. <em>Usually on the first page, near the journal name or in the footer.</em></span>
    <span class="n">3</span><b>Title</b><span>Capitalize only the first word, the first word after a colon, and names. Not italic. <em>Top of the first page.</em></span>
    <span class="n">4</span><b>Journal</b><span>The journal&rsquo;s name, in italics, with major words capitalized. <em>In the header or footer of the first page.</em></span>
    <span class="n">5</span><b>Volume (issue)</b><span>The volume number is italic; the issue number goes in parentheses and isn&rsquo;t italic.</span>
    <span class="n">6</span><b>Pages</b><span>First and last page of the article, with a dash between them.</span>
    <span class="n">7</span><b>DOI</b><span>A permanent link to the article. It starts with &ldquo;10.&rdquo; and is written as https://doi.org/&hellip; <em>Look at the top or bottom of the first page.</em></span>
  </div>
  <div class="note"><p><b>On your Paper of the Week page,</b> you&rsquo;ll write the author(s), year, title, and journal, then check the box
  once you&rsquo;ve found the DOI. Those pieces, in that order, are the backbone of every APA citation you&rsquo;ll ever write.</p></div>
  <h2 style="margin-top:4px">Try it: spot the mistakes</h2>
  <div class="spot">
    <p>This citation for the same article has <b>four mistakes</b>. Circle them.</p>
    <div class="bad">Roediger, Henry &amp; Karpicke, Jeffrey (2006) Test-Enhanced Learning: Taking Memory Tests Improves
    Long-Term Retention. Psychological Science, 17(3), 249&ndash;255.</div>
    <div class="ans"><b>Answers:</b> (1) Use initials, not first names: Roediger, H. L., III, &amp; Karpicke, J. D. (2) The year
    needs a period after it: (2006). (3) The article title should be in sentence case: Test-enhanced learning: Taking memory tests
    improves long-term retention. (4) The DOI is missing (and the journal name and volume should be italic).</div>
  </div>
  <div style="flex:1"></div>
''', "Getting Started", "ii")

# ---------- worked example ----------
SVG = '''<svg viewBox="0 0 260 150" width="260" height="150" style="position:absolute; right:14px; top:8px" fill="none" stroke="#1d3f73" stroke-linecap="round" stroke-linejoin="round">
 <path d="M18 8 L18 128 L250 128" stroke-width="2"/>
 <path d="M20 14 C 40 70, 70 100, 245 112" stroke-width="2.2"/>
 <path d="M20 14 C 32 48, 48 62, 62 66 L64 26 C 78 52, 96 58, 112 60 L114 30 C 132 50, 160 54, 190 56 L192 36 C 210 46, 230 48, 246 49" stroke-width="2.2" stroke-dasharray="1 0"/>
 <text x="2" y="70" font-family="Kalam" font-size="13" fill="#1d3f73" stroke="none" transform="rotate(-90 9 70)">memory</text>
 <text x="190" y="145" font-family="Kalam" font-size="13" fill="#1d3f73" stroke="none">time &#8594;</text>
 <text x="58" y="20" font-family="Kalam" font-size="12" fill="#1d3f73" stroke="none">review!</text>
 <text x="168" y="124" font-family="Kalam" font-size="12" fill="#1d3f73" stroke="none">no review</text>
</svg>'''

NOTES = SVG + '''
<div class="hwf" style="position:absolute; left:6px; top:9px; font-size:20px; text-decoration: underline;">Forgetting curve</div>
<div class="hwf" style="position:absolute; left:6px; top:36px; font-size:16px; line-height:25px">(Ebbinghaus)<br>drops fast, then<br>levels off. Each<br>review flattens it.</div>
<div class="hwf" style="position:absolute; left:6px; right:10px; top:184px; font-size:17px; line-height:25px">
<span style="border:1.6px solid #1d3f73; border-radius:6px; padding:0 6px">Retrieval practice = pulling it OUT, not putting it back in</span><br>
Roediger &amp; Karpicke (2006): study + test beat study + study<br>
after a week, even though study + study FELT better &rarr; !!<br>
&rarr; &ldquo;fluency illusion&rdquo;: familiar &ne; learned<br>
<br>
Teacher moves:<br>
&nbsp;&nbsp;&bull; brain dumps &nbsp;&nbsp;&bull; low-stakes quizzes &nbsp;&nbsp;&bull; exit tickets<br>
&nbsp;&nbsp;&bull; let kids struggle a little before giving the answer<br>
<br>
Q: does this work for little kids too? (ask next class)
</div>'''


def co(text, top, left, width):
    return f'<div class="callout" style="top:{top}in; left:{left}in; width:{width}in">{text}</div>'


EX = dict(
    pg=("iii", "iv"), when="Week 3 &middot; Day 1", date="Sept 16",
    warm="schemas = mental frameworks. new stuff\nsticks when it hooks onto what I know.\nassimilation vs. accommodation (?)",
    objective="Why pulling info out of memory beats\nrereading it",
    got="Yes",
    quiz="1. Why does rereading\nfeel like it works?\n\n2. What did R & K find\nafter one week?\n\n3. Sketch the forgetting\ncurve from memory.",
    notes=NOTES,
    terms=[("Retrieval practice", "pulling info from memory (brain dump, quiz yourself)"),
           ("Forgetting curve", "memory drops fast, then levels off; reviews flatten it"),
           ("Fluency illusion", "it feels easy because it's familiar, not because I know it")],
    forever="Struggling to remember is the part that makes it stick.",
    experience="The 2-minute brain dump at the start.\nI remembered WAY less than I thought.",
    unclear="How long should I wait before\nquizzing myself? Is 2 days the\nmagic number?",
    become="teacher",
    differently="Open my practicum lessons with a 3-question\nwarm-up instead of a review lecture.",
    h48_date="Sept 18",
    h48="Forgetting curve, R&K, fluency illusion, brain dumps. Blanked on\nthe details of the 1-week result, so I reread that part.",
    rating=[4, 4, 3],
    callouts_front=(co("Messy is fine. A &ldquo;(?)&rdquo; means &ldquo;check this later.&rdquo;", 2.8, 4.75, 2.45)
                    + co("Sketches count. Draw it if that helps you think.", 9.25, 4.6, 2.6)
                    + co("These become your 48-hour check.", 8.55, 0.62, 1.7)),
    callouts_back=(co("Left blank on purpose. Not every box fits every day.", 5.0, 5.55, 2.25)
                   + co("Three terms is plenty.", 2.25, 5.9, 1.6)
                   + co("Honest beats perfect.", 9.7, 3.95, 1.45)),
)

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{FM}</style></head><body>"
            + HOW + APA + front(None, None, EX) + back(None, None, EX) + SCRIPT + "</body></html>")
    (out / 'getting_started.html').write_text(html)
