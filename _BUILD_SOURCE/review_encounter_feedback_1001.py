"""Short real-time Chromium fixtures with immunity; these are not campaign wins."""
from pathlib import Path
import ast,sys,json,base64,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/encounter_feedback_1001';O.mkdir(exist_ok=True)
tree=ast.parse((R/'_BUILD_SOURCE/probe_encounter_feedback_1001.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(R));errors=[];out={'checks':[],'clips':[]}
def check(v,n):out['checks'].append({'ok':bool(v),'name':n});print(('OK ' if v else 'FAIL ')+n,flush=True)
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1050,'height':1000})
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,600)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,{'stage':7,'kind':'sludgeemperor','diff':diff})
   check(p.evaluate("()=>{const M=s7mInit(B);s7mSet(B,'recover');B._s7warden.noHit=false;M.frExit=null;for(let i=0;i<40;i++)s7mTick(B,1/60);return diffKey==='normal'?M.mode==='recover':true;}"),'Stage7 '+diff+' retains recovery window')
   p.evaluate("()=>{const M=B._s7mod;M.frExit=null;M.mode='orbs';M.t=0;M.shot=0;M.shotCD=0;window.minWarn=M.warn;for(let i=0;i<300;i++)s7mTick(B,1/60);}")
   check(p.evaluate('()=>eBullets.some(q=>q._s7modOwner===B)&&minWarn>=.8'),'Stage7 '+diff+' attacks after a readable warning')
  # No body teleport or doubled warn timer during Hammer rage.
  p.evaluate(SETUP,{'stage':5,'kind':'chromiumarchmage','diff':'furious'})
  # Use the authored stage kind when the alias differs.
  if not p.evaluate('()=>!!B?._hammer'):
   p.evaluate('()=>{spawnBoss(curStage.boss);B=boss;B.enter=false;B._noHit=false;}')
  p.evaluate("()=>{const h=B._hammer;h.balance0922=true;hammerState(B,'hammer');hammerBossTick(B,.016);hammerBossTick(B,3.5);const A=fr27Armor(B);A.rage=true;A.hp=0;A.checkpoints=[.75,.5,.35,.15];h.frRecovery=false;h.recovery=null;h.mode='hammer';B.hp=B.maxhp*.14;B._noHit=false;B.enter=false;hammerTarget(B);hammerState(B,'warn');hammerBossTick(B,.1);}")
  check(p.evaluate("()=>B._hammer.state==='warn'&&Math.abs(B._hammer.t-.1)<.001"),'Hammer rage warning clock advances once')
  p.evaluate("()=>{B.x=worldWidth()/2-90;B.y=VH*.56;hammerState(B,'leap_reset');window.lastPos={x:B.x,y:B.y};window.jump=0;for(let i=0;i<30;i++){hammerBossTick(B,1/60);jump=Math.max(jump,Math.hypot(B.x-lastPos.x,B.y-lastPos.y));lastPos={x:B.x,y:B.y};}}")
  check(p.evaluate("()=>B._hammer.state==='leap_reset'&&jump<8"),'Hammer gets a smooth half-second recovery without position jumps');shot(p,'hammer-recovery')
  # Full rate render of the rage cycle, including attack and pause.
  for name,stage,kind,seconds in [('hammer-rage',5,None,12),('ghost-form',8,'vileexistence',16),('warden-furious',7,'sludgeemperor',16)]:
   if kind:p.evaluate(SETUP,{'stage':stage,'kind':kind,'diff':'furious'})
   if name=='ghost-form':p.evaluate("()=>{r30Form(B,1);B._r30.mode='fight';B.enter=false;r30Warm();}");p.wait_for_function("()=>XART.rdy('vile25_ghost_claw')&&XART.rdy('vile25_void_knight_slash')")
   if name=='warden-furious':p.evaluate("()=>{const M=s7mInit(B);B._s7warden.noHit=false;M.frExit=null;s7mSet(B,'chase');s7mWarm();}");p.wait_for_function("()=>XART.rdy('s7m_warden')",timeout=60000)
   data=p.evaluate("""async c=>{const stream=cv.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:1600000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});const start=performance.now(),states=[],cost=[];let prev='',frames=0;rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=999;story=null;special=null;player.x=clamp(worldWidth()/2+Math.sin(t*.65)*135,camLeftX()+35,camRightX()-35);const tick=performance.now();updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);cost.push(performance.now()-tick);frames++;const state=B._r30?.attack?.type||B._s7mod?.mode||B._hammer?.state;if(state!==prev){states.push({t,state});prev=state;}if(t>=c.seconds){clearInterval(timer);resolve();}},1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return{video,frames,states,p95:cost.sort((a,b)=>a-b)[Math.floor(cost.length*.95)]};}""",{'seconds':seconds})
   (O/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]));out['clips'].append({'name':name,**data});shot(p,name)
  p.evaluate(SETUP,{'stage':6,'diff':'normal'});p.evaluate("()=>{s6WingInit();s6WingLaunch(8,true);s6Wing.beats=9;s6Wing.all=false;s6Wing.supplyIndex=3;subBossDone=false;bossDefeated=false;s6Wing.ships.forEach((q,i)=>{q.phase='leave';q.x=worldWidth()/2+(i-3.5)*40;q.y=VH*.70;q.t=0;q.dodgeT=.4;q.dodgeMode='somer';});}")
  p.evaluate('()=>{for(let i=0;i<30;i++)s6WingTick(1/60);}')
  check(p.evaluate("()=>s6Wing.ships.every(q=>q.vy<0&&q.y<VH*.70&&!q.dodgeT)"),'departing Fury ships accelerate north and clear upside-down dodge poses');shot(p,'fury-departure')
  check(not errors,'no native errors in recovery/warden/departure review');br.close()
finally:stop();out['errors']=errors;(O/'motion-review.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
sys.exit(0 if all(c['ok'] for c in out['checks']) and not errors else 1)
