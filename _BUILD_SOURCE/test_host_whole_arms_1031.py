from pathlib import Path
import sys,json,http.server,math,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/host_whole_arms_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:500]if not v else'',flush=True);assert v,(n,d)
A=json.loads((R/'assets/game/levels/stage_08/boss/whole_arms_ball_1031/manifest.json').read_text())
def cell(n,f):
 a=A[n];im=Image.open(R/a['path']);return im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch']))
ck('All466 authored frames keep even fixed cells and explicit pivots',sum(a['frames']for a in A.values())==466 and all(a['cw']%2==a['ch']%2==0 and len(a['pivot'])==2 for a in A.values()))
ck('Hit frames retain every normal-frame alpha pixel',all(cell(n,f).getchannel('A').tobytes()==cell(n+'_hit',f).getchannel('A').tobytes()for n in A if not n.endswith('_hit')for f in range(A[n]['frames'])))
ck('Original host unit stays fixed with no bank-edge clipping',all(cell(n,f).getchannel('A').getbbox()[0]>=6 and cell(n,f).getchannel('A').getbbox()[1]>=6 and cell(n,f).getchannel('A').getbbox()[2]<=A[n]['cw']-6 and cell(n,f).getchannel('A').getbbox()[3]<=A[n]['ch']-6 for n in A if not n.endswith('_hit')for f in range(A[n]['frames'])))
ck('Whole arms retain finite anatomical reach while coiling and extending',all(75<math.dist(p['root'],p['tip'])<170 for side in ['left','right']for p in A['arm_'+side]['poses']))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD96_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  ck('Correct gated possession entrance reaches the intact full-health host',advance(p,"boss._r30.mode==='fight'",100,16)and p.evaluate('boss.hp===boss.maxhp'))
  p.evaluate("()=>{window.B=boss;window.legacy96=0;const f=rd72Blit;rd72Blit=function(n){if(rd96Physical(B)&&['claw','tendon','root_left','root_right'].includes(n))legacy96++;return f.apply(this,arguments)};window.oldFold96=0;const g=er23DrawBank;er23DrawBank=function(n){if(n==='fold'&&rb23Host(B))oldFold96++;return g.apply(this,arguments)};window.core96=B.parts.find(p=>p.id==='core').maxhp;window.origin96={x:B.x,y:B.y};}")
  def step(n):
   for i in range(0,n,10):
    e=p.evaluate(STEP,min(10,n-i));assert not e,e;p.wait_for_timeout(1)
  def shot(n):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(n+'.png')))
  def start(kind,side):p.evaluate("([k,s])=>{v18Clear(B);eBullets.length=0;B.x=origin96.x;B.y=origin96.y;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;player.roll=player.somer=null;rd72Start(B,k).side=s;}",[kind,side])
  for side in ['left','right']:
   start('swipe',side);step(45);shot(side+'-windup');P=p.evaluate('({t:rd72Act(B).t,tell:rd72Act(B).tell})');step(round((P['tell']-P['t']+.25)*60));shot(side+'-punch')
   q=p.evaluate("()=>{const P=rd72Act(B),v=RD96_ART['arm_'+P.side].poses[P.rd96.f];return{advance:Math.hypot(B.x-P.origin.x,B.y-P.origin.y),length:Math.hypot(P.rig.tip.x-P.rig.root.x,P.rig.tip.y-P.rig.root.y),nodes:P.rig.nodes.length,f:P.rd96.f,anchor:rb23PartPoint(B,B.parts.find(p=>p.id===P.side)),tip:P.rig.tip};}")
   ck(side+' uses a whole finite arm, body advance and same-frame Retina anchor',q['advance']>80 and q['length']<210 and q['nodes']==0 and q['tip']==q['anchor'],q)
   before=p.screenshot();p.evaluate("()=>{const P=rd72Act(B),a=B.parts.find(p=>p.id===P.side);markHit(a,.16);drawWorld(0)}");shot(side+'-hit');after=p.screenshot();ck(side+' native hit changes visible pixels',before!=after)
   step(15);ck(side+' hit flash expires through its normal timer',p.evaluate('B.parts.find(p=>p.id===rd72Act(B).side).flash<=0'))
   ck(side+' stroke fully retracts and body returns home',advance(p,'!rd72Act(B)',250,1)and p.evaluate('Math.hypot(B.x-origin96.x,B.y-origin96.y)<1'))
  ck('Retired segmented ligament and detached claw are never rendered',p.evaluate('legacy96===0'))
  start('swipe','left');step(83)
  q=p.evaluate("()=>{const P=rd72Act(B),a=RD96_ART['arm_'+P.side],f=P.rd96.f;for(let y=0;y<a.ch;y++){const row=a.spans[f][y];if(row.length&&y>a.ch*.6){const x=(row[0]+row[1])/2-a.pivot[0],yy=y-a.pivot[1];return{actual:r30At(B,B.x+x,B.y+yy)?.id,expected:P.side};}}}")
  ck('Moving whole-arm pixels own projectile collision',q['actual']==q['expected'],q)
  p.evaluate('()=>{v18Clear(B);B.x=origin96.x;B.y=origin96.y;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;DBGT.god=true;rd72Start(B,"grab");}')
  caught=advance(p,'!!player._rd72Grab',300,1);shot('whole-arm-grab');ck('Whole-arm reach still supports a nonfatal native capture',caught,p.evaluate('({P:rd72Act(B)?.rd96,target:rd72Act(B)?.target,tip:rd72Act(B)?.rig?.tip,ship:{x:player.x,y:player.y}})'))
  y=p.evaluate('player.y');step(30);shot('whole-arm-lift');ck('Bending complete arm lifts the held pilot',p.evaluate('!!player._rd72Grab&&!player.dead&&player.y')<y-20)
  ck('Native GOD throw releases input locks safely',advance(p,'RD72.events.some(q=>q.event==="grab-god-survived")',160,1)and p.evaluate('!player.dead&&!player._rd72Grab'))
  step(60);p.evaluate('()=>{v18Clear(B);player.invuln=0;player.x=worldWidth()/2;player.y=VH-65;rd72Start(B,"grab");}')
  ck('Second complete-arm grab catches normally',advance(p,'!!player._rd72Grab',300,1));p.evaluate('()=>{const P=rd72Act(B),a=B.parts.find(p=>p.id===P.side);B._lastPart=a;modularHit(a.hp)}');ck('Destroying the grabbing arm releases the pilot and uses current-arm blast anchors',p.evaluate('!player._rd72Grab&&!player.dead&&RD96.events.some(e=>e.event==="whole-arm-break")'))
  p.evaluate('()=>{window.hp96=B.hp;B._lastPart=B.parts.find(p=>p.id==="core");modularHit(80)}');ck('Remaining arm still protects the core',p.evaluate('B.hp===hp96'))
  p.evaluate('()=>{const a=rb23Arms(B)[0];B._lastPart=a;modularHit(a.hp)}');step(1);shot('armless-complete-torso');ck('Native arm budgets leave the entire core pool intact',p.evaluate('!rb23Arms(B).length&&B.hp===core96'))
  ck('First armless frame uses complete current torso',p.evaluate('RD96.draws.armless>0&&oldFold96===0'))
  ck('Native exposed-core owner begins its new fold',advance(p,'!!rd96Fold(B)',100,1))
  q=p.evaluate('({tell:rd96Fold(B).P.tell,hp:B.hp,f:rd96Fold(B).f})');ck('Actual folding has a readable1.50second animation',q['tell']==1.5 and q['f']<4,q)
  step(30);shot('ball-fold-half');p.evaluate('window.t96=rd96Fold(B).P.t;window.x96=B.x;window.y96=B.y;setState(GS.PAUSE)');step(40);ck('Pause freezes transformation timing and movement',p.evaluate('rd96Fold(B).P.t===t96&&B.x===x96&&B.y===y96'));p.evaluate('setState(GS.PLAY)')
  step(35);shot('ball-fold-closing');ck('Current torso still renders during shell closure',p.evaluate('!!rd96Fold(B)&&RD96.draws.fold>0&&oldFold96===0'))
  ck('Native rolling begins only after the shell closes',advance(p,'!!B._r30.v18.r25BallReady',80,1)and p.evaluate('RD96.events.filter(e=>e.event==="sphere-closed").length===1&&rd73Attack(B)._rd73.phase==="bombing"'))
  shot('ball-first-solid');f=p.evaluate('B._r30.clock');step(45);shot('ball-bombing');ck('Ball keeps native ricochet movement and bomb attacks',p.evaluate('rd73Attack(B)._rd73.drops>0&&B._r30.clock')>f)
  ck('No old cropped fold plate was drawn',p.evaluate('oldFold96===0'))
  ck('Fold and rolling Retina target stay at visible body centre',p.evaluate('(()=>{const q=rb23PartPoint(B,B.parts.find(p=>p.id==="core"));return q.x===B.x&&q.y===B.y})()'))
  p.evaluate('()=>{B._lastPart=B.parts.find(p=>p.id==="core");modularHit(45)}');shot('ball-hit');ck('Rolling core still accepts native damage and flashes',p.evaluate('B.hp===core96-45&&B.parts.find(p=>p.id==="core").flash>0'))
  ck('No browser or renderer errors',not errors,errors);(W/'events.json').write_text(json.dumps(p.evaluate('RD96.events'),indent=2));br.close()
finally:stop()
ck('Core game source remains unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
print('RESULT',len(checks),'checks passed')
