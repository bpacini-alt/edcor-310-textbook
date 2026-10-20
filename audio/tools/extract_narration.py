#!/usr/bin/env python3
"""
extract_narration.py — pull only the narratable prose out of an etb chapter.

Note: the player (audio/player/etb-audio.js) has its own copy of these reading
rules for the device voice. When the ElevenLabs generation script is written,
it should take its text from the player instead, so the two never drift apart.

Usage:
    python3 audio/tools/extract_narration.py etb-live/chapter22.html audio/ch22

Writes:
    <out>/sections/NN-<id>.txt   one plain-text narration script per section
    <out>/narration.txt           the whole chapter as one plain-text file
    <out>/manifest.json           section list: id, title, word count, estimated
                                  length, and a fingerprint (hash) of the text

The fingerprint is what keeps costs down later: when a chapter is edited, only
sections whose fingerprint changed get sent back to ElevenLabs.

How each etb block is handled
-----------------------------
Read aloud:   title card, hook, big idea, concept sections (headings, paragraphs,
              lists, "classic finding" notes), applications, synthesis.
Shortened:    retrieval practice -> the question is read, followed by a cue to
              pause; the answer is not read (it stays on the page).
Converted:    tables -> one sentence per row ("Working Memory. Capacity: ...").
Skipped:      vocabulary flip cards, "also know" chips, videos, images,
              "learn more", interactive widgets, scripts and styles.

Author overrides (add to any element in the chapter HTML)
---------------------------------------------------------
    data-narrate="skip"                    leave this element out of the audio
    data-narrate-text="What to say here"   say this instead of the element's text
"""

import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

WORDS_PER_MINUTE = 155  # typical audiobook pace; adjust once real audio exists

SKIP_CLASSES = {
    "etb-flipgrid", "etb-alsoknow", "etb-yt", "etb-yt-hr", "etb-learnmore",
    "etb-title-watermark", "etb-title-meta", "etb-ret-body", "etb-ret-arrow",
}
SKIP_TAGS = {"script", "style", "img", "figure", "iframe", "video", "audio",
             "canvas", "svg", "input", "button", "select", "textarea", "hr"}

RETRIEVAL_CUE = "Pause the audio and try answering on your own before you go on."

warnings = []


def classes(el):
    return set(el.get("class", [])) if isinstance(el, Tag) else set()


def clean(text):
    text = text.replace(" ", " ")
    text = re.sub(r"\s+", " ", text).strip()
    # Visual-only arrows and "tap" hints never belong in audio.
    text = re.sub(r"[►▼▲↓↑→]", "", text).strip()
    # Symbols a voice model may stumble on. Add to this list as you hear problems.
    text = text.replace(" & ", " and ").replace("&", " and ")
    text = re.sub(r"~\s?(\d)", r"about \1", text)
    text = re.sub(r"\bd\s?=\s?", "d equals ", text)
    text = re.sub(r"\br\s?=\s?", "r equals ", text)
    return text


def sentence(text):
    text = clean(text)
    if text and text[-1] not in ".!?:\"”’)":
        text += "."
    return text


def inline_text(el):
    """Text of an element, honoring data-narrate overrides on descendants."""
    if isinstance(el, NavigableString):
        return str(el)
    if el.get("data-narrate") == "skip" or el.name in SKIP_TAGS:
        return ""
    if el.has_attr("data-narrate-text"):
        return el["data-narrate-text"]
    return "".join(inline_text(c) for c in el.children)


def table_to_sentences(table):
    headers = [clean(th.get_text(" ")) for th in table.select("thead th")]
    rows = table.select("tbody tr") or table.select("tr")[1:]
    out = []
    for tr in rows:
        cells = [clean(inline_text(td)) for td in tr.find_all(["td", "th"])]
        if not cells:
            continue
        parts = [sentence(cells[0])]
        for h, c in zip(headers[1:], cells[1:]):
            parts.append(sentence(f"{h}: {c}" if h else c))
        out.append(" ".join(parts))
    return out


INLINE_TAGS = {"strong", "em", "b", "i", "a", "cite", "sup", "sub", "code", "abbr",
               "mark", "u", "small", "q", "br", "time", "dfn", "s"}
# Small styled labels that should be spoken as their own short sentence.
LABEL_CLASSES = {"etb-app-badge", "etb-app-title", "etb-ret-badge", "etb-syn-header",
                 "etb-note-label", "etb-lm-header"}
BLOCK_TAGS = {"p", "div", "ul", "ol", "li", "table", "h1", "h2", "h3", "h4", "h5", "h6",
              "blockquote", "details", "summary", "section", "figure", "hr"}


def is_inline(node):
    if isinstance(node, NavigableString):
        return True
    if not isinstance(node, Tag):
        return False
    if classes(node) & LABEL_CLASSES:
        return False
    if node.name in INLINE_TAGS:
        return True
    # A span is inline unless it hides block content (some etb spans wrap divs).
    if node.name == "span" and not classes(node) & SKIP_CLASSES:
        return node.find(BLOCK_TAGS) is None
    return False


def walk(el, out):
    """Append narration paragraphs for el (a block container) to out.

    Runs of loose text and inline tags (bold, italics, links, tooltips) are
    joined into one paragraph so a sentence isn't broken at its bold words.
    """
    buf = []

    def flush():
        t = clean("".join(buf))
        buf.clear()
        if t:
            out.append(sentence(t))

    for child in el.children:
        if isinstance(child, Tag) and (child.get("data-narrate") == "skip" or child.name in SKIP_TAGS
                                       or classes(child) & SKIP_CLASSES):
            continue
        if is_inline(child) and not (isinstance(child, Tag) and "etb-slbl" in classes(child)):
            buf.append(" " if isinstance(child, Tag) and child.name == "br" else inline_text(child))
            continue
        flush()
        if not isinstance(child, Tag):
            continue
        c = classes(child)
        if child.get("data-narrate") == "skip" or child.name in SKIP_TAGS or c & SKIP_CLASSES:
            continue
        if child.has_attr("data-narrate-text"):
            out.append(sentence(child["data-narrate-text"]))
            continue
        if "etb-slbl" in c:
            continue  # section labels are spoken once, in the section intro
        if "etb-retrieval" in c:
            summary = child.find("summary")
            q = clean(inline_text(summary)) if summary else ""
            q = re.sub(r"^Retrieval practice\s*", "", q, flags=re.I)
            if q:
                out.append(f"Retrieval practice. {sentence(q)} {RETRIEVAL_CUE}")
            continue
        if "etb-note" in c:
            label = child.select_one(".etb-note-label")
            if label:
                out.append(sentence(inline_text(label)))
            body = child.select_one(".etb-note-body") or child
            walk(body, out)
            continue
        if child.name == "table":
            out.extend(table_to_sentences(child))
            continue
        if child.name in ("p", "li", "h2", "h3", "h4", "h5", "blockquote") or \
                c & {"etb-syn-text", "etb-app-title", "etb-syn-header"}:
            t = clean(inline_text(child))
            if t:
                out.append(sentence(t))
            continue
        if child.name in ("ul", "ol", "div", "section", "details", "summary", "span"):
            walk(child, out)
            continue
        t = clean(inline_text(child))
        if t:
            warnings.append(f"Unrecognized <{child.name} class='{' '.join(c)}'> was read as plain text: {t[:60]}…")
            out.append(sentence(t))
    flush()


def spoken_label(label):
    """'Major concept 3 · Memory' -> 'Major concept 3: Memory.'"""
    return sentence(clean(label).replace(" · ", ": "))


def extract(path):
    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "lxml")
    root = soup.select_one(".etb")
    if root is None:
        sys.exit("No .etb container found — is this an etb chapter?")

    sections = []

    # 1. Introduction: title card + hook + big idea
    intro = []
    num = clean(root.select_one(".etb-title-watermark").get_text()) if root.select_one(".etb-title-watermark") else ""
    title_el = root.select_one(".etb-title-main") or root.select_one(".etb-title-card h1, .etb-title-card h2")
    title = clean(title_el.get_text(" ")) if title_el else ""
    sub = clean(root.select_one(".etb-title-sub").get_text(" ")) if root.select_one(".etb-title-sub") else ""
    intro.append(sentence(f"Chapter {num}. {title}" if num else title))
    if sub:
        intro.append(sentence(sub))
    for sel in (".etb-hook", ".etb-bigidea"):
        el = root.select_one(sel)
        if el:
            if sel == ".etb-bigidea":
                intro.append("The big picture.")
                t = clean(inline_text(el))
                if t:
                    intro.append(sentence(t))
            else:
                walk(el, intro)
    sections.append({"id": "intro", "title": title or "Introduction", "label": "Introduction", "paras": intro})

    # 2. Concept sections
    for i, concept in enumerate(root.select(".etb-concept"), start=1):
        lbl = concept.select_one(".etb-slbl")
        h2 = concept.find("h2")
        label = clean(lbl.get_text(" ")) if lbl else f"Major concept {i}"
        heading = clean(h2.get_text(" ")) if h2 else ""
        paras = [spoken_label(label)]
        body = []
        walk(concept, body)
        # The h2 is picked up by walk(); keep it right after the label.
        paras.extend(body)
        sections.append({"id": f"concept-{i}", "title": heading or label,
                         "label": label.replace("Major concept", "Concept"),
                         "paras": paras})

    # 3. Applications and synthesis
    app = root.select_one(".etb-applications")
    if app:
        paras = []
        walk(app, paras)
        app_title = app.select_one(".etb-app-title")
        sections.append({"id": "applications", "title": clean(app_title.get_text()) if app_title else "In the Classroom",
                         "label": "In the classroom", "paras": paras})
    syn = root.select_one(".etb-synthesis")
    if syn:
        paras = []
        walk(syn, paras)
        sections.append({"id": "synthesis", "title": "Chapter Synthesis", "label": "Wrap-up", "paras": paras})

    # De-duplicate accidental repeats (e.g., a badge read twice) and drop empties.
    for s in sections:
        seen, keep = set(), []
        for p in s["paras"]:
            if p and p not in seen:
                keep.append(p)
                seen.add(p)
        s["paras"] = keep
    return title, num, sections


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    title, num, sections = extract(src)
    (out / "sections").mkdir(parents=True, exist_ok=True)

    manifest = {"chapter": num, "title": title, "source": str(src),
                "words_per_minute": WORDS_PER_MINUTE, "sections": []}
    full = []
    for n, s in enumerate(sections, start=1):
        text = "\n\n".join(s["paras"])
        words = len(text.split())
        fname = f"{n:02d}-{s['id']}"
        (out / "sections" / f"{fname}.txt").write_text(text + "\n", encoding="utf-8")
        full.append(text)
        manifest["sections"].append({
            "id": s["id"],
            "title": s["title"],
            "label": s["label"],
            "words": words,
            "characters": len(text),
            "est_seconds": round(words / WORDS_PER_MINUTE * 60),
            "hash": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
            "text": f"sections/{fname}.txt",
            "audio": f"{fname}.mp3",
        })
    (out / "narration.txt").write_text("\n\n\n".join(full) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total_words = sum(s["words"] for s in manifest["sections"])
    total_chars = sum(s["characters"] for s in manifest["sections"])
    print(f"Chapter {num}: {title}")
    for s in manifest["sections"]:
        print(f"  {s['id']:<14} {s['words']:>5} words  ~{s['est_seconds']//60:>2}:{s['est_seconds']%60:02d}  {s['title']}")
    print(f"  total          {total_words:>5} words  ~{round(total_words / WORDS_PER_MINUTE)} min  ({total_chars:,} characters ≈ ElevenLabs credits)")
    for w in warnings:
        print("  WARNING:", w)


if __name__ == "__main__":
    main()
