"""Native repairs found in Mike's 17:48 recording of Levels 4-6.

The video has no reliable spoken transcript. Verify the observed pixels,
radar actors, ongoing radio flight and the unchanged manual-missile counter.
"""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot

R=Path(__file__).resolve().parents[1]
O=R/'_shots/harrier_wing_1018/playthrough-regression';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage6_repair_1018/index.html?scene=minicore')
  p.wait_for_function('()=>ready&&!busy');w=p.frames[1];w.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  def frames(n):
   for i in range(0,n,12):
    err=w.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(5)
  def snap(name):
   w.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  def choose(scene):p.select_option('#scene',scene);p.wait_for_function('!busy')
  w.evaluate('''()=>{
   window.qp=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return d;};
   window.qSide=(a,c,x,y,h,lo,hi)=>{let n=0;for(let yy=Math.floor(y-h/2);yy<y+h/2;yy++)for(let xx=Math.floor(x+lo-camX);xx<x+hi-camX;xx++){const i=(yy*cv.width+xx)*4;if(Math.max(Math.abs(a[i]-c[i]),Math.abs(a[i+1]-c[i+1]),Math.abs(a[i+2]-c[i+2]))>15)n++;}return n;};
   window.qChanged=(a,c)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-c[i]),Math.abs(a[i+1]-c[i+1]),Math.abs(a[i+2]-c[i+2]))>15)n++;return n;};
   window.qBlue=(a,x,y,h)=>{let n=0;for(let yy=Math.floor(y-h/2);yy<y+h/2;yy++)for(let xx=Math.floor(x-22-camX);xx<x+22-camX;xx++){const i=(yy*cv.width+xx)*4;if(a[i+2]-a[i]>24&&a[i+1]-a[i]>12)n++;}return n;};
  }''')
  for diff in ['normal','hard','furious']:
   p.select_option('#difficulty',diff);p.wait_for_function('!busy')
   for scene,mini in [('minicore',True)]:
    choose(scene);frames(65)
    # The delivered page now retains live support. Stop fresh allied impacts
    # only in this flash-expiry fixture, keeping the real renderer and timers.
    w.evaluate('''()=>{pBullets=[];for(const q of s6Wing.ships){q.fcd=q.missileCd=q.specialCd=99;q.target=null;q.think=99;}subBoss.flash=subBoss._cargo13.coreFl=0;}''')
    row=w.evaluate('''()=>{const b=subBoss,P=sc13Core(b),height=95;
     const a=qp(()=>warhiveDraw(b)),before=b._cargo13.core;
     b._cargo13.directId='core';hitSubBoss(1);
     const c=qp(()=>warhiveDraw(b));return{open:sc13Open(b),side:qSide(a,c,P.x,P.y,height,29,39),changed:qChanged(a,c),blue:qBlue(c,P.x,P.y,height),flash:b.flash,damage:before-b._cargo13.core};}''')
    label=diff+' Fortress'
    check(label+' exposed core takes real damage and retains its flash timer',row['open'] and row['damage']>0 and row['flash']>0,row)
    check(label+' hit changes actual core pixels while retaining blue electricity',row['changed']>20 and row['blue']>50,row)
    check(label+' hit no longer paints a white rectangle on the surrounding hull',row['side']<8,row)
    snap(diff+'-'+scene+'-hit')
    frames(25)
    check(label+' owner and core hit flashes expire normally',w.evaluate('subBoss.flash<=0&&subBoss._cargo13.coreFl<=0'))
   choose('harrier');frames(210)
   row=w.evaluate('''()=>({core:'reactor' in boss._carrier17,targets:retinaBossTargets(boss).map(t=>t.kind),width:boss.w,wing:s6Wing.ships.length})''')
   check(diff+' Harrier uses enlarged modules and allies without the rejected core mechanic',not row['core'] and 'reactor' not in row['targets'] and row['width']>660 and row['wing']>0,row)
   choose('ace');frames(290)
   row=w.evaluate('''()=>{SC12.refresh();const b=boss,A=b._whv.ace;return{mode:b._whv.mode,alive:!b.dead,ownerMatches:b.x===A.x&&b.y===A.y,contacts:SC12.contacts.filter(p=>p.kind==='boss').length};}''')
   check(diff+' carrier-to-ace handoff keeps the real live fighter on radar',row['mode']=='ace' and row['alive'] and row['ownerMatches'] and row['contacts']==1,row)
   row=w.evaluate('''()=>{const b=boss,A=b._whv.ace;b.x=A.x=camRightX()+20;b.y=A.y=VH/2;SC12.refresh();return{contacts:SC12.contacts.filter(p=>p.kind==='boss'),renderW:200*WHV_ACE_S};}''')
   check(diff+' partially visible ace stays as a clamped edge contact',len(row['contacts'])==1 and row['contacts'][0]['x']==1,row)
   snap(diff+'-ace-edge-radar')
   row=w.evaluate('''()=>{const b=boss,A=b._whv.ace;b.x=A.x=camRightX()+100*WHV_ACE_S+2;SC12.refresh();return SC12.contacts.filter(p=>p.kind==='boss').length;}''')
   check(diff+' completely offscreen ace leaves the radar',row==0,row)
  # Already-correct live conversation must continue to behave like flight.
  w.evaluate(SETUP,dict(stage=6,pilot='yuri',diff='furious'))
  w.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=50)
  before=w.evaluate('''()=>{s6Opening=story=fb2Intro=null;BOFCinematicDirector.cancel();H3.release=false;s6WingInit();s6Wing.beats=99;s6Wing.all=true;s6Wing.fakeDone=true;subBossDone=subBossTriggered=true;fb2TalkStart();Input.keys.d=Input.keys.j=true;player.invuln=0;playerHit=()=>{};eShoot(player.x-100,player.y-150,Math.PI/2,1,'mg');window.oldRound=eBullets.at(-1);window.qPlan=stagePlan;return{x:player.x,t:stageTimer,map:mapScroll,scroll:_stage6SkyScroll,roundY:oldRound.y};}''')
  frames(120)
  after=w.evaluate('''()=>({x:player.x,t:stageTimer,map:mapScroll,scroll:_stage6SkyScroll,roundY:oldRound.y,shots:pBullets.length,talk:fb2Talk?.age,alive:fb2TalkActive(),enemies:enemies.length,plan:stagePlan===qPlan})''')
  check('Live radio retains player steering and primary fire',after['x']>before['x']+100 and after['shots']>0,after)
  check('Live radio retains old projectile motion and sky scrolling',after['roundY']>before['roundY']+100 and after['map']>before['map'] and after['scroll']>before['scroll'],after)
  check('Live radio parks new waves without discarding the pending plan',after['t']==before['t'] and after['enemies']==0 and after['plan'],after)
  check('Radio conversation advances exactly once per native frame',after['alive'] and abs(after['talk']-2)<.01,after)
  snap('live-radio-flight')
  # Observe the Stage5 counter owner with actual native impact objects; no
  # balance, health, missile classification or healing constants are changed.
  for diff,required in [('normal',3),('hard',4),('furious',5)]:
   w.evaluate(SETUP,dict(stage=5,kind='chromehammer',pilot='yuri',diff=diff))
   # The review booted Stage6; a direct beginStage fixture does not run the
   # real Stage5 launch's preloader. Queue that stage before polling its bank.
   w.evaluate('stageLoadBegin(5)')
   w.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',polling=50)
   row=w.evaluate('''()=>{story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;B._cin30Spoke=B._fb2IntroSeen=true;B._hammer.intro1002=true;fr27BeginArmor(B);B._hammer.frArmor.activated=true;B._noHit=false;fr27Restore(B,.1,false,false);const C=hc17Counter(B);
    for(let i=0;i<8;i++){_dmgBullet={kind:i%2?'spaceVolley':'mg',x:B.x,y:B.y};hammerBossDamage(B,100);} _dmgBullet=null;return{required:C.required,hits:C.hits,status:B._hammer.recovery.status};}''')
   check(diff+' normal gunfire and automatic volley cannot break Hammer healing',row['required']==required and row['hits']==0 and row['status']=='charging',row)
   row=w.evaluate('''()=>{const q={kind:'gmiss',x:B.x,y:B.y};_dmgBullet=q;hammerBossDamage(B,10);hammerBossDamage(B,10);_dmgBullet=null;const C=hc17Counter(B);return{hits:C.hits,status:B._hammer.recovery.status};}''')
   check(diff+' one manual missile counts once despite repeated collision routing',row['hits']==1 and row['status']=='charging',row)
   row=w.evaluate('''()=>{const C=hc17Counter(B),required=C.required;for(let i=1;i<required;i++){_dmgBullet={kind:'gmiss',x:B.x,y:B.y};hammerBossDamage(B,10);} _dmgBullet=null;return{hits:C.hits,required,status:B._hammer.recovery.status,state:B._hammer.state,flash:B.flash};}''')
   check(diff+' required manual salvo interrupts healing and preserves hit feedback',row['hits']>=required and row['status']!='charging' and row['flash']>0,row)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/storm_assault_1018/index.html?scene=helpers&difficulty=furious')
  p.wait_for_function('()=>ready&&!busy');w=p.frames[1];w.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  frames(24)
  check('Stage4 harmless south-entry jets do not become radar combat contacts',w.evaluate('()=>{SC12.refresh();return SC12.contacts.every(p=>p.kind!=="helper")&&boss._s4war.coreTurrets.every(q=>q._noHit); }'))
  frames(216)
  row=w.evaluate('''()=>{SC12.refresh();return{helpers:boss._s4war.coreTurrets.filter(q=>!q.dead&&!q._noHit&&q.materialize===1).length,contacts:SC12.contacts.filter(p=>p.kind==='helper').length,bosses:SC12.contacts.filter(p=>p.kind==='boss').length};}''')
  check('Stage4 on-plane helper jets appear separately from the boss on radar',row['helpers']==row['contacts']==2 and row['bosses']==1,row)
  snap('stage4-live-helper-radar')
  row=w.evaluate('''()=>{const q=boss._s4war.coreTurrets[0];enemies.push(q);try{SC12.refresh();const x=clamp((q.x-camLeftX())/viewW(),0,1),y=clamp((q.y-viewTopY())/viewH(),0,1);return SC12.contacts.filter(p=>p.x===x&&p.y===y).length;}finally{enemies.splice(enemies.indexOf(q),1);}}''')
  check('An embedded helper also present in enemies is never counted twice',row==1,row)
  row=w.evaluate('''()=>{const q=boss._s4war.coreTurrets[0],hp=q.hp;q.hp=0;try{SC12.refresh();return SC12.contacts.filter(p=>p.kind==='helper').length;}finally{q.hp=hp;}}''')
  check('Destroyed helper disappears from the radar immediately',row==1,row)
  check('Native playthrough repairs have no page, console, draw or asset errors',not errors,errors[:30])
  br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True)
sys.exit(bool(report['failed']))
