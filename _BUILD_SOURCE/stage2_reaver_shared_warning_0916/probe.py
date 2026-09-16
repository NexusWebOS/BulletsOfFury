"""Real Chromium proof for the Stage-2 Inferno Reaver role repair and shared shotgun warning."""
from pathlib import Path
import base64,http.server,json,math,sys
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'stage2_reaver_shared_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(2,'mini','yuri')");ok(fight.get('ok'),'native Stage-2 miniboss route opens in Chromium')
  keys=['nsb_inferno_reaver']+[f'l23fx_inferno_laser_{i}' for i in range(12)]+[f'l23fx_inferno_shotgun_{i}' for i in range(8)]+[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=999;run.stage=2;curStage=STAGES[1];camX=0;player.x=340;player.y=450;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;subBoss=null;subBossActive=false;spawnSubBoss('magmaward');subBoss.enter=false;subBoss.x=240;subBoss.y=120;subBoss.ty=120;subBoss._drawY=120;subBoss.fireCd=999;subBossActive=true;window.__reaverGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__reaverGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));shipBossAttack(subBoss);infernoReaverPassTick(subBoss,.73);infernoReaverPassTick(subBoss,.01);infernoReaverPassTick(subBoss,.01);return{name:subBoss.name,ship:subBoss._ship,shield:!!subBoss._mwBarrier,old:!!subBoss._mwAttack,pass:!!subBoss._irPass,slot:subBoss._l23Beam&&subBoss._l23Beam.slots[0],warm:subBoss._l23Beam&&subBoss._l23Beam.warm};}""",keys)
  ok(setup['name']=='INFERNO REAVER' and setup['ship']=='magmaward' and not setup['shield'] and not setup['old'],'the live demoted Reaver is shieldless and never enters the retired Magma Ward controller')
  ok(setup['pass'] and setup['slot']=='L' and setup['warm']>=3,'the live opener advances into a three-second shared left-cannon laser warning')
  ready=False
  for _ in range(320):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'Reaver hull, laser, shotgun and shared warning art decode before capture')
  def snap(name):
    page.evaluate('()=>{shake=0;window.__reaverGets=[];drawWorld(0)}')
    data=page.evaluate("""()=>{const b=subBoss,A=b._sba,W=A&&A.warning,B=W&&b._combatWarnings[W.id];return{name:b.name,shield:!!b._mwBarrier,pass:!!b._irPass,beam:b._l23Beam&&{slot:b._l23Beam.slots[0],t:b._l23Beam.t,warm:b._l23Beam.warm,released:b._l23Beam.released},attack:A&&{pat:A.pat,t:A.t,tell:A.tell,fired:A.fired,paths:W&&W.paths.map(q=>q.a)},warn:B&&{t:B.t,warm:B.warm,released:B.released,phase:l23FovPhase(B.t/B.warm)},shots:eBullets.map(q=>({kind:q.kind,fx:q._l23fx,x:q.x,y:q.y,a:Math.atan2(q.vy,q.vx)})),gets:Array.from(new Set(window.__reaverGets))}}""")
    raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,data
  p0,d0=snap('reaver_00_laser_pass')
  ok(d0['beam'] and not d0['beam']['released'] and len(d0['shots'])==0 and 'bmfx_fov_green_tall' in d0['gets'],'the repaired opening pass visibly begins with a harmless shared laser field')
  arm=page.evaluate("""()=>{subBoss._irPass=null;subBoss._l23Beam=null;subBoss._orb=null;subBoss._sba=null;subBoss._sbStep=0;subBoss.hp=subBoss.maxhp*.45;subBoss.x=240;subBoss.y=120;subBoss._sbaPhase=2;subBoss._combatWarnings={};eBullets=[];player.x=340;player.y=450;shipBossQueueAttack(subBoss);const A=subBoss._sba;return{pat:A.pat,tell:A.tell,paths:A.warning.paths.map(q=>q.a)};}""")
  ok(arm['pat']=='infernoburst' and arm['tell']>.65 and len(arm['paths'])==9,'the live shotgun commits nine warned trajectories with a readable delay')
  page.evaluate('()=>shipBossActionTick(subBoss,subBoss._sba.tell*.20)');p1,d1=snap('reaver_01_green')
  ok(d1['warn']['phase']=='green' and not d1['warn']['released'] and len(d1['shots'])==0,'green previews all nine lanes while the weapon is harmless')
  page.evaluate('()=>{player.x=45;player.y=300;shipBossActionTick(subBoss,subBoss._sba.tell*.30)}');p2,d2=snap('reaver_02_yellow')
  ok(d2['warn']['phase']=='yellow' and d2['attack']['paths']==arm['paths'] and len(d2['shots'])==0,'yellow preserves the committed fan after a late player move')
  page.evaluate('()=>{player.x=410;player.y=475;shipBossActionTick(subBoss,subBoss._sba.tell*.30)}');p3,d3=snap('reaver_03_red')
  ok(d3['warn']['phase']=='red' and d3['attack']['paths']==arm['paths'] and len(d3['shots'])==0,'red preserves all promised paths without releasing early')
  page.evaluate('()=>shipBossActionTick(subBoss,subBoss._sba.tell*.21)');p4,d4=snap('reaver_04_release')
  shot_angles=sorted(q['a'] for q in d4['shots']);warn_angles=sorted(arm['paths'])
  ok(d4['warn']['released'] and d4['attack']['fired'] and len(d4['shots'])==9,'nine rounds release only after the red warning completes')
  ok(all(q['kind']=='magma' and q['fx']=='inferno_shotgun' for q in d4['shots']),'every released round uses the authored Inferno shotgun projectile family')
  ok(all(abs(a-b)<1e-7 for a,b in zip(shot_angles,warn_angles)),'all nine projectiles follow the exact trajectories shown by the warning')
  shots=[p0,p1,p2,p3,p4]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  thumbs=[]
  for p in shots:
    im=Image.open(p).convert('RGB').resize((240,256),Image.Resampling.NEAREST);canvas=Image.new('RGB',(248,280),'black');canvas.paste(im,(4,4));ImageDraw.Draw(canvas).text((6,263),p.stem,fill='white');thumbs.append(canvas)
  contact=Image.new('RGB',(248*len(thumbs),280),'black')
  for i,im in enumerate(thumbs):contact.paste(im,(i*248,0))
  contact.save(OUT/'reaver_warning_contact.png')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'arm':arm,'frames':[d0,d1,d2,d3,d4],'shots':[str(p.relative_to(ROOT)) for p in shots],'contact':str((OUT/'reaver_warning_contact.png').relative_to(ROOT))};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
