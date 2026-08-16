# DeepSeek Harness execution contract

请在当前 workspace 中执行一次完整技术调研，运行目录为 `runs/<run-name>`。

执行要求：

1. 完整读取 `.agents/skills/technology-research/SKILL.md` 及其直接引用的规则和模板。
2. 读取 `runs/<run-name>/request.yaml`，把读者需要作出的决策拆成问题树；不要把检索词列表当作研究计划。
3. 检索并核对学术论文、期刊/会议论文、官方标准、工程资料和可靠产业资料。严格遵守排除范围；如果排除了 patents，不得在来源、论断或正文中加入专利材料。
4. 将来源和论断写入后台 `sources.jsonl`、`claims.jsonl`。决定性论断必须有全文或官方文本证据、成立条件、适用边界和反证处理。
5. 在写正文前实际执行：

   `./researchctl.ps1 verify --run runs/<run-name> --stage evidence`

   若失败，修复证据问题后重跑，不得绕过门禁。
6. 写 `REPORT.md`。它必须是面向专业读者的真实调研报告，以“机制 → 实验证据 → 边界 → 路线比较 → 工程判断”连续论证；不得写成来源逐条摘要、检查清单、检索日志或审查报告。正文用描述性 Markdown 链接引用，不显示内部证据编号。
7. 仅在图表能承载证据或比较关系时制作图表；图注写清数据来源、条件和限制。不得制作无数据支撑的装饰图。
8. 主报告完成后，委派一个独立审阅任务。该任务必须完整读取 `.agents/skills/technology-research-review/SKILL.md`，检查技术事实、证据匹配、可读性、决策价值和图表，并生成 `validation/report-review.md` 与 `validation/report-review.json`。主写作者不得自行冒充独立审阅者。
9. 修复所有 blocker 和 major finding，再实际执行：

   `./researchctl.ps1 verify --run runs/<run-name> --stage release`

10. 发布门禁通过后执行：

    `./researchctl.ps1 render --run runs/<run-name>`

    `./researchctl.ps1 package --run runs/<run-name>`

最终只报告：主报告路径、HTML 路径、打包文件路径、发布状态、已披露限制和未生成 PDF 的具体原因。不要用“流程已完成”代替对报告质量的说明。
