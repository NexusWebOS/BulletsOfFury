from pathlib import Path
from PIL import Image
import sys,json,hashlib,numpy as np
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-frontal-and-rage';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
sys.stdout.reconfigure(encoding='utf-8');errors=[];checks=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name,str(data)[:400]if not ok else'',flush=True);(O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,name):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--js-flags=--expose-gc']);context=br.new_context(viewport={'width':1280,'height':800});p=boot(context,port,8,errors,'boss');p.on('console',lambda m:errors.append(m.text)if'draw error'in m.text or'update error'in m.text else None)
  p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(8))updatePlay(0);return stageLoadReady(8)&&!bp119Pending()&&ba119Warm(8)&&rf1110Warm(8)}',timeout=180000)
  setup='''()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';BOFCinematicDirector.cancel();window.Q=hb20State(B);window.seed13=(mat='regular',age=0)=>{Q.action=null;Q.rf1110=null;Q.rage=false;Q.chrome=mat==='chrome';Q.opening=true;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;Q.hammerDestroyed=false;Q.cool=999;Q.scale=1;Q.gunHP=777;Q.sf1111={acquired:false,held:false,broken:false};Q.parts.forEach(p=>p.flash=0);B.hp=B.maxhp;Q.parts[0].hp=B.hp;B.dead=B.enter=B._noHit=false;B.flash=0;B.x=worldWidth()/2;B.y=viewTopY()+200;B._drawY=B.y;B._r30.mode='fight';B._r30.v18.donorAge=age;Q._td1111Dir=Q._td1111From='center';BA119.events=[];RD74.events=[];DFR13.events=[];eBullets=[];pBullets=[];player.invuln=999;};seed13();}''';(W/'setup.js').write_text(setup);p.evaluate(setup)
  for mat in ['regular','chrome']:
   for direction,i in [('center',0),('left',2),('right',1)]:
    q=p.evaluate('''([mat,i])=>{seed13(mat);Q._td1111Next=i;hb20Start(B,'skystrike');const A=Q.action;let frames=0,bad=[],banks=new Set();for(let k=0;k<450&&Q.action===A;k++){v19NativeTick(B,1/60);if(Q.action!==A)break;const a=hb20Pose(B).a;frames++;banks.add(a.bank);if(!a.faceForward)bad.push({t:A.t,bank:a.bank,frame:a.frame})}return{frames,bad,banks:[...banks],contacts:BA119.events.filter(e=>e.type==='planted-contact').length};}''',[mat,i])
    ck(f'{mat}/{direction}: entire four-contact attack stays on authored frontal poses',q['frames']>200 and not q['bad']and q['contacts']==4 and all('overhead'in b for b in q['banks']),q)
    p.evaluate("([mat,i])=>{seed13(mat);Q._td1111Next=i;hb20Start(B,'skystrike');Q.action.t=Q.action.tell+1;ba119Root(B,Q.action);}",[mat,i]);shot(p,f'{mat}-{direction}-front-contact')
   q=p.evaluate('''m=>{seed13(m);hb20Start(B,'side');const A=Q.action;let bad=[],banks=new Set();for(let i=0;i<230&&Q.action===A;i++){v19NativeTick(B,1/60);if(Q.action!==A)break;const a=hb20Pose(B).a;banks.add(a.bank);if(!a.faceForward)bad.push({bank:a.bank,frame:a.frame})}return{bad,banks:[...banks],hits:[!!A.impact3,!!A.impact4],hp:B.hp};}''',mat)
   ck(f'{mat}: both diagonal strikes face forward through windup/hit/recovery',not q['bad']and all(q['hits'])and all('overhead'in b for b in q['banks']),q)
   for right in [False,True]:
    q=p.evaluate('''([mat,right])=>{seed13(mat);hb20Start(B,'side');const A=Q.action;A.t=A.tell+(right?.7:0)+.35;const pose=hb20Pose(B),at=rd74Point(B,pose),sample=rd74Point(B,rd74Sample((right?'right_':'left_')+rd74Mat(Q),16));return{bank:pose.a.bank,frame:pose.a.frame,front:pose.a.faceForward,error:Math.hypot(at.x-sample.x,at.y-sample.y)};}''',[mat,right]);ck(f'{mat}/{"right"if right else"left"}: actual forward hammer cap matches native impact',q['front']and q['frame']==22 and q['error']<.01,q);shot(p,f'{mat}-frontal-'+('right'if right else'left'))
   # Use the actual native damage route, and inspect the visible changed pixels.
   p.evaluate("m=>{seed13(m);hb20Start(B,'side');Q.action.t=Q.action.tell+.35;B.flash=0;efxClock=100;}",mat);shot(p,f'{mat}-before-hit')
   q=p.evaluate("()=>{const hp=B.hp;B._lastPart=Q.parts[0];GP4.clock+=1;modularHit(23);return{damaged:B.hp<hp,flash:B.flash,hp:B.hp};}");shot(p,f'{mat}-white-hit')
   a=np.array(Image.open(O/f'{mat}-before-hit.png').convert('RGB'));b=np.array(Image.open(O/f'{mat}-white-hit.png').convert('RGB'));delta=np.max(np.abs(a.astype(int)-b.astype(int)),axis=2)>30;white=(b.min(axis=2)>220)&(b.max(axis=2).astype(int)-b.min(axis=2).astype(int)<12)
   ck(f'{mat}: native body damage visibly flashes the frontal source pixels',q['damaged']and q['flash']>0 and int((delta&white).sum())>500,dict(**q,changedWhitePixels=int((delta&white).sum())))
   ck(f'{mat}: white hit feedback expires normally',p.evaluate("()=>{for(let i=0;i<20;i++)updateBoss(1/60);return B.flash<=0;}"))
  q=p.evaluate('''()=>{seed13('chrome',51.99);hb20Start(B,'side');const A=Q.action;B._lastPart=Q.parts[0];GP4.clock+=1;modularHit(B.maxhp);const hp=B.hp;A.t=A.duration-.005;v19NativeTick(B,1/60);return{hp,hpAfter:B.hp,max:B.maxhp,action:Q.action?.type,mode:B._r30.mode,form:B._r30.v18.form,age:B._r30.v18.donorAge,commits:DFR13.events.filter(e=>e.type==='native-rage-committed').length};}''')
  ck('Real low-HP damage commits rage before the overdue copied-form return',q['action']=='rage'and q['form']==8 and q['mode']=='fight'and q['age']>52 and q['hp']==q['hpAfter']and abs(q['hp']-q['max']*.28)<.01 and q['commits']==1,q)
  p.evaluate('RF1110.events=[]');saved=set();phases=[];ragehp=q['hp'];completed=False
  for batch in range(100):
   rows=p.evaluate('''()=>{const out=[];for(let i=0;i<60;i++){v19NativeTick(B,1/60);const R=Q.rf1110,A=Q.action;out.push({phase:R?.phase||A?.type||'done',cycle:R?.cycle,depth:R?.volley?.depth,hp:B.hp,age:B._r30.v18.donorAge,bank:hb20Pose(B)?.a?.bank});if(DFR13.events.some(e=>e.type==='rage-book-complete'))break}drawWorld(0);return out;}''');phases.extend(rows);last=rows[-1]
   key=last['phase']+('-'+str(last.get('depth'))if last.get('depth')else'')
   if key in ['rage','kame_charge','kame_fire','volley_fire-foreground','volley_fire-background','beam']and key not in saved:shot(p,'rage-'+key);saved.add(key)
   if p.evaluate("DFR13.events.some(e=>e.type==='rage-book-complete')"):completed=True;break
   if batch%6==0:p.wait_for_timeout(1)
  stats=p.evaluate("()=>({events:DFR13.events,shots:RF1110.events.filter(e=>e.type==='palm-shot'),red:Q.rage,pool:Q.ragePool,hp:B.hp,gunHP:Q.gunHP,hammerHP:Q.hammerHP})")
  ck('Rage visibly transforms and completes opener, foreground palms, background palms and repeat wave',completed and all(k in {q['phase']for q in phases}for k in ['rage','kame_charge','kame_thrust','kame_fire','volley_fire','gather','thrust','beam']),dict(complete=completed,phases=list(dict.fromkeys(q['phase']for q in phases))))
  ck('Both full three-group rage palm volleys actually emit native shots',all(sum(s.get('depth')==d for s in stats['shots'])>=24 for d in ['foreground','background']),dict(foreground=sum(s.get('depth')=='foreground'for s in stats['shots']),background=sum(s.get('depth')=='background'for s in stats['shots'])))
  ck('Overdue rage remains finite after a full book without healing body or weapons',completed and all(abs(q['hp']-ragehp)<.01 for q in phases)and stats['gunHP']==0 and stats['hammerHP']==0 and sum(e['type']=='rage-book-complete'for e in stats['events'])==1,dict(hp=stats['hp'],pool=stats['pool'],done=[e for e in stats['events']if e['type']=='rage-book-complete']))
  (O/'rage-native-trace.json').write_text(json.dumps(dict(phases=phases,stats=stats),separators=(',',':')))
  p.evaluate("seed13('chrome');Q.sf1111={acquired:true,held:true,broken:false};Q.gunHP=321;hb20Start(B,'gun');Q.action.t=2");ck('Approved modular gun still owns its pose and remaining HP',p.evaluate('hb20Pose(B).a._dgm1111&&Q.gunHP===321'))
  ck('No native page/update/draw errors',not errors,errors);br.close()
finally:stop()
installation=json.loads((W/'installation.json').read_text());ck('Chronus original rage/wave, ships, guns and prior owners remain byte-identical',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in installation['protected'].items()))
report=dict(checks=checks,errors=errors,runtimeHash=hashlib.sha256((R/'assets/draconus_front_rage_1113.js').read_bytes()).hexdigest(),rageHash=hashlib.sha256((R/'assets/rage_palm_1110.js').read_bytes()).hexdigest());(O/'checks.json').write_text(json.dumps(report,indent=2));assert all(c['passed']for c in checks)and not errors
