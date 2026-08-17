# Evidence-bearing visual contract

Figures and tables are part of the reasoning, not layout decoration.

## Required roles for the doctoral profile

- **Mechanism**: show the causal chain, observables, cross-sensitivities, and
  system boundary.
- **Quantitative comparison**: plot verified values only when objects,
  conditions, units, and protocols are comparable; otherwise visualize the
  comparability boundary instead of ranking values.
- **Route or maturity**: connect architectures to demonstrated evidence,
  engineering constraints, unresolved tests, and suitable use cases.

Do not count workflow charts, evidence gates, review flows, investment funnels,
or generic colored boxes as technical synthesis figures. A maturity figure is
valid only when its axes, categories, placements, and evidence basis are
explicit.

## Data and provenance

Record reconstructed numeric values in `data-points.csv` with the source,
locator, condition, unit, and uncertainty. Register every report image in
`figures/figure-register.jsonl`:

```json
{"figure_id":"FIG-01","path":"figures/FIG-01.svg","kind":"chart","role":"quantitative_comparison","presentation":"data_reconstruction","destination":"main","reader_question":"What comparison should the reader see?","information_gain":"What becomes clearer than prose or a source screenshot?","caption":"","source_ids":["S-001","S-002"],"data_file":"data-points.csv","license":"author-generated from cited evidence","provenance":"what was derived and how","generated_by":"agent and script/version"}
```

Use a source figure when it is the clearest direct evidence and reuse is
permitted and documented. Use an original schematic or reconstruction only
when it adds explanation or a traceable comparison. Do not redraw merely to
change the source-figure ratio, and do not infer missing values from pixels.

Allowed `presentation` values are `synthesis`, `data_reconstruction`, and
`source_figure`. Quantitative-comparison figures require a local data file.
Every main-report figure records a reader question and information gain. If the
figure does not answer a question better than a paragraph or compact table,
remove it.

## Caption test

Every caption states what is shown, under which conditions, from which sources,
what the reader should learn, and the important comparability limitation.

## Rendered review

Inspect—not merely parse—the final HTML at two useful screen widths and print
layout. Confirm labels, legends, units, formulas, table columns, captions, and
source notes are legible and that no figure is missing, clipped, or internally
overlapping.
