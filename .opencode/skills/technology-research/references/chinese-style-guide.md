# Chinese professional report style

## Voice

Write like an engineer or researcher explaining a field to another professional.
Prefer connected paragraphs, concrete verbs, conditions, quantities, and causal
links. The reader should understand both the judgment and why it follows.

## Narrative rules

- Open sections with the question or judgment, then explain mechanism and
  evidence.
- Group studies by the technical point they establish; never summarize one
  source after another.
- Explain disagreements through differences in material, device, protocol,
  scale, metric, or deployment condition.
- Put uncertainty beside the affected conclusion.
- Use lists for genuinely enumerable items and tables for repeated comparisons;
  otherwise use prose.
- Use normal citations such as `[Novais et al., 2016](https://...)` near the
  supported statement. Keep workflow IDs backstage.

## Remove during editing

- empty openings such as “随着……不断发展” and “本文将全面介绍”；
- unsupported praise such as “意义重大”“前景广阔”；
- repetitive “首先、其次、此外、最后”；
- mechanical contrast patterns repeated across paragraphs；
- paragraph-length lists disguised as prose；
- source inventories, company inventories, and repeated section conclusions；
- headings that explain “证据如何进入正文”“如何裁决” or “门禁如何通过”；
- repeated defensive sentences built around “不能、尚未、缺乏” when one
  consolidated boundary statement would be clearer；
- slide-like verdict cards and colored-box diagrams that do not carry data or
  technical relationships；
- “研究表明” without naming the condition, result, and source；
- claims that turn “未检索到” into “不存在”。

## Final prose pass

1. Read only the report, without plans or ledgers.
2. Mark the central judgment of every section.
3. Remove any paragraph that does not advance mechanism, evidence, boundary,
   comparison, or decision.
4. Merge repeated qualifications into the sentence they constrain.
5. Confirm that editing preserved technical meaning and citations.
6. Read the first five minutes of the report as the target professional. Verify
   that the field, central disagreement, strongest evidence, and report route
   are already clear.
7. Read the report continuously without the atlas. Move any experiment card,
   evidence derivation, or validation procedure that interrupts the technical
   argument to `EVIDENCE_ATLAS.md`.
