from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_demon_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(b.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');assert advance(p,"boss._r30.mode==='fight'",100,16)
  p.evaluate('()=>{v18Clear(boss);eBullets.length=0;player.invuln=1e6;rd72Start(boss,"missiles");}');p.evaluate(STEP,82)
  before=p.evaluate('()=>{window.trackedMissile=eBullets.find(q=>q._rd72Missile);if(!trackedMissile)throw Error("No actual launched missile");player.x=trackedMissile.x;player.y=Math.min(VH-30,trackedMissile.y+100);run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);player.fireCd=0;Input.keys.j=true;return{x:trackedMissile.x,y:trackedMissile.y,playerY:player.y,interceptable:enemyOrdnanceCanIntercept(trackedMissile)};}')
  p.evaluate(STEP,12);after=p.evaluate('({dead:trackedMissile.dead,removed:!eBullets.includes(trackedMissile),y:trackedMissile.y,beam:pBullets.some(q=>q.kind==="beam"),playerDead:player.dead})');q=dict(name='A real player-fired laser intercepts the purple missile without losing shootability',passed=bool(before['interceptable']and(after['dead']or after['removed'])and after['beam']and not after['playerDead']and not errors),data=dict(before=before,after=after,errors=errors))
  (W/'ordnance-check.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True);assert q['passed'];a=json.loads((W/'checks.json').read_text());a=[r for r in a if r['name']!=q['name']]+[q];(W/'checks.json').write_text(json.dumps(a,indent=2));b.close()
finally:stop()
