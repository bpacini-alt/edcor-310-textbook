# Concept title and eyebrow approval tracker

This tracker records the current concept title/eyebrow pairs in the two live textbook sources and the approval evidence located for each pair. The unique key is book + chapter + concept.

## Scope and source snapshot

- EDCOR 310: Chapters 1–26, `etb-live/chapterN.html`
- Econ 150: Chapters 1–26, `etb-live/ChapterN.html`
- This covers numbered concept sections. It excludes the Econ Chapter 0 math review and chapter-banner title/subtitle text.
- EDCOR source snapshot: `d55b49b12010c1284c91db787ab42d0a849cd1f5`
- Econ source snapshot: `dc5c2adebddf7aa0c40caa655924ba2019d9f899`
- The current source scan contains **275 concept pairs**: 140 EDCOR and 135 Econ.

## What the status means

- **Approved — merged PR**: the current pair is supported by a merged title-review PR or a recorded user approval from the Chapter 5–7 review.
- **Approved — PR #143 open**: you approved the pair, but the implementation PR is still open.
- **Proposed — awaiting user review**: a proposal has been presented but is not yet approved. Chapter 10 is the current slate.
- **Approval record not located**: the pair exists in the current source, but I did not find a row-level approval in the title-review PR history checked so far. This does not mean you rejected it; it needs reconciliation with the prior chat decisions.
- **Recheck — current pair differs from PR #99**: an earlier merged decision exists, but the current source pair no longer matches it.

## Counts in this snapshot

| Status | Pairs |
| --- | ---: |
| Approved — merged PR | 162 |
| Approved — PR #143 open | 10 |
| Proposed — awaiting user review | 5 |
| Approval record not located | 96 |
| Recheck — current pair differs from PR #99 | 2 |
| **Total** | 275 |

## Reconciliation note

An earlier chat referred to an aggregate inventory of 246 pairs and a rough estimate of 33 remaining, but no durable row-level tracker or list of those 33 keys was found. The current source scan has 275 pairs, so that older aggregate cannot be safely carried forward as the exact remaining count. This file uses row-level PR evidence and marks missing evidence as unverified rather than assuming approval or rejection.

The five Chapter 10 proposals are in this file so they can be marked as approved, revised, or declined after review. Continue future slates from the rows whose status still needs reconciliation or approval.
