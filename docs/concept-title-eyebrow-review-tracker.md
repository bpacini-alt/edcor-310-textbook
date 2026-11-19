# Concept title and eyebrow approval tracker

This tracker records the title/eyebrow pair for each numbered concept in the two live textbook sources, along with approval status, implementation state, and review batch. The unique key is book + chapter + concept.

## Scope and source snapshot

- EDCOR 310: Chapters 1–26, `etb-live/chapterN.html`
- Econ 150: Chapters 1–26, `etb-live/ChapterN.html`
- This covers numbered concept sections. It excludes the Econ Chapter 0 math review and chapter-banner title/subtitle text.
- EDCOR source snapshot: `8cca054a79e5b2e4974f22e3cb0a069c3e2ce999`
- Econ source snapshot: `dc5c2adebddf7aa0c40caa655924ba2019d9f899`
- The source scan contains **275 concept pairs**: 140 EDCOR and 135 Econ.

## Capitalization standard

- Concept titles use **Title Case**.
- Eyebrows use **sentence case**, preserving proper names, acronyms, and named terms such as Rider and Elephant.
- This standard is applied to EDCOR title-review batches. Econ is untouched until its review.

## Status meanings

- **Clearly approved**: you explicitly approved the pair, with evidence in a merged title-review PR or recorded decision. Chapter 16.3 is live from merged PR #146. Batch 2 edits are in open PR #147; Batch 3 and the Chapter 10 slate are in open PR #149; Econ 17.2 and 19.8 are in open PR #190.
- **Needs review**: an explicit proposal is waiting for your decision, the current pair conflicts with previously approved wording, or you specifically held it for another pass.
- **Unverified — assume okay**: no row-level approval evidence was located. Under your workflow, keep the current pair and count it as okay unless you flag it.

## Progress

| Status | Pairs |
| --- | ---: |
| Clearly approved | 225 |
| Needs review | 9 |
| Unverified — assume okay | 41 |
| **Total** | **275** |

By your default-to-okay rule, **275/275 (100%)** are complete; no pairs remain in the needs-review queue. Explicitly approved: **234/275 (85.1%)**. These measures are separate: unverified rows count toward completion by default, but not toward explicit approval.

## Batch 1 outcome

All 15 EDCOR pairs that had defaulted to okay were explicitly approved. Chapter 16.3 is live with the eyebrow “Agency grows when effort works” (merged PR #146). The five Chapter 10 pairs have since been approved; see the latest title-review slate below.

## Batch 2 outcome

All 20 EDCOR Batch 2 pairs are approved. Chapter 16.6 is “Autonomy Support — Choice needs structure,” and Chapter 2.2 is “Cognitive Biases — You cannot see a blind spot.” The capitalization changes and approved pair edits are in open PR #147.

## Batch 3 outcome

All 20 EDCOR Batch 3 pairs are approved. Chapter 23.5 is now “The Flynn Effect — Intelligence responds to environment.” The Batch 3 eyebrow updates and newly approved Chapter 10 and 23.5 pairs are in open PR #149.

## Current review queue

None. All explicitly flagged items have been resolved; 41 unverified pairs remain defaulted to okay.

## Remaining unverified pairs

## Latest slate outcome

Approved: EDCOR 2.2; EDCOR 10.1–10.5; EDCOR 23.5; Econ 17.2; and Econ 19.8, “The Coase Theorem — Bargaining can (theoretically) lead to efficient outcomes.” Econ 17.5 is a separate “Measuring Deadweight Loss” section and defaults to okay.

After Batch 3, five unverified EDCOR pairs remain outside a batch. The remaining Econ unverified rows default to okay under your workflow.


## Batch 4 in progress

Twenty unverified pairs are presented in Batch 4 with the current title and eyebrow proposed unchanged. User review is pending; the pairs remain unverified until approved or flagged.
## Batch 3 inventory

Batch 3 contains EDCOR Chapter 18 Concepts 1–5; Chapter 19 Concepts 1–6; Chapter 20 Concept 1; Chapter 21 Concepts 1–4; Chapter 23 Concepts 5–6; and Chapter 24 Concepts 1–2.

## Earlier aggregate count

An earlier chat mentioned 246 pairs and roughly 33 remaining, but no durable row-level list was found to map that estimate to current concepts. The current source scan has 275 pairs, so this tracker uses the current inventory and preserves that older estimate only as context.


## Next after title review

- Create an aphorism tracker for Econ 150 and the Learning book.
- Create a teaching-strategies tracker for the Learning book only.
