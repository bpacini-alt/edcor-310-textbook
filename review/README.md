# Pull-request review packets

Use this protocol before asking Benjamin to approve a pull request that changes student-facing content or presentation.

## The goal

Benjamin should be able to answer three questions quickly:

1. What changed?
2. Where did it change?
3. What will students actually see after the change?

Do not make him hunt through the whole book or rely on a raw line number.

## Required review packet

Organize the packet by chapter or page. For each meaningful change, include:

- **Location:** chapter and title, section heading, exercise/figure/card title, and the first few words of the affected paragraph when useful.
- **Change type:** added, removed, rewritten, moved, shortened, expanded, or visual/function change.
- **Reason:** one sentence explaining the purpose of the change.
- **Net words:** approximate words added or removed for the affected section, and the total when the change is substantial.
- **Direct preview link:** link to the changed page or section on the deployed preview.

For prose, show a focused before/after comparison:

- **Before:** the old text.
- **After:** the new text.
- **Changes:** an inline red/green diff when practical, with removed text in red/strikethrough and added text in green.
- Preserve enough unchanged context to make the passage understandable.
- Always show meaningful removals; do not describe only what was added.

For visual or interactive changes, show focused before/after screenshots only when they help:

- crop to the changed area when possible;
- show the after image with the changed region highlighted;
- use a full-page screenshot only when layout or navigation is the thing being reviewed;
- keep screenshots as temporary review artifacts or compressed preview assets, not permanent textbook content;
- provide the live preview link as the authoritative rendering.

## Review scale

- **Small PR:** show every meaningful change.
- **Medium PR:** show every meaningful change, grouped by chapter.
- **Large PR:** show every meaningful change in the linked packet, while the PR description summarizes the important decisions by chapter.

Generated files should not receive separate prose explanations when their source change is already documented, unless the generated result visibly differs in a way Benjamin needs to inspect.

## Approval standard

Before requesting approval, confirm:

- the packet includes additions and removals;
- the affected chapters/pages have direct preview links;
- screenshots are included for visual changes and omitted when text comparison is clearer;
- the packet and the rendered preview agree;
- the PR's Files changed tab contains only intended files.

Approval means Benjamin has reviewed both the intellectual/content changes and the rendered student-facing result.
