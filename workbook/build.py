"""Build the EDCOR 310 course workbook.

    cd workbook && npm install && python3 build.py

Writes out/EDCOR310_Workbook.pdf (and, with --png, one PNG per page in out/pages/).
Copy the finished PDF to workbook/EDCOR310_Workbook.pdf when it's ready to share.
"""
import subprocess, sys, shutil, pathlib
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path(__file__).parent
OUT = HERE / 'out'
GENERATORS = ['classnotes.py', 'paper_of_week.py', 'studies_toc.py', 'getting_started.py', 'synthesis.py']
DOCS = ['cover', 'toc', 'getting_started', 'classnotes', 'studies', 'paper_of_week', 'synthesis']


def run(*cmd):
    subprocess.run(cmd, check=True, cwd=HERE)


def main(png=False):
    OUT.mkdir(exist_ok=True)
    run(sys.executable, 'cover.py')
    for g in GENERATORS:
        run(sys.executable, g, str(OUT))
    for d in DOCS:
        args = ['node', 'render.js', str(OUT / f'{d}.html'), str(OUT / f'{d}.pdf')]
        if png:
            args += [str(OUT / f'png_{d}'), 'pg']
        run(*args)

    # Page order: cover, contents, Getting Started (i-iv), then by week, then the synthesis.
    # Week 1 is class notes only; every later week is Day 1, Day 2, 99 Studies, Paper of the Week.
    # Every section has an even page count, so Class Notes fronts always print on a front page.
    seq = [('cover', 0), ('toc', 0)] + [('getting_started', i) for i in range(4)]
    for w in range(13):
        seq += [('classnotes', 4 * w + k) for k in range(4)]
        if w > 0:
            seq += [('studies', w - 1), ('paper_of_week', w - 1)]
    seq += [('synthesis', 0), ('synthesis', 1)]

    readers, writer = {}, PdfWriter()
    for name, i in seq:
        writer.add_page(readers.setdefault(name, PdfReader(str(OUT / f'{name}.pdf'))).pages[i])
    writer.write(str(OUT / 'EDCOR310_Workbook.pdf'))

    if png:
        pages = OUT / 'pages'
        shutil.rmtree(pages, ignore_errors=True); pages.mkdir()
        for n, (name, i) in enumerate(seq, 1):
            shutil.copy(OUT / f'png_{name}' / f'pg-{i + 1:02d}.png', pages / f'{n}.png')
    print(f'{len(seq)} pages -> out/EDCOR310_Workbook.pdf')


if __name__ == '__main__':
    main(png='--png' in sys.argv)
