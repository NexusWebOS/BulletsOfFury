[CmdletBinding(SupportsShouldProcess=$true)]
param([string]$Destination)
$ErrorActionPreference = 'Stop'
$packRoot = [IO.Path]::GetFullPath($PSScriptRoot)
if (-not $Destination) {
    $codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
    $Destination = Join-Path $codexRoot 'skills'
}
$targetRoot = [IO.Path]::GetFullPath($Destination)
$manifest = Get-Content -LiteralPath (Join-Path $packRoot 'manifest.json') -Raw | ConvertFrom-Json
if ($manifest.format -ne 1 -or @($manifest.skills).Count -eq 0) { throw 'Invalid skill manifest.' }
function Assert-ChildPath([string]$Root, [string]$Candidate) {
    $base = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    $full = [IO.Path]::GetFullPath($Candidate)
    if (-not $full.StartsWith($base, [StringComparison]::OrdinalIgnoreCase)) { throw "Path leaves expected folder: $Candidate" }
    return $full
}
function Get-Sha256([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $algorithm.Dispose(); $stream.Dispose() }
}
# Verify every payload byte before changing any installed skill.
foreach ($entry in $manifest.files) {
    $source = Assert-ChildPath $packRoot (Join-Path $packRoot $entry.path)
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing pack file: $($entry.path)" }
    $actual = Get-Sha256 $source
    if ($actual -ne $entry.sha256 -or (Get-Item -LiteralPath $source).Length -ne $entry.bytes) { throw "Damaged pack file: $($entry.path)" }
}
if (Test-Path -LiteralPath $targetRoot) {
    if ((Get-Item -LiteralPath $targetRoot).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Choose a skill folder that is not a junction or link.' }
}
$backupRoot = Join-Path (Split-Path $targetRoot -Parent) ('skill-backups\animation-' + (Get-Date -Format 'yyyyMMdd-HHmmss-ffff'))
foreach ($name in $manifest.skills) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') { throw "Invalid skill name: $name" }
    $source = Assert-ChildPath (Join-Path $packRoot 'skills') (Join-Path $packRoot "skills\$name")
    $target = Assert-ChildPath $targetRoot (Join-Path $targetRoot $name)
    if ($target -eq $source) { throw 'Install from the downloaded pack, outside the destination skills folder.' }
    if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) { throw "Missing skill entry point: $name" }
    if (Test-Path -LiteralPath $target) {
        if ((Get-Item -LiteralPath $target).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Installed skill is a link: $name" }
    }
    if ($PSCmdlet.ShouldProcess($target, 'Install animation skill, backing up an existing version')) {
        New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
        $saved = $null
        if (Test-Path -LiteralPath $target) {
            New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
            $saved = Assert-ChildPath $backupRoot (Join-Path $backupRoot $name)
            Move-Item -LiteralPath $target -Destination $saved
        }
        try {
            Copy-Item -LiteralPath $source -Destination $target -Recurse
            foreach ($entry in $manifest.files | Where-Object { $_.path.StartsWith("skills/$name/") }) {
                $relative = $entry.path.Substring(('skills/' + $name + '/').Length)
                $installed = Assert-ChildPath $target (Join-Path $target $relative)
                if ((Get-Sha256 $installed) -ne $entry.sha256) { throw "Installed file verification failed: $name/$relative" }
            }
        } catch {
            # Preserve a partial copy for inspection; restore the previous version.
            if (Test-Path -LiteralPath $target) {
                New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
                $failed = Assert-ChildPath $backupRoot (Join-Path $backupRoot ($name + '-incomplete'))
                Move-Item -LiteralPath $target -Destination $failed
            }
            if ($saved) { Move-Item -LiteralPath $saved -Destination $target }
            throw
        }
        Write-Host "Installed $name"
    }
}
if (-not $WhatIfPreference) {
    Write-Host "Installed $(@($manifest.skills).Count) animation skills in $targetRoot"
    if (Test-Path -LiteralPath $backupRoot) { Write-Host "Previous versions preserved in $backupRoot" }
    Write-Host 'Restart Codex or open a new chat. For local cleanup scripts, run Setup-Animation-Tools.cmd.'
}
