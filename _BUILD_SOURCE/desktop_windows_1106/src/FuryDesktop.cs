using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Media;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Web.Script.Serialization;
using System.Windows.Forms;
using Microsoft.Win32;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.WinForms;
[assembly: AssemblyTitle("Bullets of Fury")]
[assembly: AssemblyProduct("Bullets of Fury")]
[assembly: AssemblyCompany("ColeForge")]
[assembly: AssemblyVersion("2026.11.6.0")]
[assembly: AssemblyFileVersion("2026.11.6.0")]
[assembly: System.Runtime.Versioning.TargetFramework(".NETFramework,Version=v4.6.2",FrameworkDisplayName=".NET Framework 4.6.2")]

static class Program {
 public const string Product="ColeForge.BulletsOfFury.2026";
 public static string[] Args;
 public static string Root=AppDomain.CurrentDomain.BaseDirectory;
 public static string QaDir;
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern bool SetDllDirectory(string path);
 static void RuntimeAssemblies(){
  string folder=Path.Combine(Path.GetTempPath(),"ColeForge-BOF-Host-1.0.4314.35");Directory.CreateDirectory(folder);
  foreach(string name in new[]{"Microsoft.Web.WebView2.Core.dll","Microsoft.Web.WebView2.WinForms.dll","WebView2Loader.dll"}){
   string installed=Path.Combine(Root,name);if(File.Exists(installed))continue;
   string file=Path.Combine(folder,name);byte[] data=Art.Bytes(name);bool same=File.Exists(file)&&new FileInfo(file).Length==data.Length;
   if(!same){string next=file+"."+Process.GetCurrentProcess().Id+".tmp";File.WriteAllBytes(next,data);if(File.Exists(file))File.Delete(file);File.Move(next,file);}
  }
  SetDllDirectory(File.Exists(Path.Combine(Root,"WebView2Loader.dll"))?Root:folder);
  AppDomain.CurrentDomain.AssemblyResolve+=(s,e)=>{string name=new AssemblyName(e.Name).Name+".dll";if(name!="Microsoft.Web.WebView2.Core.dll"&&name!="Microsoft.Web.WebView2.WinForms.dll")return null;string file=Path.Combine(Root,name);return Assembly.LoadFrom(File.Exists(file)?file:Path.Combine(folder,name));};
 }
 public static bool Has(string key){return Array.IndexOf(Args,key)>=0;}
 public static string Arg(string key,string fallback){int n=Array.IndexOf(Args,key);return n>=0&&n+1<Args.Length?Args[n+1]:fallback;}
 public static void Log(string name,object data){try{if(QaDir==null)return;Directory.CreateDirectory(QaDir);lock(LogLock)File.AppendAllText(Path.Combine(QaDir,"desktop.jsonl"),new JavaScriptSerializer().Serialize(new{time=DateTime.UtcNow.ToString("o"),name=name,data=data})+"\n");}catch{}}
 static object LogLock=new object();
 [DllImport("user32.dll")] static extern bool SetProcessDPIAware();
 [DllImport("winmm.dll")] static extern uint timeBeginPeriod(uint value);
 [DllImport("winmm.dll")] static extern uint timeEndPeriod(uint value);
 [STAThread] static void Main(string[] args){
  Args=args;QaDir=Arg("--qa-dir",null);AppContext.SetSwitch("Switch.System.IO.UseLegacyPathHandling",false);AppContext.SetSwitch("Switch.System.IO.BlockLongPaths",false);SetProcessDPIAware();Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);timeBeginPeriod(1);
  Application.ThreadException+=(s,e)=>{Log("thread-error",e.Exception.ToString());MessageBox.Show(e.Exception.Message,"Bullets of Fury");};
  try{
   RuntimeAssemblies();
   foreach(string n in new[]{"hangar","doors","door-left","door-right","briefing","logo","selector","progress"})Art.Get(n);
   foreach(int h in new[]{10,12,14,21,28})PixelFont.At(h);foreach(int h in PixelFont.StrikeSizes)PixelFont.Strike(h);
   if(Has("--uninstall-worker")){Installer.UninstallWorker();return;}
   if(Has("--self-test")){SelfTests.Run();return;}
   bool setup=Has("--setup")||Payload.HasTrailer(Application.ExecutablePath);
   bool launcher=Has("--launcher")||Has("--qa-tour")||String.Equals(Path.GetFileNameWithoutExtension(Application.ExecutablePath),"BOF Launcher",StringComparison.OrdinalIgnoreCase);
   if(!setup&&!Has("--uninstall")&&(Has("--game")||!launcher)){Application.Run(new GameWindow(null));return;}
   Application.Run(new TerminalForm(setup,Has("--uninstall")));
  }catch(Exception e){Log("fatal",e.ToString());MessageBox.Show("BOF could not start.\n\n"+e.Message,"Bullets of Fury",MessageBoxButtons.OK,MessageBoxIcon.Error);Environment.ExitCode=1;}finally{timeEndPeriod(1);}
 }
}

static class Art {
 static Dictionary<string,Bitmap> bitmaps=new Dictionary<string,Bitmap>();
 public static Stream Open(string name){var s=Assembly.GetExecutingAssembly().GetManifestResourceStream("bof."+name);if(s==null)throw new FileNotFoundException("Missing launcher artwork: "+name);return s;}
 public static Bitmap Get(string name){Bitmap b;if(!bitmaps.TryGetValue(name,out b)){using(var s=Open(name+".png"))using(var v=new Bitmap(s)){b=new Bitmap(v.Width,v.Height,PixelFormat.Format32bppPArgb);using(var g=Graphics.FromImage(b)){g.CompositingMode=CompositingMode.SourceCopy;g.DrawImage(v,new Rectangle(0,0,v.Width,v.Height),new Rectangle(0,0,v.Width,v.Height),GraphicsUnit.Pixel);}}bitmaps[name]=b;}return b;}
 public static byte[] Bytes(string name){using(var s=Open(name))using(var m=new MemoryStream()){s.CopyTo(m);return m.ToArray();}}
 public static void Blit(Graphics g,string name,int x,int y){Bitmap b=Get(name);g.DrawImage(b,new Rectangle(x,y,b.Width,b.Height),new Rectangle(0,0,b.Width,b.Height),GraphicsUnit.Pixel);}
}
sealed class OpaqueBlit : IDisposable {
 IntPtr dc,bitmap,previous;int width,height;
 [DllImport("gdi32.dll")]static extern IntPtr CreateCompatibleDC(IntPtr h);
 [DllImport("gdi32.dll")]static extern IntPtr SelectObject(IntPtr d,IntPtr b);
 [DllImport("gdi32.dll")]static extern bool DeleteObject(IntPtr b);
 [DllImport("gdi32.dll")]static extern bool DeleteDC(IntPtr d);
 [DllImport("gdi32.dll")]static extern bool BitBlt(IntPtr dst,int x,int y,int w,int h,IntPtr src,int sx,int sy,uint op);
 public OpaqueBlit(Bitmap source){width=source.Width;height=source.Height;dc=CreateCompatibleDC(IntPtr.Zero);bitmap=source.GetHbitmap(Color.Black);previous=SelectObject(dc,bitmap);}
 public void Draw(Graphics g,int x,int y){IntPtr h=g.GetHdc();try{BitBlt(h,x,y,width,height,dc,0,0,0x00CC0020);}finally{g.ReleaseHdc(h);}}
 public void Dispose(){if(dc!=IntPtr.Zero){SelectObject(dc,previous);DeleteObject(bitmap);DeleteDC(dc);dc=IntPtr.Zero;}}
}
sealed class Glyph {
 public int X,Y,Advance,L,T,R,B;
}
sealed class PixelFont {
 static Dictionary<int,PixelFont> fonts=new Dictionary<int,PixelFont>();static Dictionary<int,PixelFont> strike=new Dictionary<int,PixelFont>();
 public int Height{get{return height;}}
 public static readonly int[] StrikeSizes={32,28,26,24,22,20,18,16,14,12,10,8};
 public static PixelFont Strike(int h){PixelFont f;if(!strike.TryGetValue(h,out f))strike[h]=f=new PixelFont(h,"strike");return f;}
 Bitmap image;int cw,ch,planeH,height,top;Dictionary<char,Glyph> glyphs=new Dictionary<char,Glyph>();
 public static PixelFont At(int h){PixelFont f;if(!fonts.TryGetValue(h,out f))fonts[h]=f=new PixelFont(h);return f;}
 PixelFont(int h):this(h,"font"){}
 PixelFont(int h,string family){
  image=Art.Get(family+h);string[] lines=Encoding.ASCII.GetString(Art.Bytes(family+h+".csv")).Split('\n');int[] head=lines[0].Split(',').Select(Int32.Parse).ToArray();cw=head[0];ch=head[1];planeH=head[3];top=head[4];height=head[5];
  foreach(string line in lines.Skip(1)){if(line.Trim().Length==0)continue;int[] n=line.Trim().Split(',').Select(Int32.Parse).ToArray();glyphs[(char)n[0]]=new Glyph{X=n[1],Y=n[2],Advance=n[3],L=n[4],T=n[5],R=n[6],B=n[7]};}
 }
 Glyph G(char c){Glyph q;return glyphs.TryGetValue(c,out q)?q:glyphs['?'];}
 public int Width(string s){int pen=0,l=Int32.MaxValue,r=0;foreach(char c in s){Glyph q=G(c);if(q.R>q.L){l=Math.Min(l,pen+q.L);r=Math.Max(r,pen+q.R);}pen+=q.Advance;}return l==Int32.MaxValue?pen:r-l;}
 public void Draw(Graphics g,string s,int x,int y,int palette,bool center){
  if(s==null)return;s=s.ToUpperInvariant();int pen=0,l=Int32.MaxValue,r=0;foreach(char c in s){Glyph q=G(c);if(q.R>q.L){l=Math.Min(l,pen+q.L);r=Math.Max(r,pen+q.R);}pen+=q.Advance;}if(l==Int32.MaxValue)l=0;
  pen=x-(center?(l+r)/2:l);foreach(char c in s){Glyph q=G(c);g.DrawImage(image,new Rectangle(pen,y-top,cw,ch),new Rectangle(q.X,q.Y+palette*planeH,cw,ch),GraphicsUnit.Pixel);pen+=q.Advance;}
 }
 public void Wrap(Graphics g,string s,int x,int y,int width,int palette,int leading){
  foreach(string paragraph in s.Split('\n')){string line="";foreach(string raw in paragraph.Split(' ')){string word=raw;while(Width(word)>width&&word.Length>1){int n=word.Length-1;while(n>1&&Width(word.Substring(0,n))>width)n--;if(line.Length>0){Draw(g,line,x,y,palette,false);y+=leading;line="";}Draw(g,word.Substring(0,n),x,y,palette,false);y+=leading;word=word.Substring(n);}string next=line.Length==0?word:line+" "+word;if(Width(next)>width&&line.Length>0){Draw(g,line,x,y,palette,false);y+=leading;line=word;}else line=next;}if(line.Length>0)Draw(g,line,x,y,palette,false);y+=leading;}
 }
}
static class Cues {
 static Dictionary<string,SoundPlayer> players=new Dictionary<string,SoundPlayer>();
 public static bool Enabled=true;
 public static void Play(string cue){if(!Enabled)return;try{SoundPlayer p;if(!players.TryGetValue(cue,out p)){p=new SoundPlayer(new MemoryStream(Art.Bytes(cue+".wav")));p.Load();players[cue]=p;}p.Play();Program.Log("cue",cue);}catch(Exception e){Program.Log("audio-error",e.Message);}}
 public static void Stop(){foreach(var p in players.Values)p.Stop();}
}
sealed class Preferences {
 public bool Fullscreen=true,Sound=true,QuickDoors=false;
 public static string Folder {get{return Program.Arg("--profile",Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),"ColeForge","BulletsOfFury"));}}
 public static Preferences Load(){try{return new JavaScriptSerializer().Deserialize<Preferences>(File.ReadAllText(Path.Combine(Folder,"launcher.json"))) ?? new Preferences();}catch{return new Preferences();}}
 public void Save(){Directory.CreateDirectory(Folder);File.WriteAllText(Path.Combine(Folder,"launcher.json"),new JavaScriptSerializer().Serialize(this));}
}

sealed class TerminalForm:Form {
 const int W=1024,H=576;
 static readonly int[] DoorMotion=Encoding.ASCII.GetString(Art.Bytes("door-motion.csv")).Trim().Split(',').Select(Int32.Parse).ToArray();
 public string Page="home";
 Bitmap scene=new Bitmap(W,H,PixelFormat.Format32bppRgb),surface=new Bitmap(W,H,PixelFormat.Format32bppRgb);bool sceneDirty=true;OpaqueBlit sceneBlit,leftBlit,rightBlit;
 readonly Rectangle[] windowButtons={new Rectangle(894,0,37,39),new Rectangle(932,0,37,39),new Rectangle(970,0,37,39)};
 int windowHover=-1;
 readonly bool setup,uninstall;Preferences prefs;System.Threading.Timer pulse;int pulseQueued;Stopwatch clock=Stopwatch.StartNew();
 string target;bool shortcuts=true,installing,installed,error,closing;string detail="SYSTEM READY",failure="";double progress;
 double doorStart,doorDuration=1.60,doorOpen=0;int doorMode=1;Action behindDoors;
 int selected=0;List<string> choices=new List<string>();List<Rectangle> hit=new List<Rectangle>();
 CancellationTokenSource cancel;double idleAt=0;int tour=0;List<double> paints=new List<double>();double lastPaint=0;
 public TerminalForm(bool isSetup,bool isUninstall){
  setup=isSetup;uninstall=isUninstall;prefs=Preferences.Load();Cues.Enabled=prefs.Sound;target=Program.Arg("--target",Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),"Programs","ColeForge","Bullets of Fury"));
  if(uninstall){target=Program.Root.TrimEnd(Path.DirectorySeparatorChar);selected=1;}
  Text=setup?"Bullets of Fury - Deployment Setup":"Bullets of Fury - Fury HQ";ClientSize=new Size(W,H);MinimumSize=new Size(W,H);AutoScaleMode=AutoScaleMode.None;FormBorderStyle=FormBorderStyle.None;StartPosition=FormStartPosition.CenterScreen;MaximizeBox=true;MinimizeBox=true;KeyPreview=true;DoubleBuffered=true;BackColor=Color.Black;MaximizedBounds=Screen.FromControl(this).WorkingArea;
  using(var s=Art.Open("bof.ico"))Icon=new Icon(s);SetStyle(ControlStyles.AllPaintingInWmPaint|ControlStyles.UserPaint|ControlStyles.OptimizedDoubleBuffer,true);
  leftBlit=new OpaqueBlit(Art.Get("door-left"));rightBlit=new OpaqueBlit(Art.Get("door-right"));
  Shown+=(s,e)=>{doorStart=clock.Elapsed.TotalSeconds+.35;Cues.Play("boot");RefreshChoices();Program.Log("terminal-open",new{setup,uninstall,bounds=Bounds.ToString()});};
  pulse=new System.Threading.Timer(delegate{if(!IsHandleCreated||IsDisposed||!Visible||WindowState==FormWindowState.Minimized||Interlocked.Exchange(ref pulseQueued,1)!=0)return;try{BeginInvoke((Action)delegate{Interlocked.Exchange(ref pulseQueued,0);if(!IsDisposed)Tick();});}catch{Interlocked.Exchange(ref pulseQueued,0);}},null,0,16);MouseMove+=MouseOver;MouseDown+=HandleMouseDown;KeyDown+=KeysDown;MouseLeave+=(s,e)=>{windowHover=-1;Invalidate();};Resize+=(s,e)=>{MaximizedBounds=Screen.FromControl(this).WorkingArea;Invalidate();};
  FormClosing+=(s,e)=>{if(installing){e.Cancel=true;cancel.Cancel();detail="CANCELLING - RESTORING SAFE STATE";}else{pulse.Dispose();if(sceneBlit!=null)sceneBlit.Dispose();leftBlit.Dispose();rightBlit.Dispose();Cues.Stop();prefs.Save();Program.Log("terminal-close",new{paintCount=paints.Count,meanFrameMs=paints.Count==0?0:paints.Average(),maxFrameMs=paints.Count==0?0:paints.Max()});}};
 }
 void RefreshChoices(){
  sceneDirty=true;choices.Clear();if(Page=="controls")choices.Add("BACK TO HQ");
  else if(Page=="options"){choices.Add("FULLSCREEN: "+(prefs.Fullscreen?"ON":"OFF"));choices.Add("SOUND: "+(prefs.Sound?"ON":"OFF"));choices.Add("DOORS: "+(prefs.QuickDoors?"QUICK":"CINEMATIC"));choices.Add("UNINSTALL GAME");choices.Add("BACK TO HQ");}
  else if(error){choices.Add("BACK");choices.Add("EXIT");}
  else if(uninstall){choices.Add("REMOVE GAME");choices.Add("CANCEL");}
  else if(installing)choices.Add("CANCEL INSTALL");
  else if(setup&&!installed){if(Installer.IsInstalled(target))choices.Add("OPEN LAUNCHER");else choices.Add("INSTALL GAME");choices.Add("INSTALL LOCATION");choices.Add("SHORTCUTS: "+(shortcuts?"ON":"OFF"));choices.Add("CONTROLS");choices.Add("EXIT");}
  else{choices.Add("LAUNCH GAME");choices.Add("FLIGHT CONTROLS");choices.Add("LAUNCHER OPTIONS");choices.Add("EXIT TO DESKTOP");}
  selected=Math.Min(selected,choices.Count-1);hit.Clear();for(int n=0;n<choices.Count;n++)hit.Add(Page=="controls"?new Rectangle(80,479,860,46):new Rectangle(660,174+n*52,306,44));Invalidate();
 }
 void Tick(){
  double now=clock.Elapsed.TotalSeconds;if(doorMode!=0&&now>=doorStart){double f=Math.Min(1,(now-doorStart)/doorDuration);int frame=Math.Min(95,(int)Math.Floor(f*95));double authored=DoorMotion[frame]/512.0;doorOpen=doorMode==1?authored:1-authored;if(f>=1){if(doorMode==2){doorMode=0;Action a=behindDoors;behindDoors=null;if(a!=null)a();if(!closing){doorMode=1;doorStart=now+.08;doorDuration=prefs.QuickDoors ? .50 : 1.20;Cues.Play("doors");}}else{doorMode=0;doorOpen=1;idleAt=now;Program.Log("doors-open",new{seconds=doorDuration,authoredFrames=96});}}}
  if(Program.Has("--qa-tour")&&doorMode==0&&now-idleAt>.45&&!installing){
   string name=setup?"setup":"launcher";
   if(tour==0){SaveFrame(name+"-home");tour++;if(Program.Has("--qa-install")){RunInstall();}else Go("controls");}
   else if(!Program.Has("--qa-install")&&tour==1){SaveFrame(name+"-controls");tour++;Go("options");}
   else if(!Program.Has("--qa-install")&&tour==2){SaveFrame(name+"-options");tour++;Go("home");}
   else if(!Program.Has("--qa-install")&&tour==3){SaveFrame(name+"-return");Program.Log("tour-complete",true);Close();}
   else if(Program.Has("--qa-install")&&installed){SaveFrame("install-complete");Program.Log("install-tour-complete",true);Close();}
   else if(Program.Has("--qa-install")&&error){SaveFrame("install-error");Close();}
  }
  if(Program.Has("--qa-uninstall")&&doorMode==0&&now-idleAt>.3){Program.Args=Program.Args.Where(x=>x!="--qa-uninstall").ToArray();RemoveGame();}
  if(Visible){if(doorMode!=0)Refresh();else Invalidate();}
 }
 void Go(string page){if(doorMode!=0||installing)return;Change(delegate{Page=page;selected=0;RefreshChoices();});}
 void Change(Action a){Cues.Play("doors");doorMode=2;doorStart=clock.Elapsed.TotalSeconds;doorDuration=prefs.QuickDoors ? .45 : .90;behindDoors=a;}
 void Activate(int n){if(n<0||n>=choices.Count||doorMode!=0)return;Cues.Play("confirm");selected=n;
  if(Page=="controls"){Go("home");return;}
  if(Page=="options"){if(n==0)prefs.Fullscreen=!prefs.Fullscreen;else if(n==1){prefs.Sound=!prefs.Sound;Cues.Enabled=prefs.Sound;}else if(n==2)prefs.QuickDoors=!prefs.QuickDoors;else if(n==3){Process.Start(Application.ExecutablePath,"--uninstall");Close();return;}else Go("home");prefs.Save();RefreshChoices();return;}
  if(error){if(n==0){error=false;RefreshChoices();}else Close();return;}
  if(uninstall){if(n==0)RemoveGame();else Close();return;}
  if(installing){cancel.Cancel();detail="CANCELLING - RESTORING SAFE STATE";return;}
  if(setup&&!installed){if(n==0){if(Installer.IsInstalled(target)){Process.Start(Path.Combine(target,"BOF Launcher.exe"));Close();}else RunInstall();}else if(n==1){using(var f=new FolderBrowserDialog()){f.Description="Choose the parent folder. BOF gets its own Bullets of Fury folder.";if(f.ShowDialog(this)==DialogResult.OK){target=Path.Combine(f.SelectedPath,"Bullets of Fury");detail="INSTALL LOCATION UPDATED";RefreshChoices();}}}else if(n==2){shortcuts=!shortcuts;RefreshChoices();}else if(n==3)Go("controls");else Close();return;}
  if(n==0)Change(Launch);else if(n==1)Go("controls");else if(n==2)Go("options");else Close();
 }
 void Launch(){
  if(setup){closing=true;Process.Start(Path.Combine(target,"Bullets of Fury.exe"));Close();return;}
  if(!File.Exists(Path.Combine(Program.Root,"game","index.html"))){SetError("The installed game files are missing. Run the BOF installer again.");return;}
  closing=true;Cues.Play("launch");GameWindow game=new GameWindow(this);game.FormClosed+=(s,e)=>{closing=false;Show();Activate();doorMode=1;doorStart=clock.Elapsed.TotalSeconds;doorDuration=1.2;doorOpen=0;Cues.Play("doors");};game.Shown+=(s,e)=>Hide();game.Show();
 }
 public void GameError(string message){closing=false;Show();doorMode=0;doorOpen=1;SetError(message);}
 void SetError(string message){failure=message;error=true;installing=false;detail="DEPLOYMENT NEEDS ATTENTION";RefreshChoices();Program.Log("terminal-error",message);}
 async void RunInstall(){
  if(installing)return;installing=true;error=false;progress=0;cancel=new CancellationTokenSource();detail="CHECKING PAYLOAD AND DESTINATION";RefreshChoices();
  try{await Task.Run(delegate{Installer.Install(target,shortcuts&&!Program.Has("--no-shortcuts"),cancel.Token,delegate(double p,string text){BeginInvoke((Action)delegate{progress=p;detail=text;sceneDirty=true;});});});installed=true;installing=false;progress=1;detail="INSTALL COMPLETE - READY FOR TAKEOFF";Cues.Play("confirm");RefreshChoices();idleAt=clock.Elapsed.TotalSeconds;}
  catch(OperationCanceledException){installing=false;progress=0;detail="INSTALL CANCELLED - NO PARTIAL GAME LEFT";RefreshChoices();Program.Log("install-cancelled",true);}
  catch(Exception e){Program.Log("install-exception",e.ToString());SetError(e.Message);}
 }
 void RemoveGame(){try{if(!Installer.IsInstalled(target))throw new Exception("This folder is not a registered BOF installation.");if(Installer.OtherWindowRunning(target))throw new Exception("Close the other BOF game or launcher window, then retry uninstalling.");SaveFrame("uninstall-confirmation");Installer.StartUninstall(target);Close();}catch(Exception e){SetError(e.Message);}}
 [DllImport("user32.dll")]static extern bool ReleaseCapture();[DllImport("user32.dll")]static extern IntPtr SendMessage(IntPtr h,int m,int w,int l);
 Rectangle Viewport(){int scale=Math.Max(1,Math.Min(ClientSize.Width/W,ClientSize.Height/H));return new Rectangle((ClientSize.Width-W*scale)/2,(ClientSize.Height-H*scale)/2,W*scale,H*scale);}
 Point Logical(Point p){Rectangle v=Viewport();return v.Contains(p)?new Point((p.X-v.X)*W/v.Width,(p.Y-v.Y)*H/v.Height):new Point(-1,-1);}
 void MaxRestore(){WindowState=WindowState==FormWindowState.Maximized?FormWindowState.Normal:FormWindowState.Maximized;Program.Log("window-control",new{action=WindowState==FormWindowState.Maximized?"maximize":"restore",bounds=Bounds.ToString()});Invalidate();}
 void HandleMouseDown(object sender,MouseEventArgs e){if(e.Button!=MouseButtons.Left)return;Point p=Logical(e.Location);if(p.X<0)return;for(int i=0;i<windowButtons.Length;i++)if(windowButtons[i].Contains(p)){Cues.Play("select");if(i==0){Program.Log("window-control",new{action="minimize"});WindowState=FormWindowState.Minimized;}else if(i==1)MaxRestore();else{Program.Log("window-control",new{action="close"});Close();}return;}if(p.Y<39&&p.X<890){if(e.Clicks==2)MaxRestore();else if(WindowState==FormWindowState.Normal){ReleaseCapture();SendMessage(Handle,0xA1,2,0);}return;}for(int n=0;n<hit.Count;n++)if(hit[n].Contains(p)){Activate(n);break;}}
 void MouseOver(object sender,MouseEventArgs e){Point p=Logical(e.Location);int hover=Array.FindIndex(windowButtons,b=>b.Contains(p));if(hover!=windowHover){windowHover=hover;Invalidate();}if(hover>=0){Cursor=Cursors.Hand;return;}if(doorMode!=0){Cursor=Cursors.Default;return;}for(int n=0;n<hit.Count;n++)if(hit[n].Contains(p)){if(selected!=n){selected=n;sceneDirty=true;Cues.Play("select");Invalidate();}Cursor=Cursors.Hand;return;}Cursor=Cursors.Default;}
 void KeysDown(object sender,KeyEventArgs e){if(e.KeyCode==Keys.Escape){if(Page!="home")Go("home");else if(!installing)Close();}else if(e.KeyCode==Keys.Up||e.KeyCode==Keys.W){selected=(selected+choices.Count-1)%choices.Count;Cues.Play("select");}else if(e.KeyCode==Keys.Down||e.KeyCode==Keys.S){selected=(selected+1)%choices.Count;Cues.Play("select");}else if(e.KeyCode==Keys.Enter||e.KeyCode==Keys.Space)Activate(selected);sceneDirty=true;Invalidate();}
 protected override void OnPaint(PaintEventArgs e){
  double now=clock.Elapsed.TotalMilliseconds;if(lastPaint>0&&doorMode!=0)paints.Add(now-lastPaint);lastPaint=now;Graphics g=e.Graphics;g.InterpolationMode=InterpolationMode.NearestNeighbor;g.PixelOffsetMode=PixelOffsetMode.Half;g.CompositingQuality=CompositingQuality.HighSpeed;
  if(sceneDirty){using(var sg=Graphics.FromImage(scene)){sg.InterpolationMode=InterpolationMode.NearestNeighbor;sg.PixelOffsetMode=PixelOffsetMode.Half;RenderScene(sg);}if(sceneBlit!=null)sceneBlit.Dispose();sceneBlit=new OpaqueBlit(scene);sceneDirty=false;}
  using(var fg=Graphics.FromImage(surface)){sceneBlit.Draw(fg,0,0);if(doorOpen<1){int offset=(int)Math.Round(512*doorOpen);leftBlit.Draw(fg,-offset,0);rightBlit.Draw(fg,512+offset,0);if(doorOpen==0)TextAt(fg,setup?"FURY HQ // DEPLOYMENT AUTHORIZED":"FURY HQ // OPENING HANGAR",512,430,14,3,true);}Art.Blit(fg,"titlebar",0,0);for(int i=0;i<3;i++){string key=i==0?"minimize":i==1?(WindowState==FormWindowState.Maximized?"restore":"maximize"):"close";Art.Blit(fg,key+(windowHover==i?"-hot":""),windowButtons[i].X,windowButtons[i].Y);}}
  g.Clear(Color.Black);g.DrawImage(surface,Viewport(),new Rectangle(0,0,W,H),GraphicsUnit.Pixel);
 }
 void RenderScene(Graphics g){
  bool briefing=Page=="controls";Art.Blit(g,briefing?"briefing":"hangar",0,0);
  if(briefing){
   Fit(g,"FLIGHT CONTROLS",new Rectangle(80,79,864,50),28,3,false);
   string[,] rows={{"MOVE","W A S D / ARROW KEYS"},{"PRIMARY FIRE","LEFT CLICK / J"},{"RETINA TARGET","RIGHT CLICK / C"},{"FIRE MISSILES","SPACE / K"},{"MULTI-RETINA","HOLD MOUSE BUTTON 4 / Y"},{"ALT MULTI-RETINA","RIGHT TAP, THEN RIGHT + HOLD"},{"BARREL ROLL","DOUBLE-TAP LEFT / RIGHT"},{"SOMERSAULT","DOUBLE-TAP UP"},{"FULLSCREEN / WINDOW","F11 / ALT + ENTER"},{"PAUSE","ENTER / P"}};
   for(int n=0;n<rows.GetLength(0);n++){int color=n==4||n==5?6:0;Fit(g,rows[n,0],new Rectangle(82,136+n*28,314,28),14,color,false);Fit(g,rows[n,1],new Rectangle(410,136+n*28,530,28),14,color,false);}
   Fit(g,"PRESS SPACE WHILE SCANNING TO LAUNCH THE MARKED VOLLEY.",new Rectangle(82,418,858,23),12,3,false);
   Fit(g,"BACK TO HQ",new Rectangle(82,479,860,46),22,3,true);
  }else{
   Art.Blit(g,"logo",80,92);
   if(!error)Fit(g,"2026 \u00A9 COLEFORGE PRODUCTIONS.",new Rectangle(70,369,520,38),16,0,false);
   string heading=error?"STATUS ALERT":uninstall?"DECOMMISSION":Page=="options"?"SYSTEM OPTIONS":setup&&!installed?"INSTALL BOF":"READY TO LAUNCH";
   Fit(g,heading,new Rectangle(666,105,300,38),22,3,false);
   Fit(g,installing?"DEPLOYING GAME FILES":setup&&!installed?"WINDOWS X64 / COMPLETE BUILD":"COLEFORGE / BULLETS OF FURY",new Rectangle(666,144,300,25),10,6,false);
   for(int n=0;n<choices.Count;n++)Fit(g,choices[n],new Rectangle(683,174+n*52,266,44),18,n==selected?3:0,n==selected);
   if(error)CenterWrap(g,failure,new Rectangle(77,351,540,91),14,2);
   else if(uninstall)CenterWrap(g,"REMOVE GAME FILES AND SHORTCUTS. YOUR SAVES AND SETTINGS WILL BE KEPT.",new Rectangle(78,419,540,36),12,0);
   else if(installing||installed){Fit(g,detail,new Rectangle(58,476,906,27),12,6,false);for(int i=0;i<(int)(progress*60);i++)Art.Blit(g,"progress",62+i*14,513);Fit(g,(int)(progress*100)+"%",new Rectangle(920,508,60,28),14,3,false);}
   else if(setup){Fit(g,"DESTINATION",new Rectangle(58,475,906,24),12,3,false);CenterWrap(g,target,new Rectangle(58,500,906,43),12,0);}
   else Fit(g,"THANK YOU FOR DEDICATED SUPPORT AND APPRECIATION!",new Rectangle(56,479,912,58),18,0,false);
  }
 }
 PixelFont Fitted(string text,Rectangle box,int maximum){foreach(int h in PixelFont.StrikeSizes)if(h<=maximum&&h<=box.Height-6&&PixelFont.Strike(h).Width(text)<=box.Width-8)return PixelFont.Strike(h);return PixelFont.Strike(8);}
 void Fit(Graphics g,string text,Rectangle box,int maximum,int palette,bool arrow){
  PixelFont font=Fitted(text,box,maximum);int width=font.Width(text);font.Draw(g,text,box.X+box.Width/2,box.Y+(box.Height-font.Height)/2,palette,true);
  if(arrow){int x=box.X+(box.Width-width)/2-30;Art.Blit(g,"selector",Math.Max(660==box.X?664:box.X-22,x),box.Y+(box.Height-24)/2);}
  Program.Log("text-fit",new{text,font="BOF Pixelmap Fury Strike",height=font.Height,width,available=box.Width-8,box=box.ToString(),fits=width<=box.Width-8&&font.Height<=box.Height-6});
 }
 List<string> Wrapped(PixelFont font,string text,int width){
  var lines=new List<string>();foreach(string para in text.Replace("\r","").Split('\n')){string line="";foreach(string raw in para.Split(' ')){string word=raw;while(font.Width(word)>width&&word.Length>1){if(line.Length>0){lines.Add(line);line="";}int cut=word.Length-1;while(cut>1&&font.Width(word.Substring(0,cut))>width)cut--;lines.Add(word.Substring(0,cut));word=word.Substring(cut);}string next=line.Length==0?word:line+" "+word;if(font.Width(next)>width&&line.Length>0){lines.Add(line);line=word;}else line=next;}if(line.Length>0)lines.Add(line);}return lines;
 }
 void CenterWrap(Graphics g,string text,Rectangle box,int maximum,int palette){
  PixelFont font=PixelFont.Strike(8);List<string> lines=null;foreach(int h in PixelFont.StrikeSizes){if(h>maximum)continue;var f=PixelFont.Strike(h);var candidate=Wrapped(f,text,box.Width-8);if(candidate.Count*(h+5)-5<=box.Height-6){font=f;lines=candidate;break;}}
  if(lines==null){lines=Wrapped(font,text,box.Width-8);int count=Math.Max(1,(box.Height-6)/(font.Height+5));if(lines.Count>count){lines=lines.Take(count).ToList();string last=lines[count-1];while(last.Length>0&&font.Width(last+"...")>box.Width-8)last=last.Substring(0,last.Length-1);lines[count-1]=last+"...";}}
  int block=lines.Count*(font.Height+5)-5,y=box.Y+(box.Height-block)/2;foreach(string line in lines){Fit(g,line,new Rectangle(box.X,y,box.Width,font.Height+6),font.Height,palette,false);y+=font.Height+5;}
 }
 void TextAt(Graphics g,string text,int x,int y,int h,int palette,bool center){PixelFont font=PixelFont.Strike(PixelFont.StrikeSizes.First(v=>v<=h));font.Draw(g,text,x,y,palette,center);}
 public void SaveFrame(string name){if(Program.QaDir==null)return;using(var b=new Bitmap(ClientSize.Width,ClientSize.Height)){DrawToBitmap(b,new Rectangle(Point.Empty,ClientSize));b.Save(Path.Combine(Program.QaDir,name+".png"));}Program.Log("screenshot",name);}
}

sealed class GameWindow:Form {
 WebView2 web;TerminalForm launcher;Preferences prefs;Rectangle windowBounds;bool fullscreen;bool closing;int port;
 public GameWindow(TerminalForm parent){launcher=parent;prefs=Preferences.Load();Text="Bullets of Fury";BackColor=Color.Black;AutoScaleMode=AutoScaleMode.None;KeyPreview=true;StartPosition=FormStartPosition.CenterScreen;ClientSize=new Size(1280,800);using(var s=Art.Open("bof.ico"))Icon=new Icon(s);
  fullscreen=parent==null?!Program.Has("--windowed"):prefs.Fullscreen;if(fullscreen){FormBorderStyle=FormBorderStyle.None;Bounds=Screen.FromControl(this).Bounds;WindowState=FormWindowState.Maximized;}else FormBorderStyle=FormBorderStyle.Sizable;
  Shown+=async(s,e)=>await StartGame();FormClosed+=(s,e)=>{closing=true;if(web!=null){web.Dispose();web=null;}Program.Log("game-closed",true);};
 }
 async Task StartGame(){try{
  string game=Path.Combine(Program.Root,"game");if(!File.Exists(Path.Combine(game,"index.html")))throw new FileNotFoundException("Game assets are missing. Run the complete BOF installer.");
  string runtime=CoreWebView2Environment.GetAvailableBrowserVersionString();Program.Log("runtime",runtime);
  string args="--autoplay-policy=no-user-gesture-required";port=Int32.Parse(Program.Arg("--debug-port","0"));if(port>0&&Program.QaDir!=null)args+=" --remote-debugging-port="+port;
  var options=new CoreWebView2EnvironmentOptions(args);string data=Path.Combine(Preferences.Folder,"WebView2");var env=await CoreWebView2Environment.CreateAsync(null,data,options);if(closing)return;
  web=new WebView2{Dock=DockStyle.Fill,DefaultBackgroundColor=Color.Black};Controls.Add(web);await web.EnsureCoreWebView2Async(env);web.CoreWebView2.SetVirtualHostNameToFolderMapping("bof.coleforge.local",game,CoreWebView2HostResourceAccessKind.DenyCors);
  var settings=web.CoreWebView2.Settings;settings.AreDefaultContextMenusEnabled=false;settings.IsStatusBarEnabled=false;settings.IsZoomControlEnabled=false;settings.AreDevToolsEnabled=Program.QaDir!=null;settings.IsWebMessageEnabled=true;settings.AreBrowserAcceleratorKeysEnabled=false;web.ZoomFactor=1;
  web.CoreWebView2.NewWindowRequested+=(s,e)=>e.Handled=true;
  web.CoreWebView2.WindowCloseRequested+=(s,e)=>Close();
  web.CoreWebView2.NavigationStarting+=(s,e)=>{Uri u;if(!Uri.TryCreate(e.Uri,UriKind.Absolute,out u)||u.Host!="bof.coleforge.local")e.Cancel=true;};
  web.CoreWebView2.ProcessFailed+=(s,e)=>Program.Log("web-process-failed",e.ProcessFailedKind.ToString());
  web.CoreWebView2.WebMessageReceived+=(s,e)=>{try{if(new Uri(e.Source).Host=="bof.coleforge.local"&&e.TryGetWebMessageAsString()=="bof:fullscreen")BeginInvoke((Action)ToggleFullscreen);}catch{}};
  await web.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync("addEventListener('keydown',function(e){if(e.code==='F11'||(e.code==='Enter'&&e.altKey)){e.preventDefault();e.stopImmediatePropagation();chrome.webview.postMessage('bof:fullscreen');}},true);");
  web.CoreWebView2.ContainsFullScreenElementChanged+=(s,e)=>{if(web.CoreWebView2.ContainsFullScreenElement&&!fullscreen)ToggleFullscreen();};
  web.CoreWebView2.NavigationCompleted+=(s,e)=>{Program.Log("game-navigation",new{success=e.IsSuccess,status=e.WebErrorStatus.ToString(),fullscreen,bounds=Bounds.ToString(),screen=Screen.FromControl(this).Bounds.ToString()});Activate();BringToFront();web.Focus();};
  web.Source=new Uri("https://bof.coleforge.local/index.html?quality=high");
 }catch(Exception e){Program.Log("game-error",e.ToString());if(launcher!=null){launcher.GameError("BOF needs the included WebView2 Runtime. Run setup again. Details: "+e.Message);Close();}else{MessageBox.Show(e.Message,"Bullets of Fury");Close();}}}
 void ToggleFullscreen(){if(closing)return;if(fullscreen){WindowState=FormWindowState.Normal;FormBorderStyle=FormBorderStyle.Sizable;ClientSize=new Size(1280,800);Location=new Point(Math.Max(0,(Screen.FromControl(this).WorkingArea.Width-Width)/2),Math.Max(0,(Screen.FromControl(this).WorkingArea.Height-Height)/2));}else{windowBounds=Bounds;FormBorderStyle=FormBorderStyle.None;Bounds=Screen.FromControl(this).Bounds;WindowState=FormWindowState.Maximized;}fullscreen=!fullscreen;Program.Log("fullscreen",new{enabled=fullscreen,bounds=Bounds.ToString()});}
}

sealed class BoundedStream:Stream {
 Stream source;long origin,length,position;
 public BoundedStream(Stream input,long start,long size){source=input;origin=start;length=size;source.Position=origin;}
 public override bool CanRead{get{return true;}}public override bool CanSeek{get{return true;}}public override bool CanWrite{get{return false;}}public override long Length{get{return length;}}public override long Position{get{return position;}set{Seek(value,SeekOrigin.Begin);}}
 public override int Read(byte[] b,int o,int c){c=(int)Math.Min(c,length-position);if(c<=0)return 0;source.Position=origin+position;int n=source.Read(b,o,c);position+=n;return n;}
 public override long Seek(long offset,SeekOrigin kind){long p=kind==SeekOrigin.Begin?offset:kind==SeekOrigin.Current?position+offset:length+offset;if(p<0||p>length)throw new IOException("Invalid payload offset.");position=p;return position;}
 public override void Flush(){}public override void SetLength(long v){throw new NotSupportedException();}public override void Write(byte[] b,int o,int c){throw new NotSupportedException();}
 protected override void Dispose(bool disposing){if(disposing)source.Dispose();base.Dispose(disposing);}
}
static class Payload {
 public const string Magic="BOFSETUP1106DATA";
 public static bool HasTrailer(string path){try{using(var f=File.OpenRead(path)){if(f.Length<64)return false;f.Seek(-64,SeekOrigin.End);byte[] b=new byte[16];f.Read(b,0,16);return Encoding.ASCII.GetString(b)==Magic;}}catch{return false;}}
 public static Stream Open(){string external=Program.Arg("--payload",null),source=external??Application.ExecutablePath;if(external!=null&&!HasTrailer(source))return File.OpenRead(source);var f=File.OpenRead(source);try{f.Seek(-64,SeekOrigin.End);using(var r=new BinaryReader(f,Encoding.ASCII,true)){if(Encoding.ASCII.GetString(r.ReadBytes(16))!=Magic)throw new InvalidDataException("The BOF setup payload is missing.");long start=r.ReadInt64(),size=r.ReadInt64();if(start<0||size<1||start+size+64!=f.Length)throw new InvalidDataException("The installer is incomplete. Download it again.");return new BoundedStream(f,start,size);}}catch{f.Dispose();throw;}}
}
sealed class PackageFile {public string path {get;set;} public long bytes {get;set;} public string sha256 {get;set;}}
sealed class PackageManifest {public string product {get;set;} public string version {get;set;} public long bytes {get;set;} public List<PackageFile> files {get;set;}}
static class Installer {
 const string RegistryPath="Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ColeForgeBulletsOfFury";
 // Use the explicit Win32 namespace after SafePath validation. This does not
 // depend on a machine-wide long-path registry change or administrator rights.
 static string IOPath(string path){if(path.StartsWith(@"\\?\"))return path;string full=Path.GetFullPath(path);return full.StartsWith(@"\\")?@"\\?\UNC\"+full.Substring(2):@"\\?\"+full;}
 public static string SafePath(string root,string relative){
  root=Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar;if(Path.IsPathRooted(relative))throw new InvalidDataException("Absolute path in payload.");string file=Path.GetFullPath(Path.Combine(root,relative.Replace('/',Path.DirectorySeparatorChar)));if(!file.StartsWith(root,StringComparison.OrdinalIgnoreCase))throw new InvalidDataException("Unsafe path in payload.");
  string baseFolder=root.TrimEnd(Path.DirectorySeparatorChar);for(string dir=Path.GetDirectoryName(file);dir!=null&&dir.Length>=baseFolder.Length;dir=Path.GetDirectoryName(dir)){if(Directory.Exists(dir)&&(File.GetAttributes(dir)&FileAttributes.ReparsePoint)!=0)throw new InvalidDataException("An install folder contains a linked directory. Choose a plain game folder.");if(String.Equals(dir,baseFolder,StringComparison.OrdinalIgnoreCase))break;}return file;
 }
 public static bool IsInstalled(string target){try{string p=Path.Combine(target,"BOF-INSTALL.json");var d=new JavaScriptSerializer().Deserialize<Dictionary<string,object>>(File.ReadAllText(p));return (string)d["product"]==Program.Product&&File.Exists(Path.Combine(target,"Bullets of Fury.exe"));}catch{return false;}}
 public static void Install(string target,bool shortcuts,CancellationToken token,Action<double,string> progress){
  target=Path.GetFullPath(target).TrimEnd(Path.DirectorySeparatorChar);string parent=Path.GetDirectoryName(target);if(parent==null||target==Path.GetPathRoot(target))throw new InvalidOperationException("Choose a dedicated game folder.");
  if(Directory.Exists(target))throw new InvalidOperationException("That game folder already exists. Choose a new installation folder to keep its files safe.");Directory.CreateDirectory(parent);string staging=Path.Combine(parent,".bof-install-"+Guid.NewGuid().ToString("N"));Directory.CreateDirectory(staging);bool moved=false;
  try{
   using(var zip=new ZipArchive(Payload.Open(),ZipArchiveMode.Read,false)){
    var json=new JavaScriptSerializer{MaxJsonLength=32*1024*1024};PackageManifest manifest;using(var sr=new StreamReader(zip.GetEntry("DEPLOY-MANIFEST.json").Open()))manifest=json.Deserialize<PackageManifest>(sr.ReadToEnd());if(manifest.product!=Program.Product)throw new InvalidDataException("Wrong BOF payload.");
    var drive=new DriveInfo(Path.GetPathRoot(target));if(drive.AvailableFreeSpace<manifest.bytes+512L*1024*1024)throw new IOException("Not enough disk space. Allow at least "+Math.Ceiling(manifest.bytes/1073741824.0+.5)+" GB free.");
    long done=0;Stopwatch update=Stopwatch.StartNew();byte[] buffer=new byte[128*1024];
    foreach(var row in manifest.files){token.ThrowIfCancellationRequested();ZipArchiveEntry entry=zip.GetEntry(row.path);if(entry==null||entry.Length!=row.bytes)throw new InvalidDataException("Missing or damaged package file: "+row.path);string path=SafePath(staging,row.path);Directory.CreateDirectory(Path.GetDirectoryName(path));
     using(var input=entry.Open())using(var output=new FileStream(IOPath(path),FileMode.CreateNew,FileAccess.Write,FileShare.None))using(var sha=SHA256.Create()){
      int n;while((n=input.Read(buffer,0,buffer.Length))>0){token.ThrowIfCancellationRequested();output.Write(buffer,0,n);sha.TransformBlock(buffer,0,n,null,0);done+=n;if(update.ElapsedMilliseconds>70){progress(.96*done/manifest.bytes,"INSTALLING "+(done/1048576)+" / "+(manifest.bytes/1048576)+" MB");update.Restart();}}
      sha.TransformFinalBlock(new byte[0],0,0);string hash=BitConverter.ToString(sha.Hash).Replace("-","").ToLowerInvariant();if(hash!=row.sha256)throw new InvalidDataException("Package verification failed: "+row.path);
     }
    }
    token.ThrowIfCancellationRequested();File.WriteAllText(Path.Combine(staging,"DEPLOY-MANIFEST.json"),json.Serialize(manifest));
    // The manifest is the ownership ledger. Uninstall never recursively deletes arbitrary user files.
    File.WriteAllText(Path.Combine(staging,"BOF-INSTALL.json"),json.Serialize(new{product=Program.Product,version=manifest.version,installedUtc=DateTime.UtcNow.ToString("o"),shortcuts=shortcuts,registered=!Program.Has("--no-register"),files=manifest.files.Select(x=>x.path).Concat(new[]{"DEPLOY-MANIFEST.json","BOF-INSTALL.json"}).ToArray()}));
   }
   progress(.99,"CHECKING WINDOWS GAME RUNTIME");EnsureRuntime(staging);token.ThrowIfCancellationRequested();Directory.Move(staging,target);moved=true;
   if(!Program.Has("--no-register"))Register(target,shortcuts);progress(1,"INSTALL COMPLETE - ALL FILES VERIFIED");Program.Log("install-complete",new{target,shortcuts,files=Directory.GetFiles(target,"*",SearchOption.AllDirectories).Length});
  }finally{if(!moved&&Directory.Exists(staging)){string full=Path.GetFullPath(staging);string expected=Path.GetFullPath(parent).TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar;if(!full.StartsWith(expected,StringComparison.OrdinalIgnoreCase)||!Path.GetFileName(full).StartsWith(".bof-install-"))throw new InvalidOperationException("Refusing unsafe staging cleanup.");Directory.Delete(full,true);}}
 }
 static void EnsureRuntime(string staging){
  try{if(!String.IsNullOrEmpty(CoreWebView2Environment.GetAvailableBrowserVersionString()))return;}catch{}
  string file=Path.Combine(staging,"runtime","MicrosoftEdgeWebView2RuntimeInstallerX64.exe");if(!File.Exists(file))throw new FileNotFoundException("The offline Windows game runtime is missing.");
  var p=Process.Start(new ProcessStartInfo(file,"/silent /install"){UseShellExecute=false,CreateNoWindow=true});p.WaitForExit();if(p.ExitCode!=0&&p.ExitCode!=3010)throw new Exception("Windows runtime setup returned "+p.ExitCode+". Please run the included runtime installer and retry.");
  if(String.IsNullOrEmpty(CoreWebView2Environment.GetAvailableBrowserVersionString()))throw new Exception("Windows runtime needs a restart before BOF can run.");
 }
 static bool OwnsShortcut(string path,string exe){
  if(!File.Exists(path))return false;try{Type t=Type.GetTypeFromProgID("WScript.Shell");dynamic shell=Activator.CreateInstance(t);dynamic link=shell.CreateShortcut(path);string dest=link.TargetPath as string;Marshal.FinalReleaseComObject(link);Marshal.FinalReleaseComObject(shell);return String.Equals(Path.GetFullPath(dest),Path.GetFullPath(exe),StringComparison.OrdinalIgnoreCase);}catch{return false;}
 }
 static void Shortcut(string path,string exe,string arguments){
  if(File.Exists(path)&&!OwnsShortcut(path,exe)){Program.Log("shortcut-preserved",path);return;}
  Type t=Type.GetTypeFromProgID("WScript.Shell");dynamic shell=Activator.CreateInstance(t);dynamic link=shell.CreateShortcut(path);link.TargetPath=exe;link.Arguments=arguments;link.WorkingDirectory=Path.GetDirectoryName(exe);link.IconLocation=exe+",0";link.Description="Bullets of Fury - ColeForge";link.Save();Marshal.FinalReleaseComObject(link);Marshal.FinalReleaseComObject(shell);
 }
 static void Register(string target,bool shortcuts){
  string exe=Path.Combine(target,"Bullets of Fury.exe"),group=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs),"ColeForge","Bullets of Fury");if(shortcuts){Directory.CreateDirectory(group);Shortcut(Path.Combine(group,"Bullets of Fury.lnk"),exe,"");Shortcut(Path.Combine(group,"BOF Launcher.lnk"),Path.Combine(target,"BOF Launcher.exe"),"");Shortcut(Path.Combine(group,"Uninstall Bullets of Fury.lnk"),exe,"--uninstall");Shortcut(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory),"Bullets of Fury.lnk"),exe,"");}
  using(var k=Registry.CurrentUser.CreateSubKey(RegistryPath)){k.SetValue("DisplayName","Bullets of Fury");k.SetValue("Publisher","ColeForge");k.SetValue("DisplayVersion","2026.11.06");k.SetValue("InstallLocation",target);k.SetValue("DisplayIcon",exe);k.SetValue("UninstallString","\""+exe+"\" --uninstall");k.SetValue("NoModify",1);k.SetValue("NoRepair",1);}
 }
 public static bool OtherWindowRunning(string target){foreach(string name in new[]{"Bullets of Fury","BOF Launcher"}){string exe=Path.GetFullPath(Path.Combine(target,name+".exe"));foreach(var p in Process.GetProcessesByName(name)){try{if(p.Id!=Process.GetCurrentProcess().Id&&String.Equals(p.MainModule.FileName,exe,StringComparison.OrdinalIgnoreCase))return true;}catch{}}}return false;}
 public static void StartUninstall(string target){
  string temp=Path.Combine(Path.GetTempPath(),"BOF-Uninstall-"+Guid.NewGuid().ToString("N"));Directory.CreateDirectory(temp);string exe=Path.Combine(temp,"BOF-Uninstall.exe");File.Copy(Application.ExecutablePath,exe);string args="--uninstall-worker \""+target+"\" --wait-pid "+Process.GetCurrentProcess().Id;if(Program.QaDir!=null)args+=" --qa-dir \""+Program.QaDir+"\"";Process.Start(new ProcessStartInfo(exe,args){UseShellExecute=false,CreateNoWindow=true});
 }
 public static void UninstallWorker(){
  string target=Path.GetFullPath(Program.Arg("--uninstall-worker",""));int pid=Int32.Parse(Program.Arg("--wait-pid","0"));if(pid>0)try{Process.GetProcessById(pid).WaitForExit(20000);}catch{}if(!IsInstalled(target))throw new Exception("Uninstall ownership marker is missing.");
  var j=new JavaScriptSerializer{MaxJsonLength=32*1024*1024};var data=j.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(target,"BOF-INSTALL.json")));var files=((System.Collections.IEnumerable)data["files"]).Cast<object>().Select(x=>(string)x).ToArray();
  foreach(string name in files){string file=SafePath(target,name);if(File.Exists(IOPath(file)))File.Delete(IOPath(file));}
  var ownedFolders=new HashSet<string>(StringComparer.OrdinalIgnoreCase);foreach(string name in files){string dir=Path.GetDirectoryName(SafePath(target,name));while(dir!=null&&!String.Equals(dir,target,StringComparison.OrdinalIgnoreCase)){ownedFolders.Add(dir);dir=Path.GetDirectoryName(dir);}}
  foreach(string folder in ownedFolders.OrderByDescending(x=>x.Length))if(Directory.Exists(folder)&&Directory.GetFileSystemEntries(folder).Length==0)Directory.Delete(folder);if(Directory.GetFileSystemEntries(target).Length==0)Directory.Delete(target);
  bool registered=data.ContainsKey("registered")?(bool)data["registered"]:data.ContainsKey("shortcuts")&&(bool)data["shortcuts"];if(registered){using(var k=Registry.CurrentUser.OpenSubKey(RegistryPath)){if(k!=null&&String.Equals(k.GetValue("InstallLocation")as string,target,StringComparison.OrdinalIgnoreCase))Registry.CurrentUser.DeleteSubKeyTree(RegistryPath,false);}string group=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs),"ColeForge","Bullets of Fury");foreach(string path in new[]{Path.Combine(group,"Bullets of Fury.lnk"),Path.Combine(group,"Uninstall Bullets of Fury.lnk"),Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory),"Bullets of Fury.lnk")})if(OwnsShortcut(path,Path.Combine(target,"Bullets of Fury.exe")))File.Delete(path);if(Directory.Exists(group)&&Directory.GetFileSystemEntries(group).Length==0)Directory.Delete(group);}
  if(registered){string group=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs),"ColeForge","Bullets of Fury"),link=Path.Combine(group,"BOF Launcher.lnk");if(OwnsShortcut(link,Path.Combine(target,"BOF Launcher.exe")))File.Delete(link);if(Directory.Exists(group)&&Directory.GetFileSystemEntries(group).Length==0)Directory.Delete(group);}
  Program.Log("uninstall-complete",new{target,saveFolderPreserved=Preferences.Folder});
 }
}
static class SelfTests {
 public static void Run(){
  var checks=new List<object>();Action<string,bool> ck=(n,v)=>{checks.Add(new{name=n,passed=v});if(!v)throw new Exception("Self-test failed: "+n);};
  string root=Path.Combine(Path.GetTempPath(),"BOF-owned");ck("Relative package path stays under install root",Installer.SafePath(root,"game/assets/x.png").StartsWith(root));bool escaped=false;try{Installer.SafePath(root,"../outside.txt");}catch(InvalidDataException){escaped=true;}ck("Traversal is rejected",escaped);escaped=false;try{Installer.SafePath(root,"C:\\Windows\\x");}catch(InvalidDataException){escaped=true;}ck("Absolute payload paths are rejected",escaped);
  foreach(int h in new[]{10,12,14,21,28})ck("Font "+h+" retains full R/5 extents",PixelFont.At(h).Width("READY 50/50")>0);
  foreach(string n in new[]{"hangar","doors","briefing"})ck(n+" plate has exact logical size",Art.Get(n).Size==new Size(1024,576));int[] motion=Encoding.ASCII.GetString(Art.Bytes("door-motion.csv")).Trim().Split(',').Select(Int32.Parse).ToArray();ck("96 authored door motion keys start/end without jumps",motion.Length==96&&motion[0]==0&&motion[95]==512&&motion.Zip(motion.Skip(1),(a,b)=>b-a).All(x=>x>=0&&x<=9));
  using(var m=new MemoryStream(new byte[]{0,1,2,3,4,5}))using(var b=new BoundedStream(m,2,3)){ck("Embedded payload begins at its own origin",b.ReadByte()==2&&b.Length==3);b.Seek(-1,SeekOrigin.End);ck("Embedded payload end is bounded",b.ReadByte()==4&&b.ReadByte()==-1);}
  if(Program.Has("--payload")&&Program.QaDir!=null){string cancelRoot=Path.Combine(Program.QaDir,"cancelled-game");var c=new CancellationTokenSource();c.Cancel();bool cancelled=false;try{Installer.Install(cancelRoot,false,c.Token,(p,s)=>{});}catch(OperationCanceledException){cancelled=true;}ck("Cancelled extraction leaves no partial game",cancelled&&!Directory.Exists(cancelRoot)&&Directory.GetDirectories(Program.QaDir,".bof-install-*").Length==0);}
  Program.Log("self-tests",checks);if(Program.QaDir!=null)File.WriteAllText(Path.Combine(Program.QaDir,"self-tests.json"),new JavaScriptSerializer().Serialize(checks));
 }
}
