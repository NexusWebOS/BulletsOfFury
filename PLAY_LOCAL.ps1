param([switch]$NoBrowser, [int]$DurationSeconds=0, [int]$Port=8790)
$ErrorActionPreference='Stop'
$gameRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
public static class FuryLocalServer {
 static string root; static TcpListener listener;
 public static int Start(string folder,int port) {
  root=Path.GetFullPath(folder)+Path.DirectorySeparatorChar;
  listener=new TcpListener(IPAddress.Loopback,port);listener.Start();
  ThreadPool.QueueUserWorkItem(delegate { while(true) { try {
   TcpClient c=listener.AcceptTcpClient();ThreadPool.QueueUserWorkItem(delegate { Serve(c); });
  } catch { break; } } });
  return ((IPEndPoint)listener.LocalEndpoint).Port;
 }
 static void Headers(NetworkStream s,string status,string mime,long length,string extra) {
  byte[] h=Encoding.ASCII.GetBytes("HTTP/1.1 "+status+"\r\nContent-Type: "+mime+"\r\nContent-Length: "+length+"\r\nConnection: close\r\nAccept-Ranges: bytes\r\nX-Content-Type-Options: nosniff\r\n"+extra+"\r\n");s.Write(h,0,h.Length);
 }
 static void Serve(TcpClient c) { using(c) { try {
  c.ReceiveTimeout=5000;c.SendTimeout=10000;NetworkStream s=c.GetStream();
  StreamReader r=new StreamReader(s,Encoding.ASCII,false,4096,true);
  string line=r.ReadLine();if(line==null)return;string[] req=line.Split(' ');
  if(req.Length<2||!(req[0]=="GET"||req[0]=="HEAD")){Headers(s,"405 Method Not Allowed","text/plain",0,"");return;}
  string range=null;int count=0;while(!String.IsNullOrEmpty(line=r.ReadLine())) {
   if(++count>100)return;if(line.StartsWith("Range:",StringComparison.OrdinalIgnoreCase))range=line.Substring(6).Trim();
  }
  string rel=Uri.UnescapeDataString(req[1].Split('?')[0]).TrimStart('/').Replace('/',Path.DirectorySeparatorChar);
  if(rel.Length==0)rel="index.html";string file=Path.GetFullPath(Path.Combine(root,rel));
  if(!file.StartsWith(root,StringComparison.OrdinalIgnoreCase)||!File.Exists(file)){Headers(s,"404 Not Found","text/plain",0,"");return;}
  using(FileStream f=File.OpenRead(file)) {
   long start=0,end=f.Length-1;bool partial=false;
   if(range!=null&&range.StartsWith("bytes=")) {
    string[] parts=range.Substring(6).Split('-');long n;
    if(parts.Length!=2||!Int64.TryParse(parts[0],out start)||start<0||start>=f.Length){Headers(s,"416 Range Not Satisfiable","text/plain",0,"Content-Range: bytes */"+f.Length+"\r\n");return;}
    if(Int64.TryParse(parts[1],out n))end=Math.Min(n,end);if(end<start){Headers(s,"416 Range Not Satisfiable","text/plain",0,"");return;}partial=true;
   }
   string mime;switch(Path.GetExtension(file).ToLowerInvariant()) {
    case ".html":mime="text/html; charset=utf-8";break;case ".js":mime="application/javascript; charset=utf-8";break;
    case ".css":mime="text/css";break;case ".json":mime="application/json";break;case ".webp":mime="image/webp";break;
    case ".gif":mime="image/gif";break;case ".avif":mime="image/avif";break;case ".svg":mime="image/svg+xml";break;case ".png":mime="image/png";break;case ".jpg":case ".jpeg":mime="image/jpeg";break;case ".mp3":mime="audio/mpeg";break;
    case ".wav":mime="audio/wav";break;case ".ogg":mime="audio/ogg";break;case ".woff2":mime="font/woff2";break;case ".woff":mime="font/woff";break;case ".ttf":mime="font/ttf";break;case ".mp4":mime="video/mp4";break;case ".webm":mime="video/webm";break;case ".m4a":mime="audio/mp4";break;case ".wasm":mime="application/wasm";break;default:mime="application/octet-stream";break;
   }
   long remaining=Math.Max(0,end-start+1);Headers(s,partial?"206 Partial Content":"200 OK",mime,remaining,partial?"Content-Range: bytes "+start+"-"+end+"/"+f.Length+"\r\n":"");
   if(req[0]=="HEAD")return;f.Position=start;byte[] buffer=new byte[65536];
   while(remaining>0){int n=f.Read(buffer,0,(int)Math.Min(buffer.Length,remaining));if(n<=0)break;s.Write(buffer,0,n);remaining-=n;}
  }
 } catch { } } }
 public static void Stop(){if(listener!=null)listener.Stop();}
}
'@
# A stable default origin keeps the tester's saves across restarts.
# Port 0 is reserved for isolated verification.
$buildInfo=Join-Path $gameRoot 'BUILD-INFO.json'
$buildId=if(Test-Path -LiteralPath $buildInfo){(Get-Content -LiteralPath $buildInfo -Raw | ConvertFrom-Json).buildId}else{'local'}
$localPort=$null
$candidates=if($Port -eq 0){@(0)}else{@($Port..($Port+9))}
foreach($candidate in $candidates){
 if($candidate -gt 0){
  try{
   $running=Invoke-RestMethod -Uri "http://127.0.0.1:$candidate/BUILD-INFO.json" -TimeoutSec 1
   if($running.buildId -eq $buildId -and $buildId -ne 'local'){
    $gameUrl="http://127.0.0.1:$candidate/index.html"
    Write-Output "BULLETS OF FURY READY: $gameUrl"
    if(!$NoBrowser){Start-Process $gameUrl}
    return
   }
  }catch{}
 }
 try{$localPort=[FuryLocalServer]::Start($gameRoot,[int]$candidate);break}catch{if($candidate -eq 0){throw}}
}
if($null -eq $localPort){throw 'The local game ports are busy. Close an older game server window and try again.'}
$gameUrl="http://127.0.0.1:$localPort/index.html"
Write-Output "BULLETS OF FURY READY: $gameUrl"
if(!$NoBrowser){Start-Process $gameUrl}
try {
 if($DurationSeconds -gt 0){Start-Sleep -Seconds $DurationSeconds}
 else {[void](Read-Host 'Leave this window open while playing. Press Enter to stop')}
} finally {[FuryLocalServer]::Stop()}
