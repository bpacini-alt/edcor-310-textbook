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

- **Clearly approved**: you explicitly approved the pair, with evidence in a merged title-review PR or a recorded approval. This includes the 10 approved pairs whose implementation is in open PR #143.
- **Needs review**: an explicit proposal is waiting for your decision, or the current pair conflicts with a previously approved wording.
- **Unverified — assume okay**: no row-level approval evidence was located. Under your chosen workflow, keep the current pair and count it as okay unless you flag it.

## Progress

| Status | Pairs |
| --- | ---: |
| Clearly approved | 172 |
| Needs review | 7 |
| Unverified — assume okay | 96 |
| **Total** | **275** |

By your default-to-okay rule, **268/275 (97.5%)** are complete; 7 pairs remain in the needs-review queue. Explicitly approved: **172/275 (62.5%)**. These are separate measures: unverified rows count toward completion by default, but not toward explicit approval.

## Batch 1

The first 20 pairs are EDCOR 310 Chapters 10 (Concepts 1–5), 11 (Concepts 1–6), 12 (Concepts 1–5), and 16 (Concepts 1–4). The five Chapter 10 rows have proposals awaiting your decision; the other 15 default to keeping the current wording. Rows are labeled `Batch 1` in the CSV.

## Earlier aggregate count

An earlier chat mentioned 246 pairs and roughly 33 remaining, but no durable row-level list was found to map that estimate to current concepts. The current source scan has 275 pairs, so this tracker uses the current inventory and preserves that older estimate only as context.
