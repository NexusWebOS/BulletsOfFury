"""Native gameplay checks for boat spreads, sonic tells and space death resets."""
import base64,http.server,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(sh.GAME)
OUT=Path(sh.GAME)/'_shots/repair_0927';OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(str(ROOT));errors=[];report={}
RESET="""stage=>{diffKey='hard';DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.stage=stage;beginStage(stage);setState(GS.PLAY);player.reset();player.invuln=99999;story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;player.x=worldWidth()/2;player.y=VH*.78;run.shield=0;}"""
def shot(p,name):
 p.evaluate('()=>{const inv=player.invuln;player.invuln=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);player.invuln=inv;}')
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1100,'height':1200});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate(RESET,1)
  report['boats']=p.evaluate("""()=>{const boat=spawnEnemy('s1boatpatrol',player.x,200,{});navalInit(boat,'gun');boat.enter=false;boat._entry=0;boat._navIn=1;boat._burst=1;boat._shotCd=0;navalTick(boat,.016);const shots=eBullets.map(q=>({x:q.x,y:q.y,vx:q.vx,vy:q.vy})),before=eBullets.length;for(const type of ['s1boatgun','s1boatpatrol','s1corvette'])enemyVolley({...boat,type,_volCd:0},true);return{shots,extra:eBullets.length-before};}""")
  p.evaluate('()=>{for(let f=0;f<12;f++)for(const q of eBullets){q.x+=q.vx;q.y+=q.vy;}}');shot(p,'boat-turret-spread')
  p.evaluate("()=>{spawnBoss('damkeeper');boss.enter=false;boss._ovIntro.done=true;boss._ovAirborne=false;boss.y=VH*.27;ovSonicStart(boss);ovSonicComboTick(boss,1.94);}")
  p.wait_for_function("()=>XART.rdy('ovbody_intact')")
  p.wait_for_function("()=>['bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger'].every(k=>XART.rdy(k))")
  p.wait_for_timeout(300);shot(p,'sonic-fov-warning')
  report['sonic']=p.evaluate("""()=>{let count=0,call=null;const draw=combatWarningDraw;combatWarningDraw=(o,q)=>{count++;call=q;draw(o,q);};try{ovSonicWarningDraw(boss);}finally{combatWarningDraw=draw;}const before=eBullets.filter(q=>q._ovSonicWave).length;ovSonicComboTick(boss,.61);ovSonicComboTick(boss,.01);return{count,width:call.width,progress:call.progress,before,after:eBullets.filter(q=>q._ovSonicWave).length,warningClock:boss._combatWarnings.sonicWave.t};}""")
  report['space']=[]
  for stage in [5,9]:
   p.evaluate(RESET,stage)
   p.evaluate("()=>{gravityMode.phase='active';gravityMode.narrative=false;run.spaceWeapon=1;run.spaceLevels=[5,5,5];run.spaceAkimbo=1;spaceShadowTick(.8,true);}")
   p.wait_for_function("()=>XART.rdy('gravity_space')||typeof spaceAtlasRect==='function'")
   p.wait_for_timeout(400);shot(p,'shadow-charge-'+str(stage))
   report['space'].append(p.evaluate("""()=>{let meter=0;const draw=spaceShadowIndicatorDraw;spaceShadowIndicatorDraw=(...args)=>{meter++;draw(...args);};try{gravityModeDrawShip(player.x,player.y,SPACE_SHIP_SIZE);}finally{spaceShadowIndicatorDraw=draw;}spaceShadowTick(.8,true);spaceShadowTick(.01,false);const charged=pBullets.filter(q=>q.kind==='shadowOrb').length;player.invuln=0;run.shield=0;playerHit();const result={stage:run.stage,meter,charged,weapon:run.spaceWeapon,levels:run.spaceLevels.slice(),akimbo:run.spaceAkimbo,charge:run._spaceShadowCharge,held:run._spaceShadowHeld};pBullets=[];spaceLaserFire();spaceVolleyFire();result.lasers=pBullets.filter(q=>q.kind==='spaceLaser').length;result.volley=pBullets.filter(q=>q.kind==='spaceVolley').length;result.volleyLevels=pBullets.filter(q=>q.kind==='spaceVolley').map(q=>q.lv);return result;}"""))
  report['audio']=p.evaluate("""async()=>{const ac=new AudioContext(),result=[];try{for(const key of ['spaceShadowCharge','spaceShadowRelease']){const path=BOFA.sfx[key],r=await fetch(path),d=await ac.decodeAudioData(await r.arrayBuffer());result.push({key,path,seconds:d.duration});}}finally{await ac.close();}return result;}""")
  report['errors']=errors;(OUT/'space-boats-probe.json').write_text(json.dumps(report,indent=2));b.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
shots=report['boats']['shots'];assert len(shots)==3 and len({q['vx'] for q in shots})==3 and all(q['vy']>0 for q in shots)
assert len({(q['x'],q['y']) for q in shots})==1 and report['boats']['extra']==0
assert report['sonic']['count']==1 and report['sonic']['before']==0 and report['sonic']['after']>0
assert all(r['meter']==1 and r['charged']==2 and r['weapon']==0 and r['levels']==[0,1,1] and r['akimbo']==r['charge']==0 and not r['held'] and r['lasers']==12 and r['volley']==3 and r['volleyLevels']==[1,1,1] for r in report['space'])
assert all(r['seconds']>0 for r in report['audio'])
