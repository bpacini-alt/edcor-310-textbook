# Working in this repository

This file is for every collaborator, human or AI (Claude, ChatGPT/Codex). Read it before changing anything, then read:

- `REPOSITORY-HOUSEKEEPING.md`: how collaborators coordinate, and the cleanup rules
- `PROJECT-PRIORITIES.md`: what matters most right now and what is deliberately deferred

`REPOSITORY-HOUSEKEEPING.md` is the same in both textbook repositories (`edcor-310-textbook` and `Econ-150-textbook`); change it in both, in matching pull requests.

`PROJECT-PRIORITIES.md` is each book's own list of what it needs. The goal is that each book's file lists everything that book needs, not that the two files match. When an item applies to both books (the shared design and tools, decisions about the series, work planned for both), put it in both files, in matching pull requests. When it applies to only one book, put it only in that book's file. Expect the two files to differ more over time.

## The short version

1. Start from the current `main`. Check open pull requests and the last few merges for the same task.
2. Claim the work: open a draft pull request titled with the task as soon as you start.
3. Every collaborator change goes through a branch and a pull request. The private prose editor is the documented exception: Benjamin's Save and publish action commits chapter prose directly to `main`.
4. Before you ask for review, open the pull request's **Files changed** tab and confirm it touches only the files you meant to change.
5. Merging is Benjamin's approval. Don't merge, close, or overwrite someone else's pull request.
6. Ask Benjamin before deleting files or branches.

## How this book is built (EDCOR 310)

The website is learning.benjaminpacini.com, served by Cloudflare from the `site/` folder (see `wrangler.jsonc`). Requests to `/api/*` go to `feedback/worker.js` instead.

| Folder | What it is | Edit it? |
|---|---|---|
| `etb-live/` | The chapter source: every page as captured from EdTechBooks, plus `manifest.json` (book order and titles). Chapter images are in `etb-live/images/`, at the same paths the pages use (`/images/content_images/…`); the build copies them into `site/images/`. | Yes. Chapter content changes go here. |
| `site/` | The published website, **generated** by `build/build_site.py` | **Never by hand**, except for the private editor's paired update when it saves chapter prose. The next build overwrites other hand edits. |
| `build/` | `build_site.py` and the web version of the cover | Yes |
| `frontmatter/` | The cover, contents, and About page design, shared with Econ 150 (see "Shared") | Yes, in matching pull requests |
| `audio/` | The audio player, narration tools, and previews | Yes (player: see "Shared") |
| `feedback/` | The Report a problem button and the function that receives reports | Yes (see "Shared") |
| `menus/` | The Joy of Learning reading menu: `joy-of-learning.json` holds every reading. `build/build_site.py` turns it into `site/joy-of-learning.html` | Yes, the data file (see `menus/README.md` and "Shared") |
| `original/` | The October 2026 import from Google Drive | No. Archive only. |
| `workbook/` | The printed course workbook: the finished PDF and the scripts that build it (see `workbook/README.md`) | Yes. Rebuild the PDF in the same pull request. |

After changing anything in `etb-live/`, `build/`, `menus/`, or the player, run `python3 build/build_site.py` from the repository root and commit the regenerated `site/` files in the same pull request.

A page's styles must live in its `etb-live/` file, not only in `site/`. The build checks this: if a rebuilt page would have fewer `<style>` blocks than the published one, it leaves that page alone and stops with a message naming it. Copy the missing styles into the `etb-live/` file rather than working around the check.

## Private prose editor

# Private prose editor

The book pages include an **Edit** link for the content pages listed in `etb-live/manifest.json`. The editor is served at `/editor/`; Cloudflare Access must protect `learning.benjaminpacini.com/editor/*`. The Worker also validates the Access JWT and allows only the three email addresses in `feedback/worker.js`.

For each Worker, set these top-level Worker variables and secrets in Cloudflare:

- Text variable `ACCESS_TEAM_DOMAIN`: the full Access team origin, such as `https://your-team.cloudflareaccess.com`.
- Text variable `ACCESS_AUD`: the Application Audience tag for that book's `/editor/*` Access application.
- Secret `EDITOR_GITHUB_TOKEN`: a fine-grained token with Contents: Read and write for this textbook repository only.

The two repositories use the same `feedback/worker.js` and `editor/index.html`, but each has its own Access application audience and its own Worker secret. The token is never stored in Git or sent to the browser.

The editor writes to `main` when Benjamin selects **Save and publish**. EDCOR's Worker updates both `etb-live/<page>.html` and its generated `site/<page>.html` in one Git commit. Cloudflare deploys the commit through the repository's existing deployment connection.

The editor changes only page text. It keeps every style, script, and link the page already has, and it refuses to publish if a save would remove any of them. (An earlier version dropped `<style>` blocks at the top of an `etb-live/` file and stripped scripts inside the page; see the October 24, 2026 fix.)

## Shared between the two books

- **Audio player:** `audio/player/etb-audio.js` and `audio/player/etb-audio.css` are the one place to edit the player, and both repositories must carry identical copies. Change both in matching pull requests. Never edit the copies the builds place in the published folder.
- **Report a problem button:** `feedback/report.js` (the button and form) and `feedback/worker.js` (receives reports at `/api/report` and files each one as an issue in the private `bpacini-alt/textbook-feedback` repository) are shared the same way as the audio player: identical copies in both repositories, changed in matching pull requests. The builds copy `report.js` into the published folder; never edit that copy. The function needs a `GITHUB_TOKEN` secret, set in each Worker's settings in Cloudflare. It never goes in the repository.
  - **Where it goes:** Worker → **Settings** → the top-level **Variables and Secrets** section → **Add variable**, Type **Secret**, then **Deploy**. Not the "Variables and secrets" box inside the **Build** section: that one is only available while the site builds, and the button can't see it. A plain **Text** variable gets wiped by the next deploy, so it must be a Secret.
  - **The token:** a fine-grained GitHub token limited to `textbook-feedback`, with Issues: Read and write. It expires yearly. To renew, regenerate it on GitHub and click **Rotate** on the secret in both Workers. If the button says "That didn't send," a missing or expired token is the first thing to check (the function answers `not_configured` when it has none).
- **Joy reading menus:** `menus/build_menu.py`, `menus/joy-menu.css`, and `menus/joy-menu.js` are identical in both repositories and change in matching pull requests. Each repository keeps its own menu data (`menus/joy-of-learning.json` here in EDCOR 310, `menus/joy-of-econ.json` in Econ 150). See `menus/README.md`.
- **Front pages:** `frontmatter/frontmatter.py` draws both books' cover, contents, and About pages from one design. Both repositories carry identical copies; change it in matching pull requests. Each book passes its own titles, chapters, and colors from its build script (EDCOR 310: `build/build_site.py`; Econ 150: `build/build_front.py`). Never edit the generated pages by hand.
- **Covers:** the full-size EdTechBooks cover is archived at `etb-live/cover.png`. The web version, cleaned up for the new site, is `build/cover-web.png`.

## Known Cloudflare behavior

Every pull request gets a Cloudflare preview. A few minutes after you push, Cloudflare's bot comments on the pull request with a preview address (for example `https://<branch-name>-science-of-learning.bpacini.workers.dev` for EDCOR 310, or `…-econ-150-textbook.bpacini.workers.dev` for Econ 150). Use it to check the pages you changed before asking Benjamin to merge, and give him the links. The live site updates after a merge to `main`; after merging, open the live site and check the pages you changed.

## Writing for students

Anything students read should be clear and simple, in a plain human voice. Use AI-cadence constructions sparingly: reveal pairs, drumroll setups, strings of fragments, punchy pairs, "not this, but that."

## Open decision

The two books are built differently (see "How this book is built"). Benjamin has not yet decided whether to make them match. Until he does, follow each repository's own method and don't convert one to the other.
