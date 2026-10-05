"""Native Chromium integration and pixel evidence for the recording repairs."""
from pathlib import Path
import json,base64,http.server,sys,traceback
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/repair';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={};errors=[]
def frames(p,n,expr='updatePlay(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,name,draw='drawWorld(0)'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+';}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{r30Warm();h3Warm();gp4AceWarm();}')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))&&H3_ART.every(k=>XART.rdy("h3_"+k))',timeout=120000)
  report['donors']=[]
  for form in range(1,8):
   try:
    p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
    p.evaluate('(i)=>{j3Encounter(B,2);j3Mimic(B,i);B._r30.mode="fight";B.enter=false;player.invuln=1e9;}',form)
    frames(p,900,'player.invuln=1e9;updatePlay(1/60);if(i%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
    shot(p,'donor-'+str(form))
    out=p.evaluate('()=>({form:j3State(B).mimic,hp:B.hp,history:j3State(B).gp4Donors[j3State(B).mimic].history,bullets:eBullets.length,finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy)),x:B.x,y:B.y})')
    report['donors'].append(out);print('DONOR',out,flush=True)
   except Exception as e:report['donors'].append({'form':form,'error':str(e)});print('DONOR FAIL',form,str(e),flush=True)
  p.evaluate(SETUP,{'stage':5,'kind':'chromehammer','diff':'furious'})
  p.evaluate('()=>{B._hammer.balance0922=true;B.enter=false;B._noHit=false;B.hp=B.maxhp*.081;B._hammer.restorationSeen=true;B._hammer.frTwirlDone=true;B._hammer.gp4FailsafeSeen=false;B.hp-=hammerBossDamage(B,1e8);}')
  report['hammerFloor']=p.evaluate('()=>B.hp/B.maxhp');frames(p,185,'hammerBossTick(B,1/60);')
  report['hammerReserve']=p.evaluate('()=>({hp:B.hp/B.maxhp,state:B._hammer.state,seen:B._hammer.gp4FailsafeSeen})');shot(p,'hammer-reserve')
  p.evaluate('()=>{bossDie();}');frames(p,235);shot(p,'hammer-engine-death')
  report['deathPhase']=p.evaluate('()=>H3.ending?.phase');frames(p,260);shot(p,'hammer-cutscene')
  p.evaluate('()=>{H3.ending.t=24;H3.ending.cheer=0;}');frames(p,90);shot(p,'earth-homecoming')
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':'furious'})
  p.evaluate('()=>{const R=B._rebels;rf28Init(B,R);R.frIntro={done:true};rg4Init(B);B.enter=false;B._noHit=false;for(const q of R.ships){q.mode="fight";q.warp=0;q.x=camLeftX()+viewW()*(q.i+.5)/5;q.y=140;}s6WingInit();s6WingLaunch(8,true);R.hit=0;rebelSquadDamage(B,1e8);}')
  frames(p,110);shot(p,'rebel-death');report['rebels']=p.evaluate('()=>({allies:gp4Allies(),wing:s6Wing.ships.map(q=>q.key),dead:B._rebels.ships[0].dead,portrait:GP4.death?.q.key,bossDead:B.dead})')
  frames(p,100);shot(p,'rebel-white-portrait')
  p.evaluate('()=>{H3.ending=null;boss=null;bossActive=false;run.mode="campaign";campaign.unlockedMax=8;openStageSelect(1);sselBoot=0;cmap2.cam={x:700,y:600,z:.60};}')
  p.wait_for_function('()=>GP4_MAP_KEYS.every(k=>XART.rdy("gp4_island_"+k))',timeout=120000)
  shot(p,'map-archipelago','cmap2DrawOcean();ctx.save();cmap2ApplyCamera();cmap2DrawWorld(1/60,1);ctx.restore()')
  p.evaluate('()=>{run.forgeElems={fire:1,ice:1};run.loadout=[0,1,2,3,4,5];forgeStart(()=>{});forge.row=1;forge.esel=1;forge.t=2;Input.mouse.down=false;}')
  frames(p,20,'ctx.setTransform(SS,0,0,SS,0,0);drawForge(1/60);')
  for _ in range(10):p.keyboard.press('ArrowUp');frames(p,2,'ctx.setTransform(SS,0,0,SS,0,0);drawForge(1/60);')
  shot(p,'forge-up','drawForge(0)');report['forge']=p.evaluate('()=>({error:forge.preview?.err,selection:forge.esel,elements:forgeDiscovered()})')
  browser.close()
except Exception as e:report['fatal']=str(e);traceback.print_exc()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
