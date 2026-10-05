"""Native route input, portal continuation, encounter attacks and pose pixels."""
from pathlib import Path
import json,base64,http.server,sys,traceback
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_focus_1004b';O.mkdir(exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('PASS ' if v else 'FAIL ')+name,flush=True)
def frames(p,n,expr='updatePlay(1/60);'):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(30,n-i));p.wait_for_timeout(8)
def shot(p,name,draw='drawWorld(0)'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+';}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{r30Warm();h3Warm();rg4Warm();gp4AceWarm();XART.rdy("fr27_stagex_card");}')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000)
  report['wing']=[]
  for pilot in p.evaluate('()=>PILOTS.map(p=>p.key)'):
   p.evaluate(SETUP,{'stage':6,'pilot':pilot,'diff':'furious'})
   p.evaluate('()=>{s6WingInit();s6WingLaunch(8,true);s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.beats=3;s6Wing.choice=true;s6Wing.choiceT=1;stageTimer=80;subBossDone=true;}')
   p.keyboard.down('ArrowRight');frames(p,1,'s6WingTick(1/60);');p.keyboard.up('ArrowRight');frames(p,120,'s6WingTick(1/60);')
   row=p.evaluate('()=>({pilot:run.pilot,route:s6Wing.route,allies:s6Wing.ships.filter(q=>q.phase!=="leave").map(q=>q.key)})');report['wing'].append(row)
  ck(all(x['route']=='right' and len(x['allies'])==4 and x['pilot'] not in x['allies'] for x in report['wing']),'all nine pilots retain four allies after actual Rebel-route input')
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'yuri','diff':'furious'})
  p.evaluate('()=>{rf28Init(B,B._rebels);B._rebels.frIntro={done:true};rg4Init(B);B.enter=false;B._noHit=false;s6WingInit();s6WingLaunch(8,true);s6Wing.all=true;s6Wing.route="right";s6Wing.beats=3;s6Wing.fakeDone=true;s6Wing.supplyIndex=3;window.releasePeak=0;for(const q of B._rebels.ships){q.mode="fight";q.warp=0;}}')
  frames(p,1800,'player.invuln=1e9;updatePlay(1/60);releasePeak=Math.max(releasePeak,B._rebels.ships.filter(q=>q.rg4?.act).length);if(i===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  shot(p,'rebel-five-versus-five');report['rebel']=p.evaluate('()=>({peak:releasePeak,releases:B._rebels.gang1004.events.filter(e=>e.event==="specialRelease"),wing:s6Wing.ships.filter(q=>q.phase!=="leave").map(q=>q.key)})')
  ck(report['rebel']['peak']==2 and len(set(e['pilot'] for e in report['rebel']['releases']))==5,'Furious runs two staggered specialists and all five release their own attacks')
  p.evaluate('()=>{B._rebels.ships.slice(0,3).forEach(q=>q.hp=q.max*.49);}')
  frames(p,260);shot(p,'rebel-gang');ck(p.evaluate('()=>B._rebels.gang1004.gang'),'Gang Mode still triggers at three wounded fighters')
  frames(p,3600);shot(p,'rebel-rescue-return');ck(p.evaluate('()=>B._rebels.gang1004.rescueDone&&!B._rebels.gang1004.scene&&s6Wing.ships.filter(q=>q.phase!=="leave").length===4'),'Decker scene returns the same four live allies to combat')
  p.evaluate('()=>{B._rebels.hit=0;rebelSquadDamage(B,1e8);}')
  frames(p,80);shot(p,'rebel-death-no-bar');ck(p.evaluate('()=>B._rebels.ships[0].dead&&!B.dead'),'single defeat keeps remaining encounter alive')
  # Both real Stage-6 exits create the opposite encounter, persist it and launch from map input.
  report['routes']=[]
  for route in ['left','right']:
   p.evaluate(SETUP,{'stage':6,'diff':'furious'})
   p.evaluate('(route)=>{s6WingInit();s6Wing.route=route;campaign.unlockedMax=7;scLeaveStage({bonus:0,rank:"A"});sselBoot=0;CF4.flight=3.3;}',route)
   frames(p,180,'ctx.setTransform(SS,0,0,SS,0,0);drawStageSelect(1/60);')
   shot(p,'map-pending-'+route,'drawStageSelect(0)')
   saved=p.evaluate('()=>Rival24.save()');p.evaluate('(s)=>Rival24.load(s)',saved)
   p.keyboard.press('ArrowDown');frames(p,1,'Rival24.mapInput();');frames(p,180,'ctx.setTransform(SS,0,0,SS,0,0);drawStageSelect(1/60);')
   shot(p,'map-focused-'+route,'drawStageSelect(0)')
   p.keyboard.press('Enter');frames(p,1,'Rival24.mapInput();');frames(p,2)
   row=p.evaluate('()=>({stage:run.stage,route:run._gp4StageX,pending:campaign.stageX1004,kind:boss?.kind,wing:s6Wing?.ships.length})');report['routes'].append(row)
   ck(row.get('route')==('right' if route=='left' else 'left') and row.get('wing')==4,'Stage X launches unchosen encounter after '+route+' route and save/load')
   p.evaluate('()=>scLeaveStage({bonus:0,rank:"A"})');ck(p.evaluate('()=>state===GS.STAGESEL&&campaign.stageX1004.done'),'Stage X victory returns to campaign map')
  p.evaluate(SETUP,{'stage':7,'kind':'sludgeemperor','pilot':'yuri','diff':'furious'})
  p.evaluate('()=>{run.weapon=7;run.wlevel=5;run.lives=4;s7mInit(B);B._s7mod.mode="dead";B._s7warden.final={};fr27Exit(B,1/60);Object.assign(B._s7mod.frExit,{entry:{gone:true,goneAt:0,t0:0},flame:{t0:0,k:1,fx:1},t:100});updatePlay(1/60);}')
  report['portal']=p.evaluate('()=>({stage:run.stage,state,weapon:run.weapon,lives:run.lives,mode:B._s7mod.mode,finished:B._s7warden.final.finished,rank:campaign.rank[7]})')
  ck(p.evaluate('()=>run.stage===8&&state===GS.WARPENTRY&&run.weapon===7&&run.lives>=4'),'actual Warden exit hands ship directly to Stage 8 portal with equipment and lives intact')
  frames(p,80,'ctx.setTransform(SS,0,0,SS,0,0);drawL78Entry(1/60);');shot(p,'stage8-portal-arrival','drawL78Entry(0)')
  report['reward']=p.evaluate('()=>{run.stage=6;const six=forgeComboRoll();run.stage=8;return{six,eight:forgeComboRoll()};}')
  ck(report['reward']['six']['elem']=='prism' and report['reward']['eight']['elem']=='dark','Stage 6 awards Prism; Stage 8 awards Dark Matter')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{j3Encounter(B,2);B._r30.mode="fight";B.enter=false;B._r30.cd=0;window.types=new Set();window.extents=[];}')
  for i in range(28):
   frames(p,30,'player.invuln=1e9;updatePlay(1/60);types.add(B._r30.attack?.type);')
   if i in [2,4,7,13,19,24]:shot(p,'dracula-'+str(i))
  report['dracula']=p.evaluate('()=>({types:[...types],shots:eBullets.length,finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy)),history:B._r30.history})')
  ck(all(k in report['dracula']['types'] for k in ['cf4Sweep','cf4Crush','cf4Court']) and report['dracula']['finite'],'Dracula executes three articulated attacks with finite projectiles before transformations')
  p.evaluate('()=>{j3Clear(B);j3Mimic(B,5);B._r30.mode="fight";B.enter=false;window.K=gd4Create(B,5);window.poses=new Set();}')
  for i in range(28):
   frames(p,30,'player.invuln=1e9;updatePlay(1/60);poses.add(cf4KnightFrame(K.p._hammer));')
   if i in [0,1,2,5,11,19,24]:shot(p,'knight-'+str(i))
  report['knight']=p.evaluate('()=>({poses:[...poses],history:K.history,finite:r30Parts(B).every(v=>Number.isFinite(v.x+v.y+v.rot))})')
  ck(len(report['knight']['poses'])==4 and report['knight']['finite'],'Hammer controller drives all four generated modular knight poses')
  report['music']=p.evaluate('async()=>{const out=[];for(const name of ["boss8","boss8p2","boss8p3"]){const a=new window.Audio(BOFA.music[name]);await new Promise((resolve,reject)=>{a.onloadedmetadata=resolve;a.onerror=reject;a.load();});out.push({name,src:a.src,duration:a.duration});}return out;}')
  ck(abs(report['music'][2]['duration']-131.44)<.2,'final-form MP3 preserves the supplied recording duration')
  browser.close()
except Exception as e:report['fatal']=str(e);traceback.print_exc()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
sys.exit(bool(errors) or 'fatal' in report or any(not c['ok'] for c in report['checks']))
