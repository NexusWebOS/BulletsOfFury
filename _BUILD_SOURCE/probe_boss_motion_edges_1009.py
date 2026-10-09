"""Native counter timing/geometry at both camera edges and every difficulty."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/boss_motion_1009';checks=[];errors=[];port,stop=shoot.serve(str(ROOT))
OUT.mkdir(parents=True,exist_ok=True)
def check(name,ok,data=None):checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>{bm9Warm(Object.keys(BM9_ART));fb1002Warm();}')
  p.wait_for_function('()=>Object.values(BM9_ART).flat().every(a=>XART.rdy(a.key))')
  for diff in ['easy','normal','hard','furious','insanity']:
   p.evaluate('(d)=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"yuri",diff:d,fire:false})',diff)
   for _ in range(1800):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(5).ready;}'):break
    p.wait_for_timeout(25)
   for camera in ['left','right']:
    for side in [-1,1]:
     result=p.evaluate('([camera,side])=>{camX=camera==="left"?0:Math.max(0,worldWidth()-VW);const left=camLeftX(),right=camRightX();B.x=(left+right)/2;B.y=220;player.x=B.x+side*115;player.y=PLAY.y+145;player.invuln=1e9;const h=B._hammer;h.mode="storm";h.charged=true;h.hammerDestroyed=false;h.stormHome={x:B.x,y:220};h.t=0;h.bm9Counter=null;h.bm9CounterDone=false;hammerStormTarget(B);hammerStormImpact(B);h.t=1;hammerStormTick(B,1/60);const C=h.bm9Counter;if(!C)return{started:false,mode:h.state,top:bm9StormTop(),py:player.y};let before=null,active=null;for(let i=0;i<300;i++){hammerStormTick(B,1/60);if(C.t<C.tell)before={t:C.t,f:bm9CounterFrame(C)};if(C.t>=C.tell&&C.t<C.tell+.4){const q=bm9CounterHead(B,C);active={x:q.x,y:q.y,f:bm9CounterFrame(C)};}}return{started:true,side:C.side,tell:C.tell,before,active,done:h.bm9CounterDone,band:h.stormWaves.map(q=>({top:q.y-q.height,bottom:q.y})),left,right};}',[camera,side])
     ok=result.get('started') and result['side']==side and result['tell']>=1.35 and result['before']['f']%4==1 and result['active']['f']%4>=2 and result['done'] and all(q['bottom']-q['top']<=185.01 for q in result['band'])
     check(f'{diff} {camera} camera, swipe {side}: warn/strike/recover',ok,result)
     if diff=='furious':
      p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');(OUT/f'counter-edge-{camera}-{side}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  p.evaluate('()=>BAL7.setup({stage:4,kind:"stormsovereign",pilot:"yuri",diff:"furious",fire:false})')
  for _ in range(1800):
   if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(4).ready;}'):break
   p.wait_for_timeout(25)
  check('Destroyed Sovereign turret cannot fire or present a charge',p.evaluate('()=>{mr27Init(B);const gun=mr27Part(B,"gunL");gun.hp=0;gun.dead=true;return !mr27CanFire(B,"L")&&mr27CanFire(B,"R");}'))
  br.close()
finally:stop()
check('No page or console errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'errors':errors,'checks':checks}
(OUT/'edge-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
