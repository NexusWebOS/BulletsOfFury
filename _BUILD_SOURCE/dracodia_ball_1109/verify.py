from pathlib import Path
import sys,json
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=R/'_shots/dracodia_ball_1109';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
errors=[];checks=[]
def ck(n,v,data=None):
 checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n, ''if v else str(data)[:250],flush=True)
 (O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,n):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/f'{n}.png'))
SEED="""()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=B._noHit=false;BOFCinematicDirector.cancel();const hold=Input.hold;Input.hold=function(...args){return args.includes('fire')?false:hold.apply(this,args)};
 window.ballSeed=(mat='regular',diff='furious')=>{window.Q=hb20State(B);GP4.clock+=1;efxClock+=1;diffKey=diff;DIFF=difficultyForRun(run.mode,diff);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;B.hp=B.maxhp;B.x=worldWidth()/2;B.y=viewTopY()+220;B._drawY=B.y;B.flash=0;Q.action=null;Q.cool=999;Q.opening=true;Q.chrome=mat!=='regular';Q.rage=mat==='red';Q.pendingGun=Q.pendingArsenal=false;Q.pendingRecall=null;Q.seq=3;Q.speech=null;for(const p of Q.parts)p.flash=0;B._lastPart=Q.parts[0];eBullets=[];pBullets=[];powerups=[];enemies=[];player.x=worldWidth()/2;player.y=VH-50;player.invuln=1e9;DBGT.god=true;DB119.events=[];hb20Start(B,'ball');};ballSeed();}"""
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return typeof DB119!=="undefined"&&ba119Warm(8)}',polling=50,timeout=180000);p.evaluate(SEED)
  for diff in ['normal','hard','furious']:
   for mat in ['regular','chrome','red']:
    q=p.evaluate("""([m,d])=>{ballSeed(m,d);const A=Q.action,phases=new Set(),roll=new Set(),fold=new Set();let pieces=true,bounds=true;for(let i=0;i<500&&Q.action===A;i++){v19NativeTick(B,1/60);if(Q.action!==A)break;const ph=db119Phase(A),pose=hb20Pose(B);phases.add(ph);if(ph==='roll')roll.add(pose.a.frame);else if(pose.a.bank.startsWith('ba119_corrupt-fold'))fold.add(pose.a.frame);pieces&&=v19HammerRig(B).length===1;bounds&&=ph!=='roll'||B.x>=camLeftX()+DB119.radius-.01&&B.x<=camRightX()-DB119.radius+.01&&B.y>=viewTopY()+DB119.radius-.01&&B.y<=VH-DB119.radius-12+.01;}return{phases:[...phases],roll:roll.size,fold:fold.size,pieces,bounds,ended:!Q.action,bounces:A.bounces,bullets:eBullets.length};}""",[mat,diff])
    ck(f'{diff}/{mat}: full curl/roll/unfold and native recovery',q['ended']and all(k in q['phases']for k in ['curl','roll','settle','unfold'])and q['roll']==16 and q['fold']==16,q)
    ck(f'{diff}/{mat}: one physical ball, bounded ricochet, no ghost hammer or shots',q['pieces']and q['bounds']and q['bounces']>0 and q['bullets']==0,q)
  p.evaluate("ballSeed();Q.action=null;Q.chrome=true;Q.seq=3;hb20Start(B)")
  ck('Native attack book selects the restored ball',p.evaluate("Q.action.type==='ball'&&Q.seq===4"))
  cases=[('mg',False),('laser',False),('plasma',False),('gmiss',True),('missile',True),('retinaMissile',True),('nukem',True)]
  for kind,rocket in cases:
   q=p.evaluate("""([kind,rocket])=>{ballSeed();const A=Q.action;A.t=A.tell+.3;B.y=300;B._drawY=B.y;A.angle=1;const before={vx:A.vx,vy:A.vy};const at=bossHitTest(B.x,B.y);_dmgBullet={kind,x:B.x,y:B.y+40};_dmgSrc=rocket?'missile':'bullet';modularHit(7);_dmgBullet=null;_dmgSrc=null;return{at,hit:A.hitKind,flashed:B.flash>0,deflect:A.deflected,vx:A.vx,vy:A.vy,same:A.vx===before.vx&&A.vy===before.vy};}""",[kind,rocket])
   ck(kind+': native collision and correct hit/deflection',q['at']and q['flashed']and q['hit']==('rocket'if rocket else'projectile')and(q['deflect']and q['vy']<0 if rocket else q['same']and not q['deflect']),q)
   if kind in ['mg','missile']:shot(p,'hit-'+kind)
  p.evaluate("ballSeed();Q.action.t=Q.action.tell+.3;B.y=300;B._drawY=B.y")
  shot(p,'normal-ball')
  def pixels(n):
   a=np.asarray(Image.open(O/f'{n}.png').convert('RGB'),dtype=np.int16);a=a[:755,265:1015];return dict(red=int(((a[:,:,0]>180)&(a[:,:,1]<85)&(a[:,:,2]<100)).sum()),white=int((a.min(axis=2)>238).sum()))
  base=pixels('normal-ball');red=pixels('hit-mg');white=pixels('hit-missile')
  ck('Native damaged pixels are red for gunfire',red['red']>base['red']+1000,[base,red])
  ck('Native damaged pixels are white for rockets',white['white']>base['white']+1000,[base,white])
  q=p.evaluate("""()=>{const A=Q.action;_dmgBullet={kind:'gmiss',x:B.x,y:B.y+40};_dmgSrc='missile';modularHit(7);_dmgBullet=null;_dmgSrc=null;let bouncedBack=false;for(let i=0;i<240&&Q.action===A;i++){v19NativeTick(B,1/60);if(db119Phase(A)==='roll'&&A.vy>0)bouncedBack=true;}return{bouncedBack,ended:!Q.action,events:DB119.events.slice()};}""")
  ck('Rocket counter does not bounce back at the player and recovers',not q['bouncedBack']and q['ended'],q)
  q=p.evaluate("""()=>{ballSeed();Q.action.t=Q.action.tell+.3;B.y=300;const t=retinaBossTargets(B).find(t=>t._retinaId==='hb20-core');if(!t)return{target:false};const ok=retinaMissileDamage(t,7,{kind:'retinaMissile',x:t.x,y:t.y});return{target:true,ok,deflected:Q.action.deflected,hit:Q.action.hitKind};}""")
  ck('Real Retina rocket route reaches ball counter',q.get('target')and q.get('deflected')and q.get('hit')=='rocket',q)
  p.evaluate("()=>{ballSeed();Q.action.t=Q.action.tell+.3;B.y=300;_dmgBullet={kind:'mg'};_dmgSrc='bullet';modularHit(1);_dmgBullet=null;_dmgSrc=null;}")
  p.evaluate("()=>{requestAnimationFrame=__bofRealRAF;requestAnimationFrame(loop)}");p.wait_for_timeout(800)
  ck('Hit feedback expires in the live engine',p.evaluate('B.flash===0&&Q.parts[0].flash===0'),p.evaluate('({body:B.flash,part:Q.parts[0].flash})'))
  shot(p,'after-flash')
  ck('No browser/render exceptions',not errors,errors)
  if '--record'in sys.argv:
   from capture_session import capture_session
   capture_session(p)
  br.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),failures=[c['name']for c in checks if not c['passed']],errors=errors)),flush=True)
