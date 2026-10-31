# Chapter 16 swap: matching edits in other chapters

**Status:** Ready to do once Mayleigh approves the draft (`chapter16a`). Recorded October 30, 2026, from a sweep of every chapter for ideas the new Chapter 16 covers or contradicts.

Ship these in the same pull request as the swap. If they merge before it, chapters will point to concepts the live Chapter 16 doesn't have yet. Drafted wording is a starting point for Benjamin to edit, not final text.

## Step 0: the swap itself

- [ ] Replace `etb-live/chapter16.html` with the draft's text.
- [ ] Remove `chapter16a.html` (both `etb-live/` and `site/`) and its `DRAFTS` entry in `build/build_site.py`. Ask Benjamin before deleting.
- [ ] Manifest title: "Chapter 16: Agency vs. Determinism" → "Chapter 16: Agency and Self-Belief" (approved October 30).
- [ ] Close PR #64 (concept retitles for the old Chapter 16) as moot, with Benjamin's OK.
- [ ] Rebuild, then check every chapter below on the preview.

## Must fix: these contradict the new chapter

### Chapter 19 (Behaviorism): praise and learned helplessness

Chapter 19 teaches "praise effort, never ability" in three places and gives learned helplessness the old explanation. Chapter 16 now says the praise rule was too simple (Concept 4) and that newer research reverses the old account of helplessness (Concept 3).

- [ ] **"Effective Praise and the 4:1 Ratio" box.** Now: *"…focused on effort and strategy rather than ability. Effort praise ("you kept working on that problem even when it was hard") builds resilience; ability praise ("you're so smart") makes students brittle — they start avoiding challenges that might reveal they're not as smart as advertised."*
  Draft: "…and about the work: what the student did and how. Praise that names something specific tells a student what to do again. (The popular rule "praise effort, never ability" turned out to be too simple; see Chapter 16, Concept 4.)" Keep the 4:1 material and the "Instead of 'Great essay!'" example.
- [ ] **Applications list.** Now: *"Make praise specific and effort-focused. "You kept working on that even when it was hard" builds resilience; "You're so smart" makes students avoid challenges."*
  Draft: "Make praise specific and about the work. Name what the student did that worked. Generic praise becomes wallpaper…"
- [ ] **Synthesis.** Now: *"effort praise before ability praise."* Draft: "specific praise before generic praise."
- [ ] **Learned Helplessness vocab card.** Keep the definition. Replace *"Learned helplessness is not laziness — it is the rational conclusion of repeated experience with uncontrollable outcomes"* with: "Newer research suggests giving up is the brain's default response to bad events it can't control, and what students have to learn is that their actions work (Chapter 16, Concept 3)." Or move it to "Also know."
- [ ] **"Learned helplessness — the dark side of poorly managed consequences" section.** Shrink it to the behaviorist point plus a pointer. Draft: "When consequences arrive no matter what a student does, the student stops trying. Chapter 16 (Concept 3) explains why. The lesson for this chapter: make consequences consistent and tied to what students actually do."
- [ ] **Retrieval question about the student who "stopped raising her hand."** It overlaps Chapter 16's question about the student from a chaotic home. Either cut it, or rewrite the answer around consistent, predictable consequences and point to Chapter 16 for the rest.
- [ ] Optional: the synthesis line *"Learned helplessness is not laziness — it is the rational conclusion of repeated experience"* could get the same light update.

### Chapter 20 (Motivation): growth mindset and autonomy support

- [ ] **Growth Mindset card.** Now: *"Teachers support it through effort praise and process feedback."*
  Draft: "Teachers support it mostly through classroom practice: feedback on strategy, chances to revise, and treating mistakes as information. Lessons that teach the belief directly have small effects (Chapter 16, Concept 4)." Consider moving it to "Also know."
- [ ] **Mastery section.** Now: *"Mastery requires a growth mindset — the belief that ability is developed through effort and strategy."* Draft: "A growth mindset, the belief that ability develops through effort and strategy, can help."
- [ ] **Needs table row.** Now: *"Specific, effort-focused feedback on drafts."* Draft: "Specific feedback on drafts: what to keep and what to change."
- [ ] **Practical autonomy list** ("Give students real control over the 'four T's'" and "Explaining the why"). Trim to a short callback: "Chapter 16 (Concept 6) covers what autonomy support looks like in practice, including why choice works best with structure." Keep the four T's definition in the concept text.
- [ ] **Creative-writing retrieval answer.** Now: *"Undermine — Provide a rigid template that specifies every structural element…"* Chapter 16 shows structure helps when it guides rather than controls. Draft: "Undermine — Specify every structural element and check in so often that the student feels they can't be trusted to work alone. (A model or template isn't the problem by itself; see Chapter 16, Concept 6.)"

### Chapter 22 (Cognitive load): the paradox of choice

Chapter 16's choice-overload misconception box shows that, across 50 experiments, more options made little difference on average (Scheibehenne et al., 2010). Chapter 22 presents the effect as settled.

- [ ] **"The Paradox of Choice — Schwartz and the classroom" box.** Now: *"Barry Schwartz documented a counterintuitive finding: more options do not produce better decisions — they produce anxiety, indecision, and wasted mental energy."*
  Draft: "Psychologist Barry Schwartz popularized the idea that more options produce anxiety and indecision. The evidence is more mixed than the idea's fame suggests: across many experiments, more options made little difference on average (Chapter 16, Concept 6). But choice overload does show up when people know little about what they're choosing, which describes students learning something new." Keep the rest, including "Two or three meaningful options," which matches Chapter 16. Consider retitling it "Choice and cognitive load."
- [ ] **Free-choice project answer.** Now: *"the Paradox of Choice applied to learning… Students who appear unmotivated in this scenario are often experiencing decision paralysis."* Draft: "choice overload, which is most likely when students are new to the material… Students who seem unmotivated may be stuck at the decision, not lazy."

### Chapter 24 (UDL)

- [ ] Now: *"The Paradox of Choice is real: the decision-making process itself consumes working memory…"* Draft: "Choice can add load, especially for students new to the material: deciding how to show what you know takes working memory…"

### Chapter 12 (Social learning): social persuasion row

- [ ] Now: *"Specific, credible encouragement raises efficacy. Generic praise does not. "I think you can solve this because I've seen how you approach problems" works. "You're so smart" does not."*
  Draft: "Specific, credible encouragement raises efficacy more than generic praise, which carries little information. "I think you can solve this because I've seen how you approach problems" gives a student a reason to believe. "You're so smart" gives them very little to go on."

## Should fix: accuracy and references

### Chapter 1: Pygmalion

Chapter 12 already gives the careful version: a real but moderate effect whose size is contested. Chapter 1 overstates it.

- [ ] *"is one of the most replicated results in education research"* → "is one of the best-known results in education research. Its size is debated (Chapter 12 covers the details), but later studies support the direction: expectations matter."
- [ ] *"The Pygmalion Effect has been replicated across demographic groups, school types, and decades."* → "Studies across many kinds of schools have found expectation effects, though usually smaller than the original."
- [ ] Retrieval answer, *"The research is unambiguous: expectations causally shape outcomes…"* → "The research supports this: expectations shape outcomes…"

### Chapter 26

- [ ] A retrieval answer cites *"Chapter 21 — Pygmalion Effect / Expectations."* Pygmalion is in Chapters 1 and 12. Change it to "Chapters 1 and 12."

## Optional: pointers that tie the book together

- [ ] **Chapter 9,** "The Erasure of Agency" misconception: add "(Chapter 16, Concept 2, returns to this question.)"
- [ ] **Chapter 4,** collective teacher efficacy: Chapter 4 already says the 1.57 comes from correlational studies. Add "Chapter 16 looks at which comes first, belief or success."
- [ ] **Chapter 3,** Milgram: add "Chapter 16 returns to one variation of this experiment, where two other 'teachers' refused."
- [ ] **Chapter 8:** *"If helplessness can be learned, can its opposite?"* is a fair account of Seligman's history. If you want a nod to the 2016 reversal, add "(Seligman later concluded the original explanation was backward; see Chapter 16.)"

## Checked and fine as is

- **Chapter 25:** "Growth mindset interventions: strong theory, mixed replication" matches Chapter 16.
- **Chapter 12** Pygmalion box, self-efficacy definition, and four sources all match Chapter 16, as does "Authentic mastery experiences matter more than praise."
- **Chapter 19's** "informational rewards" passage ("praise about specific effort or skill") is consistent.
- **Chapter 4's** "Low self-esteem causes psychological problems" myth, and **Chapter 9's** parenting-style table, are consistent.
- Chapters that the new Chapter 16 points to are all there: Chapter 2 (confabulation, elephant and rider), Chapter 4 (collective efficacy), Chapter 9 (twin studies), Chapter 11 (inquiry), Chapter 12 (self-efficacy, scaffolding), and Chapter 20 (autonomy).
- No chapter refers to the old Chapter 16 by number.
