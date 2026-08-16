$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$skills = @('technology-research', 'technology-research-review')
$platformRoots = @('.claude\skills', '.opencode\skills', '.agents\skills')

foreach ($skillName in $skills) {
    $skill = Join-Path $root "skill\$skillName"
    foreach ($platformRoot in $platformRoots) {
        $target = Join-Path (Get-Location) "$platformRoot\$skillName"
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        Copy-Item -Path (Join-Path $skill '*') -Destination $target -Recurse -Force
        Write-Host "synced: $target"
    }
}
