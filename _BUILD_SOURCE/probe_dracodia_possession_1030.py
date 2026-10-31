from pathlib import Path
import sys,json,http.server,numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_possession_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_08/boss/possession_1030/manifest.json').read_text())
def cell(n,f):
 a=M[n];im=Image.open(R/a['path']);return np.array(im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch'])))
ck('All31 banks have even fixed cells, measured pivots and valid atlas bounds',len(M)==31 and all(a['cw']%2==a['ch']%2==0 and max(Image.open(R/a['path']).size)<=4096 and len(a['pivot'])==2 for a in M.values()))
ck('Both toxic-rim gated portals close completely through authored fade frames',all(np.max(cell('gate_'+n,23)[:,:,3])==0 for n in ['purple','red']))
ck('Infector uses16 distinct hovering frames from the generated reference-based design',len({cell('ufo',i).tobytes()for i in range(16)})==16)
ck('Neutral drone emergence, arm lift and red-eye possession use authored frames',M['drone_emerge']['frames']==24 and M['drone_charge']['frames']==64 and not np.array_equal(cell('drone_charge',0),cell('drone_charge',63)))
ck('Code spiral materializes through eight stored-alpha frames with rear/front layers',M['helix_in_back']['frames']==M['helix_in_front']['frames']==8 and cell('helix_in_front',0)[:,:,3].sum()<cell('helix_in_front',7)[:,:,3].sum())
v=cell('drone_charge',63);red=(v[:,:,0]>200)&(v[:,:,1]<70)&(v[:,:,2]<90)&(v[:,:,3]>100);edge=np.concatenate([v[0,:,3],v[-1,:,3],v[:,0,3],v[:,-1,3]])
ck('Final possession has a bright red eye, overhead claws and an unclipped fixed canvas',int(red[105:150,140:180].sum())>30 and int((v[50:120,:,3]>0).sum())>1000 and int(edge.max())==0)
for name in ['dracodia_wind','dracodia_strike','dracodia_recover']:
 n=M['host_'+name+'_core']['frames'];count=0
 for f in range(n):
  a=[cell('host_'+name+'_'+p,f)for p in ['left','right','core']]
  ckname=''
  if f==0:count=int(np.sum(a[0][60:140,60:135,3]>0))
  assert np.max(sum((x[:,:,3]>0).astype(int)for x in a))==1
  assert all(np.array_equal(cell('host_'+name+'_'+p,f)[:,:,3],cell('host_'+name+'_'+p+'_hit',f)[:,:,3])for p in ['left','right','core'])
 ck(name+' keeps complete disjoint shoulders/arms, matching hit alpha and full core',count>100,count)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD71_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  p.evaluate("()=>{window.B=boss;window.badPortal=0;const fn=pl11World;pl11World=function(n){if(rd29Own(B)&&n==='amethyst_gate')badPortal++;return fn.apply(this,arguments)};}")
  initial=p.evaluate('({hp:B.hp,pools:j3State(B).hp,ship:{x:player.x,y:player.y}})');marks=[6.0,7.9,8.6,9.8,10.9,12.35,12.9,15,17.7,18.85,19.1,20.3];trace=[];seen=set()
  for i in range(1500):
   err=p.evaluate(STEP,1)
   if err:raise RuntimeError(err)
   q=p.evaluate('({time:rd71Time(B),mode:B._r30.mode,t:B._r30.t,last:RD71.last,hp:B.hp,ship:{x:player.x,y:player.y}})');trace.append(q)
   for k,m in enumerate(marks):
    if k not in seen and q['time']>=m:
     seen.add(k);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/('scene-'+str(m)+'.png')))
   if q['mode']=='fight':break
  ck('Native intro reaches normal first-host combat without HP writes',q['mode']=='fight'and q['hp']==initial['hp'],q)
  ck('Pilot stays anchored during the entire possession scene',all(abs(r['ship']['x']-initial['ship']['x'])<.01 and abs(r['ship']['y']-initial['ship']['y'])<.01 for r in trace if r['mode']!='fight'))
  ck('Rejected amethyst gate is never rendered',p.evaluate('badPortal===0'))
  ck('Primary portal closes before possession while drone visibly readies its attack',any(r['mode']=='v18arrival'and r['t']>1.3 and r['last']['primary']is not None for r in trace)and all(r['last']['primary']is None for r in trace if r['mode']=='v18conversion'and r['t']>.1))
  ck('Second red portal opens behind/above the visible UFO',any(r['last']['secondary']is not None and r['last']['ufo']for r in trace))
  ck('Spiraling code starts only after data bomb impact',all(not r['last']['possessed']for r in trace if r['mode']=='v18conversion'and r['t']<3.05)and any(r['last']['possessed']for r in trace))
  ev=p.evaluate('RD71.events');ck('UFO aim, actual data-bomb release and impact occur in order',next(e['time']for e in ev if e['event']=='data-bomb-charge')<next(e['time']for e in ev if e['event']=='data-bomb-release')<next(e['time']for e in ev if e['event']=='data-bomb-impact'))
  ck('Four robotic screams route through the shared mixer at loud gain',len([e for e in ev if e.get('cue','').startswith('rd71Scream')and e['gain']>=.98])==4)
  ck('Native host first appears beneath complete white coverage',all(not r['last']['host']or r['last']['white']==16 for r in trace if r['mode']=='v18conversion'and r['t']<9.4))
  ck('All parts retain the native33.3/33.3/33.4 health split',p.evaluate('B.parts.reduce((n,p)=>n+p.maxhp,0)===B.maxhp&&rb23Arms(B).length===2'))
  # Native target/collision and actual part breakup, not phase/timer shortcuts.
  q=p.evaluate('''()=>{const p=B.parts.find(p=>p.id==='left'),a=rb23PartPoint(B,p),q=r30At(B,a.x,a.y);return{target:a,part:q?.id};}''');ck('Retina arm anchor lands on the new opaque full-arm mask',q['part']=='left',q)
  p.evaluate('()=>{const p=B.parts.find(p=>p.id==="core");window.hp=B.hp;B._lastPart=p;modularHit(50)}');ck('Core remains protected while either whole arm is alive',p.evaluate('B.hp===hp'))
  p.evaluate('()=>{const p=B.parts.find(p=>p.id==="left");B._lastPart=p;modularHit(p.hp)}');ck('Native left arm damage destroys its complete shoulder/arm once',p.evaluate('B.parts.find(p=>p.id==="left").destroyed&&RD71.breaks.some(f=>f.side==="left"&&f.points.length>=4)&&RD71.events.filter(e=>e.event==="whole-shoulder-arm-break"&&e.part==="left").length===1'))
  p.evaluate(STEP,9);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'left-shoulder-exploding.png'))
  p.evaluate(STEP,45);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'left-shoulder-destroyed.png'))
  ck('No rectangular detached limb debris is emitted by the retired breakup',p.evaluate('!S78.debris.some(d=>d.owner===B)'))
  p.evaluate('()=>{const p=B.parts.find(p=>p.id==="right");B._lastPart=p;modularHit(p.hp)}');p.evaluate(STEP,9);p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/'both-shoulders-exploding.png'))
  ck('Both complete arms gate the native exposed-core phase',p.evaluate('rb23Arms(B).length===0&&B.hp===B.parts.find(p=>p.id==="core").hp'))
  ck('Break effects remain bounded and expire',advance(p,'RD71.breaks.length===0',100,1))
  ck('No native game, drawing or console errors',not errors,errors)
  (W/'trace.json').write_text(json.dumps(trace));(W/'events.json').write_text(json.dumps(p.evaluate('RD71.events'),indent=2));br.close()
finally:stop()
print(len(checks),'possession/whole-shoulder checks passed')
