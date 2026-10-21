"""Native Stage 8 ghost soul-bomb: visible FOV, committed movement and dodge timing."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import ast,base64,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/soul_bomb_1019';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def check(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_function('typeof soul19Warm==="function"');p.mouse.click(700,500)
  p.evaluate("""()=>{window.SBQA={cues:[],draws:[]};const play=Snd.play,get=XART.get,draw=ctx.drawImage,tags=new WeakMap();Snd.play=function(k){SBQA.cues.push(k);return play.apply(this,arguments);};XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};ctx.drawImage=function(im){const k=tags.get(im);if(k?.startsWith('soul19_'))SBQA.draws.push(k);return draw.apply(this,arguments);};}""")
  def setup(diff):
   p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&soul19Warm();}',polling=50)
   p.evaluate("""()=>{B=boss;v18Budget(B);v18Enter(B,1,0);v18Fight(B);B.dead=B.enter=B._noHit=false;B.hp=B.maxhp=6000;B.x=worldWidth()/2;B.y=viewTopY()+160;B._drawY=B.y;B._r30.v18.home={x:B.x,y:B.y};B._r30.v18.seq=1;
    H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;
    enemies=[];eBullets=[];pBullets=[];player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;player.rollCd=player.somerCd=0;player.x=B.x;player.y=viewTopY()+viewH()-100;run.shield=0;shake=whiteBlast=0;Input.keys={};Input.mouse.down=false;SBQA.cues=[];SBQA.draws=[];
    v18StartAttack(B);window.P=B._r30.v18.attack;SC12.refresh();__bofFit();}""")
  def tick(n):p.evaluate('n=>{for(let i=0;i<n;i++){player.invuln=Math.max(0,player.invuln-1);v18AttackTick(B,1/60);}}',n)
  def shot(name):
   p.evaluate('()=>{shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  setup('normal');p.evaluate('()=>{Audio.resume();soul19Warm();}')
  for key in ['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact']:
   data=p.evaluate("""async key=>{await Snd._audioCtx().resume();Snd.prepare(key);await new Promise(r=>setTimeout(r,800));const pool=Snd.pools[key];Snd.stopCue(key);Snd._last[key]=0;AV3.last.clear();const played=Snd.play(key);await new Promise(r=>setTimeout(r,500));return {key,played,ctx:Snd._audioCtx().state,muted:Audio.isMuted?.(),alias:window.BOF_CHIP_PASS?.aliases[key],last:Snd._last[key],slots:pool.slots.map(s=>s?{attached:s.attached,src:s.el.currentSrc,time:s.el.currentTime,ready:s.el.readyState,paused:s.el.paused,duration:s.el.duration,ended:s.el.ended,error:s.el.error?.code,muted:s.el.muted,volume:s.el.volume}:null)};}""",key)
   print(json.dumps(data),flush=True)
  br.close()
finally:stop()
