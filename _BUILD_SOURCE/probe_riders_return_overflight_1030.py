from pathlib import Path
import sys,http.server,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/returns';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'returns-checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole'});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.releaseAt=999;G.scene=null;G.rescueDone=true;window.S=rr26State(G);S.wall={hits:0,pulse:0};S.returns=[];for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;}window.target=R.ships.find(q=>q.key==='voss');target.x=240;target.y=150;window.hp=target.hp;window.calls=0;const damage=rr26Damage;rr26Damage=function(){calls++;return damage.apply(this,arguments);};rr26Reflect(G,{x:target.x,y:target.y+160,r:12});S.wall=null;window.orb=S.returns[0];window.trace=[];}""")
  ck('All17 authored depth levels and native teal frames load',p.evaluate('Object.values(RR75_ART).every(a=>XART.rdy(a.key))'))
  for i in range(70):
   p.evaluate('()=>{rr26WallTick(G,1/60);trace.push({x:orb.x,y:orb.y,size:orb._rr75?.size,phase:orb._rr75?.phase,live:S.returns.includes(orb),calls});}')
   if i in [18,26,42]:p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/f'teal-overflight-{i}.png'))
  q=p.evaluate('({trace,events:RR75.events,calls,hp,targetHP:target.hp,orb,draws:{orb:RR75.orbs,shadow:RR75.shadows},allies:s6Wing.ships.length})')
  t=q['trace'];cross=[v for v in t if v['phase']=='overflight'];ck('The reflected ball survives contact and keeps travelling behind the target',len(cross)>8 and any(v['live']and v['y']<150-40 for v in cross))
  ck('Native reflected damage is attempted exactly once',q['calls']==1,q['calls']);ck('The contact still deals its original12HP damage',abs(q['hp']-q['targetHP']-12)<.001,[q['hp'],q['targetHP']])
  ck('Depth shrinks continuously after the flyover',all(b['size']<=a['size']+.001 for a,b in zip(cross,cross[1:])))
  ck('The ball reaches the far edge before retiring',any(e['event']=='edge-exit'and e['y']<0 for e in q['events']),q['events'])
  ck('Both the shadow and foreground orb are actually drawn',q['draws']['orb']>0 and q['draws']['shadow']>0,q['draws']);ck('No return leaks after its edge exit',not q['trace'][-1]['live'])
  ck('No native browser errors',not errors,errors);(W/'returns-trace.json').write_text(json.dumps(q,indent=2));br.close()
finally:stop()
print(len(checks),'teal return checks passed')
