from pathlib import Path
import json,hashlib,zipfile,shutil,struct,time,os
W=Path(__file__).resolve().parent;OUT=W.parent/'Releases';OUT.mkdir(exist_ok=True);B=W/'host';Z=W/'bof-deploy.zip'
old=json.loads(Path(os.environ.get('BOF_OFFICIAL_RECEIPT',str(W.parent/'BOF-Official-Build-1105/package.json'))).read_text(encoding='utf8'));source=Path(os.environ.get('BOF_OFFICIAL_ZIP',old['path']));rows=[];start=time.time()
readme='''BULLETS OF FURY - FURY HQ WINDOWS EDITION

Start: double-click Bullets of Fury.exe for immediate fullscreen play.
Open BOF Launcher.exe for the animated Fury HQ launcher.
The game starts fullscreen. F11 or Alt+Enter toggles windowed mode.
Alt+F4 closes the game window and returns to the launcher.
The launcher has keyboard and mouse navigation, controls, sound and door options.

CONTROLS
Move: WASD / arrows. Fire: left-click / J.
Retina: right-click / C. Missiles: Space / K.
Multi-Retina: hold Mouse Button 4 (Back thumb button) / Y.
Alternative: short right tap, then quickly right-click again and HOLD.
Keep holding to scan; press Space to launch the marked-target volley.
Charge: H / Mouse Button 5. Pause: Enter / P.

Saves and launcher preferences are in your local ColeForge/BulletsOfFury
application-data folder, retained when uninstalling. This Windows edition uses
its own save profile; older browser-profile saves are not imported automatically.
Keep your existing browser build and its saves if you need to revisit them.

UNINSTALL
Use Windows Installed Apps or the Start menu's Uninstall Bullets of Fury entry.
Saves and extra files you add to the installation are kept.

Windows 10/11 x64. Microsoft's signed offline WebView2 runtime installer is
included in runtime/ and setup uses it only if the runtime is missing.
No Python, Node, browser window, web server or internet download is needed to play.
Online services, if used, still require their normal connection.

This is the current November 5 game snapshot in the November 6 desktop host.
It includes the new mouse controls and latest Razorwake/Thunderhead/Sumpjaw work.
The existing older full regression harness has an unrelated missing-helper setup
failure; focused desktop/game launch and packaged input tests are documented.
'''
(B/'READ-ME.txt').write_text(readme,encoding='ascii')
hostmeta=dict(product='ColeForge.BulletsOfFury.2026',version='2026.11.06',gameBuild=old['build'],host='Windows x64 / WebView2 / authored bitmap launcher',defaultFullscreen=True)
(B/'DESKTOP-BUILD.json').write_text(json.dumps(hostmeta,indent=2),encoding='utf8')
extras={p.name:p for p in B.iterdir()if p.is_file()};extras['runtime/MicrosoftEdgeWebView2RuntimeInstallerX64.exe']=W/'vendor/MicrosoftEdgeWebView2RuntimeInstallerX64.exe'
with zipfile.ZipFile(source)as src,zipfile.ZipFile(Z,'w',allowZip64=True)as dst:
 for i,info in enumerate(src.infolist()):
  name=info.filename[len(old['prefix']):]
  if not(name.startswith(('assets/','extensions/'))or name in ['index.html','BUILD-INFO.json']):continue
  target='game/'+name;zi=zipfile.ZipInfo(target,info.date_time);zi.compress_type=info.compress_type;h=hashlib.sha256();size=0
  with src.open(info)as f,dst.open(zi,'w',force_zip64=True)as o:
   for data in iter(lambda:f.read(1024*1024),b''):h.update(data);size+=len(data);o.write(data)
  rows.append(dict(path=target,bytes=size,sha256=h.hexdigest()))
  if i%2500==0:print('PACK_GAME',i,flush=True)
 for name,p in extras.items():
  zi=zipfile.ZipInfo.from_file(p,name);zi.compress_type=zipfile.ZIP_STORED if p.suffix=='.exe'and p.stat().st_size>50_000_000 else zipfile.ZIP_DEFLATED;h=hashlib.sha256()
  with p.open('rb')as f,dst.open(zi,'w',force_zip64=True)as o:
   for data in iter(lambda:f.read(1024*1024),b''):h.update(data);o.write(data)
  rows.append(dict(path=name,bytes=p.stat().st_size,sha256=h.hexdigest()))
 manifest=dict(product='ColeForge.BulletsOfFury.2026',version='2026.11.06',bytes=sum(r['bytes']for r in rows),files=rows)
 dst.writestr('DEPLOY-MANIFEST.json',json.dumps(manifest,separators=(',',':')))
print('PAYLOAD_READY',Z.stat().st_size,flush=True)
setup=OUT/'BulletsOfFury-Setup-2026-11-06.exe';temp=setup.with_suffix('.exe.partial');assert not setup.exists()
stub=B/'Bullets of Fury.exe';payloadhash=hashlib.sha256();whole=hashlib.sha256()
with temp.open('wb')as o:
 data=stub.read_bytes();o.write(data);whole.update(data);offset=len(data)
 with Z.open('rb')as f:
  for data in iter(lambda:f.read(8*1024*1024),b''):o.write(data);payloadhash.update(data);whole.update(data)
 footer=b'BOFSETUP1106DATA'+struct.pack('<qq',offset,Z.stat().st_size)+payloadhash.digest();assert len(footer)==64;o.write(footer);whole.update(footer)
temp.rename(setup);digest=whole.hexdigest();setup.with_suffix('.exe.sha256').write_text(digest+'  '+setup.name+'\n',encoding='ascii')
receipt=dict(path=str(setup),bytes=setup.stat().st_size,sha256=digest,payload=str(Z),payloadSha256=payloadhash.hexdigest(),entries=len(rows),unpackedBytes=manifest['bytes'],gameJsSha256=old['build']['gameJsSha256'],hostSha256=hashlib.sha256(stub.read_bytes()).hexdigest(),seconds=round(time.time()-start,2))
(W/'qa/installer-build.json').write_text(json.dumps(receipt,indent=2));print('INSTALLER_READY',json.dumps(receipt),flush=True)
