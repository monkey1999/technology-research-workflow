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

After the draft exists, run `technology-research-review` in a fresh review
context before the release gate.
