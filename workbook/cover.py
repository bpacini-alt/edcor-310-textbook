"""Workbook cover: recolored four-stages banner, title, and course footer."""
import pathlib
H = pathlib.Path(__file__).parent
F = H / 'node_modules/@fontsource/roboto-condensed/files'
L = H / 'node_modules/@fontsource/lato/files'

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: RC; font-weight: 300; src: url('{F}/roboto-condensed-latin-300-normal.woff2'); }}
@font-face {{ font-family: RC; font-weight: 400; src: url('{F}/roboto-condensed-latin-400-normal.woff2'); }}
@font-face {{ font-family: RC; font-weight: 700; src: url('{F}/roboto-condensed-latin-700-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 400; src: url('{L}/lato-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 700; src: url('{L}/lato-latin-700-normal.woff2'); }}
@page {{ size: 8.5in 11in; margin: 0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #fff; }}
.page {{ width: 8.5in; height: 11in; display: flex; flex-direction: column; font-family: RC, sans-serif; color: #1a1a1a; }}
.hero {{ position: relative; width: 8.5in; height: 7.0in; background: url('{H}/assets/banner-blue.png') right center / cover no-repeat; color: #fff; }}
.hero .t {{ position: absolute; left: 0.5in; top: 0.36in; }}
.code {{ display: inline-block; border: 2px solid rgba(255,255,255,.85); background: rgba(0,40,80,.35); padding: 4px 16px 3px; font-family: RC, sans-serif; font-weight: 400; font-size: 34px; letter-spacing: 1px; margin-bottom: 20px; }}
.code b {{ font-weight: 400; color: #8fc8f0; }}
.hero h1 {{ font-weight: 700; font-size: 51px; line-height: 1.02; letter-spacing: 0.3px; text-shadow: 0 2px 14px rgba(0,30,60,.35); }}
.hero h2 {{ font-weight: 300; font-size: 25px; line-height: 1.25; margin-top: 14px; }}
.hero .wb {{ display: inline-block; margin-top: 18px; font-weight: 700; font-size: 16px; letter-spacing: 3px; border: 2px solid rgba(255,255,255,.9); padding: 6px 13px 5px; }}
.low {{ flex: 1; display: flex; flex-direction: column; padding: 0.38in 0.5in 0; }}
.low h3 {{ font-weight: 700; font-size: 14px; letter-spacing: 2.5px; color: #006eb6; margin-bottom: 12px; }}
.items {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.28in; }}
.items div {{ font-family: Lato, sans-serif; font-size: 13.5px; line-height: 1.35; color: #444; border-top: 3px solid #006eb6; padding-top: 9px; }}
.items b {{ display: block; font-family: RC, sans-serif; font-weight: 700; font-size: 19px; color: #1a1a1a; margin-bottom: 3px; }}
.name {{ margin-top: auto; display: flex; align-items: flex-end; gap: 10px; font-weight: 700; font-size: 17px; letter-spacing: 1.5px; color: #006eb6; padding-bottom: 0.22in; }}
.name span {{ flex: 1; border-bottom: 2px solid #006eb6; height: 26px; }}
.foot {{ border-top: 1px solid #c9d6e2; margin: 0 0.5in; padding: 0.18in 0 0.28in; display: flex; align-items: center; }}
.foot .core {{ font-size: 24px; color: #006eb6; padding-right: 20px; }}
.foot .div {{ width: 1.5px; align-self: stretch; background: #9fb6cb; margin-right: 20px; }}
.foot .course {{ font-size: 14.5px; color: #444; line-height: 1.25; }}
.foot .num {{ margin-left: auto; font-weight: 700; font-size: 26px; color: #006eb6; }}
</style></head><body><div class="page">
  <div class="hero"><div class="t">
    <div class="code">EDCOR <b>310</b></div>
    <h1>THE SCIENCE<br>OF LEARNING:</h1>
    <h2>An Evidence-Based Approach<br>to Educational Psychology</h2>
    <div class="wb">COURSE WORKBOOK</div>
  </div></div>
  <div class="low">
    <h3>WHAT&rsquo;S INSIDE</h3>
    <div class="items">
      <div><b>99 Studies</b>Three studies a week, with takeaways for teaching and life.</div>
      <div><b>Paper of the Week</b>One research article, read closely and made sense of.</div>
      <div><b>Class Notes</b>A page for every class day, built to help you remember.</div>
    </div>
    <div class="name">NAME:<span></span></div>
  </div>
  <div class="foot">
    <div class="core">Education Core</div><div class="div"></div>
    <div class="course">Educational Psychology<br>and Human Development</div>
    <div class="num">EDCOR 310</div>
  </div>
</div>
<script>document.fonts.ready.then(()=>document.body.dataset.ready='1')</script></body></html>"""
(H / 'out/cover.html').write_text(html)
