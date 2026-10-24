# EDCOR 310 course workbook

The printed workbook students use alongside *The Science of Learning*: Class Notes for every class day, weekly 99 Studies and Paper of the Week pages, a Unit Review after each unit, a Getting Started section, and a closing Course Synthesis. The current version is `EDCOR310_Workbook.pdf` (93 pages, letter size).

## Rebuilding it

```
cd workbook
npm install
python3 build.py          # add --png for one PNG per page
```

The new PDF lands in `out/`. When it's ready to share, copy it over `EDCOR310_Workbook.pdf` in the same pull request as the change.

| File | What it builds |
|---|---|
| `classnotes.py` | Shared page styles, the page order and numbering (`layout()`), and the Class Notes front and back (also used for the filled-in example) |
| `paper_of_week.py` | Paper of the Week, with the APA citation skeleton |
| `studies_toc.py` | 99 Studies pages and the Table of Contents |
| `getting_started.py` | How to Use This Workbook, Reading an APA Citation, and the example Class Notes (pages i–iv) |
| `review.py` | Unit Reviews (brain dump + unit synthesis, after Weeks 4, 7, 10, and 13) and the Course Synthesis |
| `cover.py` | The cover |
| `purpose.py` | The Purpose of This Workbook (the page after the cover; it also keeps the spreads facing) |
| `banner.py` | Recolors the Canvas banner (`assets/banner-original.png`) into `assets/banner-blue.png`. Only rerun it if the banner changes. |
| `build.py` | Renders everything and puts the pages in order |

## Decisions to keep

- **Look:** matches the textbook. Blue (#006EB6) and white on the cover and contents page, black and white inside so it prints cheaply. Headings in Roboto Condensed, text in Lato (Canvas's own font). The EDCOR 310 box appears on the cover, contents, and notes pages.
- **Title:** *The Science of Learning* with "Course Workbook," and the course title (Educational Psychology and Human Development) in the footer.
- **Order:** Week 1 is Class Notes only. Weeks 2–13 run Day 1, Day 2, 99 Studies, Paper of the Week. A two-page Unit Review follows Weeks 4, 7, 10, and 13, and the Course Synthesis closes the book. `layout()` in `classnotes.py` is the one place the order lives; page numbers and the contents page come from it. Every section has an even page count, and the unnumbered purpose page after the cover shifts everything by one, so each Class Notes day (and the example, each Unit Review, and the Course Synthesis) opens as a facing spread: A on the left, B on the right. Keep sections even-length, and if the purpose page ever goes, replace it with another single page.
- **Practice and vocab:** the front's left column holds two tricky practice questions with their answers (students get unlimited practice quizzes), retried at the 48-hour check. Vocab goes in the table on the back.
- **Unit Reviews:** the brain dump is fast and fragmentary and includes things learned indirectly (teaching methods, a classmate, a friend). Then top ten alone, top five with a group, top three alone again. The back asks how the unit makes students better teachers, disciples, and leaders at home, at church, and in the community, and what they'll do differently. The Course Synthesis asks the same questions about the whole course.
- **Class Notes:** the boxes are tools, not a form to complete. The page says so, the example leaves boxes blank on purpose, and the self-check asks whether the notes helped students make meaning, remember, and grow, not whether every box is full.
- **Citations:** students fill in author, year, title, and journal and check that they found the DOI, instead of handwriting a full APA citation.
