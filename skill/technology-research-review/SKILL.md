---
name: technology-research-review
description: Independently review a completed technology research report for technical integrity, evidence fit, narrative quality, decision usefulness, and rendered readability. Use after a technology-research draft exists and before release.
---

# Technology Research Review

## Objective

Act as an independent professional reader and adversarial technical reviewer.
Review the report without turning it into an audit document. Findings belong in
`validation/`; the reader-facing report remains a technical narrative.

Read:

- `request.yaml`
- `REPORT.md`
- `sources.jsonl`
- `claims.jsonl`
- the main skill's `references/evidence-policy.md`
- the main skill's `references/report-schema.md`
- the rendered `REPORT.html` when present

## Review

1. Check whether the report answers the reader's decisions and explains the
   field through mechanism, evidence, boundary, comparison, and judgment.
2. Challenge decisive scientific, engineering, industry, standards, and
   maturity claims against the recorded evidence and scope.
3. Identify overstatement, source mismatch, missing conditions, absent
   alternatives, and conclusions that rely on search absence.
4. Read the prose as a professional reader. Flag source-by-source summaries,
   list compulsion, repeated conclusions, generic AI phrasing, and sections
   that do not advance the argument.
5. Inspect tables and figures for legibility, provenance, units, and actual
   explanatory value.
6. Classify findings as `blocker`, `major`, or `minor`. Provide the smallest
   revision that resolves each finding.

## Output

Write `validation/report-review.md` with findings first. Write
`validation/report-review.json` in this form:

```json
{
  "independent": true,
  "status": "pass",
  "release_recommendation": "ready",
  "findings": []
}
```

Use `status: fail` when blocker or major findings remain. Allowed release
recommendations are `ready`, `ready_with_limitations`, and `needs_review`.
Never mark a report ready merely because its files, headings, or citations
exist.

