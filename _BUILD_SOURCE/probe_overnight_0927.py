"""Live Chromium regression diagnostics for Mike's September 27 video."""
from pathlib import Path
import json,base64,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927');OUT.mkdir(exist_ok=True,parents=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
SETUP="""n=>{diffKey='normal';DIFF=DIFFS.normal;run.mode='arcade';run.pilot='cole';beginStage(n);setState(GS.PLAY);player.reset();player.invuln=9999;story=null;special=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;bossDefeated=false;groundTargetingReset();s6Opening=null;mapScroll=1200;player.x=worldWidth()/2;player.y=VH*.8;camX=player.x-viewW()/2;return {stage:n,zoom:viewZoom(),x:player.x,y:player.y};}"""
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  report['kills']=[]
  for n in range(1,10):
   p.evaluate(SETUP,n)
   report['kills'].append(p.evaluate("""n=>{const x=player.x,y=player.y,z=viewZoom(),cx=camX;let delta=0,viewDelta=0;
    for(let j=0;j<8;j++){const e=spawnEnemy('scout',player.x+60,player.y-170,{});if(e)hitEnemy(e,9999);for(let k=0;k<5;k++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);delta=Math.max(delta,Math.hypot(player.x-x,player.y-y));viewDelta=Math.max(viewDelta,Math.abs(camX-cx));}}
    return {stage:n,delta,viewDelta,zoomDelta:viewZoom()-z,state};}""",n))
   p.wait_for_timeout(20)
  report['missiles']=[]
  for target in ['enemy','hammer','bomber']:
   p.evaluate(SETUP,5)
   result=p.evaluate("""target=>{run.spaceMode=true;run.spaceLevels=[3,3,3];run.spaceVolleyLevel=3;window.B=null;
    if(target==='enemy'){B=spawnEnemy('s5space_scavenger',player.x,120,{});if(!B)B=spawnEnemy('scout',player.x,120,{});B.hp=B.maxhp=1000;}
    else if(target==='hammer'){spawnBoss('chromehammer');B=boss;B.enter=false;B._noHit=false;hammerState(B,'hammer');B._hammer.balance0922=true;B.x=player.x;B.y=130;}
    else{spawnSubBoss__inner('siegebomber');B=subBoss;B.enter=false;B.x=player.x;B.y=130;}
    const before=B.hp;spaceVolleyFire();const starts=pBullets.map(q=>({kind:q.kind,t:q._target?.kind||q._target?.type,dead:q._target?.dead}));
    for(let i=0;i<120;i++){for(const q of pBullets)if(!q.dead)spaceBulletTick(q,1/60);pBullets=pBullets.filter(q=>!q.dead);}
    return {target,before,after:B.hp,starts,left:pBullets.map(q=>({x:q.x,y:q.y,kind:q.kind})),modules:B._hammer?{hammer:B._hammer.hammerHP,gun:B._hammer.chainHP}:null};}""",target)
   report['missiles'].append(result)
  p.evaluate(SETUP,6)
  p.evaluate("()=>{spawnBoss('warhive');B=boss;B.enter=false;B.x=worldWidth()/2;B.y=VH*.55;B._whv.cy=B.y;B._whv.cx=B.x;B._whv.doorOpen=true;whvLaunchJet(B);window.J=enemies[enemies.length-1];window.path=[];}")
  for i in range(13):
   p.evaluate("()=>{path.push({x:J.x,y:J.y,scale:J._scale,heading:J._faceAng});for(let f=0;f<6;f++)hivewingTick(J,1/60,ELITEX.hivewing);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}")
   if i in [0,5,10]:shot(p,'harrier-launch-'+str(i))
   p.wait_for_timeout(40)
  report['bay']=p.evaluate('()=>path')
  p.evaluate(SETUP,4);report['zoom']=p.evaluate("()=>{const before=viewZoom();spawnBoss('stormsovereign');return {before,after:viewZoom()};}")
  report['errors']=errors;(OUT/'diagnostics.json').write_text(json.dumps(report,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
