# Chapters 21–22 draft review

Benjamin requested review previews on November 26, 2026, following the outline in the Chapters 21–22 reorganization plan (PR #178) and Mayleigh's attached patch, notes, and chapter drafts.

Starting point: Learning `main` at `3d631c3`, including PRs #172 and #180. The implementation uses separate `chapter21a.html` and `chapter22a.html` review pages, registered in `DRAFTS`. The current numbered chapters remain the published versions.

Draft direction: six concepts in Attention, Executive Function & ADHD; four concepts in Working Memory & Long-Term Memory. Keep Fryer at the Chapter 21 opening and place the pass-counting task/reveal in its Attention concept. Chapter 22 opens with the existing working-memory hook and has no new opening artwork. Preserve the fuller Chapter 21 for Benjamin's first review.

## Review outline

| Draft | Concepts, in order |
|---|---|
| `chapter21a.html` · Attention, Executive Function & ADHD | 1. Executive Function; 2. Attention; 3. Executive Dysfunction; 4. ADHD and Executive Function; 5. Tier 1 Interventions; 6. Assessment and Diagnosis |
| `chapter22a.html` · Working Memory & Long-Term Memory | 1. Memory; 2. Cognitive Load Theory; 3. Forgetting and Desirable Difficulties; 4. Retrieval, Spacing, and Interleaving (including metacognition) |

Concepts have stable `#concept-1`, `#concept-2`, etc. anchors for review.

## What was carried forward

Mayleigh's November 24 patch and November 25 attachment to PR #178 supply the section moves, transitions, working-memory bridge, merged attention concept, and the new flashcard retrieval question. Her earlier Chapter 21 revision is already in main via PR #150.

The drafts preserve main's subsequent metacognition subsection (#180) and reciprocal-teaching limitation (#172), along with the Dunedin paragraph, schemas, worked examples, fading, and the activities for using working memory. No broad Chapter 21 trim was applied.

Small editorial changes beyond Mayleigh's attachment:

- The Chapter 22 title follows Benjamin's discussed working-memory/long-term-memory split. Titles remain editable at review.
- The old two-meanings-of-chunking box becomes a short steps-versus-chunks clarification, since Chapter 21 now consistently says steps.
- The active-learning/feeling-of-learning side quest moves from CLT to Forgetting and Desirable Difficulties. The retrieval side quest remains with retrieval practice.
- The CLT/desirable-difficulties bridge includes retrieving, discriminating between methods, and spaced returns, and emphasizes manageable challenge and sufficient prior knowledge.
- The attention opener acknowledges both deliberate control and automatic capture. The video-game cross-reference is framed as an application of laboratory research, not a demonstrated explanation of games.
- Two reference placeholders are completed from the original sources. The Harvard phone report is correctly attributed to **Burland et al.**, not Kane as first author. Allcott et al.'s publication status is updated from working paper to accepted journal article, including the matching retrieval answer.

## Images

All approved image files are reused unchanged. Fryer opens 21a; the pass-counting task opens its Attention concept and the gorilla reveal remains beside the explanation. This is a deliberate draft placement within the new chapter; the current Chapter 22 opening remains unchanged. Chapter 22a has no new opening artwork and retains the conceptual forgetting-curve SVG beside its explanation.

## Source checks for unfinished references

- Fabiano et al. (2026): [publisher article](https://jamanetwork.com/journals/jamapediatrics/article-abstract/2856649), DOI `10.1001/jamapediatrics.2026.5973`. Title, authors, publication date, and accommodation finding confirmed.
- Burland et al. (2026): [Harvard report](https://cepr.harvard.edu/sites/g/files/omnuum9881/files/2026-11/Phone-Free%20Schools%20and%20Achievement%20Growth.pdf). Correct author order and report title confirmed.
- Allcott et al. (2026): [accepted journal article](https://doi.org/10.1093/qje/qjag050), published online October 30, 2026. The near-zero average achievement effect remains; the claim that both phone studies are unreviewed working papers is removed.

This is a structural revision with focused source checks, not a new full evidence audit of both chapters.

## Validation

- `python3 build/build_site.py` completes; its aphorism check reports no problems.
- Only the two draft sources, their generated pages, the `DRAFTS` registration, and review documentation change. The current numbered chapters and contents remain unchanged.
- Each concept retains retrieval practice; 21a has seven questions across six concepts, and 22a has four across four concepts.
- The drafts retain every existing image, iframe, script, and aphorism from the combined current chapters; the forgetting-curve SVG stays in 22a. No duplicate HTML IDs or unresolved reference placeholders were found.
- Draft banners link to the current chapters, and both generated pages have `noindex` metadata.

## At the eventual chapter swap

After Benjamin has reviewed and approved the drafts, coordinate the numbered chapter replacements, manifest titles, Chapter 24 perceptual-load pointer, anchor inventory/source notes and cross-book ledger, concept title/eyebrow tracker, Chapter 22 narration, item-bank concept labels, Top Hat/slides, and forgetting-curve priority pointer. The published record should continue to describe the current chapters until that swap. PR #178 remains the planning/history handoff; this PR supplies the review pages.

## Revision 1: purpose and organization (November 26, 2026, Benjamin's review)

Benjamin's review: the chapters are good but repetitive, and they spend too much time qualifying research and too little on application. The main fix is a clear purpose for each chapter.

**Shared spine.** A simplified learning map (senses → attention → working memory → long-term memory, based on Atkinson & Shiffrin, 1968). Chapter 21 shows the first steps; Chapter 22 completes the map, including encoding and retrieval.

### Chapter 21a (done in this revision)

- **Purpose:** how information gets in, and how the learner manages it. ADHD is the main case. The teacher's role: get curious, build the system, hand it over.
- **Hook:** Fryer, explained up front and tied to executive function (clear steps lower the planning and working memory load). The CEO story and the elephant/rider passage are cut. Fryer appears once more, as a pointer in the Daily Report Card card. Checked against Fryer (2011): overall Dallas effects were not significant; gains were for students tested in English; the NYC qualitative finding and Fryer's two explanations (students didn't know how to turn effort into scores; quizzes gave immediate feedback) are as stated.
- **One evidence note after the big picture**, listing the ideas the chapter repeats: attention is limited; executive function grows; behavior systems, organization training, and self-monitoring have the strongest evidence; lend your systems, then fade them; observe, describe, and refer. Later sections drop their separate caveats.
- **"Can't or won't" becomes will and skill, approached with curiosity.** It now appears in the big picture, Concept 1, the About the Aphorism box, the classroom list, and the synthesis.
- **Four concepts:** 1. Executive Function (opens with Dunedin; includes "When executive function struggles" with the pattern questions and the 1 Samuel box) · 2. Attention · 3. ADHD (assessment and the teacher's role become a subheading) · 4. Supporting Students.
- **Attention:** the phone box now lists what we know, with Ward demoted to one sentence and the publication-status detail removed. The decorations box uses the Goldilocks framing and ends with why the finding runs against school culture. The "it also has limits" paragraph and the flow box are folded into a sentence or two. Fabiano (2026) moves to "Tested, and didn't help."
- **Removed duplication:** the second executive-dysfunction box, the 2-minute-rule box (now a table row), the prose list of ADHD myths (citations moved into the myths table), the Fryer research box, and the video-game retrieval question (replaced by an inattentive-presentation scenario).
- **Collapsible notes** (these two chapters only): side notes are closed by default. The professional-line box is collapsible but starts open.
- **Length:** visible text, not counting references, went from about 10,100 to 9,200 words. Concept text went from 8,330 to 7,310. The default reading path, with notes closed, is shorter still.

### Chapter 22a (done in this revision; plan as agreed)

- Title: **Memory and Cognitive Load**. The big picture says the teacher's goal is long-term memory.
- Concepts: 1. Memory (full learning map; Miller's 1956 paper told straight, then why "seven" stuck, with the phone-number claim checked against the paper; chunking with a two-meanings box that points back to Fryer's steps; schemas point back to Chapter 11; fluency defined as a skill running with little working memory because long-term memory supplies it) · 2. Cognitive Load Theory (intrinsic vs. extraneous; no germane box; "Putting memory to work: Implications of Cognitive Load Theory" with five principles: ruthlessly cut extraneous load, with seductive details promoted and defined; practice beyond mastery; build an intuition for how much to teach at once, with the curse of knowledge pointing back to Chapter 2; adjust based on mastery, with worked examples; put everything in one place) · 3. Retention and Transfer (opens with desirable difficulties, pointing back to Chapter 1 and named as the turning point after CLT; residue of thought; forgetting curve; retrieval routines including "teach a spot in the room," a directed brain dump; spacing; interleaving reframed as learning to recognize the kind of problem; explaining and teaching activities moved here from CLT) · 4. Metacognition (eyebrow: "The rider teaches the elephant." The text says the feeling of familiarity doesn't go away; the rider learns not to trust it and builds habits).
- Aphorisms, one per concept: new card **"Clear their path, but make them climb."** (Benjamin's wording, approved November 26) at the end of CLT; "Memory is the residue of thought" in Retention and Transfer; "The brain is not designed for thinking…" in Metacognition. Record the new line in the cross-book aphorism bank (Econ 150 repository).
- Fix the formatting problem around the "Best learning doesn't feel like learning" side quest.
- Practice sort (intrinsic vs. extraneous load): deferred to the practice-items work. No placeholder for students.

### Swap implications

The move from six concepts to four (Chapter 21) changes concept numbers for item-bank labels, Top Hat quizzes, and slides. Add this to the swap checklist above.

### Chapter 22a: build notes

- **Miller check:** the 1956 paper never mentions telephone numbers. The hook says only what Miller argued. "How small is working memory?" explains why "seven" stuck (the title, everyday seven-digit numbers) and quotes Miller's own doubt ("only a pernicious, Pythagorean coincidence").
- **Restored a missing line:** Willingham's "Practice until you are perfect and you will be perfect only briefly" (Willingham, 2004). The aphorism bank records it in Chapter 22's Spaced Practice prose, but it was in neither `main` nor the draft. It now sits in Principle 2.
- **Fixed the side-quest layout:** the floating video cards were followed by a heading and table that clear floats, which left a blank gap. Both cards now sit beside prose: "Active learning" in Retention and Transfer, and "Best learning doesn't feel like learning" in Metacognition.
- **Principle 5 (split attention)** cites Chandler & Sweller (1991).
- **Additions:** a load-examples table (intrinsic vs. extraneous), new retrieval questions on calibration (metacognition), vocabulary cards for seductive details and metacognition, and "Teach a spot in the room" as a fourth retrieval routine.
- **Length:** visible text, not counting Learn More, went from about 6,770 to 7,480 words. The added material (map, principles, examples, metacognition concept) outweighs the cuts. If shorter is better, the likeliest places to trim are "Explain it to learn it" and the interleaving evidence paragraph.
- **Still open:** Chapter 22 has no reference list, on `main` or here. References are a deferred workstream in `PROJECT-PRIORITIES.md`. Log "Clear their path, but make them climb." in the cross-book aphorism bank (Econ 150 repository; this session has read-only access to it).

## Swap (November 26, 2026)

Benjamin approved both drafts and asked for them to be merged. The draft text replaced `chapter21.html` and `chapter22.html`, the `DRAFTS` entries and draft pages were removed, and the manifest titles were updated. Chapter 24's perceptual-load pointer now says Chapter 21. The concept title/eyebrow tracker, anchor records, and forgetting-curve priority note were also updated. Out-of-repo follow-ups are listed in `PROJECT-PRIORITIES.md` under "Chapters 21–22 reorganization follow-ups."
