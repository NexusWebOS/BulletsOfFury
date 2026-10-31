from pathlib import Path
import sys,json,http.server,hashlib,math
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/sumpjaw_duo_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:650]if not v else'',flush=True);assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031/manifest.json').read_text());ck('847 fixed even frames and18 editable banks',sum(a['frames']for a in M['banks'].values())==847 and len(M['banks'])==18 and all(a['w']%2==a['h']%2==0 and(R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031'/(n+'.aseprite')).exists()for n,a in M['banks'].items()))
ck('Registered source cells and pages stay within4096px',all(Image.open(R/p['path']).size==(a['cols']*a['w'],math.ceil(p['frames']/a['cols'])*a['h'])and max(Image.open(R/p['path']).size)<=4096 for a in M['banks'].values()for p in a['pages']))
ck('Baked hit frames keep the exact normal alpha',all(ImageChops.difference(Image.open(R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031'/f'body{s}_0.png').getchannel('A'),Image.open(R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031'/f'hit{s}_0.png').getchannel('A')).getbbox()is None for s in range(4)))
port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,7,errors)
  p.wait_for_function('()=>{stageLoadTick();return sj98Ready()}',timeout=180000)
  def step(n):
   for i in range(0,n,12):
    e=p.evaluate(STEP,min(12,n-i));assert not e,e;p.wait_for_timeout(1)
  def reset():
   p.evaluate("()=>{diffKey='furious';spawnSubBoss('dualscoopdredger');window.B=subBoss;window.G=B._sj98;G.rest=99;for(const a of G.actors){a.phase='idle';a.frame=0;a.t=0;}eBullets.length=0;SJ98.events=[];SJ98.draws={};player.reset();player.x=camLeftX()+viewW()/2;player.y=VH-60;player.dead=player.out=false;player.invuln=0;DBGT.god=true;for(const k of Object.keys(Input.keys))Input.keys[k]=false;setState(GS.PLAY);}")
  def shot(n):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(n+'.png')))
  reset();shot('pair-idle')
  ck('Furious contains two independent full-health actors and no Dredger rig',p.evaluate('G.actors.length===2&&G.actors.every(a=>a.hp===a.maxhp)&&!B._s7mod&&!B._ship&&B._s4MiniSafe'))
  ck('Complete local health budget equals both real actors',p.evaluate('B.hp===G.actors.reduce((s,a)=>s+a.hp,0)&&B.maxhp===G.actors.reduce((s,a)=>s+a.maxhp,0)'))
  ck('Four gills target initially; hearts and hull do not consume shots',p.evaluate("retinaBossTargets(B).length===4&&G.actors.every(a=>{const p=sj98Socket(a,'heart');return !subBossSolidAt(p.x,p.y)})"))
  ck('Ordinary bullet geometry reaches all four gill centers',p.evaluate("G.actors.every(a=>a.pools.slice(0,2).every(z=>{const q=sj98Socket(a,z.id);return !!subBossHitPart(q.x,q.y)&&subBossSolidAt(q.x,q.y)}))"))
  p.evaluate("()=>{window.A=G.actors[0];window.P=A.pools[0];const q=sj98Socket(A,P.id);window.hp0=P.hp;hitSubBoss(10,q.x,q.y);}");ck('Native point damage affects one pool and one actor',p.evaluate('P.hp<hp0&&G.actors[1].hp===G.actors[1].maxhp&&A.flash>0&&A.hp===A.pools.reduce((s,p)=>s+p.hp,0)'));shot('actual-hit')
  p.evaluate('()=>{window.normal98=SJ98.draws.body0||0;window.hit98=SJ98.draws.hit0||0;sj98Draw(B)}');ck('Real native hit-white bank draws',p.evaluate('(SJ98.draws.hit0||0)>hit98'))
  step(8);ck('Hit flash expires through its normal timer',p.evaluate('A.flash===0'))
  p.evaluate("()=>{const z=sj98Socket(A,'gillL');sj98Damage(B,99999,z.x,z.y);sj98Damage(B,99999,z.x,z.y);}");ck('One broken gill preserves the sealed heart and other actor',p.evaluate("A.pools[0].hp===0&&A.pools[1].hp>0&&A.pools[2].hp===A.pools[2].maxhp&&G.actors[1].hp===G.actors[1].maxhp"))
  p.evaluate("()=>{const z=sj98Socket(A,'gillR');sj98Damage(B,99999,z.x,z.y);sj98Damage(B,99999,z.x,z.y);}");shot('opened-heart')
  ck('Both broken gills expose exactly one real intake heart',p.evaluate("sj98State(A)===3&&A.pools[2].hp===A.pools[2].maxhp&&retinaBossTargets(B).filter(t=>t._retinaId.startsWith('sump0-')).map(t=>t._retinaId).join(',')==='sump0-heart'"),p.evaluate("({pools:A.pools,phase:A.phase,targets:retinaBossTargets(B).map(t=>({id:t._retinaId,hp:t.hp,dead:t.dead})),events:SJ98.events.slice(-4)})"))
  step(80);p.evaluate("()=>{const z=sj98Socket(A,'heart');sj98Damage(B,99999,z.x,z.y);sj98Damage(B,99999,z.x,z.y);}");ck('First creature dies without completing encounter or harming survivor',p.evaluate('A.dead&&!B.dead&&!subBossDone&&G.actors[1].hp===G.actors[1].maxhp&&B.hp===G.actors[1].hp'));shot('one-survivor')
  reset();p.evaluate("()=>{window.A=G.actors[0];sj98Start(B,A);}");step(36);ck('Breach warns before hitting; distant body has no target',p.evaluate("A.phase==='warn'&&A.attack==='breach'&&!sj98Foreground(A)&&!retinaBossTargets(B).some(t=>t._retinaId.startsWith('sump0-'))"));shot('breach-warning')
  p.evaluate('()=>{window.t0=A.t;setState(GS.PAUSE)}');step(50);ck('Pause freezes attack and landing clocks',p.evaluate('A.t===t0'));p.evaluate('setState(GS.PLAY)');step(144);shot('breach-foreground')
  ck('Foreground breach returns real targets and recovery',p.evaluate('sj98Foreground(A)&&A.phase==="recover"'))
  reset();p.evaluate("()=>{window.A=G.actors[0];A.seq=1;sj98Start(B,A)}");step(60);ck('Toxic lobs launch from the actual mouth and acquire separate landings',p.evaluate('G.flights.length===1&&Math.hypot(G.flights[0].from.x-sj98Socket(A,"heart").x,G.flights[0].from.y-sj98Socket(A,"heart").y)<3'));shot('mouth-lob')
  step(100);ck('Landed globules emit finite unshootable toxic scatter',p.evaluate('SJ98.events.some(e=>e.event==="splash")&&eBullets.filter(q=>q._sj98Owner).length>0&&eBullets.filter(q=>q._sj98Owner).every(q=>enemyOrdnanceCanIntercept(q)===false)'));shot('toxic-scatter')
  step(210);ck('Toxic fragments expire instead of bouncing forever',p.evaluate('!eBullets.some(q=>q._sj98Owner)&&G.flights.length===0'))
  reset();p.evaluate('()=>{G.rest=0;window.viol98=[];window.maxFX98=0;}')
  bounds=True;interlock=True
  for i in range(180):
   step(12);q=p.evaluate('({count:G.actors.filter(a=>["warn","dive","breach","bite","lob"].includes(a.phase)).length,bounds:G.actors.every(a=>{const p=sj98Pose(a),l=a.x+(a.flip?-p.bounds[2]:p.bounds[0]),r=a.x+(a.flip?-p.bounds[0]:p.bounds[2]);return l>=camLeftX()&&r<=camRightX()}),clear:(()=>{const a=G.actors[0],b=G.actors[1],pa=sj98Pose(a),pb=sj98Pose(b);return a.x+pa.bounds[2]+15<b.x-pb.bounds[2]})(),flights:G.flights.length})');interlock&=q['count']<=1;bounds&=q['bounds'];
  ck('Heavy attacks remain staggered through repeated books',interlock)
  ck('Both complete silhouettes remain inside visible camera bounds',bounds)
  ck('Each creature uses breach, toxic lob and bite rather than simultaneous heavy attacks',p.evaluate('G.actors.every(a=>["breach","lob","bite"].every(k=>SJ98.events.some(e=>e.event==="attack"&&e.actor===a.i&&e.kind===k)))'))
  reset();p.evaluate("()=>{DBGT.god=false;player.invuln=0;player.x=camLeftX()+viewW()/2;player.y=VH-60;}");step(100);ck('Parent encounter box causes no invisible body deaths',p.evaluate('!player.dead'))
  reset();p.evaluate("()=>{for(const a of G.actors){for(const z of a.pools){a.phase='idle';const q=sj98Socket(a,z.id);sj98Damage(B,999999,q.x,q.y,{a,p:z});sj98Damage(B,999999,q.x,q.y,{a,p:z});}}}")
  ck('Both full budgets must exhaust before the one native defeat',p.evaluate('B.dead&&B.hp===0&&SJ98.events.filter(e=>e.event==="pair-defeat").length===1&&retinaBossTargets(B).length===0'));step(160)
  ck('Exactly one completion/reward hands the stage back without a softlock',p.evaluate('subBoss===null&&!subBossActive&&subBossDone&&SJ98.events.filter(e=>e.event==="progression").length===1'))
  for rank in ['normal','hard']:
   p.evaluate('(rank)=>{diffKey=rank;spawnSubBoss("dualscoopdredger")}',rank);ck(rank+' keeps the existing Dredger encounter',p.evaluate('!subBoss._sj98&&subBoss._ship==="dualscoopdredger"'))
  reset();ck('Retry restores two intact independent budgets and empty attack effects',p.evaluate('G.actors.every(a=>!a.dead&&a.pools.every(p=>p.hp===p.maxhp))&&G.flights.length===0&&G.fx.length===0'))
  ck('No native browser or draw errors',not errors,errors);br.close()
finally:stop()
ck('Core source is unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
print('RESULT',len(checks),'checks passed',flush=True)
