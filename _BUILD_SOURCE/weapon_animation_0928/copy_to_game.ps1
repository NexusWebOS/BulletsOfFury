$ErrorActionPreference = 'Stop'
$artWorkspace = 'C:\Users\Mike\Documents\New project\bof-repair-0927'
$gameCheckout = 'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury'
$artDirectories = @('assets\game\weapon_animation_0928', '_ART_SOURCES\weapon_animation_0928', '_BUILD_SOURCE\weapon_animation_0928')
foreach ($relativeArtDirectory in $artDirectories) {
    $sourceArtDirectory = Join-Path $artWorkspace $relativeArtDirectory
    $targetArtDirectory = Join-Path $gameCheckout $relativeArtDirectory
    foreach ($artFile in Get-ChildItem -LiteralPath $sourceArtDirectory -Recurse -File) {
        $relativeArtFile = $artFile.FullName.Substring($sourceArtDirectory.Length).TrimStart('\')
        $targetArtFile = Join-Path $targetArtDirectory $relativeArtFile
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetArtFile) | Out-Null
        Copy-Item -LiteralPath $artFile.FullName -Destination $targetArtFile -Force
        if ((Get-FileHash -LiteralPath $artFile.FullName -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $targetArtFile -Algorithm SHA256).Hash) {
            throw "Copied art did not match: $relativeArtFile"
        }
    }
}
Write-Output 'Copied and hash-verified only the three weapon_animation_0928 art directories.'
