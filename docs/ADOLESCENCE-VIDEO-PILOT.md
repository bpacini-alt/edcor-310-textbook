# Chapter 13 video + research box pilot

Two non-live insertions are added only to `chapter13-video-prototype.html` (not the canonical Chapter 13):

1. After concept 1, Adolescent Egocentrism — `#teen-stereotypes-video`.
2. After concept 2, Id, Ego, and Superego — `#teen-parenting-video`.

Each reusable `etb-video-research` component has a 16:9 video placeholder, a concise nonredundant research digest, evidence-strength caveat, practical implication, and `<details>` references. The card's styles live in the chapter source, not only generated output. The draft is registered in `build/build_site.py`, hidden from menus, and should be removed from DRAFTS when approved or abandoned.

To add videos after upload, replace only each `.evr-video` placeholder with a responsive accessible embed (use a descriptive iframe title, loading=lazy, and privacy-conscious domain where possible). Keep the evidence summary available as text, and check captions/transcripts.

The prototype intentionally avoids a transcript that duplicates the spoken video. The teen-stereotype evidence is rated promising because the experiments are limited to young people's own stereotypes and three days of follow-up. The parenting meta-analyses are more informative for developmental patterns than for causal intervention claims.

**Build:** `python3 build/build_site.py` from the repo root regenerates `site/chapter13-video-prototype.html`. Do not merge until the preview is reviewed and a full build is verified.
