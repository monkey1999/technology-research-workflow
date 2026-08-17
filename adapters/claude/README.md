# Claude Code adapter

Run the installer to expose both the main research skill and the independent
review skill:

```powershell
.\install.ps1 -Scope Project
```

Invoke with:

```text
/technology-research
```

After the report, brief, atlas, and evidence-bearing visuals exist, render
`REPORT.html` first. Then use two distinct fresh contexts with
`/technology-research-review`: one technical reviewer and one reader editor.
Bind both reviews to the final Markdown and HTML hashes before the release gate.
