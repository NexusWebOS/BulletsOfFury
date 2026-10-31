from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/nyx_retina_1029';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=999;G.rd21.fleet=null;G.rd21.next=999;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;q.x=70+q.i*60;q.y=100;}window.n=R.ships.find(q=>q.key==='nyx');n.x=400;n.y=170;ny46Cloak(n);player.x=400;player.y=440;run.bombs=40;}""")
  ck('Hidden Nyx is absent from offensive and ally target lists',p.evaluate("!_lockTargets().some(ny46Target)&&!retinaBossTargets(boss).some(ny46Target)"))
  ck('Direct hull collision skips hidden Nyx',p.evaluate("(()=>{const h=rebelSquadHitTest(boss,n.x,n.y);return !h||R.hit!==n.i})()"))
  ck('Missiles cannot reveal Nyx',p.evaluate("!rd21Reveal(n,'missile')&&n._ny46Hidden"))
  ck('All direct damage routes preserve hidden hull and parts',p.evaluate("(()=>{const hp=n.hp,parts=fr27RebelModules(n).map(p=>p.hp),total=boss.hp;for(const kind of ['mg','beam','missile','nukem','sonic']){R.hit=n.i;R.frHit='left';_dmgSrc=kind==='missile'?'missile':'bullet';_dmgBullet={kind};rebelSquadDamage(boss,99);}return n.hp===hp&&boss.hp===total&&fr27RebelModules(n).every((p,i)=>p.hp===parts[i])})()"))
  ck('Cloak suppresses hull drawing and attack starts',p.evaluate("(()=>{let draws=0;const old=ctx.drawImage;ctx.drawImage=function(){draws++};try{fr27RebelDrawShip(n)}finally{ctx.drawImage=old}rg4Attack(n,R,G);return draws===0&&!n.rg4.act})()"))
  p.evaluate("()=>{for(let i=0;i<25;i++){cycleLock();if(ny46Target(retina.target))break;}}")
  ck('Real single Retina can acquire hidden signal',p.evaluate("ny46Target(retina.target)&&retina.phase==='seek'&&n._ny46Hidden"),p.evaluate("({id:retina.target?._retinaId,phase:retina.phase,scan:NY46.scan,base:NY46.base.targets(boss).map(t=>t._retinaId),state:{hidden:n._ny46Hidden,dead:n.dead,mode:n.mode,cloak:n.frCloak}})"))
  p.evaluate("()=>{for(let i=0;i<10;i++)updateRetina(.05)}")
  ck('Completed single lock alone starts cloak burn-off',p.evaluate("!n._ny46Hidden&&n._ny46Revealing>0&&NY46.events.some(e=>e.event==='retina-reveal')"))
  ck('Burn-off still prevents weapon damage and auto-targeting',p.evaluate("(()=>{const hp=n.hp;R.hit=n.i;R.frHit=null;rebelSquadDamage(boss,99);return n.hp===hp&&!_lockTargets().some(ny46Target)})()"))
  p.evaluate(STEP,80)
  ck('Nyx becomes a legal weapon target only after full visible fade',p.evaluate("!ny46Hidden(n)&&_lockTargets().some(ny46Target)"))
  ck('Revealed hull takes native damage and white hit flash',p.evaluate("(()=>{const hp=n.hp;R.hit=n.i;R.frHit=null;rebelSquadDamage(boss,1);return n.hp<hp&&n.flash>0})()"))
  p.screenshot(path=str(W/'revealed.png'))
  p.evaluate("()=>{retina.target=null;retina.phase=null;ny46Cloak(n);n.rg4.act=null;const t=(()=>{NY46.scan++;try{return retinaBossTargets(boss).find(ny46Target)}finally{NY46.scan--}})();retinaScanAdd(t);}")
  p.evaluate("()=>{for(let i=0;i<10;i++)retinaScanTick(.05)}")
  ck('Multi-Retina also completes a legitimate reveal',p.evaluate("!n._ny46Hidden&&n._ny46Revealing>0"))
  p.evaluate(STEP,80)
  p.evaluate("()=>{retina.target=null;retina.phase=null;retinaScanClear();n.rg4.act=null;rg4Attack(n,R,G);}")
  ck('Uncovered Nyx can perform her existing attack book without self-cloaking',p.evaluate("(()=>{for(let i=0;i<30;i++)rg4AttackTick(n,R,G,1/60);return !!n.rg4.act&&!n._rd21Cloak&&!ny46Hidden(n)})()"))
  ck('Native recloak restores immunity and prevents ally tracking',p.evaluate("(()=>{n.rg4.act.phase='cloak';rg4AttackTick(n,R,G,1/60);const a=s6Wing.ships[0];const t=(()=>{NY46.scan++;try{return retinaBossTargets(boss).find(ny46Target)}finally{NY46.scan--}})();a.target=t;rebelSquadTick(boss,1/60);return ny46Hidden(n)&&a.target!==t&&!_lockTargets().some(ny46Target)})()"))
  ck('Other Riders remain targetable',p.evaluate("retinaBossTargets(boss).some(t=>String(t._retinaId).startsWith('rook'))"))
  ck('Stage X is outside the new rule',p.evaluate("(()=>{run._gp4StageX=true;const on=ny46Own(n);run._gp4StageX=false;return !on})()"))
  ck('No native JavaScript errors',not errors,errors);b.close()
finally:stop()

