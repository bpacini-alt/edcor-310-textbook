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
