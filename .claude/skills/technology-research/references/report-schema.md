# Reader-facing report schema

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

## Argument unit

Build paragraphs and subsections from this sequence:

```text
reader question → mechanism → representative evidence → boundary or conflict
→ comparison → engineering meaning → judgment
```

Do not force every unit into a visible heading. The report should read as one
argument whose sections advance the reader's understanding.

## Visuals

Prefer one to four visuals when evidence supports them:

- a mechanism or system-boundary diagram;
- a technology-route comparison table;
- a plot reconstructed from verified quantitative data;
- an engineering maturity or deployment roadmap.

Every figure needs a caption, provenance, units where relevant, and an explicit
statement of what the reader should learn from it. Keep copyright-protected
source figures out of the package unless reuse is authorized.

