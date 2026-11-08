from pathlib import Path
import json,hashlib,zipfile,time,os,re
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parent/'Releases';O.mkdir(exist_ok=True)
assert all(c['passed']for c in json.loads((W/'controls-checks.json').read_text())['checks'])
assert not json.loads((W/'asset-text-scan.json').read_text())['suspectFiles']
prefix='BulletsOfFury-Official-2026-11-05/'
corehash=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest();info={'title':'Bullets of Fury','date':'2026-11-05','buildId':'BOF-Official-2026-11-05-MK-'+corehash[:10],'edition':'Official mouse and keyboard tester snapshot','controls':{'fire':'Left click / J','retina':'Right click / C','missiles':'Space / K','multiRetina':'Hold mouse button 4 / Y, or double-tap right-click and hold the second press'},'launcher':'START-BOF.cmd','requirements':'Windows 10/11, Windows PowerShell and a desktop browser; no Python or Node install','source':'Current local production build, including uncommitted game updates','gameJsSha256':corehash}
(W/'BUILD-INFO.json').write_text(json.dumps(info,indent=2),encoding='utf8')
sources={}
for folder in ['assets','extensions']:
 for p in (R/folder).rglob('*'):
  if p.is_file():assert p.resolve().is_relative_to(R.resolve());sources[p.relative_to(R).as_posix()]=p
sources['index.html']=R/'index.html'
for n in ['PLAY_LOCAL.ps1','START-BOF.cmd','HOW_TO_PLAY.txt','README-TESTER.txt','BUILD-INFO.json']:sources[n]=W/n
refs=re.findall(r'<script[^>]+src=["\x27]([^"\x27]+)',(R/'index.html').read_text(encoding='utf8'));missing=[s for s in refs if not s.startswith(('http:','https:'))and s.split('?')[0]not in sources];assert not missing,missing
path=O/'BulletsOfFury-Official-2026-11-05-MouseKeyboard.zip';i=2
while path.exists():path=O/f'BulletsOfFury-Official-2026-11-05-MouseKeyboard-{i}.zip';i+=1
temp=path.with_suffix('.zip.partial');rows=[];start=time.time();stored={'.png','.webp','.jpg','.jpeg','.gif','.mp3','.mp4','.webm','.ogg','.aseprite','.zip','.woff2','.7z'}
with zipfile.ZipFile(temp,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for i,(name,p)in enumerate(sorted(sources.items())):
  st=p.stat();h=hashlib.sha256();zi=zipfile.ZipInfo.from_file(p,prefix+name);zi.compress_type=zipfile.ZIP_STORED if p.suffix.lower()in stored else zipfile.ZIP_DEFLATED
  with p.open('rb')as f,z.open(zi,'w',force_zip64=True)as out:
   for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);out.write(chunk)
  after=p.stat();assert(st.st_size,st.st_mtime_ns)==(after.st_size,after.st_mtime_ns),'Source changed while packaging: '+name
  rows.append({'path':name,'bytes':st.st_size,'sha256':h.hexdigest()})
  if i%1500==0:print('PACKING',i,'/',len(sources),name,flush=True)
 manifest={'build':info,'files':rows,'filesIncludingManifest':len(rows)+1,'unpackedBytes':sum(r['bytes']for r in rows),'localScriptReferences':len(refs),'allAssetsAndExtensions':True}
 z.writestr(prefix+'FILE-MANIFEST.json',json.dumps(manifest,separators=(',',':')))
os.replace(temp,path)
h=hashlib.sha256()
with path.open('rb')as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
digest=h.hexdigest();checksum=path.with_suffix('.zip.sha256');checksum.write_text(digest+'  '+path.name+'\n',encoding='ascii')
receipt={'path':str(path),'checksumPath':str(checksum),'sha256':digest,'bytes':path.stat().st_size,'files':len(rows)+1,'unpackedBytes':manifest['unpackedBytes'],'prefix':prefix,'build':info,'seconds':round(time.time()-start,2)}
(W/'package.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');(W/'file-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print('ZIP_READY',json.dumps(receipt),flush=True)
