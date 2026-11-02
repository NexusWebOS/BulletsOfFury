"""Native Stage4 correction checks, pixels and actual attack ownership."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage4_amplify_1101';O.mkdir(exist_ok=True);checks=[];errors=[];runs=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if passed else'FAIL',name,flush=True)
SETUP=r'''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;S411.events=[];player.invuln=40002;playerLocks=[];return {type:E.type,hp:E.hp,ground:E.ground,body:[E.w,E.h],x:E.x,y:E.y};}'''
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
  p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(4,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&Object.values(S411_ART.banks).every(B=>XART.rdy(B.key))}',timeout=180000)
  p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
  specs=json.loads((R/'_shots/enemy_flight_1031/before/stage4-specs.json').read_text());types=['sandtank','s4missile','s4command','s4tanker','s4tractor','s4heavyjet','s4sam']
  for typ in types:
   spec=next(s for s in specs if s['type']==typ);initial=p.evaluate(SETUP,spec);trace=[]
   for j in range(27):
    q=p.evaluate('()=>{for(let i=0;i<40;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return {x:E.x,y:E.y,dead:E.dead,hp:E.hp,phase:E._s411?.phase,dir:E._s411Rendered?.dir,key:E._s411Rendered?.key,mod:E._modJet,body:[E._drawW,E._drawH]};}');trace.append(q);p.wait_for_timeout(3)
    if j in[4,10,16]and not q['dead']:p.screenshot(path=str(O/(typ+'-'+str(j)+'.png')))
    if q['dead']:break
   events=p.evaluate('S411.events');runs.append(dict(type=typ,initial=initial,trace=trace,events=events));(O/'runs.json').write_text(json.dumps(runs,indent=2))
   ck(typ+' retains native hull HP',all(q['hp']==initial['hp']for q in trace),initial)
   if typ=='sandtank':ck('Highway Tank has no lateral drift',max(q['x']for q in trace)-min(q['x']for q in trace)<.01,trace)
   elif typ=='s4tanker':ck('Tanker drives forward quickly and never fires',not any(e['event']=='shot'for e in events)and trace[-1]['y']>400,trace[-1])
   else:ck(typ+' actually releases its native weapon',any(e['event']=='shot'for e in events),events[-5:])
   if typ in['s4command','s4heavyjet']:
    ck(typ+' uses changing authored headings and no modular turrets',len({q['dir']for q in trace if q.get('dir')is not None})>=4 and all(not q.get('mod')for q in trace),trace)
    ck(typ+' rounds leave in facing direction',all(abs((e['a']-(3.141592653589793/2+round((e['a']-3.141592653589793/2)/(3.141592653589793*2)*16)*3.141592653589793*2/16)))<.0001 for e in events if e['event']=='shot'))
   if typ=='s4command':ck('Command is machine-gun ammunition only',all(e['kind']=='s4brass'for e in events if e['event']=='shot'))
   if typ=='s4tractor':ck('Tractor never fires backwards',all(e['vy']>0 and abs(e['vx'])<.001 for e in events if e['event']=='shot'))
   if typ=='s4sam':
    releases=[e for e in events if e['event']=='missile-release'];d=[round(releases[i+1]['t']-releases[i]['t'],3)for i in range(len(releases)-1)if releases[i+1]['index']!=0];ck('SAM releases three missiles one at a time',len(releases)>=3 and releases[:3][0]['index']==0 and[e['index']for e in releases[:3]]==[0,1,2]and all(.15<=x<=.22 for x in d),releases)
  # Actual pixels and expiry, using a freshly centered native actor crop.
  p.evaluate('''()=>{window.vehiclePixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return {white,color};};}''')
  for typ in types:
   p.evaluate(SETUP,next(s for s in specs if s['type']==typ));p.evaluate('()=>{for(let i=0;i<80;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=230;camX=E.x-VW/2;}');q=p.evaluate('()=>{const clean=vehiclePixels();hitEnemy(E,.01);const hit=vehiclePixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=230;return {clean,hit,expired:vehiclePixels()};}');ck(typ+' native damaged pixels and expiry',q['hit']['white']>q['clean']['white']+20 and q['expired']['white']<q['hit']['white'],q)
  # A real fuel kill damages nearby regular objects once, preserves distant ones.
  p.evaluate(SETUP,next(s for s in specs if s['type']=='s4tanker'))
  q=p.evaluate('''()=>{E.x=worldWidth()/2;E.y=220;window.fixtureSpawn=true;const near=spawnEnemy('s4barrel',E.x+70,E.y),far=spawnEnemy('s4barrel',E.x+230,E.y);window.fixtureSpawn=false;const before=[near.hp,far.hp];hitEnemy(E,99999);if(E._dyingT==null&&!E.dead)hitEnemy(E,99999);const first=S411.events.filter(e=>e.event==='fuel-splash');killEnemy(E);return {before,after:[near.hp,far.hp],count:S411.events.filter(e=>e.event==='fuel-splash').length,events:first,death:E._deathFxStarted};}''')
  ck('Tanker death has native explosions and one local splash',q['death']and q['count']==1 and q['after'][0]<q['before'][0]and q['after'][1]==q['before'][1],q)
  p.evaluate(SETUP,next(s for s in specs if s['type']=='s4sam'))
  q=p.evaluate('''()=>{E.x=worldWidth()/2;E.y=150;const A=E._s411;s411Salvo(E,3);for(let i=0;i<49;i++)updatePlay(1/60);hitEnemy(E,99999);if(E._dyingT==null&&!E.dead)hitEnemy(E,99999);const n=S411.events.filter(e=>e.event==='missile-release').length;for(let i=0;i<80;i++)updatePlay(1/60);return {before:n,after:S411.events.filter(e=>e.event==='missile-release').length,locks:playerLocks.filter(L=>L.src===E).length};}''')
  ck('Launcher defeat cancels its remaining salvo/Retina',q['before']==q['after']and q['locks']==0,q)
  q=p.evaluate('''()=>{const b=s411Round(E,0,true);const s={kind:'s4brass',_weaponProof:true,_shootable:false};return {ordinary:enemyOrdnanceCanIntercept(s),missile:enemyOrdnanceCanIntercept({kind:'s4missile',hp:2,_shootable:true,_weaponProof:false})};}''');ck('Ordinary MG rounds stay immune; real missiles remain interceptable',not q['ordinary']and q['missile'],q)
  ck('No native page/console errors',not errors,errors);b.close()
finally:(O/'errors.json').write_text(json.dumps(errors,indent=2))
sys.exit(0 if all(c['passed']for c in checks)else 1)
