from pathlib import Path
import sys,json,math
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
results=[];errors=[];port,stop=serve(str(R))
def reachable(q):
 x=np.arange(q['left']+18,q['right']-17,3);y=np.arange(q['top']+18,495,3);X,Y=np.meshgrid(x,y);a=np.zeros(X.shape,bool)
 a[np.argmin(abs(y-q['player']['y'])),np.argmin(abs(x-q['player']['x']))]=True
 # Slowest unupgraded pilot; axis-normalized movement; no roll/somersault.
 speed=2.6*.92*60;step=speed*.05;offsets=[(j,i)for j in range(-3,4)for i in range(-3,4)if math.hypot(i*3,j*3)<=step]
 counts=[]
 for k,frame in enumerate(q['frames']):
  expanded=np.zeros_like(a)
  for j,i in offsets:
   sy=slice(max(0,-j),min(a.shape[0],a.shape[0]-j));sx=slice(max(0,-i),min(a.shape[1],a.shape[1]-i))
   dy=slice(max(0,j),min(a.shape[0],a.shape[0]+j));dx=slice(max(0,i),min(a.shape[1],a.shape[1]+i));expanded[dy,dx]|=a[sy,sx]
  bad=np.zeros_like(a)
  for L in frame:
   dx=L['ex']-L['x'];dy=L['ey']-L['y'];den=dx*dx+dy*dy
   u=np.clip(((X-L['x'])*dx+(Y-L['y'])*dy)/max(.001,den),0,1)
   bad|=(X-L['x']-u*dx)**2+(Y-L['y']-u*dy)**2<10**2
  a=expanded&~bad;counts.append(int(a.sum()))
  if not a.any():return {'survives':False,'lostAt':round((k+1)*.05,2),'counts':counts,'speed':speed}
 return {'survives':True,'minimumAfterWarmup':min(counts[30:]),'endReachable':counts[-1],'speed':speed}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,9,errors)
  for version,rank,mode in [('old','furious','spiral'),('old','furious','sweep'),('new','hard','spiral'),('new','furious','spiral'),('new','furious','sweep')]:
   q=p.evaluate('''([version,rank,mode])=>{run.stage=9;diffKey=rank;DIFF=difficultyForRun('campaign',rank);run.ngplus=false;coopOn=false;spawnSubBoss('voidhorizon');const b=subBoss,H=eh57State(b);H.angle=0;b.enter=false;H.protected=false;H.mode='recover';eh57Move(b,camLeftX()+240,180);player.x=camLeftX()+240;player.y=VH-65;eh57Set(b,mode);if(version==='old'){H.warm=1.3;H.active=mode==='spiral'?4.7:3.8;H.on=H.period=999;H.rest=99;}const frames=[],duration=H.warm+H.active;for(let t=0;t<duration;t+=.05){let lines=[];for(let i=0;i<3;i++){s9VoidHorizonTick(b,1/60);lines.push(...H.beams.map(l=>({...l})));}frames.push(lines);}return{left:camLeftX(),right:camRightX(),top:viewTopY(),player:{x:player.x,y:player.y},frames};}''',[version,rank,mode])
   r={'version':version,'rank':rank,'mode':mode,**reachable(q)};results.append(r);print(json.dumps({k:v for k,v in r.items()if k!='counts'}),flush=True)
  br.close()
finally:stop()
(W/'dodge-analysis.json').write_text(json.dumps({'method':'Conservative reachable-cell test against three native beam samples per50ms;3px grid,10px clearance,143.52px/s, start south-centre, no dodge abilities. Diagnostic only; excludes regular bullets, input latency and future adaptive re-aim.','results':results,'errors':errors},indent=2))
