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
OUT=ROOT/'_shots/hammer_finish_1019';OUT.mkdir(parents=True,exist_ok=True)
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
  p.wait_for_function('typeof hf19Ready==="function"');p.evaluate('()=>{hf19Ready();hm10Warm();}');p.wait_for_function('()=>hf19Ready()&&hm10Ready()',polling=50)
  p.evaluate("""()=>{window.hf19Draw=()=>{BAL7.seed(1019);shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width/SS,cv.height/SS);hammerBossDraw(B);};window.hf19Pixels=()=>Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);}""")
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   for state in ['chaingun','shield','fr_activation','hammer_stun','storm_stun','fr_stun','recover','hammer','storm_idle','storm_raise']:
    row=p.evaluate("""state=>{const h=B._hammer;B.dead=false;B.hp=6000;B._gp4FlashNext=0;h.hc11Counter=null;h.state=state;h.t=state==='storm_raise'?1.4:.7;h.chainDestroyed=false;h.chainHeat=.6;h.chainMuzzle=state==='chaingun'?.09:0;h.empowered=true;h.empowerLevel=1;h.charged=true;h.recovery=null;B._noHit=false;B.flash=0;h.frArmor.barrier=['shield','fr_activation'].includes(state)?2:0;hf19Draw();let before=hf19Pixels();const pick=hf19Pick(B);const old=HMF19.draws.recovery||0;hammerBossDamage(B,1);const nativeFlash=B.flash,armorFlash=h.frArmor.flash;B.flash=0;h.frArmor.flash=0;hf19Draw();before=hf19Pixels();B.flash=nativeFlash;h.frArmor.flash=armorFlash;hf19Draw();const after=hf19Pixels();let changed=0,white=0;for(let i=0;i<before.length;i+=4){if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])changed++;if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;}const hit=B.flash;B.flash=0;if(h.frArmor)h.frArmor.flash=0;hf19Draw();const expiry=hf19Pixels();let mismatch=0;for(let i=0;i<before.length;i++)if(before[i]!==expiry[i])mismatch++;return{changed,white,hit,mismatch,kind:pick?.kind,key:pick?.a.key,alpha:ctx.globalAlpha,recovery:HMF19.draws.recovery-old};}""",state)
    check(diff+' '+state+' native hit changes actual pixels',row['changed']>20 and row['white']>20 and row['hit']>0,row)
    check(diff+' '+state+' original colours return after flash',row['mismatch']<1500,row)
    if state in ['hammer_stun','storm_stun','fr_stun','recover']:check(diff+' '+state+' uses opaque intact recovery bank',row['kind']=='recovery' and row['recovery']>0 and row['alpha']==1,row)
    if state in ['shield','fr_activation']:check(diff+' '+state+' uses new shield pose',row['kind']=='shield' and row['key'].startswith('hm10_shield_form'),row)
    if diff=='normal' and state in ['chaingun','shield','hammer_stun','storm_raise']:snap(state)
   row=p.evaluate("""()=>{const h=B._hammer;h.state='chaingun';h.chainDestroyed=false;h.chainMuzzle=.09;const keys=[];for(let i=0;i<16;i++){h.t=i/16;keys.push(hf19Pick(B).a.key);}h.chainDestroyed=true;return{unique:new Set(keys).size,broken:hf19Pick(B)};}""")
   check(diff+' firing reel visits eight poses and hides when gun breaks',row['unique']==8 and row['broken'] is None,row)
  setup('normal')
  row=p.evaluate("""()=>{const h=B._hammer;h.state='shield';B.flash=0;B._gp4FlashNext=0;const q={x:B.x,y:B.y+85,vy:-1};cp12Absorb(B,q);return{dead:q.dead,flash:B.flash,armor:h.frArmor.flash};}""")
  check('Absorbed projectile flashes the actual boss and shield owners',row['dead'] and row['flash']>0 and row['armor']>0,row)
  p.evaluate('()=>XART.rdy("ht27_boss")');p.wait_for_function('()=>XART.rdy("ht27_boss")',polling=50)
  row=p.evaluate("""()=>{B._hammerTime={mode:'dance'};const draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width/SS,cv.height/SS);ht27Sprite('boss',0,240,350,225,.58);};B.flash=0;draw();const before=hf19Pixels();markHit(B);B.flash=.16;draw();const after=hf19Pixels();let changed=0;for(let i=0;i<before.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)changed++;delete B._hammerTime;return changed;}""")
  check('Password choreography uses a bright hit flash instead of fading',row>20,row)
  # Native Stage 8 Hammer body uses the same selected bank and opaque rig.
  p.evaluate('(diff)=>BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff,fire:false,seconds:60})','normal')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}',polling=50)
  p.evaluate("""()=>{B=boss;v18Budget(B);v18Enter(B,2,8);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+190;B._drawY=B.y;window.P=gd4Create(B,8).p;window.H=P._hammer;H.hc11Counter=null;H.throw=null;H.hammerDestroyed=false;H3.release=false;H3.ending=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();P.x=B.x;P.y=B.y;}""")
  for state in ['chaingun','shield','hammer_stun']:
   row=p.evaluate("""state=>{H.state=state;H.t=.7;H.chainDestroyed=false;H.chainMuzzle=.09;P.flash=B.flash=0;const rig=v19HammerRig(B);ctx.setTransform(SS,0,0,SS,0,0);v19Body(B);return{keys:rig.map(v=>v.key),opaque:rig.every(v=>v.alpha===1),picked:hf19Pick(P)?.a.key};}""",state)
   check('Stage 8 '+state+' shares the approved animation bank',row['opaque'] and row['picked'] in row['keys'],row)
  check('No native page, console or asset errors',not errors,errors)
  br.close()
finally:
 print('ERRORS',json.dumps(errors),flush=True)
 stop()
(OUT/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8')
sys.exit(any(not q['pass'] for q in checks))
