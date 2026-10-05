"""Final pixels, readable pressure, and real loop/input checks."""
from pathlib import Path
import json,base64,sys,traceback
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/polish';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={};errors=[]
def frames(p,n,expr='updatePlay(1/60);'):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(30,n-i));p.wait_for_timeout(8)
def loop(p,n):
 for i in range(0,n,20):
  err=p.evaluate(sh.STEP,min(20,n-i))
  if err:errors.append(err)
  p.wait_for_timeout(12)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>{er26Warm();mm1003Warm();h3Warm();r30Warm();gp4AceWarm();cmap2Warm();mapgWarm();}')
  p.wait_for_function('()=>XART.rdy("mr27_storm")&&GP4_MAP_KEYS.every(k=>XART.rdy("gp4_island_"+k))&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000)
  report['pressure']=[]
  for stage,kind,mini in [(3,'frostcruiser',True),(3,'cryospear',False),(4,'olivewarden',True)]:
   p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':mini,'diff':'furious'})
   p.evaluate('()=>{window.seen=new Set();window.peak=0;window.beamFrames=0;window.attacks=new Set();}')
   frames(p,2700,'player.invuln=1e9;updatePlay(1/60);for(const q of eBullets)seen.add(q);peak=Math.max(peak,eBullets.length);if(B._l23Beam)beamFrames++;attacks.add(B._er26?.mode);if(i%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   report['pressure'].append(p.evaluate('()=>({kind:B._ship,modes:[...attacks],shots:seen.size,peak,beamFrames})'));shot(p,kind)
  # Validate fire burst splash and full launch-to-impact at the game's native damage path.
  p.evaluate(SETUP,{'stage':3,'diff':'normal'})
  p.evaluate('()=>{run.weapon=5;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.wvars=WEAPONS.map(()=>null);run.wvars[5]="fireorb";run.forge={};window.targets=[0,48].map(dx=>{const e=spawnEnemy("fighter",player.x+dx,player.y-125,{});e.hp=e.maxhp=250;e.vy=0;return e;});pShoot();window.orb=pBullets.find(q=>q.kind==="orb");}')
  frames(p,55,'for(const e of targets){e.y=player.y-125;e.vy=0;}updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);')
  report['fireOrb']=p.evaluate('()=>({element:orb._el,base:orb.dmg,dead:orb.dead,damage:targets.map(e=>250-e.hp),finite:Number.isFinite(orb.x+orb.y+orb.spin)})');shot(p,'fire-orb-burst')
  # Formation and each delayed portrait must finish before the one encounter reward.
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':'furious'})
  p.evaluate('()=>{const R=B._rebels;rf28Init(B,R);R.frIntro={done:true};const G=rg4Init(B);G.scene=null;G.gang=true;G.rescueDone=true;for(const q of R.ships){q.mode="fight";q.warp=0;q.x=camLeftX()+viewW()*(q.i+.5)/5;q.y=140;}for(let i=0;i<5;i++){R.hit=i;rebelSquadDamage(B,1e8);}}')
  frames(p,90);loop(p,1);shot(p,'rebel-first-death')
  frames(p,140);loop(p,1);shot(p,'rebel-white-death')
  frames(p,1200);report['rebelFinish']=p.evaluate('()=>({dead:B.dead,crashed:B._rebels.ships.every(q=>q._gpDeath?.crash),queued:GP4.deaths.length,portrait:GP4.death,defeated:bossDefeated})')
  # Actual frame loop supplies the widescreen transform and HUD; no mock map compositor.
  p.evaluate('()=>{H3.ending=null;run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.rivalScattered=false;campaign.rank={1:"S",2:"A",3:"A"};openStageSelect(1,{boot:true});sselUnlockCine=null;Input.clearTaps();Input.mouse.moved=false;window.sselCommitted=false;}')
  loop(p,210);shot(p,'map-zoom-arriving');loop(p,780)
  p.evaluate('()=>{MAPG.typing.at=performance.now()-12000;}');loop(p,2);shot(p,'map-desktop');p.screenshot(path=str(O/'map-full-window.png'))
  z0=p.evaluate('()=>cmap2.cam.z');p.evaluate('()=>{sselCursor=4;Input.mouse.moved=false;}');loop(p,100)
  p.evaluate('()=>{MAPG.typing.at=performance.now()-12000;}');loop(p,2);shot(p,'map-stage4-hover')
  report['map']=p.evaluate('()=>({camera:cmap2.cam,selected:sselCursor,lift:cmap2.lift[4],boot:sselBoot,keys:GP4_MAP_KEYS.map(k=>({key:k,point:cmap2World(k)}))})')
  p.set_viewport_size({'width':1000,'height':900});loop(p,120);shot(p,'map-compact')
  browser.close()
except Exception as e:report['fatal']=str(e);traceback.print_exc()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
