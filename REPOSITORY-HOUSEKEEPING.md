# Repository Housekeeping

**Purpose:** Keep the textbook repositories understandable, current, and safe for collaboration between Benjamin, Claude, and ChatGPT.

## Standing responsibility

Repository maintenance is part of the project, not an afterthought. The active state of the books should be easy to identify, and obsolete material should not quietly accumulate until it becomes confusing or dangerous.

The default behavior is:

> Inspect, report, recommend, then act.

## What to monitor

Look periodically for:

- outdated drafts, abandoned experiments, and duplicate files;
- generated files that are no longer produced by the current build;
- orphaned images, audio, PDFs, scripts, and other assets;
- broken links and references to renamed or removed chapters;
- obsolete instructions, configuration, and documentation;
- inconsistent naming, folder structure, or chapter conventions;
- stale branches, issues, and project entries that obscure active work;
- build artifacts or temporary files that do not belong in source control;
- divergence between the published book and the actual source files;
- mismatches between the two textbook repositories that should be intentional and documented.

## Safe cleanup protocol

Before proposing cleanup:

1. Identify the file, branch, issue, or configuration item.
2. Explain why it appears stale, duplicated, orphaned, misplaced, or obsolete.
3. Search for references and dependencies.
4. Check recent commits and recent collaborator activity.
5. Recommend the safest action: keep, move, rename, archive, or delete.
6. Ask Benjamin before deleting files, removing branches, or making any other irreversible change.
7. Record meaningful cleanup decisions when they establish a new convention.

Old does not automatically mean obsolete. Unfamiliar work may have been added by Claude, ChatGPT, or another collaborator and must be investigated before removal.

## What may be fixed proactively

Low-risk, reversible maintenance may be handled as ordinary work when the intent is clear:

- repair broken links;
- correct obvious documentation errors;
- standardize clearly inconsistent names;
- move files that are plainly in the wrong location;
- update instructions that describe an already-confirmed workflow;
- remove accidental temporary artifacts when their origin and lack of value are certain.

When there is meaningful uncertainty, pause and ask.

## Collaboration rules

- Treat GitHub as the source of truth.
- Pull or inspect the current repository state before beginning work.
- Do not overwrite or delete another collaborator's work merely because it is unfamiliar.
- Prefer branches and pull requests for nontrivial changes.
- Keep commits focused and descriptive.
- Avoid creating duplicate versions of the same source file.
- After a structural change, update relevant documentation and links.
- When the two textbook repositories share a convention, keep the corresponding documentation synchronized.

## Maintenance report format

When reporting housekeeping findings, use:

- **Finding:** What appears stale, duplicated, broken, or confusing.
- **Evidence:** What references, history, or build behavior support that judgment.
- **Recommendation:** Keep, move, rename, archive, or delete.
- **Risk:** What could break if the recommendation is wrong.
- **Approval needed:** Whether Benjamin must approve before action.

## Relationship to priorities

Housekeeping should support the priorities document. It should not become a source of busywork. Cleanup is worth doing when it:

- removes friction for students or collaborators;
- prevents build or publishing errors;
- clarifies the current source of truth;
- unlocks a higher-impact feature;
- reduces the chance of losing or misusing existing work.

The goal is not a perfectly empty repository. The goal is a repository in which the important work is easy to find, safe to change, and kept current.
