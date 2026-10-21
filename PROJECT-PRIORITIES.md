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

### Priority 1 — Polish and stabilize the student-facing books

Make the existing learning experience clear, coherent, and trustworthy before adding substantial new functionality.

- Improve chapter organization and navigation.
- Standardize headings, terminology, examples, figures, exercises, and answer/review patterns.
- Remove confusing or redundant material.
- Repair technical rough edges and inconsistent presentation.
- Check mobile readability, accessibility, page load, and basic usability.
- Identify the chapters where students are most likely to get lost or misunderstand the central idea.

**Why this is high priority:** Better presentation and fewer points of friction benefit every student immediately and multiply the value of every later feature.

### Priority 2 — Add a small number of high-yield interactives/manipulatives

Build simple, reusable interactives that let students see a concept change when they change an input.

Start with concepts where a visual or manipulable model is substantially better than static prose or a graph alone.

- Prefer small, fast, maintainable components over ambitious applications.
- Build reusable patterns rather than one-off experiments.
- Pair every interactive with a clear learning question or prediction task.
- Include a static explanation or fallback so the chapter remains useful if the interactive fails.
- Measure success by whether the interactive helps students reason, not merely whether it looks impressive.

**Why this comes before larger AI features:** A well-designed manipulative can directly improve conceptual understanding with modest technical complexity.

### Priority 3 — Add chapter audio

Continue the audio work already underway, beginning with the chapters where audio will most help students.

- Use the author's voice when practical and pedagogically appropriate.
- Prioritize clear introductions, summaries, difficult explanations, and review sections before recording every word.
- Keep audio associated with the relevant chapter location.
- Provide transcripts or preserve the text as the primary accessible form.
- Establish a repeatable recording, editing, naming, and publishing workflow.

**Why this matters:** Audio improves access and gives students another way to review, but it should not outrank core content repair or the highest-value interactives.

### Priority 4 — Build a reliable PDF export/compiler

Create a polished way for students to download or print a coherent PDF of a book or selected chapters.

- Preserve headings, figures, equations, links, page breaks, and accessibility as well as possible.
- Support both complete-book and chapter-level export if feasible.
- Test output on desktop, mobile, and common PDF readers.
- Automate the process so PDF output stays synchronized with the source.

**Why this matters:** A dependable PDF gives students a familiar, portable, printable format and may be relatively high leverage if the existing publishing system supports it cleanly.

### Priority 5 — Add an AI/notebook export workflow

Investigate an export that lets students use approved chapter materials in an AI notebook or study environment—for example, to summarize, ask questions, review vocabulary, and quiz themselves.

The first version should be simple and controlled:

- Export clean chapter text and supporting materials in a predictable format.
- Include clear instructions and suggested study prompts.
- Preserve citations or links back to the relevant chapter.
- Make the workflow work with more than one service if possible rather than locking the textbook to a single vendor.
- Be explicit about what the AI can and cannot guarantee.

**Why this is not first:** It could be powerful, but its value depends on clean content, stable exports, and careful attention to student privacy, accuracy, and platform changes.

### Priority 6 — Develop real-time policy analysis practice

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
| 1 | Polish and improve the books | Very high | Medium | Main ongoing focus |
| 2 | Small, high-yield interactives | High | Medium | Build selectively |
| 3 | Chapter audio | Medium–high | Medium | Continue in a repeatable workflow |
| 4 | PDF compiler/export | Medium–high | Low–medium | Build once the pipeline is understood |
| 5 | AI/notebook export | Potentially high | Medium–high | Prototype after content/export foundations |
| 6 | Real-time policy analysis coach | Potentially very high | Very high | Strategic later project |

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

### Loose ends from the move to the new sites (recorded October 20, 2026)

Small items found while moving both books off EdTechBooks. Most are quick. Items marked **(Benjamin)** need his decision or his account first.

1. **Images still load from EdTechBooks.** 5 images in EDCOR 310 and 10 in Econ 150 are still served from books.byui.edu. Copy them into each repository and point the pages at the copies **before** EdTechBooks is retired, or they will break.
2. **Switching students to the new sites (Benjamin).** Decide when students move over (a unit boundary or next semester), make the old-to-new address list for updating I-Learn links, and decide what happens to the EdTechBooks versions afterward.
3. **EDCOR 310 reading times disagree.** The contents page estimates reading time from word counts (Chapter 22: 26 min), but each chapter's title card states its own estimate (~50 min). Use the chapter's own number, in `build/build_site.py`.
4. **Typo in Econ 150 Chapter 16:** "argu e" should be "argue."
5. **Leftover branches (Benjamin).** About 29 branches across both repositories belong to pull requests that are already merged or closed. Delete them once Benjamin approves. One of them, `docs/collaborator-coordination` (in both repositories), is the broken version that deleted nearly every file. It must never be merged.
6. **Econ 150 `site/` folder (Benjamin).** It holds an old placeholder page that Cloudflare does not serve. Keep or remove.
7. **Protect `main` (Benjamin).** In each repository's Settings → Branches, add a rule for `main` that requires a pull request and blocks deletion and force-pushes.
8. **Cloudflare preview builds (Benjamin).** Every branch shows a red X. Either turn off branch builds, or turn on preview links, so each pull request gets a test address to click before merging.
9. **The professional website (Benjamin).** benjaminpacini.com is registered, and the old Google Site is archived in the `benjaminpacini-site` repository, but the new site isn't built or connected to Cloudflare yet. benpacini.com, the short version to redirect, is not registered yet.
10. **Renew the report button's GitHub token (Benjamin), by October 2027.** See "Report a problem button" in `AGENTS.md`.

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
