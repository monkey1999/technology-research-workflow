# Primary-report fit contract

The primary report is a technical survey. It exists to improve the reader's
understanding of the field, not to display the research workflow.

## Output separation

| Surface | Reader need | Content |
| --- | --- | --- |
| `REPORT.md` | Understand mechanisms, evidence, route differences, boundaries, and the current state of the field | Continuous technical synthesis, decisive experiments, analytical visuals, and conclusions |
| `EXECUTIVE_BRIEF.md` | Orient a technical lead in minutes | Core judgment, route choices, near-term action, and evidence that would change the judgment |
| `EVIDENCE_ATLAS.md` | Audit or reuse the research | Experiment cards, full comparison matrices, extraction notes, conflicts, and unresolved gaps |
| `validation/` | Control release quality | Search, provenance, review, hashes, render checks, and gate results |

Do not solve overload by duplicating the same prose across all three reader
surfaces. The brief compresses; the atlas expands; the report synthesizes.

## Main-report exclusions

Keep these out of `REPORT.md`:

- search logs, source IDs, claim IDs, evidence ledgers, and artifact hashes;
- sections explaining how evidence entered the report or how a judgment was adjudicated;
- gate status, protected-baseline checks, review results, and workflow recovery;
- complete study cards, full extraction tables, and project-management checklists;
- detailed confirmation-test governance unless experimental design is the research topic.

## Reader-fit tests

A primary report passes only when all are true:

1. The opening identifies the technical problem and present state without
   narrating the workflow.
2. Every major section answers one technical question and adds a non-duplicate
   conclusion.
3. Representative experiments are selected because they discriminate between
   explanations or routes, not because every retrieved source needs a paragraph.
4. Limitations sit beside the conclusion they constrain and are not repeated as
   a defensive refrain throughout later sections.
5. Every figure contributes direct evidence, synthesis, or comparison. Choose
   source figures and redrawn figures by information value, traceability,
   legibility, and reuse conditions rather than by a fixed ratio.
6. A professional reader can explain the field map, strongest evidence, main
   disagreement, and practical boundary after a continuous read.

## Compression pass

Before review, read only `REPORT.md` and remove or move any paragraph that does
not change mechanism understanding, evidence interpretation, route comparison,
or the final technical judgment. When detail interrupts the main argument or
creates repetition, move study records to `EVIDENCE_ATLAS.md`; do not use a
fixed character target, shrink fonts, or compress prose into dense tables.

## Negative benchmark

A long report with abundant citations, tables, and figures still fails when its
primary organizing logic is evidence adjudication, investment gates, or review
procedure. Quantity gates protect against thin reports; they never override a
report-type or reader-fit failure.
