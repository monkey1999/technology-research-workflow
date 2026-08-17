---
name: technology-research-review
description: Independently review a completed technical research report and its rendered HTML for scientific integrity, argument quality, decision usefulness, figure and table validity, and professional readability. Use only after drafting and rendering; review files stay backstage.
---

# Technology Research Review

## Objective

Protect the quality of an already written report. Do not turn the report into
an audit artifact and do not excuse weak content because files or gates exist.

Run two reviews in distinct fresh contexts. The technical reviewer reads
`request.yaml`, `REPORT.md`, `REPORT.html`, `sources.jsonl`, `claims.jsonl`,
`experiment-matrix.csv`, `data-points.csv`, `visual-plan.json`,
`figures/figure-register.jsonl`, and the main skill references. The reader
editor reads `request.yaml`, `REPORT.md`, `REPORT.html`, `EXECUTIVE_BRIEF.md`,
`EVIDENCE_ATLAS.md`, the figure register, and the reader-fit contract. Do not
give either reviewer the author's self-assessment.

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
5. **Synthesis**: determine whether the report selects and connects decisive
   experiments, resolves apparent conflicts, and produces conclusions that are
   not source inventories or evidence cards.
6. **Report-type fit**: reject a technical survey whose organizing logic is
   adjudication, investment gates, validation procedure, or workflow reporting.
7. **Reader experience**: read continuously. Test whether a professional can
   orient within five minutes, whether sections add non-duplicate conclusions,
   and whether detail is placed on the correct report, brief, or atlas surface.
   Treat body length and source-figure share as diagnostics only. Report the
   concrete repetition, fragmentation, missing interpretation, provenance, or
   readability problem instead of failing an artifact because of a ratio.

Classify findings as `blocker`, `major`, or `minor`. Give each a stable ID:
`BLK-n`, `MAJ-n`, or `MIN-n`. Never delete a finding to make a gate pass. Mark
it resolved only with concrete evidence and the SHA-256 of the corrected
`REPORT.md`. Any edit after review makes both artifact hashes stale and requires
a new rendered review.

## Output

The technical reviewer writes `validation/report-review.md`. The reader editor
writes `validation/reader-review.md`. Both lead with findings. Consolidate all
findings in `validation/report-review.json`:

```json
{
  "review_version": "0.4",
  "independent": true,
  "reviewers": {
    "technical": {
      "agent": "fresh technical reviewer",
      "session_id": "technical-session-id",
      "fresh_context": true
    },
    "reader_editor": {
      "agent": "fresh reader editor",
      "session_id": "different-reader-session-id",
      "fresh_context": true
    }
  },
  "artifacts": {
    "report_sha256": "sha256 hex of REPORT.md",
    "html_sha256": "sha256 hex of REPORT.html"
  },
  "scientific_review": {"status": "pass"},
  "synthesis_review": {"status": "pass"},
  "narrative_review": {"status": "pass"},
  "visual_review": {
    "status": "pass",
    "viewports": ["1440x1000", "1024x768", "print"],
    "figures_reviewed": 5,
    "tables_reviewed": 5,
    "synthesis_figures_reviewed": 3,
    "quantitative_figures_reviewed": 2
  },
  "report_type_review": {
    "status": "pass",
    "report_type": "technical-survey",
    "primary_report_fit": true,
    "audit_material_backstage": true
  },
  "reader_experience_review": {
    "status": "pass",
    "continuous_reading_pass": true,
    "five_minute_orientation_pass": true
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
The two session identifiers must differ. Any edit invalidates both reviews. The
human reader still decides whether the report is accepted.
