from pathlib import Path
import zipfile,json,hashlib,copy,time
W=Path(__file__).resolve().parent;O=W.parent/'Releases';T=O/'BulletsOfFury-Windows-2026-11-06';S=O/'BulletsOfFury-Setup-2026-11-06.exe';Z=O/'BulletsOfFury-Launcher-and-Game-2026-11-06-RevF.zip';P=Z.with_suffix('.zip.partial');start=time.time()
assert not Z.exists()and not P.exists(),'Archive already exists; do not overwrite it.'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
ready={p.relative_to(T).as_posix():p for p in T.rglob('*')if p.is_file()}
manifest=json.loads((T/'DEPLOY-MANIFEST.json').read_text(encoding='utf8'));expected={r['path']:r for r in manifest['files']}
for name in ['BOF-INSTALL.json','DEPLOY-MANIFEST.json','START-HERE.txt']:
 p=T/name;expected[name]={'path':name,'bytes':p.stat().st_size,'sha256':sha(p)}
assert set(ready)==set(expected),'Unexpected or missing files in the ready game folder.'
readme='''BULLETS OF FURY - COMPLETE LAUNCHER AND GAME / REVISION F

1. Extract ALL files into one folder. Do not run the game inside the ZIP.
2. Open BOF Launcher.exe for the animated launcher.
   Open Bullets of Fury.exe for immediate fullscreen play.
3. Keep the game, runtime and DLL files together in this folder.

If the Windows WebView2 runtime is missing, run the included
runtime/MicrosoftEdgeWebView2RuntimeInstallerX64.exe once, then open BOF again.

F11 or Alt+Enter switches fullscreen/windowed play.
Move: WASD / arrows. Fire: left-click / J.
Retina: right-click / C. Missiles: Space / K.
Multi-Retina: hold Mouse Button 4 / Y, or right-tap then right-click and HOLD.
Charge: H / Mouse Button 5. Pause: Enter / P.

Includes all current game assets, the new launcher captions, locked Cole's
gray/black pilot/jet/padlock frames, neutral locked backgrounds, and the
ordinary-bullet/sonic-wave interception protection. Stage5's original blue sky\nascent, cloud assembly and space starfield/parallax are restored. Incoming\nkit pieces are smaller; the completed ship retains its original size.\nWindows 10/11 x64.
'''
# Preserve the already verified compressed records. This avoids recompressing
# gigabytes of PNG/audio data or making a second full game copy on disk.
with zipfile.ZipFile(S)as src,S.open('rb')as raw,P.open('xb')as output,zipfile.ZipFile(output,'w',allowZip64=True)as dst:
 items=sorted(src.infolist(),key=lambda q:q.header_offset)
 for i,info in enumerate(items):
  assert info.filename in expected,info.filename
  end=items[i+1].header_offset if i+1<len(items)else src.start_dir
  raw.seek(info.header_offset);left=end-info.header_offset;new=copy.copy(info);new.header_offset=output.tell()
  while left:
   block=raw.read(min(left,4*1024*1024));assert block;output.write(block);left-=len(block)
  dst.filelist.append(new);dst.NameToInfo[new.filename]=new;dst.start_dir=output.tell();dst._didModify=True
 copied=set(dst.NameToInfo)
 for name,p in ready.items():
  if name not in copied:dst.write(p,name,compress_type=zipfile.ZIP_DEFLATED)
 dst.writestr('OPEN-ME.txt',readme,compress_type=zipfile.ZIP_DEFLATED)
 assert len(dst.filelist)==len({i.filename for i in dst.filelist})==len(ready)+1
print('ZIP_CREATED',P.stat().st_size,'bytes; verifying all files',flush=True)
with zipfile.ZipFile(P)as z:
 assert set(z.namelist())==set(ready)|{'OPEN-ME.txt'}
 for i,(name,row)in enumerate(expected.items()):
  h=hashlib.sha256();size=0
  with z.open(name)as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block);size+=len(block)
  assert size==row['bytes']and h.hexdigest()==row['sha256'],name
  if i%5000==0:print('VERIFIED',i,'/',len(expected),flush=True)
 assert z.read('OPEN-ME.txt').decode('ascii')==readme
digest=sha(P);P.rename(Z);Z.with_suffix('.zip.sha256').write_text(digest+'  '+Z.name+'\n',encoding='ascii')
result={'path':str(Z),'bytes':Z.stat().st_size,'sha256':digest,'version':'2026.11.06f','files':len(ready)+1,'verifiedGameFiles':len(expected),'contains':['BOF Launcher.exe','Bullets of Fury.exe','game/ (all assets)','runtime/ (offline Windows runtime)','all host DLLs and notices','OPEN-ME.txt'],'seconds':round(time.time()-start,2)}
(O/'BulletsOfFury-Launcher-and-Game-2026-11-06-RevF.json').write_text(json.dumps(result,indent=2),encoding='utf8');print('ZIP_READY',json.dumps(result),flush=True)
