$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing.Common,System.Drawing.Primitives,System.Private.Windows.GdiPlus,System.Private.Windows.Core -TypeDefinition @'
using System;using System.Drawing;using System.Drawing.Imaging;
public static class SkyArt {
 public static void Build(string path,string dest){using(var s=new Bitmap(path))using(var half=new Bitmap(512,512)){
 using(var g=Graphics.FromImage(half))g.DrawImage(s,0,0,512,512);
 using(var o=new Bitmap(1024,1024)){for(int y=0;y<1024;y++)for(int x=0;x<1024;x++)o.SetPixel(x,y,half.GetPixel(x<512?x:1023-x,y<512?y:1023-y));o.Save(dest+"/sky-loop.png",ImageFormat.Png);
 string[] names={"day","night","dawn","morning"};float[,] tint={{1,1,1},{.14f,.17f,.34f},{.72f,.38f,.51f},{.83f,.9f,.87f}};
 for(int i=0;i<4;i++)using(var p=new Bitmap(1024,1024)){for(int y=0;y<1024;y++)for(int x=0;x<1024;x++){var c=o.GetPixel(x,y);p.SetPixel(x,y,Color.FromArgb((int)(c.R*tint[i,0]),(int)(c.G*tint[i,1]),(int)(c.B*tint[i,2])));}p.Save(dest+"/sky-"+names[i]+".png",ImageFormat.Png);}
 for(int i=0;i<1024;i++)if(o.GetPixel(i,0)!=o.GetPixel(i,1023)||o.GetPixel(0,i)!=o.GetPixel(1023,i))throw new Exception("Sky seam");
 }} }
}
'@
[SkyArt]::Build((Join-Path $PSScriptRoot 'assets/sky.png'),(Join-Path $PSScriptRoot 'assets'))
$tank=Join-Path $PSScriptRoot '../razor-tank'
$files=Get-ChildItem (Join-Path $tank 'sprites') -Filter '*.png'
$sheet=[Drawing.Bitmap]::new(1000,([int][Math]::Ceiling($files.Count/5)*220));$g=[Drawing.Graphics]::FromImage($sheet);$g.Clear([Drawing.Color]::FromArgb(15,22,28));$font=[Drawing.Font]::new('Consolas',12)
for($i=0;$i -lt $files.Count;$i++){$b=[Drawing.Bitmap]::new($files[$i].FullName);$x=($i%5)*200;$y=[int][Math]::Floor($i/5)*220;$scale=[Math]::Min(180/$b.Width,180/$b.Height);$g.DrawImage($b,[single]($x+100-$b.Width*$scale/2),[single]($y+90-$b.Height*$scale/2),[single]($b.Width*$scale),[single]($b.Height*$scale));$g.DrawString($files[$i].BaseName,$font,[Drawing.Brushes]::White,$x+10,$y+190);$b.Dispose()}
$g.Dispose();$sheet.Save((Join-Path $tank 'contact-sheet.png'));$sheet.Dispose();$font.Dispose()
'PASS: opposing sky edges identical, four palette exports, tank contact sheet.'
