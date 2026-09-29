$ErrorActionPreference = 'Stop'
$hamaWorkspace = 'C:\Users\Mike\Documents\New project\bof-repair-0927'
$hamaCheckout = 'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury'
$hamaDirectories = @('assets\game\hama_art_0928', '_ART_SOURCES\hama_art_0928', '_BUILD_SOURCE\hama_art_0928')
foreach ($hamaRelativeDirectory in $hamaDirectories) {
    $hamaSourceDirectory = Join-Path $hamaWorkspace $hamaRelativeDirectory
    $hamaTargetDirectory = Join-Path $hamaCheckout $hamaRelativeDirectory
    foreach ($hamaFile in Get-ChildItem -LiteralPath $hamaSourceDirectory -Recurse -File) {
        $hamaRelativeFile = $hamaFile.FullName.Substring($hamaSourceDirectory.Length).TrimStart('\')
        $hamaTargetFile = Join-Path $hamaTargetDirectory $hamaRelativeFile
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $hamaTargetFile) | Out-Null
        Copy-Item -LiteralPath $hamaFile.FullName -Destination $hamaTargetFile -Force
        if ((Get-FileHash -LiteralPath $hamaFile.FullName -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $hamaTargetFile -Algorithm SHA256).Hash) {
            throw "Hama art copy mismatch: $hamaRelativeFile"
        }
    }
}
Write-Output 'Copied and hash-verified only the three hama_art_0928 art directories.'
