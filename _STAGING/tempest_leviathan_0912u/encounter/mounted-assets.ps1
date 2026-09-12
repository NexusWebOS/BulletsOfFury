$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$source='C:/Users/Mike/.codex/generated_images/01a092a0-0744-71b1-8d8d-c95ab7f90646/exec-66572366-a3b8-49e9-beb9-08126fa659e6.png'
Copy-Item $source (Join-Path $PSScriptRoot 'sources/mounted-turrets.png')
$b=[Drawing.Bitmap]::new($source)
for($i=0;$i -lt 2;$i++){$o=[Drawing.Bitmap]::new(1024,1024);$g=[Drawing.Graphics]::FromImage($o);$r=[Drawing.Rectangle]::new(($i*887),0,887,887);$y=if($i -eq 0){12}else{67};$g.DrawImage($b,[Drawing.Rectangle]::new(68,$y,887,887),$r,[Drawing.GraphicsUnit]::Pixel);$g.Dispose();$name=if($i -eq 0){'turret-mounted'}else{'turret-carriage'};$o.Save((Join-Path $PSScriptRoot "assets/$name.png"));$o.Dispose()};$b.Dispose()
