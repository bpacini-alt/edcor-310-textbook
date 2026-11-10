"""Getting Started, pages i-viii: How to Use (i), Your Week (ii), Reading an APA Citation (iii),
Research Terms in Plain Words (iv), and worked examples: Class Notes (v-vi), 99 Studies (vii),
Paper of the Week (viii). Keep the page count even so the spreads after it still face. arg: outdir"""
import sys, pathlib
from classnotes import CSS, SCRIPT, front, back, foot, VIDEO
import studies_toc, paper_of_week

FM = """
.fm h1 { text-align: left; font-size: 44px; margin: 6px 0 2px; }
.fm .lede { font-size: 15px; line-height: 1.5; color: #222; margin-bottom: 4px; }
.fm h2 { font-family: RC, sans-serif; font-weight: 700; font-size: 21px; margin: 4px 0 6px; }
.fm p, .fm li { font-size: 14.4px; line-height: 1.5; color: #222; }
.fm ul { padding-left: 20px; }
.fm li { margin-bottom: 4px; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 11px; }
.card { border: 1.8px solid #111; border-radius: 11px; overflow: hidden; }
.card .tab { display: inline-flex; font-size: 13.5px; letter-spacing: .6px; padding: 5px 12px 5px 11px; }
.card .in { padding: 9px 13px 11px; }
.card .when { font-family: RC, sans-serif; font-weight: 700; font-size: 13px; letter-spacing: .8px; text-transform: uppercase; color: #555; margin-bottom: 4px; }
.card p { font-size: 13px; }
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
.wk { display: grid; grid-template-columns: 1.05fr 1.6fr 0.75fr; border: 1.8px solid #111; border-radius: 11px; overflow: hidden; }
.wk > div { padding: 10px 14px; border-top: 1.3px solid #111; font-size: 14.2px; line-height: 1.45; }
.wk > div:nth-child(-n+3) { border-top: none; background: #111; color: #fff; font-family: RC, sans-serif; font-weight: 700; font-size: 13.5px; letter-spacing: 1px; padding: 7px 14px; }
.wk > div:nth-child(3n+2) { border-left: 1.3px solid #111; border-right: 1.3px solid #111; }
.wk .w { font-family: RC, sans-serif; font-weight: 700; font-size: 17px; line-height: 1.2; }
.wk .w small { display: block; font-family: Lato, sans-serif; font-weight: 400; font-size: 12.5px; color: #555; margin-top: 2px; }
.wk ul { padding-left: 18px; margin: 3px 0 0; }
.wk li { font-size: 14px; margin: 0; }
.wk .t { font-family: RC, sans-serif; font-weight: 700; font-size: 16px; }
.terms2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 26px; }
.terms2 > div { break-inside: avoid; border-top: 1.3px solid #bbb; padding-top: 7px; }
.terms2 b { display: block; font-family: RC, sans-serif; font-weight: 700; font-size: 16.5px; color: #111; }
.terms2 p { font-size: 13.4px; line-height: 1.45; }
.terms2 em { color: #555; }
.ladder { display: flex; align-items: stretch; gap: 0; border: 1.8px solid #111; border-radius: 11px; overflow: hidden; font-size: 12.8px; line-height: 1.3; }
.ladder > div { flex: 1; padding: 8px 9px; text-align: center; }
.ladder > div + div { border-left: 1.3px solid #111; }
.ladder b { display: block; font-family: RC, sans-serif; font-size: 14px; }
.ans { transform: rotate(180deg); font-size: 12.5px; color: #444; line-height: 1.45; margin-top: 6px; }
"""


def page(inner, label, pg):
    return f'<div class="page"><div class="frame fm">{inner}{foot(label, pg, "")}</div></div>'


HOW = page('''
  <h1>How to Use This Workbook</h1>
  <p class="lede">This workbook is where you think on paper. It has four kinds of pages. Each one is built to help you
  understand ideas, remember them, and use them.</p>
  <div class="cards">
    <div class="card"><div class="tab">CLASS NOTES</div><div class="in"><div class="when">Every class day</div>
      <p>Take notes, record tricky practice questions, build your vocab, and connect what you learned to your life.</p></div></div>
    <div class="card"><div class="tab">99 STUDIES</div><div class="in"><div class="when">Weekly, from Week 2</div>
      <p>Pick three of the week&rsquo;s nine studies. Write takeaways for teaching, for life, and gospel connections.</p></div></div>
    <div class="card"><div class="tab">PAPER OF THE WEEK</div><div class="in"><div class="when">Weekly, from Week 2</div>
      <p>Read one research article closely. Pull out its citation, judge the evidence, and bring it to the jigsaw.</p></div></div>
    <div class="card"><div class="tab">UNIT REVIEW</div><div class="in"><div class="when">End of each unit</div>
      <p>Brain-dump everything from the unit, pick your top ten, five, and three, then reflect on who you&rsquo;re becoming.</p></div></div>
  </div>
  <div class="two">
    <div>
      <h2>Take notes your way</h2>
      <p>You&rsquo;re welcome to take notes however works best for you: on the Class Notes pages, in a notebook, or on a laptop.
      The workbook is here to help. Use the boxes that help you make sense of the day and leave the rest blank. A page with
      a few thoughtful answers beats a page full of filler. The examples on pages v&ndash;viii show what that can look like.</p>
      <h2 style="margin-top:12px">Bring it to every class</h2>
      <p>You&rsquo;ll use it during class, and some days we&rsquo;ll stop and work on one box together.</p>
    </div>
    <div>
      <h2>Two habits do the most for your memory</h2>
      <ul>
        <li><b>The warm-up.</b> At the start of class, write what you remember from last time without looking. Pulling ideas out of memory makes them stick better than rereading.</li>
        <li><b>The 48-hour check.</b> Two days later, cover both pages and see what you can still recall. Then cover the answers and retry your tricky practice questions. Coming back after a gap is what makes learning last.</li>
      </ul>
      <h2 style="margin-top:12px">Rate yourself at the end</h2>
      <p>Each Class Notes page ends with a short self-check: did these notes help you make sense of the ideas, remember them,
      and grow as a disciple, teacher, and person? Be honest. It&rsquo;s for you.</p>
    </div>
  </div>
  <div class="note" style="margin-top:6px"><p><b>What&rsquo;s due when?</b> Page ii lays out a normal week, with about how long
  each piece takes. Each Class Notes page also starts with a short checklist of what to finish before that class.</p></div>
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
''', "Getting Started", "iii")

WEEK = page(f'''
  <h1>Your Week</h1>
  <p class="lede">Every week has two class days and two readings. Reading <b>X.1</b> is due right before the first class of
  the week, and <b>X.2</b> right before the second. Plan on about two hours of preparation a week.</p>
  <div class="wk">
    <div>WHEN</div><div>WHAT TO DO</div><div>ABOUT HOW LONG</div>
    <div><div class="w">Before Class 1<small>Reading X.1</small></div></div>
    <div>Read that week&rsquo;s <b>Joy of Learning</b> reading.</div><div class="t">1 hour</div>
    <div><div class="w">Before Class 2<small>Reading X.2, research seminar</small></div></div>
    <div><ul><li>Watch the {VIDEO}.</li><li>Fill out your <b>99 Studies</b> page (three studies).</li>
      <li>Read and fill out the <b>Paper of the Week</b>. Bring both pages to class for the jigsaw.</li></ul></div>
    <div><div class="t">1 hour</div>15 min<br>15 min<br>30 min</div>
    <div><div class="w">Two days after each class</div></div>
    <div>Do the <b>48-hour check</b> on that day&rsquo;s Class Notes, and retry your tricky practice questions.</div><div class="t">A few minutes</div>
    <div><div class="w">End of each unit<small>After Weeks 4, 7, 10, and 13</small></div></div>
    <div>Do the <b>Unit Review</b>: brain dump, top ten, five, and three, and the unit synthesis.</div><div class="t">In class</div>
  </div>
  <h2 style="margin-top:6px">Good to know</h2>
  <ul>
    <li><b>Week 1</b> has reading 1.1 but no research seminar. 99 Studies and Paper of the Week start in Week 2.</li>
    <li>Each week&rsquo;s 99 Studies and Paper of the Week pages come right after that week&rsquo;s Class Notes.</li>
    <li>Each Class Notes page starts with a <b>Before this class</b> checklist, so you can check things off as you go.</li>
    <li>The times are estimates. Some weeks will go faster and some slower. If a week regularly takes you much longer, tell us.</li>
  </ul>
  <div style="flex:1"></div>
''', "Getting Started", "ii")

TERMS = page('''
  <h1>Research Terms in Plain Words</h1>
  <p class="lede">You&rsquo;ll see these in almost every study. You don&rsquo;t need to calculate any of them. You just need to know
  what they&rsquo;re telling you.</p>
  <div class="terms2">
    <div><b>Sample size (n or N)</b><p>How many people were studied. Bigger samples give steadier, more trustworthy results.</p></div>
    <div><b>Mean (M) and standard deviation (SD)</b><p>The mean is the average. The SD is how spread out the scores are around it.</p></div>
    <div><b>p-value</b><p>If there were really no effect, how surprising would results like these be? A small p (usually below .05) means
      &ldquo;probably not just luck.&rdquo; <em>It doesn&rsquo;t tell you how big or important the effect is.</em></p></div>
    <div><b>Statistically significant</b><p>The result is unlikely to be chance alone, usually meaning p &lt; .05. Significant doesn&rsquo;t
      mean large or important.</p></div>
    <div><b>Effect size</b><p>How big the difference or relationship is. This is the number that tells you whether a finding matters
      in a real classroom.</p></div>
    <div><b>Cohen&rsquo;s d</b><p>The difference between two groups, in standard deviations. A rough guide: 0.2 is small, 0.5 medium,
      0.8 large. <em>In schools, even small effects can be worth it if they&rsquo;re cheap and reach many students.</em></p></div>
    <div><b>Correlation (r)</b><p>How closely two things move together, from &minus;1 to +1. Zero means no relationship.
      <em>A correlation alone can&rsquo;t show that one thing causes the other.</em></p></div>
    <div><b>R&sup2; (and &eta;&sup2;)</b><p>The share of the differences in one thing that another thing accounts for, from 0 to 1.
      An r of .30 gives an R&sup2; of .09, or 9%.</p></div>
    <div><b>Experiment / randomized controlled trial</b><p>Researchers randomly put people into groups and change one thing. The best
      design for showing cause and effect.</p></div>
    <div><b>Control group</b><p>The comparison group that doesn&rsquo;t get the new method. Without one, you can&rsquo;t tell what the method did.</p></div>
    <div><b>Correlational study</b><p>Researchers measure things as they already are and look for patterns. Useful, but it can&rsquo;t
      prove cause.</p></div>
    <div><b>Meta-analysis</b><p>A study that combines the results of many studies on the same question, giving an overall effect size.</p></div>
    <div><b>Replication</b><p>Repeating a study to see if the result holds up. A finding that replicates is much more trustworthy.</p></div>
    <div><b>Peer review</b><p>Other experts checked the study before the journal published it. A good sign, but no guarantee.</p></div>
  </div>
  <h2 style="margin-top:4px">The hierarchy of evidence</h2>
  <div class="ladder">
    <div><b>Weaker</b>Opinions and stories</div><div>Case studies</div><div>Correlational studies</div>
    <div>Experiments (RCTs)</div><div><b>Stronger</b>Meta-analyses of experiments</div>
  </div>
  <div style="flex:1"></div>
''', "Getting Started", "iv")

# ---------- worked example ----------
SVG = '''<svg viewBox="0 0 260 150" width="260" height="150" style="position:absolute; right:14px; top:8px" fill="none" stroke="#1d3f73" stroke-linecap="round" stroke-linejoin="round">
 <rect x="0" y="0" width="260" height="150" fill="#fff" stroke="none"/>
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
    pg=("v", "vi"), week=3, day=1, done=("r", "c"), when="Week 3 &middot; Day 1", date="Sept 16",
    warm="schemas = mental frameworks. new stuff\nsticks when it hooks onto what I know.\nassimilation vs. accommodation (?)",
    objective="Why pulling info out of memory beats\nrereading it",
    got="Yes",
    q1="Reread 3x vs. quiz\nmyself once: who\nremembers more\nafter a week?",
    a1="Quizzing! Rereading\nfeels better but fades.",
    q2="Best example of\nretrieval practice?\na) highlight b) reread\nc) brain dump",
    a2="c) brain dump",
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
    h48="Forgetting curve, R&K, fluency illusion, brain dumps. Got Q2. Missed Q1\nagain (said rereading!), so I reread that part of Ch. 22.",
    rating=[4, 4, 3],
    callouts_front=(co("Messy is fine. A &ldquo;(?)&rdquo; means &ldquo;check this later.&rdquo;", 3.13, 4.75, 2.45)
                    + co("Sketches count. Draw it if that helps you think.", 9.95, 4.6, 2.6)
                    + co("Cover the answers and retry these at your 48-hour check.", 9.9, 0.62, 1.75)),
    callouts_back=(co("Left blank on purpose. Not every box fits every day.", 5.0, 5.55, 2.25)
                   + co("Three vocab terms is plenty.", 2.25, 5.7, 1.8)
                   + co("Honest beats perfect.", 9.7, 3.95, 1.45)),
)

EX99 = dict(
    pg="vii", when="Week 3",
    studies=[
        ("The one about spacing your learning",
         "Spread practice out.\nRevisit old topics in\nwarm-ups instead of\none big review day.",
         "Study a little each\nday before the exam,\nnot all of it the\nnight before.",
         "\"Line upon line\"\n(2 Ne. 28:30). We\nlearn in small pieces\nover time."),
        ("The one about how much we forget",
         "Kids forget a lot of\na lesson fast unless\nwe come back to it.\nPlan the review in.",
         "Forgetting my Week 1\nnotes is normal. It\nmeans review, not\nthat I'm bad at this.",
         "\"Remember, remember\"\n(Hel. 5:12).\nRemembering takes\neffort on purpose."),
        ("The one about pre-questions",
         "Ask a question before\nteaching the answer.\nEven wrong guesses\nhelp kids learn it.",
         "Before I read, look\nat the questions and\nguess first.",
         ""),
    ],
    callouts=(co("Short is fine. A few words per box is plenty.", 3.5, 3.05, 2.1)
              + co("Left blank on purpose. Not every study has one.", 8.7, 5.65, 2.15)),
)

EXPOTW = dict(
    pg="viii", when="Week 3", name="Alex R.",
    author="Roediger, H. L., III, & Karpicke, J. D.", year="2006",
    title1="Test-enhanced learning: Taking memory tests improves",
    title2="long-term retention",
    journal="Psychological Science", doi=True,
    method="Two lab experiments with college students",
    stat="Exp. 1: 120 students (Exp. 2: 180).\nThey report F and t tests; the\nmain results were significant.",
    prac="After 1 week: 56% recalled after\na practice test vs. 42% after\nrereading. d = 0.83, a large effect.",
    level=4, why="One lab study, short readings",
    synth="A practice test helped college students remember a reading a week\nlater much better than rereading it (56% vs. 42%, d = 0.83).\nRereading only won when the final test came 5 minutes later.\nA strong, useful finding, though it was tested in a lab.",
    lim="Lab, not a real class. College\nstudents, short science passages,\nand only recall was tested.",
    impl="Quick no-stakes quizzes and\nbrain dumps beat a review\nlecture or rereading.",
    ques="Why did the students who only\nreread think they'd remember\nmore? Does it work for kids?",
    vocab="idea units: the small pieces\nof the passage they scored",
    callouts=(co("The numbers come straight from the results section.", 3.57, 5.55, 2.2)
              + co("There's no single right dot. Explain your choice.", 6.4, 5.85, 2.1)),
)

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{FM}{studies_toc.EXTRA}{paper_of_week.EXTRA}</style></head><body>"
            + HOW + WEEK + APA + TERMS + front(None, None, EX) + back(None, None, EX)
            + studies_toc.studies(None, EX99) + paper_of_week.page(None, EXPOTW) + SCRIPT + "</body></html>")
    (out / 'getting_started.html').write_text(html)
