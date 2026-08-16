# Technology Research Workflow

面向 Claude Code、OpenCode、Codex 和 DeepSeek Harness 的通用技术领域调研报告工作流。

目标不是生成审查日志，而是自动产出专业人员能够直接阅读的技术全景与工程成熟度报告。

## 核心原则

- `REPORT.md` 是第一交付物；证据账本和运行日志属于后台材料。
- 先定义读者需要回答的问题，再组织检索。
- 先形成技术判断，再用学术、工程、产业、标准和可选专利证据支撑判断。
- 正文采用连续论证，不把论文和网页逐条罗列成资料清单。
- 去模板化编辑不能改变数字、单位、公式、引用、技术术语和不确定性。
- 允许 `ready_with_limitations`，不得把证据缺口伪装成确定结论。

## 快速开始

```powershell
cd technology-research-workflow
./researchctl.ps1 doctor
./researchctl.ps1 init --config request.yaml --slug demo-topic
```

然后在目标 Agent 中调用 `technology-research` skill，完成检索、综合和写作。

```text
/technology-research
```

最后执行：

```powershell
./researchctl.ps1 verify --run runs/demo-topic
./researchctl.ps1 render --run runs/demo-topic
./researchctl.ps1 package --run runs/demo-topic
```

`render` 会生成可离线打开的单文件 `REPORT.html`：报告中的本地 PNG、JPEG、GIF、WebP
和 SVG 会被嵌入 HTML，Markdown 表格会转换为标准 HTML 表格，样式也内嵌在文件中。
因此可以直接把 `REPORT.html` 发给别人，不需要额外发送图片目录。若报告引用了缺失的本地
图片或外部 HTTP 图片，渲染命令会报告问题并以失败状态结束，避免产生看似完整但无法离线阅读的报告。

`package` 还会生成 `REPORT-package.zip`，其中包含 HTML、Markdown、证据文件和
`package-manifest.json`，适合需要同时交付报告和可复核材料的场景。

## 当前边界

本仓库提供工作流契约、模板、校验、离线 HTML 渲染和发布打包基础设施；具体网页搜索、论文 API、企业资料和模型调用由当前 Agent 或后续 source adapter 提供。

