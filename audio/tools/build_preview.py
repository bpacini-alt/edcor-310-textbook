#!/usr/bin/env python3
"""
build_preview.py — make a stand-alone preview page: a chapter plus the audio player.

Device voice (no audio files; the browser reads the chapter aloud):
    python3 audio/tools/build_preview.py etb-live/chapter22.html audio/preview/chapter22.html

Recorded audio (MP3s listed in a manifest from extract_narration.py):
    python3 audio/tools/build_preview.py etb-live/chapter22.html audio/preview/chapter22-mp3.html \
        --audio audio/ch22 --base ../ch22/

--base is where the page should look for the MP3s, relative to the page.

The chapter HTML is not changed. The page is: a plain shell, the chapter
exactly as it is, the audio data (recorded mode only), and the player inlined.
On the real site the player will be two shared files instead of inlined copies.
"""

import argparse
import json
from pathlib import Path

PLAYER = Path(__file__).resolve().parent.parent / "player"

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>html{{color-scheme:light}}body{{margin:0;background:#fff;color:#1a1a1a}}
/* Preview-only fix: the chapter's hidden hover definitions push the page wider than a phone screen. */
.etb{{overflow-x:clip}}</style>
</head>
<body>
{chapter}
{data}
<style>
{css}
</style>
<script>
{js}
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    ap.add_argument("out")
    ap.add_argument("--audio", help="folder with manifest.json and MP3s (omit for the device voice)")
    ap.add_argument("--base", help="path from the page to the MP3 folder, ending in /")
    ap.add_argument("--book", default="edcor310")
    ap.add_argument("--book-title", default="EDCOR 310 · The Science of Learning")
    ap.add_argument("--author", default="Benjamin Pacini")
    ap.add_argument("--title", help="page title")
    a = ap.parse_args()

    data_block, title = "", a.title or Path(a.chapter).stem
    if a.audio:
        if not a.base:
            ap.error("--base is required with --audio")
        m = json.loads((Path(a.audio) / "manifest.json").read_text(encoding="utf-8"))
        data = {
            "book": a.book,
            "book_title": a.book_title,
            "author": a.author,
            "chapter": m["chapter"],
            "base": a.base,
            "placeholder": m.get("placeholder", False),
            "full_url": a.base + m["full_audio"] if m.get("full_audio") else None,
            "sections": [{k: s[k] for k in ("id", "title", "label", "audio", "est_seconds")} for s in m["sections"]],
        }
        data_block = ('<script type="application/json" id="etb-audio-data">'
                      + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
        title = a.title or f"Chapter {m['chapter']}: {m['title']}"

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(SHELL.format(
        title=title,
        chapter=Path(a.chapter).read_text(encoding="utf-8"),
        data=data_block,
        css=(PLAYER / "etb-audio.css").read_text(encoding="utf-8"),
        js=(PLAYER / "etb-audio.js").read_text(encoding="utf-8"),
    ), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
