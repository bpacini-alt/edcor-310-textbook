# Chapter Anchor Workflow

**Applies to:** Joy of Economics and Joy of Learning.  
**Author direction recorded:** November 22, 2026. **Opening-placement standard approved:** November 23, 2026. Keep this file identical in both repositories.

## Start here

Read each repository's `AGENTS.md`, `REPOSITORY-HOUSEKEEPING.md`, and relevant priorities before changing files. Then read:

- [Current handoff and next work](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/docs/CHAPTER-ANCHOR-HANDOFF.md).
- [Cross-book chapter ledger and decision log](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/docs/CHAPTER-MENTAL-ANCHOR-TRACKER.md).
- The actual chapter on current `main`, its existing figures, and relevant open PRs.

The handoff is a dated snapshot. Recheck current `main` and PR status rather than assuming a previous chat's status still applies. The chapter text is the authority for what the chapter currently says. Do not depend on a local file path, chat memory, or an unmerged branch as if it were published.

## Purpose and working rhythm

Create a memorable scene that helps a student recall the chapter's central model, relationship, story, or research finding. A chapter title illustrated literally is not enough.

Work in small reviewable batches, normally one or two chapters. When Benjamin requests brainstorming, provide descriptions first. “No images yet” is a real constraint. Generate when he selects a direction and asks to try it. A clear request to generate, revise, place approved images, or open a PR authorizes that work; routine implementation choices do not need repeated permission.

## 1. Read and hunt

Read the chapter's central explanations and nearby examples. Look for its strongest actual stories, research findings, parables, historical cases, and narratives. Search the rest of the book for a candidate before assigning it: an excellent story may belong more strongly elsewhere.

Distinguish an empirical finding from a thought experiment, metaphor, or teaching parable. Do not promote a memorable anecdote into verified history. If a new story or finding would strengthen the chapter, identify it as proposed new content, verify it with primary sources, and develop a short sourced vignette for review.

Record the source repository, chapter file, section heading, and reviewed commit. Check the real chapter list rather than inferring numbering.

## 2. Give a compact scene brief

Explain:

1. The chapter idea in one sentence.
2. A short anchor name.
3. One concrete scene and how its visible parts map to the idea.
4. One likely misconception to avoid.
5. The chapter source and any evidence needed for a new vignette.

Prefer a strong focal point and a coherent scene. Avoid generic decoration, collages, many panels, and piles of explanatory labels. A caption may explain the relationship, but it should not have to rescue an unrelated picture.

## 3. Match the correct book's approved style

Open and inspect approved repository images before generating. Reuse their art direction without copying the subject matter.

| Book | Established treatment | Useful approved references |
| --- | --- | --- |
| Joy of Economics | Restrained, utilitarian charcoal/graphite on warm cream paper; sparse forms, minimal detail, quiet analytical tone, negative space. Muted color accents and lettering have been approved for particular scenes. | [Broken window](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/etb-live/images/chapter-anchors/ch01-broken-window.png), [diamond–water](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/etb-live/images/chapter-anchors/ch02-diamond-water.png), [cafés](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/etb-live/images/chapter-anchors/ch23-monopolistic-competition-cafes.png) |
| Joy of Learning | Bright, lively, warm, human-centered realistic cartoon; painterly texture, believable people and objects, clear storytelling. Keep expressive faces and natural proportions. | [Highlighter](https://github.com/bpacini-alt/edcor-310-textbook/blob/main/etb-live/images/chapter-anchors/intro-highlighter-retrieval.png), [elephant and rider](https://github.com/bpacini-alt/edcor-310-textbook/blob/main/etb-live/images/chapter-anchors/ch02-elephant-rider.png), [baseball study](https://github.com/bpacini-alt/edcor-310-textbook/blob/main/etb-live/images/chapter-anchors/ch11-baseball-prior-knowledge.png), [curb ramp](https://github.com/bpacini-alt/edcor-310-textbook/blob/main/etb-live/images/chapter-anchors/ch24-curb-cut-access.png) |

Do not blend Econ's charcoal treatment into Learning or make Econ glossy and colorful by default.

Images are text-free by default. Specific author-requested lettering or numbers are exceptions: café signage, the Army test heading, gas prices, and the $1 / $5,000 diamond–water cards are established examples. Keep HTML captions outside the image. Do not add incidental brands, watermarks, or unnecessary labels.

## 4. Generate, inspect, and revise

Use original AI-generated artwork by default and the available image-generation workflow. For an edit, inspect the exact target image and preserve the approved scene, style, and other requested invariants. Fix one concrete problem at a time.

Before presenting a candidate, inspect:

- Hands, tools, machinery, animal anatomy, furniture, and perspective.
- Object proportions relative to people and one another.
- The physical action and whether it suggests a false mechanism.
- Expressions, gaze, social relationships, and unintended emotional signals.
- Clothing and setting: avoid incidental tourist or costume narratives that distract from a metaphor.
- Readability at a chapter's normal size, including any explicitly requested text.

Save versioned candidates and their prompts/source notes. Keep original and revision prompts distinguishable. A generated file's actual dimensions may differ by a pixel; read them instead of assuming a standard size.

## 5. Keep three decisions separate

| Decision | Meaning |
| --- | --- |
| Concept selected | Benjamin chose a story or scene direction. |
| Exact image approved | Benjamin explicitly approved the displayed candidate/version. |
| Published | The placement PR has merged and the live page has been checked. |

“I like it” followed by a requested change means revise. Style approval does not approve every candidate. A single “Both approved” can approve both exact images just shown. Never silently substitute an earlier draft for an approved revision.

After explicit image approval, proceed with the requested placement/PR work. Preserve the exact approved artwork and record which version was approved. Any later visual modification requires an image decision again.

## 6. File in GitHub and place chapter anchors at the opening

**Benjamin's current destination is the textbook repositories, with chapter figures and merge PRs.** Library folders are an optional archive. Older cached Chapter Anchor Studio instructions describing Library-only filing or read-only repository work do not reflect his later explicit GitHub direction. Do not require Library access or claim Library filing without verification.

| Book | Editable source and image folder | Required publication step |
| --- | --- | --- |
| Econ | `etb-live/ChapterN.html`; images in `etb-live/images/chapter-anchors/`. Chapter-owned HTML is between the page-header/footer markers. | Econ serves `etb-live/` directly. Follow `AGENTS.md` for wrapper/front-page rebuild triggers; do not hand-edit generated headers, footers, or assets. |
| Learning | `etb-live/chapterN.html` or the real front-matter filename; images in `etb-live/images/chapter-anchors/`. | Run `python -X utf8 build/build_site.py`; commit the corresponding generated `site/` pages and copied `site/images/` assets. Never hand-author the generated pages. |

Use descriptive stable asset filenames, such as `ch02-elephant-rider.png`. Preserve the approved source file by default; do not crop or recompress an approved image silently.

Use a semantic `figure` with:

- Descriptive alt text for the visible scene.
- A student-facing `figcaption` connecting the scene to the chapter.
- Actual intrinsic width/height and responsive sizing with automatic height.
- Lazy loading where appropriate.
- A stable figure ID for direct preview links.

For each approved chapter-anchor entry with a title card, place the opening figure immediately after the card (after its title, subtitle, and metadata) and before the opening hook. The image and caption should orient the reader to the chapter's central idea before the prose begins. Apply the same rule to an approved titled pre-chapter page such as the study guide.

Keep ordinary charts, diagrams, research evidence figures, and other supporting visuals beside the passage they explain; they are not chapter-opening anchors.

For an anchor designed as a task and reveal pair, place the unsolved task immediately after the title card and keep the solution or reveal beside its explanation later in the chapter. Do not expose the answer before the attempt. Record any other author-approved placement exception and its learning reason in the chapter note and cross-book tracker. Source notes and generation details belong in documentation, not in the student flow.

For each new approval, add or update `docs/chapter-anchors/<concept>.md` with the source/commit, mapping, misconception, exact filename/version, approval record, original prompt, and edit prompts. Keep an approval index or ledger link nearby. If an older image's original prompt is unavailable, say so rather than inventing a reproduction record.

## 7. Verify and deliver a review-ready PR

Start from current `main`, inspect open work, preserve unrelated changes, and use a branch and PR. Follow each repository's build method.

For this author-approved anchor workflow, deliver one ready-for-review PR when asked for a mergeable PR. If available tools cannot promote a draft, prepare and verify the branch first and open the final PR as non-draft. This is the narrow exception to early draft-claim timing in the repository coordination instructions; avoid creating duplicate PRs to escape draft status.

Verification should establish:

- The published image is the exact approved asset; source and generated copies agree.
- Captions, alt text, references, and actual dimensions are correct.
- Existing prose, scripts, styles, practice embeds, and navigation are preserved.
- Required builds pass, and generated changes are limited to the expected files.
- The deployed preview loads the images and captions at desktop and phone widths without horizontal overflow.
- The PR's Files changed tab contains only the intended files.
- GitHub reports the final PR ready and conflict-free; report check failures or concrete limits accurately.

Use the PR's actual Cloudflare preview URL. Screenshot/rendering failures are not evidence that the page is visually correct; distinguish rendered inspection from DOM/geometry checks. Do not claim a check you could not perform.

Do not add tests that merely mirror a low-impact insertion. Use meaningful build, preservation, asset, and layout checks. Documentation-only work needs focused link/diff checks rather than a whole-book rebuild unless the repository requires one.

Benjamin normally merges. Do not merge, close someone else's PR, or delete files/branches without the appropriate author instruction. After a merge, check the live pages before declaring publication verified.

## 8. Update continuity before leaving the task

Update the [cross-book tracker](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/docs/CHAPTER-MENTAL-ANCHOR-TRACKER.md), the relevant per-book index/source notes, and the [handoff](https://github.com/bpacini-alt/Econ-150-textbook/blob/main/docs/CHAPTER-ANCHOR-HANDOFF.md). Record concepts, exact-image approvals, publication routes, and the next unresolved work separately.

The shared tracker lives in Econ. A Learning placement may therefore have a small companion Econ documentation PR. Cross-link them and give Benjamin both links.

List current pending image PRs from GitHub; label drafts, superseded work, and tracker-only PRs clearly. Recheck after a merge instead of leaving stale “waiting” claims. A new chat should be able to continue using GitHub alone.
