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

## Data and provenance

Record reconstructed numeric values in `data-points.csv` with the source,
locator, condition, unit, and uncertainty. Register every report image in
`figures/figure-register.jsonl`:

```json
{"figure_id":"FIG-01","path":"figures/FIG-01.svg","kind":"schematic","caption":"","source_ids":["S-001"],"data_file":"","license":"author-generated from cited evidence","provenance":"what was derived and how","generated_by":"agent and script/version"}
```

Do not copy a publisher figure unless reuse is permitted and documented. Prefer
an original schematic or a reconstruction from explicitly cited values.

## Caption test

Every caption states what is shown, under which conditions, from which sources,
what the reader should learn, and the important comparability limitation.

## Rendered review

Inspect—not merely parse—the final HTML at two useful screen widths and print
layout. Confirm labels, legends, units, formulas, table columns, captions, and
source notes are legible and that no figure is missing, clipped, or internally
overlapping.
