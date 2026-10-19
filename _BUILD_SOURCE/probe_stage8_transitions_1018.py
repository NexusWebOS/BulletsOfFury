"""Full native phase fades, comms, module beam cancellation and reunion."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_pixellab_1018/transitions';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  html=(R/'index.html').read_text()
  if 'assets/stage8_pixellab_1018.js' not in html:
   html=html.replace('</body>','<script src="assets/stage8_pixellab_art_1018.js"></script><script src="assets/stage8_pixellab_1018.js"></script></body>');p.route('**/index.html',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V18!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)");p.evaluate(SETUP,dict(stage=8,diff='furious',kind='vileexistence',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}')
  p.evaluate('''()=>{playerHit=function(){};s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];player.x=worldWidth()/2;player.y=VH-65;V18.events=[];v18Enter(B,0);v18Fight(B);bossWarned=true;SC12.refresh();__bofFit();}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(60);snap('phase1-fade')
  check('old phase remains before blackout',p.evaluate('j3State(B).encounter===0&&B._r30.v18.arenaPhase===0'))
  frames(8);snap('blackout')
  check('phase2 background swaps behind full black',p.evaluate('j3State(B).encounter===1&&B._r30.v18.arenaPhase===1&&v18Fade(B)===1'))
  frames(100);snap('ghost-emerges');frames(140)
  check('ghost intro restores damage and flight',p.evaluate('B._r30.mode==="fight"&&!B.enter&&!B._noHit&&!dr5Locked()'))
  p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(68);snap('phase3-blackout');frames(100);snap('colossus-emerges');frames(140)
  check('phase3 has exactly five enabled pools',p.evaluate('j3State(B).hp.map((v,i)=>v>0?i:null).filter(i=>i!=null).join()==="0,1,2,6,8"'))
  check('new main form keeps the existing Dracodia monologue',p.evaluate('B._r30.mode==="dr5Monologue"&&!!dr5State(B).radio'))
  snap('dracodia-monologue')
  for _ in range(20):
   if p.evaluate('B._r30.mode!=="dr5Monologue"'):break
   p.evaluate('()=>{const d=dr5State(B);if(d.radio)d.radio.t=dr5TalkDuration(d.radio.text)+.05;}');frames(3)
  check('native monologue reaches damageable combat',p.evaluate('B._r30.mode==="fight"&&!B.enter&&!B._noHit'),p.evaluate('({mode:B._r30.mode,enter:B.enter,nohit:B._noHit})'))
  check('monologue cannot leak its180-second cinematic invulnerability into combat',p.evaluate('player.invuln<=.5'),p.evaluate('player.invuln'))
  frames(35);check('combat grace actually expires',p.evaluate('player.invuln<=0'),p.evaluate('player.invuln'))
  # A destroyed emitter cancels only its own active beam, leaving the other
  # cannon live. This is real modular behavior, not a disappearing overlay.
  p.evaluate('''()=>{v18Enter(B,2,6);v18Fight(B);B._r30.v18.arenaPhase=2;B._r30.v18.seq=0;v18StartAttack(B);B._r30.v18.attack.t=B._r30.v18.attack.tell;}''');frames(3)
  check('Harrier actually projects both warned fan beams',p.evaluate('B._r30.v18.beams.length===2'))
  p.evaluate('()=>{const p=B.parts.find(p=>p.id==="left");B._lastPart=p;hitBoss(p.hp+1);}');frames(3);snap('harrier-one-emitter')
  check('destroyed left emitter cancels its beam and leaves right beam active',p.evaluate('B._r30.v18.beams.length===1&&B._r30.v18.beams[0].module==="right"'))
  # The old death/return controller must still see all pools depleted once.
  p.evaluate('''()=>{v18Enter(B,2,0);v18Fight(B);const J=j3State(B);for(const id of V18.forms)if(id!==0)J.hp[id]=0;B._lastPart=B.parts[0];hitBoss(1e8);}''')
  check('final depletion reaches the established one-time death',p.evaluate('B._r30.mode==="dr5Death"&&dr5State(B).deathStarted'))
  frames(700);snap('final-death');frames(400);snap('red-return-portal');frames(850)
  check('final death red portal and reunion reach campaign clear',p.evaluate('state===GS.STAGECLEAR&&run._realmReturned&&run._trueFinaleCleared'),p.evaluate('({state,mode:B._r30.mode,returned:run._realmReturned,cleared:run._trueFinaleCleared})'))
  check('no page console drawing or asset errors',not errors,errors)
  br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps(dict(passed=data['passed'],failed=data['failed'],errors=errors)));sys.exit(bool(data['failed']))
