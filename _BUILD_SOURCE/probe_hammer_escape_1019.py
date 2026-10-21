"""Native Hammer follow-up: actual canvas pixels, collisions and fixed-step video.

Uses shoot's Chromium/server and the existing Hammer/BAL7 encounter fixture.
"""
from pathlib import Path
import base64,json,sys,subprocess,http.server
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/hammer_escape_1019';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];videos=[]
def check(name,passed,data=None):
 checks.append({'name':name,'pass':bool(passed),'data':data})
 print(('PASS ' if passed else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.mouse.click(650,450);p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>{hm10Warm();hc11Ready();}')
  p.wait_for_function('()=>hc11Ready()',polling=50)
  def setup(diff='normal'):
   p.evaluate('(diff)=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff,fire:false,seconds:60})',diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hc11Ready();}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;
    AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.flash=0;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='storm';
    h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
    B.x=worldWidth()/2;B.y=180;h.stormHome={x:B.x,y:B.y};camX=B.x-viewW()/2;
    player.dead=player.out=false;player.alive=true;player.invuln=40002;player.x=B.x;player.y=hammerStormFloorY()-60;
    player.roll=player.somer=player._spin=player._voidDeath=null;run.shield=0;shake=whiteBlast=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;stagePlan=[];spawnClock=9999;
    HC11.events=[];hammerStormTarget(B);hammerStormImpact(B);h.leapFx=0;}''')
  def draw():p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
  def snap(name,render=True):
   if render:draw()
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));shots.append(name+'.png')
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   result=p.evaluate("""()=>{const h=B._hammer,q=h.stormWaves[2],at=q.split+q.delay+q.warm;player.invuln=0;player.x=q.x;player.y=q.y-40;player.rollCd=0;startRoll(1);const duration=player.roll?.dur;for(let i=0;i<30;i++){player.invuln=Math.max(0,player.invuln-1);q.t=at+i/60;hammerStormWaveTick(B,0);}return {alive:!player.dead,duration,active:q.active,expired:hammerStormSpikeShape(q)===null};}""")
   check(diff+' native roll survives the complete spike and its collision expires',result['alive'] and result['expired'] and result['active']<result['duration'],result)
   setup(diff)
   result=p.evaluate("""()=>{const q=B._hammer.stormWaves[2],at=q.split+q.delay+q.warm;player.invuln=0;player.x=q.x;player.y=q.y-40;player.somerCd=0;startSomersault();const duration=player.somer?.dur;for(let i=0;i<42;i++){player.invuln=Math.max(0,player.invuln-1);q.t=at+i/60;hammerStormWaveTick(B,0);}return {alive:!player.dead,duration,active:q.active,expired:hammerStormSpikeShape(q)===null};}""")
   check(diff+' native somersault survives the complete spike and its collision expires',result['alive'] and result['expired'] and result['active']<result['duration'],result)
   setup(diff)
   result=p.evaluate("""()=>{const C=hc11BeginCounter(B,{x:B.x+90,y:hc11MidY()-35,seat:1});window.C=C;player.invuln=0;player.x=C.anchor.x;player.y=C.anchor.y;hc11CounterTick(B,C,C.diveAt+.21);const air={x:B.x,y:B.y,expected:(C.oy+C.land.y)/2};return {alive:!player.dead,raised:air.y<air.expected-90,warning:C.tell,flight:C.tell-C.diveAt};}""")
   check(diff+' real counter jumps above its committed path without flight damage',result['alive'] and result['raised'] and result['warning']>=1.17,result)
   if diff=='normal':snap('jump-midflight')
   p.evaluate("()=>{player.x=C.anchor.x+160;hc11CounterTick(B,C,C.tell-C.t+.03);}")
   check(diff+' moving out of the warned landing survives',p.evaluate('!player.dead'))
   if diff=='normal':snap('jump-landing')
   setup(diff);p.evaluate("()=>{const q=B._hammer.stormWaves[2];q.t=q.split+q.delay+q.warm+.18;}")
   if diff=='normal':snap('spike-live')
  check('No native page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8')
sys.exit(any(not q['pass'] for q in checks))
