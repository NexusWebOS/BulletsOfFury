"""Native Jace small-orb muzzle fixtures; preserves the large helix controller."""
from pathlib import Path
import ast,json,math
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/jace_turrets_1028/probe';O.mkdir(parents=True,exist_ok=True)
def strings(file):return[n.value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8')))if isinstance(n,ast.Constant)and isinstance(n.value,str)]
SETUP=next(s for s in strings('_BUILD_SOURCE/probe_feedback_1002.py')if s.startswith('c=>{ht27Stop'))
INIT=next(s for s in strings('_BUILD_SOURCE/probe_rebel_balance_1019.py')if s.startswith('gang=>{window.R='))
errors=[];checks=[]
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.stage=6;stageLoadBegin(6);}");p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'));p.evaluate(INIT,True)
  p.wait_for_function("()=>{stageLoadTick();rr26Warm();return stageLoadReady(6)&&Object.keys(JR36_TURRETS).every(k=>XART.rdy(k))&&XART.rdy('jr36_spin')}")
  p.evaluate("()=>{window.jace=R.ships.find(q=>q.key==='jace');G.age=20;G.rr26=rr26State(G);G.rr26.wall=null;G.rd21.fleet=null;G.rescueAt=999;G.rd21.next=999;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.rg4.gunCd=999;q.frCloak=0;q.evadeT=0;q.warp=0;q.mode='fight';}jace.x=worldWidth()/2;jace.y=150;jace.rfHeading=Math.PI/2;jace.flash=0;player.x=worldWidth()/2;player.y=440;eBullets=[];}")
  q=p.evaluate("()=>{return [-1,1].map(side=>{jace._rr26RoundAt=0;jace.rg4._rbal19Gun={side,tx:player.x,ty:player.y};const p=jr36Turret(jace,side),z=rg4Round({x:jace.x+side*18,y:jace.y},Math.PI/2,3,'s6tracer',{owner:jace});return{side,p,x:z.x,y:z.y,proof:!enemyOrdnanceCanIntercept(z),ordinary:z._jr36Bullet,asterisk:pw5Impact(z,player),angle:Math.atan2(z.vy,z.vx),expected:Math.atan2(player.y-p.y,player.x-p.x)};});}")
  ck('Both small fireballs begin exactly at their visible wing turret sockets',all(r['ordinary']and abs(r['x']-r['p']['x'])<.001 and abs(r['y']-r['p']['y'])<.001 for r in q),q)
  ck('Release uses the wide wing turrets rather than the old center offset',all(abs(r['p']['x']-340)>30 and abs(r['p']['y']-150)<12 for r in q))
  ck('Actual launch direction reaches the committed target from the new muzzle',all(abs(r['angle']-r['expected'])<.00001 for r in q))
  ck('Small orbs remain dodge-only and have no projectile asterisk',all(r['proof']and r['asterisk']is None for r in q))
  q=p.evaluate(r"""()=>{jace.rg4._rbal19Gun=null;const rows=[];for(let i=0;i<8;i++){jace.rfHeading=Math.PI/2+i*TAU/8;const pose=rr26AnimatedPose(jace)||rr26Pose(jace);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#07131e';ctx.fillRect(0,0,cv.width,cv.height);fr27RebelDrawShip(jace);for(const side of [-1,1]){const p=jr36Turret(jace,side),x=Math.round(p.x),y=Math.round(p.y),a=ctx.getImageData(x-4,y-4,9,9).data;let metal=0;for(let k=0;k<a.length;k+=4)if(a[k]+a[k+1]+a[k+2]>140)metal++;rows.push({i,side,key:p.key,frame:p.frame,rendered:jace._air13RenderedKey,pixels:metal});}ctx.restore();}return rows;}""")
  ck('Each heading selects the same authored frame for art and muzzle anchors',all(r['key']==r['rendered']for r in q),q)
  ck('All sixteen heading sockets meet actual native hull/turret pixels',all(r['pixels']>=4 for r in q),q)
  q=p.evaluate(r"""()=>{jace.rfHeading=Math.PI/2;jace.rg4.act=null;jace.rg4.gunCd=0;jace.rg4._rbal19Gun={side:-1,t:1,warm:.65,tx:player.x,ty:player.y,target:'cole'};jace._rr26RoundAt=0;eBullets=[];const muzzle=wm26Emit,calls=[];wm26Emit=function(q,x,y,a,family,color,opt){calls.push({x,y,a,family,color,follow:opt.follow?.()});return muzzle.apply(this,arguments);};try{ra4Gun(jace,G,1/60);}finally{wm26Emit=muzzle;}const z=eBullets.find(q=>q._jr36Bullet);return{z:z&&{x:z.x,y:z.y},calls,pending:jace.rg4._rbal19Gun,cooldown:jace.rg4.gunCd};}""")
  ck('Native gun controller attaches its orange muzzle flash to the fireball mouth',q['z']and len(q['calls'])==1 and q['calls'][0]['family']=='orb'and abs(q['calls'][0]['x']-q['z']['x'])<.01 and abs(q['calls'][0]['y']-q['z']['y'])<.01,q)
  ck('Native tell, release and cooldown ownership remain intact',q['pending']is None and q['cooldown']>=1.5)
  q=p.evaluate("()=>{eBullets=[];jace.rg4._rbal19Gun={side:1,t:1,warm:.65,tx:player.x,ty:player.y};const T=jace.rg4._rbal19Gun;jace.evadeT=.2;ra4Gun(jace,G,1/60);const waiting=jace.rg4._rbal19Gun===T&&eBullets.length===0;jace.evadeT=0;jace._rr26RoundAt=0;ra4Gun(jace,G,1/60);return{waiting,released:eBullets.some(q=>q._jr36Bullet)};}")
  ck('Ready turret fire waits through an evasive roll then releases visibly',q['waiting']and q['released'],q)
  q=p.evaluate(r"""()=>{jace.rg4._rbal19Gun={side:1,t:.4,warm:.65};const orb=jr36Orb,calls=[];jr36Orb=function(x,y){calls.push({x,y});return orb.apply(this,arguments);};try{fr27RebelDrawShip(jace);}finally{jr36Orb=orb;}const p=jr36Turret(jace,1);return{p,calls};}""")
  ck('Pre-shot charge light uses that same turret mouth',any(abs(r['x']-q['p']['x'])<.01 and abs(r['y']-q['p']['y'])<.01 for r in q['calls']),q)
  p.evaluate("()=>{jace.rg4._rbal19Gun=null;jace.rfHeading=Math.PI/2;G.ord=[];G.rr26.wall=null;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}");p.screenshot(path=str(O/'turret-fire.png'))
  q=p.evaluate("()=>{const parts=fr27RebelModules(jace);parts[0].hp=0;jace.rg4._rbal19Gun={side:-1,tx:player.x,ty:player.y};const z=rr36Bullet(jace,jace.x,jace.y,Math.PI/2,3);const single=z._jr36Side===1;parts[1].hp=0;const none=rr36Bullet(jace,jace.x,jace.y,Math.PI/2,3);updatePlay(.000001);return{single,quiet:none.dead,cancel:z.dead};}")
  ck('Destroyed wing turrets cannot emit or keep their orphaned rounds',q['single']and q['quiet']and q['cancel'],q)
  q=p.evaluate("()=>{for(const m of fr27RebelModules(jace))m.hp=m.max;jace.rg4._rbal19Gun=null;G.ord=[];ra4Helix(jace,G,{a:Math.PI/2});const o=G.ord.at(-1);return{large:o._jr36Helix,hp:o.hp,r:o.r,x:o.x,y:o.y};}")
  ck('Large ranged helix and its independent native origin remain unchanged',q['large']and q['hp']==6 and q['r']==28 and abs(q['x']-340)<1,q)
  ck('No browser, console or asset errors',not errors,errors)
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));b.close()
finally:stop()
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
