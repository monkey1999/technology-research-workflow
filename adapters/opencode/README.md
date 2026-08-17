# OpenCode adapter

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
`REPORT.html`, then run `technology-research-review` in two distinct fresh
contexts: one technical reviewer and one reader editor. Both reviews must bind
to the final Markdown and HTML hashes before the release gate.
