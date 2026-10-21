# Working in this repository

This file is for every collaborator, human or AI (Claude, ChatGPT/Codex). Read it before changing anything, then read:

- `REPOSITORY-HOUSEKEEPING.md`: how collaborators coordinate, and the cleanup rules
- `PROJECT-PRIORITIES.md`: what matters most right now and what is deliberately deferred

Those two documents are identical in both textbook repositories (`edcor-310-textbook` and `Econ-150-textbook`). Keep them that way: a change to one goes into the other in a matching pull request.

## The short version

1. Start from the current `main`. Check open pull requests and the last few merges for the same task.
2. Claim the work: open a draft pull request titled with the task as soon as you start.
3. Every change goes through a branch and a pull request. Never push directly to `main`.
4. Before you ask for review, open the pull request's **Files changed** tab and confirm it touches only the files you meant to change.
5. Merging is Benjamin's approval. Don't merge, close, or overwrite someone else's pull request.
6. Ask Benjamin before deleting files or branches.

## How this book is built (EDCOR 310)

The website is learning.benjaminpacini.com, served by Cloudflare from the `site/` folder (see `wrangler.jsonc`). Requests to `/api/*` go to `feedback/worker.js` instead.

| Folder | What it is | Edit it? |
|---|---|---|
| `etb-live/` | The chapter source: every page as captured from EdTechBooks, plus `manifest.json` (book order and titles) | Yes. Chapter content changes go here. |
| `site/` | The published website, **generated** by `build/build_site.py` | **Never by hand.** The next build overwrites hand edits. |
| `build/` | `build_site.py` and the web version of the cover | Yes |
| `audio/` | The audio player, narration tools, and previews | Yes (player: see "Shared") |
| `feedback/` | The Report a problem button and the function that receives reports | Yes (see "Shared") |
| `original/` | The October 2026 import from Google Drive | No. Archive only. |

After changing anything in `etb-live/`, `build/`, or the player, run `python3 build/build_site.py` from the repository root and commit the regenerated `site/` files in the same pull request.

## Shared between the two books

- **Audio player:** `audio/player/etb-audio.js` and `audio/player/etb-audio.css` are the one place to edit the player, and both repositories must carry identical copies. Change both in matching pull requests. Never edit the copies the builds place in the published folder.
- **Report a problem button:** `feedback/report.js` (the button and form) and `feedback/worker.js` (receives reports at `/api/report` and files each one as an issue in the private `bpacini-alt/textbook-feedback` repository) are shared the same way as the audio player: identical copies in both repositories, changed in matching pull requests. The builds copy `report.js` into the published folder; never edit that copy. The function needs a `GITHUB_TOKEN` secret, set in each Worker's settings in Cloudflare. It never goes in the repository.
- **Covers:** the full-size EdTechBooks cover is archived at `etb-live/cover.png`. The web version, cleaned up for the new site, is `build/cover-web.png`.

## Known Cloudflare behavior

Cloudflare's build check shows a red X on every branch and pull request. That comes from Cloudflare's preview-build settings, not from the changes. The build that matters runs on `main` after a merge. After merging, open the live site and check the pages you changed.

## Writing for students

Anything students read should be clear and simple, in a plain human voice. Use AI-cadence constructions sparingly: reveal pairs, drumroll setups, strings of fragments, punchy pairs, "not this, but that."

## Open decision

The two books are built differently (see "How this book is built"). Benjamin has not yet decided whether to make them match. Until he does, follow each repository's own method and don't convert one to the other.
