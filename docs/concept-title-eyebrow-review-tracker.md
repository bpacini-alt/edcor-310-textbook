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
| Clearly approved | 252 |
| Needs review | 1 |
| Unverified — assume okay | 22 |
| **Total** | **275** |

By your default-to-okay rule, **274/275 (99.6%)** are complete; 1 pair remains in the needs-review queue. Explicitly approved: **252/275 (91.6%)**. These measures are separate: unverified rows count toward completion by default, but not toward explicit approval.

## Batch 1 outcome

All 15 EDCOR pairs that had defaulted to okay were explicitly approved. Chapter 16.3 is live with the eyebrow “Agency grows when effort works” (merged PR #146). The five Chapter 10 pairs have since been approved; see the latest title-review slate below.

## Batch 2 outcome

All 20 EDCOR Batch 2 pairs are approved. Chapter 16.6 is “Autonomy Support — Choice needs structure,” and Chapter 2.2 is “Cognitive Biases — You cannot see a blind spot.” The capitalization changes and approved pair edits are in open PR #147.

## Batch 3 outcome

All 20 EDCOR Batch 3 pairs are approved. Chapter 23.5 is now “The Flynn Effect — Intelligence responds to environment.” The Batch 3 eyebrow updates and newly approved Chapter 10 and 23.5 pairs are in open PR #149.

## Current review queue

- EDCOR 310: Chapter 24 Concept 3. The current pair is “Readiness Gaps, Clinical Needs, and Context — Three Types of Student Differences.” A simpler proposal is “Student Differences — Readiness, clinical needs, and context”; an alternative is “Three Kinds of Student Differences — What students need and how to support them.”

## Remaining unverified pairs

There are 22 unverified pairs: Econ 18.3 was not explicitly approved in Batch 4 and remains defaulted to okay; 21 others remain for later batches.

## Latest slate outcome

Approved: EDCOR 2.2; EDCOR 10.1–10.5; EDCOR 23.5; Econ 17.2 and 19.8; EDCOR 24.4–24.6 and 26.5; Econ 3.4–3.5, 15.3–15.7, 16.1–16.4, 17.5, and 18.1–18.2. Econ 18.3 remains unverified/default okay. The sole needs-review item is EDCOR 24.3.

## Batch 4 in progress

Eighteen Batch 4 pairs are explicitly approved. EDCOR 24.3 is held for simpler wording. Econ 18.3 was not explicitly approved and remains unverified under the default-to-okay workflow.

## Batch 3 inventory

Batch 3 contains EDCOR Chapter 18 Concepts 1–5; Chapter 19 Concepts 1–6; Chapter 20 Concept 1; Chapter 21 Concepts 1–4; Chapter 23 Concepts 5–6; and Chapter 24 Concepts 1–2.

## Earlier aggregate count

An earlier chat mentioned 246 pairs and roughly 33 remaining, but no durable row-level list was found to map that estimate to current concepts. The current source scan has 275 pairs, so this tracker uses the current inventory and preserves that older estimate only as context.


## Next after title review

- Create an aphorism tracker for Econ 150 and the Learning book.
- Create a teaching-strategies tracker for the Learning book only.
