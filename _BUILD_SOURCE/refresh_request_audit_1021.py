from pathlib import Path
import sys,json,base64,http.server,zipfile,shutil
from playwright.sync_api import sync_playwright
from PIL import Image
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
E=R/'extensions/bof-field-manual'; A=E/'art'
O=R/'_shots/request_completion_1021'; O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE')); import shoot
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R)); errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4',timeout=180000);p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();UI20.warm();return stageLoadReady(1)&&UI20_KEYS.every(k=>XART.rdy(k))&&bmfReady(window.BOF_UI_FACE||"game")}',timeout=180000)
  data=p.evaluate('()=>({pilots:PILOTS,specials:SPECIAL_INFO,displayAbilities:PC_SPECIAL,stages:STAGES.map(s=>({...s,bossName:debugFightFor(s.n,"boss")?.name||debugBossName(s.boss)})),fights:debugFightList(),weapons:WEAPONS,difficulties:DIFFS,enemies:ENEMY_ART,air:AF21_ART,aliases:[...AF21.aliases].map(([alias,a])=>[alias,a.id])})')
  # Prime the native icon caches and wait for those very same sources.
  p.evaluate('()=>{run.score=123456;run.speed=3;run.shield=5;run.lives=3;run.bombs=24;highScore=Math.max(highScore,987654);SC12.invalidate();ui20Render([]);}')
  p.wait_for_function('()=>{const v=ui20Seat(1);ui20Render([]);return XART.rdy(v.portrait)&&[v.ship,v.weapon.key,"spicon_cole","nmi_2","special_icon_cole_nuclear_warheads"].every(ui20IconReady)}',timeout=180000)
  for i in range(6):p.evaluate(shoot.STEP,5);p.wait_for_timeout(80)
  p.evaluate('()=>{SC12.invalidate();SC12.fit(1440,1000);ui20Render([]);}')
  p.screenshot(path=str(A/'hud-live.png'))
  for side in range(2):
   image=p.evaluate('side=>{const c=document.createElement("canvas");c.width=376;c.height=1024;ui20Rail(c.getContext("2d"),side,ui20Seat(1));return c.toDataURL().split(",")[1]}',side)
   (A/('hud-right.png' if side else 'hud-left.png')).write_bytes(base64.b64decode(image))
  # Complete, actual current hulls; this never fits a whole atlas as a sprite.
  for name in ['rook','nyx','jace','kaia','voss','s1jetbomber']:
   p.wait_for_function('name=>!!af21Pose(name)',arg=name,timeout=180000)
   image=p.evaluate('name=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);af21Draw(af21Pose(name),VW/2,VH/2,200);return cv.toDataURL().split(",")[1]}',name)
   im=Image.open(__import__('io').BytesIO(base64.b64decode(image)));im.thumbnail((440,440));im.save(A/('current-'+name+'.png'))
  # Keep the original offline images, refresh numerical data without losing art links.
  old=json.loads((E/'data.js').read_text(encoding='utf-8').removeprefix('const MANUAL = ').rstrip().removesuffix(';'))
  for q in data['pilots']:
   prev=next(v for v in old['pilots'] if v['key']==q['key']);q.update({k:v for k,v in prev.items() if k in ['art','abilityArt']})
  for q in data['fights']:
   prev=next((v for v in old['fights'] if v['stage']==q['stage'] and v['role']==q['role']),{})
   # A renamed encounter must not inherit the silhouette of the old opponent.
   if prev.get('kind')==q.get('kind'):q.update({k:v for k,v in prev.items() if k in ['art','scene']})
  for k in ['enemyPlates','extraArt']:data[k]=old.get(k,[] if k=='enemyPlates' else {})
  runtime={k:data.pop(k) for k in ['air','aliases']}
  (E/'data.js').write_text('const MANUAL = '+json.dumps(data,separators=(',',':'))+';',encoding='utf-8')
  (O/'runtime-census.json').write_text(json.dumps({**data,**runtime},indent=2),encoding='utf-8')
  b.close()
finally:stop()
assert not errors,errors

im=Image.open(R/'_shots/menu_heart_1021/heart-actions.gif');frames=[];dur=[]
for i in range(0,im.n_frames,4):
 im.seek(i);frame=im.convert('RGB');frame.thumbnail((360,384),Image.Resampling.NEAREST);frames.append(frame);dur.append(im.info.get('duration',80)*min(4,im.n_frames-i))
frames[0].save(A/'chrome-heart.webp',save_all=True,append_images=frames[1:],duration=dur,loop=0,quality=82,method=4)
# This uncompressed duplicate was made by this refresh, not a source asset.
if (A/'chrome-heart.gif').exists():(A/'chrome-heart.gif').unlink()
js=(E/'guide.js').read_text(encoding='utf-8')
extra=r'''
// October21 verified controller notes. Stable dossier IDs preserve local bookmarks.
for(const [id,title,tag,body] of [
 ['hud-full','YOUR COMBAT CONSOLE','COMMAND ARMOR / LIVE CAPTURE','Left: Roll, Somersault, lives, missiles, primary ability and the separate secondary ability or Retina status. Right: pilot portrait, score, high score, equipped weapon, speed and armor. Narrow windows move these into the compact console below the playfield.'],
 ['hud-left','MANEUVERS & RESOURCES','LEFT PANEL','Solid green bars show Roll and Somersault readiness. Ship and missile icons show your stocks. The primary ability has its own filled meter and status; the second row distinguishes paired abilities instead of conflating their resources.'],
 ['hud-right','PILOT & FIREPOWER','RIGHT PANEL','Your pilot portrait and color tab identify the seat. Large score and high score sit above the equipped weapon and level. Solid cyan/blue meters show armor and speed upgrades.'],
 ['stage-x','STAGE X / SEABREAK COASTAL CITY','PROTECTED ENTRANCE / SEAMLESS SCROLL','A protected stage card leads from the coast into seamless city districts. Water animates independently. Harrier uses the main boss display; each Rebel has an individual pilot-themed bar.'],
 ['tempest','STAGE 5 / SIEGE BOMBER','FULL MODULE HEALTH','The displayed health includes the core and surviving weapon modules. Destroying the core alone does not end the fight. Break the cannon modules to cancel their owned warnings, beams and shots. Reposition during relocation and recovery.'],
 ['siege','STAGE 6 / CARGO FORTRESS','SEQUENCED LASER TURRETS','The enormous carrier crosses above the field. Read each turret windup and the committed beam lane; use the gaps and recovery rather than crossing a live ray. Destroyed turrets stop firing and stop drawing their live weapon animation.']
]){const e=entries.find(e=>e.id===id);if(e)Object.assign(e,{title,tag,body});}
add('survival','stormglass','STORMGLASS ACADEMY','DEDICATED TUTORIAL','Instructor Cole demonstrates FOV lanes, ground impact Retinas, Roll, Somersault, normal and Multi-Retina targeting, elemental weaknesses and pilot abilities. B.O.B. is a modular exam: missile pod 90 HP, cannon 110 HP, core 240 HP. Remove both pods first; the blue core is weak to fire.');
add('bosses','hammer-current','HAMMER / READ THE RECOVERY','STAGE 5 & CODE HAMMER','Shield impacts absorb damage and play feedback. The flashing SHOOT objective identifies the exposed hammer recharge target. The dedicated chaingun crate and icon precede his weapon transition. The corrupted final form adds a sky strike with side waves, broken-core blast with a safe angular sector, then a permanent unarmed fire phase. Roll and Somersault remain usable during Multi-Retina.');
add('bosses','phoenix-current','CORRUPTED FIRE PHOENIX','FINAL BOSS / MODULAR SWOON','Destroy the arm cannons to expose the body, head, wings and talons. When it retreats into depth, read the corner asterisk and angled arrow. Its diagonal dive commits from one end of an X; leave that path before contact.');
add('bosses','dracodia-download','DRACODIA / DOWNLOADED ARENAS','DEMONIC ROBOTIC FINALE','Ghost teleports, code shields and wireframe downloads precede the copied forms. Each arena download is a corrupted version of its origin stage. The rotating shadow ball tracks until its final approach, then commits; escape sideways or use a protected maneuver. It has no FOV warning.');
add('bosses','chrome-heart','CHROME HEART','BARBIE / EARNED SECRET','Win the real final fight as Falva or Lizzie to unlock BARBIE, including an eligible co-op seat. The optional pink chrome Hammer dances, slams, waltzes, forms absorbing heart shields and fires heart bouquets. Read the actual-ray FOVs and committed ground impact. This preview does not grant the unlock.','art/chrome-heart.webp','#ff63b4');
add('enemies','air-current','AIRCRAFT / FIVE MOTION BANKS','40 REFITS / 53 DESIGN IDS','Updated airborne families use fixed-pivot idle, attack, drift, barrel-roll and somersault banks. Native weapon mounts still own muzzle flashes and projectiles. Small aircraft trade excessive HP for faster attack pressure.','art/current-s1jetbomber.png');
add('bosses','rebel-formations','REBEL SQUAD / BREAK THE FORMATION','STAR / BOWLING / H / X','The formation warns before two shootable homing missiles per surviving fighter. Your guns and allied guns can intercept them. After the volley, the fighters scatter south, then scale back into the foreground with shadows. Heavy personal attacks are interlocked.');
for(const [key,title,body,color] of [
 ['rook','ROOK / BREACHHAMMER','Machine guns, heavy cannon, a committed charge ram and Rookhook. Leave the grapple line before he can pull and throw your jet.','#f5a64b'],
 ['kaia','KAIA / WIND CANNON','Slower teal wind-infused spread projectiles. Read every warned lane and slip between committed rays.','#57dec9'],
 ['jace','JACE / HELIX DRIFT','Charges a helix ball, then swerves and drifts into its attack. Preserve room on the opposite side of his committed route.','#72aaff'],
 ['voss','VOSS / TURBO SLINGSHOT','Flashes in turbo mode, scales into the distance, then returns visibly into a foreground ram. Move off the committed line.','#efbc58'],
 ['nyx','NYX / SHADOW ORBS','Regular Retina, Multi-Retina or a missile hit reveals her cloak. She charges and launches dark-purple shadow orbs after reveal.','#bd80ff']
])add('bosses','rebel-current-'+key,title,'STAGES 6 / X',body,'art/current-'+key+'.png',color);
'''
start=js.find('// October21 verified controller notes.')
if start>=0:js=js[:start]+js[js.index('function persist(){',start):]
js=js.replace('function persist(){',extra+'\nfunction persist(){')
(E/'guide.js').write_text(js,encoding='utf-8')
h=(E/'guide.html').read_text(encoding='utf-8').replace('October 12, 2026 edition','October 21, 2026 edition')
(E/'guide.html').write_text(h,encoding='utf-8')
m=json.loads((E/'manifest.json').read_text());m['version']='1.2.0';(E/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(E/'README.md').write_text('''# Bullets of Fury: Field Manual 1.2

Offline Manifest V3 extension. No host permissions, tracking, external code or network requests. Notes/bookmarks remain on this device.

## Install or update

Extract into a permanent folder. In chrome://extensions or edge://extensions enable Developer mode, choose Load unpacked and select the folder containing manifest.json. For an existing install, replace its files in the same folder and press Reload on its extension card to retain notes/bookmarks. Firefox can open guide.html as a standalone document; this is not a Firefox add-on.

October 21, 2026 edition. Current runtime pilot, weapon, stage and difficulty data; fresh Command Armor screenshots; paired-ability details; revised Hammer, Phoenix, Dracodia and Rebel tactics; Stormglass/B.O.B. and Chrome Heart briefings; actual current aircraft art. Unchanged historical encounter pictures remain illustrative; dynamic attack timing is authoritative in the game. This manual does not measure human win rates. Overdrive uses separate rules.

Chrome Heart uses the native gameplay reel. The guide does not grant password unlocks. Aqua music is not bundled. Original game art, generated insignia and BlackOpsOne font (license in art) retained.
''',encoding='utf-8')

# Refresh the live encyclopedia's authored aircraft contact sheets. Combat still
# runs through its native adapter; this only replaces stale source references.
path=R/'assets/data/enemy_atlas_1013.json';atlas=json.loads(path.read_text(encoding='utf-8'));aliases=dict(runtime['aliases']);models=runtime['air']['models'];count=0
for e in atlas['entries']:
 if e['game']!='bof':continue
 key=e.get('spawn',{}).get('type')
 mid=aliases.get(key)
 if not mid:continue
 model=models[mid];bank={'id':mid}
 for name,B in model['banks'].items():
  sheet=runtime['air']['sheets'][B['key']] if B['key'] in runtime['air']['sheets'] else next(s for s in runtime['air']['sheets'].values() if s['key']==B['key'])
  bank[name]={'kind':'strip','path':sheet['path'],'frames':B['frames'],'cell':128,'pivot':[64,64]}
 e['animationBanks']=[bank];e.setdefault('sources',[])
 if not any(s['file']=='assets/air_refit_1021.js' for s in e['sources']):e['sources'].append({'file':'assets/air_refit_1021.js','symbol':'af21Pose / af21Draw'})
 e['artKeys']=[model['banks']['idle']['key']];count+=1
atlas['generated']='2026-10-21';atlas['aircraftBankRefresh']={'date':'2026-10-21','entries':count,'note':'Aircraft contact sheets reflect the current refits; legacy source census is retained. Native previews use current game controllers.'}
for f in data['fights']:
 category='miniboss' if f['role']=='mini' else 'boss'
 e=next((e for e in atlas['entries'] if e['game']=='bof' and e['category']==category and e['spawn'].get('kind')==f['kind']),None)
 if not e:
  e={'id':'bof-'+category+'-'+f['kind'],'game':'bof','category':category,'status':'current','spawn':{'method':'encounter','kind':f['kind'],'role':f['role']},'attacks':[],'artKeys':[],'animationBanks':[],'sources':[{'file':'assets/game.js','symbol':'debugFightList / spawnBoss'}]};atlas['entries'].append(e)
 e['stages']=[f['stage']];e['spawn']['stage']=f['stage'];e['name']=f['name']
 # Historical HP/source snapshots do not describe the updated current opponent.
 if f['kind'] in ['siegebomber','siegefortress17']:e.pop('audit',None);e['runtime']={'controller':'siegeBomberTick' if f['kind']=='siegebomber' else 'warhiveTick / sc13GunDraw'}
 if f['kind']=='siegebomber':e['attacks']=[{'name':'Full module fight','description':'Core plus surviving cannons share the displayed health budget. Core loss does not kill surviving weapon modules.'},{'name':'Paired lances and flak','description':'Animated windup, recoil and recovery follow the native warning and beam owners. Destroyed cannons cancel their own ordnance.'}]
 if f['kind']=='siegefortress17':e['attacks']=[{'name':'Cargo fortress laser batteries','description':'Sequential turret windups and committed laser lanes. Destroying a turret cancels its pending release and its live animation.'}]
for e in atlas['entries']:
 if e['id']=='bof-miniboss-spacebomber':e['status']='legacy-spawnable'
 if e['id']=='bof-form-vileexistence-2':e['attacks']=[{'name':'Corrupted fire Phoenix','description':'Independent head, body, wings, claws and removable arm cannons. Losing the cannons triggers depth retreats and diagonal corner dives; asterisk/angled arrows identify the committed X route.'}]
 if e['id']=='bof-form-vileexistence-8':e['attacks']=[{'name':'Code Hammer','description':'Two-handed energy hammer, absorbing digital shield, sky strike with side waves, broken-core angular blast and permanent unarmed fire phase. Native hit flashes, recovery and Retina targets remain active.'}]
 if e['category']=='rebel' and e['game']=='bof':e['attacks'].append({'name':'Formation missile volley','description':'Star, bowling, H and X formations warn before shootable homing missile volleys. Scatter south, then scale back north with shadows; heavy attacks are interlocked.'}) if not any(a.get('name')=='Formation missile volley' for a in e['attacks']) else None
src=(R/'assets/chrome_heart_art_1021.js').read_text(encoding='utf-8');heart=json.loads(src[src.index('=')+1:].strip().removesuffix(';'))
if not any(e['id']=='bof-secret-chrome-heart' for e in atlas['entries']):
 atlas['entries'].append({'id':'bof-secret-chrome-heart','name':'CHROME HEART','game':'bof','category':'password-boss','status':'current','stages':[5],'passwords':['BARBIE'],'spawn':{'method':'chrome-heart','stage':5,'kind':'chromehammer'},'attacks':[{'name':n,'description':d} for n,d in [('Dance fan','Aimed heart volleys after complete-ray FOV warnings.'),('Heart hammer slam','Committed ground impact and native recovery.'),('Heart shield','Absorbs damage without deflection; breakable energy budget.'),('Hammer waltz','Moving spin with ring bursts.'),('Heart bouquet','Wider warned spread with open lanes.')]],'animationBanks':[],'artKeys':[s['key'] for s in heart['sheets'].values()],'sources':[{'file':'assets/chrome_heart_1021.js','symbol':'ch21Start / ch21Init'}],'runtime':{'controller':'ch21Tick','notes':'Read-only preview does not grant the account unlock. Real BARBIE requires a final win as Falva or Lizzie.'}})
entry=next(e for e in atlas['entries'] if e['id']=='bof-secret-chrome-heart')
entry['animationBanks']=[{'id':'chrome-heart',**{name:{'kind':'strip','path':heart['sheets'][name]['path'],'frames':len(B['frames']),'cell':[B['w'],B['h']],'pivot':B['pivot']} for name,B in heart['banks'].items()}}]
path.write_text(json.dumps(atlas,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
path=R/'assets/enemy_atlas_engine_1013.js';s=path.read_text(encoding='utf-8')
s=s.replace('BOFDEBUG.lab.on(Math.min(9,stage)', 'run._heartMode=false;BOFDEBUG.lab.on(Math.min(9,stage)') if 'run._heartMode=false;BOFDEBUG.lab.on' not in s else s
if "s.method==='chrome-heart'" not in s:s=s.replace("}else if(s.method==='encounter'||s.method==='rebel'){","}else if(s.method==='chrome-heart'){\n    run._heartMode=true;spawnBoss('chromehammer');A.actor=boss;\n   }else if(s.method==='encounter'||s.method==='rebel'){")
s=s.replace('pattern:b._ep13?.kind||', 'pattern:b._heart?.action?.type||b._ep13?.kind||') if 'pattern:b._heart?.action?.type||' not in s else s
path.write_text(s,encoding='utf-8')
path=R/'assets/enemy_atlas_1013.js';s=path.read_text(encoding='utf-8').replace("['heading','roll','idle','attack','fire','move']","['heading','idle','attack','drift','roll','somer','fire','move']").replace("['heading','idle','attack','drift','roll','somer','fire','move']","['heading','idle','attack','drift','roll','somer','fire','move','dance','slam','spin','channel','heart','shield']");path.write_text(s,encoding='utf-8')
path=R/'enemy-atlas.html';s=path.read_text(encoding='utf-8').replace('13 OCT 2026','21 OCT 2026 / AIR REFIT');path.write_text(s,encoding='utf-8')
Z=Path(r'C:/Users/Mike/Documents/New project/output/bof-field-manual/BOF-Field-Manual-1.2.zip');Z.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED) as z:
 for f in E.rglob('*'):
  if f.is_file():z.write(f,Path('bof-field-manual')/f.relative_to(E))
report={'errors':errors,'aircraftEntriesRefreshed':count,'manualVersion':'1.2.0','zip':str(Z),'bytes':Z.stat().st_size}
(O/'refresh.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
