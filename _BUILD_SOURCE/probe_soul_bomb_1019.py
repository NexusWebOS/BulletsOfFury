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
  for diff in ['easy','normal','hard','furious']:
   setup(diff);row=p.evaluate('({type:P.type,tell:P.tell,travel:P.travel,target:P.target,phase:P.phase,cues:SBQA.cues})')
   check(diff+' ghost naturally selects the new soul bomb',row['type']=='soulBomb' and row['tell']>=1.3,row)
   check(diff+' only one recorded charge cue is requested',row['cues'].count('bossWeaponCharge')==1 and 'shadowCharge' not in row['cues'],row['cues'])
   tick(12)
   if diff=='normal':shot('charge-green')
   p.evaluate('()=>{P.t=P.tell-.12;}');tick(1);check(diff+' complete warning stays harmless',p.evaluate('!player.dead&&P.phase==="charge"'))
   if diff=='normal':shot('charge-red')
   row=p.evaluate('()=>{const frozen=JSON.stringify(P.target);player.x+=135;return frozen;}');tick(1);check(diff+' dodging never drags the captured target',p.evaluate('JSON.stringify(P.target)')==row)
   p.evaluate('()=>{P.t=P.tell+P.travel*.45;P.x=lerp(P.cast.x,P.target.x,.45);P.y=lerp(P.cast.y,P.target.y,.45);P.phase="flight";}')
   if diff=='normal':shot('skull-flight')
   tick(60);check(diff+' moving aside survives the comet and burst',p.evaluate('!player.dead'))
   # Held target must take real native damage once the projectile arrives.
   setup(diff);tick(p.evaluate('Math.ceil((P.tell+P.travel+.1)*60)'));check(diff+' holding the warned position is dangerous',p.evaluate('player.dead||run.shield<0'))
   for dodge in ['roll','somersault']:
    setup(diff);p.evaluate('()=>{P.t=P.tell+Math.max(0,P.travel-.20);const u=Math.max(0,P.travel-.20)/P.travel;P.x=lerp(P.cast.x,P.target.x,u);P.y=lerp(P.cast.y,P.target.y,u);P.started=true;P.phase="flight";}')
    p.evaluate('()=>startRoll(1)' if dodge=='roll' else '()=>startSomersault()');tick(34 if dodge=='roll' else 44)
    check(diff+' well-timed '+dodge+' clears the full damage window',p.evaluate('!player.dead'))
   setup(diff);p.evaluate('()=>{player.x=P.target.x+150;P.t=P.tell+P.travel+.23;P.x=P.target.x;P.y=P.target.y;P.phase="burst";}')
   if diff=='normal':shot('burst')
   before=p.evaluate('P.t');p.evaluate('()=>{for(let i=0;i<8;i++)soul19Draw(B);}');check(diff+' rendering cannot advance the attack clock',p.evaluate('P.t')==before)
   row=p.evaluate('()=>{v18Clear(B);const before=SBQA.draws.length;soul19Draw(B);return{cleared:!B._r30.v18.attack,extra:SBQA.draws.length-before};}');check(diff+' phase cancellation removes every bomb visual',row['cleared'] and row['extra']==0,row)
  p.evaluate('()=>{Audio.resume();soul19Warm();}')
  for cue in ['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact']:
   row=p.evaluate("""async key=>{await Snd._audioCtx().resume();const alias=CA15.aliases[key]||key,canonical=window.BOF_CHIP_PASS?.aliases[alias]||alias;Snd.stopCue(canonical);Snd._last[canonical]=0;AV3.last.clear();const requested=Snd.play(key);let a=null;for(let wait=0;wait<100;wait++){a=Snd.pools[canonical]?.slots.find(v=>v?.attached&&!v.el.paused&&v.el.currentTime>0)?.el;if(a)break;await new Promise(r=>setTimeout(r,10));}if(!a)return {playing:false,requested,canonical};const c=Snd._audioCtx(),m=c.createAnalyser();m.fftSize=256;let capture=null;if(a._bofNode)a._bofNode.connect(m);else{capture=c.createMediaStreamSource((a.captureStream||a.mozCaptureStream).call(a));capture.connect(m);}const data=new Float32Array(256);let peak=0;for(let i=0;i<28;i++){await new Promise(r=>setTimeout(r,10));m.getFloatTimeDomainData(data);for(const v of data)peak=Math.max(peak,Math.abs(v));}if(a._bofNode)a._bofNode.disconnect(m);capture?.disconnect();return {canonical,playing:a.currentTime>0,peak,volume:a.volume};}""",cue)
   check(cue+' plays decoded nonzero audio through the native mixer',row.get('playing') and row.get('peak',0)>0 and row.get('volume',0)>0,row)
  check('Real charge/flight/burst sheets all render through the game canvas',p.evaluate("['charge','flight','burst'].every(k=>SOUL19.draws[k]>0)"),p.evaluate('SOUL19.draws'))
  # Real encounter animation film: native boss clock and canvas, no fabricated frames.
  setup('normal');p.evaluate('player.x+=140;player.invuln=999;');film=[]
  for i in range(70):
   p.evaluate('()=>{for(let j=0;j<3;j++)r30Tick(B,1/60);shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   film.append(Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGBA'))
  film[0].save(O/'encounter.webp',save_all=True,append_images=film[1:],duration=50,loop=0,lossless=True)
  check('No page, console, draw or asset errors',not errors,errors)
  br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2)+'\n',encoding='utf-8');sys.exit(any(not q['passed'] for q in checks))
