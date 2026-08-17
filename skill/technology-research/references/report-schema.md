# Reader-facing technical-survey schema

The report is a technical narrative, not a completed template. Use the six
chapters below as a default and rename them when a clearer domain-specific title
helps the reader.

1. **摘要与核心判断** — answer the reader's main decision in a few connected
   paragraphs; state conditions and uncertainty next to each judgment.
2. **技术问题与作用机制** — explain the problem, observables, physical or
   computational mechanism, and concept boundaries.
3. **技术路线与关键差异** — organize the field by mechanism and architecture;
   explain why routes differ rather than listing papers or companies.
4. **实验证据、性能与适用边界** — connect representative experiments and
   quantitative results to what is and is not established.
5. **工程化、产业格局与应用选择** — cover integration, reliability, cost,
   standards, supply chain, deployment evidence, alternatives, and maturity in
   the context of concrete use cases.
6. **结论与未来路线** — give decision-relevant conclusions, practical next
   steps, unresolved discriminating tests, and conditions that would change the
   judgment.

End with a normal **参考文献** section containing descriptive Markdown links.
Do not expose claim IDs, source IDs, validation states, or search logs.

The six chapters describe a technical survey, not a technology due-diligence
memo. Engineering and maturity judgment belongs in the report, but investment
gates, evidence-adjudication procedure, full study cards, and detailed test
governance belong in `EVIDENCE_ATLAS.md`.

## Argument unit

Build paragraphs and subsections from this sequence:

```text
reader question → mechanism → representative evidence → boundary or conflict
→ comparison → engineering meaning → judgment
```

Do not force every unit into a visible heading. The report should read as one
argument whose sections advance the reader's understanding.

## Evidence integration

Decision-critical claims must be supported by descriptive Markdown links in
the reader body, not only in the bibliography. The paragraph must give the
experimental object or system, condition, measured quantity, result, and the
boundary relevant to the current judgment. A citation does not repair a vague
sentence.

Populate `experiment-matrix.csv` before synthesis. It is the comparability
surface for study object, route, sensor placement, sample size, test condition,
reference measurement, metric, result, uncertainty, replication, and
limitation. The matrix remains backstage; its findings are rewritten as
connected technical reasoning and analytical tables.

## Visuals

Under the doctoral profile, include at least the configured minimum figures and
tables, covering these evidence roles:

- a mechanism or system-boundary diagram;
- a technology-route comparison table;
- a plot reconstructed from verified quantitative data;
- an engineering maturity or deployment roadmap.

At least the configured number of figures must synthesize two or more sources
when the evidence supports a valid comparison. Source-paper figures are valid
direct evidence for indispensable setups, phenomena, and measured responses;
there is no fixed source-figure ratio. Select each presentation by explanatory
value, traceability, legibility, and reuse conditions.

Every figure needs a caption, provenance, units where relevant, conditions, and
an explicit statement of what the reader should learn and where comparison
stops. Keep copyright-protected source figures out of the package unless reuse
is authorized. A text-only report cannot pass the doctoral profile.

## Depth floor versus quality

Configured source, citation, experiment, data, figure, and table minima are
release floors. Body length is diagnostic, not a release floor or ceiling. Do
not pad or truncate the report to reach a character target. If the field lacks
comparable data for a requested chart, show the comparability boundary and
explain why a ranking would be misleading. Professional judgment, causal
argument, and honest uncertainty remain necessary after every numeric gate
passes.

Use heading-density and reader-review checks to detect fragmentation. When
detail obscures the decisive technical argument, preserve it in the atlas and
rewrite for continuity; do not decide this from body length alone.
