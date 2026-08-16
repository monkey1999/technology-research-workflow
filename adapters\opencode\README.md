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

After the draft and evidence-bearing visuals exist, render `REPORT.html`, then
run `technology-research-review` in a fresh review context. The review must bind
to the final Markdown and HTML hashes before the release gate.
