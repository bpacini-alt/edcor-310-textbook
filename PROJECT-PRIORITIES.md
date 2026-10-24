# Textbook Priorities

**Status:** Initial strategic roadmap  
**Purpose:** Keep textbook development focused on the changes most likely to improve student learning and use right now.

## The governing question

Whenever a new idea, task, or request appears, ask:

> Is this the most important thing we could be doing for students right now?

The answer should be based on four considerations:

1. **Student impact:** Will this materially improve understanding, practice, retention, access, or motivation?
2. **Reach:** Will it help many students across many chapters, or only a narrow edge case?
3. **Leverage:** Does it create infrastructure or reusable components that make later improvements easier?
4. **Cost and readiness:** Can we implement and maintain it reliably with the tools and time available now?

An attractive feature should be deferred when it is less valuable than improving the core content, fixing broken workflows, or finishing a high-impact feature already underway.

## Repository stewardship

The textbook repositories should stay orderly enough that the current state is obvious to both humans and AI collaborators. I will serve as the repository housekeeper: periodically inspect the repositories, notice drift, and propose cleanup before clutter becomes a problem.

I should watch for:

- outdated drafts, abandoned experiments, and duplicate files;
- generated files that are no longer produced by the current build;
- orphaned images, audio, PDFs, scripts, and other assets;
- broken links and references to renamed or removed chapters;
- obsolete instructions, configuration, and documentation;
- inconsistent naming, folder structure, or chapter conventions;
- stale branches, issues, and project entries when they obscure the active work;
- build artifacts or temporary files that do not belong in the source repository;
- divergence between the published book and the actual source files.

The default behavior is **inspect, report, recommend, then act**:

1. Identify the item and explain why it appears obsolete, duplicated, or misplaced.
2. Check whether anything currently references or depends on it.
3. Recommend the safest action: keep, move, rename, archive, or delete.
4. Ask the author before deleting files, removing branches, or making other irreversible changes.
5. Record meaningful cleanup decisions so the same question does not recur.

Safe reversible improvements—such as fixing links, clarifying documentation, standardizing names, or reorganizing clearly misplaced files—may be proposed as ordinary maintenance. Deletion is never assumed merely because a file is old.

When Claude or another collaborator has recently worked in the repository, first inspect the current state and recent history before cleaning up. Do not mistake unfamiliarity for obsolescence, and do not delete work simply because it is not part of the current preferred workflow.

## Strategic order of work

### Priority 0 — Establish the source of truth and working system

Before expanding the books, make sure the basic system is dependable.

- Identify the two books and their intended audiences.
- Confirm the repository structure and build instructions.
- Make sure chapters render correctly and consistently.
- Identify broken links, missing assets, failed builds, accessibility problems, and confusing navigation.
- Establish a simple issue/project system with priorities, owners, status, and next actions.
- Create a lightweight definition of done for chapter work and feature work.

**Why this comes first:** Every later feature is less valuable if students cannot reliably access or use the books.

### Priority 1 — Polish and standardize each book

Make each book clear, coherent, accessible, and trustworthy before adding substantial new functionality.

- Standardize formatting **within each book**: headings, terminology, examples, figures, exercises, answer/review patterns, and page conventions. Do not force EDCOR 310 and Econ 150 into identical presentation when their audiences or content call for different choices.
- Improve chapter organization and navigation.
- Remove confusing or redundant material.
- Repair technical rough edges and inconsistent presentation.
- Conduct a dedicated readability and accessibility pass: plain language, heading hierarchy, link text, alt text, contrast, keyboard navigation, focus states, screen-reader labels, mobile layout, and basic usability.
- Put reference lists in expandable/drop-down sections so sources remain available without interrupting the reading flow. Treat this as a substantial evidence-and-sourcing pass: transparency must not become a way to hide inconvenient evidence, and design choices must not reinforce confirmation bias.
- Identify the chapters where students are most likely to get lost or misunderstand the central idea.
- Integrate the chapter-fit readings removed from the student-facing Joy of Econ menu into the relevant Econ 150 chapters. Use the [Joy of Econ chapter-addition backlog](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/menus/joy-of-econ-chapter-additions.md) and classify each item as **add**, **companion**, or **discard**. This is a mid-level quality pass to complete alongside normal chapter revisions.

**Why this is high priority:** Better presentation, trustworthy sourcing, and fewer points of friction benefit every student immediately and multiply the value of every later feature.

### Priority 2 — Make every chapter practice-heavy

Revise both books chapter by chapter so students regularly retrieve, predict, explain, apply, and receive feedback—not merely read and then answer a few questions at the end.

- Build frequent, purposeful practice into the chapter flow rather than treating practice as an appendix.
- Use a mix of recognition, understanding, prediction, explanation, application, and simple transfer, with difficulty increasing as the chapter develops.
- Use practice to surface common misconceptions, not just to reward recall.
- Provide answers, explanations, or feedback where appropriate so students can learn from the attempt.
- Prefer a manageable number of high-quality tasks over busywork or question volume for its own sake.
- Keep the practice aligned with the chapter's central ideas and learning outcomes.

**Why this is high priority:** Practice is where students turn exposure into durable understanding. A practice-heavy chapter can improve learning more directly than adding another presentation feature.

### Priority 3 — Add a small number of high-yield interactives/manipulatives

Build simple, reusable interactives that let students see a concept change when they change an input.

Start with concepts where a visual or manipulable model is substantially better than static prose or a graph alone.

- Prefer small, fast, maintainable components over ambitious applications.
- Build reusable patterns rather than one-off experiments.
- Pair every interactive with a clear learning question or prediction task.
- Include a static explanation or fallback so the chapter remains useful if the interactive fails.
- Measure success by whether the interactive helps students reason, not merely whether it looks impressive.

**Why this comes before larger AI features:** A well-designed manipulative can directly improve conceptual understanding with modest technical complexity.

### Priority 4 — Add chapter audio

Continue the audio work already underway, beginning with the chapters where audio will most help students.

- Use the author's voice when practical and pedagogically appropriate.
- Prioritize clear introductions, summaries, difficult explanations, and review sections before recording every word.
- Keep audio associated with the relevant chapter location.
- Provide transcripts or preserve the text as the primary accessible form.
- Establish a repeatable recording, editing, naming, and publishing workflow.

**Why this matters:** Audio improves access and gives students another way to review, but it should not outrank core content repair or the highest-value interactives.

### Priority 5 — Build a reliable PDF export/compiler

Create a polished way for students to download or print a coherent PDF of a book or selected chapters.

- Preserve headings, figures, equations, links, page breaks, and accessibility as well as possible.
- Support both complete-book and chapter-level export if feasible.
- Test output on desktop, mobile, and common PDF readers.
- Automate the process so PDF output stays synchronized with the source.

**Why this matters:** A dependable PDF gives students a familiar, portable, printable format and may be relatively high leverage if the existing publishing system supports it cleanly.

### Priority 6 — Add an AI/notebook export workflow

Investigate an export that lets students use approved chapter materials in an AI notebook or study environment—for example, to summarize, ask questions, review vocabulary, and quiz themselves.

The first version should be simple and controlled:

- Export clean chapter text and supporting materials in a predictable format.
- Include clear instructions and suggested study prompts.
- Preserve citations or links back to the relevant chapter.
- Make the workflow work with more than one service if possible rather than locking the textbook to a single vendor.
- Be explicit about what the AI can and cannot guarantee.

**Why this is not first:** It could be powerful, but its value depends on clean content, stable exports, and careful attention to student privacy, accuracy, and platform changes.

### Priority 7 — Develop real-time policy analysis practice

Explore a later-stage system in which students analyze a policy in real time, using their notes while responding to probing questions.

Possible components include:

- A policy case with relevant evidence and constraints.
- Student-written analysis rather than simple recall.
- Adaptive follow-up questions.
- Rubric-based feedback.
- A transparent record of sources and reasoning.
- Academic-integrity safeguards appropriate to the course.

**Why this is downstream:** It is potentially the most educationally distinctive idea, but it requires reliable content, assessment design, privacy decisions, platform integration, and careful technical development. It should follow—not displace—the work that makes the books solid and usable.

## Provisional ranking of the current ideas

| Rank | Initiative | Immediate student value | Effort/risk | Recommended posture |
|---:|---|---|---|---|
| 0 | Fix core apps, builds, navigation, and access | Very high | Low–medium | Do first and continuously |
| 1 | Polish and standardize each book | Very high | Medium | Main ongoing focus |
| 2 | Practice-heavy chapters | Very high | Medium–high | Build into every chapter |
| 3 | Small, high-yield interactives/manipulables | High | Medium | Build selectively |
| 4 | Chapter audio | Medium–high | Medium | Continue in a repeatable workflow |
| 5 | PDF compiler/export | Medium–high | Low–medium | Build once the pipeline is understood |
| 6 | AI/notebook export | Potentially high | Medium–high | Prototype after content/export foundations |
| 7 | Real-time policy analysis coach | Potentially very high | Very high | Strategic later project |

This ranking is provisional. A concrete task can move upward if it solves an urgent student problem, unlocks several other projects, or is dramatically easier than expected.

## How book-level priorities should work

The two books should not automatically receive equal attention. Each should be evaluated using:

- number of students affected;
- severity and frequency of current student problems;
- alignment with course outcomes;
- quality and completeness of the current content;
- readiness for improvements;
- reuse across the other book;
- cost of postponing the work.

The default strategy should be to focus on the book, chapter, or feature with the highest combination of student reach and learning impact—not simply the one that is most fun to build.

## Known problems to fix

These are broken now, so they count as Priority 0. Fix them in the GitHub copies when the chapters move to the new site. Leave the EdTechBooks copies alone for now.

### Econ 150: Broken interactive widgets in Chapters 2 and 4

Four interactive pieces don't run in the current chapter files:

- **Chapter 2:** two graph widgets. One is the "Missing Market" widget (the chapter's first script); the other is the chapter's eighth script.
- **Chapter 4:** Interactive practice 1 ("Predict the new equilibrium") and Interactive practice 2 ("Binding or not?").

**Cause:** when EdTechBooks squashed each script onto a single line, a `//` comment ended up commenting out everything after it, so the browser stops with "Unexpected end of input."

**How to fix:** in each affected script, change `//` comments to `/* … */` or restore the line breaks. Then load the chapter on the new site and confirm the widgets work.

**Status:** fix on the new site; do not edit in EdTechBooks. Found during the audio-player work, which doesn't affect these widgets. A check of every EDCOR 310 chapter found no similar problems.

## Deferred structural revisions

### Econ 150 — Reorder the firm-behavior sequence

When we next revise the Econ 150 textbook's firm-behavior unit, change the chapter order to:

9. **Production Decisions**
10. **Costs**
11. **Profit Maximization in the Short Run**
12. **Profit Maximization in the Long Run**

The reasoning is that students should first understand how firms turn inputs into output and make production decisions, then derive and interpret costs, and only afterward apply those ideas to short-run and long-run profit maximization.

**Status:** Record for later; do not implement yet. When this becomes active work, create a GitHub issue to track the structural revision, then use a pull request for the actual chapter and navigation changes.

### EDCOR 310: Fix the unit labels on chapter title cards

The small label at the top of each chapter's title card (for example, "Unit 3 · The Developing Learner") doesn't match the book's four units. Chapters 1–8 say "Unit 1 · The Great Adventure" instead of "Unit 1 · Intro to Psychology," Chapter 14 says Unit 3 though it sits in Unit 2, and Chapters 16–24 say Units 4 and 5.

**How to do it:** go chapter by chapter with Benjamin. Show what each label says now, ask what it should say, then make the changes in one batch.

**Status:** Record for later; do not implement yet.

### Both books: Add recorded narration in Benjamin's voice (ElevenLabs)

Right now every chapter is read aloud by the student's own device voice. That's a stopgap while chapters are still being edited, so no money is spent on audio that would have to be regenerated. Once editing is done, replace it with narration in Benjamin's cloned voice.

**How to do it:**

1. Set up the voice: an ElevenLabs plan with Professional Voice Cloning (Creator or higher), then record clean voice samples and create the clone.
2. Write the generation script. It should take each chapter's text from the player's own reading rules, so the recording says exactly what the device voice says. It generates one file per section, and it keeps a fingerprint of each section's text so later edits only regenerate the sections that changed. Save at 64 kbps mono.
3. For each chapter, after its final edit pass, generate the audio and add the MP3s and section list to that book's repo. The player switches that chapter from the device voice to the recording on its own.

Full details, costs, and file-size limits are in `audio/README.md` under "Stage 2: recordings."

**Status:** Record for later; do not start until the chapters are done being edited. Then go chapter by chapter, starting with the chapters students will be assigned first.

### Both books: "Worth remembering" aphorism boxes (recorded October 24, 2026)

**Benjamin's view:** a clever turn of phrase makes a real difference to what students remember. Each chapter's big ideas should get a short, memorable line, shown in a "Worth remembering" box right where the idea is taught, with a recap of all of them after the chapter synthesis.

**The model:** EDCOR 310 Chapter 11 (Constructivism), added in EDCOR 310 pull request #35. It has six aphorisms, such as "Your brain thinks in examples, not definitions" and "To change a mind, change the schema," each with a one- or two-sentence follow-up, and a recap of all six at the end. The look is the `etb-aphorism` style, which for now lives only in Chapter 11's own style block.

**How to do it:**

1. Move the `etb-aphorism` styles somewhere both books can share, so every chapter uses one design.
2. Go chapter by chapter with Benjamin. Draft three to six candidate aphorisms from each chapter's major concepts; Benjamin chooses and rewords them. They have to sound like him, and each one has to stay true to the evidence in the chapter.
3. Place each box where its idea is taught and add the recap after the synthesis. Use the same wording in the slides and any other course materials, so students meet the same phrase every time.

**Priority:** Medium. Useful for students, but a big lift across two books, because the wording has to be drafted and approved chapter by chapter.

**Status:** Record for later; start when there is time. EDCOR 310 Chapter 11 is done (once #35 is merged).

### Loose ends from the move to the new sites (recorded October 20, 2026)

Small items found while moving both books off EdTechBooks. Most are quick. Items marked **(Benjamin)** need his decision or his account first.

1. **Images still load from EdTechBooks.** 5 images in EDCOR 310 and 10 in Econ 150 are still served from books.byui.edu. Copy them into each repository and point the pages at the copies **before** EdTechBooks is retired, or they will break.
   **Done October 20, 2026** (EDCOR 310 #15, Econ 150 #14). All 15 are now copied into the repositories at the paths the pages already used. The 10 Econ 150 images had been returning "not found" on the new site; the 5 EDCOR 310 images were still loading from books.byui.edu. Wide images were also being cut off at the edge of the page, so EDCOR 310 Chapter 2 and Econ 150 Chapter 1 now shrink images to fit the column.
2. **Switching students to the new sites (Benjamin).** Decide when students move over (a unit boundary or next semester), make the old-to-new address list for updating I-Learn links, and decide what happens to the EdTechBooks versions afterward.
3. **EDCOR 310 reading times disagree.** The contents page estimates reading time from word counts (Chapter 22: 26 min), but each chapter's title card states its own estimate (~50 min). Use the chapter's own number, in `build/build_site.py`.
   **Done October 20, 2026** (EDCOR 310 #15). The book's total on the home page changes from about 13 hours to about 21.
4. **Typo in Econ 150 Chapter 16:** "argu e" should be "argue."
   **Done October 20, 2026** (Econ 150 #14).
5. **Leftover branches (Benjamin).** About 29 branches across both repositories belong to pull requests that are already merged or closed. Delete them once Benjamin approves. One of them, `docs/collaborator-coordination` (in both repositories), is the broken version that deleted nearly every file. It must never be merged.
   **Approved and checked October 20, 2026; deletion still to do (Benjamin).** Benjamin approved deleting every branch whose pull request is merged or closed. 26 qualify: 13 in each repository, listed in EDCOR 310 #16 and Econ 150 #15. Each one's last commit is already in `main` or belongs to a closed pull request. Claude's GitHub access in that session couldn't delete branches, so delete them from each repository's **Branches** page. Keep `main`, any branch with an open pull request, and `docs/collaborator-coordination-clean-20261021` (no pull request; ask Benjamin).
6. **Econ 150 `site/` folder (Benjamin).** It holds an old placeholder page that Cloudflare does not serve. Keep or remove.
7. **Protect `main` (Benjamin).** In each repository's Settings → Branches, add a rule for `main` that requires a pull request and blocks deletion and force-pushes.
8. **Cloudflare preview builds (Benjamin).** Every branch shows a red X. Either turn off branch builds, or turn on preview links, so each pull request gets a test address to click before merging.
9. **The professional website (Benjamin).** benjaminpacini.com is registered, and the old Google Site is archived in the `benjaminpacini-site` repository, but the new site isn't built or connected to Cloudflare yet. benpacini.com, the short version to redirect, is not registered yet.
10. **Renew the report button's GitHub token (Benjamin), by October 2027.** See "Report a problem button" in `AGENTS.md`.
11. **One image rule for each whole book.** An image with no width limit spills past the text column and gets cut off, worst on phones. EDCOR 310 Chapter 2 and Econ 150 Chapter 1 now carry their own fix (`:where(.etb) img{max-width:100%;height:auto}` at the start of the chapter's styles), but an image added to any other chapter will have the same problem. Move the rule into each book's page wrapper: `wrap_chapter_page()` in EDCOR 310's `build/build_site.py`, and the page header in Econ 150's `build/wrap_pages.py`. The Econ 150 change rewrites every chapter's header, so rerun the script and commit all the pages. Then remove the two per-chapter copies and check a few chapters with images at phone width.
12. **Small content fixes.**
    - **EDCOR 310 Chapter 7:** the title card reads "Chapter 7~ 55 min read." The other chapters put the chapter number and the time in separate `<span>`s, which shows them as two items. Give Chapter 7 the same markup.
    - **Econ 150 empty unit pages (Benjamin):** `cvjsuukrox.html` (Unit 1: Markets in Perfect Competition), `PartII.html` (Unit II: The Firm in Perfect Competition), `PartIII.html` (Part II: The Critique of the Market), and `PartIV.html` (Unit IV: The Firm in Imperfect Competition) are empty files, so each shows a blank page on the live site. They were empty on EdTechBooks too, and nothing on the site links to them. Decide whether to write these unit pages (`PartI.html` is the model) or remove them and their `manifest.json` entries.
13. **EDCOR 310 reading times: consider the audio player's length (Benjamin, later).** The contents page now shows each chapter title card's "~N min read," but those numbers were typed by hand and don't track the text well (Chapter 7: card 55 min, player 67; Chapter 11: card 60, player 33; whole book: 21 hours on the cards, 15 by the player). The player measures what it actually reads aloud: 155 words a minute plus short pauses. That number is listening time, so label it "min listen," or note that silent reading is faster. To use it, either run the player in a headless browser during the build (exact, but the build needs a browser) or repeat its word count in Python (simpler, but the two could drift apart). Update the title cards at the same time, so the contents page and the chapter agree. Once the ElevenLabs recordings exist, use the real file lengths instead. Not urgent.

### The series look and front matter (recorded October 22, 2026)

**Benjamin's decision:** the two books should look like two books in a series. They don't have to be identical, but the front matter, the page framing, and the navigation should be built the same way in both unless a real student need calls for a difference. Students who take both courses will know what to expect, and so will anyone working on either book. This settles part of the "Open decision" in each `AGENTS.md`: front matter and page framing will be shared. Whether the chapters themselves are built the same way is still open.

The mockups are in Benjamin's Claude canvas "BenjaminPacini.com Landing Page": the hub, plus a cover page and a contents page for each book. Ask Benjamin for access; it is private.

**Ready to build once preview links work (Priority 1: navigation and access)**

*Status, October 23, 2026: items 1, 2, 4, and 5 are built (pull requests "Cover and contents pages (shared design)" in both repositories). Benjamin chose the two-page version, a cover and then a contents page, over a one-page front, and the plain white Econ look with navy and light brass accents over the darker Canvas-course colors. Still open: item 3 (the shared top bar on chapter pages), Econ 150's unit hooks and reading times, and EDCOR 310's "How to Get the Most Out of This Book" and Introduction.*

1. **A cover page for each book.** The cover art, title, subtitle, authors, and course, with an "Open the book" button (to the contents) and one quick-start button. EDCOR 310's current home page becomes this page. Econ 150 has no cover page yet; its cover is `build/cover-web.png`.
2. **A contents page for each book, in the same design.** A "Start here" group of front matter numbered i, ii, iii. Then each unit with its Roman-numeral badge, a one- or two-sentence hook, and its chapters (number, title, subtitle, reading time). Then back matter, such as EDCOR 310's quick references. Keep EDCOR 310's unit outcomes as a collapsible line under each unit.
3. **The same top bar on every page of both books:** "Benjamin Pacini" (a link to benjaminpacini.com) / the book's title / Contents. Students should always have a way back.
4. **Each book takes its accent color from its cover:** EDCOR 310 uses the cover's blue (#145d90). Econ 150 uses the cover's night navy (#1b2430) with gold numerals (#a87d32). Everything else follows the styles the chapters already use (Georgia, white title cards, the uppercase labels), as in EDCOR 310's `site/assets/book.css`.
5. **Build the front matter from one template,** kept identical in both repositories and changed in matching pull requests, the same way as the audio player.

**Do first:** loose end 8 (Cloudflare preview links), so Benjamin can look at the new pages before anything is merged.

**Writing for Benjamin to do later (Priority 1: content)**

6. **"How to Get the Most Out of This Book," the opening chapter of both books.** Benjamin wants to keep this idea. It sits at ii in "Start here."
7. **An Introduction for EDCOR 310,** at iii in "Start here." Econ 150 already has one ("The Wealth of Nations").
8. **An "About this book" page for each book,** at i in "Start here". EDCOR 310 has a simple version now (`about.html`, built October 23). Benjamin wants it built deliberately, later, as one page with four sections: the book (how it was made), **the authors** (a photo and short bio for each: Benjamin and Mayleigh Barth for EDCOR 310, Benjamin for Econ 150), acknowledgments, and license and how to cite. **Waiting on:** bios (Benjamin's can start from his BYU-Idaho directory bio; Mayleigh's from her), photos, Econ 150's license choice, and a few sentences on how Econ 150 came to be. Build it together with item 3, the shared top bar on chapter pages, which Benjamin approved October 23, and give the About pages the Previous / Contents / Next bar.
9. **One- or two-sentence hooks for Econ 150's four units,** for the contents page. This connects to loose end 12 (Econ 150's empty unit pages).

**Decisions and quick fixes (Benjamin decides; Priority 1)**

10. **Econ 150 chapter titles disagree** between the home page and the chapters' own title cards in Chapters 7, 11, 12, 14, 19, and 26. Chapter 24's title card says "Imperfect Competition I" instead of II, and Chapter 10's subtitle says "fim" for "firm." Decide which titles win, then make the two match. Pull request #22 (the TA's updates to Chapters 13–26) may change some of these, so check after it is settled.
11. **Econ 150 reading times.** The chapters don't state a reading time the way EDCOR 310's do. Word-count estimates put Chapters 17–26 at 10 to 20 minutes, far shorter than the earlier chapters. Recheck after #22, and use the same approach as loose end 13.
12. **Econ 150's license and cover credit** aren't stated on the new site. EDCOR 310 uses CC BY-SA 4.0.

**The hub at benjaminpacini.com (Priority 0: student access)**

13. **A simple landing page at benjaminpacini.com,** so Benjamin can tell students "go to benjaminpacini.com" and they find their textbook right away. It has his photo, a card for each book, and a short "More from me" list (professional site, Substack, LinkedIn). It belongs in the `benjaminpacini-site` repository and connects to loose end 9. **Waiting on:** Benjamin's photo.

### The Joy reading menus (recorded October 22, 2026)

The Joy of Learning and Joy of Econ menus moved from Word into `menus/` (see `menus/README.md`). These items are deliberately low on the list.

14. **Uneven weeks (Benjamin, later).** Some weeks offer far more than others. Joy of Econ: Weeks 9 and 12 have 2 readings each and Week 5 has 3, while Week 13 has 32. Joy of Learning, now that bundles are split: Week 1 has 3 readings and Week 12 has 19. Students choose from the whole unit, so no one is short of options, but a 32-reading week is a wall to scroll through. No good answer yet. Ideas to weigh: move some Week 13 pieces into earlier weeks, group Week 13 by subtopic (inequality, capitalism debates, debt, happiness), or leave it.
15. **Readings whose links need a look (Benjamin).**
    - *Emotional intelligence* (Joy of Learning, Week 12): the YouTube video is gone. It was dropped from the menu and needs a replacement.
    - *How to Think About Trade Deficits* (Joy of Econ, Week 3): the link is a 33-second clip, but the menu promises a ~25-minute EconTalk segment.
    - *The Moral Obligation of Self Worth* (Joy of Learning, Week 8): the link is a 7-minute clip ("Rule 2," JBProbe), but the menu says ~50 minutes.
    - *The Success Paradox* (Joy of Learning, Week 8): the link plays Veritasium's "Why Being Delusional Is a Superpower." Confirm it's the intended video.
    - *The Scandal That Shook Psychology to Its Core* (Joy of Learning, Week 3): the video runs about 30 minutes. The menu keeps ~10 as a stop point.
    - Nine YouTube videos, mostly John List's UChicago series, don't allow embedding. They play fine on YouTube. This matters only if the menus ever embed videos.
16. **One rating scale (decided October 22, 2026).** Reading ratings use the Reading Return four-point scale: 4 · Celebrate (S-tier), 3 · Keep, 2 · Reconsider, 1 · Replace (F-tier). The Joy of Econ instructions now say so. Every menu reading has a permanent `id` the ratings can attach to.

## Cool ideas for later

These are promising possibilities, but they are intentionally near the bottom of the backlog. They should not displace the current work on content quality, practice, accessibility, interactives, audio, exports, or the series/front-matter system.

### Found October 23, 2026

1. **Missing shapes in figures (Priority: High; fix Monday, October 26).** About 50 shapes in both books have no width or height, so they draw nothing: bars, shaded areas, and legend swatches simply aren't there. This is the bug fixed in Econ 150 Chapter 10 (Econ pull request #33), and it was already in the Drive originals.
   - **Econ 150 (about 42):** Chapter 13 is the worst. Its callback-rate, earnings-by-education, and pay-gap charts show no bars at all (15 shapes). Also Chapters 0, 2, 4, 8, 11, 17, and 22, `introduction.html`, and `ittrdogupr.html` (the Chapter 9 homework draft).
   - **EDCOR 310 (8):** Chapter 6's five-color band figure (5) and the legend swatches in A Hero's Journey (`sup1.html`, 3).
   - **The fix:** work out each size from points already drawn in the same figure (axes, labels, lines, dots), the way Chapter 10 was fixed. Then render every figure and compare it with its caption. A shape with an `id`, or inside a practice widget, may be redrawn by code; check before editing it.
2. **Econ 150 unit names on title cards (Benjamin decided October 23; fix Monday).** The contents page's unit names are the official ones: The Case for the Market, The Firm in Perfect Competition, The Critique of the Market, and The Firm in Imperfect Competition. Several chapter title cards use other names ("How Markets Coordinate," "The Logic of Competition," "Critique of Markets," "Market Power and Imperfect Competition"), and Chapters 25 and 26 carry their own labels. Make the cards match the contents page. Still open for Benjamin: the book's subtitle says "Choice, Incentives, and Human Flourishing," while the Canvas course card says "Choice, Tradeoffs, and Human Flourishing."
3. **Save the old Google Site's images (`benjaminpacini-site`).** The archive in `archive/google-site-2026-10-20/` has every page's HTML and every embedded Drive file, but not the pictures shown on the pages. About 40 pages still load their images from Google's servers, so the archive would lose them if the Google Site were deleted. Download the images into the archive, using a browser (Claude's shell can't reach Google Sites), and point the archived pages, or the manifest, at the local copies. **Don't delete the Google Site until this is done.**

### Student sign-in and lightweight progress tracking

Explore a simple Google sign-in system for students, ideally restricted to verified `@byui.edu` accounts. The first useful version would not attempt to replace Canvas or become a full learning-management system. It would provide a shared identity across both books and optionally record low-stakes activity such as reading-check scores, practice scores, and completion dates.

A student dashboard could eventually show a student's own progress, but that is secondary. Instructor dashboards, grade passback, homework management, roster synchronization, and Canvas integration are explicitly out of scope for the first experiment.

**Possible first experiment:** a hidden preview page with Google sign-in and one saved sample score. Test whether BYU-Idaho accounts work cleanly, whether scores persist across devices, and whether the experience is worth maintaining before expanding it.

**Status:** Interesting but deferrable; revisit later. Do not begin until the higher-priority textbook work is in good shape.

## The standing decision protocol

When the author proposes a task, classify it as one of four things:

1. **Critical:** Broken access, broken builds, missing core content, or a problem blocking students now.
2. **High-impact:** A change likely to improve understanding or use for many students.
3. **Strategic infrastructure:** A reusable system that enables several high-impact improvements.
4. **Interesting but deferrable:** Valuable or exciting, but not the best use of current effort.

Before starting a task, report briefly:

- what priority it appears to have;
- what it would displace;
- why it helps students;
- whether it unlocks future work;
- the recommended next action.

If a proposed task is not the highest-value next move, say so plainly and ask whether to proceed anyway.

## Initial operating rhythm

- Maintain one prioritized backlog across both books.
- Keep a short list of the next three highest-value tasks.
- Re-rank when new evidence appears: student confusion, usage data, instructor feedback, failed builds, or new technical constraints.
- Finish small slices before opening too many parallel projects.
- Prefer one working, student-tested feature over several impressive prototypes.
- Review priorities at the beginning and end of each meaningful work session.

## Immediate next steps after GitHub connection

1. Inspect both repositories and identify the actual source/build/publishing structure.
2. Determine which book is currently closer to student-ready and which has the larger urgent need.
3. Inventory broken workflows, unfinished chapters, existing audio, current interactives, and export capabilities.
4. Create the first evidence-based top-three backlog.
5. Choose one student-facing improvement and one enabling infrastructure improvement.
6. Revisit this document whenever a new project is proposed.

## North-star test

The goal is not to build the most technologically elaborate textbook. The goal is to give students a clearer, more useful, more engaging way to understand difficult ideas—and to keep improving the parts that matter most.
