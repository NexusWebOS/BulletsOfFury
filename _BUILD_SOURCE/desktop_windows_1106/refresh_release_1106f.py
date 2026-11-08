from pathlib import Path
import zipfile,json,hashlib,struct,time,copy,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parent/'Releases';T=O/'BulletsOfFury-Windows-2026-11-06';B=W/'host';out=O/'BulletsOfFury-Setup-2026-11-06.exe'
gamefiles=['assets/game.js','assets/stage3_combat_1004k.js','assets/menu_sceneries_1103.js','assets/projectile_contract_1106.js','assets/pixelmap_ui_1027.js','assets/playthrough_ui_1011.js','assets/locked_pilot_art_1106.js','assets/locked_pilot_1106.js','assets/data/ART_TAXONOMY.json','index.html']
gamefiles += [p.relative_to(R).as_posix()for p in (R/'assets/game/shared/combat/space_pages_1106').iterdir()if p.is_file()]
gamefiles += ['assets/layered_stages_1102.js','assets/audio_latency_1106.js','assets/campaign_controls_1004h.js','assets/pixel_glow_1015.js','assets/space_pages_1106.js','assets/space_pages_art_1106.js','HOW_TO_PLAY.txt']
gamefiles += [p.relative_to(R).as_posix()for p in (R/'assets/game/shared/ui/locked_pilot_1106').iterdir()if p.is_file()]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for data in iter(lambda:f.read(4*1024*1024),b''):h.update(data)
 return h.hexdigest()
readme='''BULLETS OF FURY - WINDOWS EDITION / NOVEMBER 6 REVISION F

PLAY NOW: double-click Bullets of Fury.exe. The real game starts FULLSCREEN
automatically. F11 or Alt+Enter switches between fullscreen and windowed play.
FURY HQ: double-click BOF Launcher.exe for the animated graphical launcher.
Its upper-right buttons minimize, maximize/restore and close the window.

Fire: left-click / J. Retina: right-click / C. Missiles: Space / K.
Multi-Retina: hold Mouse Button 4 / Y, or right-tap then right-click and hold.
Move: WASD / arrows. Charge: H / Mouse Button 5. Pause: Enter / P.

TUTORIAL / MAP: Enter/Start confirms deployment. Back/Esc opens the menu.
Quick mission clicks are buffered; Save and Load remain separate choices.
SHORT SFX: bounded decoded playback cache, shared mixer and native cue gates.
STAGE 5: smaller kit pieces; original blue sky, cloud assembly and starfield.\nSPACE: bounded image decode queue and faster stage asset lookup, same art.
FLAMETHROWER: +27 visible pixels of range at levels 1-5, upgraded damage progression.

All nine pilot selection screens use their own solid 16-bit palette fill.
Locked Cole has synchronized gray/black pilot, jet and padlock frames with
neutral black/gray backgrounds. His real password restores full-color artwork.
Enemy machine-gun bullets and sonic pressure waves cannot be shot down.
Physical missiles retain their authored interception behavior.

All game assets and the offline Microsoft WebView2 runtime are included.
Windows 10/11 x64. No Python, Node, web server or separate browser is needed.
Saves live in LocalAppData/ColeForge/BulletsOfFury and survive uninstalling.
Existing browser saves remain separate from this desktop game profile.
The game executable is not code-signed.
'''
(B/'READ-ME.txt').write_text(readme,encoding='ascii')
meta=json.loads((B/'DESKTOP-BUILD.json').read_text());meta.update(version='2026.11.06f',defaultFullscreen=True,gameExecutable='Bullets of Fury.exe',launcherExecutable='BOF Launcher.exe',gameJsSha256=digest(R/'assets/game.js'),revision='Stage5 assembly pieces reduced from194.7px to64px cells with original jet/final ship sizes; Stage5 original ascent sky and starfield/parallax restored; no city or orbital overlay / tutorial deployment and buffered map clicks / decoded low-latency SFX / bounded high-quality space loading / flame range +27px and balanced fire damage; all revision C features retained')
(B/'DESKTOP-BUILD.json').write_text(json.dumps(meta,indent=2))
buildinfo=T/'game/BUILD-INFO.json'
if buildinfo.exists():
 data=json.loads(buildinfo.read_text(encoding='utf-8-sig'));data['desktopRevision']=meta;buildinfo.write_text(json.dumps(data,indent=2))
extras={p.name:p for p in B.iterdir()if p.is_file()}
extras.update({'game/'+n:R/n for n in gamefiles})
if buildinfo.exists():extras['game/BUILD-INFO.json']=buildinfo
start=time.time();temp=out.with_suffix('.exe.partial');stub=B/'Bullets of Fury.exe';offset=stub.stat().st_size
class RelativeFile:
 def __init__(self,f,base):self.f=f;self.base=base
 def tell(self):return self.f.tell()-self.base
 def seek(self,n,whence=0):return self.f.seek(n+self.base if whence==0 else n,whence)-self.base
 def write(self,data):return self.f.write(data)
 def read(self,n=-1):return self.f.read(n)
 def flush(self):self.f.flush()
 def seekable(self):return True
with zipfile.ZipFile(out)as src,out.open('rb')as raw,temp.open('w+b')as final:
 manifest=json.loads(src.read('DEPLOY-MANIFEST.json'));manifest['version']='2026.11.06f';rows={r['path']:r for r in manifest['files']}
 replace=set(extras)|{'DEPLOY-MANIFEST.json'};final.write(stub.read_bytes());rel=RelativeFile(final,offset)
 with zipfile.ZipFile(rel,'w',allowZip64=True)as dst:
  items=sorted(src.infolist(),key=lambda i:i.header_offset)
  for n,info in enumerate(items):
   if info.filename in replace:continue
   # Carry the exact original compressed local record. No art is resized or
   # recompressed and no second full payload is needed on the tester's disk.
   end=items[n+1].header_offset if n+1<len(items)else src.start_dir
   raw.seek(info.header_offset);left=end-info.header_offset;new=copy.copy(info);new.header_offset=rel.tell()
   while left:
    block=raw.read(min(left,4*1024*1024));assert block;rel.write(block);left-=len(block)
   dst.filelist.append(new);dst.NameToInfo[new.filename]=new;dst.start_dir=rel.tell();dst._didModify=True
  for name,p in extras.items():
   dst.write(p,name,compress_type=zipfile.ZIP_DEFLATED);rows[name]={'path':name,'bytes':p.stat().st_size,'sha256':digest(p)}
  manifest['files']=list(rows.values());manifest['bytes']=sum(r['bytes']for r in manifest['files'])
  dst.writestr('DEPLOY-MANIFEST.json',json.dumps(manifest,separators=(',',':')))
  assert len(dst.filelist)==len({i.filename for i in dst.filelist})==len(manifest['files'])+1
 size=final.tell()-offset;payloadhash=hashlib.sha256();final.seek(offset)
 for block in iter(lambda:final.read(4*1024*1024),b''):payloadhash.update(block)
 final.seek(0,2);final.write(b'BOFSETUP1106DATA'+struct.pack('<qq',offset,size)+payloadhash.digest());final.flush()
# Read every ZIP member through its CRC and the ownership manifest, including
# unchanged game artwork. This also proves raw compressed-record relocation.
with zipfile.ZipFile(temp)as z:
 for i,row in enumerate(manifest['files']):
  with z.open(row['path'])as f:
   h=hashlib.sha256();size=0
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block);size+=len(block)
  assert size==row['bytes']and h.hexdigest()==row['sha256'],row['path']
  if i%5000==0:print('VERIFIED',i,'/',len(manifest['files']),flush=True)
whole=digest(temp);temp.replace(out);out.with_suffix('.exe.sha256').write_text(whole+'  '+out.name+'\n',encoding='ascii')
for name,p in extras.items():
 if not name.startswith('game/')or name!='game/BUILD-INFO.json':
  dest=T/name;dest.parent.mkdir(parents=True,exist_ok=True)
  if p.resolve()!=dest.resolve():shutil.copy2(p,dest)
(T/'DEPLOY-MANIFEST.json').write_text(json.dumps(manifest,separators=(',',':')))
marker=json.loads((T/'BOF-INSTALL.json').read_text());marker['version']='2026.11.06f';marker['files']=[r['path']for r in manifest['files']]+['DEPLOY-MANIFEST.json','BOF-INSTALL.json'];(T/'BOF-INSTALL.json').write_text(json.dumps(marker))
receipt=dict(path=str(out),version='2026.11.06f',bytes=out.stat().st_size,sha256=whole,entries=len(manifest['files']),unpackedBytes=manifest['bytes'],gameJsSha256=digest(R/'assets/game.js'),hostSha256=digest(stub),payloadSha256=payloadhash.hexdigest(),allFilesVerified=True,seconds=round(time.time()-start,2))
(W/'qa/installer-1106f-build.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)
