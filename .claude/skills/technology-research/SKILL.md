---
name: technology-research
description: Produce an evidence-grounded, professional technical survey whose primary deliverable is a readable research report with integrated experiments, quantitative comparisons, figures, tables, engineering boundaries, and decisions. Use for academic, engineering, industry, standards, and maturity research across technical fields; not for patent analysis.
---

# Technology Research

## Objective

Deliver the report a domain expert needs to read. Evidence ledgers and review
records protect that report but are backstage artifacts; they are never the
organizing principle or substitute for the report.

Before starting, read the nearest `request.yaml` and these references:

- `references/report-schema.md`
- `references/evidence-policy.md`
- `references/visual-contract.md`
- `references/reader-fit-contract.md`
- `references/chinese-style-guide.md` for Chinese reports

## Non-negotiable output hierarchy

1. `REPORT.md`: a continuous technical argument that answers the configured
   decisions.
2. `EXECUTIVE_BRIEF.md`: a short technical-lead orientation, derived from but
   not copied from the report.
3. `EVIDENCE_ATLAS.md`: experiment cards, full matrices, conflicts, and
   provenance needed for deeper inspection.
4. `REPORT.html`: the rendered, self-contained report with legible figures and
   tables.
5. `REPORT.pdf`: when the environment supports a PDF engine.
6. Ledgers, matrices, plans, and review files: provenance and release controls.

Never spend the report explaining the workflow. Never present source IDs,
claim IDs, search logs, audit tables, or gate results to the reader.

## Execution

1. Convert the decisions into a question tree about mechanism, competing
   routes, discriminating experiments, performance boundaries, integration,
   alternatives, maturity, and what evidence would change the judgment.
2. Search academic and in-scope engineering, industry, and official sources.
   Search results, aggregators, abstracts, and bibliographies are discovery
   inputs; open and verify decisive primary sources.
3. Record sources and decision-relevant claims in `sources.jsonl` and
   `claims.jsonl`. Populate `experiment-matrix.csv` study by study, retaining
   objects, conditions, reference measurements, uncertainty, replication, and
   limitations. Put plot-ready verified values in `data-points.csv`.
4. Complete `visual-plan.json`. It must cover mechanism, quantitative
   comparison, and route or maturity. Record the reader question, intended
   insight, presentation type, and destination for every visual.
5. Run `researchctl verify --stage evidence`. Fix evidence depth, matrices,
   duplicate-document, and source-quality failures before drafting.
6. Write a short backstage synthesis spine: decisive question → mechanism →
   representative experiments → disagreement or boundary → route comparison →
   engineering meaning → judgment.
7. Design the analytical figures before prose expansion. At least the
   configured number must synthesize multiple sources or reconstruct verified
   quantitative values. Do not use workflow diagrams or evidence gates as
   substitutes for technical figures.
8. Draft `REPORT.md` from the spine and reader-fit contract. Integrate citations into the body beside
   the facts they support. Explain why a metric matters before presenting its
   values. Compare studies only after checking objects, conditions, units, and
   protocols.
9. Draft `EXECUTIVE_BRIEF.md` and `EVIDENCE_ATLAS.md`. Move complete experiment
   cards, derivation records, detailed test governance, and unresolved-source
   notes into the atlas instead of expanding the primary report.
10. Produce evidence-bearing figures and analytical tables. Use
   `scripts/render_evidence_chart.py` for traceable SVG charts when applicable.
   Register every figure in `figures/figure-register.jsonl` with caption,
   provenance, role, presentation, reader question, information gain, source
   IDs, data file, and license/reuse status.
11. Run a scope-aware compression pass. Use body length as a diagnostic only;
    remove repeated conclusions and move detail that interrupts the argument,
    plus audit/process material, backstage.
12. Render `REPORT.html`. Inspect the actual output at desktop, narrower screen,
   and print/PDF layout. Fix clipping, unreadable labels, table overflow,
   missing images, weak captions, and figures that do not advance the argument.
13. Delegate a fresh-context technical review and a different fresh-context
    reader-editor review to `technology-research-review`. Both inspect the final
    Markdown and rendered HTML; the reader editor also judges report-type fit,
    continuity, overload, repetition, and visual information gain.
14. Resolve all blocker and major findings, rerender, and repeat both reviews
    against the revised hashes. Then run `researchctl verify --stage release`
    and package the outputs.

## Doctoral profile

When `quality_profile: doctoral` is configured, the evidence and content minima
in `request.yaml` are hard gates. They include full-text academic depth, primary
research depth, experiment rows, quantitative data points, body citations,
figures, and analytical tables. Body length is recorded but is neither a floor
nor a ceiling. Bibliography links do not count as body citations. A text wall or
a source-rich bibliography cannot pass.

These minima are floors, not targets. Passing them does not prove doctoral
quality; the mechanism–evidence–boundary argument and professional visual
review remain decisive. Heading, process-meta, and synthesis-figure gates help
prevent an evidence-rich audit package from masquerading as the primary survey.
Source-figure share is diagnostic only; reviewers judge every figure by direct
evidence value, information gain, provenance, legibility, and reuse conditions.

## Writing rules

- Lead sections with a technical question or judgment, then establish it.
- Group studies by what they establish, not by publication.
- Put limitations next to the conclusion they constrain.
- Explain conflicts through material, device, protocol, scale, metric, or
  deployment differences.
- Distinguish demonstrated, inferred, proposed, and marketed capabilities in
  prose.
- Prefer paragraphs for reasoning, tables for repeated comparisons, and
  figures for relationships or quantitative patterns.
- Preserve all values, units, formulas, conditions, negative evidence, names,
  citations, and applicability boundaries during style editing.

## Completion

For a doctoral profile, a passing machine gate produces
`candidate_for_human_acceptance`, never an automatic final publication claim.
Report paths, quality metrics, disclosed limitations, and the reason for any
missing format. Do not describe a passing workflow as proof of scientific
correctness.
