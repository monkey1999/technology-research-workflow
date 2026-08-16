param(
    [ValidateSet('Project','Global')]
    [string]$Scope = 'Project'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$skills = @('technology-research', 'technology-research-review')

if ($Scope -eq 'Global') {
    $platformRoots = @(
        (Join-Path $env:USERPROFILE '.claude\skills'),
        (Join-Path $env:USERPROFILE '.config\opencode\skills'),
        (Join-Path $env:USERPROFILE '.agents\skills')
    )
} else {
    $platformRoots = @(
        (Join-Path (Get-Location) '.claude\skills'),
        (Join-Path (Get-Location) '.opencode\skills'),
        (Join-Path (Get-Location) '.agents\skills')
    )
}

foreach ($skillName in $skills) {
    $skill = Join-Path $root "skill\$skillName"
    foreach ($platformRoot in $platformRoots) {
        $target = Join-Path $platformRoot $skillName
        New-Item -ItemType Directory -Force -Path $platformRoot | Out-Null
        if (Test-Path -LiteralPath $target) {
            Write-Host "exists, skipped: $target"
            continue
        }
        Copy-Item -LiteralPath $skill -Destination $target -Recurse
        Write-Host "installed: $target"
    }
}
