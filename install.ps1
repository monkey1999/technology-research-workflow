param(
    [ValidateSet('Project','Global')]
    [string]$Scope = 'Project'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$skill = Join-Path $root 'skill\technology-research'

if ($Scope -eq 'Global') {
    $targets = @(
        (Join-Path $env:USERPROFILE '.claude\skills\technology-research'),
        (Join-Path $env:USERPROFILE '.config\opencode\skills\technology-research'),
        (Join-Path $env:USERPROFILE '.agents\skills\technology-research')
    )
} else {
    $targets = @(
        (Join-Path (Get-Location) '.claude\skills\technology-research'),
        (Join-Path (Get-Location) '.opencode\skills\technology-research'),
        (Join-Path (Get-Location) '.agents\skills\technology-research')
    )
}

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    if (Test-Path -LiteralPath $target) {
        Write-Host "exists, skipped: $target"
        continue
    }
    Copy-Item -LiteralPath $skill -Destination $target -Recurse
    Write-Host "installed: $target"
}


