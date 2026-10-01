import sys, json, base64, time, http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
out=ROOT/'_shots/fusion_0930';out.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
def ok(cond,name,detail=None):
 results.append(dict(ok=bool(cond),name=name,detail=detail));print(('OK ' if cond else 'FAIL ')+name,detail or '',flush=True)
def grab(p,name):
 data=p.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
 (out/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
setup="""() => {diffKey='furious';DIFF=DIFFS.furious;run.mode='campaign';run.pilot='yuri';beginStage(5);setState(GS.PLAY);story=null;special=null;player.reset();
 gravityMode.phase='active';gravityMode.t=6;run.spaceMode=true;run.spaceWeapon=1;run.spaceLevels=[3,3,3];
 player.x=VW/2;player.y=VH-95;enemies=[];pBullets=[];eBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
 stagePlan=[];waveIdx=999;spawnClock=9999;fusion30Warm();return true;}"""
port,stop=sh.serve(str(ROOT))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1100,'height':1000})
 p.on('pageerror',lambda e: errors.append(str(e)))
 p.on('console',lambda m: errors.append(m.text[:300]) if m.type=='error' or 'draw error' in m.text else None)
 p.goto('http://127.0.0.1:%s/index.html'%port,wait_until='load',timeout=120000)
 p.wait_for_function('() => (window.__bofFrames|0)>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
 p.evaluate(setup);p.wait_for_function('() => Object.values(FUSION30_ART).every(a=>XART.rdy(a.key))',timeout=30000)
 row=p.evaluate("""()=>{const c=document.createElement('canvas');c.width=620;c.height=150;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.fillStyle='#091019';g.fillRect(0,0,c.width,c.height);for(let i=1;i<=5;i++)spaceAtlasIconBlit(g,'space_fusion_icon_'+i,62+(i-1)*124,75,128,true);return c.toDataURL();}""")
 (out/'approved_icon_row.png').write_bytes(base64.b64decode(row.split(',')[1]))
 ok(p.evaluate("() => spaceWeaponName()==='FUSION CANNON' && spaceWeaponIconKey()==='space_fusion_icon_3'"),'Fusion name and HUD icon')
 for pct,scale in [(100,1),(150,1.5),(199,2)]:
  r=p.evaluate("p => {pBullets=[];spaceShadowRelease(FUSION30_FULL*p/100);let b=pBullets.find(b=>b.kind==='spaceFusion');return b?{scale:b.scale,w:b.w,h:b.h}:null;}",pct)
  ok(r and r['scale']==scale,str(pct)+'% release size',r)
 p.evaluate("() => {pBullets=[];run._spaceShadowCharge=FUSION30_FULL*1.95;run._spaceShadowHeld=true;drawWorld(0);}");grab(p,'charged_195')
 p.evaluate("() => {spaceShadowRelease(FUSION30_FULL*1.95);drawWorld(0);}");grab(p,'beam_195')
 r=p.evaluate("""() => {pBullets=[];enemies=[];const e=spawnEnemy('s1jetbomber_b',player.x,player.y-180,{});e.hp=e.maxhp=900;e.w=55;e.h=60;
 spaceShadowRelease(FUSION30_FULL);const b=pBullets.find(q=>q.kind==='spaceFusion');for(let i=0;i<12;i++)spaceBulletTick(b,1/60);
 return {hp:e.hp,hits:b._hit.filter(t=>t===e).length,fx:pBullets.filter(q=>q.kind==='spaceFusionFx').length};}""")
 ok(r['hp']<900 and r['hits']==1 and r['fx']>=2,'beam sweeps target once and creates impact/scar',r)
 # Exercise real playerHit/death code, shields and invulnerability must not absorb overload.
 for stage in [5,9]:
  p.evaluate(setup)
  r=p.evaluate("""stage => {run.stage=stage;run.shield=5;player.invuln=120;run._spaceShadowHeld=true;run._spaceShadowCharge=FUSION30_FULL*1.99;
 const deaths=stageStats.deaths;spaceShadowTick(FUSION30_FULL*.01,true);
 const once=stageStats.deaths;spaceShadowTick(.1,true);
 return {dead:player.dead,spin:!!player._spin,deathT:player.deathT,shield:run.shield,charge:run._spaceShadowCharge,weapon:run.spaceWeapon,deaths:once-deaths,repeat:stageStats.deaths-once,beams:pBullets.filter(q=>q.kind==='spaceFusion').length};}""",stage)
  ok(r['dead'] and (r['spin'] or r['deathT']>0) and r['shield']==0 and r['charge']==0 and r['weapon']==0 and r['deaths']==1 and r['repeat']==0 and r['beams']==0,'Stage '+str(stage)+' 200% is one real death despite protection',r)
  p.evaluate('() => drawWorld(0)');grab(p,'overload_stage'+str(stage))
 p.evaluate(setup)
 r=p.evaluate("() => {run._spaceShadowCharge=1;run._spaceShadowHeld=true;run.spaceWeapon=0;spaceShadowTick(.1,false);return run._spaceShadowCharge;}")
 ok(r==0,'switching weapon cancels charge')
 r=p.evaluate("() => {run.stage=8;return Array.from({length:500},()=>[mslBigPackForStage(8),mslPackRoll()]).flat().includes('missilepack100');}")
 ok(not r,'random Stage8 supply never gives x100')
 r=p.evaluate("() => {powerups=[];run.retinaScan=false;retinaScanSupply({kind:'mcrate',x:100,y:100});return powerups.length;}")
 ok(r==0,'retina upgrade no longer spawns')
 r=p.evaluate("() => {run.stage=5;run._spaceArmoryBag=['spacehelper'];return Array.from({length:30},()=>spaceArmoryRoll()).includes('spacehelper');}")
 ok(not r,'Stage5 helper removed from fresh and saved reward bags')
 r=p.evaluate("""() => {setState(GS.PASSWORD);pwInput='HAMMER';let calls=0,value='';const submit=submitPassword,st=Input.menuStart;
 submitPassword=()=>{calls++;value=pwInput;};Input.menuStart=()=>true;
 try{drawPassword(1/60);}finally{submitPassword=submit;Input.menuStart=st;}return {calls,value};}""")
 ok(r=={'calls':1,'value':'HAMMER'},'Start submits once without inserting keypad text',r)
 ok(not errors,'no browser errors',errors[:8]);b.close()
stop();(out/'results.json').write_text(json.dumps(results,indent=2))
sys.exit(0 if all(r['ok'] for r in results) else 1)
