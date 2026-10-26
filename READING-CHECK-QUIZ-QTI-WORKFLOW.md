# Reading-Check Quizzes: Pedagogy, Workflow, and Top Hat QTI

This document describes the repeatable process for turning a textbook chapter into a short, importable reading-check quiz.

The central question is simple:

> **Did the student read the chapter?**

These quizzes are not intended to measure sophisticated application, transfer, calculation, or comparative statics. Those belong in class activities, practice sets, exams, and application quizzes. The reading check should reward students who noticed and remembered what the chapter actually said.

## 1. Why use a reading check?

A reading assignment without retrieval is easy to misunderstand. Students may read the words, recognize the ideas while the text is in front of them, and then retain very little afterward. A short quiz creates a reason to read attentively and gives students a small amount of retrieval practice immediately after reading.

The quiz also protects the role of the textbook. If the quiz asks only for generic definitions or requires students to solve novel problems, students can sometimes succeed without reading the chapter. A good reading check makes the chapter's own stories, examples, language, and claims matter.

The quiz should therefore be:

- short enough that it does not compete with the chapter;
- specific enough that reading is rewarded;
- memorable enough that students remember the chapter's central images and claims;
- easy to score automatically; and
- separate from the deeper application work that happens elsewhere.

## 2. What belongs in the quiz?

The best candidates usually come from the chapter's most memorable material:

- opening stories and hooks;
- aphorisms, quips, and memorable turns of phrase;
- names of thinkers, researchers, companies, or historical examples;
- unusual numbers or comparisons that make an idea concrete;
- distinctive examples used to explain a concept;
- important claims made in the chapter's own language;
- diagrams or narratives that students should recognize; and
- vocabulary when the chapter gives the term a particularly useful meaning.

The strongest question is often not “Why is this important?” but:

> **Which example, phrase, person, number, or claim did the chapter use?**

For example, rather than asking students to apply a general principle to a new housing market, ask them to identify the chapter's explanation of who benefits from restricted housing and who bears the cost. Rather than asking students to solve a new supply-and-demand problem, ask what happened in the chapter's two-city housing story.

## 3. The standard workflow

### Step 1: Gather the chapter

Use the cleanest available source:

1. direct chapter HTML or text when available;
2. a PDF when the web page is inaccessible; or
3. pasted text as a fallback.

The chapter should be read as a whole. The goal is not to pull isolated vocabulary from a summary. We want to understand what the author emphasized, what stories carried the chapter, and what claims students are most likely to remember.

If a web page is blocked or returns incomplete content, provide the HTML, PDF, or text rather than relying on a partial scrape. The source supplied for quiz writing should be treated as authoritative.

### Step 2: Generate ten candidates

For each chapter, generate **10 candidate four-option, single-answer multiple-choice questions**. The candidates should cover the chapter's strongest reading-check material rather than distribute evenly across every paragraph.

The initial set should deliberately include variety:

- a story or opening hook;
- an aphorism or distinctive phrase;
- a named thinker, company, or example;
- a central claim;
- a concrete number or comparison;
- a key term in the chapter's own framing; and
- one or two questions that test the chapter's central narrative.

The user then selects the preferred questions. The final quiz will often contain five questions, although the number can vary by chapter.

### Step 3: Modify the selected questions

The first draft is a candidate pool, not the final quiz. During revision:

- sharpen vague stems;
- make the correct answer express the chapter's actual point;
- replace “why is this important?” wording with recognition of the chapter's example or claim;
- remove accidental application or calculation;
- clarify any pronouns, dates, names, or comparisons;
- ensure that only one option is defensible; and
- keep the question readable without making it obvious.

The user may ask a question to emphasize a particular point. For example, a question about housing can be revised from a broad NIMBYism definition to the more important reading check: **who benefits from restricted housing, and who pays for it?**

### Step 4: Perform the quality-control pass

Before packaging, check every item against the following standards.

#### Content and scope

- Does the answer come directly from the chapter?
- Is this primarily a reading-recall question?
- Does it avoid novel scenarios, calculations, and comparative statics unless the chapter itself made that exact detail memorable?
- Does it test something worth remembering from the chapter rather than a minor sentence?
- Does it duplicate another item too closely?

#### Answer quality

- Are there exactly four options?
- Is exactly one option clearly correct?
- Are the distractors plausible to a student who skimmed or misunderstood the chapter?
- Are all options in the same conceptual category and grammatical form?
- Do the distractors avoid being silly, obviously false, or unrelated?

#### Test-taking cues

- Are correct-answer positions varied and reasonably balanced?
- Has the answer order been randomized intentionally?
- Is the correct answer always the longest, most qualified, or most specific option?
- Do punctuation, capitalization, or wording patterns reveal the answer?
- Does the stem itself accidentally give away the answer?

The longest-answer check is especially important. Correct answers often need more qualification than distractors, so they can become visibly longer. After writing the items, compare option lengths and revise distractors or the correct answer so length is not functioning as a clue. The goal is not mathematical equality; the goal is that the correct answer is not predictably the longest answer.

## 4. What the final question format is

The default item is:

- single-answer multiple choice;
- exactly four choices labeled A, B, C, and D;
- one point;
- one defensible correct answer; and
- no platform-side answer shuffling after the answer positions have been deliberately randomized.

This keeps the quizzes easy to import, easy to answer, and easy to score. More complicated question types can be useful elsewhere, but basic single-answer items are the most reliable route for this reading-check workflow.

## 5. Why the package is Canvas-shaped QTI

Top Hat's import route expects a **QTI package in the form of a standard Canvas export**, not simply one standalone QTI XML file.

This distinction matters. A bare IMS QTI file may be valid XML and still fail to import because the platform is looking for a Common Cartridge-style package with a manifest, resource relationships, Canvas metadata, and expected file paths.

There are two different Top Hat pathways to keep separate:

- **Question import:** Top Hat's educator import tool accepts a file, scans it, and creates questions in the course. The current support page says that QTI import is for classic, single-correct multiple-choice questions and requires a `.zip` in QTI 1.1.3 format. See [Top Hat's Question Upload guide](https://support.tophat.com/article/Educator-Question-Import).
- **LMS integration:** Top Hat's Canvas and other LMS integrations handle course launch, roster synchronization, grade synchronization, and—under LTI 1.3—deep links to Top Hat content. They do not turn Top Hat into a general-purpose question-authoring API. See [Top Hat's LMS integration overview](https://tophat.com/features/integrations/).

In this workflow, the QTI package is therefore the bridge between question writing and Top Hat. As of October 26, 2026, there is no Top Hat connector exposed in this ChatGPT workspace that would let the assistant create, edit, or assign Top Hat questions directly. The assistant can prepare, validate, and revise the import package; a person still performs the final Top Hat import and preview.

The working approach is therefore:

1. create the Canvas-export-shaped QTI assessment XML used by this workflow;
2. place it inside a Canvas/Common Cartridge-style directory structure;
3. include the manifest and Canvas metadata;
4. zip the contents with the manifest at the root; and
5. upload the resulting `.zip` through Top Hat's question-import route.

**Version note:** Top Hat's public help currently labels its accepted QTI import as version 1.1.3, while Canvas-export packages and the XML namespace used in this workflow are commonly described as QTI 1.2. Do not treat those labels as interchangeable. When Top Hat changes its importer—or when an import fails—test a one-question package against the current Top Hat documentation and update the package builder and this guide together.

## 6. Required QTI package structure

The ZIP should have this basic structure:

```text
imsmanifest.xml
chapter12_factor_markets/
    assessment_meta.xml
    assessment_qti.xml
    chapter12_factor_markets.xml
non_cc_assessments/
    chapter12_factor_markets.xml.qti
course_settings/
    canvas_export.txt
```

The folder and assessment names can change by chapter, but the relationships among the files must remain consistent.

### `imsmanifest.xml`

The manifest is the package's map. It should:

- declare the IMS Common Cartridge namespace;
- include `<organizations />`;
- define an assessment resource with type `imsqti_xmlv1p2`;
- point that resource to the main QTI XML file;
- define an associated-content metadata resource; and
- declare the dependency between the assessment and its metadata resource.

The manifest's file paths must match the ZIP paths exactly. A mismatch between a manifest path and an actual filename can cause an otherwise valid package to fail.

### Assessment metadata

The Canvas-style metadata file identifies the assessment and its settings. It should include:

- the assessment identifier;
- the quiz title;
- the total number of points;
- one allowed attempt, unless a different setting is intentionally requested; and
- the assessment's answer-shuffling and navigation settings.

The total points should equal the number of one-point questions.

### QTI assessment XML

The main assessment in the current Canvas-export-shaped package uses this QTI namespace:

```xml
http://www.imsglobal.org/xsd/imsqtiasiv1p2
```

The assessment should include:

- `cc_maxattempts` metadata;
- a root section wrapper;
- a named chapter section containing the items; and
- one item for each quiz question.

The root section wrapper is important for compatibility with the Canvas-style import path.

### QTI item structure

Each question should include:

- a unique item identifier;
- `maxattempts="1"`;
- item metadata declaring `multiple_choice_question`;
- `points_possible` of `1.0`;
- an assessment-question reference identifier;
- a single-cardinality response;
- `rtiming="No"`;
- four response labels; and
- a response-processing rule awarding 100 percent to the correct response.

The response-processing section should use a decimal score variable with a range from 0 to 100. The item metadata handles the one-point Canvas interpretation; the QTI response-processing rule handles correctness.

The response renderer should use:

```xml
<render_choice shuffle="No">
```

Answer positions are randomized during quiz construction and then held fixed in the imported item. This prevents Top Hat from changing the carefully checked option order.

### Duplicate QTI copies

The same assessment XML should appear in the expected assessment folder and in `non_cc_assessments/`. A copy should also be available as `assessment_qti.xml` in the associated-content folder.

The copies should be byte-for-byte identical. Different importers and export conventions inspect different paths, so this redundancy improves compatibility.

### `course_settings/canvas_export.txt`

This file should contain:

```text
common_cartridge
```

It signals the Canvas/Common Cartridge export convention expected by the import workflow.

## 7. Packaging and import procedure

### Build the package

1. Create the chapter-specific directory structure.
2. Write the manifest, metadata, QTI assessment, duplicate QTI copies, and Canvas export marker.
3. Make sure the manifest is at the root of the ZIP.
4. Do not place the entire build folder inside another top-level folder in the ZIP.
5. Name the final file clearly, for example:

   ```text
   econ_chapter12_factor_markets_housing_reading_check_tophat_qti.zip
   ```

### Validate before uploading

The package should be checked programmatically before import:

- the ZIP opens successfully;
- the ZIP has no corrupt entries;
- every manifest path exists;
- the assessment resource has type `imsqti_xmlv1p2`;
- the dependency points to the metadata resource;
- the QTI XML parses successfully;
- the assessment contains the intended number of items;
- each item has exactly four choices;
- every item has exactly one scoring key;
- the answer positions match the intended answer key;
- the duplicate QTI files are identical; and
- the item metadata and response-processing rules are present.

The answer key should also be reviewed independently of the XML. A structurally valid file can still contain a content error if the wrong option was marked correct.

### Upload to Top Hat

Use Top Hat's educator question-import workflow and upload the ZIP package. Top Hat currently documents this route for classic, single-correct multiple-choice questions and QTI 1.1.3 packages; verify the version requirement before each semester. If the course is connected through Canvas, use the institution's Top Hat test or assessment integration rather than the separate textbook-reading integration. The exact label may vary by institution, but the important distinction is that this is a test/question-bank import, not a textbook-content link.

The Canvas connection is optional for creating the questions. It is useful later for course launch, roster sync, deep linking, and grade sync, but it does not replace the question-import step.

After import, spot-check the questions in Top Hat:

1. confirm that all items appeared;
2. confirm that the option text is intact;
3. confirm that one answer is marked correct;
4. confirm that the answer order is the expected order; and
5. preview or take the quiz once before assigning it to students.

## 8. Troubleshooting guide

### “The file is invalid” or the import fails immediately

Check:

- Is the upload a ZIP rather than a standalone XML file?
- Is `imsmanifest.xml` at the ZIP root?
- Is the package actually Canvas/Common Cartridge-shaped?
- Do all manifest paths match the filenames exactly?
- Is the QTI namespace QTI 1.2?
- Are all XML files well formed?

### The package imports but questions are missing

Check:

- whether the assessment resource points to the correct QTI file;
- whether the section and item identifiers are unique;
- whether the duplicate QTI files contain the same assessment; and
- whether the expected `non_cc_assessments` path is present.

### The choices appear but the answer is wrong

Check the response-processing section, not just the visible choice order. The `varequal` response identifier must match the response label containing the intended correct answer.

### The answer choices are unexpectedly shuffled

Check that the imported item uses `shuffle="No"`. If positions were randomized during construction, the platform should not reshuffle them during import or delivery.

### The quiz is too obvious

Return to the content QA pass. Look especially for:

- correct answers that are much longer;
- distractors that are not from the same conceptual neighborhood;
- one option that uses unusually precise or qualified language;
- answer positions that form a visible pattern; and
- a question that asks for the chapter's main point in a way that repeats the answer.

## 9. Recommended recordkeeping

For each chapter, preserve:

1. the source chapter;
2. the ten-question candidate set;
3. the user's selected questions and requested modifications;
4. the final answer key;
5. the validated QTI ZIP; and
6. any Top Hat or Canvas import notes.

Use a descriptive filename that identifies the course, chapter, subject, and platform. Keep the source and the final package together so that a later revision can be traced back to the chapter version used to write it.

## 10. The repeatable standard

The complete process is:

```text
Read the chapter
    ↓
Find the juicy, memorable reading material
    ↓
Write 10 direct-recall candidates
    ↓
Select the best questions
    ↓
Revise for clarity and centrality
    ↓
Check distractors, answer positions, and answer lengths
    ↓
Build Canvas-export QTI 1.2 package
    ↓
Validate XML, manifest, scoring, and ZIP paths
    ↓
Import into Top Hat
    ↓
Preview before assigning
```

The goal is a quiz that is modest in scope but high in fidelity: students should be able to answer because they read the chapter, not because they guessed the test-writer's pattern or solved a problem that was never the point of the reading.
