from pathlib import Path
import sys,json,http.server,hashlib,math
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_gated_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
D=R/'assets/game/levels/stage_08/effects/gated_possession_1031';A=json.loads((D/'manifest.json').read_text());I=json.loads((D/'inputs.json').read_text())
ck('All six banks use144 actual gated PixelLab frames',len(A)==6 and sum(a['frames']for a in A.values())==144)
for n,a in A.items():
 im=Image.open(R/a['path']);ck(n+' fixed even cells, centre pivot and editable source',a['cw']%2==a['ch']%2==0 and a['pivot']==[a['cw']//2,a['ch']//2]and im.size==(a['cw']*8,a['ch']*math.ceil(a['frames']/8))and (D/(n+'.aseprite')).exists())
ck('All original purple/red gated input hashes match',all(hashlib.sha256((R/f['path']).read_bytes()).hexdigest()==f['sha256']for b in I['banks'].values()for f in b['frames']))
ck('Sources are the sewer mechanical gate family, not RD71 energy-only rims',all('/pixellab_void_1017/'in f['path']and ('void_rift_'in f['path']or'red_rift_'in f['path'])for b in I['banks'].values()for f in b['frames']))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD94_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  p.evaluate("()=>{window.B=boss;window.bad94=0;window.gate94={};const f=rd71Blit;rd71Blit=function(n){if(n==='gate_red'||n==='gate_purple')bad94++;return f.apply(this,arguments)};const g=rd94GateBlit;rd94GateBlit=function(q,x,y){if(q)gate94[q.color+'_'+q.phase]=(gate94[q.color+'_'+q.phase]||0)+1;return g.apply(this,arguments)};}")
  initial=p.evaluate('({hp:B.hp,parts:B.parts.map(p=>p.hp),ship:{x:player.x,y:player.y}})');trace=[];seen=set();marks=[6,8,10.3,11.4,12.4,13.4,13.94,14.45,15.1,18.8,19,20.2]
  for i in range(450):
   err=p.evaluate(STEP,3)
   if err:raise RuntimeError(err)
   p.wait_for_timeout(1);q=p.evaluate('({time:rd71Time(B),mode:B._r30.mode,t:B._r30.t,last:RD71.last,hp:B.hp,ship:{x:player.x,y:player.y}})');trace.append(q)
   for k,m in enumerate(marks):
    if k not in seen and q['time']>=m:
     seen.add(k);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/('scene-'+str(m)+'.png')))
   if q['mode']=='fight':break
  (W/'trace.json').write_text(json.dumps(trace,indent=2));ev=p.evaluate('RD71.events');(W/'events.json').write_text(json.dumps(ev,indent=2))
  ck('Native entrance reaches full-health first-host fight',q['mode']=='fight'and q['hp']==initial['hp'],q)
  ck('Player stays anchored during possession',all(r['ship']==initial['ship']for r in trace if r['mode']!='fight'))
  ck('Energy-only red/purple portal frames are never drawn',p.evaluate('bad94===0'))
  ck('Both actual metal gates render their authored form, loop and close banks',p.evaluate("['purple','red'].every(c=>['form','loop','close'].every(n=>gate94[c+'_'+n]>0))"),p.evaluate('gate94'))
  ck('Purple gate opens first and closes after neutral drone emerges',any(r['last']['primaryPhase']=='loop'and r['mode']=='v18arrival'for r in trace)and all(r['last']['primary']is None for r in trace if r['mode']=='v18conversion'and r['t']>.1))
  ck('Red gate stays fully open during aim, data bomb and return',all(r['last']['secondaryPhase']=='loop'for r in trace if 10<=r['time']<14.05))
  ck('Infector leaves the red aperture and visibly hovers in front',any(r['last']['ufoAt']['y']-r['last']['redGateAt']['y']>60 for r in trace if 10.6<r['time']<12.9))
  ret=[r for r in trace if 12.95<r['time']<14]
  dist=lambda r:math.hypot(r['last']['ufoAt']['x']-r['last']['redGateAt']['x'],r['last']['ufoAt']['y']-r['last']['redGateAt']['y'])
  ck('Return flight approaches the same red aperture and ends inside',len(ret)>10 and dist(ret[-1])<1 and all(dist(a)>dist(b)for a,b in zip(ret,ret[1:])),[dist(ret[0]),dist(ret[-1])])
  ck('Red gate never closes over a still-visible infector',all(not r['last']['ufo']for r in trace if r['last']['secondaryPhase']=='close'))
  ck('Red gate closes after infector is gone and fully disappears',any(r['last']['secondaryPhase']=='close'for r in trace)and all(r['last']['secondary']is None for r in trace if 14.9<r['time']<18))
  ck('Data bomb fires and impacts before return/closure',next(e['time']for e in ev if e['event']=='data-bomb-release')<next(e['time']for e in ev if e['event']=='data-bomb-impact')<next(e['time']for e in ev if e['event']=='infector-returns-through-red-gate')<next(e['time']for e in ev if e['event']=='red-gate-closes-after-return'))
  ck('Code possession only starts after the native impact',all(not r['last']['possessed']for r in trace if r['mode']=='v18conversion'and r['t']<3.05)and any(r['last']['possessed']for r in trace))
  ck('Host remains concealed under full white at reveal',all(not r['last']['host']or r['last']['white']==16 for r in trace if r['mode']=='v18conversion'and r['t']<9.4))
  ck('Robotic screams still route through the native mixer',len([e for e in ev if e.get('cue','').startswith('rd71Scream')])==4)
  ck('Health split and arm protection remain intact',p.evaluate('B.parts.reduce((n,p)=>n+p.maxhp,0)===B.maxhp&&rb23Arms(B).length===2'))
  p.evaluate('()=>{const c=B.parts.find(p=>p.id==="core");window.before94=B.hp;B._lastPart=c;modularHit(50)}');ck('Core cannot take damage before the whole arms',p.evaluate('B.hp===before94'))
  p.evaluate('()=>{const a=B.parts.find(p=>p.id==="left");B._lastPart=a;modularHit(a.hp)}');ck('Whole shoulder/arm destruction owner is unchanged',p.evaluate('B.parts.find(p=>p.id==="left").destroyed&&RD71.breaks.some(f=>f.side==="left"&&f.points.length>=4)'))
  ck('Stage7 rescue still has its original green gated banks',p.evaluate('SR93.speed===400&&SC86_ART.green_loop.frames===32'))
  ck('No game or rendering errors',not errors,errors);br.close()
finally:stop()
ck('Core engine source remains unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
print('RESULT',len(checks),'checks passed')
