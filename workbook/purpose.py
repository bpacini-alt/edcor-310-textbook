"""The Purpose of This Workbook: the unnumbered page right after the cover. arg: outdir

It also does a layout job. With it, the book opens to the contents page on the right, and every
two-page section after that (each Class Notes day, the example, each Unit Review, the Course
Synthesis) starts on a left-hand page, so its two pages face each other when the book is open.
Remove it and the facing pages break: replace it with another single page, never nothing.
"""
import sys, pathlib
from classnotes import CSS, SCRIPT

EXTRA = """
.pp { padding: 0.95in 0.95in 0.7in; height: 11in; display: flex; flex-direction: column; }
.pp .code { align-self: flex-start; border: 1.6px solid #006eb6; color: #006eb6; padding: 3px 12px 2px; font-family: RC, sans-serif; font-size: 22px; letter-spacing: .5px; }
.pp .code b { font-weight: 400; color: #6aa9d8; }
.pp h1 { text-align: left; font-size: 48px; line-height: 1.02; margin: 18px 0 8px; }
.pp .rule { width: 1.1in; height: 5px; background: #006eb6; margin: 6px 0 30px; }
.pp p { font-size: 16.5px; line-height: 1.62; color: #222; margin-bottom: 16px; max-width: 5.9in; }
.pp .three { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin: 22px 0 0; }
.pp .three div { border-top: 3px solid #006eb6; padding-top: 10px; font-size: 14.2px; line-height: 1.45; color: #333; }
.pp .three b { display: block; font-family: RC, sans-serif; font-weight: 700; font-size: 20px; color: #111; margin-bottom: 3px; }
.pp .verse { margin-top: auto; border-left: 4px solid #006eb6; padding: 4px 0 4px 18px; font-size: 15.5px; line-height: 1.55; color: #333; font-style: italic; max-width: 5.6in; }
.pp .verse span { display: block; font-style: normal; font-family: RC, sans-serif; font-weight: 700; font-size: 13.5px; letter-spacing: 1px; color: #006eb6; margin-top: 6px; }
"""

PAGE = '''<div class="page"><div class="pp">
  <div class="code">EDCOR <b>310</b></div>
  <h1>The Purpose of<br>This Workbook</h1>
  <div class="rule"></div>
  <p>This course is about how people learn, grow, and change. This workbook is where you practice that on yourself.</p>
  <p>Most of what we cover this semester, you could look up later. What you can&rsquo;t look up is the change in how you
  see learners, how you teach, and who you&rsquo;re becoming. That change comes from thinking hard about ideas, pulling them
  back out of memory, connecting them to your life, and acting on them. Every page in this workbook is built to help you
  do one of those things.</p>
  <p>So write messy, sketch, and leave a box blank when it doesn&rsquo;t fit the day. By the end of the semester you&rsquo;ll
  have a record of what you learned and what you decided to do about it.</p>
  <div class="three">
    <div><b>Make meaning</b>Connect new ideas to what you already know and to the people you&rsquo;ll teach.</div>
    <div><b>Remember</b>Pull ideas out of memory, then come back to them after a gap.</div>
    <div><b>Become</b>Decide what you&rsquo;ll do differently as a disciple, teacher, and leader.</div>
  </div>
  <div class="verse">&ldquo;Seek ye out of the best books words of wisdom; seek learning, even by study and also by faith.&rdquo;
  <span>DOCTRINE AND COVENANTS 88:118</span></div>
</div></div>'''

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    (out / 'purpose.html').write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body>{PAGE}{SCRIPT}</body></html>")
