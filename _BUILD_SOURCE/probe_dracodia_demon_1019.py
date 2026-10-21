"""Native phase/difficulty choreography, defenses, deaths and rendered art."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import ast,base64,http.server,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_demon_1019';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&dr21Warm();}',polling=80)
  p.evaluate("""()=>{window.demonSetup=(phase,diff,type)=>{diffKey=diff;DIFF=DIFFS[diff]||DIFF;B=boss;v18Clear(B);v18Budget(B);v18Enter(B,phase,0);v18Fight(B);B.dead=B.enter=B._noHit=false;B.hp=B.maxhp=10000;B.parts.forEach(q=>{q.hp=q.maxhp=10000;q.destroyed=false;q.flash=0;});B.x=worldWidth()/2;B.y=viewTopY()+190;B._drawY=B.y;B._r30.v18.home={x:B.x,y:B.y};
   H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;
   enemies=[];eBullets=[];pBullets=[];explosions=[];particles=[];floaters=[];smokeTrails=[];sprAnims=[];fadeOuts=[];pilotFx=[];B._r30.v18.arenaPhase=phase;player.dead=player.out=false;player._dr21Death=null;player._spin=null;player._eradicated=false;player.invuln=0;player.roll=player.somer=null;player.x=worldWidth()/2;player.y=viewTopY()+viewH()-110;run.shield=0;shake=whiteBlast=0;Input.keys={};Input.mouse.down=false;
   DR21.events=[];if(type)dr21Begin(B,type);else v18StartAttack(B);window.P=B._r30.v18.attack;SC12.refresh();__bofFit();return{type:P.type,tell:P.tell,target:P.target};};
   window.demonTick=n=>{for(let i=0;i<n;i++){player.invuln=Math.max(0,player.invuln-1);if(player.roll)updateRoll(1/60);if(player.somer)updateSomersault(1/60);r30Tick(B,1/60);if(player.dead)updateDeathSpin(1/60);for(const e of enemies)if(e._d20)d20EnemyTick(e,1/60);}};
  }""")
  def setup(phase=2,diff='normal',kind='shadowAscension'):return p.evaluate('([a,b,c])=>demonSetup(a,b,c)',[phase,diff,kind])
  def tick(n):p.evaluate('demonTick',n)
  def shot(name):
   p.evaluate('()=>{shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   raw=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));(O/(name+'.png')).write_bytes(raw);return Image.open(BytesIO(raw)).convert('RGB')
  for diff in ['easy','normal','hard','furious']:
   setup(2,diff);tick(65);check(diff+' overhead cast retreats visibly',p.evaluate('P.depth<.7&&!player.dead'))
   original=p.evaluate('P.target.x');p.evaluate('player.x+=80');tick(12);check(diff+' ball follows the living pilot during charge',p.evaluate('P.target.x===player.x&&P.target.x!=='+str(original)))
   p.evaluate('P.t=P.tell+.8;player.x-=120');tick(1);check(diff+' projectile continues homing after release',p.evaluate('P.target.x===player.x&&!P.locked'))
   p.evaluate('P.t=P.tell+P.lockAt');tick(1);target=p.evaluate('JSON.stringify(P.target)');row=p.evaluate('({locked:P.locked,window:P.dodgeWindow,remaining:P.travel-(P.t-P.tell)})');check(diff+' target freezes for the final one to two seconds',row['locked'] and 1.2<=row['window']<=2 and row['remaining']>=1.2,row)
   p.evaluate('player.x+=150');tick(230);check(diff+' late lateral dodge clears the frozen aim',p.evaluate('!player.dead') and p.evaluate('JSON.stringify(P.target)')==target)
   setup(2,diff);tick(450);check(diff+' staying in depth ball triggers actual eradication death',p.evaluate('player.dead&&player._dr21Death?.kind==="shadow"'))
   setup(2,diff);p.evaluate('run.shield=5');tick(450);check(diff+' shadow ball respects native shield and hits once',p.evaluate('!player.dead&&run.shield===4'))
   for action in ['roll','somersault']:
    setup(2,diff);p.evaluate('P.t=P.tell+P.travel*.94-.04;player._rollCool=player._somerCool=0;')
    if action=='roll':p.evaluate('startRoll(1)')
    else:
     p.wait_for_function('()=>XART.rdy("ship_cole_so0")');p.evaluate('startSomersault()')
    check(diff+' native '+action+' activates its defense',p.evaluate('player.invuln>0'))
    tick(90);check(diff+' native '+action+' avoids the final projectile',p.evaluate('!player.dead&&P.hit.size===0'))
   setup(2,diff);row=p.evaluate('()=>{const a=combatWarningDraw,r=groundTargetReticleDraw;let n=0;combatWarningDraw=groundTargetReticleDraw=()=>n++;try{v18Warnings(B);P.t=P.tell+.5;v18Warnings(B);}finally{combatWarningDraw=a;groundTargetReticleDraw=r;}return n;}');check(diff+' shadow ball draws no FOV or reticle',row==0,row)
   p.evaluate('P.t=P.tell+P.travel*.985');tick(1);check(diff+' shadow ball projects larger than the whole playfield',p.evaluate('P.projectedSize*.31>viewW()'))
   for phase in [1,2]:
    setup(phase,diff,'ghostTeleport');p.evaluate('player.x=camLeftX()+65');tick(300);row=p.evaluate('({hops:DR21.events.filter(q=>q.event==="teleport").length,warning:DR21.events.find(q=>q.event==="slam-tell")?.tell})');check(f'{diff} phase{phase+1} multiple ghost feints then warned strike',row['hops']>=3 and row['warning']>=.95,row)
   setup(1,diff,'downloadRitual');p.evaluate('player.invuln=999');tick(180);row=p.evaluate('enemies.filter(e=>e._d20).map(e=>({hp:e.maxhp,source:e._d20.sourceHP,kind:e._d20.kind}))');check(diff+' downloads stay capped and use half source HP',0<len(row)<=[1,2,2,3][['easy','normal','hard','furious'].index(diff)] and all(abs(e['hp']-e['source']*.5)<=1 for e in row),row)
   setup(2,diff,'shadowAscension');tick(60);p.evaluate('v18Clear(B);B._r30.cd=999;');tick(250);check(diff+' phase cancellation prevents delayed projectile',p.evaluate('!player.dead&&!B._r30.v18.attack'))
  # Real shields / damaged pixels, not timer-only evidence.
  setup(2,'normal','codeAegis');tick(35);before=shot('shield-before');p.evaluate('B._lastPart=B.parts[1];modularHit(25)');after=shot('shield-hit');row=p.evaluate('({hp:B.hp,shield:P.shield,max:P.shieldMax,owner:B.flash,part:B.parts[1].flash})');check('Code shield absorbs without reflection and flashes owner/module',row['hp']==10000 and row['shield']==row['max']-25 and row['owner']>0 and row['part']>0 and before.tobytes()!=after.tobytes(),row)
  tick(15);check('Hit flash expires through native timers',p.evaluate('B.flash<=0&&B.parts[1].flash<=0'))
  check('Native HUD exposes finite shield mini bar',p.evaluate('bossShieldFrac(B)>0&&bossShieldFrac(B)<1'))
  setup();row=p.evaluate('()=>{v18Clear(B);d20Start(B,"armLasers");v18AttackTick(B,.05);const old=combatWarningDraw,seen=[];combatWarningDraw=function(b,q){seen.push(q);return old.apply(this,arguments);};try{d20Warnings(B);}finally{combatWarningDraw=old;}return seen.map(q=>({alert:!!q.alertOnly,field:!!q.fieldOnly}));}');check('Retained archive beams use only field warnings',len(row)>0 and all(not q['alert'] and q['field'] for q in row),row)
  for kind in ['demonJet','demonRobot','halberd']:
   setup(2,'normal','codeAegis');p.evaluate('kind=>{v18Clear(B);B._r30.cd=999;window.E=d20Enemy(kind,worldWidth()/2,viewTopY()+200,B,kind==="halberd");}',kind);tick(160)
   before=shot(kind+'-before');p.evaluate('E._d20.direct="left";hitEnemy(E,3)');after=shot(kind+'-hit');row=p.evaluate('({flash:E.flash,part:E._d20.parts[1].flash,hp:E.hp})');check(kind+' actual helper/module damage flashes visible pixels',row['flash']>0 and row['part']>0 and before.tobytes()!=after.tobytes(),row)
   tick(20);check(kind+' helper flash expires',p.evaluate('E._d20.parts[1].flash<=0'))
  setup(2,'normal','shadowAscension');p.evaluate('()=>{coopOn=true;run2.shield=0;player2.reset();player2.x=player.x;player2.y=player.y;player2.invuln=0;player2.dead=player2.out=false;}');tick(450)
  check('Co-op depth blast uses independent damage/death owners',p.evaluate('player.dead&&player2.dead&&player._dr21Death?.kind==="shadow"&&player2._dr21Death?.kind==="shadow"'));p.evaluate('coopOn=false')
  for pilot in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
   setup();p.evaluate('pilot=>{run.pilot=pilot;XART.rdy("ship_"+pilot+"_sp0");}',pilot);p.wait_for_function('pilot=>XART.rdy("ship_"+pilot+"_sp0")',arg=pilot)
   check(pilot+' contextual death captures actual aircraft',p.evaluate('()=>!!dr21Hull()'))
  p.evaluate('run.pilot="cole"')
  for phase,kind in [(0,'machineLasers'),(0,'armOrbs'),(0,'machineGrab'),(1,'ghostTeleport'),(1,'downloadRitual'),(2,'shadowAscension')]:
   setup(phase,'normal',kind);p.evaluate('player.invuln=999');tick(70);shot(kind+'-cast');tick(100);shot(kind+'-release');check(kind+' executes and paints without errors',p.evaluate('Number.isFinite(B.x)&&Number.isFinite(B.y)'))
  for kind,source in [('ice','cryo ice shard'),('laser','laser beam'),('burn','firewall'),('shadow','Dracodia shadow eradication'),('throw','Dracodia machine grab')]:
   setup();p.evaluate('source=>playerHit(source)',source);tick(25);shot('death-'+kind);check(kind+' uses actual pilot hull in contextual death',p.evaluate('kind=>player.dead&&player._dr21Death?.kind===kind&&player._dr21Death.image.width===192',kind))
  setup();row=p.evaluate('()=>{playerHit("ice");player.reset(true);player.invuln=0;playerHit();return{dead:player.dead,custom:!!player._dr21Death,spin:!!player._spin};}');check('A later ordinary death returns to the native burning spin',row['dead'] and not row['custom'] and row['spin'],row)
  setup();p.evaluate('player.invuln=999');film=[]
  for i in range(72):tick(4);film.append(shot('_film'))
  film[0].save(O/'encounter.webp',save_all=True,append_images=film[1:],duration=67,loop=0,quality=85)
  # All recorded cue routes must decode and play, with the pool warmed first.
  p.evaluate('()=>{Audio.resume();dr21Warm();}')
  for cue in ['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact','teleportIn','shadowRelease','shieldHitHeavy','shieldBreakCombat','slice','enemyIceBolt','flameThrowerStart']:
   row=p.evaluate("""async key=>{await Snd._audioCtx().resume();const a=CA15.aliases[key]||key,k=window.BOF_CHIP_PASS?.aliases[a]||a;Snd.prepare(k);await new Promise(r=>setTimeout(r,900));Snd.stopCue(k);Snd._last[k]=0;AV3.last.clear();const requested=Snd.play(key);let el=null;for(let i=0;i<200;i++){el=Snd.pools[k]?.slots.find(s=>s?.attached&&!s.el.paused&&s.el.currentTime>0)?.el;if(el)break;await new Promise(r=>setTimeout(r,10));}return{key:k,requested,playing:!!el,volume:el?.volume,ready:el?.readyState};}""",cue)
   check(cue+' recorded native audio plays',row['playing'] and row.get('ready',0)>=2 and row.get('volume',0)>0,row)
  check('All new effect banks actually blit through game canvas',p.evaluate("['ball','fade_ghost','shield','download','ice','erase'].every(k=>DR21.draws[k]>0)"),p.evaluate('DR21.draws'))
  check('No page, console, asset or draw errors',not errors,errors)
  br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors)),flush=True)
raise SystemExit(0 if all(q['passed'] for q in checks) and not errors else 1)
