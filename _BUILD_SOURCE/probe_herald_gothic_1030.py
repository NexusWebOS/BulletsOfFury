from pathlib import Path
import sys,json,http.server,numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_gothic_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_08/miniboss/herald_gothic_1030/manifest.json').read_text())
ck('All78 banks use even fixed cells, valid pivots and atlases no larger than4096',len(M)==78 and all(a['cw']%2==a['ch']%2==0 and max(Image.open(R/a['path']).size)<=4096 and a['pivot']for a in M.values()))
def cell(n,f):
 a=M[n];im=Image.open(R/a['path']);return np.array(im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch'])))
ck('Skull loop has16 distinct authored frames',len({cell('skull_7',f).tobytes()for f in range(16)})==16)
ck('Head cast genuinely changes jaw/eye source frames',len({cell('head_cast',f).tobytes()for f in range(24)})>=16)
ck('Arms reach the raised pose continuously during charge and lower back to idle',abs(M['gunL_cast']['poses'][23]['a']-M['gunL_raised']['poses'][0]['a'])<.001 and M['gunL_lower']['poses'][0]['a']==M['gunL_raised']['poses'][0]['a']and abs(M['gunL_lower']['poses'][23]['a'])<.001)
ck('Spiral has96 distinct genuine depth and roll views with per-frame sockets and masks',M['spiral']['frames']==96 and len(M['spiral']['sockets'])==len(M['spiral']['spans'])==96 and len({cell('spiral',f).tobytes()for f in range(96)})==96)
ck('Every spiral and yaw hit frame exactly preserves visible source alpha',all(np.array_equal(cell(n,f)[:,:,3],cell(n+'_hit',f)[:,:,3])for n in ['yaw','spiral']for f in range(M[n]['frames'])))
ck('Depth sphere glass bursts use only the skull-free source segment',all(np.array_equal(cell('glass_'+str(i),0),cell('impact_'+str(i),7))and np.array_equal(cell('glass_'+str(i),15),cell('impact_'+str(i),15))for i in range(8)))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate("()=>{run.stage=8;stageLoadBegin(8)}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;pBullets=[];eBullets=[];}")
  ck('Native Herald completes entrance',advance(p,'!B.enter',300,1));ck('All new art is preloaded',p.evaluate('Object.values(HG70_ART).every(a=>XART.rdy(a.key))'))
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  def snap(name):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(name+'.png')))
  p.evaluate("()=>{hr28Start(B,'nuke');HG70.events=[];HH52.events=[];}");step(65);snap('gothic-charge')
  ck('Charge selects an animated face and smoothly raised arms through native pose owner',p.evaluate("(()=>{const A=hh52Special(B),h=hd1003Pose(B,hd1003Part(B,'head')),g=hd1003Pose(B,hd1003Part(B,'gunL'));return A.clip==='cast'&&A.frame>0&&h.y<B.y&&Math.abs(g.a)>.3})()"))
  ck('Actual gothic skull release occurs',advance(p,"eBullets.some(q=>q._hh52Skull)",180,1));step(72);snap('gothic-skull-bombs')
  r=p.evaluate("""()=>{const q=eBullets.find(q=>q._hh52Skull&&!q.dead),old=ctx.drawImage,calls=[];ctx.drawImage=function(im,...a){if(im===XART.get(HH52_ART['skull_'+q._hh52Level].key))calls.push(a);return old.apply(this,[im,...a])};try{drawCombatFinalProjectile(q)}finally{ctx.drawImage=old}return calls;}""")
  ck('Native skull projectile draws the new gothic atlas at fixed132px size',len(r)==1 and r[0][-2:]==[132,132],r)
  r=p.evaluate("""()=>{const q=eBullets.find(q=>q._hh52Skull&&!q.dead);q.x=player.x+120;q.y=player.y-130;const n=eBullets.length;ordnanceBreak1002(q);q.dead=true;return{chunks:eBullets.slice(n).map(p=>({orb:p._hh52Chunk,proof:enemyOrdnanceCanIntercept(p)})),fx:HH52.fx.at(-1)};}""")
  ck('Skull destruction creates dangerous red lightning ricochets and new shatter art',len(r['chunks'])>=6 and all(q['orb']and not q['proof']for q in r['chunks'])and r['fx']is not None)
  snap('gothic-shatter')
  ck('Skull attack enters continuous lower-arm recovery',advance(p,"hh52Special(B)?.phase==='recover'",650,1));step(10);ck('Recovery selects the authored lower bank',p.evaluate("hh52Special(B)?.clip==='lower'&&hh52Special(B).frame>0"));snap('gothic-recovery')
  # Enter the20% threshold through the native damage function, never start by rewriting its phase.
  p.evaluate("()=>{pBullets=[];eBullets=[];HH52.skulls.clear();hr28End(B);hd1003Hit(B,B.maxhp*3,B.x,B.y,'core')}")
  ck('Native20% damage gate launches desperation at the correct HP',p.evaluate('B._hd1003.hd54&&Math.abs(B.hp/B.maxhp-.2)<.001'))
  ck('Background spin begins after native five-second charge',advance(p,"hd54Own(B)?.phase==='spin'",600,1));ck('Native depth orb becomes a visible foreground projectile',advance(p,'HD54.flights.some(hg70Active)',200,1))
  p.evaluate('()=>{window.F=HD54.flights.find(hg70Active);window.hpBefore=B.hp;hd1003Hit(B,100,B.x,B.y,"core")}')
  ck('Ordinary fire still cannot damage the protected background Herald',p.evaluate('B.hp===hpBefore'))
  ck('Both Retina modes can select the actual visible orb',p.evaluate('retinaBossTargets(B).some(t=>t._retinaId==="hg70-orb-"+F.id)'))
  p.evaluate("()=>{pBullets.push({kind:'bullet',x:F.q.x,y:F.q.y,vx:0,vy:-4,w:8,h:8,dmg:2});}");step(1)
  ck('Ordinary machine-gun fire does not destroy or reflect the depth orb',p.evaluate('hg70Active(F)&&!F.returning'))
  p.evaluate("()=>{pBullets=[];pBullets.push({kind:'gmiss',x:F.q.x,y:F.q.y,vx:0,vy:-6,spd:7.2,w:10,h:18,dmg:24,t:0});}");step(1)
  ck('Physical missile collision knocks the orb back and removes hostile collision',p.evaluate('!!F.returning&&!F.q&&!F.done'));snap('missile-orb-return')
  ck('Returned orb reaches background Herald and deals native HP damage',advance(p,"HG70.events.some(e=>e.event==='orb-counter-hit')",100,1))
  r=p.evaluate("HG70.events.find(e=>e.event==='orb-counter-hit')");ck('Counter damage is1.25% native max HP without weakening background protection',abs(r['damage']-p.evaluate('B.maxhp*.0125'))<.01 and p.evaluate('hd54Protected(B)&&!B._hg70Counter'),r)
  ck('Background counter hit has matched white flash art',p.evaluate('XART.rdy(HD54_ART.spin_hit.key)'))
  ck('Another depth orb becomes targetable',advance(p,'HD54.flights.some(hg70Active)',100,1));p.evaluate('()=>{F=HD54.flights.find(hg70Active);player.x=F.q.x;pBullets=[{kind:"beam",x:F.q.x,y:player.y,w:20,top:-20,bot:player.y,life:.3,dmg:1,_hit:[]}]}');step(1)
  ck('Actual laser beam shatters the orb into dangerous glass fragments',p.evaluate('F.done&&eBullets.some(q=>q._hg70Glass&&!q.dead)'));snap('laser-glass-shatter')
  ck('Glass uses native lethal collision and cannot be shot down',p.evaluate('eBullets.filter(q=>q._hg70Glass&&!q.dead).every(q=>q._hs53==="shard"&&!enemyOrdnanceCanIntercept(q)&&q._weaponProof&&!q._shootable)'))
  p.evaluate('()=>{pBullets=[]}');ck('Native sequence returns to its foreground attack',advance(p,"hd54Own(B)?.phase==='foreground'",1100,1));step(50);snap('foreground-circular-volley')
  ck('Foreground yaw fires a complete circular volley',p.evaluate('HG70.events.some(e=>e.event==="foreground-circle"&&e.count>=8&&e.bank==="yaw")'))
  ck('Pseudo3D spiral bank begins while still firing',advance(p,"hd54Own(B)?.bank==='spiral'",240,1));step(30);snap('foreground-3d-spiral')
  ck('Native rendering selects a fixed authored spiral frame and same-frame socket',p.evaluate('(()=>{const A=hd54Own(B);return A.frame>=0&&A.frame<96&&HD54_ART[A.bank].sockets[A.frame].length===2})()'))
  ck('Foreground spiral resumes depth shots as well as circular shots',advance(p,'HG70.events.some(e=>e.event==="foreground-circle"&&e.bank==="spiral")&&HD54.events.filter(e=>e.event==="roller-release").some(e=>e.frame>=32)',150,1))
  r=p.evaluate('''()=>{const A=hd54Own(B),a=HD54_ART[A.bank];let hits=0,gaps=0;for(let y=0;y<320;y+=7)for(let x=0;x<320;x+=7){const id=hd1003At(B,B.x+x-160,B.y+y-160);if(id)hits++;else gaps++;}return{hits,gaps};}''')
  ck('Visible rotated hull is hittable and surrounding alpha gaps pass through',r['hits']>20 and r['gaps']>100,r)
  p.evaluate('()=>{hpBefore=B.hp;hd1003Hit(B,10,B.x,B.y,"core")}');ck('Foreground still takes native weapon damage',p.evaluate('B.hp<hpBefore'))
  ck('Pressure remains bounded and prior red lasers, Retinas and tornado work stays loaded',p.evaluate('HD54.flights.length<=48&&eBullets.filter(q=>q._heraldOwner1003===B&&!q.dead).length<=128&&typeof HL67!=="undefined"&&XART.rdy(HL51_ART.key)&&XART.rdy(HH69_ART.flash.key)'))
  # A glass fragment must be capable of normal player damage, not cosmetic debris.
  p.evaluate('()=>{pBullets=[];eBullets=[];DBGT.god=false;player.invuln=0;player.dead=false;window.oldLives=run.lives;window.oldDeaths=run.stats?.deaths;const q=hs53Round(B,player,0,0,"shard",{_hg70Glass:true,_hs53Dir:0,_hs53Phase:0});q.vx=q.vy=0;}');step(3)
  r=p.evaluate('({dead:player.dead,lives:run.lives,oldLives,invuln:player.invuln})');ck('Red glass can kill the player through normal engine damage',r['dead']or r['lives']<r['oldLives'],r)
  ck('No native game, drawing or console errors',not errors,errors)
  (W/'events.json').write_text(json.dumps(p.evaluate('({gothic:HG70.events,depth:HD54.events,chaos:HH52.events})'),indent=2));br.close()
finally:stop()
print(len(checks),'Herald gothic and counter checks passed')
