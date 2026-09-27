"""Step-controlled native play through actual keyboard events, with ordinary lives/damage.
Read JSON {keys:[...],seconds:...} from stdin. This is not uninterrupted real-time play.
"""
import ast, base64, http.server, json, sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright

name=sys.argv[1] if len(sys.argv)>1 else 'tempest'
stage,kind,mini={'hammer':(5,'chromehammer',False),'tempest':(6,'tempestbrothers',True),'ward':(2,'magmaward',True),'razorback':(1,'razorback',True),'warden':(7,'sludgeemperor',False),'horizon':(9,'voidhorizon',True)}[name]
case={'stage':stage,'kind':kind,'mini':mini,'diff':sys.argv[2] if len(sys.argv)>2 else 'normal'}
OUT=Path('_shots/overnight_0927/manual-'+name+'-'+case['diff']+('-'+sys.argv[3] if len(sys.argv)>3 else ''));OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];actions=[];held=set()
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(100)
  p.evaluate(SETUP,case)
  print(p.evaluate("""c=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.lives=4;run.contUsed=0;run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.spaceWeapon=0;run.spaceLevels=[3,3,3];run.forge={};run.wvars=[];run.infusion=null;run.bombs=12;run.missileLevel=2;run.shield=0;run.retinaScan=false;special=null;run.sonicT=run.dkT=0;timeScale=1;s6Opening=null;stageTimer=34;if(c.stage===6){s6WingLaunch(2,false);s6Wing.beats=1;}player.invuln=2;window.manualElapsed=0;return keybindFor(1);}""",case),flush=True)
  for raw in sys.stdin:
   req=json.loads(raw)
   if req.get('close'):break
   keys=set(req.get('keys',[]))
   for k in held-keys:p.keyboard.up(k)
   for k in keys-held:p.keyboard.down(k)
   if req.get('doubleTap'):
    k=req['doubleTap'];p.keyboard.up(k);p.evaluate(sh.STEP,1)
    p.keyboard.down(k);p.evaluate(sh.STEP,1);p.keyboard.up(k);p.evaluate(sh.STEP,1)
    p.keyboard.down(k);p.evaluate(sh.STEP,1)
    if k not in keys:p.keyboard.up(k)
   held=keys;frames=round(min(10,max(0,req.get('seconds',1)))*60)
   for batch in range(0,frames,30):
    result=p.evaluate(sh.STEP,min(30,frames-batch));assert result is None,result
    p.wait_for_timeout(12)
   r=p.evaluate("""n=>{manualElapsed+=n/60;return {at:manualElapsed,state,lives:run.lives,dead:player.dead,player:{x:player.x,y:player.y,roll:player._rollCool,somer:player._somerCool},hp:B?.hp,max:B?.maxhp,ammo:run.bombs,encounter:B?._er26?{mode:B._er26.mode,t:B._er26.t,x:B.x,y:B.y,warm:B._er26.warm}:null,projectiles:eBullets.filter(q=>q.y>VH*.4).map(q=>({x:q.x,y:q.y,vx:q.vx,vy:q.vy})).slice(0,25),hammer:B?._hammer?{x:B.x,y:B.y,state:B._hammer.state,t:B._hammer.t,mode:B._hammer.mode,tx:B._hammer.tx,ty:B._hammer.ty,head:hammerHeadPoint(B),recovery:B._hammer.recovery,storm:B._hammer.stormWaves?.map(q=>({x:q.x,y:q.y,t:q.t,delay:q.delay,warm:q.warm,split:q.split}))}:null,ships:subBoss?._tempestDuo?.ships.map(p=>({x:p.x,y:p.y,hp:p.hp,phase:p._ai.phase,mode:p._ai.state,jet:p._jet.active?p._jet.state:null,jetTime:p._jet.t,angle:p._jet.angle,lock:p._jet.lock}))};}""",frames+(4 if req.get('doubleTap') else 0))
   name=f'{len(actions):02d}.png';(OUT/name).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]));r.update({'input':req,'image':name});actions.append(r)
   (OUT/'report.json').write_text(json.dumps({'case':case,'actions':actions,'errors':errors,'limits':'Paused between observations, selected mid-level equipment. Ordinary collision/lives. Not a real-time campaign win.'},indent=2),encoding='utf-8')
   print(json.dumps(r),flush=True)
  br.close()
finally:stop()
print(json.dumps({'errors':errors,'actions':len(actions)}),flush=True)
