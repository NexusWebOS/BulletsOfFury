from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/nyx_firing_1029';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=999;G.rd21.fleet=null;G.rd21.next=999;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;q.x=70+q.i*60;q.y=100;}window.n=R.ships.find(q=>q.key==='nyx');n.x=400;n.y=170;ny46Cloak(n);player.x=400;player.y=440;run.bombs=40;}""")
  p.wait_for_function('()=>Object.keys(NY47_SOCKETS).every(k=>XART.rdy(k))')
  ck('Squad dispatch cannot spend a hidden Nyx attack turn',p.evaluate('(()=>{const turn=n.rg4._rd42Turn;RD42.attack(n,R,G);return !n.rg4.act&&n.rg4._rd42Turn===turn})()'))
  p.evaluate("()=>{for(let i=0;i<20;i++){cycleLock();if(ny46Target(retina.target))break;}for(let i=0;i<10;i++)updateRetina(.05)}")
  p.evaluate(STEP,80)
  ck('Retina-only discovery remains required before firing',p.evaluate('!ny46Hidden(n)'))
  p.evaluate(STEP,600)
  ck('Revealed Nyx stays visible beyond the retired seven-second timer',p.evaluate('!ny46Hidden(n)&&n._rr26Fade===0&&n._rd21Visible>990'))
  results=[]
  for angle in [.95,1.1,1.3,1.57,1.8,2.05,2.19]:
   for frame in range(8):
    q=p.evaluate("""v=>{G.rd21.fleet=null;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;}rg4Attack(n,R,G);const A=n.rg4.act;A.phase='charge';A.t=1.5;A.warm=1.8;A.a=v.a;A.from={x:camLeftX()-200,y:-200};n.t=v.f/12;rg4AttackTick(n,R,G,1/60);const calls=[],f=combatWarningDraw;combatWarningDraw=function(a,p){calls.push({x:p.x,y:p.y,angle:Math.atan2(p.ey-p.y,p.ex-p.x),len:p.len});};try{rg4Warning(n,A);}finally{combatWarningDraw=f;}const ports=[nx37Socket(n,-1),nx37Socket(n,1)];return{visible:ny47Visible(n),calls,ports,angle:A.a};}""",dict(a=angle,f=frame));results.append(q)
  ck('All charge poses stay wholly in the current visible firing region',all(q['visible']for q in results))
  ck('Both FOVs start at the exact registered muzzle on every tested heading/frame',all(len(q['calls'])==2 and all(abs(a['x']-b['x'])<1e-8 and abs(a['y']-b['y'])<1e-8 and abs(a['angle']-q['angle'])<1e-8 for a,b in zip(q['calls'],q['ports']))for q in results))
  ck('Warning spans end inside the visible playfield',all(36<=p['len']<650 for q in results for p in q['calls']))
  ck('All tested firing sockets use registered visible animation frames',all(p['key']in ['af21_nyx_attack','air13_s6_nyx_heading']for q in results for p in q['ports']))
  q=p.evaluate("""()=>{const rows=[];let minPixels=999;for(const B of Object.values(NY47_SOCKETS)){const im=XART.get(Object.keys(NY47_SOCKETS).find(k=>NY47_SOCKETS[k]===B)),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);for(let i=0;i<B.points.length;i++)for(const xy of B.points[i]){const cell=B.cells[i],d=c.getContext('2d').getImageData(cell[0]+xy[0],cell[1]+xy[1],1,1).data;minPixels=Math.min(minPixels,d[3]);}}return minPixels;}""");ck('Every registered muzzle touches actual authored hull pixels',q>220,q)
  shots=[]
  for pan in [0,100,200,0]:
   q=p.evaluate("""pan=>{camX=pan;const A=n.rg4.act;A.phase='fire';A.t=0;A.cd=0;A.from={x:pan-100,y:-100};A.a=1.57;const start=eBullets.length;rg4AttackTick(n,R,G,1/60);return{visible:ny47Visible(n),shots:eBullets.slice(start).filter(q=>q._nx37Laser).map(z=>({x:z.x,y:z.y,s:z._ny47Socket})),x:n.x,y:n.y};}""",pan);shots.append(q)
  ck('Firing follows viewport changes and never emits from offscreen',all(q['visible']and len(q['shots'])==2 for q in shots),shots)
  ck('Both real shots begin at their FOV turret sockets',all(abs(z['x']-z['s']['x'])<1e-7 and abs(z['y']-z['s']['y'])<1e-7 for q in shots for z in q['shots']))
  p.evaluate('()=>{eBullets=[];retina.target=null;retina.phase=null;retinaScanClear();for(const q of R.ships)if(q!==n){q.x=2000;q.y=-1000;}camX=100;const A=n.rg4.act;A.phase="charge";A.t=1;A.from={x:300,y:150};A.a=1.9;ny47Hold(n,A);drawWorld(0)}');p.screenshot(path=str(W/'turret-fov.png'))
  p.evaluate('()=>{const A=n.rg4.act;A.phase="fire";A.t=.3;A.cd=0;rg4AttackTick(n,R,G,1/60);drawWorld(0)}');p.screenshot(path=str(W/'turret-fire.png'))
  ck('Old side-offscreen firing anchors are repaired before the native tick',p.evaluate('(()=>{const A=n.rg4.act;A.phase="fire";A.from={x:camLeftX()-300,y:100};A.cd=0;rg4AttackTick(n,R,G,1/60);return ny47Visible(n)})()'))
  ck('Hidden cloak still cancels firing completely',p.evaluate('(()=>{ny46Cloak(n);const first=eBullets.length;rg4AttackTick(n,R,G,1/60);return !n.rg4.act&&eBullets.length===first})()'))
  ck('Stage X retains its previous socket and movement owners',p.evaluate('(()=>{run._gp4StageX=true;const same=JSON.stringify(nx37Socket(n,-1))===JSON.stringify(NY47.base.socket(n,-1));run._gp4StageX=false;return same})()'))
  ck('No native errors',not errors,errors);(W/'pose-results.json').write_text(json.dumps(results,indent=2));b.close()
finally:stop()



