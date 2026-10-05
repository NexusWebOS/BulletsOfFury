"""Native Chromium proof for pilot bars, arsenal pixels and survivor scenes."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/rebel_arsenal_1004c';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[]
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
RESET="""()=>{rg4Clear(G);G.scene=null;G.rescueDone=true;H3.release=false;B._noHit=false;G.releaseAt=G.age+999;G.novaFx=[];G.rebelBoxes=[];eBullets=[];pBullets=[];for(const q of R.ships){q.dead=false;q.hp=q.max;q.frCloak=0;q.flash=0;q.rfHeading=null;q.evadeT=0;q.rg4.cd=999;q.rg4.gunCd=999;q.rg4.act=null;q.rg4.supply=null;q.rg4.armed=null;q.rg4.trace=[];q.mode='fight';q.x=worldWidth()/2+(q.i-2)*72;q.y=130+(q.i%2)*75;}player.invuln=1e9;}"""
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  if '--review' in sys.argv:
   p.goto(f'http://127.0.0.1:{port}/_shots/rebel_arsenal_1004c/review.html',timeout=120000)
   p.screenshot(path=str(O/'review-page.png'))
   for label,kind in [('Full encounter','intro'),('Fight now','fight'),('Gang Mode','gang'),('Voss turbo','turbo'),('Voss Fusion','fusion'),('Rook .50 cal','slug'),('Jace helix','helix'),('Kaia rockets','rockets'),('Nyx stealth','cloak')]:
    p.get_by_role('button',name=label,exact=True).click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Encounter ready."',timeout=120000)
    f=p.locator('#arena').element_handle().content_frame();f.evaluate(sh.TRAP_RAF);frames(f,1)
    ck(f.evaluate('(kind)=>kind==="intro"?!boss._rebels.frIntro?.done:kind==="fight"?!rg4State().scene:kind==="gang"?rg4State().scene?.kind==="gang":boss._rebels.ships.some(q=>q.rg4.act?.kind===kind)',kind),label+' opens its live encounter state')
    ck(f.evaluate('()=>s6Wing.ships.length===4'),'practice '+kind+' keeps exactly four allies beside the player')
    if kind=='fight':
     f.evaluate('()=>player.invuln=1e9');key=f.evaluate('()=>keybindFor(1).fire[0]');p.keyboard.down(key);frames(f,15);p.keyboard.up(key)
     ck(f.evaluate('()=>pBullets.some(q=>!q.ally)'),'real keyboard fire creates player shots in practice');shot(f,'playable-fight')
   p.get_by_label('Pilot',exact=True).select_option('decker')
   for survivor in ['kaia','nyx','jace','rook','voss']:
    p.get_by_label('Counter-scan survivor',exact=True).select_option(survivor);p.get_by_role('button',name='Decker cloak scene',exact=True).click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Encounter ready."',timeout=120000)
    f=p.locator('#arena').element_handle().content_frame();f.evaluate(sh.TRAP_RAF);frames(f,1)
    ck(f.evaluate('(s)=>rg4State().scanner===s&&rg4State().members.filter(m=>m.key==="decker").length===1&&rg4State().members[0].ref===player',survivor),'practice '+survivor+' scene selects correct survivor without duplicating Decker')
   ck(not errors,'all playable shortcuts have zero page/console errors');report['errors']=errors
   (O/'review-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8');browser.close();sys.exit(any(not c['ok'] for c in report['checks']))
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':'furious','pilot':'yuri'})
  p.evaluate("""()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=false;B._noHit=false;window.G=rg4Init(B);H3.release=false;fb2Talk=null;s6Opening=null;rg4Warm();s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;for(const q of s6Wing.ships){q.phase='fight';q.specialCd=999;q.missileCd=999;q.fcd=999;}}""")
  p.wait_for_function("()=>XART.rdy('ra4_ui')&&XART.rdy('ra4_fx')&&Object.values(RA4_ART.palette).every(q=>XART.rdy(q.key))",timeout=90000)
  frames(p,150);p.evaluate(RESET)
  p.evaluate("""()=>{window.nativeBlits={};const map=new Map();const get=XART.get,draw=ctx.drawImage;XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)nativeBlits[k]=(nativeBlits[k]||0)+1;return draw.apply(this,arguments);};for(const k of ['ra4_ui','ra4_fx','ra4_nhxsb_g_2','ra4_fchgc_2','nhxsb_g_2','fchgc_2'])XART.rdy(k);} """)
  p.wait_for_function("()=>XART.rdy('nhxsb_g_2')&&XART.rdy('fchgc_2')",timeout=90000)
  # Direct resolved source art, drawn by the game context; no .src/identity assumptions.
  p.evaluate("""()=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#071522';ctx.fillRect(0,0,cv.width,cv.height);ctx.drawImage(XART.get('ra4_ui'),0,0,cv.width,cv.height*.6);['nhxsb_g_2','ra4_nhxsb_g_2','fchgc_2','ra4_fchgc_2'].forEach((k,i)=>ctx.drawImage(XART.get(k),25+i*115,cv.height*.65,100,140));}""")
  (O/'source-art.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  shot(p,'five-vs-five')
  ck(p.evaluate('()=>RA4.bars.length===5&&new Set(RA4.bars.map(q=>q.pilot)).size===5'),'five independent pilot-attached health readouts render')
  ck(p.evaluate('()=>new Set(RA4.badges.map(q=>q.key)).size===5'),'player and four live allies render their ability icons')
  p.evaluate('()=>{window.beforeBar=RA4.bars.find(q=>q.pilot==="jace");R.ships[4].x+=37;R.ships[4].y+=29;}');shot(p,'attached-bars')
  ck(p.evaluate('()=>{const q=RA4.bars.find(q=>q.pilot==="jace");return q.x-beforeBar.x===37&&q.y-beforeBar.y===29;}'),'rendered Jace bar follows his moved ship without a fixed HUD slot')
  for key,kind,warm in [('voss','turbo',1.35),('rook','slug',1.0),('jace','helix',2.0),('kaia','rockets',1.75),('nyx','cloak',1.15)]:
   p.evaluate(RESET);p.evaluate('([key,kind])=>{window.Q=R.ships.find(q=>q.key===key);if(key==="nyx")window.oldNyxLock=retinaBossTargets(B).find(t=>t._retinaId==="nyx-hull");rg4Attack(Q,R,G,kind);}',[key,kind]);frames(p,int(warm*60*.7));shot(p,kind+'-charge');frames(p,int(warm*60*.3)+10);shot(p,kind+'-release')
   ck(p.evaluate('(kind)=>G.events.some(e=>e.event==="specialRelease"&&e.kind===kind)',kind),kind+' warned release reaches real gameplay')
   if kind=='turbo':
    for i in range(40):
     frames(p,5)
     if p.evaluate('()=>Q.rg4.act?.phase==="row"'):break
    frames(p,25);shot(p,'turbo-warning-row');ck(p.evaluate('()=>Q.rg4.act?.phase==="row"&&(Q.x<camLeftX()||Q.x>camRightX())'),'turbo commits offscreen horizontal passes with a warning row')
   if kind=='helix':
    ck(p.evaluate('()=>G.ord.some(q=>q.kind==="helix"&&!q.dead)'),'actual authored red-orange ball exists in combat')
    frames(p,80);shot(p,'helix-eight-way-nova');ck(p.evaluate('()=>G.events.some(e=>e.event==="helixNova"&&e.count===8)&&eBullets.filter(q=>q._ra4MiniBall).length===8'),'actual helix detonation emits eight energy balls')
   if kind=='rockets':
    frames(p,28);shot(p,'alternating-rockets');ck(p.evaluate('()=>{const a=G.events.filter(e=>e.event==="rocketLaunch").slice(-2);return a.length===2&&a[0].side===-a[1].side;}'),'Kaia renders sequential alternating launcher releases')
   if kind=='cloak':
    ck(p.evaluate('()=>!RA4.bars.some(q=>q.pilot==="nyx")&&!retinaBossTargets(B).some(q=>q._retinaId==="nyx-hull")'),'Nyx tracing remains visible while HP and missile acquisition disappear')
    ck(p.evaluate('()=>oldNyxLock&&!retinaTargetValid(oldNyxLock)'),'cloaking invalidates Nyx missile locks acquired before the cloak')
    frames(p,180);shot(p,'cloak-ambush');ck(p.evaluate('()=>eBullets.some(q=>q._ra4Ghost)&&Q.frCloak>0'),'cloaked Nyx fires actual ambush rounds')
    p.evaluate('()=>{window.nyxHp=Q.hp;pBullets.push({kind:"mg",x:Q.x,y:Q.y,vx:0,vy:0,w:12,h:20,dmg:3,t:0});}');frames(p,1);shot(p,'cloak-hit-white')
    ck(p.evaluate('()=>Q.hp<nyxHp&&Q.flash>0'),'blind gunfire damages cloaked Nyx and renders the white hit silhouette')
  ck(p.evaluate('()=>nativeBlits.ra4_fx>0&&nativeBlits.ra4_nhxsb_g_2>0&&nativeBlits.ra4_fchgc_2>0'),'generated launchers, rockets, wakes, nova and actual palette cells draw through game canvas')
  ck(p.evaluate('()=>Object.keys(nativeBlits).some(k=>k.includes("impact_imminent"))'),'original asterisk warning art renders during charges')
  # Real player gunfire against independently shootable rocket/helix.
  p.evaluate(RESET);p.evaluate("""()=>{window.Q=R.ships[3];rg4Attack(Q,R,G,'rockets');Q.rg4.act.locked=true;Q.rg4.act.target={ref:player,key:'yuri'};Q.rg4.act.phase='fire';Q.rg4.act.t=0;rg4AttackTick(Q,R,G,.01);window.rocket=eBullets.find(q=>q._ra4Rocket);rocket.x=player.x+60;rocket.y=player.y-85;pBullets.push({kind:'mg',x:rocket.x,y:rocket.y,vx:0,vy:0,w:12,h:20,dmg:9,t:0});}""");frames(p,1)
  ck(p.evaluate('()=>rocket.dead||!eBullets.includes(rocket)'),'ordinary player bullets intercept Kaia missiles in the native update')
  p.evaluate(RESET);p.evaluate("""()=>{window.Q=R.ships[4];ra4Helix(Q,G,{a:Math.PI/2});window.ball=G.ord[0];pBullets.push({kind:'mg',x:ball.x,y:ball.y,vx:0,vy:0,w:12,h:20,dmg:20,t:0});}""");frames(p,1)
  ck(p.evaluate('()=>ball.dead'),'ordinary gunfire destroys Jace helix before detonation')
  p.evaluate(RESET);p.evaluate("""()=>{G.gang=false;rg4Attack(R.ships[3],R,G);}""");shot(p,'personal-rocket-box')
  ck(p.evaluate('()=>G.rebelBoxes[0]?.key==="kaia"&&retinaBossTargets(B).some(p=>p.kind==="support")'),'generated Kaia box is a real hittable missile-targetable enemy cache')
  p.evaluate("""()=>{window.box=G.rebelBoxes[0];pBullets.push({kind:'mg',x:box.x,y:box.y,vx:0,vy:0,w:10,h:16,dmg:9,t:0});}""");frames(p,1)
  ck(p.evaluate('()=>box.dead&&!R.ships[3].rg4.supply'),'actual gunfire destroys the enemy cache before pickup')
  p.evaluate(RESET);p.evaluate('()=>{G.gang=false;G.releaseAt=G.age;for(const q of R.ships){q.rg4.cd=0;q.rg4.gunCd=0;}window.naturalAt=G.age;}')
  for i in range(48):
   frames(p,30)
   if i==0:shot(p,'natural-ability-pickup')
   if i==16:shot(p,'natural-dogfight')
  ck(p.evaluate('()=>R.ships.every(q=>G.events.some(e=>e.event==="personalBoxCollected"&&e.pilot===q.key))'),'all five Rebels naturally acquire their own generated ability boxes')
  ck(p.evaluate('()=>R.ships.every(q=>G.events.some(e=>e.event==="specialRelease"&&e.pilot===q.key&&e.t>=naturalAt))'),'live encounter scheduler releases every requested pilot special')
  # Every survivor scene uses live radio identities, including Voss's Rook correction.
  for scanner,dead in [('kaia',[]),('nyx',['kaia']),('jace',['kaia','nyx']),('rook',['kaia','nyx','jace']),('voss',['kaia','nyx','jace','rook'])]:
   p.evaluate(RESET);p.evaluate('(dead)=>{for(const q of R.ships)if(dead.includes(q.key)){q.dead=true;q.hp=0;}G.gang=true;G.rescueDone=false;rg4RescueStart(B,G);}',dead)
   ck(p.evaluate('(k)=>G.scanner===k&&G.scene.lines.filter(q=>REBEL_KEYS.includes(q.who)).every(q=>ra4Alive(R.ships.find(v=>v.key===q.who)))',scanner),scanner+' fallback assigns only surviving Rebel portrait speakers')
   p.evaluate('()=>{const s=G.scene;s.i=s.lines.findIndex(q=>q.event==="scan");s.t=1.6;s.age=18;rg4SceneEvent(B,G,s,s.lines[s.i]);}');frames(p,1);shot(p,'scanner-'+scanner)
  # Let the entire nine-line Rook/Voss rescue run in the real clock.
  p.evaluate(RESET);p.evaluate("""()=>{R.ships.filter(q=>['kaia','nyx','jace'].includes(q.key)).forEach(q=>{q.dead=true;q.hp=0;});G.gang=true;G.rescueDone=false;rg4RescueStart(B,G);window.startScroll=_stage6SkyScroll;window.linesSeen=new Set();}""")
  for i in range(180):
   frames(p,20);p.evaluate('()=>{if(G.scene)linesSeen.add(G.scene.lines[G.scene.i]?.text);}');
   if not p.evaluate('()=>!!G.scene'):break
  ck(p.evaluate('()=>!G.scene&&linesSeen.size===9&&G.events.some(q=>q.event==="rescueComplete")'),'all nine Rook/Voss dialogue beats complete without skipping')
  ck(p.evaluate('()=>_stage6SkyScroll!==startScroll'),'world scroll continues during protected dialogue')
  shot(p,'combat-resumed')
  report['draws']=p.evaluate('()=>nativeBlits');report['events']=p.evaluate('()=>G.events');report['errors']=errors;ck(not errors,'zero page and console errors');browser.close()
finally:stop()
(O/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('RESULT',sum(c['ok'] for c in report['checks']),'/',len(report['checks']),flush=True)
sys.exit(any(not c['ok'] for c in report['checks']))
