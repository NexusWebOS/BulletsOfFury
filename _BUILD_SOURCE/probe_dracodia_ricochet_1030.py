from pathlib import Path
import sys,json,http.server,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_ricochet_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  ck('Native entrance reaches the unchanged5945HP first host',advance(p,"boss._r30.mode==='fight'",100,16)and p.evaluate('boss.hp===5945'))
  p.evaluate('()=>{window.B=boss;window.core=B.parts.find(p=>p.id==="core");window.hp=core.hp;B._lastPart=core;modularHit(40);}')
  ck('Arms still protect the entire core budget',p.evaluate('core.hp===hp'))
  p.evaluate('()=>{for(const id of ["left","right"]){const a=B.parts.find(p=>p.id===id);B._lastPart=a;modularHit(a.hp);}player.invuln=1e9;}')
  ck('Real destruction of both arms enters the new rolling state',advance(p,'!!B._r30.v18.attack?._rd73',100,4)and p.evaluate('!rb23Arms(B).length&&B.hp===hp'))
  p.evaluate('''()=>{window.trace=[];window.targets=new Map();window.targetMoves=[];window.rollFrames=new Set();const fn=er23DrawBank;er23DrawBank=function(n,f){if(n==='roll')rollFrames.add(f);return fn.apply(this,arguments)};
  window.__qaTick=function(){const P=rd73Attack(B),M=P?._rd73;if(!M)return;const bombs=enemies.filter(e=>!e.dead&&e._d20?.owner===B&&e._d20.kind==='bomb'&&e._d20.phase!=='erase');
   for(const e of bombs){const A=e._d20,last=targets.get(A.id);if(last&&(last.x!==A.target.x||last.y!==A.target.y))targetMoves.push(A.id);targets.set(A.id,{...A.target});}
   trace.push({clock:efxClock,x:M.x,y:M.y,vx:M.vx,vy:M.vy,phase:M.phase,cycle:M.cycle,bombs:bombs.length,blasts:D20.blasts.filter(q=>q.owner===B).length,hp:B.hp});};}''')
  for i in range(27):
   err=p.evaluate(STEP,60)
   if err:raise RuntimeError(err)
   if i in [0,3,7,13,23]:
    p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/('ricochet-'+str(i)+'.png')))
  q=p.evaluate('({trace,events:RD73.events,bounds:rd73Bounds(),frames:[...rollFrames],moved:targetMoves,hp:B.hp})');t=q['trace'];e=q['events'];moving=[v for v in t if v['phase']!='fold'];drops=[v for v in e if v['event']=='rapid-code-drop'];rebounds=[v for v in e if v['event']=='wall-rebound'];bounds=q['bounds']
  ck('Core rebounds from all four screen edges',set(v['edge']for v in rebounds)=={'left','right','top','bottom'},len(rebounds))
  ck('Every active frame stays fully inside the arena',all(bounds['left']-.01<=v['x']<=bounds['right']+.01 and bounds['top']-.01<=v['y']<=bounds['bottom']+.01 for v in moving))
  vw,top,vh=p.evaluate('[viewW(),viewTopY(),VH]');ck('All24 measured body silhouettes stay clear of HUD and screen edges',all(v['x']-118>=0 and v['x']+122<=vw and v['y']-105>=top+44 and v['y']+104<=vh for v in moving))
  ck('Wall reflections have continuous motion without waypoint teleports',max(((b['x']-a['x'])**2+(b['y']-a['y'])**2)**.5 for a,b in zip(moving,moving[1:]))<=330/60+.1)
  ck('Furious rapidly drops more than40 bombs over this27s run',len(drops)>40,len(drops))
  ck('The original24 authored3D roll frames remain active',len(q['frames'])==24,len(q['frames']))
  ck('Bomb count never exceeds the six-live-bomb pressure cap',max(v['bombs']for v in t)<=6,max(v['bombs']for v in t))
  ck('Every bomb retains its native1.8s flight/arming warning',all(abs(v['warning']-1.8)<.001 for v in drops))
  ck('Every committed landing point stays fixed as the core moves',not q['moved'],q['moved'])
  ck('Finite barrage recovery keeps the ball moving and resumes bombing',any(v['phase']=='coast'for v in moving)and max(v['cycle']for v in moving)>=2 and all(v['vx']and v['vy']for v in moving))
  ck('Motion and bomb spawning do not rewrite the original core HP',q['hp']==p.evaluate('hp'))
  hit=p.evaluate('()=>{B._lastPart=core;const before=B.hp;modularHit(25);return{before,after:B.hp};}')
  ck('The exposed rolling core still accepts ordinary native damage',hit['before']-hit['after']==25,hit)
  p.evaluate('()=>{B._lastPart=core;modularHit(core.hp);}')
  ck('Native core defeat still enters its original rebirth sequence',p.evaluate('B.hp===0&&B._r30.mode==="dr5er23rebirth"'))
  p.evaluate(STEP,90)
  ck('Defeat clears bomb danger and retires every owned bomb',p.evaluate('!D20.blasts.some(q=>q.owner===B)&&!enemies.some(e=>!e.dead&&e._d20?.owner===B&&e._d20.phase!=="erase")'))
  ck('No native drawing, console or browser errors',not errors,errors)
  (W/'trace.json').write_text(json.dumps(q));br.close()
finally:stop()
print(len(checks),'ricochet/rapid-bomb checks passed')
