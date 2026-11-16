from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source')
OUT=ROOT/'_shots/cockpit_talk_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];samples=[]
def check(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL '+name+' '+str(data),flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?cockpit-talk-qa=1114')
 p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=0;coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 pilots=p.evaluate('CP15_ART.pilots')
 for pk in pilots:
  p.evaluate("p=>{BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;BOFCinematicDirector.start(2,()=>{});CP15.history=[];}",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=__bofStepNow=performance.now();}')
  poses=set();shots=[]
  for i in range(100):
   checkerr=p.evaluate(shoot.STEP,1)
   if checkerr:errors.append(checkerr);break
   q=p.evaluate('({pose:CP15.last,shown:BOFCinematicDirector.current.shown,time:BOFCinematicDirector.current.t,who:BOFCinematicDirector.current.beats[0].who})')
   poses.add(q['pose']['frame'])
   if len(shots)<1 and q['pose']['frame'] in [1,3,4]:
    p.locator('#screen').screenshot(path=str(OUT/(pk+'-speaking.png')));shots.append(q)
  check(pk+' mouth follows native reveal',len(poses)>=4,sorted(poses))
  check(pk+' correct cockpit asset',q['pose']['key']=='cp15_'+pk,q['pose'])
  check(pk+' seated cockpit visible',q['pose']['image'][1]>=0,q['pose']['image'])
  p.evaluate('()=>{const s=BOFCinematicDirector.current;s.i=1;s.t=1;s.shown=15;CP15.history=[];}')
  p.evaluate(shoot.STEP,1)
  idle=p.evaluate('CP15.last')
  check(pk+' idle while remote tech speaks',idle['frame'] in [0,7],idle)
  samples.append({'pilot':pk,'poses':sorted(poses),'talk':shots,'listener':idle})
  print(pk+' service cockpit verified',flush=True)
  p.evaluate("p=>FURY14.preview('stage1',p)",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  p.evaluate('()=>{const s=BOFCinematicDirector.current;s.i=3;s.t=1.9;s.shown=12;CP15.history=[];}')
  p.evaluate(shoot.STEP,1)
  p.locator('#screen').screenshot(path=str(OUT/(pk+'-jungle.png')))
  q=p.evaluate('({last:CP15.last,comic:FIXC14.last})')
  check(pk+' Stage1 cockpit hook',q['last']['key']=='cp15_'+pk,q)
 # Existing comic radio framing, including the offscreen/zoomed top edge.
 p.evaluate("()=>D1110.preview('post-6','cole')")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 rows=p.evaluate('BOFCinematicDirector.current.beats.map((b,i)=>({i,who:b.who,places:b.fpLocations,kind:b.kind}))')
 idx=next(q['i'] for q in rows if q['kind']=='dialogue' and q['places'].get('cole','').startswith('cockpit-') and q['who']=='COLE')
 p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i;s.t=1.2;s.shown=9;CP15.history=[];}',idx)
 p.evaluate(shoot.STEP,1);p.locator('#screen').screenshot(path=str(OUT/'cole-native-radio.png'))
 q=p.evaluate('CP15.history')
 check('generic radio panel uses cockpit bank',any(x['pilot']=='cole' for x in q),q)
 check('generic radio panel preserves hair at visible top',all(x['image'][1]>=0 for x in q),q)
 q=p.evaluate("()=>{const out=[];for(const pk of CP15_ART.pilots)for(const room of ['cockpit-sky','cockpit-space','cockpit-tunnel'])for(const n of [48,64,84,96])out.push(FP5_ART.banks['mini-'+room+'-'+pk+'-'+n].key==='cp15_'+pk+'_'+n);return out;}")
 check('108 cockpit radio bindings',len(q)==108 and all(q))
 q=p.evaluate("()=>CP15_ART.pilots.map(pk=>FP5_ART.banks['mini-workshop-'+pk+'-64'].key.startsWith('cp15_'))")
 check('HQ portrait family retained',not any(q))
 q=p.evaluate("()=>{D1110.static=false;return CP15_ART.pilots.map(pk=>{const text='a e o u f m t';const b={who:pk.toUpperCase(),text};const s={shown:1,age:0};let out=[];for(const n of [1,3,5,7,9,11,13]){s.shown=n;out.push(cp15Pose(pk,b,s));}return {pk,out,done:cp15Pose(pk,b,{shown:text.length,age:0}),other:cp15Pose(pk,{...b,who:'SYSTEM'},s)};});}")
 for v in q:check(v['pk']+' phoneme and idle logic',v['out'][:6]==[1,2,3,4,5,0] and v['done']==0 and v['other']==0,v)
 check('no Chromium page/console/HTTP errors',not errors,errors)
 b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'samples':samples,'errors':errors,'scope':'Native dialogue checkpoints; not campaign runs.'},indent=2),encoding='utf-8')
print(str(sum(q['ok'] for q in checks))+'/'+str(len(checks))+' checks passed',flush=True)
assert all(q['ok'] for q in checks)

