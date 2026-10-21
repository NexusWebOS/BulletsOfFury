from pathlib import Path
from PIL import Image
from io import BytesIO
import ast,base64,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text());SETUP=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SETUP' for x in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500);p.evaluate(SETUP,dict(stage=5,kind='chromehammer',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&hm10Ready()&&b20Ready(HB20_ART.banks);}')
  p.evaluate('''()=>{window.source20=diff=>{ht27Stop();diffKey=diff;DIFF=DIFFS[diff];run.mode='arcade';run.pilot='cole';B=boss;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.x=worldWidth()/2;B.y=180;camX=B.x-VW/2;const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;B._cin30Spoke=B._fb2IntroSeen=true;h.mode='storm';h.phasePending=h.frRecovery=h.openingJump1003=false;h.recovery=null;h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};h.stormHome={x:B.x,y:B.y};h.hammerDestroyed=false;h.hammerHP=h.hammerMax;h.hc11Counter=null;h.hm10BreakPending=false;h.hb20Pickup=null;player.dead=player.out=false;player.roll=player.somer=null;player.invuln=999;player.x=B.x+40;player.y=viewTopY()+110;player.fireCd=99999;run.shield=0;run.lives=9;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;H3.ending=null;stagePlan=[];spawnClock=999999;enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=99999;D27_MODULE_DEBRIS.length=0;explosions=[];particles=[];floaters=[];smokeTrails=[];sprAnims=[];fadeOuts=[];VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;GP4.clock+=1;};window.sourceFrame20=()=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);shake=whiteBlast=0;drawWorld(0);drawHUD();};}''')
  def step(n):
   e=p.evaluate(shoot.STEP,n)
   if e:errors.append(e)
  def frame():p.evaluate('sourceFrame20');return Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB')
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('diff=>{source20(diff);hammerStormTarget(B);hammerStormImpact(B);window.C20=hc11BeginCounter(B,{x:player.x,y:player.y,seat:1});}',diff)
   row=p.evaluate('()=>{const p=hc11Tip(C20,11,C20.land.x,C20.land.y,C20.land.scale,C20.land.angle);return{error:Math.hypot(p.x-C20.anchor.x,p.y-C20.anchor.y),key:HM10_ART[C20.bank][11].key};}');ck(diff+' source counter meets its actual new PixelLab hammer head',row['error']<.001 and row['key'].startswith('hb20_counter'),row)
   images=[]
   for i in range(25):step(6);images.append(frame())
   ck(diff+' source counter completes without losing the native controller',p.evaluate('!B._hammer.hc11Counter&&Number.isFinite(B.x+B.y)'))
   if diff=='normal':images[0].save(O/'stage5-counter.webp',save_all=True,append_images=images[1:],duration=100,loop=0,quality=87)
   p.evaluate('diff=>{source20(diff);hammerStormTarget(B);hammerStormImpact(B);window.C20=hc11BeginCounter(B,{x:player.x,y:player.y,seat:1});player.invuln=0;}',diff);step(p.evaluate('Math.ceil(C20.strikeEnd*60)+2'));ck(diff+' remaining on the source counter target receives native damage',p.evaluate('player.dead'))
  for state in ['hammer','shield','hammer_stun','chaingun','spin']:
   p.evaluate('state=>{source20("normal");B._hammer.hc11Counter=null;B._hammer.hammerDestroyed=state==="hammer_stun";B._hammer.chainDestroyed=false;hammerState(B,state);B.flash=0;}',state)
   row=p.evaluate('''()=>{sourceFrame20();const a=ctx.getImageData(0,0,cv.width,cv.height).data.slice();B._hammerModuleHit=null;hammerBossDamage(B,1);sourceFrame20();const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])n++;return{pixels:n,flash:B.flash,pose:hb20Blue(B)?.a.key};}''');ck('Stage5 '+state+' visibly flashes the actual selected actor art',row['pixels']>10 and row['flash']>0,row)
  ck('No source-Hammer native renderer or update errors',not errors,errors);br.close()
finally:stop()
(O/'source-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors)),flush=True);raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
