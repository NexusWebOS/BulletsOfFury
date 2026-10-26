"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_voice_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function("window.__bofFrames>5&&typeof C36!=='undefined'&&typeof c32Warm==='function'",timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate("()=>{fresh();boss._hammer.hb20Pickup=null;boss._hammer.state='hammer';BOFCinematicDirector.play('c36-pilot',[{who:'DECKER',text:'Bring that back in one piece!'}],()=>{},true);}")
  p.wait_for_timeout(300);shot('decker-portrait');ck('Decker uses his portrait and gold color',p.evaluate("!!UI20.dialogue.portrait&&UI20.dialogue.color==='#ffd24a'"))
  p.evaluate("()=>{BOFCinematicDirector.cancel();BOFCinematicDirector.play('c36-taunt',[{who:'CHRONOS',text:'Dodge THIS!'}],()=>{},true);}");shot('side-taunt');ck('Chronos speaks beside his body without a dialogue window',p.evaluate("C34.radio===null&&C36.caption?.text==='Dodge THIS!'"))
  p.evaluate("()=>{BOFCinematicDirector.cancel();fresh();boss._hammer.hb20Pickup=null;boss._hammer.state='shield';}")
  q=p.evaluate("()=>{const h=boss._hammer,A=fr27Armor(boss),before=[boss.hp,A.hp,h.hammerHP];boss._hammerModuleHit='body';const damage=hammerBossDamage(boss,999);return {damage,before,after:[boss.hp,A.hp,h.hammerHP]}}")
  ck('Shield absorbs without armor or body damage',q['damage']==0 and q['before']==q['after'],q);shot('absorbing-shield')
  p.evaluate("()=>{fresh();boss._hammer.hb20Pickup=null;c29Break(boss,'armor');boss._hammer.c29Break.t=1;}");shot('armor-death-pose');ck('Armor break holds authored death pose',p.evaluate("ha21Blue(boss).a.key==='c25_empty_0'"))
  p.evaluate("boss._hammer.c29Break.t=3.4");shot('armor-recovery');ck('Recovery rises through the same authored bank',p.evaluate("ha21Blue(boss).a.key.startsWith('c25_empty_')&&ha21Blue(boss).a.frame>0"))
  p.evaluate("()=>{armGun();boss._hammer.c29Break={reason:'gun',t:1};}");shot('blue-stun')
  audio=p.evaluate("""async()=>{const rows=[];for(const name of C33_CUES){const res=await fetch('assets/game/shared/combat/chronos_storm_1025/'+name+'.mp3'),buf=await res.arrayBuffer(),ac=new AudioContext(),d=await ac.decodeAudioData(buf);let peak=0;for(const v of d.getChannelData(0))peak=Math.max(peak,Math.abs(v));rows.push({name,duration:d.duration,peak});await ac.close();}return rows;}""")
  ck('All seven attack effects decode with audible samples',len(audio)==7 and all(q['peak']>.01 for q in audio),audio)
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
print(json.dumps(checks));assert all(c['passed'] for c in checks)
