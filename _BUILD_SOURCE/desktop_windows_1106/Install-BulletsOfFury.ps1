param([switch]$VerifyOnly)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
Add-Type -AssemblyName System.Net.Http
$bofRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$parts=@(
    @{Name='BulletsOfFury-Setup-2026-11-06-RevF.exe.part1'; Bytes=1950000000; Sha256='a5be8400546b3c0b0c235e809c42972a9717dc804fba36fe034ff9a57ebacdd2'; Url='https://github.com/NexusWebOS/BulletsOfFury/releases/download/bof-windows-2026-11-06-revf/BulletsOfFury-Setup-2026-11-06-RevF.exe.part1'}
    @{Name='BulletsOfFury-Setup-2026-11-06-RevF.exe.part2'; Bytes=1935709224; Sha256='544abbe3a240f121ef73719760c025ead566e0f403771a3169b82dfa922c3b27'; Url='https://github.com/NexusWebOS/BulletsOfFury/releases/download/bof-windows-2026-11-06-revf/BulletsOfFury-Setup-2026-11-06-RevF.exe.part2'}
)
$bofOutput=Join-Path $bofRoot 'BulletsOfFury-Setup-2026-11-06-RevF.exe'
$bofHash='ab019939bc940a79ff41e3333787b08ac532347e71a6e0a6019fe4fff9266d37'
function Get-BofHash([string]$path){
    $stream=[IO.File]::OpenRead($path);$sha=[Security.Cryptography.SHA256]::Create()
    try{return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','').ToLowerInvariant()}
    finally{$stream.Dispose();$sha.Dispose()}
}
function Check-BofFile([string]$path,[long]$size,[string]$hash){
    return [IO.File]::Exists($path) -and ([IO.FileInfo]$path).Length -eq $size -and (Get-BofHash $path) -eq $hash
}
foreach($part in $parts){
    $bofPartPath=Join-Path $bofRoot $part.Name
    if(!(Test-Path -LiteralPath $bofPartPath)){
        if($VerifyOnly){throw "Missing download: $($part.Name)"}
        Write-Host "Downloading $($part.Name)..."
        $bofTemp=$bofPartPath+'.downloading-'+[Guid]::NewGuid().ToString('N')
        $client=[Net.Http.HttpClient]::new();$client.Timeout=[TimeSpan]::FromMinutes(60)
        $response=$null;$inputStream=$null;$outputStream=$null
        try{
            $response=$client.GetAsync($part.Url,[Net.Http.HttpCompletionOption]::ResponseHeadersRead).GetAwaiter().GetResult()
            [void]$response.EnsureSuccessStatusCode()
            $inputStream=$response.Content.ReadAsStreamAsync().GetAwaiter().GetResult()
            $outputStream=[IO.File]::Open($bofTemp,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
            $buffer=New-Object byte[] 4194304;$received=0L;$lastPrint=0L
            while(($count=$inputStream.Read($buffer,0,$buffer.Length)) -gt 0){
                $outputStream.Write($buffer,0,$count);$received+=$count
                if($received-$lastPrint -gt 104857600){Write-Host ([Math]::Round(100*$received/$part.Bytes).ToString()+'%');$lastPrint=$received}
            }
            $outputStream.Dispose();$outputStream=$null
            if(!(Check-BofFile $bofTemp $part.Bytes $part.Sha256)){throw 'The download did not pass verification. Run this helper again.'}
            [IO.File]::Move($bofTemp,$bofPartPath)
        }finally{
            if($outputStream){$outputStream.Dispose()};if($inputStream){$inputStream.Dispose()};if($response){$response.Dispose()};$client.Dispose()
            if(Test-Path -LiteralPath $bofTemp){Remove-Item -LiteralPath $bofTemp}
        }
    }
    if(!(Check-BofFile $bofPartPath $part.Bytes $part.Sha256)){throw "Checksum mismatch in $($part.Name). Move the damaged part away and run this helper again."}
    Write-Host "Verified $($part.Name)"
}
if($VerifyOnly){Write-Host 'Both parts passed verification.';exit 0}
if(Test-Path -LiteralPath $bofOutput){
    if(!(Check-BofFile $bofOutput 3885709224 $bofHash)){throw 'A different setup file already exists here. Move it away before retrying.'}
}else{
    Write-Host 'Joining the complete Bullets of Fury installer...'
    $bofTemp=$bofOutput+'.assembling-'+[Guid]::NewGuid().ToString('N')
    $outputStream=$null
    try{
        $outputStream=[IO.File]::Open($bofTemp,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
        foreach($part in $parts){$inputStream=[IO.File]::OpenRead((Join-Path $bofRoot $part.Name));try{$inputStream.CopyTo($outputStream,4194304)}finally{$inputStream.Dispose()}}
        $outputStream.Dispose();$outputStream=$null
        if(!(Check-BofFile $bofTemp 3885709224 $bofHash)){throw 'The assembled installer did not pass verification.'}
        [IO.File]::Move($bofTemp,$bofOutput)
    }finally{if($outputStream){$outputStream.Dispose()};if(Test-Path -LiteralPath $bofTemp){Remove-Item -LiteralPath $bofTemp}}
}
Write-Host 'Verified. Opening the Fury HQ installer...'
Start-Process -FilePath $bofOutput -ArgumentList '--setup' -WindowStyle Normal -Wait
