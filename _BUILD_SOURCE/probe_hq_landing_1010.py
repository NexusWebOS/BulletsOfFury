"""Real Chromium homecoming art, physical roots, timing and continuation."""
from pathlib import Path
import sys,json,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/os.environ.get('BOF_HL10_OUT','_shots/hq_landing_1010');OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,30):
    e=p.evaluate(shoot.STEP,min(30,n-i))
    if e:errors.append(e);break
    p.wait_for_timeout(4)
  def start(pilot='cole',trueEnding=True):
   p.evaluate("q=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=q.pilot;story=null;fb2Talk=null;s6Opening=null;drawVictory._t=0;drawVictory._ready=false;drawVictory._wait=0;drawVictory._waitF=0;drawVictory._sfx={};drawVictory._hl10=null;drawVictory._trueEnding=q.trueEnding;setState(GS.VICTORY);victoryEndingWarm();hl10Warm();}",dict(pilot=pilot,trueEnding=trueEnding))
   p.wait_for_function('victoryEndingReady()&&hl10Warm()',polling=50)
   frames(2)
  def seek(t,name=None):
   p.evaluate("t=>{drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);}",t)
   if name:p.screenshot(path=str(OUT/(name+'.png')))
   return p.evaluate('HL10.last')
  start();check('Cold homecoming acquires all selected-pilot art before advancing',p.evaluate('drawVictory._ready&&drawVictory._t<.1&&hl10Warm()'))
  door=p.evaluate('''()=>{const size={w:cv.width,h:cv.height},out=[];
   try{cv.width=cv.height=384;ctx.setTransform(1,0,0,1,0,0);
    const capture=f=>{ctx.clearRect(0,0,384,384);hl10Cell('door',f,192,288,384);return ctx.getImageData(0,0,384,384).data;};
    const reference=capture(15),states=[];
    for(let f=0;f<16;f++){const pixels=capture(f);let fixedChanged=0,movingChanged=0;
     for(let y=0;y<384;y++)for(let x=0;x<384;x++){const i=(y*384+x)*4;
      const changed=pixels[i]!==reference[i]||pixels[i+1]!==reference[i+1]||pixels[i+2]!==reference[i+2]||pixels[i+3]!==reference[i+3];
      if(changed){if(x>=138&&x<246&&y>=124&&y<278)movingChanged++;else fixedChanged++;}}
     states.push({frame:f,fixedChanged,movingChanged});}return states;
   }finally{cv.width=size.w;cv.height=size.h;ctx.setTransform(SS,0,0,SS,0,0);}}''')
  check('Native door pillars, lintel and threshold are pixel-identical across all sixteen frames',all(q['fixedChanged']==0 for q in door),door)
  check('Door panels reveal the fixed corridor continuously in every frame',all(door[i]['movingChanged']>door[i+1]['movingChanged'] for i in range(15)) and door[-1]['movingChanged']==0,door)
  opening=[];closing=[]
  for f in range(16):
   a=seek(20+(f+.1)*1.1/16);opening.append(a['doorFrame'])
   b=seek(24.55+(15-f+.1)*1.1/16);closing.append(b['doorFrame'])
  check('The homecoming opening and closing use the same registered door frames',opening==list(range(16)) and closing==list(range(16)),dict(opening=opening,closing=closing))
  camera=p.evaluate('''()=>{const cell=hl10Cell,caption=victoryCaption,records=[];
   try{let row;
    hl10Cell=function(bank){if(bank==='background'){const m=ctx.getTransform();row.scene={x:m.a/SS,y:m.d/SS,b:m.b,c:m.c};}return cell.apply(this,arguments);};
    victoryCaption=function(){const m=ctx.getTransform();row.caption={x:m.a/SS,y:m.d/SS,e:m.e,f:m.f};return caption.apply(this,arguments);};
    for(const t of [9.4,11.08,13.6,16.6,18.38,20.60,22.52,24,25.65]){
     row={t};drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);
     const s=HL10.last,R=s.rect,c=s.camera;row.camera=c;
     if(s.actor){const a=s.actor;row.actor={x:((a.foot.x-R.x)/R.w-c.x)*c.zoom+.5,
      y:((a.foot.y-a.height*.5-R.y)/R.h-c.y)*c.zoom+.5};}
     const patches=[];
     for(const [x,y]of [[.03,.03],[.97,.03],[.03,.94],[.97,.94]]){
      const pixels=ctx.getImageData(Math.round((R.x+x*R.w)*SS),Math.round((R.y+y*R.h)*SS),6,6).data;
      let lit=0;for(let i=0;i<pixels.length;i+=4)if(pixels[i]+pixels[i+1]+pixels[i+2]>12)lit++;patches.push(lit);}
     row.edgePixels=patches;records.push(row);
    }return records;
   }finally{hl10Cell=cell;victoryCaption=caption;}}''')
  check('Native camera pushes from the wide landing to the doorway continuously',all(camera[i]['camera']['zoom']<=camera[i+1]['camera']['zoom'] for i in range(len(camera)-1)) and camera[0]['camera']['zoom']==1 and camera[-1]['camera']['zoom']==3,camera)
  check('Every scene layer uses the same proportional camera transform',all(abs(q['scene']['x']-q['camera']['zoom'])<1e-6 and abs(q['scene']['y']-q['camera']['zoom'])<1e-6 and q['scene']['b']==0 and q['scene']['c']==0 for q in camera),camera)
  check('Captions stay fixed outside the camera transform',all(q['caption']==dict(x=1,y=1,e=0,f=0) for q in camera),camera)
  check('The moving pilot remains in the camera frame throughout the walk',all(.08<q['actor']['x']<.92 and .08<q['actor']['y']<.92 for q in camera if 'actor' in q),camera)
  check('Camera edges contain authored scene pixels instead of uncovered black gaps',all(min(q['edgePixels'])>24 for q in camera),camera)
  motion=p.evaluate('''()=>{const points=[];for(let t=9.4;t<=26.4;t+=1/60)points.push(hl10Camera(t));
   let delta=0;for(let i=1;i<points.length;i++)delta=Math.max(delta,...['x','y','zoom'].map(k=>Math.abs(points[i][k]-points[i-1][k])));
   return {maxStep:delta,bounded:points.every(c=>c.x-.5/c.zoom>=-1e-8&&c.x+.5/c.zoom<=1+1e-8&&c.y-.5/c.zoom>=-1e-8&&c.y+.5/c.zoom<=1+1e-8),
    seams:HL10.cameraTrack.slice(1,-1).map(k=>{const a=hl10Camera(k[0]-.0001),b=hl10Camera(k[0]+.0001);return Math.max(...['x','y','zoom'].map(p=>Math.abs(a[p]-b[p])));})};}''')
  check('Camera interpolation has no jumps at touchdown, disembark or walk cues',motion['maxStep']<.01 and max(motion['seams'])<.0002,motion)
  check('The camera never samples beyond the authored background',motion['bounded'],motion)
  for t,name in [(1.3,'escape'),(4.5,'earth'),(7.8,'coast'),(9.65,'gear-unfold'),(10.4,'descent'),(11.16,'touchdown'),(12.7,'shutdown'),(13.5,'hatch-open'),(14.1,'climb'),(16.0,'step-off'),(18.6,'walk-around'),(21.3,'door-open'),(23.0,'entering'),(24.2,'inside'),(25.8,'parked')]:seek(t,name)
  a=seek(13.55);b=seek(16.55);c=seek(19.7);d=seek(25.9)
  check('Grounded ship remains exactly stationary through exit, walk and entry',all(abs(q['ship']['x']-a['ship']['x'])<.01 and abs(q['ship']['y']-a['ship']['y'])<.01 and abs(q['ship']['scale']-a['ship']['scale'])<.0001 for q in [b,c,d]),[q['ship'] for q in [a,b,c,d]])
  check('Landing struts touch down before the pilot exits',a['grounded'] and not a['actor'] and b['actorClip']=='exit')
  q=seek(21.45);check('HQ door is fully open before the pilot reaches its threshold',q['doorFrame']==15 and q['actor'] and not q['actor']['inside'],q)
  q=seek(24.2);check('Pilot enters the building instead of fading on the apron',q['entered'] and not q['actor'] and q['phase']=='inside',q)
  visible=[]
  for t in [18.6,20.4,21.3,22.2,23.0]:
   seek(t)
   q=p.evaluate("()=>{const a=ctx.getImageData(0,0,cv.width,cv.height).data,draw=hl10Actor;try{hl10Actor=()=>null;drawVictory(0);const b=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<a.length;i+=4)if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>24)changed++;return changed;}finally{hl10Actor=draw;drawVictory(0);}}")
   visible.append(dict(time=t,changed_pixels=q))
  check('Actual pilot pixels remain visible around the nose and into the open doorway',all(q['changed_pixels']>80 for q in visible),visible)
  q=p.evaluate("()=>{const warm=hl10Warm,last=HL10.last;try{hl10Warm=()=>false;victoryRestoration(7.8,cutsceneViewWidth(),VH,'cole');return HL10.last!==last&&HL10.last.phase==='approach';}finally{hl10Warm=warm;}}")
  check('Bounded loading fallback never restores the retired parked planes',q)
  q=p.evaluate("()=>Object.fromEntries(HL10.pilots.map(k=>[k,{walk:hl10BodyGeometry(k),ship:hc10ShipGeometry(k,'rear')}]))")
  check('Every pilot and original static airframe includes its entire visible silhouette',all(v['walk']['height']>140 and v['ship']['w']>0 and v['ship']['h']>0 for v in q.values()),q)
  for pilot in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
   start(pilot);seek(13.3,'pilot-'+pilot+'-landed');seek(18.3,'pilot-'+pilot+'-walking');seek(14.8,'pilot-'+pilot+'-exiting')
  q=p.evaluate('({...HL10.draws,...HC10.draws})');check('All nine selected pilots render their original aircraft, exit and walk pixels',all(q.get('ship_'+k+'_so2',0)>0 and all(any(v>0 for key,v in q.items() if key.startswith('hl10_'+k+'_'+b+'_')) for b in ['exit','walk']) for k in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']),q)
  start('falva');seek(4.0);check('Earth return uses Falva\'s original static rear view on the straight descent',p.evaluate("HC10.last.bank==='ship_falva_so2'&&HC10.last.rotation===0&&HC10.draws.ship_falva_so2>0"))
  start();p.evaluate('()=>{drawVictory._t=9.40;drawVictory._hl10=null;HL10.events=[];}');frames(450)
  q=p.evaluate("HL10.events.filter(q=>q.event==='sound').map(q=>q.cue)");check('Landing sounds fire once at their physical events',q==['gear','touchdown','hatch'],q)
  before=p.evaluate('HL10.events.length');p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);drawVictory(0);drawVictory(0);}')
  check('Extra redraws cannot replay landing sounds',p.evaluate('HL10.events.length')==before)
  start()
  fades=[]
  for t,name in [(25.65,'door-closed-closeup'),(26.05,'homecoming-fade'),(26.3999,'homecoming-black'),(26.4,'next-scene-black'),(26.725,'next-scene-fade'),(27.1,'next-scene')]:
   seek(t,name)
   q=p.evaluate('''()=>{const pixels=ctx.getImageData(0,0,cv.width,cv.height).data;let sum=0,max=0;
    for(let i=0;i<pixels.length;i+=4){sum+=pixels[i]+pixels[i+1]+pixels[i+2];max=Math.max(max,pixels[i],pixels[i+1],pixels[i+2]);}
    const m=ctx.getTransform();return {transition:HL10.transition,mean:sum/(pixels.length/4*3),max,
     transform:{x:m.a/SS,y:m.d/SS,b:m.b,c:m.c,e:m.e,f:m.f},alpha:ctx.globalAlpha};}''')
   fades.append(dict(time=t,**q))
  check('Homecoming fades only after the pilot enters and the door closes',fades[0]['transition']['fade']==0 and p.evaluate("hl10Sample(25.65).entered&&hl10Sample(25.65).doorFrame===0"),fades)
  check('The cut between HQ and the next scene is completely black on both sides',fades[2]['max']==0 and fades[3]['max']==0,fades)
  check('The survivor scene fades in and reaches full visibility',fades[3]['transition']['phase']=='survivor' and fades[3]['mean']==0 and 0<fades[4]['mean']<fades[5]['mean'] and fades[5]['transition']['fade']==0,fades)
  check('Camera and fade restore drawing state before subsequent scenes',all(q['transform']==dict(x=1,y=1,b=0,c=0,e=0,f=0) and q['alpha']==1 for q in fades),fades)
  start();p.evaluate('drawVictory._t=26.3');frames(15)
  q=p.evaluate('({t:drawVictory._t,state,dish:VICTORY_DISH_AT,survivor:!!drawVictory._sfx})');check('True ending continues into the original survivor sequence after entering HQ',q['state']==p.evaluate('GS.VICTORY') and 26.4<q['t']<27,q)
  p.screenshot(path=str(OUT/'survivor-continuation.png'))
  start(trueEnding=False);p.evaluate('drawVictory._t=26.3');frames(15)
  check('Ordinary ending reaches its final card only after the full homecoming',p.evaluate('drawVictory._t>=VICTORY_CARD_AT'))
  p.screenshot(path=str(OUT/'ordinary-final-card.png'))
  p.evaluate("()=>{run.mode='arcade';drawVictory._t=0;drawVictory._ready=false;setState(GS.VICTORY);}");frames(3)
  check('Arcade still opens directly on its score/end card',p.evaluate('drawVictory._t<.2&&!drawVictory._ready'))
  p.set_viewport_size(dict(width=480,height=900));start('yuri');q=seek(21.1,'narrow-door-walk')
  r=p.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.width/cutsceneViewWidth(),y:r.height/VH};}')
  check('Narrow cinematic keeps aircraft, characters and doorway evenly proportioned',abs(r['x']/r['y']-1)<.005,r)
  check('Narrow camera remains clipped to its cinematic viewport',q['rect']['x']>=0 and q['rect']['x']+q['rect']['w']<=p.evaluate('cutsceneViewWidth()')+.01,q['rect'])
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
