# Chapter 13 video + research box pilot

Two non-live insertions are added only to `chapter13-video-prototype.html` (not the canonical Chapter 13):

1. After concept 1, Adolescent Egocentrism — `#teen-stereotypes-video`.
2. After concept 2, Id, Ego, and Superego — `#teen-parenting-video`.

Each reusable `etb-video-research` component has a 16:9 video placeholder, a concise nonredundant research digest, evidence-strength caveat, practical implication, and `<details>` references. The card's styles live in the chapter source, not only generated output. The draft is registered in `build/build_site.py`, hidden from menus, and should be removed from DRAFTS when approved or abandoned.

To add videos after upload, replace only each `.evr-video` placeholder with a responsive accessible embed (use a descriptive iframe title, loading=lazy, and privacy-conscious domain where possible). Keep the evidence summary available as text, and check captions/transcripts.

The prototype intentionally avoids a transcript that duplicates the spoken video. The teen-stereotype evidence is rated promising because the experiments are limited to young people's own stereotypes and three days of follow-up. The parenting meta-analyses are more informative for developmental patterns than for causal intervention claims.

**Build:** `python3 build/build_site.py` from the repo root regenerates `site/chapter13-video-prototype.html`. Do not merge until the preview is reviewed and a full build is verified.

## Updated design and video IDs

The prototype now matches the previously approved compact optional video side-quest pattern: calm blue, right-floated beside concept prose on desktop, full width on mobile, with a click-to-expand native `<details>` player and nested sources. Avoids making video mandatory or repeating the entire spoken script. Each video uses a YouTube privacy-enhanced iframe and a direct YouTube fallback link.

- Assumed video-order mapping from the two URLs supplied: `6dsDNHMNc8M` = teenager stereotypes; `hxvtdETIAGs` = parenting teenagers. YouTube metadata and transcripts were not accessible through the available retrieval methods, so verify video titles before merging.
- Transcripts: not yet inspected. YouTube captions should be verified manually if accessible; don't label the research boxes as transcripts.

## Three-part research note + evidence ladder revision

Both optional side quests now open with a video, then **1. Findings**, **2. Nuance**, **3. Application**, followed by expandable study-by-study primary references. A compact four-rung CSS-only evidence hierarchy highlights where the claims are grounded; for parenting it highlights both synthesis and the longitudinal designs inside it. The diagram notes that meta-analysis of observational evidence is not automatically causal.

For teen stereotypes, the main studies are **Arnett (1999)**, **Jacobs et al. (2005)**, **Buchanan & Hughes (2009)**, and **Jussim & Harber (2005)**. **Qu et al. (2020)** is contextual supplementary evidence, not the leading result, because it manipulated young people's own beliefs, rather than parental expectations. Student-facing text explicitly distinguishes perceptual bias from self-fulfilling effects.

**Pending:** Neither exact transcript has been provided or verified yet. Once available, compare what the videos say with the prose and citations; retain only complementary material in these boxes.
