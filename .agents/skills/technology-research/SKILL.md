---
name: technology-research
description: >
  Research any technology domain and produce a readable, evidence-grounded
  technical landscape and engineering maturity report. Use when the user asks
  for a technology survey, literature-and-industry review, technical landscape,
  engineering assessment, roadmap, or comparable report.
license: MIT
compatibility: Claude Code, OpenCode, Codex, DeepSeek Harness
metadata:
  workflow-version: "0.1.0"
---

# Technology Research

## Primary objective

The primary deliverable is a readable professional report. Evidence ledgers,
search logs, task states, and review records are backstage artifacts. Do not
turn the main report into an audit checklist.

## Required resources

Before drafting, read:

- `references/report-schema.md`
- `references/chinese-style-guide.md` when the report language is Chinese
- `references/evidence-policy.md`

Use the nearest `request.yaml` as the task contract. If it is missing, create
one from `templates/request.yaml` before research begins.

## Workflow

1. Read the request and identify the audience, time boundary, inclusions,
   exclusions, and decisions the reader must make.
2. Build a report-oriented question tree. Do not begin with a list of source
   types or a generic literature-review outline.
3. Search academic, engineering, industry, standards, and optional patent
   sources in parallel. Use primary or authoritative sources where available.
4. Record sources and evidence in the run directory. Every important factual
   or numeric statement in the draft must have a source or an explicit
   unresolved status.
5. Synthesize mechanisms, technology routes, performance boundaries,
   engineering conditions, negative evidence, and contradictions.
6. Draft the report as a continuous argument: question, mechanism, evidence,
   boundary, comparison, and judgment.
7. Apply the professional writing guide. Remove generic AI phrasing, source-by-
   source listing, unnecessary headings, and list compulsion without changing
   the technical meaning.
8. Verify citations, numbers, units, formulas, names, scope, and uncertainty.
9. Render Markdown to HTML and PDF when the tools are available.
10. Review the rendered report as a reader who cannot see the run logs. If the
    reader cannot identify the key judgments and their boundaries, revise the
    report even when the evidence checks pass.

## Report-first rules

- Lead with the conclusion or technical judgment when the evidence allows it.
- Explain why an indicator matters before comparing values.
- Group sources into mechanisms and technology routes; do not summarize papers
  one by one.
- Distinguish demonstrated capability, inferred capability, proposed capability,
  and unverified marketing claims.
- State conditions and boundaries next to the conclusion they qualify.
- Use tables only when they make a comparison easier to read.
- Keep internal evidence IDs out of the main narrative; place the full mapping
  in the evidence appendix.

## Protected content during prose editing

Do not alter numbers, units, formulas, citations, proper nouns, technical terms,
experimental conditions, negative findings, uncertainty, or applicability
boundaries merely to make the prose sound more natural.

## Completion states

- `ready`: required questions answered and key evidence verified.
- `ready_with_limitations`: useful report delivered with explicit gaps and
  recovery conditions.
- `needs_review`: a material scientific or scope judgment remains unresolved.
- `blocked`: required access or evidence is unavailable.

Do not claim full completion when the report is only a source inventory or an
unverified draft.


