$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root='C:/Users/Mike/.codex/generated_images/01a092a0-0744-71b1-8d8d-c95ab7f90646'
$ship=Join-Path $root 'exec-c74a532b-bfaf-44ac-adc0-3980fad15e7d.png'
$fx=Join-Path $root 'exec-28717fb1-6f31-4925-b415-c054538ee782.png'
Copy-Item $ship (Join-Path $PSScriptRoot 'sources/interceptor-v2.png')
Copy-Item $fx (Join-Path $PSScriptRoot 'sources/interceptor-projectiles.png')
$b=[Drawing.Bitmap]::new($ship);$half=[int]($b.Width/2)
for($i=0;$i -lt 2;$i++){$c=$b.Clone([Drawing.Rectangle]::new(($i*$half+40),40,807,700),[Drawing.Imaging.PixelFormat]::Format32bppArgb);$n=if($i -eq 0){'interceptor'}else{'interceptor-damaged'};$c.Save((Join-Path $PSScriptRoot "assets/$n.png"));$c.Dispose()};$b.Dispose()
$b=[Drawing.Bitmap]::new($fx);$w=[int]($b.Width/2);$h=[int]($b.Height/2);$names=@('laser-beam','plasma-bolt','laser-charge','needle-missile')
for($i=0;$i -lt 4;$i++){$c=$b.Clone([Drawing.Rectangle]::new(($i%2*$w),([int][Math]::Floor($i/2)*$h),$w,$h),[Drawing.Imaging.PixelFormat]::Format32bppArgb);if($i -eq 0){$t=$c.Clone([Drawing.Rectangle]::new(190,5,240,($h-10)),[Drawing.Imaging.PixelFormat]::Format32bppArgb);$c.Dispose();$c=$t};$c.Save((Join-Path $PSScriptRoot ('assets/'+$names[$i]+'.png')));$c.Dispose()};$b.Dispose()
