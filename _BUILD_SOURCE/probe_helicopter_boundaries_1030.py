from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_helicopter_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
port,stop=serve(str(R));errors=[];checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
setup="""([rank,kind])=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.x=340;B.y=174;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;player.x=340;player.y=VH-65;DBGT.god=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;hc79State(B).seq=1;window.P=hc79Start(B,kind);}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   p.evaluate(setup,[rank,'guns'])
   for i in range(240):p.evaluate('()=>{Input.keys.a=player.x>P.safeX+2;Input.keys.d=player.x<P.safeX-2;}');p.evaluate(STEP,1)
   check(rank+' opposite-side committed gun corridor survives without GOD',p.evaluate('!player.dead&&P.safeX>340&&Math.abs(player.x-P.safeX)<7'))
   p.evaluate(setup,[rank,'sonic'])
   for i in range(280):p.evaluate('()=>{Input.keys.a=player.x>135;Input.keys.d=false;}');p.evaluate(STEP,1)
   check(rank+' broad red waves have a reachable safe flank without GOD',p.evaluate('!player.dead&&player.x<140'))
  p.evaluate(setup,['furious','missiles']);p.evaluate('()=>{DBGT.god=true;window.beepN=0;window.beepOriginal=Audio.SFX.retinaLockBeep;Audio.SFX.retinaLockBeep=function(){beepN++;return beepOriginal.apply(this,arguments);};}');p.evaluate(STEP,95)
  check('Actual shared warning voice beeps during player Retina arming/approach',p.evaluate('beepN>3&&playerLocks.some(L=>L.src?._hc79Host===B)'));p.evaluate('Audio.SFX.retinaLockBeep=beepOriginal')
  p.evaluate('()=>{v18Clear(B);window.oldBullets=eBullets.filter(q=>q._hc79Owner===B).length;}');check('Owner clear removes detached projectiles and all pending pod launches',p.evaluate('oldBullets===0&&playerLocks.filter(L=>L.src?._hc79Host===B).every(L=>L.launches.every(sh=>sh.done))'))
  p.evaluate(setup,['furious','guns']);p.evaluate('()=>{DBGT.god=true;hc79State(B).age=43;hc79Finish(B,P);B._r30.cd=.5;}');p.evaluate(STEP,1)
  check('Living copied-form visit still triggers its native covered return',p.evaluate('B._r30.mode==="v18formOut"&&rd30State(B).transition?.to===0'))
  p.evaluate(STEP,300);check('Live return preserves copied HP and main-body protection',p.evaluate('B._r30.v18.form===0&&B._r30.mode==="fight"&&j3State(B).hp[1]===j3State(B).max[1]&&rd30Locked(B)'))
  p.evaluate(setup,['furious','missiles']);p.evaluate('()=>{DBGT.god=true;for(const id of ["left","right"]){B._lastPart=B.parts.find(p=>p.id===id);modularHit(B._lastPart.hp);}hc79State(B).seq=0;v18Clear(B);window.coreBook=[];for(let i=0;i<4;i++){v18StartAttack(B);coreBook.push(hc79State(B).action.kind);v18Clear(B);}}')
  check('Destroying both pods leaves native core HP alive',p.evaluate('B.hp>1800&&B.parts.filter(p=>p.id!=="core").every(p=>p.destroyed)'))
  check('Unarmed attack book skips guns and missiles for sonic/charge counters',p.evaluate('coreBook.join(",")==="sonic,dash,sonic,dash"'))
  p.evaluate('()=>{run.stage=1;spawnBoss("damkeeper");window.O=boss;}');check('Original Stage1 helicopter remains outside the new controller',p.evaluate('!hc79Own(O)&&!hc79Live(O)'))
  check('No browser or native draw errors in boundary pass',not errors);br.close()
finally:stop();(W/'boundary-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
