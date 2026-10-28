from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,numpy as np,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/harrier_turrets_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];http=[];console=[];checks=[]
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks-partial.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert v,name
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None);p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof HT28!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  def setup():
   p.evaluate("()=>{run.ngplus=false;diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,kind:'warhive',role:'boss',name:'Solid Harrier modules'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;}")
   for i in range(50):
    step(30)
    if p.evaluate('boss?._carrier17?.phase==="fight"&&!boss._carrier17.depth'):break
   p.wait_for_timeout(1500);step(4)
  setup();p.screenshot(path=str(W/'after-native.png'))
  poses=p.evaluate('''()=>{const b=boss,C=b._carrier17,out=[];for(const g of C.parts.filter(p=>p.kind==='gun')){for(const a of[0,Math.PI/4,Math.PI/2,Math.PI,Math.PI*1.5]){g.er28Bearing=g.angle=a;g.muzzleAge=99;g.phase='rest';const q=roster17Mount(b,g);out.push({id:g.id,a,frame:ht28Frame(g),centerOpaque:ht28Opaque(b,g,q.x,q.y),hit:roster17At(b,q.x,q.y),muzzle:roster17Muzzle(b,g)});}}return out}''')
  check('Every turret remains solid and targetable at its mounting pivot through five headings',all(q['centerOpaque']and q['hit']==q['id']for q in poses),poses)
  banks=p.evaluate('HT28_ART')
  for i in range(4):
   a=banks[f'gun_{i}'];im=np.array(Image.open(R/a['path']).convert('RGBA'));v=im[im[:,:,3]>0];check(f'Gun{i} uses full opaque coloured metal instead of translucent white highlight masks',np.all(v[:,3]==255)and len(np.unique(v[:,:3],axis=0))>12 and np.mean(np.all(v[:,:3]>230,axis=1))<.1,{'colours':len(np.unique(v[:,:3],axis=0)),'opaque':bool(np.all(v[:,3]==255))})
   check(f'Gun{i} all256 directional/recoil poses preserve fixed even cells and bore metadata',a['cw']==a['ch']==96 and a['frames']==256 and len(a['muzzles'])==256 and len(a['bounds'])==256)
  p.evaluate("()=>{const b=boss;for(const g of b._carrier17.parts.filter(p=>p.kind==='gun')){g.phase='rest';g.t=0;g.cool=99;g.er28Bearing=g.angle=Math.PI/2;g.flash=0;g.muzzleAge=99;} }");step(1);p.screenshot(path=str(W/'modules-idle.png'))
  # Exact source-to-world sockets follow a hull movement without detaching.
  follow=p.evaluate('''()=>{const b=boss,g=b._carrier17.parts.find(p=>p.id==='hullGun1'),a=roster17Muzzle(b,g);b.x+=17;b.y+=9;const c=roster17Muzzle(b,g);b.x-=17;b.y-=9;return{dx:c.x-a.x,dy:c.y-a.y}}''');check('Bore sockets follow the moving hull exactly',abs(follow['dx']-17)<.001 and abs(follow['dy']-9)<.001,follow)
  p.evaluate('''()=>{const b=boss,g=b._carrier17.parts.find(p=>p.id==='hullGun1');g.phase='fire';g.angle=g.er28Bearing=Math.PI/2;g.lanes=Array.from({length:9},()=>Math.PI/2);g.round=0;g.shot=0;g.t=0;g.muzzleAge=99;g.hp=g.maxhp;window.htShots=[];window.htOldMuzzle=roster17Muzzle;roster17Muzzle=function(b,p){const m=htOldMuzzle.apply(this,arguments);if(HT28.emitting===p)window.htLastMuzzle={...m};return m;};window.htOldShoot=eShootT;eShootT=function(x,y,a,s,k,o){const q=htOldShoot.apply(this,arguments);if(HT28.emitting)htShots.push({x,y,a,id:HT28.emitting.id,round:HT28.emitting.round,expected:htLastMuzzle});return q;};}''');step(40);shots=p.evaluate('htShots');check('Native gun fire launches from the actual alternating bore sockets',len(shots)>=5 and all(abs(q['x']-q['expected']['x'])<.001 and abs(q['y']-q['expected']['y'])<.001 for q in shots),shots);p.screenshot(path=str(W/'modules-firing.png'));p.evaluate('()=>{eShootT=htOldShoot;roster17Muzzle=htOldMuzzle}')
  # An actual native module hit must produce visible white pixels then expire.
  p.evaluate("()=>{const g=boss._carrier17.parts.find(p=>p.id==='hullGun0');g.phase='rest';g.cool=99;g.er28Bearing=g.angle=Math.PI/2;g.muzzleAge=99;g.flash=g.fl=0;}");step(1)
  sample='''()=>{const b=boss,g=b._carrier17.parts.find(p=>p.id==='hullGun0'),q=roster17Mount(b,g),px=Math.floor(q.x-camLeftX()-20),py=Math.floor(q.y-25),d=ctx.getImageData(px,py,40,50).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>245&&d[i+1]>245&&d[i+2]>245)white++;return{white,hp:g.hp,flash:g.flash}}'''
  before=p.evaluate(sample);p.evaluate("()=>{boss._carrier17.direct='hullGun0';_dmgBullet=null;hitBoss(7);}");step(1);hit=p.evaluate(sample);check('Native damage reduces its own gun pool and visibly flashes the complete module',hit['hp']<before['hp']and hit['white']>before['white']+60,{'before':before,'hit':hit});p.screenshot(path=str(W/'module-hit.png'));step(20);after=p.evaluate(sample);check('Native white hit flash expires back to coloured armor',after['flash']==0 and after['white']<hit['white'],after)
  targets=p.evaluate("()=>retinaBossTargets(boss).filter(q=>String(q._retinaId).includes('hullGun')).map(q=>({id:q._retinaId,x:q.x,y:q.y,hp:q.hp}))");check('All four modules retain independent live Retina targets',len(targets)==4,targets)
  dead=p.evaluate('''()=>{const b=boss,C=b._carrier17,g=C.parts.find(p=>p.id==='hullGun0'),prior=C.parts.filter(p=>p!==g).reduce((s,p)=>s+p.hp,0),m=roster17Muzzle(b,g);C.direct=g.id;_dmgBullet=null;hitBoss(g.hp+1);const shots=C.shots;roster17HullGun(b,g,2);return{dead:g.dead,hp:g.hp,other:C.parts.filter(p=>p!==g).reduce((s,p)=>s+p.hp,0),prior,unchangedShots:C.shots===shots,remainingTarget:retinaBossTargets(b).some(q=>String(q._retinaId).includes('hullGun0'))}}''');check('Destroying one turret stops its fire and Retina target without deleting other module HP',dead['dead']and dead['hp']==0 and dead['other']==dead['prior']and dead['unchangedShots']and not dead['remainingTarget'],dead);step(18);p.screenshot(path=str(W/'module-destroyed.png'))
  ordinary=p.evaluate("eBullets.filter(q=>q._carrierHullGun).map(q=>enemyOrdnanceCanIntercept(q))");check('Harrier gun bullets remain unshootable',not any(ordinary))
  check('No game/page/console/HTTP errors',not errors and not http and not console,{'page':errors,'http':http,'console':console});br.close()
finally:
 stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'pageErrors':errors,'HTTPerrors':http,'consoleErrors':console},indent=2),encoding='utf-8')
print(f'{len(checks)} native/art checks passed.')
