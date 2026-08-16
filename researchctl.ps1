param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $root 'cli\researchctl.py'

$pythonPath = $null
if ($env:TECH_RESEARCH_PYTHON) {
    if (Test-Path -LiteralPath $env:TECH_RESEARCH_PYTHON -PathType Leaf) {
        $pythonPath = (Resolve-Path -LiteralPath $env:TECH_RESEARCH_PYTHON).Path
    } else {
        $pythonCommand = Get-Command $env:TECH_RESEARCH_PYTHON -ErrorAction SilentlyContinue
        if ($pythonCommand) { $pythonPath = $pythonCommand.Source }
    }
}
if (-not $pythonPath) {
    foreach ($candidate in @('python', 'python3', 'py')) {
        $pythonCommand = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($pythonCommand) {
            $pythonPath = $pythonCommand.Source
            break
        }
    }
}
if (-not $pythonPath) {
    throw 'Python 3 was not found. Install Python 3, add it to PATH, or set TECH_RESEARCH_PYTHON to the executable path.'
}

if ([System.IO.Path]::GetFileName($pythonPath) -in @('py', 'py.exe')) {
    & $pythonPath -3 $script @Arguments
} else {
    & $pythonPath $script @Arguments
}
exit $LASTEXITCODE
