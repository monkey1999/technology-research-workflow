# Evidence policy

## Source record

Each source should record at least:

```json
{
  "source_id": "E-ACA-001",
  "source_type": "journal_article",
  "title": "",
  "authors": [],
  "year": 2024,
  "url": "",
  "authority": "primary",
  "as_of": "",
  "locator": "section/table/figure/page",
  "verification_status": "unverified"
}
```

Allowed `verification_status` values:

- `verified`
- `secondary_unverified`
- `unverified`
- `unavailable`

Search snippets, model memory, and another document's bibliography are discovery
inputs, not verified evidence.

## Claim record

Important claims should map to one or more source IDs and state their scope:

```json
{
  "claim_id": "C-ENG-001",
  "claim": "",
  "evidence_ids": ["E-ACA-001"],
  "claim_type": "engineering_boundary",
  "confidence": "medium",
  "counter_evidence": [],
  "scope_limit": ""
}
```

Do not promote metadata, theory, patent text, or marketing claims into
experimental, legal-status, FTO, or deployment facts.


