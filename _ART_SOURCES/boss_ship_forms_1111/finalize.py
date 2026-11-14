from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess,html
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Boss-ships-and-gun';O.mkdir(exist_ok=True);E=W/'exports';M=json.loads((W/'manifest.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=json.loads((O/'verification/checks.json').read_text());assert all(c['passed']for c in checks['checks']),checks;assert not checks['errors'],checks['errors'];assert checks['runtimeHash']==sha(R/'assets/boss_ship_forms_1111.js'),'Runtime changed since verification'
installed=json.loads((W/'install-report.json').read_text());assert all(sha(R/n)==h for n,h in installed['protected'].items()),'Protected owner changed'
for n in ['boss_ship_forms_1111.js','boss_ship_forms_art_1111.js']:assert sha(W/n)==sha(R/'assets'/n)
for p in E.glob('*.webp'):assert sha(p)==sha(R/'assets/game/shared/combat/boss_ship_forms_1111'/p.name)
# Required broad checks keep their exact exit codes, including pre-existing failures.
suite=[]
for name,args in [('syntax',['node','--check','assets/game.js']),('game-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 q=subprocess.run(args,cwd=R,capture_output=True,encoding='utf-8',errors='replace');(W/(name+'.txt')).write_text(q.stdout+'\n'+q.stderr,encoding='utf-8');suite.append(dict(name=name,exit=q.returncode,tail=(q.stdout+'\n'+q.stderr)[-1800:]));print(name,'exit',q.returncode,flush=True)
(W/'full-suite.json').write_text(json.dumps(suite,indent=2));assert suite[0]['exit']==0
# Open the real graphics editor invisibly, save editable timelines, then compare
# its decoded pixels with the exact PNG imports.
exe=r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe';lua=str(W/'author.lua')
ps="$a=Start-Process -FilePath '"+exe+"' -ArgumentList @('--batch','--script-param','out="+W.as_posix()+"','--script','"+lua.replace('\\','/')+"') -WindowStyle Hidden -Wait -PassThru;exit $a.ExitCode"
q=subprocess.run(['powershell','-NoProfile','-Command',ps],capture_output=True,text=True);(W/'aseprite-log.txt').write_text(q.stdout+q.stderr);assert q.returncode==0,q.stderr
frames=0
for n,a in M.items():
 source=np.array(Image.open(E/(n+'_regular.png')).convert('RGBA'));roundtrip=np.array(Image.open(E/(n+'_roundtrip.png')).convert('RGBA'));assert np.array_equal(source,roundtrip),n
 for mat in ['regular','chrome','red','hit']:
  x=np.array(Image.open(E/(n+'_'+mat+'.webp')).convert('RGBA'));assert np.array_equal(source[:,:,3],x[:,:,3]),(n,mat)
 frames+=a['count']
(W/'export-verification.json').write_text(json.dumps(dict(exactEditableFrames=frames,banks=len(M),materialAlphaMatches=True),indent=2));print('Exact editable frames:',frames,flush=True)
P=O/'art';P.mkdir(exist_ok=True)
for n,a in M.items():
 for mat in ['regular','chrome']:
  shutil.copy2(E/(n+'_'+mat+'.webp'),P/(n+'_'+mat+'.webp'))
def pose(n,f,mat='regular'):
 a=M[n];cw,ch=a['cell'];s=Image.open(E/(n+'_'+mat+'.webp')).convert('RGBA');f=min(a['count']-1,max(0,f));return s.crop((f%4*cw,f//4*ch,f%4*cw+cw,f//4*ch+ch))
forms=[('chronus','regular','CHRONUS'),('draconus','regular','DRACONUS'),('chronus','chrome','CHRONUS / CHROMIUM'),('draconus','chrome','DRACONUS / CHROMIUM')]
timeline=[0]*8+list(range(24))+[23]*12+list(reversed(range(24)))+[0]*8
gifs=[]
for f in timeline:
 board=Image.new('RGBA',(1024,1088),'#101820');d=ImageDraw.Draw(board)
 for k,(n,m,title)in enumerate(forms):
  x=k%2*512;y=k//2*544;d.text((x+16,y+12),title,fill='white');board.alpha_composite(pose(n+'-transform',f,m),(x,y+32))
 gifs.append(board.convert('RGB'))
gifs[0].save(O/'all-four-ship-transforms.gif',save_all=True,append_images=gifs[1:],duration=83,loop=0,optimize=False)
gifs[0].save(O/'ship-forms.png')
# Portable, local-only frame player; production assets are unmodified.
spec={n:{k:v for k,v in a.items()if k!='meta'}for n,a in M.items()}
page='''<!doctype html><meta charset="utf-8"><title>BOF — ships and Draconus gun</title><style>body{margin:24px;background:#101820;color:#e9f0ff;font:16px system-ui}button,select,input{font:inherit;margin:8px;padding:8px}main{display:grid;grid-template-columns:repeat(2,minmax(260px,512px));gap:16px}canvas{width:100%;height:auto;image-rendering:pixelated;background:#0c1219}h1{font-size:24px}a{color:#8dd8ff}</style><h1>Boss ships and gun animation review</h1><p>Chronus: swept-wing blue reactor ship. Draconus: horned crescent ship. Closed ships carry no exposed gun or hammer.</p><select id="mode"><option value="transform">Ship transformation</option><option value="gun-spin">Gun rev</option><option value="gun-fire">Gun fire</option><option value="catch-pre">Empty-hand catch anticipation</option><option value="catch-take">Gun catch</option><option value="gun-stow">Gun stow</option><option value="gun-break">Gun break</option><option value="gun-armor">Gun retained during Chromium activation</option></select><button id="play">Pause</button><button id="prev">Previous</button><button id="next">Next</button><input id="seek" type="range" min="0" max="23" value="0"><span id="frame"></span><main></main><p>Native game recordings: <a href="draconus-normal-native.gif">Normal</a> · <a href="draconus-chromium-native.gif">Chromium</a>. These show the real icon box, catch, firing, stow and hammer recall.</p><script>const A=SPEC;let f=0,playing=true;const imgs={};const forms=[['chronus','regular','Chronus'],['draconus','regular','Draconus'],['chronus','chrome','Chronus / Chromium'],['draconus','chrome','Draconus / Chromium']];let views=[];for(const [unit,mat,title]of forms){const div=document.createElement('div');div.innerHTML='<p>'+title+'</p><canvas width="512" height="512"></canvas>';document.querySelector('main').append(div);views.push({unit,mat,c:div.querySelector('canvas')})}function draw(){const mode=document.querySelector('#mode').value,limit=mode==='transform'?24:A['draconus-'+mode].count;f=(f+limit)%limit;seek.max=limit-1;seek.value=f;frame.textContent=(f+1)+' / '+limit;for(const v of views){const n=mode==='transform'?v.unit+'-transform':'draconus-'+mode,a=A[n],mat=mode==='gun-armor'?'regular':v.mat,key=n+'_'+mat;let im=imgs[key];if(!im){im=imgs[key]=new Image;im.onload=draw;im.src='art/'+key+'.webp'}const g=v.c.getContext('2d');g.clearRect(0,0,512,512);g.imageSmoothingEnabled=false;if(im.complete&&im.naturalWidth)g.drawImage(im,f%4*a.cell[0],Math.floor(f/4)*a.cell[1],...a.cell,0,0,512,512)}}play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};prev.onclick=()=>{playing=false;f--;draw()};next.onclick=()=>{playing=false;f++;draw()};seek.oninput=()=>{playing=false;f=+seek.value;draw()};mode.onchange=()=>{f=0;draw()};setInterval(()=>{if(playing){f++;draw()}},83);draw();</script>'''.replace('SPEC',json.dumps(spec,separators=(',',':')))
page=page.replace('const imgs={};','const imgs={};const seek=document.querySelector("#seek"),frame=document.querySelector("#frame"),play=document.querySelector("#play"),prev=document.querySelector("#prev"),next=document.querySelector("#next"),mode=document.querySelector("#mode");').replace('views.push({unit,mat,c:','views.push({unit,mat,div,c:').replace('for(const v of views){const n=','for(const v of views){v.div.hidden=mode!=="transform"&&v.unit==="chronus";if(v.div.hidden)continue;const n=')
(O/'playback.html').write_text(page,encoding='utf-8')
from playwright.sync_api import sync_playwright
preview_errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',headless=True);p=br.new_page(viewport={'width':1120,'height':900});p.on('pageerror',lambda e:preview_errors.append(str(e)));p.goto((O/'playback.html').as_uri());p.wait_for_function('Object.values(imgs).length===4&&Object.values(imgs).every(i=>i.complete&&i.naturalWidth>0)')
 p.locator('#play').click();p.locator('#seek').fill('12');p.locator('#seek').dispatch_event('input');p.screenshot(path=str(O/'playback-preview.png'))
 p.locator('#mode').select_option('gun-fire');p.wait_for_function('Object.values(imgs).every(i=>i.complete&&i.naturalWidth>0)');p.locator('#next').click();assert p.locator('main>div:visible').count()==2
 br.close()
assert not preview_errors,preview_errors
for mat in ['normal','chromium']:
 im=Image.open(O/('draconus-'+mat+'-native.gif'));board=Image.new('RGB',(480*4,512*2),'#101820')
 for k,f in enumerate([0,21,39,48,68,90,126,141]):im.seek(min(f,im.n_frames-1));board.paste(im.convert('RGB'),(k%4*480,k//4*512))
 board.save(O/'verification'/('native-'+mat+'-contact-sheet.png'))
report=f'''# Original boss ships and Draconus gun — November 11, 2026

Chronus/Chronos now enters as a new closed swept-wing black/silver fighter with a cyan reactor. Draconus/copied Chronos Dracodia has a distinct purple crescent-wing craft with horned fins and a red reactor. Neither closed ship has an exposed chaingun or hammer. Each transformation has24 complete registered frames; normal and Chromium endpoints are the exact approved current hammer-ready pixels. The actual Stage5 flyby/unfold and HAMMER password intro use the new blue ship. The actual Stage8 boss-draw transition uses the purple ship and its reverse folding sequence, including the joined host/form timing. Other copy forms retain their own controllers.

Draconus strikes the approved exclusive orange gun ICON BOX with the actual lower hammer cap, holds contact, lifts/releases the hammer, opens the nine-frame box, receives the ejected gun, closes both hands around it, revs, fires, coasts, stows, and recalls the hammer. The box frame has a purple material variant; its original orange gun icon is preserved. This is the existing icon-box design, not a chest. Held gun poses are complete whole-actor drawings; released props alone travel separately. Native rotary fire sounds, projectile cadence/pattern/speed, HP floors, copy progression, death/rewards and all approved hammer banks remain owned by the existing encounter. The original finite gun pass remains finite; the added coast/stow segment finishes through native hammer recall.

The gun has its own source-alpha target subset and native HP pool within the complete actor drawing. Gun hits select authored whole-frame gun-only white feedback; body hits retain their own pool. Broken gun drops through authored recovery frames, stops new volleys immediately and never respawns. Chromium activation retains the held gun and its remaining budget, with eight baked material-activation steps. Warn fields, ordinary rounds, muzzle flash and the SHOOT marker use the actual measured muzzle and existing shared graphics. No runtime limb/weapon rotation, morphing or synthetic body drawing is added.

Sources/installation: assets/boss_ship_forms_art_1111.js, assets/boss_ship_forms_1111.js, assets/game/shared/combat/boss_ship_forms_1111; two late script includes in index.html. Both ships, transformation intermediates and gun acting were created through the built-in image tool. PixelLab credits were not used. Raw requests, original accepted/rejected candidates, registration data, fixed-cell PNGs, lossless material WebPs and editable Aseprite sources are retained. Phase openings that folded already extended legs back into the hull were excluded, as were a clipped-hand anticipation pose, a malformed firing-face candidate and an incomplete weapon-exit pose. The source archive documents these rather than counting rejected candidates as finished frames. The native canonical five-bore gun phases were a mechanical reference.

Verification: {len(checks['checks'])} focused native checks passed with no renderer errors. Both normal/Chromium pickup/fire/stow/recall loops ran through the real game loop and were recorded as native GIFs. Cap/box contact, no early shots or HP reset, muzzle/round origins, independent gun/body damage, white flash expiry, no gun respawn, Chromium retention and exit cleanup were checked. The prior center/right/left hammer tests were rerun in all four forms: four native Furious contacts, planted roots, clearance, warning/cap alignment, direction cycling and initial grip continuity. All{frames} editable timeline frames round-trip exactly through Aseprite, and every material preserves alpha. This focused fixture review is not a claimed full campaign clear.

Required broad suite: game.js syntax exits{suite[0]['exit']}; test_fl.js exits{suite[1]['exit']}. See full-suite.txt and verification.json for the exact output. If the known missing difficultyHealthBaseline15 helper remains, the suite is recorded as failed, not passed. No commit, push, installer or publication was requested or performed.

Open playback.html for selectable frame stepping; all-four-ship-transforms.gif shows the four transformation variants. draconus-normal-native.gif and draconus-chromium-native.gif show actual running-game handoffs. Runtime-visible canonical spellings remain Chronos and Dracodia; the preview uses Mike's Chronus/Draconus references.
'''
archive=R/'_ART_SOURCES/boss_ship_forms_1111';archive.mkdir(parents=True,exist_ok=True)
for name in ['generated','jobs','references','reviews']:shutil.copytree(W/name,archive/name,dirs_exist_ok=True)
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.json','.lua','.js','.txt']:shutil.copy2(p,archive/p.name)
ae=archive/'exports';ae.mkdir(exist_ok=True)
for p in E.iterdir():
 if p.is_file()and p.suffix in ['.aseprite','.webp','.png']and'_roundtrip'not in p.name:shutil.copy2(p,ae/p.name)
summary=dict(nativeChecks=len(checks['checks']),failures=[],rendererErrors=checks['errors'],requests=checks['requests'],exports=dict(exactFrames=frames,banks=len(M)),fullSuite=suite,runtimeHash=checks['runtimeHash'],protected=installed['protected'])
for p in [O/'README.md',archive/'README.md',R/'docs/BOSS_SHIPS_GUN_1111.md']:p.write_text(report,encoding='utf-8')
(O/'verification.json').write_text(json.dumps(summary,indent=2));shutil.copy2(W/'game-suite.txt',O/'full-suite.txt');qa=R/'docs/qa/boss_ship_forms_1111';qa.mkdir(parents=True,exist_ok=True)
for p in [O/'verification.json',O/'full-suite.txt',O/'verification/checks.json',O/'verification/traces.json']:shutil.copy2(p,qa/p.name)
note=f'''## November11,2026 - Original boss ships and Draconus gun

Mike requested distinct closed ship forms and complete copied-boss gun pickup.
SF1111 owns new24-frame Chronos/Dracodia ship transformations, both materials,
and the actual native morph-draw override. Closed ships have no gun. Dracodia
has the exclusive icon-box strike/eject/catch, full-actor gun acting, measured
muzzle/FOV, independent native gun HP/flash/break, stow and hammer recall.
Approved three-way hammer banks/native pools/progression remain protected.
{len(checks['checks'])} focused native checks and{frames} exact Aseprite frames pass.
Broad test_fl.js exits{suite[1]['exit']}; exact log: docs/qa/boss_ship_forms_1111.
Source/rebuild: _ART_SOURCES/boss_ship_forms_1111; docs/BOSS_SHIPS_GUN_1111.md.
No game.js edit, commit, push or installer.

'''.encode('utf-8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
if b'Original boss ships and Draconus gun'not in old:
 assert p.read_bytes()==old;p.write_bytes(note+old)
with zipfile.ZipFile(O/'BOF-boss-ships-and-gun-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
print('Saved animations, editable sources, native evidence and handoff.',flush=True)
