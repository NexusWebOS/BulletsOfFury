using System;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
class CopyrightGlyphs {
 static readonly string[] Grid={"..########..",".##......##.","##........##","##..####..##","##.##.....##","##.##.....##","##.##.....##","##.##.....##","##..####..##","##........##",".##......##.","..########.."};
 static double Light(Color c){return c.R*.2126+c.G*.7152+c.B*.0722;}
 static void Main(string[] args){
  string art=Path.Combine(args[0],"art");
  foreach(int h in new[]{8,10,12,14,16,18,20,22,24,26,28,32}){
   string name="strike"+h,path=Path.Combine(art,name+".png"),csv=Path.Combine(art,name+".csv");var lines=File.ReadAllLines(csv).Where(s=>!s.StartsWith("169,")).ToList();int[] head=lines[0].Split(',').Select(Int32.Parse).ToArray(),o=lines.First(s=>s.StartsWith("79,")).Split(',').Select(Int32.Parse).ToArray();int cw=head[0],ch=head[1],pw=head[2],ph=head[3],cols=pw/cw,gx=(95%cols)*cw,gy=(95/cols)*ch;
   using(var source=new Bitmap(path))using(var b=new Bitmap(source.Width,source.Height,PixelFormat.Format32bppArgb)){
    using(var g=Graphics.FromImage(b))g.DrawImage(source,new Rectangle(0,0,b.Width,b.Height),new Rectangle(0,0,b.Width,b.Height),GraphicsUnit.Pixel);
    int size=Math.Min(o[6]-o[4],o[7]-o[5]),left=o[4],top=o[5]+((o[7]-o[5])-size)/2;
    for(int dim=0;dim<b.Width/pw;dim++)for(int palette=0;palette<b.Height/ph;palette++){
     for(int y=0;y<ch;y++)for(int x=0;x<cw;x++)b.SetPixel(dim*pw+gx+x,palette*ph+gy+y,Color.Transparent);
     for(int y=0;y<size;y++){
      int sy=o[2]+Math.Min(o[7]-1,top+y)+palette*ph;Color face=Color.White;double best=-1;
      for(int x=o[4];x<o[6];x++){Color c=source.GetPixel(dim*pw+o[1]+x,sy);double v=Light(c);if(c.A>220&&v>best){best=v;face=c;}}
      for(int x=0;x<size;x++)if(Grid[Math.Min(11,y*12/size)][Math.Min(11,x*12/size)]=='#')b.SetPixel(dim*pw+gx+left+x,palette*ph+gy+top+y,face);
     }
    }
    string temp=path+".copyright.png";b.Save(temp,ImageFormat.Png);source.Dispose();File.Copy(temp,path,true);File.Delete(temp);
    lines.Add(String.Join(",",new[]{169,gx,gy,o[3],left,top,left+size,top+size}));File.WriteAllLines(csv,lines.ToArray());
   }
  }
  Console.WriteLine("Authored copyright glyph in all 12 Fury Strike native banks.");
 }
}
