"""Native PixelLab sonic-bank playback, damage flashes, tells and safe gaps."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/sonic_refine_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&window.BOF_SONIC_EFFECTS');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.mode="arcade";run.pilot="cole";pilotIndex=PILOTS.findIndex(q=>q.key==="cole");startRun(1);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);player.invuln=1e9;storySkip();BOFCinematicDirector.cancel();}')
  p.evaluate('''()=>{sx21Warm();window.sx21draws=[];const draw=ctx.drawImage;
   ctx.drawImage=function(im,...args){if(im?._so21)sx21draws.push({...im._so21,args});return draw.call(this,im,...args);};}''')
  p.wait_for_function('()=>Object.values(SX21_ART.banks).every(a=>XART.rdy(a.key)&&XART.rdy(a.sourceKey))')
  p.wait_for_function('()=>["rzbf_hull_0","rzbf_turret","rzbf_machinegun","rzb_sonic_wave"].every(k=>XART.rdy(k))')
  p.evaluate('()=>{diffKey="furious";DIFF=difficultyForRun(run.mode,diffKey);boss=null;enemies=[];spawnSubBoss("razorback");subBoss.enter=false;subBoss.y=VH*.3;subBoss.x=camLeftX()+viewW()/2;subBoss._rzb.trans=0;}')
  for attack in ['suppression','sonic','nova','missiles']:
   print(attack,p.evaluate('''attack=>{const b=subBoss,R=b._rzb;eBullets=[];R.attack=attack;R.state='guns';R.at=0;R.beat=-1;R.mgBeat=-1;R.waves=[];R.turret=0;R.a=0;R.tgt={x:b.x,y:b.y};for(let i=0;i<100;i++){razorbackUpdate(b,1/60);for(const q of eBullets){q.t+=1/60;q.x+=q.vx;q.y+=q.vy;}}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return eBullets.map(q=>({kind:q.kind,w:q.w,h:q.h,furious:q._rzbFurious,rzb:q._rzb}));}''',attack),flush=True)
   p.screenshot(path=str(O/('before-'+attack+'.png')))
  b.close()

finally:stop()
