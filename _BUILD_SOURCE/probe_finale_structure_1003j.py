"""Latest integration: real three-encounter flow, persistent forms, whole rebels, live radio."""
from pathlib import Path
import json,base64,http.server,sys
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/('_shots/live_dialogue_1003j' if '--radio' in sys.argv else '_shots/finale_structure_1003j');O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
TSET=(R/'_BUILD_SOURCE/probe_teamscene_1002.py').read_text(encoding='utf-8').split('SETUP = r"""')[1].split('"""')[0]
report={'checks':[],'forms':[],'screens':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('PASS ' if v else 'FAIL ')+name,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(6)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(name)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  if '--review' in sys.argv:
   p.goto(f'http://127.0.0.1:{port}/_shots/finale_structure_1003j/review.html',timeout=120000)
   p.screenshot(path=str(O/'review-page.png'))
   for label,mode in [('Full finale',0),('Ghost fight',1),('Dracula fight',2),('Rebel encounter',-1)]:
    p.get_by_role('button',name=label,exact=True).click()
    p.wait_for_function('()=>document.querySelector("#status").textContent==="Encounter ready."',timeout=120000)
    # Read state in the frame realm, where game lexical globals live.
    actual=p.locator('#arena').element_handle().content_frame().evaluate('()=>({enc:j3State(boss)?.encounter,rebel:!!boss?._rebels})')
    ck(actual.get('rebel',False) if mode<0 else actual.get('enc')==mode,label+' selects correct encounter')
   ck(not errors,'review page and playable buttons have no browser errors')
   (O/'review-checks.json').write_text(json.dumps({'checks':report['checks'],'errors':errors},indent=2));browser.close();sys.exit(any(not c['ok'] for c in report['checks']))
  p.evaluate('()=>r30Warm()');p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(CWD_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000)
  if '--debug' in sys.argv:
   p.evaluate(TSET,{'pilot':'yuri'});p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;}')
   for _ in range(35):
    frames(p,30)
    if p.evaluate('()=>fb2TalkActive()'):break
   p.evaluate('()=>{window.holdJ=Input.hold;Input.hold=function(s,a){return a==="right"||holdJ.apply(this,arguments)}}')
   expr='()=>({x:player.x,sky:_stage6SkyScroll,flight:furyFlightTime,ctrl:s6OpeningControlsLocked(),choice:s6Wing?.choice,route:s6Wing?.route,t:fb2Talk?.t,idx:fb2Talk?.i,live:BOFCinematicDirector.live,game:state})'
   print('BEFORE',p.evaluate(expr),flush=True);frames(p,40);print('AFTER',p.evaluate(expr),flush=True)
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{j3Encounter(B,2);B._r30.mode="fight";B.enter=false;}')
   for _ in range(6):
    frames(p,180);print('DRACULA',p.evaluate('()=>({mode:B._r30.mode,J:j3State(B),attack:B._r30.attack?.type,cd:B._r30.cd})'),flush=True)
   browser.close();sys.exit(0)
  if '--radio' not in sys.argv:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
   p.evaluate('()=>{B.enter=true;B.y=-170;window.music=[];const m=bossPhaseMusic;bossPhaseMusic=function(s,n){music.push([s,n]);return m.apply(this,arguments)};}')
   frames(p,80);shot(p,'01-normal-drone')
   ck(p.evaluate('()=>j3State(B).encounter===0&&B._r30.mode==="arrival1003j"&&B.enter'),'normal drone arrives before mutation')
   frames(p,175);shot(p,'02-mutation')
   ck(p.evaluate('()=>B._r30.mode==="takeover"&&fmcGauge(B).charge===-1'),'mutation has no eight-life fill')
   frames(p,200);shot(p,'03-mutated-drone')
   ck(p.evaluate('()=>r30Live(B)&&j3State(B).encounter===0&&B.maxhp===4100&&r30Parts(B).length===3'),'first fight is the 4100 HP modular mutated drone')
   p.evaluate('()=>{r30Clear(B);B._lastPart=B.parts[0];modularHit(B.hp+1);}');frames(p,420);shot(p,'04-ghost')
   ck(p.evaluate('()=>j3State(B).encounter===1&&B.parts.length===1&&B.maxhp===4715&&!j3State(B).visited.length'),'second fight is the ghost with its own complete HP pool')
   ck(p.evaluate('()=>{const seen=[];for(let i=0;i<8;i++){r30Attack(B);seen.push(B._r30.attack.type);}B._r30.attack=null;return !seen.some(k=>["knight","chopper","furnace","ball"].includes(k));}'),'ghost never takes Dracula transformations')
   frames(p,45);p.evaluate('()=>{B._lastPart=B.parts[0];modularHit(B.hp+1);}');frames(p,355);shot(p,'05-dracula-arrival')
   ck(p.evaluate('()=>j3State(B).encounter===2&&j3State(B).mimic===null&&B._r30.mode==="coronation1003j"&&r30Parts(B).some(v=>v.key==="colossus_body")'),'third encounter reveals approved Dracula body and arms')
   for i in range(8):
    p.evaluate('(i)=>B._r30.t=.3+i*.5+.2',i);shot(p,'fill-'+str(i+1))
   ck(p.evaluate('()=>{const cols=[];for(let i=0;i<8;i++){B._r30.t=.3+i*.5+.2;const g=fmcGauge(B);cols.push(g.color);if(Math.abs(g.frac-.5)>.001)return false;}return new Set(cols).size===8}'),'Dracula gauge fills eight times in eight colors')
   frames(p,80);shot(p,'06-dracula-fight')
   ck(p.evaluate('()=>music.map(x=>x[1]).join(",")==="1,2,3"'),'three separate encounters select phase music 1, 2 and 3')
   # Natural transformation after Dracula's own arm/tentacle attacks.
   for _ in range(50):
    frames(p,30)
    if p.evaluate('()=>j3State(B).mimic===0&&r30Live(B)'):break
   ck(p.evaluate('()=>j3State(B).mimic===0&&j3State(B).encounter===2'),'Dracula naturally enters first copied form')
   for _ in range(650):
    frames(p,60,'r30Tick(B,1/60);eBullets.length=0;S81003.beams.length=0;')
    if p.evaluate('()=>j3State(B).visited.length===8'):break
   ck(p.evaluate('()=>j3State(B).visited.join(",")==="0,1,2,3,4,5,6,7"&&B._r30.history.filter(e=>e.event==="draculaReturn").length>=7'),'all eight transformations are reachable in natural order without forced form changes')
   for i in range(8):
    p.evaluate('(i)=>{j3Mimic(B,i);B._r30.mode="fight";B._r30.cd=99;B.enter=false;powerups=[];}',i)
    d=p.evaluate('()=>({id:f1003bDef(B).id,hp:B.maxhp,book:f1003bDef(B).book,parts:r30Parts(B).length})');report['forms'].append(d);shot(p,f'mimic-{i+1}-{d["id"]}')
    ck(d['parts']>=3,f'{d["id"]}: independent authored modules')
    for a,attack in enumerate(d['book']):
     p.evaluate('(a)=>{j3Clear(B);j3State(B).attacks=0;B._r30.seq=a;r30Attack(B);window.PJ=B._r30.attack;window.peakJ=0;}',a)
     taken=False
     for _ in range(140):
      frames(p,5)
      status=p.evaluate('()=>{peakJ=Math.max(peakJ,eBullets.length+S81003.beams.length);return {same:B._r30.attack===PJ,u:PJ.t-PJ.tell,phase:PJ.k1003?.phase}}')
      if not taken and (status['u']>.2 or status.get('phase')=='slashTell'):
       shot(p,f'mimic-{i+1}-{attack}');taken=True
      if not status['same']:break
     ck(p.evaluate('()=>B._r30.attack!==PJ&&B._r30.cd>0&&r30Parts(B).every(v=>Number.isFinite(v.x+v.y+v.rot))'),f'{d["id"]}: {attack} completes and recovers')
    # A real projectile uses live module hit geometry; damage persists on return.
    p.evaluate('()=>{j3Clear(B);B._r30.cd=99;const v=r30Parts(B).find(v=>v.p.id!=="core"&&v.p.id!=="rotor");window.partJ=v.p;window.hpJ=B.hp;window.partHPJ=v.p.hp;pBullets.push({kind:"mg",_chaingun:true,x:v.x,y:v.y,vx:0,vy:0,w:6,h:10,dmg:12,t:0});}')
    frames(p,1)
    ck(p.evaluate('()=>B.hp<hpJ&&partJ.hp<partHPJ'),f'{d["id"]}: real projectile damages visible module and health')
    ck(p.evaluate('(i)=>{B._lastPart=partJ;modularHit(partJ.hp+1);const hp=B.hp;j3Morph(B,"home");j3Home(B);j3Mimic(B,i);B._r30.mode="fight";B.enter=false;return B.hp===hp&&B.parts.includes(partJ)&&partJ.destroyed&&Math.abs(fmcGauge(B).frac-hp/B.maxhp)<1e-8;}',i),f'{d["id"]}: damaged HP and destroyed module persist across transformations')
   # Drain every remaining life through damage and let the real ending finish once.
   p.evaluate('()=>{window.scoreBefore=run.score;}')
   for i in range(8):
    p.evaluate('(i)=>{j3Mimic(B,i);B._r30.mode="fight";B.enter=false;B._lastPart=B.parts[0];modularHit(B.hp+1);}',i)
    if i<7:ck(p.evaluate('()=>!B._r30.rewarded&&state===GS.PLAY&&!bossDefeated'),f'life {i+1} cannot end campaign early')
   frames(p,960)
   ck(p.evaluate('()=>B._r30.rewarded&&B._r30.mode==="done"&&run._trueFinaleCleared&&state===GS.STAGECLEAR'),'all eight Dracula lives lead to the single portal/reunion reward')
  # Stage 6 team scene: world keeps updating, protected combat stays locked.
  for pilot in ['yuri','cole']:
   p.evaluate(TSET,{'pilot':pilot});p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;H3.ending=null;fb2Talk=null;B=null;}')
   for _ in range(35):
    frames(p,30)
    if p.evaluate('()=>fb2TalkActive()'):break
   ck(p.evaluate('()=>fb2TalkActive()'),pilot+': reaches natural Cole dialogue')
   p.evaluate('()=>{window.beforeJ={i:fb2Talk.i,x:player.x,sky:_stage6SkyScroll,t:AV3.clock,bombs:run.bombs};window.holdJ=Input.hold;Input.hold=function(s,a){return a==="right"||holdJ.apply(this,arguments)};}')
   p.keyboard.down('KeyZ');p.keyboard.down('Enter');frames(p,40);p.keyboard.up('KeyZ');p.keyboard.up('Enter')
   ck(p.evaluate('()=>player.x>beforeJ.x&&_stage6SkyScroll>beforeJ.sky&&AV3.clock>beforeJ.t'),pilot+': flight, world update and sky continue during dialogue')
   ck(p.evaluate('()=>state===GS.PLAY&&fb2TalkActive()&&fb2Talk.i===beforeJ.i&&eBullets.length===0&&pBullets.length===0&&run.bombs===beforeJ.bombs'),pilot+': combat stays protected and dialogue unskippable')
   p.evaluate('()=>Input.hold=holdJ');shot(p,'radio-moving-'+pilot)
   p.evaluate('()=>window.demoJ={shots:0,release:false};')
   for _ in range(320):
    frames(p,30,'updatePlay(1/60);if(fb2Talk?.demo){demoJ.shots=Math.max(demoJ.shots,fb2Talk.demo.fired);demoJ.release=demoJ.release||!!fb2Talk.demo.released;}drawWorld(1/60);')
    if p.evaluate('()=>s6Wing?.choice&&!fb2TalkActive()'):break
   ck(p.evaluate('()=>state===GS.PLAY&&s6Wing?.choice&&!fb2TalkActive()'),pilot+': full timed conversation finishes and releases route choice')
   if pilot=='cole':ck(p.evaluate('()=>demoJ.shots>0&&demoJ.release&&run.weapon===1&&run.wlevel===3'),'Cole scripted demonstration completes and restores loadout in the moving world')

  p.evaluate(SETUP,{'stage':6,'diff':'furious'});p.evaluate('()=>{fb2Talk=null;spawnBoss("rebelsquad");window.B=boss;B._be=null;B.enter=false;}');frames(p,250);shot(p,'rebels-intro')
  ck(p.evaluate('()=>h3RebelIntro()&&B._rebels.ships.every(q=>!q.shield&&!q.shieldMax)'), 'rebel arrival has no shields')
  p.evaluate('()=>{window.skyJ=_stage6SkyScroll;window.timeJ=AV3.clock;}');frames(p,30)
  ck(p.evaluate('()=>_stage6SkyScroll>skyJ&&AV3.clock>timeJ&&eBullets.length===0'),'rebel dialogue runs in a live protected world')
  for _ in range(150):
   frames(p,30)
   if p.evaluate('()=>B._rebels.frIntro.done'):break
  ck(p.evaluate('()=>B._rebels.frIntro.done&&!B._noHit&&state===GS.PLAY'),'full rebel introduction finishes naturally and starts combat')
  p.evaluate('()=>{const R=B._rebels;R.frIntro.done=true;for(const q of R.ships){q.mode="fight";q.warp=0;q.frCloak=0;q.hp=q.max;for(const m of fr27RebelModules(q))m.hp=0;}R.hit=0;R.frHit="left";window.hullHP=R.ships[0].hp;rebelSquadDamage(B,20);}')
  ck(p.evaluate('()=>B._rebels.ships[0].hp===hullHP-20&&fr27RebelModules(B._rebels.ships[0]).every(m=>m.hp>0)'), 'wing hit damages hull without deleting a wing')
  p.wait_for_function('()=>XART.rdy("fr27_rebel_pitch")&&REBEL_SHIPS.every((k)=>XART.rdy("rr_ship_"+k))',timeout=60000)
  for f in range(4):
   p.evaluate('(f)=>{B._rebels.ships.forEach((q,i)=>{q.x=camLeftX()+60+i*(viewW()-120)/4;q.y=180+i%2*140;q.frSomersault=true;q.evadeT=.38*(1-(f+.2)/4);q.rfHeading=null;q.flash=.13;q.t=2;});}',f);shot(p,'rebels-damaged-pitch-'+str(f))
  p.evaluate('()=>{const R=B._rebels;R.ships.forEach(q=>{q.dead=q.i!==0});rf28Fallen(B,R,R.ships[1]);}');frames(p,1)
  ck(p.evaluate('()=>B._rebels.ships.every(q=>!q.shield&&!q.shieldMax)'), 'last rebel cannot regenerate a shield')
  ck(not errors,'no page or console errors');report['errors']=errors
  (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[c['name'] for c in report['checks'] if not c['ok']],'errors':errors}),flush=True)
  browser.close()
finally:stop()
sys.exit(any(not c['ok'] for c in report['checks']) or bool(errors))
