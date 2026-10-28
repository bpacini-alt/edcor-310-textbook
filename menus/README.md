# Reading menus

The Joy reading menus are the weekly enrichment readings for each course: **The Joy of Learning** (EDCOR 310) and **The Joy of Econ** (Econ 150). Each menu is one web page, built from a data file.

| File | What it is | Shared? |
|---|---|---|
| `build_menu.py` | Builds a menu page from its data file | Identical in both repositories |
| `joy-menu.css`, `joy-menu.js` | The page's look and its buttons, inlined into the page by the builder | Identical in both repositories |
| `joy-of-learning.json` (EDCOR 310) or `joy-of-econ.json` (Econ 150) | This course's menu: settings, instructions, units, weeks, and readings | This repository only |

Change the shared files in both repositories in matching pull requests, the same way as the audio player.

## Changing a reading

Edit this course's `.json` file, then rebuild:

- EDCOR 310: `python3 build/build_site.py` (it builds `site/joy-of-learning.html` along with the rest of the site)
- Econ 150: `python3 build/wrap_pages.py` (it builds `etb-live/joy-of-econ.html`)

Commit the data file and the rebuilt page together. Never edit the built page by hand. The next build overwrites it.

Each reading looks like this:

```json
{
  "id": "the-case-for-phone-free-schools",
  "title": "The Case for Phone-Free Schools",
  "url": "https://www.afterbabel.com/p/phone-free-schools",
  "minutes": 20,
  "format": "read",
  "topic": "Adolescence / technology",
  "hook": "Should phones be locked away for the whole school day?",
  "blurb": "Jonathan Haidt argues that schools should go phone-free…",
  "source": "After Babel — read for about 20 minutes.",
  "alt": [{"label": "Transcript", "url": "https://…"}],
  "pairs": ["another-reading-id"]
}
```

- `id` is permanent. Students' saved picks, and the planned Reading Return ratings, attach to it. Keep it when you retitle a reading. A new reading needs a new, unique id (lowercase words joined by hyphens).
- `minutes` is the stop point the hour meter counts, not necessarily the full runtime. Keep it equal to the number in `source`.
- `format` is `watch`, `listen`, or `read`.
- `topic` (EDCOR 310) or `stance` (Econ 150: `Pro-market` or `Market-critique`) is optional.
- `alt` lists the same content somewhere else (a BYU-Idaho copy, a transcript). Different content gets its own entry.
- `pairs` points to readings that go together. The builder links them both ways in the page and stops if an id is missing.

A week can carry content notes in its `notes` list. The requirement (an hour a week from the unit's menu, or an hour per unit) is set by `requirement` in the `course` block.

## What the page does

Students can mark readings "I'll read this" or "My group has it," filter by format, length, and viewpoint, and copy their list for slides or prep checks. A meter shows the minutes picked against each unit's requirement. All of it is saved in the student's browser only. Nothing is sent anywhere, and the page still lists every reading if the script fails. There is deliberately no notes box: students submit their notes separately.

## History

These menus were moved here in October 2026 from two Word documents: *ECON 150 Pacini Joy of Econ Menu* and the Joy of Learning section of *EDCOR 310 Reading Calendar and Study Guide*. Each repository keeps its own course's original in `menus/original/` for reference. The data files are now the source of truth. Bundled entries were split so that every reading has its own heading, link, and time.


## Vote distributions

Anyone can open a reading with `+` and use the small **Reveal** button to see that reading's aggregate semester histogram. The **Reveal all votes** button at the bottom shows the distributions for every reading. These are aggregate semester ratings, not individual responses; students should make their own reading decisions before revealing the comparison data.
