"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_storm_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=true;h.hammerDestroyed=false;h.frArmor.hp=0;h.state='hammer';boss.hp=boss.maxhp*.15;}")
  p.evaluate("()=>{armGun();boss._hammer.state='chaingun';cr17Guard(boss).tokens=0;hammerBossTick(boss,.2);}");ck('Committed minigun replenishes automatic-weapon damage allowance',p.evaluate('cr17Guard(boss).tokens>0'))
  p.evaluate("()=>{const h=boss._hammer;h._hf22Charge=null;h._hf22Red=true;c30Start(boss);h.c30.cycle=2;c30Retreat(boss);}")
  p.evaluate(STEP,100);shot('gather')
  p.evaluate(STEP,110);shot('beam')
  ck('Wave darkens scene and draws four authored descending bolts',p.evaluate('C33.lastDraw?.level===1&&C33.lastDraw.bolts===4'),p.evaluate('C33.lastDraw'))
  frame=p.evaluate('C33.lastDraw.frame');p.evaluate(STEP,7);shot('beam-next');ck('Lightning animates across native frames',p.evaluate('C33.lastDraw.frame')!=frame)
  q=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const n of C33_CUES){const d=await a.decodeAudioData(await(await fetch(BOFA.sfx['c33_'+n])).arrayBuffer());const v=d.getChannelData(0);let peak=0,sum=0;for(const x of v){peak=Math.max(peak,Math.abs(x));sum+=x*x;}out.push({name:n,duration:d.duration,peak,rms:Math.sqrt(sum/v.length)});}return out;}""")
  ck('All five ElevenLabs game cues decode with audible samples',all(v['peak']>.05 and v['rms']>.005 for v in q),q)
  p.evaluate(STEP,100);shot('restored');ck('Dimming clears outside the wave',p.evaluate('C33.lastDraw===null'))
  p.evaluate("c33Sound('rage',boss)");p.wait_for_timeout(100)
  ck('New sound uses shared mixer voice',p.evaluate("Snd.pools.c33_rage.slots.some(s=>s?.el&&!s.el.paused&&s.el.currentTime>0)"))
  p.evaluate('cr17Guard(boss).tokens=0');p.evaluate(STEP,10);ck('Rage replenishes the shared automatic-shot damage budget',p.evaluate('cr17Guard(boss).tokens>0'))
  q=p.evaluate("""()=>{const b=boss,h=b._hammer;b.hp=b.maxhp*.08;b._noHit=false;h.c30.cycle=0;c30Retreat(b);const q=ha21Blue(b),im=XART.get(q.a.key),c=document.createElement('canvas');c.width=q.a.w;c.height=q.a.h;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height).data;let pt;for(let y=70;y<150&&!pt;y++)for(let x=105;x<150;x++)if(d[(y*c.width+x)*4+3]>200){pt={x:b.x+(x+.5-q.a.pivot[0])*q.k,y:b.y+(y+.5-q.a.pivot[1])*q.k};break;}_dmgBullet={kind:'bullet',...pt};_lastHitX=pt.x;_lastHitY=pt.y;const hit=bossHitTest(pt.x,pt.y);if(hit)hitBoss(b.maxhp*10);_dmgBullet=null;return{hit,hp:b.hp,dead:b.dead,failsafe:h.gp4FailsafeSeen,emergency:!!h.gp4Emergency};}""")
  ck('Real lethal rage hit defeats Chronos through the old8% floor',q['hit']and q['dead']and not q['emergency'],q)
  p.evaluate(STEP,1)
  ck('Defeat stops owner audio',p.evaluate("C33_CUES.every(n=>Snd.pools['c33_'+n].slots.every(s=>!s?.el||s.el.paused))"))
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks))),flush=True)
