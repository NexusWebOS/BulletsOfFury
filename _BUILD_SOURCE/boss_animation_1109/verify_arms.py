from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2];O=R/'_shots/boss_animation_1109';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
errors=[];checks=[]
def ck(n,v,data=None):
 checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,str(data)[:180]if not v else'',flush=True)
def shot(p,n):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/f'{n}.png'))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return ba119Warm(8)}',polling=50,timeout=180000)
  p.evaluate("()=>{window.B=boss;v18Enter(B,0,0);B._r30.mode='fight';B.enter=B._noHit=false;BOFCinematicDirector.cancel();}")
  for side in ['left','right']:
   p.evaluate("s=>{v18Clear(B);B.x=worldWidth()/2;B.y=viewTopY()+180;player.x=worldWidth()/2;player.y=VH-65;window.P=rd72Start(B,'swipe');P.side=s;}",side)
   for i in range(110):p.evaluate(STEP,1)
   shot(p,'drone-'+side+'-strike')
   q=p.evaluate("""()=>{const a=BA119_ART[ba119ArmBank('drone',P.side)],i=ba119ArmIndex(P.rd96.f),m=a.meta[i],root=P.rig.root,anchor=ba119ArmAnchor(P.side,'drone'),tip={x:root.x+m.tip[0]-anchor[0],y:root.y+m.tip[1]-anchor[1]};let hit=null;for(let y=0;y<576&&!hit;y++)for(let k=0;k<m.spans[y].length;k+=2){const x=(m.spans[y][k]+m.spans[y][k+1]-1)/2;const wx=root.x+x-anchor[0],wy=root.y+y-anchor[1];if(r30At(B,wx,wy)?.id===P.side){hit={x:wx,y:wy};break;}}return{drift:Math.hypot(tip.x-P.rig.tip.x,tip.y-P.rig.tip.y),hit,f:P.rd96.f,draws:BA119.draws[ba119ArmBank('drone',P.side)]};}""")
   ck('Drone '+side+' rendered new whole-arm poses',q['draws']>0,q)
   ck('Drone '+side+' Retina and contact use same-frame claw pixels',q['drift']<.01 and q['hit']is not None,q)
  p.evaluate("()=>{v18Clear(B);B.x=worldWidth()/2;B.y=viewTopY()+180;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;DBGT.god=true;window.P=rd72Start(B,'grab');}")
  caught=False
  for i in range(250):
   p.evaluate(STEP,1)
   if p.evaluate('!!player._rd72Grab'):caught=True;break
  ck('New drone arm retains native nonfatal catch',caught)
  if caught:
   y=p.evaluate('player.y');p.evaluate(STEP,30);ck('New held frames curl and lift the captive',p.evaluate('player.y')<y-20)
   for i in range(200):
    p.evaluate(STEP,1)
    if p.evaluate('!player._rd72Grab'):break
   ck('Native throw releases the invulnerable observer safely',p.evaluate('!player._rd72Grab&&!player.dead'))
  p.evaluate("()=>{v18Clear(B);v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=viewTopY()+180;window.P=rd77Start(B);}")
  for i in range(125):p.evaluate(STEP,1)
  shot(p,'dracodia-final-claw')
  q=p.evaluate("""()=>{const q=rd88Frame(B),P=rd88Act(B),s=P.order[P.index||0],a=q.parts[s],J=q.joints[s].shoulder;return{stage:P.stage,key:a.key,tip:q.joints[s].tip,target:a.target,shoulder:J,rect:a.rect,rows:a.spans.length,registered:!!RD88_ART.pages[a.key],px:RD88_ART.pivot};}""")
  ck('Final form uses the new articulated claw module',q['key'].startswith('nca_ba119_final-arm'),q)
  ck('Final module Retina target equals its authored claw contact',all(abs(q['tip'][k]-q['px'][k]-q['target'][k])<.01 for k in range(2)),q)
  ck('Final module keeps exact native alpha masks and hit artwork',q['rows']==576 and q['registered'],q)
  ck('No browser/renderer errors',not errors,errors);br.close()
finally:stop()
(O/'arm-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps({'failed':[c['name']for c in checks if not c['passed']],'errors':errors}),flush=True)
