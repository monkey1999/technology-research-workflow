# DeepSeek Harness adapter

本适配器针对官方 `deepseek-ai/deepseek-harness` Web UI。该项目仍处于 developer preview，工作区和插件行为可能发生不兼容变化，因此这里依赖最稳定的两个边界：以本仓库作为 workspace，以及让 Agent 直接读取仓库内的技能和执行契约。

## 启动

```powershell
cd D:\Codes\03_Projects\DBRLaser\technology-research-workflow
npx @deepseek-ai/dsh web
```

打开命令输出的网址（默认通常为 `http://127.0.0.1:3080`），选择上述目录为 workspace。官方说明指出，`dsh` 以启动目录作为默认文件系统位置，但仍需在新 Web UI 中显式选择 workspace。

## 执行

1. 编辑根目录 `request.yaml`。
2. 运行 `./researchctl.ps1 init --config request.yaml --slug <run-name>`。
3. 新建 Harness 任务，粘贴 `adapters/deepseek/EXECUTE.md`，并替换其中的 `<run-name>`。
4. 任务应读取 `.agents/skills/technology-research/SKILL.md`，完成来源、论断、实验矩阵、定量数据和视觉计划的证据门禁后再写正文。
5. 正文完成后先渲染 HTML；只有最终渲染产物存在，才能委派一个不继承正文写作立场的审阅任务，读取 `.agents/skills/technology-research-review/SKILL.md`。
6. 修改正文或图表会使审阅哈希失效，必须重新渲染和重新审阅。最后再执行发布门禁与打包。

不要只输入“生成调研报告”。执行契约明确了主报告优先级、实验与定量账本、强制图表、渲染后审阅和停止条件，能拦截资料清单、审查日志和无图文字墙。

官方入口：<https://github.com/deepseek-ai/deepseek-harness>
