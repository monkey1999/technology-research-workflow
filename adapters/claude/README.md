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

After the draft exists, start a fresh review context or delegate a reviewer and
invoke `/technology-research-review` before the release gate.
