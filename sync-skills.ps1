$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$skill = Join-Path $root 'skill\technology-research'
$targets = @(
    (Join-Path (Get-Location) '.claude\skills\technology-research'),
    (Join-Path (Get-Location) '.opencode\skills\technology-research'),
    (Join-Path (Get-Location) '.agents\skills\technology-research')
)

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item -Path (Join-Path $skill '*') -Destination $target -Recurse -Force
    Write-Host "synced: $target"
}

