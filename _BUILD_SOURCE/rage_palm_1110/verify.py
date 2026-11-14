from pathlib import Path
import json,sys,ast
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP;from barrage_review_common_1025 import boot
seed=(W/'seed119.js').read_text(encoding='utf8')
errors=[];checks=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n, ''if v else str(d)[:500],flush=True);(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,n):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(n+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss');p.wait_for_function('()=>{stageLoadTick();return rf1110Warm(5)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{seed119('furious','regular');B._hammer.frArmor.hp=0;B.hp=B.maxhp*.1;hf22BeginBlueRage(B);RF1110.events=[];}")
  q=p.evaluate("""()=>{const C=B._hammer._hf22Charge;let poses=new Set(),n=0;while(B._hammer._hf22Charge===C&&n++<700){hammerBossTick(B,1/60);efxClock+=1/60;if(cgChargeU(B)>=.30&&B._hammer._hf22Charge===C)poses.add(rf1110ChargeFrame(cgChargeU(B)));}return{time:n/60,frames:[...poses],strikes:RF1110.events.filter(e=>e.type==='charge-strike').length,release:RF1110.events.filter(e=>e.type==='charge-release').length,ended:!B._hammer._hf22Charge,red:B._hammer._hf22Red,hammer:B._hammer.hammerDestroyed};}""")
  ck('Chronos: full native rage transition, 16 poses, 26 once-only lightning strikes',q['ended']and q['red']and q['strikes']==26 and q['release']==1 and len(q['frames'])==16,q)
  p.evaluate("()=>{const h=B._hammer;h._c46Done=true;h._hf22Charge=null;h._hf22Red=true;h.c30=null;c30Start(B);RF1110.events=[];}")
  q=p.evaluate("""()=>{let frames=new Set(),drifts=[],hits=[],count=0;const old=c32Shot;c32Shot=function(b){const before=eBullets.length;old(b);const hands=c32Hands(b);for(const q of eBullets.slice(before))drifts.push(Math.min(...hands.map(p=>Math.hypot(p.x-q.x,p.y-q.y))));};while(count++<2500){hammerBossTick(B,1/60);efxClock+=1/60;const R=B._hammer.c30;if(R.phase==='volley_fire')frames.add(c32Pose(B).a.frame);if(R.cycle>=2)break;}c32Shot=old;const h=B._hammer,R=h.c30;return{frames:[...frames],shots:C32.events.filter(e=>e.type==='palm-shot').slice(-48).length,maxAnchor:Math.max(...drifts),count,cycle:R.cycle,hammer:h.hammerDestroyed,hp:h.hammerHP};}""")
  ck('Chronos: separate hand cycles and shots originate at actual palms',len(q['frames'])>=12 and q['maxAnchor']<.01 and q['hammer']and q['hp']==0,q)
  p.evaluate("()=>{const R=B._hammer.c30;R.phase='volley_fire';R.t=.02;R.scale=1;R.volley={beat:1,shotAt:0,lastSide:0,dual:false,group:0,flash:[.08,0],angles:[1.57,1.57],target:{x:player.x,y:player.y}};B.x=worldWidth()/2;B.y=viewTopY()+220;B.flash=0;}");shot(p,'chronos-palm')
  q=p.evaluate("()=>{const R=B._hammer.c30;R.scale=.42;return{background:bossHitTest(B.x,B.y),body:ha21Blue(B).a._rf1110};}");ck('Chronos: background remains invulnerable',not q['background']and q['body'],q)
  p.close();p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');p.wait_for_function('()=>{stageLoadTick();return rf1110Warm(8)}',timeout=180000)
  p.evaluate("""()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);Q.rage=false;Q.chrome=true;Q.pendingGun=Q.pendingArsenal=false;Q.pendingRecall=null;Q.action=null;Q.cool=999;Q.speech=null;B.hp=B.maxhp*.28;B.x=worldWidth()/2;B.y=viewTopY()+220;hb20Start(B,'rage');RF1110.events=[];}""")
  q=p.evaluate("""()=>{let n=0,poses=new Set();while(Q.action?.type==='rage'&&n++<600){v19NativeTick(B,1/60);efxClock+=1/60;const q=hb20Pose(B);if(q.a._rf1110)poses.add(q.a.frame);}return{time:n/60,poses:[...poses],rage:Q.rage,action:Q.action?.type,phase:Q.rf1110?.phase,strikes:RF1110.events.filter(e=>e.type==='charge-strike').length,hammer:Q.parts[1].destroyed,gun:Q.parts[2].destroyed,hp:B.hp};}""")
  ck('Dracodia: same full charge, 26 strikes, empty-handed rage entry',q['rage']and q['action']=='rf1110_rage'and q['phase']=='kame_up'and q['strikes']==26 and len(q['poses'])==16 and q['hammer']and q['gun'],q)
  q=p.evaluate("""()=>{let phases=new Set(),shapes=new Set(),background=true,purple=true,count=0;const hp=B.hp;RF1110.events=[];while(count++<4000&&Q.rf1110){v19NativeTick(B,1/60);efxClock+=1/60;const R=Q.rf1110;if(!R)break;phases.add(R.phase);shapes.add(hb20Pose(B).a.frame);if(R.scale<.7)background&&=B._noHit;for(const q of eBullets)purple&&=!!q._rf1110Purple;if(R.cycle>=2)break;}return{phases:[...phases],poses:[...shapes],background,purple,shots:RF1110.events.filter(e=>e.type==='palm-shot'),rig:v19HammerRig(B).map(v=>v.p.id),hp,hpAfter:B.hp,count};}""")
  required=['kame_up','kame_strafe','kame_charge','kame_thrust','kame_fire','kame_recover','kame_return','volley_move','volley_warn','volley_fire','volley_recover','retreat']
  ck('Dracodia: shared opener, foreground/background volleys, correct purple shots',all(s in q['phases']for s in required)and q['purple']and len(q['shots'])==48,q)
  ck('Dracodia: native HP preserved, core-only anatomy, protected background',q['hp']==q['hpAfter']and q['background']and q['rig']==['core'],q)
  p.evaluate("()=>{Q.rf1110.scale=1;Q.rf1110.phase='volley_fire';Q.rf1110.t=.02;Q.rf1110.volley={beat:1,shotAt:0,lastSide:0,dual:false,group:0,flash:[.08,0],angles:[1.57,1.57],target:{x:player.x,y:player.y}};B.x=worldWidth()/2;B.y=viewTopY()+220;B.flash=0;Q.parts[0].flash=0;B._noHit=false;}");shot(p,'drac-palm')
  q=p.evaluate("()=>{const a=hb20Pose(B).a;return{bank:a.bank,key:a.key,ready:XART.rdy(a.key),rig:v19HammerRig(B).map(v=>({id:v.p.id,x:v.x,y:v.y,w:v.w,h:v.h}))};}");ck('Dracodia: rendered authored frame and native modular body',q['ready']and q['bank'].startswith('drac_palms'),q)
  q=p.evaluate("()=>{B._r30.mode='fight';GP4.clock+=1;B._lastPart=Q.parts[0];const old=B.hp;modularHit(7);return{old,hp:B.hp,flash:B.flash};}");ck('Dracodia: foreground core remains damageable with true hit feedback',q['hp']==q['old']-7 and q['flash']>0,q);shot(p,'drac-palm-hit')
  ck('No browser or renderer errors',not errors,errors);br.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),failed=[x['name']for x in checks if not x['passed']],errors=errors)))
