"""Native pixels, committed attacks, modular Furnace and actual finale reward."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];archive_fixture='--archive-fixture' in sys.argv;archive=archive_fixture or '--archive' in sys.argv;O=R/('_shots/dracodia_archive_1018/sequences' if archive else '_shots/stage8_identity_1018/sequences');O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V19!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  if archive_fixture:
   p.add_script_tag(url=f'http://127.0.0.1:{port}/_shots/dracodia_archive_1018/fixture_art.js')
   p.evaluate('''()=>{const copy=b=>({...b,frames:b.frames.map(a=>({...a,w:b.w,h:b.h,pivot:b.pivot}))});D20_ART.fx={bomb_charge:copy(ST18_ART.bomb),bomb_burst:copy(ST18_ART.impact),lightning_loop:copy(ST18_ART.impact),storm_loop:{fps:10,frames:PXV17_ART.code}};}''')
   p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/dracodia_archive_1018.js')
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{playerHit=function(){};window.v19Pixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let h=2166136261,n=0;for(let i=0;i<a.length;i++){h=Math.imul(h^a[i],16777619)>>>0;if(i%4===3&&a[i]>128)n++;}ctx.restore();return{hash:h,pixels:n};};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(phase=2,form=0,diff='normal'):
   p.evaluate(SETUP,dict(stage=8,diff=diff,kind='vileexistence',pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&(typeof D20==="undefined"||d20Warm())&&bmfReady("game")}')
   p.evaluate('''([phase,form])=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];v18Budget(B);v18Enter(B,phase,form);B._r30.v18.arenaPhase=phase;v18Fight(B);bossWarned=true;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;V19.events=[];V19.draws={};V18.events=[];SC12.refresh();__bofFit();}''',[phase,form])
  setup()
  for name in ['colossus_roar','colossus_scythe','colossus_death','infused_death','ghost_death','avatar_speech']:
   data=p.evaluate('''name=>{const frames=V19_ART.clips[name].frames,out=[];for(const a of frames){if(a.w!==320||a.h!==320||a.pivot.join()!=="160,160")throw Error('bad frame format');out.push(v19Pixels(()=>v18Cell(a,camX+240,260,320)));}return{count:frames.length,unique:new Set(out.map(q=>q.hash)).size,min:Math.min(...out.map(q=>q.pixels))};}''',name)
   check(name+' every fixed even pose renders through native drawImage',data['count']>=16 and data['unique']>=data['count']-1,data)
  # Roar and scythe read as real articulation, including their actual masks.
  p.evaluate('B._r30.v18.seq=typeof D20!=="undefined"?D20.book.indexOf("voidRoar"):1;v18StartAttack(B)');frames(90);snap('colossus-roar')
  check('main body raises its arms using the new roar bank',p.evaluate('B._r30.v18.acting==="colossus_roar"&&!!v19Acting(B)?.layers'))
  p.evaluate('B._r30.v18.attack=null;B._r30.v18.seq=typeof D20!=="undefined"?1:0;v18StartAttack(B)');frames(105);snap('colossus-scythe')
  check('scythe attack sweeps actual shoulder-mounted limb masks',p.evaluate('!!B._r30.v18.swipe&&v18Rig(B).some(v=>v.p.id!=="core"&&Math.abs(v.rot)>.1)&&v18Rig(B).every(v=>v.key.startsWith("v18_colossus"))'))
  check('Physical scythe strikes use limb contact without stray missiles or beams',p.evaluate('B._r30.v18.beams.length===0&&!eBullets.some(q=>q._finale1003b==="missile")'))
  # Native anchored Stage5 side strike, including its full committed target.
  setup(2,8);p.evaluate('''()=>{const p=gd4Create(B,8).p,h=p._hammer;h.mode='storm';h.stormHome={x:B.x,y:B.y};h.stormTarget={x:player.x,y:player.y};h.stormBounds={l:camLeftX(),r:camRightX(),top:PLAY.y+125,bottom:hammerStormFloorY()};hammerStormImpact(p);hc11BeginCounter(p,{x:player.x-60,y:PLAY.y+viewH()*.35,seat:0});window.v19Anchor={...h.hc11Counter.anchor};}''')
  frames(50);snap('hammer-side-windup');p.evaluate('player.x+=90;B._lastPart=B.parts[0];hitBoss(1)');frames(100);snap('hammer-side-strike')
  check('side strike stays committed after movement and a hit',p.evaluate('HC11.events.some(e=>e.event==="anchored-hammer-impact"&&Math.abs(e.x-v19Anchor.x)<1)'))
  check('Hammer rig has exactly body plus its real hammer, no third arm',p.evaluate('B.parts.map(p=>p.id).join()==="core,hammer"'))
  p.evaluate('''()=>{const p=gd4Create(B,8).p;hammerStormImpact(p);window.v19Columns=p._hammer.stormWaves.map(q=>({beam:q.hc11Beam,top:q.top,bottom:q.y}));}''')
  check('native Chromium columns stop halfway up the playfield',p.evaluate('v19Columns.length>0&&v19Columns.every(q=>q.beam&&Math.abs(q.top-hc11MidY())<1)'))
  # Full-sized physical parts drive native arms/core/head damage states.
  setup(2,2);frames(100)
  check('volcano retains a continuous physical arm flamethrower',p.evaluate('gd4Create(B,2).p._fz.beams.some(q=>q.kind==="flame"&&q._v19Flame)'))
  snap('volcano-flamethrower')
  p.evaluate('''()=>{const v=v19VolcanoRig(B).find(v=>v.layer==='left'),m=furnaceMuzzle(gd4Create(B,2).p,'left'),q=v19WorldPoint(v,V19_ART.volcanoMuzzles.left);window.v19MuzzleError=Math.hypot(q.x-m.x,q.y-m.y);B._lastPart=B.parts.find(p=>p.id==='left');hitBoss(1e6);}''');frames(5)
  check('fire starts at the visible muzzle and a broken arm stops it',p.evaluate('v19MuzzleError<.01&&!v19VolcanoRig(B).some(v=>v.layer==="left")&&!gd4Create(B,2).p._fz.beams.some(q=>q.kind==="flame")'))
  p.evaluate('B._lastPart=B.parts.find(p=>p.id==="right");hitBoss(1e6)');frames(120)
  check('both broken arms expose the Furnace body state',p.evaluate('gd4Create(B,2).p._fz.phase==="core"&&retinaBossTargets(B).some(q=>!q.dead)'))
  snap('volcano-core')
  p.evaluate('B._lastPart=B.parts.find(p=>p.id==="core");hitBoss(1e6)');frames(120)
  check('body destruction leaves only its independently damageable head',p.evaluate('gd4Create(B,2).p._fz.phase==="head"&&v19VolcanoRig(B).length===1&&v19VolcanoRig(B)[0].layer==="head"'))
  frames(125);snap('volcano-head-lasers')
  check('head turns and projects both lasers from its eyes',p.evaluate('Math.abs(gd4Create(B,2).p._fz._v19Head.roll)>.1&&gd4Create(B,2).p._fz.beams.filter(q=>q.kind==="eye").length===2'))
  frames(410);check('head completes a genuine full 360-degree sweep',p.evaluate('V19.events.some(e=>e.event==="volcano-full-head-turn"&&Math.abs(e.radians)>6.28)'))
  p.evaluate('B._lastPart=B.parts.find(p=>p.id==="head");hitBoss(1)');check('primary damage can hurt the detached head',p.evaluate('B.parts.find(p=>p.id==="head").hp<B.parts.find(p=>p.id==="head").maxhp'))
  # Damage and destroyed modules persist when a copy returns.
  setup(2,2);p.evaluate('''()=>{B._lastPart=B.parts.find(p=>p.id==='left');hitBoss(80);window.v19Saved={hp:B.hp,arm:B.parts.find(p=>p.id==='left').hp,body:B.parts[0].hp};j3Save(B);v18Enter(B,2,0);v18Enter(B,2,2);v18Fight(B);}''')
  check('Furnace pools and body HP persist across copied-form visits',p.evaluate('B.hp===v19Saved.hp&&B.parts.find(p=>p.id==="left").hp===v19Saved.arm&&B.parts[0].hp===v19Saved.body'))
  # A last copied form must shatter before the true Colossus death begins.
  setup(2,8);p.evaluate('''()=>{for(const id of V18.forms)j3State(B).hp[id]=0;B.hp=0;r30Break(B);}''');frames(165)
  check('last copied form shatters and reforms before the Colossus death',p.evaluate('B._r30.mode==="v19FinalReform"&&!dr5State(B).deathStarted'))
  frames(150);check('last-copy reform starts exactly one true Colossus death',p.evaluate('B._r30.mode==="dr5Death"&&dr5State(B).deathStarted&&DR5.events.filter(e=>e.event==="dracodiaFinalDeath").length===1'))
  # Authored deaths precede both full-black arena swaps and the new avatar.
  setup(0);p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(65);snap('host-death')
  check('host plays its generated collapse before fading',p.evaluate('B._r30.mode==="v19phaseDeath"&&V19.draws.infused_death>0'))
  frames(160);snap('first-blackout');check('first arena changes only behind full blackout',p.evaluate('j3State(B).encounter===1&&v18Fade(B)===1'))
  frames(240);p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(65);snap('ghost-death');frames(160);snap('second-blackout')
  check('second arena changes only behind full blackout',p.evaluate('j3State(B).encounter===2&&v18Fade(B)===1'))
  frames(240);snap('dracodia-new-avatar');check('new Dracodia avatar is wired to his actual dialogue',p.evaluate('B._r30.mode==="dr5Monologue"&&!!dr5Portrait(3,1)&&V19.draws.avatar>0'))
  for _ in range(20):
   if p.evaluate('B._r30.mode!=="dr5Monologue"'):break
   p.evaluate('()=>{const D=dr5State(B);if(D.radio)D.radio.t=dr5TalkDuration(D.radio.text)+.05;}');frames(3)
  check('dialogue restores normal combat protection timing',p.evaluate('B._r30.mode==="fight"&&!B._noHit&&player.invuln<=.5'))
  p.evaluate('''()=>{for(const id of V18.forms)j3State(B).hp[id]=id===0?B.hp:0;B._lastPart=B.parts[0];hitBoss(1e8);}''');frames(95);snap('final-colossus-agony');frames(185);snap('final-colossus-shatter')
  check('final death shatters the new body, without old-body sunbeams',p.evaluate('V19.events.some(e=>e.event==="new-colossus-shatter")&&V19.draws.colossus_death>0&&!(DR5.draws.sunbeam>0)'))
  check('final armor breaks into actual even-canvas opaque fragments',p.evaluate('B._r30.v18.shards.length>=8&&B._r30.v18.shards.every(q=>q.image.width===80&&q.image.height===80&&q.w===q.h&&D27_MODULE_DEBRIS.includes(q))'))
  frames(120);snap('armor-scattered');check('armor fragments scatter beyond the battlefield',p.evaluate('B._r30.v18.shards.some(q=>q.x<camLeftX()-q.w||q.x>camRightX()+q.w||q.y>VH+q.h)'))
  frames(330);snap('return-portal');frames(900)
  check('finale still reaches exactly one campaign clear through the red portal',p.evaluate('state===GS.STAGECLEAR&&run._realmReturned&&run._trueFinaleCleared&&DR5.events.filter(e=>e.event==="dracodiaFinalDeath").length===1'),p.evaluate('({state,mode:B._r30.mode,returned:run._realmReturned,cleared:run._trueFinaleCleared})'))
  check('no page, console, draw or missing asset errors',not errors,errors[:30]);br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['passed','failed','errors']}));sys.exit(bool(data['failed']))
