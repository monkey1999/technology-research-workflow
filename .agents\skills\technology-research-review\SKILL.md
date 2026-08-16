---
name: technology-research-review
description: Independently review a completed technical research report and its rendered HTML for scientific integrity, argument quality, decision usefulness, figure and table validity, and professional readability. Use only after drafting and rendering; review files stay backstage.
---

# Technology Research Review

## Objective

Protect the quality of an already written report. Do not turn the report into
an audit artifact and do not excuse weak content because files or gates exist.

Use a fresh context and read `request.yaml`, `REPORT.md`, `REPORT.html`,
`sources.jsonl`, `claims.jsonl`, `experiment-matrix.csv`, `data-points.csv`,
`visual-plan.json`, `figures/figure-register.jsonl`, and the main skill's
evidence, report, and visual references.

## Review dimensions

1. **Scientific**: challenge mechanisms, decisive claims, reported values,
   experimental comparability, standards statements, alternatives, negative
   evidence, and the step from laboratory evidence to engineering judgment.
2. **Narrative**: determine whether each section advances mechanism → evidence
   → boundary → comparison → judgment. Flag source-by-source summaries,
   generic AI prose, repeated conclusions, list compulsion, and audit language.
3. **Visual**: inspect the rendered HTML at two screen widths and print layout.
   Review every figure and table for legibility, units, provenance, conditions,
   comparability, caption meaning, clipping, and actual explanatory value.
4. **Decision usefulness**: verify that the report answers every configured
   decision and says what evidence would reverse or qualify the conclusion.

Classify findings as `blocker`, `major`, or `minor`. Give each a stable ID:
`BLK-n`, `MAJ-n`, or `MIN-n`. Never delete a finding to make a gate pass. Mark
it resolved only with concrete evidence and the SHA-256 of the corrected
`REPORT.md`. Any edit after review makes both artifact hashes stale and requires
a new rendered review.

## Output

Write `validation/report-review.md` with findings first, followed by passed
checks and residual limitations. Write `validation/report-review.json`:

```json
{
  "review_version": "0.3",
  "independent": true,
  "reviewer": {
    "agent": "fresh reviewer identity",
    "session_id": "non-empty independent session identifier",
    "fresh_context": true
  },
  "artifacts": {
    "report_sha256": "sha256 hex of REPORT.md",
    "html_sha256": "sha256 hex of REPORT.html"
  },
  "scientific_review": {"status": "pass"},
  "narrative_review": {"status": "pass"},
  "visual_review": {
    "status": "pass",
    "viewports": ["1440x1000", "1024x768", "print"],
    "figures_reviewed": 3,
    "tables_reviewed": 3
  },
  "status": "pass",
  "release_recommendation": "candidate_for_human_acceptance",
  "findings": [
    {
      "id": "MAJ-1",
      "severity": "major",
      "status": "resolved",
      "resolution_evidence": "specific correction and verification",
      "resolved_in_report_sha256": "same final REPORT.md hash"
    }
  ]
}
```

Use `status: fail` while blocker or major findings remain. For the doctoral
profile, only `candidate_for_human_acceptance` is a valid passing recommendation.
The human reader still decides whether the report is accepted.
