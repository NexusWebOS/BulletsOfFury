from pathlib import Path
import argparse,sys,json,http.server,base64,time,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
p=argparse.ArgumentParser();p.add_argument('--overlay');p.add_argument('--browser',choices=['chromium','firefox','webkit'],default='chromium');p.add_argument('--out',default='release_probe');a=p.parse_args()
O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None;port,stop=shoot.serve(str(R));report={'checks':{},'whirl':[],'errors':[]}
def ready(page,stage,kind):
 page.evaluate('c=>BAL7.setup(c)',{'stage':stage,'kind':kind,'diff':'normal','pilot':'juggernaut','level':0,'seed':7})
 end=time.monotonic()+90
 while time.monotonic()<end:
  page.evaluate('()=>{stageLoadTick();drawWorld(0);}');page.wait_for_timeout(30)
  if page.evaluate('()=>stageLoadInfo(run.stage).ready'):return
 raise RuntimeError('Stage assets did not become ready')
def shot(page,name):
 page.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(page.evaluate("()=>cv.toDataURL().split(',')[1]")))
try:
 with sync_playwright() as pw:
  br=getattr(pw,a.browser).launch(**({'args':['--mute-audio']} if a.browser=='chromium' else {}));report['engine']=a.browser;report['browser']=br.version;page=br.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');page.wait_for_function('()=>window.__bofFrames>4');page.evaluate(shoot.TRAP_RAF)
  page.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  if a.overlay:page.add_script_tag(path=a.overlay)
  ready(page,2,'infernoreaver')
  report['checks'].update(page.evaluate("""()=>{const out={};bossActive=false;warnKind='';subBossActive=true;subBoss={dead:false};player.dead=false;player.invuln=1e6;wfxReset();wfx.fireCd=.01;s2VentT=.01;s2Vents=[];fireDebris=[];geysers=[];for(let i=0;i<360;i++){wfxUpdate(1/60);s2VentTick(1/60);}out['miniboss holds NEW weather and vent events']=!wfx.fseq&&!s2Vents.length&&!fireDebris.length;out['miniboss holds three seconds of post-fight breathing room']=wfx.fireCd>=2.99&&s2VentT>=2.99;wfx.fseq={ph:'waves',t:0,fired:3,lanes:[100,300,500],wave:{x:100,y:VH+179,t:0,sc:1},_bt:[]};s2Vents=[{side:-1,x:22,y:VH+2,t:S2VENT.warn-.01,done:false}];wfxUpdate(1/60);s2VentTick(1/60);out['an already visible firewall finishes normally']=!wfx.fseq;out['an already warned vent erupts rather than disappearing']=geysers.length===1&&fireDebris.length===5;wfx.fseq=null;wfx.fireCd=3;s2VentT=3;s2Vents=[];fireDebris=[];geysers=[];subBossActive=false;for(let i=0;i<60;i++){wfxUpdate(1/60);s2VentTick(1/60);}out['environment stays quiet for the first second after victory']=!wfx.fseq&&!s2Vents.length;for(let i=0;i<125;i++){wfxUpdate(1/60);s2VentTick(1/60);}out['stage hazards resume with their normal warnings after the break']=wfx.fseq?.ph==='alerts'&&s2Vents.length===1&&!s2Vents[0].done;return out;}"""))
  for diff in ['easy','normal','hard','furious']:
   for phase in ['live','fade','gap','warn']:
    result=page.evaluate('''c=>{BAL7.setup({stage:2,kind:'infernoreaver',diff:c.diff,pilot:'juggernaut',level:0,seed:7});window.B=on5LaunchEncounter({...ON5_CODES.BOSS2,code:'BOSS2'});const b=B,F=b._fz;furnaceSync(b);furnaceEnter(b,'arms');F.attack='spin900';F.idx=0;b.flash=0;F.flash={};F.at=1;F.trans=0;b._mwStun=0;if(b._mwBarrier)b._mwBarrier.active=false;const C=balanceFlameCycle(F),offset=c.phase==='live'?C.on/2:c.phase==='fade'?C.on+C.fade/2:c.phase==='gap'?C.on+C.fade+C.gap/2:C.on+C.fade+C.gap+C.warn/2;F.at=1+offset;F.beams=[];F.tells=[];furnaceCombat(b,0);const L=F.beams[0]||F.tells[0];player.dead=false;player.invuln=0;run.shield=0;if(L){player.x=(L.x+L.ex)/2;player.y=(L.y+L.ey)/2;}else{player.x=camRightX()-20;player.y=VH-40;}const width=F.beams[0]?.width||0;furnaceTick(b,0);const dead=player.dead;b.flash=0;F.flash={};player.dead=false;player.x=camLeftX()+36;player.y=VH-70;return {dead,width,beams:F.beams.length,tells:F.tells.length};}''',{'diff':diff,'phase':phase})
    report['checks'][f'{diff} flame {phase} collision matches visible phase']=result['dead'] if phase in ['live','fade'] else not result['dead']
    if diff=='normal':shot(page,'furnace-'+phase)
  report['checks'].update(page.evaluate("""()=>{BAL7.setup({stage:2,kind:'infernoreaver',diff:'normal',pilot:'juggernaut',level:0,seed:7});const b=B;furnaceSync(b);furnaceEnter(b,'arms');const F=b._fz;F.trans=0;F.attack='spin900';F.at=2;F.beams=[{x:1,y:1,ex:1,ey:500,width:30}];F.pools.left=0;F.pools.right=Math.max(1,F.pools.right);furnaceBreak(b,'left');return {'breaking the first arm restarts a fresh attack warning':F.phase==='arms'&&F.at===0&&F.beams.length===0&&b._mwStun>=1.65};}"""))
  ready(page,5,'chromehammer')
  for diff in ['easy','normal','hard','furious']:
   for y in [200,300,400]:
    for stationary in [False,True]:
     q=page.evaluate('''c=>{BAL7.setup({stage:5,kind:'chromehammer',diff:c.diff,pilot:'juggernaut',level:0,seed:7});const b=B,h=b._hammer;b.x=24;b.y=200;b.enter=b._noHit=false;player.x=55;player.y=c.y;player.dead=false;player.invuln=0;run.shield=0;h.whirl={l:24,r:worldWidth()-24,dir:1,pass:1,passes:2,reel:0};hammerWhirlLane(b,false);h.hitCd=0;const warm=h.whirl.warm,cy=h.whirl.y+36;let t=0;const dir=player.y>=cy?1:-1;for(let i=0;i<300&&!player.dead;i++){t+=1/60;BAL7.q.t=t;if(!c.stationary&&t>=.4)player.y=clamp(player.y+dir*playerBaseSpeed()*1.35,PLAY.y+12,VH-12);h.t+=1/60;hammerCombatTick(b,1/60);if(t>warm+1.6)break;}return{...c,warm,survived:!player.dead,yEnd:player.y};}''',{'diff':diff,'y':y,'stationary':stationary})
     report['whirl'].append(q)
  page.evaluate("()=>{BAL7.setup({stage:5,kind:'chromehammer',diff:'normal',pilot:'juggernaut'});B.enter=B._noHit=false;player.x=65;player.y=310;B._hammer.whirl={l:24,r:worldWidth()-24,dir:1,pass:1,passes:2,reel:0};hammerWhirlLane(B,false);B._hammer.t=.4;hammerCombatTick(B,0);}")
  shot(page,'whirl-warning')
  ready(page,4,'stormsovereign')
  report['checks'].update(page.evaluate('''()=>{const b=B,S=b._s4war;b.enter=b._noHit=false;b.x=400;b.y=350;b._mr27.stun=1.5;S.coreUnlocked=true;stage4CoreTurretSpawnMissing(b);stage4ShieldSyncNodes(b);for(const d of S.coreTurrets){const p=stage4CoreTurretTarget(b,d.side);d.x=p.x;d.y=p.y;d.spawnT=1;d.materialize=1;}const before=S.coreTurrets.map(d=>({x:d.x,y:d.y}));b._er26.mode='escort-crossfire';b._er26.t=b._er26.warm+1;eBullets=[];for(let i=0;i<36;i++){mr27Tick(b,1/60);er26WarTick(b,1/60);}return {'Sovereign retreats out of lower arena':b.y<250,'quiet helpers stay finite and materialize':S.coreTurrets.every(d=>Number.isFinite(d.x+d.y+d.materialize)),'quiet recovery emits no shots':eBullets.length===0,'quiet hull remains physical':bossHitTest(b.x,b.y-6),'helpers follow retreat':S.coreTurrets.some((d,i)=>d.y<before[i].y)};}'''))
  shot(page,'sovereign-recovery')
  for diff in ['easy','normal','hard','furious']:
   report['checks'].update(page.evaluate("""difficulty=>{BAL7.setup({stage:4,kind:'stormsovereign',diff:difficulty,pilot:'juggernaut',level:0,seed:7});const b=B;b.enter=b._noHit=false;const C=hc1007CrossStart(b,['C','C','C','C']),P=balanceRecoveryProfile(),out={};out[difficulty+' cross retains six sectors and a full revolution']=C.duration===C.cycle*6;out[difficulty+' cross reserves its entire clear interval']=C.cycle-C.on-C.fade-C.rewarn>=P.crossGap-1e-9;for(const [mode,t] of [['live',C.on/2],['dissolve',C.on+C.fade/2],['gap',C.on+C.fade+P.crossGap/2],['tell',C.cycle-C.rewarn/2]]){C.age=C.warm+t;const S=hc1007CrossState(b),L=S.rays[0];player.dead=false;player.invuln=0;run.shield=0;player.x=L.x+(L.ex-L.x)*.2;player.y=L.y+(L.ey-L.y)*.2;hc1007CrossTick(b,0);out[difficulty+' cross '+mode+' has correct real damage']=S.mode===mode&&player.dead===(mode==='live');}player.dead=false;player.x=camLeftX()+30;player.y=VH-70;return out;}""",diff))
  shot(page,'cross-reappearance-warning')
  report['checks'].update(page.evaluate("()=>{const n=powerups.length;balanceMilestone(B,'native-test',true);const added=powerups.slice(n);balanceMilestone(B,'native-test',true);return {'milestone spawns actual collectible weapon and shield':added.length===2&&added[0].kind==='weapon'&&added[1].kind==='shield','same milestone cannot duplicate':powerups.length===n+2};}"))
  shot(page,'earned-supplies')
  br.close()
finally:stop()
report['checks']['whirl delayed movement survives 12 of 12']=sum(q['survived'] for q in report['whirl'] if not q['stationary'])==12
report['checks']['whirl stationary controls still take damage']=sum(not q['survived'] for q in report['whirl'] if q['stationary'])==12
report['runtimeSHA256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'index.html',R/'assets/game.js',R/'assets/balance_recovery_1007b.js',R/'assets/maneuver_safety_1007.js'] if p.exists()}
report['overlay']=({str(Path(a.overlay)):hashlib.sha256(Path(a.overlay).read_bytes()).hexdigest()} if a.overlay else None)
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report['checks'],indent=2));print('errors',report['errors']);assert all(report['checks'].values()) and not report['errors']
