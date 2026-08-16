---
name: technology-research
description: Research a technology domain and produce a readable, evidence-grounded technical landscape and engineering maturity report. Use for technology surveys, literature-and-industry reviews, route comparisons, engineering assessments, and decision-oriented research reports.
---

# Technology Research

## Objective

Produce a professional report that explains the technology, not a research log
or an audit report. Keep source ledgers, claim mappings, validation results, and
review findings in the run directory as backstage material.

Before starting, read:

- `references/report-schema.md`
- `references/chinese-style-guide.md` for Chinese reports
- `references/evidence-policy.md`
- the nearest `request.yaml`

## Workflow

1. Identify the reader's decisions, scope, exclusions, time boundary, and the
   questions the report must answer.
2. Build a question tree around mechanisms, technical routes, demonstrated
   results, performance boundaries, engineering conditions, alternatives, and
   maturity. Do not organize the plan by source type.
3. Search academic, engineering, industry, standards, and other in-scope
   sources. Treat search results and aggregators as discovery inputs only.
4. Record source evidence and important claims in `sources.jsonl` and
   `claims.jsonl`. Run `researchctl verify --stage evidence` before drafting.
5. Create a short synthesis brief that states the argument spine: what problem
   matters, how each route works, what experiments establish, where evidence
   stops, and what this means for engineering decisions.
6. Draft `REPORT.md` from the synthesis brief. Write connected explanation in
   the order mechanism → evidence → boundary → comparison → judgment. Do not
   write source-by-source summaries.
7. Add only evidence-bearing visuals: a mechanism or route map, a comparison
   table, a result plot reconstructed from verified data, or a maturity
   roadmap. Do not add decorative images or search statistics.
8. Cite important facts near the relevant sentence with normal Markdown links.
   Keep internal source and claim IDs out of the reader-facing narrative.
9. Delegate a fresh-context review to `technology-research-review`. If
   delegation is unavailable, perform a separate review pass that reads the
   artifacts without relying on drafting notes. Save review output under
   `validation/` and revise all blocker or major findings.
10. Run `researchctl verify --stage release`, then render and package. Do not
    declare completion when the release check fails.

## Report rules

- Lead with the technical judgment when evidence supports one.
- Explain why a metric matters before comparing values.
- Put limitations beside the conclusion they qualify; do not create a giant
  audit-style limitations dump.
- Distinguish demonstrated, inferred, proposed, and marketed capabilities in
  prose without exposing internal workflow labels.
- Use tables only for real comparison and figures only when they clarify a
  mechanism, quantitative result, route relationship, or timeline.
- Write the main report for a reader who never sees the run directory.

## Protected content

Editing for readability must not change numbers, units, formulas, citations,
proper nouns, experimental conditions, negative findings, uncertainty, or
applicability boundaries.

## Completion

The agent does not choose the final state. `researchctl verify --stage release`
derives it from the evidence gate and independent review:

- `ready`: decision-critical evidence and report quality pass.
- `ready_with_limitations`: the report is useful and remaining gaps do not
  invalidate its main judgments; recovery conditions are explicit backstage.
- `needs_review`: a material technical, source, scope, or writing issue remains.
- `blocked`: required access or evidence is unavailable.

