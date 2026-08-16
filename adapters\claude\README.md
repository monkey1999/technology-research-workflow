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

After the draft and evidence-bearing visuals exist, render `REPORT.html` first.
Then start a fresh review context or delegate a reviewer, invoke
`/technology-research-review`, and bind the review to the final Markdown and
HTML hashes before the release gate.
