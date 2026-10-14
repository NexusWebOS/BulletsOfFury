from pathlib import Path
import sys,json,base64,zipfile
from playwright.sync_api import sync_playwright
from PIL import Image
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');E=R/'extensions/bof-field-manual';A=E/'art';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));exports=[];errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  data=p.evaluate('()=>({pilots:PILOTS,specials:SPECIAL_INFO,displayAbilities:PC_SPECIAL,stages:STAGES.map(s=>({...s,bossName:debugFightFor(s.n,"boss")?.name||debugBossName(s.boss)})),fights:debugFightList(),weapons:WEAPONS,difficulties:DIFFS,enemies:ENEMY_ART})')
  def export(key,name):
   try:
    if not key or not p.evaluate('k=>!!XART._src[k]||XART.rdy(k)',key):return None
    p.wait_for_function('(k)=>XART.rdy(k)',arg=key,timeout=5000)
    url=p.evaluate('k=>{const im=XART.get(k),c=document.createElement("canvas");c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL("image/png")}',key)
    dest=A/(name+'.png');dest.write_bytes(base64.b64decode(url.split(',')[1]));im=Image.open(dest);im.thumbnail((440,440));im.save(dest);exports.append({'key':key,'file':dest.name});return 'art/'+dest.name
   except Exception:return None
  for q in data['pilots']:
   q['art']='art/'+q['key']+'.png';q['abilityArt']=export(data['displayAbilities'][q['key']]['icon'],'ability-'+q['key']) or export(p.evaluate('k=>specialArtKey("spicon_"+k)',q['key']),'ability-'+q['key'])
   if not q['abilityArt']:
    url=p.evaluate('k=>{const c=document.createElement("canvas");c.width=c.height=180;ph8Icon(c.getContext("2d"),specialArtKey("spicon_"+k),90,90,160);return c.toDataURL()}',q['key'])
    (A/('ability-'+q['key']+'.png')).write_bytes(base64.b64decode(url.split(',')[1]));q['abilityArt']='art/ability-'+q['key']+'.png'
  extras={}
  for k in ['nsw_icon_cole','nsw_ring_2','special_icon_cole_nuclear_warheads','nsw_icon_decker','nlz_mount','micon_thermoshock_0','special_icon_juggernaut_wrecking_ball']:
   art=export(k,k)
   if art:extras[k]=art
  for f in data['fights']:
   key=p.evaluate('f=>{const d=typeof SHIPBOSS!=="undefined"&&SHIPBOSS[f.kind];const m=typeof MEGABOSS!=="undefined"&&MEGABOSS[f.kind];return d?.key||m?.key||null}',f)
   f['art']=export(key,'boss-'+str(f['stage'])+'-'+f['role']) if key else None
  # Selected real registry entries, including tanks and elite aircraft; never substitute artwork.
  enemies=[]
  for name,key in data['enemies'].items():
   if len(enemies)>=24:break
   art=export(key,'enemy-'+name)
   if not art:art=export(key+'_idle','enemy-'+name)
   if art:enemies.append({'name':name,'key':key,'art':art})
  data['enemyPlates']=enemies;data['extraArt']=extras
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&XART.rdy(SC12_ART.key)&&bmfReady("game")}',timeout=120000);p.evaluate(shoot.STEP,15)
  p.screenshot(path=str(A/'hud-live.png'));p.locator('#siege-left').screenshot(path=str(A/'hud-left.png'));p.locator('#siege-right').screenshot(path=str(A/'hud-right.png'))
  # Real fight fixtures capture assembled modules and warnings as seen in the runtime.
  for stage,role in [(4,'boss'),(5,'mini'),(6,'mini'),(8,'mini'),(8,'boss')]:
   f=next(x for x in data['fights'] if x['stage']==stage and x['role']==role)
   p.evaluate('f=>debugStartFight(f,{pilot:"cole"})',f);p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=120000)
   for i in range(14):p.evaluate(shoot.STEP,30);p.wait_for_timeout(80)
   p.screenshot(path=str(A/f'encounter-{stage}-{role}.png'));f['scene']=f'art/encounter-{stage}-{role}.png'
   print('Captured',f['name'],flush=True)
  b.close()
finally:stop()
(E/'data.js').write_text('const MANUAL = '+json.dumps(data)+';',encoding='utf-8')
js=(E/'guide.js').read_text(encoding='utf-8')
start=js.index('for(const p of MANUAL.pilots)');end=js.index('const advice=',start)
js=js[:start]+'''const abilityDetail={cole:'NUCLEAR WARHEADS: native lock-on nuclear special. SONIC BOOM: separate timed pickup weapon; lasts 22 seconds and replaces primary fire while active. Charged release launches expanding damaging sound waves with a parked distortion trail. The warheads remain available independently.',decker:'CLOAKING SYSTEM: native targeting disruption. INCENDIARY SHOTGUN: separate timed weapon pickup, shown with its own remaining-time HUD row. A cloak is protection; the shotgun is your attack tool.',lizzie:'ATOM BOMB: nuclear missile ability. HEAVY TURRET: separate pickup attachment that arcs toward the nose, shrinks, docks, and fires heavy slugs. Its 15-second lifetime starts after docking. This is a distinct mounted weapon, not the same bomb under a second name.',freezer:'TIME FREEZE: battlefield control. THERMOSHOCK: a separate fire-and-ice orb attack with its own charge and authored release effects. The two functions work together but should be learned separately.',juggernaut:'WRECKING BALL: rage protection against enemy fire while active. CHARGE DASH: hold CHARGE + UP to wind up, then release to ram forward. Charge time determines distance; keep the destination lane clear.'};
for(const p of MANUAL.pilots){const s=MANUAL.displayAbilities[p.key];add('pilots',p.key,p.name,p.role,s.name+': '+(abilityDetail[p.key]||MANUAL.specials[p.key].desc),p.art,p.tint);add('abilities','ability-'+p.key,s.name,p.name+' / ABILITY LOADOUT',abilityDetail[p.key]||MANUAL.specials[p.key].desc,p.abilityArt,p.tint)}
''' +js[end:]
js=js.replace("['arsenal','Arsenal']","['abilities','Special abilities'],['hud','HUD field guide'],['enemies','Enemy recognition'],['arsenal','Arsenal']")
needle='function persist(){'
extra='''add('hud','hud-full','YOUR COMBAT CONSOLE','ACTUAL IN-GAME CAPTURE','Left: score, maneuver readiness, equipped weapon, upgrades and pilot. Right: radar, special loadout, lives, missiles and Retina lock. These are actual rendered panels, not a mockup.','art/hud-live.png');
add('hud','hud-left','FIREPOWER & FLIGHT','LEFT PANEL','Roll and somersault use filled readiness meters. Equipped weapon shows its current level; timed pickup loans have their own indicators. Speed and shield pips report upgrades.','art/hud-left.png');
add('hud','hud-right','TARGETS & RESOURCES','RIGHT PANEL','The special name includes paired abilities. The active special resource meter does not mean every paired pickup shares that resource. Radar contacts and Retina target lock are separate signals.','art/hud-right.png');
for(const e of MANUAL.enemyPlates)add('enemies','enemy-'+e.name,e.name.replaceAll('_',' ').toUpperCase(),'ACTUAL REGISTERED ENEMY ART','Recognize this silhouette before entering its firing lane. Look for the warning and leave room to cross. Registry: '+e.key+'.',e.art);
for(const f of MANUAL.fights){const id='fight-'+f.stage+'-'+f.role;const entry=entries.find(e=>e.id===id);if(entry)entry.art=f.art||f.scene;if(f.scene)add('bosses','scene-'+f.stage+'-'+f.role,f.name+' / IN THE ARENA','STAGE '+f.stage+' / '+f.role.toUpperCase(),'Actual assembled encounter captured through the game’s debug fight route. This image identifies the live fight and its arena; it is not a claim that every attack has been measured.',f.scene)}
'''
js=js.replace(needle,extra+needle);(E/'guide.js').write_text(js,encoding='utf-8')
css=(E/'style.css').read_text();css+='\n#hud-full,#scene-4-boss,#scene-5-mini,#scene-6-mini,#scene-8-mini,#scene-8-boss{grid-column:1/-1}.card img{max-height:360px}#hud-full img,[id^="scene-"] img{max-height:none}#hud-left img,#hud-right img{max-height:600px}\n';(E/'style.css').write_text(css)
m=json.loads((E/'manifest.json').read_text());m['version']='1.1.0';(E/'manifest.json').write_text(json.dumps(m,indent=2))
O=Path(r'C:\Users\Mike\Documents\New project\output\bof-field-manual');zpath=O/'BOF-Field-Manual-1.1.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for f in E.rglob('*'):
  if f.is_file():z.write(f,Path('bof-field-manual')/f.relative_to(E))
(R/'_shots/browser_pass_1012/graphics-export.json').write_text(json.dumps({'exports':exports,'enemies':len(enemies),'errors':errors},indent=2));print('Exports',len(exports),'enemies',len(enemies),'ZIP',zpath.stat().st_size,'errors',errors)
