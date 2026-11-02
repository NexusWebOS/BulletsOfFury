"""Native storm-contact books, exact pools, gun sockets, pixels and cleanup.
Isolated part-damage fixtures are separate from untouched full-fight recordings.
"""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/furious_encounters_1102';checks=[];errors=[];rows=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',name,flush=True)
with sync_playwright()as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate('''()=>{s6WingTick=()=>{};s6WingLaunch=()=>{};allyUpdate=()=>{};window.stormSetup=role=>{EA11.setup(6,'furious');if(s6Wing)s6Wing.ships=[];ally=null;stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;player.invuln=0;run.bombs=40;FB112.events=[];if(role==='mini'){spawnSubBoss('siegefortress17');window.B=subBoss;}else{spawnBoss('warhive');window.B=boss;}return{kind:B.kind,hp:B.hp,max:B.maxhp};};}''')
 for role in ['mini','boss']:
  before=p.evaluate('stormSetup',role);p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  for i in range(112):
   q=p.evaluate('''()=>{for(let i=0;i<15;i++){updatePlay(1/60);if(i%3===0){ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/20);}}return{t:B.t,phase:B._fb112.phase,attack:B._fb112.attack,hp:B.hp,parts:B._fb112.parts.map(p=>({id:p.id,hp:p.hp})),hazards:B._fb112.hazards.length,dead:player.dead};}''');rows.append(q)
   if i%18==0:p.screenshot(path=str(O/(role+'-book-'+str(i)+'.png')))
   if errors:break
  ev=p.evaluate('FB112.events');seen={e['attack']for e in ev if e['event']=='warning'};expected={'guns','pass','shear','vortex'}if role=='mini'else{'guns','gates','rail','vortex'}
  ck(role+' selects its Furious-only identity',before['kind']==('razorwake'if role=='mini'else'thunderhead'),before)
  ck(role+' native book runs every initial attack at untouched HP',expected<=seen and all(q['hp']==before['hp']for q in rows[-112:]),sorted(seen))
  ck(role+' emits native unshootable wind rounds',p.evaluate('()=>{const emitted=FB112.events.some(e=>e.event==="round");fb112Shot(B,B._fb112.parts[0],Math.PI/2);return emitted&&!enemyOrdnanceCanIntercept(eBullets.at(-1));}'))
  ck(role+' preserves complete displayed composite budget',p.evaluate('()=>B.hp===B._fb112.parts.reduce((s,p)=>s+p.hp,0)+B._fb112.core.hp'))
  ck(role+' actual muzzle sockets agree with source modules',p.evaluate('()=>B._fb112.parts.filter(p=>p.type==="gun").every(p=>{const a=fb112PartPoint(B,p),m=fb112Bore(B,p);return Math.hypot(a.x-m.x,a.y-m.y)>15&&Number.isFinite(m.x+m.y);})'))
  ck(role+' live target centres overlap actual native source alpha',p.evaluate('()=>B._fb112.parts.every(p=>{const at=fb112PartPoint(B,p);return fb112At(B,at.x,at.y)===p;})'))
  q=p.evaluate('''()=>{const q=B._fb112,at=fb112PartPoint(B,q.core),hp=B.hp;fb112Damage(B,20,at.x,at.y);return B.hp===hp;}''');ck(role+' core is protected until the actual weapons are gone',q)
  # Fresh isolated native owner for pixel/damage/part cancellation checks.
  p.evaluate('stormSetup',role);p.evaluate('''()=>{for(let i=0;i<240;i++)updatePlay(1/60);}''')
  q=p.evaluate('''()=>{const p=B._fb112.parts[0],at=fb112PartPoint(B,p);const pixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);fb112Draw(B);ctx.restore();let n=0;const a=ctx.getImageData(0,0,cv.width,cv.height).data;for(let i=0;i<a.length;i+=4)if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>180)n++;return n;};const clean=pixels();fb112Damage(B,1,at.x,at.y,p);const hit=pixels();for(let i=0;i<24;i++)updatePlay(1/60);return{clean,hit,after:pixels(),flash:p.flash};}''');ck(role+' native damaged module pixels flash and expire',q['hit']>q['clean']+10 and q['after']<q['hit']and q['flash']<=0,q)
  q=p.evaluate('''()=>{const p=B._fb112.parts[0];fb112Shot(B,p,Math.PI/2);fb112Damage(B,p.hp+1,null,null,p);return{broken:p.hp===0,rounds:eBullets.filter(r=>r._fb112Part===p&&!r.dead).length,targets:retinaBossTargets(B).filter(t=>t._retinaId?.includes(p.id)).length};}''');ck(role+' broken weapon cancels its rounds and target',q['broken']and q['rounds']==0 and q['targets']==0,q)
  p.evaluate('''()=>{for(const p of B._fb112.parts)for(let i=0;i<2&&p.hp>0;i++)fb112Damage(B,p.hp+1,null,null,p);}''');ck(role+' exhausting every weapon exposes only the live core',p.evaluate('()=>B._fb112.open&&retinaBossTargets(B).length===1&&B.hp===B._fb112.core.hp'))
  if role=='boss':
   for i in range(55):p.evaluate('()=>{for(let j=0;j<15;j++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(1)
   ck('Thunderhead exposed reactor runs the hurricane eye',p.evaluate('FB112.events.some(e=>e.event==="warning"&&e.attack==="eye")'));p.screenshot(path=str(O/'thunder-eye.png'))
  p.evaluate('''()=>{for(let j=0;j<2&&!B.dead;j++)fb112Damage(B,B.hp+1,null,null,B._fb112.core);for(let i=0;i<210;i++)updatePlay(1/60);}''');ck(role+' native defeat completes once with clean owned ordnance',p.evaluate('()=>B.dead&&eBullets.every(r=>r._fb112Owner!==B||r.dead)&&FB112.events.filter(e=>e.event==="defeat").length===1'))
 # Difficulty/route gates are exercised with the live native spawn owners.
 for diff in ['normal','hard']:
  q=p.evaluate('''d=>{EA11.setup(6,'furious');diffKey=d;DIFF=difficultyForRun(run.mode,d);spawnSubBoss('siegefortress17');const mini=!!subBoss?._fb112;spawnBoss('warhive');return{mini,boss:!!boss?._fb112};}''',diff);ck(diff+' keeps native Stage6 encounters',not q['mini']and not q['boss'],q)
 q=p.evaluate('''()=>{EA11.setup(6,'furious');run._gp4StageX='left';spawnBoss('warhive');return{storm:!!boss?._fb112,carrier:!!boss?._whv};}''');ck('Stage X retains its own native Harrier',not q['storm']and q['carrier'],q)
 q=p.evaluate('''()=>{EA11.setup(6,'furious');spawnBoss('rebelsquad');return{storm:!!boss?._fb112,riders:!!boss?._rebels};}''');ck('Furious keeps the separate right-hand Rough Riders route',not q['storm']and q['riders'],q)
 q=p.evaluate('''()=>{EA11.setup(7,'furious');spawnSubBoss('dualscoopdredger');return{pair:!!subBoss?._sj98,count:subBoss?._sj98?.actors.length};}''');ck('Furious Stage7 retains the generated mechanical Sumpjaw pair',q['pair']and q['count']==2,q)
 ck('No page, console or native renderer errors',not errors,errors);browser.close()
(O/'native-report.json').write_text(json.dumps(dict(checks=checks,errors=errors,rows=rows),indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks));sys.exit(0 if all(c['passed']for c in checks)else 1)
