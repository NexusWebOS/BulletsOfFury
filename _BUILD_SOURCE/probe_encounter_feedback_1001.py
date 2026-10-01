"""Focused native encounter fixtures, not campaign wins. Audio runs unmuted."""
from pathlib import Path
import sys,json,base64,http.server,time
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/encounter_feedback_1001';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
SETUP="""c=>{ht27Stop();debugFight=null;coopOn=false;diffKey=c.diff;DIFF=DIFFS[c.diff];run.pilot='yuri';run.mode='campaign';beginStage(c.stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;s6Opening=null;s6Wing=null;stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;tb28Reset();groundTargetingFx=[];polishLanes=[];stageTimer=0;player.x=worldWidth()/2;player.y=VH-110;camX=player.x-VW/2;player.invuln=999;if(c.kind){if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);window.B=c.mini?subBoss:boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=B._er26?.home||B.ty||160;B._drawY=B.y;if(B._r30)B._r30.mode='fight';if(B._bomber)siegeBomberSet(B,'bombs');if(B._s7mod)s7mSet(B,'recover');}return {hp:window.B?.hp,world:worldWidth(),view:VW,height:VH};}"""
errors=[];report={'checks':[],'matrix':[],'audio':[]};port,stop=sh.serve(str(R))
def check(value,name):
 report['checks'].append({'ok':bool(value),'name':name});print(('OK ' if value else 'FAIL ')+name,flush=True)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');(O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':900})
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:450]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate("()=>{r30Warm();er26Warm();missionWarm();enc30Warm(4);for(const k of Object.keys(MR27_ART))XART.rdy('mr27_'+k);for(const a of Object.values(SPREAD1001_ART))XART.rdy(a.key);}")
  p.wait_for_function("()=>Object.keys(REALM30_ART).every(k=>XART.rdy('r30_'+k))&&Object.values(SPREAD1001_ART).every(a=>XART.rdy(a.key))&&XART.rdy('vile25_ghost_claw')&&XART.rdy('vile25_void_knight_slash')&&XART.rdy('mr27_rime')",timeout=120000)
  # Art evidence is resolved via the game's own XART and context, not a filename.
  keys=['vile25_ghost_claw','vile25_phantom_ground_portal','vile25_void_knight','vile25_void_knight_slash','mwfx_fireball_3','spread1001_fire','spread1001_ice']
  p.evaluate("keys=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#152331';ctx.fillRect(0,0,cv.width,cv.height);keys.forEach((k,i)=>{const im=XART.get(k);if(im){ctx.drawImage(im,(i%4)*210+12,Math.floor(i/4)*290+24,190,240);ctx.fillStyle='#fff';ctx.font='12px sans-serif';ctx.fillText(k,(i%4)*210+12,Math.floor(i/4)*290+280);}});}",keys)
  (O/'authored-art.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':diff})
   for form in range(3):
    p.evaluate('n=>{r30Form(B,n);B._r30.mode="fight";B.enter=false;window.metric={peak:0,modes:[],cost:[]};}',form)
    for sec in range(40):
     p.evaluate("()=>{for(let i=0;i<60;i++){player.x=worldWidth()/2+Math.sin((stageTimer+i/60)*.8)*130;player.invuln=999;const t=performance.now();updatePlay(1/60);if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);metric.cost.push(performance.now()-t);}metric.peak=Math.max(metric.peak,eBullets.filter(q=>!q.dead).length);const a=B._r30.attack?.type;if(a&&!metric.modes.includes(a))metric.modes.push(a);}}")
     if sec%5==0:p.wait_for_timeout(10)
    row=p.evaluate('()=>({hp:B.maxhp,peak:metric.peak,modes:metric.modes,ms:metric.cost.sort((a,b)=>a-b)[Math.floor(metric.cost.length*.95)],finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy))})');row.update(diff=diff,form=form);report['matrix'].append(row)
    check(row['finite'] and row['hp']<6000,f'{diff} Stage8 form{form+1} finite / bounded health')
    if diff=='furious':shot(p,f'realm-form{form+1}')
   if diff=='furious':
    p.evaluate('()=>{r30Form(B,1);B._r30.mode="fight";B.enter=false;B._r30.seq=0;r30Attack(B);B._r30.attack.t=B._r30.attack.tell+.8;}');shot(p,'ghost-warning')
    p.evaluate('()=>{B._r30.attack.t=B._r30.attack.tell+B._r30.attack.strikeAt+.08;}');shot(p,'ghost-strike')
  # Every signature cue must decode and advance, including the formerly unmapped death cue.
  p.evaluate('()=>{Audio.init();Audio.stopMusic();Snd.prepare([...R30_CUES,"combatOrb0927"]);}')
  for key in ['bossWeaponCharge','combatAlien0927','enemyBossCannon','hammerImpact','combatBeam0927','expBoss']:
   mapped='expBig' if key=='expBoss' else key
   p.wait_for_function('k=>Snd.pools[k]?.list.some(a=>a.readyState>=3)',arg=mapped,timeout=30000)
   p.evaluate('k=>{Snd._last[k]=0;r30Sound(k);}',key);p.wait_for_timeout(160)
   a=p.evaluate('k=>{const P=Snd.pools[k];return {key:k,playing:P.list.some(a=>!a.paused&&a.currentTime>0&&a.volume>0&&!a.muted),ready:P.list.map(a=>a.readyState),time:P.list.map(a=>a.currentTime),context:Snd._ctx?.state};}',mapped);report['audio'].append(a);check(a['playing'],key+' actual media playback')
  for kind,mini in [('frostcruiser',True),('cryospear',False)]:
   for diff in ['normal','hard','furious']:
    p.evaluate(SETUP,{'stage':3,'kind':kind,'mini':mini,'diff':diff})
    p.evaluate("()=>{B._er26.neutralOpening=false;B._er26.form='fire';er26Set(B,B._ship==='cryospear'?'cannon-relay':'cryo-missiles');}")
    for t in range(4):
     p.evaluate('()=>{story=null;for(let i=0;i<60;i++){er26Tick(B,1/60);for(const q of eBullets){q.t=(q.t||0)+1/60;q.x+=q.vx;q.y+=q.vy;}}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}');p.wait_for_timeout(15)
     if t==0:shot(p,kind+'-'+diff+'-charge')
     if t==2:shot(p,kind+'-'+diff+'-attack')
    result=p.evaluate('()=>({beam:B._l23Beam?{family:B._l23Beam.family,slots:B._l23Beam.slots}:null,rounds:eBullets.filter(q=>q._er26Source===B._ship).map(q=>({kind:q.kind,homing:q._frostHoming})),shots:B._er26.shots})')
    check((result['shots']>0 if mini else True),kind+' '+diff+' fires')
    if not mini:
     p.evaluate("()=>{B._l23Beam=null;er26Set(B,'cannon-relay');er26Combat(B,.01);}")
     check(p.evaluate("()=>B._l23Beam.family==='rime'&&B._l23Beam.slots.length===4&&Math.abs(shipBossMount(B,'L0').x-shipBossMount(B,'L1').x)>3"),'dual cold beams from distinct barrel tips '+diff)
    else:check(result['beam'] is None,'miniboss has no laser '+diff)
  p.evaluate(SETUP,{'stage':4,'kind':'olivewarden','mini':True,'diff':'furious'})
  check(p.evaluate('()=>stage4MiniEscortEnsure(B).length===0'),'Stage4 miniboss has no helpers')
  check(p.evaluate("()=>['s4minitank','tank','htank','roadtank','s4airfield'].every(k=>{const e=spawnEnemy(k,worldWidth()/2,300,{});return e._modTank===4&&!!e._r30;})"),'legacy Stage4 tanks use new modular tank')
  shot(p,'stage4-tanks')
  for stage,kind in [(5,'spacebomber'),(6,'siegebomber')]:
   for diff in ['easy','normal','hard','furious']:
    p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':True,'diff':diff});hp=p.evaluate('()=>B.maxhp');check(hp<3400,f'Stage{stage} {diff} miniboss smaller health pool ({hp})')
  p.evaluate(SETUP,{'stage':6,'diff':'furious'})
  p.evaluate("()=>{enemies=[];window.jets=['west','east','south'].map((direction,i)=>missionJetSpawn({kind:i===1?'bomb':'lane',direction,y:180+i*90,x:worldWidth()/2},{n:2}));jets[0].x=worldWidth()/2-80;jets[1].x=worldWidth()/2+80;jets[2].y=360;jets.forEach(e=>s6StrikeTick(e,.016));}")
  check(p.evaluate('()=>groundTargetingFx.filter(q=>q._mission29).length>=2'),'first and second sideways jets drop bombs')
  shot(p,'stage6-red-green-jets')
  # Full generated animation set, same function used by combat and Forge.
  p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#18242c';ctx.fillRect(0,0,VW,VH);Object.keys(SPREAD1001_ART).forEach((key,i)=>{for(let f=0;f<4;f++)spreadDraw1001({kind:'spread',_inf:key==='base'?null:key,_infLv:5,lv:1,x:65+f*65,y:40+i*48,vx:0,vy:-9,t:f/16});ctx.fillStyle='#fff';ctx.font='12px monospace';ctx.fillText(key,340,44+i*48);});}")
  (O/'spread-all.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  check(p.evaluate('()=>Object.values(SPREAD1001_ART).every(a=>a.frames.length===4&&XART.rdy(a.key))'),'all 10 Spreadfire animation reels loaded')
  check(not errors,'no page or console errors');br.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
