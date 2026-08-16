param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $root 'cli\researchctl.py'

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw 'Python 3 was not found. Install Python 3.11+ or add it to PATH.'
}

if ($python.Name -eq 'py.exe') {
    & $python.Source -3 $script @Arguments
} else {
    & $python.Source $script @Arguments
}
exit $LASTEXITCODE


