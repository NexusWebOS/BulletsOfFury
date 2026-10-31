from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/sewer_rescue_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,d if not v else'')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=7;stageLoadBegin(7)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:7,role:'boss',kind:'sludgeemperor'},{pilot:'cole',record:false});spawnBoss('sludgeemperor');debugFight.spawned=true;bossActive=true;warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=boss;}")
  for i in range(22):p.evaluate(STEP,30)
  p.evaluate("()=>{debugFight=null;run.mode='campaign';const M=B._s7mod;for(const q of M.parts)q.hp=0;for(const q of M.er28Canisters||[]){q.hp=0;q.dead=true}M.shield=0;M.core=10;B.hp=10;s7mSet(B,'recover');mapScroll=levelScrollRange()-1800;drawWorld(0);s7mHit(B,11,B.x,B.y,'core');fr27Exit(B,1/60);window.E=B._s7mod.frExit;window.Q=E.sc86;window.C=Q.sr93}")
  d=p.evaluate("""()=>{const old=run.pilot,out=[];for(const pilot of PILOTS){run.pilot=pilot.key;C.phase='form';C.t=.15;C.alarm=false;fr27Exit(B,.02);out.push({key:pilot.key,expected:'WHAT IS THAT? '+pilot.name.toUpperCase()+', NOOOO!',actual:B._s7warden.final.radio.full,who:B._s7warden.final.radio.who})}run.pilot=old;return out}""")
  ck('Decker uses every selected pilot name, including the longest names',all(q['actual']==q['expected']and q['who']=='DECKER'for q in d),d)
  p.evaluate("()=>{coopOn=true;run2.pilot='yuri';player2.reset();player2.x=460;player2.y=430;player.x=200;player.y=440;Q.source=285;C.phase='form';C.t=SR93.form-.01;C.alarm=true;fr27Exit(B,.02)}")
  ck('Both live seats are captured for portal rescue',p.evaluate("C.phase==='enter'&&C.seats.length===2"))
  p.evaluate("()=>{for(let i=0;i<45;i++)fr27Exit(B,1/60)}")
  ck('Both pilots reach the same gate and survive the collapse',p.evaluate('B._s7warden.final.shipHidden&&!player.dead&&!player2.dead&&Math.hypot(player.x-E.portalX,player.y-E.portalY)<2&&Math.hypot(player2.x-E.portalX,player2.y-E.portalY)<2'))
  p.evaluate("()=>{coopOn=false;beginStage(1);BOFCinematicDirector.cancel();setState(GS.PLAY)}");p.evaluate(STEP,3);ck('Restart cancels all rescue effects',p.evaluate('!SR93.owner&&!SR93.fx.length'))
  ck('No native browser exceptions',not errors,errors);br.close()
finally:stop()
(W/'extra-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks)
