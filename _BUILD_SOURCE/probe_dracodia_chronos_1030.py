from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[]
def ck(n,v,d=None):
 checks.append({'name':n,'passed':bool(v),'data':d});(W/'checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;B._noHit=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
  ck('Copied hammer fixture uses native form8 health',p.evaluate('B.hp===j3State(B).hp[8]&&B.maxhp===j3State(B).max[8]'))
  p.evaluate(STEP,5);p.screenshot(path=str(W/'native-idle.png'))
  ck('All authored banks and wave/lightning assets load',p.evaluate('rd74Keys().every(k=>XART.rdy(k))'))
  for difficulty,n in [('normal',1),('hard',2),('furious',4)]:
   p.evaluate("([d])=>{diffKey=d;hb20Start(B,'skystrike');}",[difficulty]);ck(difficulty+' uses the correct stroke count',p.evaluate('Q.action.strikes')==n)
   p.evaluate(STEP,50);ck(difficulty+' background windup rejects hits',p.evaluate('B._noHit'))
   p.evaluate(STEP,75);ck(difficulty+' foreground landing accepts hits',p.evaluate('!B._noHit'))
   p.screenshot(path=str(W/(difficulty+'-strike.png')))
   advance(p,'!Q.action',30,20)
  ck('Four Furious strokes include both downward impacts and side swipes',p.evaluate('RD74.events.filter(e=>e.event==="hammer-impact").slice(-4).map(e=>e.stroke).join()')=='1,2,3,4')
  p.evaluate("()=>{window.bullets0=eBullets.length;hb20Start(B,'armor');}");ck('Live armor dialogue opens with Dracodia and preserves bullets',p.evaluate('Q.speech.text==="CHROMIUM CODE ARMOR, ACTIVATED."&&!BOFCinematicDirector.active&&eBullets.length===bullets0'))
  p.evaluate(STEP,120);p.screenshot(path=str(W/'native-armor.png'));ck('Armor activation has no shield timer or legacy circular-shield action',p.evaluate('Q.shield===0&&Q.action.type==="armor"&&B._noHit'))
  p.evaluate(STEP,140);ck('Armor completes and exposes the same native HP pool',p.evaluate('Q.chrome&&Q.gunSeen&&B.hp===j3State(B).hp[8]'))
  p.evaluate("()=>{hb20Start(B,'arsenal');}");p.evaluate(STEP,165);p.screenshot(path=str(W/'native-arsenal.png'));ck('Arsenal releases the hammer upward and lifts the canonical rotary gun from its icon box',p.evaluate('Q.action.type==="arsenal"&&!!Q.action.launch&&hb20Pose(B).a.bank==="pickup_chrome"&&RD74.events.some(e=>e.event==="arsenal-gun-catch")'))
  p.evaluate(STEP,90);ck('Arsenal connects directly to the tactical chaingun body',p.evaluate('Q.action.type==="gun"&&hb20Pose(B).a.bank==="gun_chrome"'))
  p.evaluate("()=>{hb20Start(B,'throw');}");p.evaluate(STEP,90);p.screenshot(path=str(W/'native-throw.png'))
  ck('Throw releases a separate canonical hammer and empty-handed body',p.evaluate('!!Q.action.launch&&hb20Pose(B).a.empty'))
  p.evaluate("()=>{window.hp0=B.hp;window.dir0=Q.action.direction;B._lastPart=Q.parts[1];_dmgSrc=null;modularHit(20);}");ck('Ordinary gunfire cannot alter or recall the hammer',p.evaluate('Q.action.direction===dir0&&B.hp===hp0'))
  p.evaluate("()=>{_dmgSrc='missile';modularHit(20);_dmgSrc=null;}");ck('A missile reverses its direction without starting recall',p.evaluate('Q.action.direction===-dir0&&Q.action.t<5.6'))
  p.evaluate("()=>{hb20Start(B,'rage');}");p.evaluate(STEP,245);p.screenshot(path=str(W/'native-rage-charge.png'))
  ck('Rage has animated red code, dark scenery and accumulating lightning',p.evaluate('hb20Pose(B).a.bank==="charge"&&Q.action.n>0&&Q.shield===0'))
  p.evaluate(STEP,195);ck('Rage completes in7.2s with the original native HP preserved',p.evaluate('Q.rage&&Q.ragePool===hp0&&B.hp===hp0'))
  ck('Rage triggers26 lightning strikes',p.evaluate('RD74.events.filter(e=>e.event==="rage-lightning").length')==26)
  p.evaluate("()=>{hb20Start(B,'wave');}");p.evaluate(STEP,225);p.screenshot(path=str(W/'native-wave.png'));ck('Rage wave is fired from a connected hand with audible charge and release events',p.evaluate('RD74.events.some(e=>e.key==="rd74WaveCharge")&&RD74.events.some(e=>e.key==="rd74WaveFire")'))
  ck('Wave origin stays on the generated palm pixels',p.evaluate('Math.abs(Q.action.fireX-rd74Point(B,hb20Pose(B),"muzzle").x)<1'))
  p.evaluate("()=>{hb20Start(B,'gun');}");p.evaluate(STEP,120);p.screenshot(path=str(W/'native-gun.png'));ck('Chaingun uses regenerated evil body and native fan/straight volleys',p.evaluate('hb20Pose(B).a.bank==="gun_red"&&RD74.events.some(e=>e.event==="gun-volley"&&e.fan)&&RD74.events.some(e=>e.event==="gun-volley"&&!e.fan)'))
  p.evaluate("()=>{hb20Start(B,'side');B._noHit=false;B._lastPart=Q.parts[0];window.before=B.hp;modularHit(17);}");ck('Foreground body accepts native damage',p.evaluate('Math.abs(before-B.hp-17)<.001'))
  p.evaluate("()=>{v18Clear(B);}");ck('Cleanup retires state and shield danger',p.evaluate('!Q.action&&Q.shield===0'))
  ck('Native browser/drawing has no errors',not errors,errors);(W/'probe-events.json').write_text(json.dumps(p.evaluate('RD74.events'),indent=2));br.close()
finally:stop()
print(len(checks),'checks passed',flush=True)
