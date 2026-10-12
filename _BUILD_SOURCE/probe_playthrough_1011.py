"""Real Chromium review of October 11 gameplay fixes and approved HUD."""
from pathlib import Path
import base64, json, sys
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/playthrough_1011/runtime';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,passed,data=None):
    checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name+((' '+json.dumps(data)) if not passed else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&XART.rdy(AC11_ART.key)&&XART.rdy("nli_3")&&XART.rdy("nmi_3");}',polling=50)
  p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=thaw=null;H3.release=false;H3.ending=null;
   run.lives=7;run.bombs=18;run.score=123456;player.x=worldWidth()/2;player.y=VH*.78;player.invuln=0;
   camX=player.x-VW/2;window.hudReviewJet=spawnEnemy('l6v_s2',player.x,170,{});hudReviewJet.y=170;}''')
  p.wait_for_function('()=>XART.rdy("ship_maverick")&&XART.rdy("n6v2_steel_intact_c")')
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();window.__bofFit();}')
  p.screenshot(path=str(OUT/'armored-command-stage6.png'))
  q=p.evaluate('''()=>{const f=ph8Frame(),r=f.rect;return{key:f.a.key,radar:!!r.radar,life:r.lives,weapon:r.weapon,top:AC11_ART.top,row:PH8.row,
   inside:Object.values(r).every(a=>a.every(Number.isFinite)&&a[0]>=0&&a[0]+a[2]<=VW&&a[1]>=0&&a[1]+a[3]<=PH8.height),state:PH8.last};}''')
  check('Approved Armored Command renders, with stocks above and no radar',q['key']=='hud_armored_command_1011' and not q['radar'] and q['life'][1]>q['row'] and q['weapon'][1]<q['row'],q)
  check('All eleven wells stay within proportional authored bands',q['inside'])
  check('HUD uses actual pilot stocks and score',q['state'][0]['lives']==7 and q['state'][0]['missiles']==18 and q['state'][0]['score']==123456)
  for width,height in [(1920,1080),(1280,720),(820,900),(480,900),(360,800)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('window.__bofFit()')
   q=p.evaluate('''()=>{const ids=['hud-row','screen','hud-bottom'];return ids.map(id=>{const a=document.getElementById(id).getBoundingClientRect();return{x:a.left,y:a.top,right:a.right,bottom:a.bottom,w:a.width};});}''')
   check(f'HUD and playfield fit {width}x{height}',all(v['x']>=-1 and v['right']<=width+1 and v['y']>=-1 and v['bottom']<=height+1 for v in q) and abs(q[0]['w']-q[2]['w'])<2,q)
  p.set_viewport_size(dict(width=1280,height=1000))
  q=p.evaluate('''()=>{run.stage=2;run.spaceMode=false;run.pilot='maverick';run.weapon=3;run.wvars=[];run.wlevels=WEAPONS.map(()=>1);run.wlevel=1;run.forge={};run.forgeForms={};run.forgeElems={fire:1};special=null;run.infusion=null;pBullets=[];
   applyPowerup({kind:'weapon',wtype:3,wvar:'laserbeam',x:240,y:300});pShoot();return{held:heldVariant(3),level:run.wlevels[3],kinds:pBullets.map(b=>b.kind),fixed:pBullets.every(b=>b.lv===1),forms:weaponBaseForms(3)};}''')
  check('Maverick pickup preserves fixed-tier lances while storing separate beam levels',q['held']=='mavhoming' and q['level']==2 and q['kinds']==['mavlaser']*3 and q['fixed'],q)
  check('Fire Whip stays absent until actually forged',not any(v['id']=='firewhip' for v in q['forms']))
  q=p.evaluate('''()=>{weaponFormSelect(3,{kind:'variant',id:'laserbeam'});applyPowerup({kind:'weapon',wtype:3,wvar:'mavhoming',x:240,y:300});pBullets=[];pShoot();const beam=heldVariant(3)==='laserbeam'&&pBullets.some(b=>b.kind==='beam');
   weaponFormSelect(3,{kind:'variant',id:'mavhoming'});window.reviewLance=forgePreviewNew(3,null,5);reviewLance.variant='mavhoming';reviewLance.pilot='maverick';return beam;}''')
  check('Explicit beam selection is also preserved by pickups',q)
  for batch in range(6):
   p.evaluate('()=>{for(let i=0;i<12;i++)forgePreviewTick(reviewLance,260,300,1/60);}');p.wait_for_timeout(20)
  q=p.evaluate('''()=>{const P=reviewLance;ctx.setTransform(SS,0,0,SS,0,0);forgePreviewDraw(P,60,80,300,350);return{err:P.err,fired:P.fired,visible:P.bullets.filter(b=>b.kind==='mavlaser'&&!b._launchDelay&&b.y<player.y).length};}''')
  p.locator('#screen').screenshot(path=str(OUT/'maverick-lance-preview.png'))
  check('Preview runs the real lance launch and homing tick',not q['err'] and q['fired']>0 and q['visible']>0,q)
  q=p.evaluate('''()=>{const stop=Snd.stopCue,seen=[];Snd.stopCue=k=>seen.push(k);forgePreviewCues.clear();forgePreviewCues.add('laser');forgePreviewCues.add('maverick');setState(GS.TITLE);Snd.stopCue=stop;return{seen,left:forgePreviewCues.size};}''')
  check('Leaving a preview stops its sampled cues',all(k in q['seen'] for k in ['laser','maverick']) and q['left']==0,q)
  q=p.evaluate('''()=>{const old=campSession,raw=localStorage.getItem(CAMP_AUTO_KEY);campSession=null;localStorage.setItem(CAMP_AUTO_KEY,JSON.stringify({v:CAMP_SAVE_VER,mode:'campaign',stage:3}));p2HubSync();const fresh=!campCanContinue()&&!CAMPHUB_ITEMS.some(i=>i.act==='continue'),load=campHubEnabled('load');
   campSession={v:CAMP_SAVE_VER,mode:'campaign',stage:3};p2HubSync();const same=campCanContinue()&&CAMPHUB_ITEMS.some(i=>i.act==='continue');campSession=old;if(raw===null)localStorage.removeItem(CAMP_AUTO_KEY);else localStorage.setItem(CAMP_AUTO_KEY,raw);return{fresh,load,same};}''')
  check('Fresh session hides Continue but retains explicit checkpoint Load',q['fresh'] and q['load'] and q['same'],q)
  q=p.evaluate('''()=>{run.stage=6;boss=null;subBoss=null;bossActive=subBossActive=false;stageTimer=22;AP10_X.intro=null;s6Opening=null;run._gp4StageX=false;s6WingInit();s6WingTick(.1);return{s:s6Wing.ships.length,t:s6Wing.combatTime};}''')
  check('Stage 6 ordinary controller fields allies and advances',q['s']>0,q)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready}')
  q=p.evaluate('''()=>{BOFCinematicDirector.cancel();story=special=fb2Talk=null;boss=subBoss=null;bossActive=subBossActive=false;run.weapon=1;run.wlevels[1]=3;run.wlevel=3;run.wvars=[];run.forge={};run.infusion=null;pBullets=[];player.shootCd=0;pShoot();return pBullets.filter(b=>b.kind==='spread').map(b=>({speed:Math.hypot(b.vx,b.vy),dmg:b.dmg,frame:projectileVisualFrame(b,24,16)}));}''')
  check('Ordinary spread travels at 336 px/sec with unchanged level-three damage and a stable plate',len(q)==5 and all(abs(v['speed']-5.6)<.01 and v['dmg']==3 and v['frame']==0 for v in q),q)
  q=p.evaluate('''()=>{const e=spawnEnemy('s1jetstrafer_b',220,100,{route:'straight'});e._s1DelayFrames=0;jetTick(e,1/60);e._dodge=0;e._pt11DodgeCd=0;const sides=[];for(let i=0;i<70;i++){pBullets=[{kind:'missile',x:e.x+(i%2?20:-20),y:e.y+50}];jetTick(e,1/60);sides.push(e._dodgeDir);}return{unique:new Set(sides.filter(Boolean)).size,dodge:e._dodge,cool:e._pt11DodgeCd,y:e.y};}''')
  check('Repeated homing threats cannot flip the Stage 1 dodge side every frame',q['unique']==1 and q['y']>130,q)
  q=p.evaluate('''()=>['mg','slug','pellet','bullet'].map(kind=>enemyOrdnanceCanIntercept({kind,x:240,y:160,vx:0,vy:3,w:5,h:9,mg:kind==='mg'}))''')
  check('Ordinary enemy pellets remain unshootable',not any(q),q)
  p.evaluate('()=>{pBullets=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();window.__bofFit();}')
  p.screenshot(path=str(OUT/'stage1-committed-fighter.png'))
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] or errors else 0)
