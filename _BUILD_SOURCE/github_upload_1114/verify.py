from pathlib import Path
import sys,json,hashlib,zipfile,struct,os,re,time,subprocess
from playwright.sync_api import sync_playwright
from github_api import R,REPO,session,api
from remote_zip import PartsReader
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';P=json.loads((O/'package-receipt.json').read_text());local=json.loads((O/'DEPLOY-MANIFEST.json').read_text());s=session();release=api(s,'GET','repos/'+REPO+'/releases/'+str(P['releaseId']));assets={p['name']:p for p in release['assets']};parts=[]
for q in P['parts']:
 r=assets[q['name']];assert r['size']==q['bytes']and r['digest']=='sha256:'+q['sha256'];parts.append(r)
reader=PartsReader(parts,s);reader.seek(-64,2);footer=reader.read(64);assert footer[:16]==b'BOFSETUP1106DATA';offset,length=struct.unpack('<qq',footer[16:32]);assert offset==P['stubBytes']and length==P['payloadBytes']and footer[32:].hex()==P['payloadSha256']and reader.length==P['installerBytes'];verified=[]
with zipfile.ZipFile(reader)as z:
 manifest=json.loads(z.read('DEPLOY-MANIFEST.json'));assert manifest==local;names=set(z.namelist());assert len(names)==len(z.infolist())==len(local['files'])+1
 for row in local['files']:assert z.getinfo(row['path']).file_size==row['bytes'],row['path']
 # Read back every executable/host dependency and every active script from the
 # actual uploaded parts. The central table validates every payload entry.
 index=z.read('game/index.html').decode();scripts=re.findall(r'<script\b[^>]*\bsrc=["\x27]([^"\x27]+)',index,re.I);wanted=['game/index.html','game/assets/game.js','Bullets of Fury.exe','BOF Launcher.exe','Microsoft.Web.WebView2.Core.dll','Microsoft.Web.WebView2.WinForms.dll','WebView2Loader.dll','READ-ME.txt','DESKTOP-BUILD.json','game/BUILD-INFO.json']+['game/'+x.split('?',1)[0]for x in scripts if not x.startswith(('http:', 'https:'))]
 wanted+=['game/assets/game/levels/stage_05/miniboss/assault_1114/retina_tracking_1114.webp','game/assets/game/levels/stage_08/enemies/atlas/stage8_leech_recovery_1114.png'];rows={q['path']:q for q in local['files']}
 for n in sorted(dict.fromkeys(wanted),key=lambda n:z.getinfo(n).header_offset):
  data=z.read(n);assert hashlib.sha256(data).hexdigest()==rows[n]['sha256'],n;verified.append(n)
 print('REMOTE PACKAGE:',len(local['files']),'entries and',len(verified),'critical/script payloads verified.',flush=True)
sourceChecks=0
for record in subprocess.check_output(['git','-C',str(R),'ls-tree','-rz','--full-tree',P['sourceCommit'],'--','assets','extensions','index.html','HOW_TO_PLAY.txt']).split(b'\0'):
 if not record:continue
 attrs,name=record.split(b'\t',1);name=name.decode('utf-8');expected=attrs.split()[2].decode();path=R/name;h=hashlib.sha1(b'blob '+str(path.stat().st_size).encode()+b'\0')
 with path.open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 assert h.hexdigest()==expected,name;sourceChecks+=1
print('COMMITTED RUNTIME INPUTS VERIFIED',sourceChecks,flush=True)
# A clean directory with byte-identical hard links avoids a second4GB copy.
# Package/input hashes above bind it to the actual uploaded installer.
stage=O/'Current-Windows-Build';stage.mkdir(exist_ok=True);inputs=json.loads((O/'package-inputs.json').read_text())
for name,source in inputs.items():
 target=stage/name;target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():os.link(source,target)
 assert target.stat().st_size==rows[name]['bytes']
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
from barrage_review_common_1025 import boot
errors=[];checks=[];port,stop=serve(str(stage/'game'))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disk-cache-size=1','--media-cache-size=1','--disable-gpu-shader-disk-cache']);c=br.new_context(viewport={'width':1280,'height':800});p=c.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text or'update error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof S5B14!=="undefined"',timeout=180000)
  q=p.evaluate('()=>({native:!!document.querySelector("canvas"),god:DBGT.god,shared:BOF_DIFFICULTY_RULES_15.state===DR15,retina:S5B14_ART.banks.retina_tracking_1114.count})');assert q['native']and not q['god']and q['shared']and q['retina']==256;checks.append(dict(name='Fresh packaged title, normal controls, shared helpers and new optic metadata',passed=True,data=q));p.screenshot(path=str(O/'packaged-title.png'));p.close()
  for st in [5,6,7,8]:
   p=boot(c,port,st,errors,'mini'if st in [5,6,7]else'boss');p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)}',arg=st,timeout=180000)
   if st==5:p.evaluate('()=>{const b=subBoss;b.enter=false;b.y=b.ty;b._bomber.mode="recover";s5b14Init(b);s5b14Mode(b,"lock");for(let i=0;i<30;i++)updatePlay(1/60);drawWorld(0);SC12.refresh();__bofFit()}')
   else:p.evaluate('()=>{for(let i=0;i<3;i++)updatePlay(1/60);drawWorld(0);SC12.refresh();__bofFit()}')
   assert not errors,errors;p.screenshot(path=str(O/f'packaged-stage{st}.png'));checks.append(dict(name='Packaged Stage'+str(st)+' loads, updates and renders',passed=True));p.close()
  br.close()
finally:stop()
assert not errors
result=dict(committedRuntimeInputs=sourceChecks,files=len(local['files']),allEntrySizesMatch=True,remotePartDigests=len(parts),readBackVerifiedFiles=verified,networkBytes=reader.received,footerAndManifestMatch=True,sourceCommit=P['sourceCommit'],checks=checks,errors=errors);(O/'package-verification.json').write_text(json.dumps(result,indent=2));print('CLEAN PACKAGE CHECKS:',len(checks),'passed,0 errors.',flush=True)
