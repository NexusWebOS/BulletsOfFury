from pathlib import Path
import json,subprocess,hashlib,collections,zipfile,struct,os,re,shutil
from github_api import session,api,R,REPO
from remote_zip import PartsReader
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';I=json.loads((O/'inventory.json').read_text());s=session();base=json.loads((O/'remote.json').read_text())['base'];parts=sorted([p for p in base['assets']if'.exe.part'in p['name']],key=lambda p:p['name']);assert len(parts)==2
reader=PartsReader(parts,s);reader.seek(-64,2);footer=reader.read(64);assert footer[:16]==b'BOFSETUP1106DATA';offset,length=struct.unpack('<qq',footer[16:32]);assert offset+length+64==reader.length
host=W/'host';host.mkdir(exist_ok=True);reader.seek(0);exe=reader.read(offset);assert exe[:2]==b'MZ';(host/'Bullets of Fury.exe').write_bytes(exe);(host/'BOF Launcher.exe').write_bytes(exe)
with zipfile.ZipFile(reader)as z:
 manifest=json.loads(z.read('DEPLOY-MANIFEST.json'));(O/'base-deploy-manifest.json').write_text(json.dumps(manifest,indent=2));names=z.namelist();print('Base native host recovered:',offset,'bytes; original payload entries:',len(names),flush=True)
 for n in ['Microsoft.Web.WebView2.Core.dll','Microsoft.Web.WebView2.WinForms.dll','WebView2Loader.dll','WebView2-LICENSE.txt']:
  data=z.read(n);row=next(q for q in manifest['files']if q['path']==n);assert hashlib.sha256(data).hexdigest()==row['sha256'];(host/n).write_bytes(data)
 # Preserve the signed offline runtime in the finished build by copying its
 # original compressed record during packaging, without a second local copy.
 runtime=next(i for i in z.infolist()if i.filename=='runtime/MicrosoftEdgeWebView2RuntimeInstallerX64.exe');nextOffset=min([i.header_offset for i in z.infolist()if i.header_offset>runtime.header_offset]+[z.start_dir]);runtimeMeta={k:getattr(runtime,k)for k in ['filename','header_offset','compress_size','file_size','CRC','compress_type','flag_bits','date_time','extract_version','create_version','external_attr','internal_attr','volume','create_system']};runtimeMeta['recordEnd']=nextOffset;runtimeMeta['row']=next(q for q in manifest['files']if q['path']==runtime.filename)
(O/'base-host.json').write_text(json.dumps(dict(stubBytes=offset,stubSha256=hashlib.sha256(exe).hexdigest(),runtime=runtimeMeta,networkBytes=reader.received),indent=2))
# Review every pending text file without printing matched secret values.
rows=json.loads((O/'changes.json').read_text());matches=[];patterns={'credential':re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{28,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{32,}|-----BEGIN (?:RSA |EC )?PRIVATE KEY-----)'),'signed-download':re.compile(r'https?://[^\s\"<>]+(?:X-Amz-Signature=|X-Goog-Signature=)[^\s\"<>]*',re.I)}
for row in rows:
 p=R/row['path']
 if not p.is_file()or p.stat().st_size>12_000_000 or p.suffix.lower()not in ['.js','.cjs','.mjs','.json','.html','.md','.py','.ps1','.txt','.log','.yaml','.yml','.sql','.env']:continue
 try:text=p.read_text(encoding='utf-8')
 except UnicodeError:continue
 for kind,pattern in patterns.items():
  for m in pattern.finditer(text):matches.append(dict(path=row['path'],kind=kind,line=text.count('\n',0,m.start())+1))
(O/'secret-scan.json').write_text(json.dumps(dict(files=len(rows),matches=matches),indent=2));assert not matches,'Pending files contain sensitive material; inspect the file/line-only scan before staging.'
print('Pending text scan passed; native dependencies verified; free bytes',shutil.disk_usage(R).free,flush=True)
