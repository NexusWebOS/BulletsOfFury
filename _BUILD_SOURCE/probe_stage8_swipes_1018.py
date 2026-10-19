"""Actual Stage 8 shoulder arcs, native pixels, warnings and swept contact."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/('_shots/dracodia_archive_1018/swipes' if '--archive' in sys.argv else '_shots/stage8_swipes_1018');O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V19!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.swipeHits=[];playerHit=function(reason){swipeHits.push({reason,t:B._r30.v18.swipe?.q?.t,stack:reason?null:new Error().stack.split('\\n').slice(1,5)});};
   window.swipePixel=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);v19Body(B);const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return a;};
   window.swipeDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.swipeTrace=[];window.swipeObserve=()=>{const W=B._r30.v18.swipe,Q=W?.q;let data={x:B.x,y:B.y};if(Q){const v=v18Rig(B).find(v=>v.p.id===Q.id);if(v)data={...data,id:Q.id,serial:W.index,t:Q.t,tell:Q.tell,swing:Q.swing,rot:v.rot,root:[v.ax,v.ay],joint:[B.x+Q.off.x,B.y+Q.off.y],tip:v19WorldPoint(v,Q.tip),target:{...Q.target},source:[v.a.w,v.a.h],scale:v.k,damaged:v.p.flash>0};}swipeTrace.push(data);};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);swipeObserve();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name,onion=False):
   p.evaluate('''onion=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);if(onion){const Q=B._r30.v18.swipe?.q,v=v18Rig(B).find(v=>v.p.id===Q?.id);if(v){ctx.save();ctx.translate(-camX,0);for(const u of [0,.25,.5,.75,1]){ctx.save();ctx.globalAlpha=.24;v19Paint({...v,ax:Q.root.x,ay:Q.root.y,rot:lerp(Q.start,Q.end,u)},B);ctx.restore();}ctx.restore();}}SC12.refresh();__bofFit();}''',onion);p.screenshot(path=str(O/(name+'.png')))
  def setup(phase,form,diff='normal'):
   p.evaluate(SETUP,dict(stage=8,diff=diff,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}')
   p.evaluate('''([phase,form])=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];v18Budget(B);v18Enter(B,phase,form);B._r30.v18.arenaPhase=phase;v18Fight(B);
    for(const i of V18.forms)if(i!==form)j3State(B).hp[i]=0;bossWarned=true;player.x=worldWidth()/2;player.y=VH-70;player.invuln=0;player.dead=player.out=false;run.shield=0;run.spaceMode=false;
    for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;V19.events=[];V19.draws={};swipeTrace=[];swipeHits=[];SC12.refresh();__bofFit();}''',[phase,form])
  for diff in (['normal'] if '--smoke' in sys.argv else ['normal','hard','furious']):
   for phase,form,name in [(0,0,'infused'),(1,0,'ghost'),(2,0,'colossus'),(2,2,'volcano')]:
    setup(phase,form,diff)
    p.evaluate('''()=>{if(v19Native(B)){const F=gd4Create(B,2).p._fz;F.trans=0;}v19BeginSwipe(B,'review-swipes','left');}''')
    frames(40)
    if diff=='normal':snap(name+'-tell')
    # The visible swinging part must retain actual hit pixels and expiry.
    flash=p.evaluate('''()=>{const v=v18Rig(B).find(v=>v.p.id==='left'),a=swipePixel(),hp=B.hp;B._lastPart=v.p;hitBoss(1);const pixels=swipeDiff(a,swipePixel());return{pixels,flash:v.p.flash,owner:B.flash,damage:hp-B.hp};}''')
    check(diff+' '+name+' real moving limb pixels flash',flash['pixels']>20 and flash['flash']>0 and flash['owner']>0 and flash['damage']>0,flash)
    frames(20);check(diff+' '+name+' flash expires during the swipe',p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
    if diff=='normal':snap(name+'-onion',True)
    frames(310)
    row=p.evaluate('''()=>{const T=swipeTrace.filter(q=>q.id),sides=['left','right'].map(id=>{const a=T.filter(q=>q.id===id&&q.serial===(id==='left'?0:1)&&q.t>=q.tell&&q.t<=q.tell+q.swing);return{id,samples:a.length,arc:a.length?Math.max(...a.map(q=>q.rot))-Math.min(...a.map(q=>q.rot)):0};}),commits=V19.events.filter(e=>e.event==='swipe-release');return{diff:diffKey,name:v18Model(B),sides,commits,hits:swipeHits,rootError:Math.max(...T.map(q=>Math.hypot(q.root[0]-q.joint[0],q.root[1]-q.joint[1]))),step:Math.max(...swipeTrace.slice(1).map((q,i)=>Math.hypot(q.x-swipeTrace[i].x,q.y-swipeTrace[i].y))),format:T.every(q=>q.source[0]===320&&q.source[1]===320&&q.scale===T[0].scale),complete:V19.events.some(e=>e.event==='swipe-complete')};}''');rows.append(row)
    check(diff+' '+name+' completes real arcs on both sides',all(q['samples']>=12 and q['arc']>2.20 for q in row['sides']) and row['complete'],row)
    check(diff+' '+name+' keeps planted shoulders and uniform art',row['rootError']<.001 and row['format'] and row['step']<25,row)
    check(diff+' '+name+' hits a pilot who stays in the warned attack',any('swipe' in (h['reason'] or '') for h in row['hits']),row['hits'])
    # No homing once a side has committed; a dodge cannot pull the arc after us.
    setup(phase,form,diff);p.evaluate("v19BeginSwipe(B,'commit-check','right');window.fixedTarget={...B._r30.v18.swipe.q.target};player.x=camLeftX()+20;player.y=viewTopY()+70;")
    frames(100)
    check(diff+' '+name+' locks the target and leaves a dodge lane',p.evaluate('V19.events.filter(e=>e.event==="swipe-release").every(e=>e.side!=="right"||Math.hypot(e.target.x-fixedTarget.x,e.target.y-fixedTarget.y)<.001)&&!swipeHits.some(h=>h.reason?.includes("swipe"))'),p.evaluate('swipeHits'))
  # Windup and recovery are never dangerous simply because an arm overlaps us.
  for phase,form,name in [(0,0,'infused'),(1,0,'ghost'),(2,0,'colossus'),(2,2,'volcano')]:
   setup(phase,form);p.evaluate("v19BeginSwipe(B,'inner-safety','left')")
   frames(50);p.evaluate('''()=>{const Q=B._r30.v18.swipe.q;player.x=Q.root.x;player.y=Q.root.y;swipeHits=[];}''');frames(70)
   check(name+' empty center/shoulder is outside blade contact',p.evaluate('!swipeHits.some(h=>h.reason?.includes("swipe"))'),p.evaluate('swipeHits'))
   setup(phase,form);p.evaluate("v19BeginSwipe(B,'break-check','left')");frames(76)
   p.evaluate("B._lastPart=B.parts.find(p=>p.id==='left');hitBoss(B._lastPart.hp+.1);window.breakPoint={...B._r30.v18.swipe.q.target};swipeHits=[];")
   frames(45)
   check(name+' destroyed arm stops its swipe and lock',p.evaluate('!v18Rig(B).some(v=>v.p.id==="left")&&!retinaBossTargets(B).some(q=>!q.dead&&q.id?.includes("left"))&&!swipeHits.some(h=>h.reason==="symbiote left swipe")'),p.evaluate('swipeHits'))
   p.evaluate('v18Clear(B)');check(name+' phase cleanup cancels arm damage',p.evaluate('!B._r30.v18.swipe&&!B._r30.v18.attack'))
  # The actual campaign attack books must call the arcs without review forcing.
  for phase,form,name in [(0,0,'infused'),(1,0,'ghost'),(2,0,'colossus'),(2,2,'volcano')]:
   setup(phase,form);frames(1800)
   events=p.evaluate('V19.events.filter(e=>e.event==="swipe-release").map(e=>e.side)')
   check(name+' production controller naturally swipes from both sides','left' in events and 'right' in events,events)
  check('no page, console, draw or missing asset errors',not errors,errors[:30]);br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['passed','failed','errors']}));sys.exit(bool(data['failed']))
