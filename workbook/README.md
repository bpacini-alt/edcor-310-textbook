# EDCOR 310 course workbook

The printed workbook students use alongside *The Science of Learning*: Class Notes for every class day, weekly 99 Studies and Paper of the Week pages, a Getting Started section, and a closing Course Synthesis. The current version is `EDCOR310_Workbook.pdf` (84 pages, letter size).

## Rebuilding it

```
cd workbook
npm install
python3 build.py          # add --png for one PNG per page
```

The new PDF lands in `out/`. When it's ready to share, copy it over `EDCOR310_Workbook.pdf` in the same pull request as the change.

| File | What it builds |
|---|---|
| `classnotes.py` | Shared page styles, plus the Class Notes front and back (also used for the filled-in example) |
| `paper_of_week.py` | Paper of the Week, with the APA citation skeleton |
| `studies_toc.py` | 99 Studies pages and the Table of Contents |
| `getting_started.py` | How to Use This Workbook, Reading an APA Citation, and the example Class Notes (pages i–iv) |
| `synthesis.py` | Course Synthesis (pages 77–78) |
| `cover.py` | The cover |
| `banner.py` | Recolors the Canvas banner (`assets/banner-original.png`) into `assets/banner-blue.png`. Only rerun it if the banner changes. |
| `build.py` | Renders everything and puts the pages in order |

## Decisions to keep

- **Look:** matches the textbook. Blue (#006EB6) and white on the cover and contents page, black and white inside so it prints cheaply. Headings in Roboto Condensed, text in Lato (Canvas's own font). The EDCOR 310 box appears on the cover, contents, and notes pages.
- **Title:** *The Science of Learning* with "Course Workbook," and the course title (Educational Psychology and Human Development) in the footer.
- **Order:** Week 1 is Class Notes only. Weeks 2–13 run Day 1, Day 2, 99 Studies, Paper of the Week. Every section has an even page count so each Class Notes front and back share a sheet when printed double-sided from the cover. Keep it that way when adding pages.
- **Class Notes:** the boxes are tools, not a form to complete. The page says so, the example leaves boxes blank on purpose, and the self-check asks whether the notes helped students make meaning, remember, and grow, not whether every box is full.
- **Citations:** students fill in author, year, title, and journal and check that they found the DOI, instead of handwriting a full APA citation.
