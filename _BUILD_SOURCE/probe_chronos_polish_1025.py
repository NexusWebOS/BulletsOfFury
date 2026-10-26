"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_polish_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
src=ast.parse((R/'_BUILD_SOURCE/audit_chronos_aura_gun_1025.py').read_text(encoding='utf8'))
seed=next(n.args[0].value for n in ast.walk(src) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.seedGun=' in n.args[0].value)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function("window.__bofFrames>5&&typeof C35!=='undefined'&&typeof c32Warm==='function'",timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  q=p.evaluate("()=>{C37.init(boss);const base=boss._hammer.chainMax;hammerBossInit(boss);return {hp:boss._hammer.chainHP,expected:Math.ceil(base*3)}}")
  ck('Triple native gun health',q['hp']==q['expected'],q)
  p.evaluate("armGun();boss._hammer.state='chaingun';")
  q=p.evaluate("()=>{const h=boss._hammer;h.c29GunTime=4;hammerBossTick(boss,0);boss._hammerModuleHit='chaingun';const hp=h.chainHP;hammerBossDamage(boss,100);return {heat:h.chainHeat,protected:h.chainHP===hp,interval:h.shotCd}}")
  ck('Full RPM before protection ends',q['heat']==1 and q['protected'],q)
  q=p.evaluate("()=>{boss._hammer.c29GunTime=5.01;boss._hammerModuleHit='chaingun';hammerBossDamage(boss,100);return boss._hammer.chainHP}")
  ck('Protection still ends at five seconds',q<1000,q)
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.state='hammer';boss.flash=0;boss._gp4FlashNext=0;}");shot('before-hit')
  p.evaluate("markHit(boss)");shot('hit')
  ck('Short positive body flash',p.evaluate('boss.flash===.065'))
  p.evaluate("()=>{boss.flash=Math.max(0,boss.flash-.08);markHit(boss);}");shot('expired')
  ck('Flash expires and retrigger gate preserves palette',p.evaluate('boss.flash===0'))
  from PIL import ImageChops
  before=Image.open(O/'before-hit.png');hit=Image.open(O/'hit.png');expired=Image.open(O/'expired.png')
  ck('Native hit changes rendered pixels',ImageChops.difference(before,hit).getbbox() is not None)
  ck('Native palette returns after flash',sum(1 for a,b,c in zip(before.convert('RGB').getdata(),hit.convert('RGB').getdata(),expired.convert('RGB').getdata()) if sum(abs(x-y) for x,y in zip(a,b))>180 and sum(abs(x-y) for x,y in zip(a,c))<30)>1000)
  q=p.evaluate("()=>{boss._hammer.state='fr_activation';const a=powerups.length,n=l5Rocks.length;run._spaceArmoryTimer=0;spawnContainer('crate');spaceArmorySupplyTick(1);l5RockT=0;l5RocksUpdate(.016);return {quiet:c37Quiet(),queued:C37.queue.length,pickups:powerups.length-a,rocks:l5Rocks.length-n}}")
  ck('Charge defers new supply and rock spawns',q['quiet'] and q['queued']==1 and q['pickups']==0 and q['rocks']==0,q)
  q=p.evaluate("()=>{boss._hammer.state='hammer';const n=powerups.length;hammerBossTick(boss,0);return {queued:C37.queue.length,added:powerups.length-n}}")
  ck('Deferred crate resumes outside charge',q['queued']==0 and q['added']==1,q)
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
assert all(c['passed'] for c in checks)
