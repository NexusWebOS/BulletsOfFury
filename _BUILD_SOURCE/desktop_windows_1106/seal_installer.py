from pathlib import Path
import zipfile,json,hashlib,struct,time,os
W=Path(__file__).resolve().parent;Z=W/'bof-deploy.zip';B=W/'host';out=W.parent/'Releases/BulletsOfFury-Setup-2026-11-06.exe';start=time.time()
extras={p.name:p for p in B.iterdir()if p.is_file()};manifest=None
# Refresh host records without copying or re-compressing 3.6GB of unchanged art.
# The central directory contains exactly one entry for every installed file.
with zipfile.ZipFile(Z,'a',allowZip64=True)as z:
 manifest=json.loads(z.read('DEPLOY-MANIFEST.json'));replace=set(extras)|{'DEPLOY-MANIFEST.json'}
 z.filelist=[i for i in z.filelist if i.filename not in replace]
 for n in replace:z.NameToInfo.pop(n,None)
 manifest['files']=[r for r in manifest['files']if r['path']not in extras]
 for n,p in extras.items():
  z.write(p,n,compress_type=zipfile.ZIP_DEFLATED);manifest['files'].append(dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 manifest['bytes']=sum(r['bytes']for r in manifest['files']);z.writestr('DEPLOY-MANIFEST.json',json.dumps(manifest,separators=(',',':')))
 assert len(z.filelist)==len({i.filename for i in z.filelist})
stub=B/'Bullets of Fury.exe';temp=out.with_suffix('.exe.partial');payloadhash=hashlib.sha256();whole=hashlib.sha256()
with temp.open('wb')as o:
 data=stub.read_bytes();offset=len(data);o.write(data);whole.update(data)
 with Z.open('rb')as f:
  for data in iter(lambda:f.read(8*1024*1024),b''):o.write(data);payloadhash.update(data);whole.update(data)
 footer=b'BOFSETUP1106DATA'+struct.pack('<qq',offset,Z.stat().st_size)+payloadhash.digest();assert len(footer)==64;o.write(footer);whole.update(footer)
temp.replace(out);digest=whole.hexdigest();out.with_suffix('.exe.sha256').write_text(digest+'  '+out.name+'\n',encoding='ascii')
old=json.loads(Path(os.environ.get('BOF_OFFICIAL_RECEIPT',str(W.parent/'BOF-Official-Build-1105/package.json'))).read_text(encoding='utf8'))
receipt=dict(path=str(out),bytes=out.stat().st_size,sha256=digest,payload=str(Z),payloadSha256=payloadhash.hexdigest(),entries=len(manifest['files']),unpackedBytes=manifest['bytes'],gameJsSha256=old['build']['gameJsSha256'],hostSha256=hashlib.sha256(stub.read_bytes()).hexdigest(),seconds=round(time.time()-start,2))
(W/'qa/installer-build.json').write_text(json.dumps(receipt,indent=2));print('INSTALLER_READY',json.dumps(receipt),flush=True)
