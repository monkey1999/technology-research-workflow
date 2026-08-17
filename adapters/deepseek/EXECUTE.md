# DeepSeek Harness execution contract

请在当前 workspace 中执行一次完整技术调研，运行目录为 `runs/<run-name>`。

执行要求：

1. 完整读取 `.agents/skills/technology-research/SKILL.md` 及其直接引用的规则和模板。
2. 读取 `runs/<run-name>/request.yaml`，把读者需要作出的决策拆成问题树；不要把检索词列表当作研究计划。
3. 检索并核对学术论文、期刊/会议论文、官方标准、工程资料和可靠产业资料。严格遵守排除范围；如果排除了 patents，不得在来源、论断或正文中加入专利材料。
4. 将来源和论断写入后台 `sources.jsonl`、`claims.jsonl`，并填写 `experiment-matrix.csv`、`data-points.csv` 和 `visual-plan.json`。决定性论断必须有全文或官方文本证据、成立条件、适用边界和反证处理。
5. 在写正文前实际执行：

   `./researchctl.ps1 verify --run runs/<run-name> --stage evidence`

   若失败，修复证据问题后重跑，不得绕过门禁。
6. 写 `REPORT.md`、`EXECUTIVE_BRIEF.md` 和 `EVIDENCE_ATLAS.md`。主报告必须是面向专业读者的技术领域调研报告，以“机制 → 实验证据 → 边界 → 路线比较 → 工程判断”连续论证；逐实验卡、证据推导、完整缺口和验证治理下沉到证据图谱。不得把投资门、审查门、检索日志或工作流写进主报告。
7. 博士级配置下，实际产出不少于配置数量的证据图和分析表，并覆盖机制、定量比较、路线/成熟度。每张图写入 `figures/figure-register.jsonl`，登记角色、呈现方式、读者问题、信息增益、来源和数据文件。论文原图可作为直接实验证据，不设占比限制；必须标明来源、定位、复用状态和适用边界。仅在跨来源综合或可追溯重绘确实提高理解时重新绘图，不得制作无数据支撑的装饰图或证据门流程图。
8. 主报告完成后先实际执行 `./researchctl.ps1 render --run runs/<run-name>`。检查最终 HTML 的桌面、窄屏和打印布局，确认图、表、公式、单位、图注可读。
9. 渲染后委派两个使用不同新上下文的审阅任务。技术审阅者检查技术事实、证据匹配、综合论证和全部渲染图表；读者编辑检查报告类型、连续阅读、重复、信息过载和图表信息增益。两者都必须完整读取 `.agents/skills/technology-research-review/SKILL.md`，分别写 `validation/report-review.md` 和 `validation/reader-review.md`，并把最终 `REPORT.md` 与 `REPORT.html` 的 SHA-256 写入审阅 JSON。主写作者不得自行冒充任一审阅者。
10. 修复所有 blocker 和 major finding 后重新渲染，并在两个新上下文中重新完成技术与读者审阅。然后实际执行：

    `./researchctl.ps1 verify --run runs/<run-name> --stage release`

    `./researchctl.ps1 package --run runs/<run-name>`

最终只报告：主报告、执行摘要、证据图谱、HTML、PDF（如生成）与打包文件路径，正文字符数、正文引用数、图数、表数、发布状态、已披露限制和未生成 PDF 的具体原因。博士级门禁通过后的状态只能是 `candidate_for_human_acceptance`，不要用“流程已完成”代替对报告质量的说明。
