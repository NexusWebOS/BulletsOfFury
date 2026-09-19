$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$gen='C:/Users/Mike/.codex/generated_images/01a092a0-0744-71b1-8d8d-c95ab7f90646'
$dest=Join-Path $PSScriptRoot 'assets'
function Sheet($name,$file,$cols,$rows,$names){
 Copy-Item (Join-Path $gen $file) (Join-Path $PSScriptRoot "sources/$name.png")
 $b=[Drawing.Bitmap]::new((Join-Path $gen $file));$w=[int]($b.Width/$cols);$h=[int]($b.Height/$rows)
 for($i=0;$i -lt $names.Count;$i++){$r=[Drawing.Rectangle]::new(($i%$cols)*$w,[int][Math]::Floor($i/$cols)*$h,$w,$h);$c=$b.Clone($r,[Drawing.Imaging.PixelFormat]::Format32bppArgb);$c.Save((Join-Path $dest ($names[$i]+'.png')));$c.Dispose()};$b.Dispose()
}
Sheet 'jet-parts' 'exec-226f9c4f-c282-488e-8e6a-70b8c75ac819.png' 2 2 @('jet','jet-damaged','turret','missile')
Sheet 'weather' 'exec-05a1e694-7de2-4a8f-aad1-5b13d1917346.png' 3 2 @('cloud','storm','lightning','rain','smoke','fire')
Copy-Item (Join-Path $gen 'exec-96b8bf68-c133-4410-b35b-0153479dcdf7.png') (Join-Path $dest 'sky.png')
$src='C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'
$atlas=[Drawing.Bitmap]::new((Join-Path $src 'assets/game/atlas/fx_explosions.png'))
for($i=0;$i -lt 8;$i++){$c=$atlas.Clone([Drawing.Rectangle]::new((637+258*$i),403,256,256),[Drawing.Imaging.PixelFormat]::Format32bppArgb);$c.Save((Join-Path $dest "explosion-$i.png"));$c.Dispose()};$atlas.Dispose()
Copy-Item (Join-Path $src 'assets/game/ships_v2/ship_yuri_v2_hero.png') (Join-Path $dest 'player.png')
foreach($n in @('explosion_jet_breakup','explosion_boss_core','reviewed_maverick_helix_release','enemy_machine_shot_heavy','explosion_air_small_01')){Copy-Item (Join-Path $src "assets/game/sounds/$n.mp3") (Join-Path $dest "$n.mp3")}
'Assets extracted'
