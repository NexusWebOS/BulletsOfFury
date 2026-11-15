[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$launcher = $null
$launcherArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    try {
        & py -3.12 -c 'import sys; assert sys.version_info[:2] == (3,12)' 2>$null
        if ($LASTEXITCODE -eq 0) { $launcher = 'py'; $launcherArgs = @('-3.12') }
    } catch { $launcher = $null }
}
if (-not $launcher -and (Get-Command python -ErrorAction SilentlyContinue)) {
    try {
        & python -c 'import sys; assert sys.version_info[:2] == (3,12)' 2>$null
        if ($LASTEXITCODE -eq 0) { $launcher = 'python' }
    } catch { $launcher = $null }
}
if (-not $launcher) { throw 'Install Python 3.12 (64 bit), with the Python launcher or Add to PATH selected, then run this again.' }
$venv = Join-Path $PSScriptRoot '.venv'
& $launcher @launcherArgs -m venv $venv
if ($LASTEXITCODE -ne 0) { throw 'Could not create the isolated tools environment.' }
$python = Join-Path $venv 'Scripts\python.exe'
& $python -m pip install --disable-pip-version-check -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Python dependencies could not be installed. Check the connection and error above.' }
& $python (Join-Path $PSScriptRoot 'skills\clean-pixel-effect-gifs\scripts\clean_gif.py') --help | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'The cleanup tool could not start.' }
Write-Host "Cleanup tools ready: $python"
Write-Host 'Keep the downloaded folder. Ask Codex to use this Python for the bundled scripts.'
