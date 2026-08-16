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
4. 任务应读取 `.agents/skills/technology-research/SKILL.md`，完成后台证据门禁后再写正文。
5. 主任务完成后，要求 Harness 委派一个不继承正文写作立场的审阅任务，读取 `.agents/skills/technology-research-review/SKILL.md`。
6. 发布门禁、HTML 渲染和打包必须实际执行成功。

不要只输入“生成调研报告”。执行契约明确了主报告、后台账本、独立审阅和停止条件，能降低 Agent 把产物写成资料清单或审查日志的概率。

官方入口：<https://github.com/deepseek-ai/deepseek-harness>
