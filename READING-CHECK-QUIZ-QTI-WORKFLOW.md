> **Status: Standard for both courses, set by Benjamin on November 10, 2026.**
> This replaces the earlier five-question reading-check workflow. The first import under this format was the Econ 150 Session 17 pilot (November 10, 2026); see the pilot log at the end. The pedagogy and the ten-slot layout are settled. Re-test the Top Hat import details whenever an import fails or Top Hat changes its importer.

# Class Quizzes in Top Hat: Format, Workflow, and QTI Packaging

This document describes how to build the short Top Hat quiz students take at the start of class, for Econ 150 and EDCOR 310. The same document lives in both textbook repositories; change it in both, in matching pull requests.

## 1. What the quiz is for

Students take the quiz in the first few minutes of class. It used to ask one question: did the student read the chapter? It now does more than that. Each quiz gives students a short round of practice:

- easy recall of today's vocabulary and concepts, so everyone starts with a few wins;
- questions that are easy only if you read the chapter, so reading still pays off;
- one strong question on today's chapter that takes real understanding;
- retrieval practice on chapters from earlier in the course, drawn from the course's quizzes and practice quizzes, so the Top Hat quiz is also a chance to practice for the quizzes that count; and
- an honest check on whether the student prepared for class.

It is still short and automatically scored. The strong question (slot 6) gives the class something to start from: Top Hat shows how answers split, so class can open by teaching from it.

## 2. The ten slots

Every quiz has exactly ten questions, in this order.

| # | Slot | What it asks | Source | Difficulty |
|---|---|---|---|---|
| 1–3 | Vocabulary and concept identification | Name a term from its meaning, or classify a simple example | Today's chapter | Easy |
| 4–5 | Reading checks | The chapter's own stories, examples, numbers, and claims | Today's chapter; written new | Easy if you read it |
| 6 | The strong question | One high-quality question that takes understanding, not just recall | Today's chapter; parallel to the common quiz item on this chapter | Harder |
| 7–9 | Retrieval from earlier chapters | Concepts from earlier chapters and units | The course's quizzes and practice quizzes | Moderate |
| 10 | Preparation | "Did you fully prepare for class today?" Yes / No | Fixed | Credit for either answer |

## 3. Rules for each slot

### Slots 1–3: vocabulary and concept identification

- Use the same form as the books' retrieval practice: "What is the word for…?" or "What is the term for…?", with the meaning in the stem and terms as the choices.
- One slot may ask students to classify a simple, new example (for instance, which type of externality a situation is). Keep it easy.
- Distractors are real terms from the same chapter or course, so a student who only half knows them has to think.

### Slots 4–5: reading checks

These are the questions from the earlier workflow. They reward the student who read.

- Pull from the chapter's most memorable material: opening stories and hooks, aphorisms and memorable phrases, named people and examples, unusual numbers, and the chapter's central claims in its own language.
- Ask which example, phrase, person, number, or claim the chapter used, rather than "why is this important?"
- No novel scenarios or calculations in these slots.

### Slot 6: the strong question

- One question on today's chapter that takes understanding: a calculation, a graph reading in words, or an application to a new case.
- Build it as a **parallel** to the common quiz item on this chapter's topic: the same skill with a new context and new numbers. Never copy a graded quiz item.
- Aim it at what the common quiz actually asks about this chapter, and only at material the class has reached by that day. If the chapter goes further than the quiz or than class has gone (in Econ 17, measuring deadweight loss), leave that out of slot 6.
- Students take it before class, so it must be fair to someone who read the chapter carefully but hasn't been taught it yet. It can be harder than the other slots; it can't depend on class.
- Make each wrong answer a specific, common mistake (for example: forgetting the ½, or reporting total damage as deadweight loss). Then the answer split tells Benjamin what to teach.
- This is the only slot where application and calculation belong.

### Slots 7–9: retrieval from earlier chapters

- One question from **two or three chapters back**, and two from **an earlier unit**, so the spacing widens.
- Prefer concepts the class is about to review or that students recently missed (check the session slides' agenda and exam notes).
- Source them from the course's quizzes, practice quizzes, practice banks, and memorization quizzes (see section 4).
- **Graded quizzes:** write parallel versions only (the same idea with a different example or different numbers). Practice quizzes that mirror a graded quiz word for word count as graded for this rule.
- **Practice-bank items** written for practice (for example, `practice-engines` items) may be reused word for word when they are single-answer multiple choice. They may keep two or three choices if that is how they were written.
- Stems may name the chapter ("Back in Chapter 7…") when that helps students place the idea.

### Slot 10: preparation

- Always exactly: **"Did you fully prepare for class today?"** with the choices **Yes** and **No**, in that order.
- Either answer earns the point. An honest "No" should never cost a student, or students learn to click Yes.
- The QTI import can mark only one answer correct, so the package keys "Yes." After import, open this question in Top Hat and either mark both answers correct or set it to participation credit (see section 8).

## 4. Sources by course

### Econ 150

| Source | Where | Use |
|---|---|---|
| Chapter pages | `etb-live/ChapterN.html` in this repository | Slots 1–6 |
| Session slides | Google Drive, "Econ 150 Micro Session N" (find the chapter, agenda, and exam notes for the day) | Choosing the chapter and slots 6–9 |
| Original common quizzes (graded) | `legacy/econ-150/quiz-sources/original/` in `practice-engines` | Parallel versions only (slots 6–9) |
| Practice quizzes and answer keys | `legacy/econ-150/quiz-sources/practice/` in `practice-engines` | These mirror the graded quizzes, so parallel versions only |
| Memorization quizzes (Units 1–4) | `legacy/econ-150/memorization-quizzes/` in `practice-engines` | Vocabulary, rules, and stories for slots 1–3 and 7–9 |
| Live practice banks | `items/econ-150/` in `practice-engines` | Single-answer items may be reused as written |

Everything in `practice-engines/legacy/` is historical. Check any item against the current chapter before using it.

### EDCOR 310

**Pending.** Benjamin is gathering the EDCOR 310 quizzes and practice quizzes. Until they arrive, build EDCOR quizzes from the chapter for slots 1–6, and for slots 7–9 use earlier chapters and the concept banks in `practice-engines/legacy/edcor-310/supporting/`. When the quiz sources arrive, add them to this table (in both repositories) and clear the matching item in EDCOR 310's `PROJECT-PRIORITIES.md`.

## 5. The workflow

1. **Find the day's chapter.** Use the session slides for the class day (they name the chapter and show the agenda). The session number and chapter number often match but don't have to.
2. **Read the whole chapter**, from this repository's page. Note the vocabulary cards, stories, misconceptions, worked examples, and quiz-watch notes.
3. **Find the sources for slots 6–9**: the common quiz on this chapter's topic, and two or three earlier topics worth retrieving (section 4).
4. **Draft candidates.** For a normal build, draft about 14: five vocabulary, five reading checks, and four for slots 6–9. Benjamin picks nine; slot 10 is fixed. When Benjamin asks for a quiz the same day, draft the nine directly and offer swaps.
5. **Revise** the selected questions: sharpen stems, make sure only one choice is defensible, and keep the language plain.
6. **Quality-control pass** (section 6).
7. **Record and package** the quiz (section 7), and validate it.
8. **Send Benjamin** the zip and a readable copy of the questions with the key.
9. **Import, fix slot 10, and preview** in Top Hat (section 8).

## 6. Quality control

### Content and scope

- Does each answer come directly from the chapter (slots 1–6) or from the course (slots 7–9)?
- Are slots 1–5 recall and recognition, with no new calculations?
- Is slot 6 fair to a careful reader who hasn't had class yet?
- Are slots 7–9 parallel versions, never copies, of graded or mirrored quiz items?
- Does any question duplicate another too closely?

### Answer quality

- Slots 1–9 have exactly four choices, except reused practice-bank items that were written with two or three. Slot 10 has two.
- Exactly one choice is clearly correct.
- Distractors are plausible to a student who skimmed or misunderstood, sit in the same category and grammatical form as the answer, and are never silly.

### Test-taking cues

- Correct-answer positions across slots 1–9 are varied and roughly balanced (no position more than three times).
- The correct answer is not predictably the longest, most qualified, or most specific choice.
- Punctuation, capitalization, and wording don't give the answer away, and no stem gives away its own answer.

## 7. Recording and packaging

Each quiz is recorded as a data file, then built into the import package with the shared script:

```text
quizzes/top-hat/build_tophat_qti.py            the builder and validator (identical in both repositories)
quizzes/top-hat/<course>/session-NN.json       one file per class quiz: stems, choices, key, slot, and source
```

Run, from the repository root:

```text
python3 quizzes/top-hat/build_tophat_qti.py quizzes/top-hat/econ-150/session-17.json <output folder>
```

The script refuses to build if the quiz breaks the format: not ten questions, slots out of order, a slot 10 that isn't the standard question, choices that aren't four and distinct, a correct answer that is clearly the longest, or answer positions that bunch up. It then builds the zip and checks it (below). Commit the session file, not the zip.

### Why the package is Canvas-shaped QTI

Top Hat's import route expects a **QTI package in the form of a standard Canvas export**, not one standalone QTI XML file. A bare QTI file can be valid XML and still fail, because the importer looks for a Common Cartridge-style package with a manifest, Canvas metadata, and expected file paths.

- **Question import:** Top Hat's educator import tool accepts a `.zip`, scans it, and creates questions. Its support page says QTI import is for classic, single-correct multiple-choice questions, in QTI 1.1.3 format. See [Top Hat's Question Upload guide](https://support.tophat.com/article/Educator-Question-Import).
- **LMS integration:** Top Hat's Canvas integration handles course launch, rosters, grade sync, and deep links. It is not a way to write questions. See [Top Hat's LMS integration overview](https://tophat.com/features/integrations/).

There is no Top Hat connector for Claude to create or assign questions directly. Claude prepares and validates the package; a person imports it and previews it.

**Version note:** Top Hat's help labels its accepted format QTI 1.1.3, while Canvas-export packages (and this package's XML namespace) are QTI 1.2. Don't treat those as the same. If an import fails, test a one-question package against Top Hat's current documentation and update the script and this guide together.

### Package structure

```text
imsmanifest.xml
<assessment id>/
    <assessment id>.xml
    assessment_qti.xml
    assessment_meta.xml
non_cc_assessments/
    <assessment id>.xml.qti
course_settings/
    canvas_export.txt          contains: common_cartridge
```

- The manifest declares the assessment as type `imsqti_xmlv1p2`, points it at the main QTI file, and declares a dependency on the metadata resource. Every path in the manifest must exist in the zip.
- The metadata gives the title, total points (ten), one allowed attempt, and no answer shuffling.
- The QTI uses the namespace `http://www.imsglobal.org/xsd/ims_qtiasiv1p2`, with `cc_maxattempts`, a `root_section` wrapper, and one chapter section holding the items.
- Each item is a `multiple_choice_question` worth `1.0` point, with `maxattempts="1"`, single cardinality, one `varequal` key scoring 100, and `<render_choice shuffle="No">`. Answer positions are set while writing the quiz and held fixed.
- The three QTI copies are byte-for-byte identical, because different importers look in different places.
- The manifest is at the root of the zip, not inside a top folder.

### What the script checks

The zip opens with no corrupt entries; every manifest path exists; the resource type and dependency are right; the XML parses; the item count matches; every item has the right number of choices, exactly one key, and no shuffling; the keyed choice is the intended answer; the item metadata is present; and the QTI copies match.

A valid file can still have a content error. Review the answer key yourself, separately from the XML.

## 8. Importing into Top Hat

1. Upload the zip through Top Hat's educator question import. If the course connects through Canvas, use the test or assessment import, not the textbook-reading integration.
2. Confirm all ten questions arrived, the choice text is intact, each question has one correct answer marked, and the choices are in the expected order.
3. **Fix slot 10:** open "Did you fully prepare for class today?" and either mark both Yes and No correct or set the question to participation credit.
4. Preview or take the quiz once before class.

## 9. Troubleshooting

**"The file is invalid," or the import fails right away.** Check that the upload is a zip, `imsmanifest.xml` is at its root, manifest paths match filenames exactly, the namespace is QTI 1.2, and every XML file is well formed.

**The package imports but questions are missing.** Check that the assessment resource points to the right QTI file, that section and item identifiers are unique, that the QTI copies match, and that `non_cc_assessments/` is present.

**The choices appear but the wrong answer is marked.** Check the `varequal` in the item's response processing, not the visible order. It must match the label of the intended answer.

**The choices are shuffled.** Check that the item has `shuffle="No"`.

**Slot 10 marks "No" wrong.** It wasn't fixed after import. See section 8, step 3.

**The quiz is too easy to guess.** Go back to the quality-control pass: correct answers that are longer, distractors from a different category, unusually precise wording in one choice, a visible pattern in positions, or a stem that repeats the answer.

## 10. Pilot log

| Date | Course and session | Chapter | Notes |
|---|---|---|---|
| November 10, 2026 | Econ 150, Session 17 | 17, Externalities | First quiz in the ten-slot format. Slot 6 is a positive-externality question (direction and size of underproduction, and D2 − D1 as the external benefit), parallel to Market Failures common quiz items 10–11. A first draft asked students to calculate deadweight loss; Benjamin cut it because class hasn't covered that yet, which led to the slot 6 rule about staying within the quiz and class. Retrieval from Ch 15 (elasticity), Ch 7 (tax deadweight loss), and Ch 9 (MC and ATC, the exam's most-missed idea). Import result: to be recorded after class. |
