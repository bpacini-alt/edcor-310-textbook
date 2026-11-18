# Concept title and eyebrow approval tracker

This tracker records the current title/eyebrow pair for each numbered concept in the two live textbook sources, along with approval status, implementation state, and any review batch. The unique key is book + chapter + concept.

## Scope and source snapshot

- EDCOR 310: Chapters 1–26, `etb-live/chapterN.html`
- Econ 150: Chapters 1–26, `etb-live/ChapterN.html`
- This covers numbered concept sections. It excludes the Econ Chapter 0 math review and chapter-banner title/subtitle text.
- EDCOR source snapshot: `d55b49b12010c1284c91db787ab42d0a849cd1f5`
- Econ source snapshot: `dc5c2adebddf7aa0c40caa655924ba2019d9f899`
- The source scan contains **275 concept pairs**: 140 EDCOR and 135 Econ.

## Status meanings

- **Clearly approved**: you explicitly approved the pair, with evidence in a merged title-review PR or a recorded approval. Implementation state is tracked separately; the approved Chapter 8–9 edits are in open PR #143, and the approved Chapter 16.3 eyebrow is in open PR #146.
- **Needs review**: an explicit proposal is waiting for your decision, or the current pair conflicts with a previously approved wording. It also includes pairs you have specifically flagged for closer review.
- **Unverified — assume okay**: no row-level approval evidence was located. Under your chosen workflow, keep the current pair and count it as okay unless you flag it.

## Progress

| Status | Pairs |
| --- | ---: |
| Clearly approved | 187 |
| Needs review | 7 |
| Unverified — assume okay | 81 |
| **Total** | **275** |

By your default-to-okay rule, **268/275 (97.5%)** are complete; 7 pairs remain in the needs-review queue. Explicitly approved: **187/275 (68.0%)**. These are separate measures: unverified rows count toward completion by default, but not toward explicit approval.

## Batch 1 outcome

You approved all 15 EDCOR pairs that had defaulted to okay. Chapter 16.3 keeps the title “Learned Helplessness” and uses the approved eyebrow “Agency grows when effort works”; its implementation is in PR #146. The five EDCOR Chapter 10 proposals remain in the needs-review queue.

## Batch 2

Batch 2 contains 20 unverified EDCOR pairs: Chapter 1 Concepts 1–6; Chapter 2 Concepts 1–4; Chapter 3 Concepts 1–3; Chapter 16 Concepts 5–6; and Chapter 17 Concepts 1–5. They remain **Unverified — assume okay** until you flag a pair. The Econ Chapter 17 conflicts remain on hold for a later review.

## Current review queue

- EDCOR 310: Chapter 10 Concepts 1–5.
- Econ 150: Chapter 17 Concepts 2 and 5 (current wording differs from older approved wording). These are on hold for later review.

## Earlier aggregate count

An earlier chat mentioned 246 pairs and roughly 33 remaining, but no durable row-level list was found to map that estimate to current concepts. The current source scan has 275 pairs, so this tracker uses the current inventory and preserves that older estimate only as context.
