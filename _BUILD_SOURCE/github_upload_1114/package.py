from pathlib import Path
import io,os,json,hashlib,struct,zipfile,copy,time,subprocess,shutil,urllib.parse,zlib
from github_api import R,REPO,session,api
from remote_zip import PartsReader
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';TAG='bof-windows-2026-11-14-revg';VERSION='2026.11.14g';PREFIX='BulletsOfFury-Setup-2026-11-14-RevG.exe';s=session();source=json.loads((O/'source-upload.json').read_text());base=json.loads((O/'remote.json').read_text())['base'];hostmeta=json.loads((O/'base-host.json').read_text());start=time.monotonic();uploaded=[];live={};limit=256*1024*1024
def state(**kw):
 live.update(kw);(O/'live-build.json').write_text(json.dumps(live,indent=2))
body='''Current Windows build with all November14 source, authored art and gameplay changes. Includes restored Chronus/Draconus hammer and rage attacks, ship and gun work, Stage5 bomber pursuit and continuously rotating/flashing/beeping targeting, current pilot/playtest improvements, and the shared health-helper fix.\n\nFull regression suite:8,969 passed,0 failures. Native bomber/weapon:60 passed. Targeting:7 passed.\n\nDownload BOF-Install-Helper-RevG.zip, extract it, and run Install-BulletsOfFury.cmd. It downloads the verified installer parts, joins and verifies them, then opens the existing Fury HQ graphical setup. All game art/audio, the Windows launcher, and the offline Microsoft WebView2 runtime are included. Windows10/11 x64. Allow at least16GB free during download/setup.\n\nThis is the current development prerelease for playtesting; the full unassisted experience/balance review is still pending. Earlier releases remain available.\n'''
existing=api(s,'GET','repos/'+REPO+'/releases?per_page=100');release=next((r for r in existing if r['tag_name']==TAG),None)
if release:
 assert release['draft']and not release['assets'],'A release already contains uploaded parts; resume from its receipt rather than overwriting.'
else:release=api(s,'POST','repos/'+REPO+'/releases',json=dict(tag_name=TAG,target_commitish=source['commit'],name='Bullets of Fury — November 14 current Windows build (Rev G)',body=body,draft=True,prerelease=True))
(O/'draft-release.json').write_text(json.dumps(release,indent=2));rid=release['id'];print('DRAFT',TAG,'source',source['commit'],flush=True)
class ProgressFile:
 def __init__(self,f,size,name):self.f=f;self.size=size;self.name=name;self.sent=0;self.last=0
 def read(self,n=-1):
  b=self.f.read(n);self.sent+=len(b)
  if self.sent-self.last>=64*1024*1024:self.last=self.sent;state(phase='uploading',part=self.name,sent=self.sent,partBytes=self.size);print('UPLOADING',self.name,round(self.sent/self.size*100),'%',flush=True)
  return b
def upload(path,remove=False):
 size=path.stat().st_size;h=hashlib.sha256()
 with path.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 digest=h.hexdigest();url='https://uploads.github.com/repos/'+REPO+'/releases/'+str(rid)+'/assets?name='+urllib.parse.quote(path.name)
 state(phase='uploading',part=path.name,sent=0,partBytes=size)
 with path.open('rb')as f:
  response=s.request('POST',url,data=ProgressFile(f,size,path.name),headers={'Content-Type':'application/octet-stream','Content-Length':str(size)},timeout=3600)
 assert response.ok,'Upload HTTP '+str(response.status_code)+' '+response.text[:200];remote=response.json();assert remote['size']==size and remote['state']=='uploaded'and remote.get('digest')=='sha256:'+digest,'Server checksum mismatch'
 row=dict(name=path.name,bytes=size,sha256=digest,id=remote['id'],url=remote['browser_download_url'],apiUrl=remote['url'],verified=True);uploaded.append(row);(O/'uploaded-assets.json').write_text(json.dumps(uploaded,indent=2));print('UPLOADED AND SHA256 VERIFIED',path.name,size,flush=True)
 if remove:
  assert path.resolve().parent==O.resolve()and path.name.startswith(PREFIX+'.part');path.unlink()
 return row
class PartsSink:
 def __init__(self):self.total=0;self.whole=hashlib.sha256();self.fp=None;self.part=0;self.used=0
 def tell(self):return self.total
 def flush(self):
  if self.fp:self.fp.flush()
 def next(self):
  self.part+=1;self.path=O/(PREFIX+'.part'+str(self.part));assert not self.path.exists();self.fp=self.path.open('xb');self.used=0
 def finishPart(self):
  if self.fp:self.fp.close();self.fp=None;upload(self.path,remove=True)
 def write(self,data):
  original=len(data);view=memoryview(data);self.whole.update(data)
  while view:
   if self.fp is None:self.next()
   take=min(len(view),limit-self.used);self.fp.write(view[:take]);self.used+=take;self.total+=take;view=view[take:]
   if self.used==limit:self.finishPart()
  return original
class Payload:
 def __init__(self,sink,offset):self.sink=sink;self.offset=offset;self.hash=hashlib.sha256()
 def write(self,b):self.hash.update(b);return self.sink.write(b)
 def tell(self):return self.sink.tell()-self.offset
 def seek(self,*a):raise OSError('streaming installer')
 def flush(self):self.sink.flush()
 def seekable(self):return False
def sha(path):
 h=hashlib.sha256()
 with path.open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
host=W/'host';readme='''BULLETS OF FURY — NOVEMBER14,2026 / WINDOWS REVISION G

This is the complete current game, including all artwork/audio and Fury HQ.
Download/extract BOF-Install-Helper-RevG.zip, then run Install-BulletsOfFury.cmd.
The helper downloads each installer part, verifies SHA256, joins them in order,
verifies the complete EXE, then opens graphical setup. Keep the parts together.
Allow16GB free for download, assembled installer and installed game.

Play: Bullets of Fury.exe. Launcher: BOF Launcher.exe.
Windows10/11 x64. Offline WebView2 runtime is included. The host is unsigned.
No Python, Node, separate browser or web server is required to play.
F11/Alt+Enter toggles fullscreen. Fire: left-click/J. Retina: right-click/C.
Missiles: Space/K. Multi-Retina: Mouse4/Y or right tap then right-click/hold.
Move: WASD/arrows. Charge: H/Mouse5. Pause: Enter/P.
Saves remain in LocalAppData/ColeForge/BulletsOfFury, separate from browser saves.

All current source/art changes are on GitHub main and the production branch.
Full suite:8,969 passed,0 failures;60 native bomber/weapon and7 targeting checks.
Current development prerelease; full unassisted playtest/balance review pending.
'''
(host/'READ-ME.txt').write_text(readme,encoding='utf-8');(host/'DESKTOP-BUILD.json').write_text(json.dumps(dict(product='ColeForge.BulletsOfFury.2026',version=VERSION,gameBuild=source['commit'],defaultFullscreen=True,gameExecutable='Bullets of Fury.exe',launcherExecutable='BOF Launcher.exe',hostSha256=hostmeta['stubSha256'],gameJsSha256=sha(R/'assets/game.js'),fullAssertions=8969,fullFailures=0),indent=2))
files={p.name:p for p in host.iterdir()if p.is_file()}
for root in ['assets','extensions']:
 for p in(R/root).rglob('*'):
  if p.is_file():assert p.resolve().is_relative_to(R.resolve());files['game/'+p.relative_to(R).as_posix()]=p
files['game/index.html']=R/'index.html';files['game/HOW_TO_PLAY.txt']=R/'HOW_TO_PLAY.txt'
buildinfo=dict(product='Bullets of Fury',version=VERSION,sourceCommit=source['commit'],gameJsSha256=sha(R/'assets/game.js'),fullAssertions=8969,fullFailures=0,nativeBomberChecks=60,targetingChecks=7,hostSha256=hostmeta['stubSha256']);(O/'BUILD-INFO.json').write_text(json.dumps(buildinfo,indent=2));files['game/BUILD-INFO.json']=O/'BUILD-INFO.json'
tracked={}
for line in subprocess.check_output(['git','-C',str(R),'ls-tree','-r','--full-tree','HEAD','--','assets','extensions','index.html','HOW_TO_PLAY.txt']).decode().splitlines():
 attrs,name=line.split('\t',1);tracked['game/'+name]=attrs.split()[2]
(O/'package-inputs.json').write_text(json.dumps({name:str(p)for name,p in files.items()},indent=2));rows=[];sink=PartsSink();stub=(host/'Bullets of Fury.exe').read_bytes();assert hashlib.sha256(stub).hexdigest()==hostmeta['stubSha256'];sink.write(stub);payload=Payload(sink,len(stub));baseParts=sorted([p for p in base['assets']if'.exe.part'in p['name']],key=lambda p:p['name']);reader=PartsReader(baseParts,s)
with zipfile.ZipFile(payload,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True)as z:
 for i,(name,p)in enumerate(sorted(files.items())):
  info=zipfile.ZipInfo.from_file(p,name);info.compress_type=zipfile.ZIP_DEFLATED;info._compresslevel=1;h=hashlib.sha256();gitHash=hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0');size=0;stat=p.stat()
  with p.open('rb')as f,z.open(info,'w',force_zip64=True)as target:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b);gitHash.update(b);target.write(b);size+=len(b)
  assert p.stat().st_size==stat.st_size and p.stat().st_mtime_ns==stat.st_mtime_ns,'Source changed during packaging: '+name
  if name in tracked:assert gitHash.hexdigest()==tracked[name],'Packaged bytes differ from committed source: '+name
  rows.append(dict(path=name,bytes=size,sha256=h.hexdigest()))
  if i%1500==0:state(phase='building',files=i,totalFiles=len(files),written=sink.total);print('PACKAGED',i,'/',len(files),'installer MB',round(sink.total/1e6),flush=True)
 # Carry the exact signed offline runtime record, checking its stored bytes.
 with zipfile.ZipFile(reader)as original:
  item=original.getinfo('runtime/MicrosoftEdgeWebView2RuntimeInstallerX64.exe');assert item.compress_type==zipfile.ZIP_STORED and not(item.flag_bits&8);reader.seek(item.header_offset);header=reader.read(30);assert header[:4]==b'PK\x03\x04';fname,extra=struct.unpack('<HH',header[26:30]);new=copy.copy(item);new.header_offset=payload.tell();payload.write(header+reader.read(fname+extra));h=hashlib.sha256();left=item.compress_size
  while left:
   b=reader.read(min(left,1024*1024));assert b;h.update(b);payload.write(b);left-=len(b)
  assert h.hexdigest()==hostmeta['runtime']['row']['sha256'];rows.append(hostmeta['runtime']['row']);z.filelist.append(new);z.NameToInfo[new.filename]=new;z.start_dir=payload.tell();z._didModify=True
 manifest=dict(product='ColeForge.BulletsOfFury.2026',version=VERSION,sourceCommit=source['commit'],bytes=sum(q['bytes']for q in rows),files=rows);z.writestr('DEPLOY-MANIFEST.json',json.dumps(manifest,separators=(',',':')))
 assert len(z.filelist)==len(set(z.namelist()))==len(rows)+1
length=payload.tell();footer=b'BOFSETUP1106DATA'+struct.pack('<qq',len(stub),length)+payload.hash.digest();assert len(footer)==64;sink.write(footer);sink.finishPart();whole=sink.whole.hexdigest()
receipt=dict(tag=TAG,version=VERSION,releaseId=rid,sourceCommit=source['commit'],installerName=PREFIX,installerBytes=sink.total,installerSha256=whole,payloadSha256=payload.hash.hexdigest(),payloadBytes=length,stubBytes=len(stub),files=len(rows),unpackedBytes=manifest['bytes'],parts=uploaded.copy(),seconds=time.monotonic()-start,inputFilesMatchGit=True)
(O/'DEPLOY-MANIFEST.json').write_text(json.dumps(manifest,separators=(',',':')));(O/'package-receipt.json').write_text(json.dumps(receipt,indent=2));(O/'READ-ME.txt').write_text(readme,encoding='utf-8');print('COMPLETE INSTALLER UPLOADED',sink.total,'bytes in',len(uploaded),'verified parts',flush=True)
