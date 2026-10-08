"""Isolate the real Sovereign damaged-weapon ram and shared body collision."""
from pathlib import Path
import json,sys,time,http.server,base64,argparse
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--out',default='ram_before');ap.add_argument('--candidate');ap.add_argument('--ram-fix',action='store_true');ap.add_argument('--matrix',action='store_true');a=ap.parse_args();O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *args:None;port,stop=shoot.serve(str(R));rows=[];errors=[]
TEST=r'''c=>{BAL7.setup({stage:4,kind:'stormsovereign',diff:c.diff,pilot:'juggernaut',level:0,seed:7});const b=B;player.x=worldWidth()*(c.position||.5);player.y=VH-65;b.x=worldWidth()/2;b.y=100;b._drawY=b.y;b.enter=false;b._be=null;b._er26.mode='recover';b._er26.home=100;b._hc1007=null;for(const p of b._mr27.parts.slice(0,2)){p.dead=true;p.hp=0;}b._mr27.ram1002=null;b._s4war.shield.active=c.shield;b._s4war.shield.rearming=false;player.invuln=0;run.shield=0;let t=0,warning=null,firstDrive=null;for(let i=0;i<360&&!player.dead;i++){t+=1/60;BAL7.q.t=t;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();if(!c.stationary&&t>=c.reaction)for(const k of keybindFor(1)[c.position>.5?'left':'right'])if(!k.startsWith('pad_'))Input.keys[k]=true;eBullets=[];pBullets=[];groundTargetingReset();stateT+=1/60;updatePlay(1/60);const E=b._mr27.ram1002;if(!warning&&b._er26.warnings?.length)warning=JSON.parse(JSON.stringify(b._er26.warnings[0]));if(firstDrive===null&&E?.state==='drive')firstDrive=t;if(c.captureAt&&t>=c.captureAt)break;if(firstDrive!==null&&E?.state==='return'&&E.t>.2)break;}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {...c,survived:!player.dead,t,firstDrive,w:b.w,h:b.h,shieldRadius:b.w*.67,warning,hits:BAL7.q.hits,endPosition:{x:player.x,y:player.y,bx:b.x,by:b.y}};}'''
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--mute-audio']);p=b.new_page();p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort());p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  if a.ram_fix:p.route('**/assets/feedback_1002.js',lambda r:r.fulfill(status=200,content_type='text/javascript',body=(R/'_BUILD_SOURCE/maneuver_cases_1007/feedback_ram_candidate_1007.js').read_text(encoding='utf-8')))
  if a.ram_fix:p.route('**/assets/encounters_0926.js',lambda r:r.fulfill(status=200,content_type='text/javascript',body=(R/'_BUILD_SOURCE/maneuver_cases_1007/encounters_ram_candidate_1007.js').read_text(encoding='utf-8')))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  if a.candidate:p.add_script_tag(path=a.candidate)
  p.evaluate("()=>BAL7.setup({stage:4,kind:'stormsovereign',diff:'normal'})");deadline=time.monotonic()+90
  while time.monotonic()<deadline:
   p.evaluate('()=>{stageLoadTick();drawWorld(0);}');p.wait_for_timeout(35)
   if p.evaluate('()=>stageLoadInfo(4).ready'):break
  for diff in ['easy','normal','hard','furious']:
   for shield in [False,True]:
    for stationary in [False,True]:
     for position in ([.15,.5,.85] if a.matrix else [.5]):
      c=dict(diff=diff,shield=shield,stationary=stationary,reaction=.4,position=position);rows.append(p.evaluate(TEST,c));p.wait_for_timeout(5)
   print(diff,flush=True)
  p.evaluate(TEST,dict(diff='normal',shield=True,stationary=True,reaction=.4,captureAt=.65,position=.5))
  (O/'tell.png').write_bytes(base64.b64decode(p.evaluate("()=>cv.toDataURL().split(',')[1]")));b.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf-8');print(json.dumps({'moving':[{k:r[k] for k in ['diff','shield','survived','firstDrive','w','shieldRadius','warning','hits']} for r in rows if not r['stationary']],'errors':errors}));assert not errors
