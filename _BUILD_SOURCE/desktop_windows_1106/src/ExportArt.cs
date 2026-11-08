using System;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Drawing2D;
using System.Linq;
class ExportArt {
 static void Stamp(Graphics g,string art,string text,int cx,int y,int height,int palette){
  var lines=File.ReadAllLines(Path.Combine(art,"strike"+height+".csv"));var head=lines[0].Split(',').Select(Int32.Parse).ToArray();var glyphs=lines.Skip(1).Where(s=>s.Trim().Length>0).Select(s=>s.Split(',').Select(Int32.Parse).ToArray()).ToDictionary(n=>n[0]);
  int pen=0,l=Int32.MaxValue,r=0;foreach(char c in text){var q=glyphs[c];if(q[7]>q[5]){l=Math.Min(l,pen+q[4]);r=Math.Max(r,pen+q[6]);}pen+=q[3];}pen=cx-(l+r)/2;
  using(var image=new Bitmap(Path.Combine(art,"strike"+height+".png")))foreach(char c in text){var q=glyphs[c];g.DrawImage(image,new Rectangle(pen,y-head[4],head[0],head[1]),new Rectangle(q[1],q[2]+palette*head[3],head[0],head[1]),GraphicsUnit.Pixel);pen+=q[3];}
 }
 static Bitmap SizeImage(string path,int w,int h) {
  using(var src=new Bitmap(path)) {var dst=new Bitmap(w,h,PixelFormat.Format32bppArgb);using(var g=Graphics.FromImage(dst)){g.InterpolationMode=InterpolationMode.NearestNeighbor;g.PixelOffsetMode=PixelOffsetMode.Half;g.DrawImage(src,new Rectangle(0,0,w,h));}return dst;}
 }
 static void Main(string[] a) {
  string root=a[0],art=Path.Combine(root,"art");
  foreach(string name in new[]{"hangar","doors","briefing"})using(var b=SizeImage(Path.Combine(art,name+"-generated.png"),1024,576))b.Save(Path.Combine(art,name+".png"));
  using(var b=SizeImage(Path.Combine(art,"hangar-generated-v2.png"),1024,576)){
   using(var g=Graphics.FromImage(b)){g.FillRectangle(new SolidBrush(Color.FromArgb(18,21,29)),47,5,289,29);Stamp(g,art,"BULLETS OF FURY",193,10,18,3);g.FillRectangle(new SolidBrush(Color.FromArgb(18,21,29)),510,5,123,27);Stamp(g,art,"FURY HQ",572,10,16,0);}
   b.Save(Path.Combine(art,"hangar.png"));using(var title=b.Clone(new Rectangle(0,0,1024,40),PixelFormat.Format32bppArgb))title.Save(Path.Combine(art,"titlebar.png"));
   string[] names={"minimize","maximize","close"};int[] xs={894,932,970};for(int n=0;n<3;n++)using(var button=b.Clone(new Rectangle(xs[n],0,37,39),PixelFormat.Format32bppArgb)){
    button.Save(Path.Combine(art,names[n]+".png"));using(var hot=(Bitmap)button.Clone()){for(int y=0;y<hot.Height;y++)for(int x=0;x<hot.Width;x++){var c=hot.GetPixel(x,y);hot.SetPixel(x,y,Color.FromArgb(c.A,Math.Min(255,c.R+25),Math.Min(255,c.G+25),Math.Min(255,c.B+25)));}hot.Save(Path.Combine(art,names[n]+"-hot.png"));}
   }
  }
  foreach(string suffix in new[]{"","-hot"})using(var b=new Bitmap(Path.Combine(art,"maximize"+suffix+".png"))){using(var g=Graphics.FromImage(b)){g.FillRectangle(new SolidBrush(Color.FromArgb(13,20,27)),9,7,21,24);using(var p=new Pen(Color.FromArgb(40,225,255),2)){g.DrawRectangle(p,15,10,12,12);g.DrawRectangle(p,10,15,12,12);}}b.Save(Path.Combine(art,"restore"+suffix+".png"));}
  using(var src=new Bitmap(a[1])) {
   // Source is the game's existing chroma-keyed logo; export its existing key to alpha.
   for(int y=0;y<src.Height;y++)for(int x=0;x<src.Width;x++){Color c=src.GetPixel(x,y);if(c.R>220&&c.B>220&&c.G<70)src.SetPixel(x,y,Color.Transparent);}
   using(var dst=new Bitmap(500,248,PixelFormat.Format32bppArgb)) {using(var g=Graphics.FromImage(dst)){g.InterpolationMode=InterpolationMode.NearestNeighbor;g.PixelOffsetMode=PixelOffsetMode.Half;g.DrawImage(src,new Rectangle(0,0,500,248));}dst.Save(Path.Combine(art,"logo.png"));}
  }
  using(var doors=new Bitmap(Path.Combine(art,"doors.png")))using(var logo=new Bitmap(Path.Combine(art,"logo.png"))){using(var g=Graphics.FromImage(doors))g.DrawImageUnscaled(logo,262,148);using(var left=doors.Clone(new Rectangle(0,0,512,576),PixelFormat.Format32bppArgb))left.Save(Path.Combine(art,"door-left.png"));using(var right=doors.Clone(new Rectangle(512,0,512,576),PixelFormat.Format32bppArgb))right.Save(Path.Combine(art,"door-right.png"));}
  using(var b=SizeImage(Path.Combine(art,"emblem-generated.png"),256,256)){
   b.Save(Path.Combine(art,"emblem.png"));using(var ms=new MemoryStream()){b.Save(ms,ImageFormat.Png);byte[] p=ms.ToArray();using(var bw=new BinaryWriter(File.Create(Path.Combine(art,"bof.ico")))){bw.Write((short)0);bw.Write((short)1);bw.Write((short)1);bw.Write((byte)0);bw.Write((byte)0);bw.Write((byte)0);bw.Write((byte)0);bw.Write((short)1);bw.Write((short)32);bw.Write(p.Length);bw.Write(22);bw.Write(p);}}
  }
  // Authored segments, exported once. The launcher only tiles/clips these bitmaps.
  using(var b=new Bitmap(14,18,PixelFormat.Format32bppArgb)){using(var g=Graphics.FromImage(b)){g.Clear(Color.FromArgb(255,22,25,29));g.FillRectangle(new SolidBrush(Color.FromArgb(245,168,28)),1,2,11,14);g.FillRectangle(new SolidBrush(Color.FromArgb(255,224,112)),1,2,11,3);g.FillRectangle(new SolidBrush(Color.FromArgb(153,79,11)),1,13,11,3);}b.Save(Path.Combine(art,"progress.png"));}
  using(var b=new Bitmap(24,24,PixelFormat.Format32bppArgb)){using(var g=Graphics.FromImage(b)){g.Clear(Color.Transparent);g.FillPolygon(Brushes.Black,new[]{new Point(3,2),new Point(22,12),new Point(3,23)});g.FillPolygon(new SolidBrush(Color.FromArgb(255,191,61)),new[]{new Point(4,3),new Point(20,12),new Point(4,21)});g.FillPolygon(new SolidBrush(Color.FromArgb(255,234,147)),new[]{new Point(5,4),new Point(17,11),new Point(5,9)});}b.Save(Path.Combine(art,"selector.png"));}
  Console.WriteLine("Exported generated plates, existing bitmap font/logo and authored status pieces.");
 }
}
