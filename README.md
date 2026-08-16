# Technology Research Workflow

面向 Claude Code、OpenCode、Codex 和 DeepSeek Harness 的通用技术调研工作流。它的第一目标是输出专业人员愿意读、能够据此形成判断的调研报告，而不是把检索过程包装成审查报告。

## 交付模型

- `REPORT.md`：主交付物。正文围绕机制、路线、实验结果、边界、工程化和选择建议连续论证。
- `REPORT.html`：单文件离线版，内嵌样式和本地图像，带目录、表格及可点击引用。
- `REPORT.pdf`：环境存在 Pandoc 及可用 PDF 引擎时生成。
- `sources.jsonl`、`claims.jsonl`、`validation/`：后台证据和质量账本，不进入读者正文。
- `experiment-matrix.csv`：逐项保留对象、路线、条件、对照、指标、结果、不确定性、复现和限制，防止把不可比实验强行并列。
- `data-points.csv`、`visual-plan.json`、`figures/figure-register.jsonl`：可追溯定量图表的数据、目的与来源登记。
- `REPORT-package.zip`：报告和可复核材料的完整交付包。

证据账本服务于报告，但不能取代报告。正文不得泄漏内部来源编号、检查清单或检索日志；结论必须说明成立条件和证据边界。

## 快速开始

先编辑 `request.yaml`，至少明确主题、读者、时间边界、研究问题、纳入/排除范围和期望决策。随后执行：

```powershell
cd technology-research-workflow
./researchctl.ps1 doctor
./researchctl.ps1 init --config request.yaml --slug demo-topic
```

如果 Python 已安装但不在 `PATH`，可先把解释器绝对路径写入
`TECH_RESEARCH_PYTHON` 环境变量；脚本也会依次识别 `python`、`python3` 和
Windows `py` launcher。

在目标 Agent 中要求其使用 `technology-research` skill 完成检索、综合和写作。证据准备完成后先运行后台门禁：

```powershell
./researchctl.ps1 verify --run runs/demo-topic --stage evidence
```

正文和证据图表完成后先渲染；独立上下文必须审阅最终 Markdown 和实际 HTML，并把两者哈希写入 `validation/report-review.json`。最后执行发布门禁和交付构建：

```powershell
./researchctl.ps1 render --run runs/demo-topic
## 独立审阅并修订后，如有修改必须重新 render 和 review
./researchctl.ps1 verify --run runs/demo-topic --stage release
./researchctl.ps1 package --run runs/demo-topic
```

`quality_profile: doctoral` 默认要求至少 18,000 个正文非空白字符、20 个正文内证据链接、3 张证据图、3 张分析表、8 条实验矩阵记录、6 个作图数据点、15 篇全文学术来源和 10 篇全文原始研究。它们是防止低质量报告混过门槛的下限，不是“博士级”的充分证明。通过后状态仍是 `candidate_for_human_acceptance`，必须由人作最终接受判断。

## DeepSeek Harness

官方 Web UI 使用启动命令：

```powershell
cd technology-research-workflow
npx @deepseek-ai/dsh web
```

在页面中选择当前仓库作为 workspace，新建任务并粘贴 `adapters/deepseek/EXECUTE.md`。仓库内 `.agents/skills/` 保存了主执行和独立审阅技能副本。具体操作和开发预览兼容性说明见 `adapters/deepseek/README.md`。

## HTML 离线交付

`render` 会把本地 PNG、JPEG、GIF、WebP 和 SVG 转为 data URI，并把 Markdown 表格转换为标准 HTML 表格。因此可单独发送 `REPORT.html`。外部 HTTP 图片、缺失图片或越界路径会让渲染返回失败。博士级报告中的每张图还必须登记来源、数据、图注和生成方式。

## 当前边界

仓库提供报告契约、证据门禁、写作规则、独立审阅、离线渲染和打包。网页搜索、论文数据库访问和模型调用仍由当前 Agent 及其可用工具负责；验证器只能证明结构化规则通过，不能代替专业人员对技术事实和图表的最终判断。
