$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$captureRoot = [IO.Path]::GetFullPath((Join-Path $projectRoot '_shots\boss_comparison_1102'))
$archiveRoot = [IO.Path]::GetFullPath('D:\BOF-Downloads\2026-10-31\current\boss-comparison-1102-media')
New-Item -ItemType Directory -Path $archiveRoot -Force | Out-Null
foreach ($difficulty in @('normal', 'hard', 'furious')) {
    $stateFile = Join-Path $captureRoot "$difficulty\batch.json"
    if (!(Test-Path -LiteralPath $stateFile)) { continue }
    $state = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
    foreach ($property in $state.jobs.PSObject.Properties) {
        $job = $property.Value
        if (!$job.passed) { continue }
        $sourcePath = [IO.Path]::GetFullPath((Join-Path $projectRoot $job.folder))
        if (!$sourcePath.StartsWith($captureRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source escapes this recording pass' }
        $item = Get-Item -LiteralPath $sourcePath
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
        if (!(Test-Path -LiteralPath (Join-Path $sourcePath 'report.json'))) { throw 'Missing recording receipt' }
        $targetParent = Join-Path $archiveRoot $difficulty
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
        $targetPath = [IO.Path]::GetFullPath((Join-Path $targetParent $item.Name))
        if (!$targetPath.StartsWith($archiveRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Destination escapes the recording archive' }
        if (Test-Path -LiteralPath $targetPath) { throw "Archive target already exists: $targetPath" }
        Move-Item -LiteralPath $sourcePath -Destination $targetPath
        New-Item -ItemType Junction -Path $sourcePath -Target $targetPath | Out-Null
        Write-Output "Archived $difficulty $($job.id)"
    }
}
# Preserve the two closed, incomplete Retina-pilot takes on D: as iteration
# evidence too. Their replacements have different timestamped directories.
foreach ($difficulty in @('normal', 'hard')) {
    $sourcePath = [IO.Path]::GetFullPath((Join-Path $captureRoot "$difficulty\stage6-rough-riders"))
    if (!$sourcePath.StartsWith($captureRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Iteration source escapes recording root' }
    if (!(Test-Path -LiteralPath $sourcePath)) { continue }
    $item = Get-Item -LiteralPath $sourcePath
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
    $receipt = Get-Content -LiteralPath (Join-Path $sourcePath 'report.json') -Raw | ConvertFrom-Json
    if ($receipt.reason -ne 'recording time limit' -or !$receipt.sourceStable) { continue }
    $targetPath = [IO.Path]::GetFullPath((Join-Path $archiveRoot "$difficulty\stage6-rough-riders"))
    if (!$targetPath.StartsWith($archiveRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Iteration destination escapes archive' }
    if (Test-Path -LiteralPath $targetPath) { throw 'Iteration archive already exists' }
    Move-Item -LiteralPath $sourcePath -Destination $targetPath
    New-Item -ItemType Junction -Path $sourcePath -Target $targetPath | Out-Null
    Write-Output "Archived closed $difficulty Retina-pilot iteration"
}
