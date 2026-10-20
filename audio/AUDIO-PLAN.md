# Chapter audio: draft plan

**Status:** draft for discussion. Nothing here touches the live chapters yet.

The goal is to replace the current audio version (which reads the HTML along with the prose, and often doesn't work) with narration in Benjamin's own voice, generated with ElevenLabs. This folder holds a working mock-up in Chapter 22 and the tools that would produce the real thing.

## What's in this folder

| Path | What it is |
|---|---|
| `preview/chapter22.html` | Chapter 22 exactly as it is now, plus the audio player. Open it in a browser to try it. |
| `player/etb-audio-player.html` | The player itself: one block of style and script that gets added to the end of a chapter. |
| `tools/extract_narration.py` | Pulls only the prose a listener should hear out of a chapter and splits it into sections. |
| `tools/build_preview.py` | Puts a chapter, its section list, and the player together into one page. |
| `ch22/` | Chapter 22's narration script (`narration.txt`, plus one file per section), its section list (`manifest.json`), and **silent placeholder MP3s** sized to the estimated length of each section. |

The placeholder audio is silent on purpose. Everything else about the player is real: the timeline, skipping, speed, jumping between sections, resuming. Once there's a voice clone, the silent files get swapped for real ones and nothing else changes.

## How it looks in the chapter

**A Listen button on the title card.** It sits under the subtitle, styled like the rest of the etb labels, and shows the listening time ("Listen · 28 min"). If a student stops partway through, it changes to "Resume · 12:27" the next time they open the chapter. A small "Text-only version" link sits next to it.

**A quiet "Listen" link on each section label.** Each "Major concept" label gets a small link on its right edge with that section's length. It's gray until you hover. When that section is playing, it turns green and shows a small moving sound indicator. Students can start the audio at any concept without scrubbing.

**A player docked at the bottom of the screen.** It slides up when someone presses Listen. It shows which section is playing (tap the title to scroll the text back to it), back and forward 15 seconds, play/pause, a timeline with small breaks between sections, and a speed button (0.75× to 2×). A contents button lists every section with its length, plus "Download the whole chapter (MP3)" and the text-only version. The player works on phones, and the audio keeps playing with the screen locked, with lock-screen controls.

**A thin green line beside the section being read**, so a student who glances back at the page can find their place.

## What gets read aloud

The extractor follows the etb design system, so it works on all 26 chapters without changes. A test run on every chapter produced no warnings.

| Read | Changed | Skipped |
|---|---|---|
| Title and subtitle, hook, big picture | Retrieval practice: the question is read, then "Pause the audio and try answering on your own before you go on." The answer isn't read. | Vocabulary flip cards and "also know" chips |
| Concept sections: headings, paragraphs, lists | Tables: each row becomes a sentence ("Working Memory. Capacity: about 4 chunks. Duration: …") | Videos, images, "learn more" |
| Classic-finding and research boxes | A few symbols: "&" becomes "and", "~4" becomes "about 4", "d = 0.5" becomes "d equals 0.5" | Interactive widgets |
| In the classroom, chapter synthesis | | Hover definitions (the term is read, the pop-up isn't) |

These are defaults, and all of them can change. Two attributes give you control over any single element in a chapter:

- `data-narrate="skip"` leaves that element out of the audio.
- `data-narrate-text="…"` says something different from what's on the page. This is the tool for figures and graphs: `<img … data-narrate-text="Figure 2.1 shows confirmation bias as a loop …">`.

To check what will be read before paying for anything, open the chapter's `narration.txt`.

## What it would cost

Narration length, using the extractor's counts at a typical audiobook pace:

- Chapter 22: about 4,400 words, 28 minutes, roughly 28,000 characters.
- Chapters run from about 19 minutes (Ch. 26) to 63 minutes (Ch. 7). Most are 28–40 minutes.
- The whole book: about 136,000 words, roughly 14½ hours, and about 886,000 characters.

ElevenLabs charges in credits, roughly one per character at its best quality. As of fall 2026 its pricing page lists the Creator plan (the cheapest one with a Professional Voice Clone) at about 121,000 credits a month, and the Pro plan at 600,000. That works out to:

- **Creator:** about four chapters a month. Fine for the just-in-time approach.
- **Pro for one month, then back to Creator:** enough for most of the book in one push.

Unused credits roll over for up to two months while the plan stays active. Prices change, so check the pricing page before deciding.

## Keeping regeneration cheap while chapters change

This is why the audio is split by section instead of one long file per chapter. Each section in `manifest.json` has a `hash`, a fingerprint of its exact text. When a chapter is edited, the generation script compares fingerprints and only sends the changed sections to ElevenLabs. Fixing a typo in Concept 3 regenerates about two minutes of audio, not the whole chapter. The full-chapter download file gets rebuilt from the section files at no cost.

The working plan stays the same: do a final edit pass on a chapter shortly before students are assigned it, then generate.

## Where the audio files would live

Not in this GitHub repo. MP3s are large (the whole book is roughly 400–800 MB, depending on quality), and Git handles large files poorly. When the site moves to Cloudflare, the audio goes in Cloudflare's file storage (R2), and the page points there. The `--base` option in `build_preview.py` exists so that switching locations is a one-line change. The silent placeholders in `ch22/` are small enough that keeping them here for the draft is fine.

## Listening outside the book

- **Now:** "Download the whole chapter (MP3)" in the player. Students can put it in any audio app.
- **Later, if wanted:** a podcast feed for the book. A private feed URL works in Apple Podcasts and most other podcast apps. Spotify only takes public shows, so putting the book on Spotify would make the audio public.

## Text-only version

For now, the "Text-only version" link opens `narration.txt`, the same clean text the voice reads. That already fixes the "hearing the HTML" problem for students using screen readers or their phone's read-aloud. A nicer version would be a simple reading page with real headings, which screen readers can navigate by section. That's a small follow-up once the site moves.

## Something found along the way

On phones, the hidden hover definitions (`data-tip`) make Chapter 22 slightly wider than the screen, so the page can be dragged sideways. Twenty-five chapters use the same hover definitions, so most probably have the same issue. It's barely noticeable now, but it pushes a bottom-docked player partly off screen. The preview page works around it with one line of CSS (`.etb{overflow-x:clip}`). The real fix is a small change to the tooltip CSS in each chapter, which fits naturally into the batch edits planned after the move.

## Next steps

1. Decide on the open questions below.
2. Record audio for the voice clone and set it up in ElevenLabs.
3. Write the generation script. It runs on Benjamin's computer with the API key kept in a local file (never committed here), reads each `manifest.json`, generates only new or changed sections, and builds the full-chapter MP3.
4. Generate one real chapter and listen critically: pacing, pronunciation, how the retrieval cues feel.
5. Add the player to chapters as their audio is ready.
6. Check whether the Econ 150 chapters use the same design system, and adapt the extractor if not.

## Open questions

- Should the vocabulary cards be read? They're left out now because the same terms are defined in the text.
- Is the retrieval-practice cue right? Other options: read the question and the answer, or skip retrieval practice entirely.
- Should "Text-only version" stay on the title card, or move into the player's menu only?
- Is a podcast feed worth doing, and if so, private or public?
