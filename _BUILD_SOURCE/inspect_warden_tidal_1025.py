"""Native pre-change rendering diagnostics; all output is ignored scratch."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
import json,http.server,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_tidal_1025/before';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1'
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R));errors=[];out=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=bc.new_page()
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(7,'boss'),{pilot:'cole'});spawnBoss('sludgeemperor');debugFight.spawned=true;bossActive=true;warnT=0;s7mInit(boss);s7mSet(boss,'recover');BOFCinematicDirector.cancel();DBGT.god=true;player.invuln=1e9;player.y=VH-65;bm9Warm(bm9StageNames(7));r25Warm(7);s7mWarm();}")
  p.wait_for_function('()=>{stageLoadTick();return r25Warm(7)&&stageLoadReady(7)&&bm9StageNames(7).every(n=>BM9_ART[n].every(a=>XART.rdy(a.key)))}',timeout=180000)
  for mode in ['recover','chase','battery1009','chaingun','swipeL','swipeR','swipeX','jump']:
   p.evaluate("m=>{const b=boss,M=b._s7mod;b.x=worldWidth()/2;b.y=260;b._drawY=b.y;M.height=0;M.drop=0;M.lean=0;M.r25Gait=null;s7mSet(b,m);}",mode)
   for t in [0,.32,1.25,1.40,1.7]:
    q=p.evaluate("t=>{const b=boss,M=b._s7mod;M.t=t;drawWorld(0);return{mode:M.mode,t,legs:s7mPose(b).filter(p=>['frontL','frontR','gunL','gunR'].includes(p.id)).map(p=>{const im=s7mCell('warden',p.cell,true);let ink=0;if(im){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);for(const a of g.getImageData(0,0,c.width,c.height).data.filter((v,i)=>i%4===3))if(a>48)ink++;}return{...p,ink,loaded:!!im};})};}",t);out.append(q)
    if t in [0,1.25,1.7]:p.screenshot(path=str(O/(mode+'-'+str(t)+'.png')))
  p.evaluate("()=>{const b=boss,M=b._s7mod;b.x=worldWidth()/2;b.y=330;s7mSet(b,'recover');M.r25Gait=null;}")
  trail=[]
  for i in range(12):
   p.evaluate(STEP,4);trail.append(p.evaluate('({y:boss.y,g:boss._s7mod.r25Gait,mode:boss._s7mod.mode,pose:s7mPose(boss).filter(p=>p.r25).map(p=>({id:p.id,f:p.frame,stance:p.stance}))})'))
  (O/'diagnostics.json').write_text(json.dumps({'poses':out,'retreat':trail,'errors':errors},indent=2),encoding='utf8')
  print(json.dumps({'errors':errors,'unloaded':[(q['mode'],q['t'],p['id'],p['cell'])for q in out for p in q['legs']if not p['loaded']],'retreat':trail[-1]},indent=2),flush=True);br.close()
finally:stop()
