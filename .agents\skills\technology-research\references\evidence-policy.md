# Backstage evidence policy

Evidence records protect the report but do not define its prose structure.

## Source record

Use one JSON object per line in `sources.jsonl`:

```json
{
  "source_id": "S-001",
  "source_class": "journal_article",
  "title": "",
  "authors": [],
  "year": 2025,
  "doi": "",
  "canonical_url": "",
  "authority": "primary",
  "verification_level": "full_text_verified",
  "locator": "section, page, figure, table, or paragraph",
  "extracted_evidence": "faithful paraphrase of the supporting passage",
  "accessed_at": "2026-08-16",
  "content_hash": "sha256:..."
}
```

If two records share a content hash but use different canonical URLs, resolve
whether they are genuinely the same document. Use `duplicate_of` only for a
confirmed duplicate; never let one downloaded page stand in for two standards
or papers. An official-text locator must point into the cited document, not a
related-standards list.

Allowed `verification_level` values:

- `metadata_verified`: title, authors, venue, date, and identifier checked.
- `abstract_verified`: abstract read; do not infer unreported methods or values.
- `full_text_verified`: relevant full-text passage, table, or figure checked.
- `official_text_verified`: authoritative standard, regulation, or official
  record checked at the cited locator.
- `secondary_only`: useful secondary account; cannot establish primary
  experimental or legal facts by itself.
- `unavailable`: required evidence could not be accessed.
- `conflict`: metadata or content conflicts with another record.

Search snippets, aggregators, model memory, bibliographies, and news coverage are
discovery inputs. They are not full-text or official evidence.

## Claim record

Use one JSON object per line in `claims.jsonl`:

```json
{
  "claim_id": "C-001",
  "claim": "",
  "importance": "decision_critical",
  "claim_type": "demonstrated_capability",
  "support_type": "direct",
  "evidence_ids": ["S-001", "S-002"],
  "counter_evidence_ids": ["S-003"],
  "conditions": ["cell type", "test protocol"],
  "scope_limit": "",
  "confidence": "medium"
}
```

Decision-critical claims need direct evidence. When the request requires
counter-evidence, record the strongest credible challenge or state why no
testable counter-source exists. An empty array is not evidence of a search.

## Hard boundaries

- Do not label an aggregator or news page as a primary source.
- Do not use metadata to establish experimental values or conclusions.
- Do not use patent text to establish deployment, legal status, or product
  capability.
- When patents are excluded, do not use them anywhere in the report or ledgers.
- Standards and regulatory conclusions require `official_text_verified`.
- “No public case was identified in the searched scope” is not “no case exists.”
- Important numbers require a locator and a source that actually reports them.
- Conflicting metadata, duplicated canonical URLs with different titles, and
  unsupported exclusivity language must be resolved before release.

## Experiment and quantitative ledgers

For each study used in route or performance judgments, populate
`experiment-matrix.csv`. Do not collapse multiple test conditions into one row.
Use `unknown` only after checking the available full text; explain the effect in
`limitations`.

Values used in a plot belong in `data-points.csv`. Record the source ID, exact
locator, unit, condition, and uncertainty. Digitized values must say so in the
locator or uncertainty field and must not imply the precision of an original
data table.
