from pathlib import Path
import sys,ast,json,http.server,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_finish_1020';checks=[];errors=[]
def value(file,name):return next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE'/file).read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
SETUP=value('probe_feedback_1002.py','SETUP');CLEAR=value('probe_performance_1020.py','CLEAR')
def ck(n,v,d=None):checks.append(dict(name=n,ok=bool(v),data=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
def setup(p,stage=1,kind=None,mini=False,diff='normal'):
 p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,diff=diff,pilot='cole'));p.evaluate(CLEAR);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1366,height=900));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate('BOFPERFORMANCE.warm();dr21Warm();');p.wait_for_function('()=>{BOFPERFORMANCE.warm();return BOFPERFORMANCE.ready&&dr21Warm()}')
  for diff in ['easy','normal','hard','furious']:
   for kind,source in [('laser','committed bomber lance'),('ice','Cryogenic laser mortar'),('dark','evil chromium void'),('shadow','Dracodia shadow eradication')]:
    setup(p,diff=diff);out=p.evaluate('''s=>{run.lives=4;player.invuln=0;run.shield=0;playerHit(s);const first=player._dr21Death?.kind;for(let i=0;i<240;i++)updatePlay(1/60);return{first,dead:player.dead,lives:run.lives,context:!!player._dr21Death,invuln:player.invuln};}''',source)
    ck(diff+' '+kind+' native respawn spends exactly one life and clears effect',out['first']==kind and not out['dead'] and out['lives']==3 and not out['context'],out)
  for stage,kind,mini in [(5,'siegebomber',True),(6,'siegefortress17',True),(6,'warhive',False)]:
   setup(p,stage,kind,mini);out=p.evaluate('''kind=>{let p,clock,kill,draw,expiry;
    if(kind==='siegebomber'){B._bomber.mode='recover';hc1007BomberTick(B,.01);hc1007BomberSet(B,'lances');p=B._bomber.parts.find(q=>q.id==='laserL');clock=()=>hc1007BomberTick(B,.02);kill=()=>siegeBomberHit(B,1e6,NaN,NaN,p.id);draw=()=>siegeBomberDraw(B);siegeBomberHit(B,1,NaN,NaN,p.id);expiry=()=>p.flash;}
    else if(kind==='siegefortress17'){const C=B._cargo13;C.mode='batteries';p=C.guns[0];C.directId=p.id;warhiveDamage(B,1);clock=()=>{warhiveTick(B,.02)};kill=()=>{sc13StartLaser(B,p.id);C.directId=p.id;warhiveDamage(B,1e6)};draw=()=>sc13GunDraw(B,p);expiry=()=>Math.max(p.fl||0,p.flash||0);}
    else{const C=B._carrier17;C.phase='fight';C.depth=false;p=C.parts.find(q=>q.kind==='laser');C.direct=p.id;roster17Damage(B,1);clock=()=>roster17FlashTick(C,.02);kill=()=>{p.phase='tell';p.t=.4;C.direct=p.id;roster17Damage(B,1e6)};draw=()=>roster17Draw(B);expiry=()=>Math.max(p.fl||0,p.flash||0);}
    for(let i=0;i<30;i++)clock();const expired=expiry()<=0;kill();const before=PF20.draws[kind==='siegebomber'?'bomber_cannon':'carrier_turret']||0;ctx.setTransform(SS,0,0,SS,0,0);draw();const delta=(PF20.draws[kind==='siegebomber'?'bomber_cannon':'carrier_turret']||0)-before;
    return{expired,dead:p.dead||p.hp<=0,delta,livePieces:kind==='siegebomber'?B._bomber.parts.filter(q=>q.id.startsWith('laser')&&q.hp>0).length:kind==='warhive'?B._carrier17.parts.filter(q=>q.kind==='laser'&&!q.dead).length:0,pending:kind==='siegebomber'?B._hc1007.lines.some(q=>q.id===p.id):kind==='siegefortress17'?B._cargo13.lasers.some(q=>q.id===p.id):p.phase==='tell'&&!p.dead};}''',kind)
   ck(kind+' hit flash expires and destroyed weapon cancels pending release',out['expired'] and out['dead'] and not out['pending'],out)
   ck(kind+' destroyed weapon leaves no animated ghost',out['delta']==out['livePieces'],out)
  setup(p);out=p.evaluate('''()=>{const before=JSON.stringify({q:groundTargetingFx.length,shots:eBullets.length,hp:run.shield});const o=[];for(const k of ['carrier_turret','bomber_cannon'])for(const phase of ['tell','fire','recover']){const i=pf20WeaponFrame(phase,.2,1);pf20Frame(k,i,200,200,.3);o.push(PF20.last);}return{same:before===JSON.stringify({q:groundTargetingFx.length,shots:eBullets.length,hp:run.shield}),frames:o};}''')
  ck('Rendering weapon frames creates no attacks, damage or warnings',out['same'],out)
  setup(p);p.evaluate('''()=>{for(const P of PILOTS)XART.rdy('ship_'+P.key+'_sp0');}''');p.wait_for_function('PILOTS.every(P=>XART.rdy("ship_"+P.key+"_sp0"))')
  for space in [False,True]:
   p.evaluate('space=>{run.stage=space?5:1;run.spaceMode=space;}',space)
   if space:p.wait_for_function('PILOTS.every(P=>!!spaceAtlasCanvas("ship_base",P.key))')
   out=p.evaluate('''space=>{run.spaceMode=space;const rows=[];for(const P of PILOTS){run.pilot=P.key;player.reset();const im=dr21Hull();if(!im){rows.push({pilot:P.key,missing:true});continue;}const a=im.getContext('2d').getImageData(0,0,192,192).data;let n=0,hash=0;for(let i=0;i<a.length;i+=4)if(a[i+3]){n++;hash=(hash*33+a[i]*3+a[i+1]*5+a[i+2]*7)>>>0;}rows.push({pilot:P.key,n,hash,space:spaceShipActive()});}return rows;}''',space)
   ck(('Furyship' if space else 'Aircraft')+' captures actual artwork for all nine pilots',len(out)==9 and all(q.get('n',0)>500 for q in out),out)
  setup(p);out=p.evaluate('''()=>{coopOn=true;run.lives=run2.lives=4;run.pilot='cole';run2.pilot='yuri';for(const s of seatList())withSeat(s,()=>{player.reset();player.invuln=0;run.shield=0;playerHit(s===1?'laser beam':'cryo shard');});const a=seatShip(1)._dr21Death,b=seatShip(2)._dr21Death;for(let i=0;i<240;i++)updatePlay(1/60);return{different:a!==b&&a.image!==b.image,kinds:[a.kind,b.kind],dead:seatList().map(s=>seatShip(s).dead),lives:seatList().map(s=>seatRun(s).lives),contexts:seatList().map(s=>!!seatShip(s)._dr21Death),seat:_seat};}''')
  ck('Co-op victims keep separate effect canvases, clocks, lives and restored seat',out['different'] and out['kinds']==['laser','ice'] and out['lives']==[3,3] and not any(out['dead']) and not any(out['contexts']) and out['seat']==1,out)
  setup(p);out=p.evaluate('''()=>{player.invuln=0;playerHit('laser');const D=player._dr21Death;setState('paused');const t=D.t;for(let i=0;i<30;i++)loop(performance.now()+i*16.67);return{same:D.t===t,state};}''')
  ck('Pause does not advance contextual death clock',out['same'] and out['state']=='paused',out)
  setup(p);p.keyboard.press('Shift');out=p.evaluate('''()=>{const keys=['beamCharge','laserShot','bossWeaponCharge','enemyHeavyLaser','combatBeam0927','enemyMG','slice','shadowRelease','expIce'].filter(k=>Snd.pools[k]);Snd.prepare(keys);return keys;}''');p.wait_for_function('keys=>keys.every(k=>Snd.pools[k].slots.some(v=>v?.attached&&v.el.readyState>=3))',arg=out,timeout=30000)
  sounds=p.evaluate('''()=>{const events=[],play=Snd.play;Snd.play=function(k,...a){events.push(k);return play.call(this,k,...a);};try{for(const kind of ['laser','ice','dark','shadow']){player.dead=true;player._dr21Death={kind,t:.45,life:1.5};updateDeathSpin(.02);}return{events,ready:events.map(k=>({key:k,decoded:Snd.pools[k]?.slots.some(v=>v?.attached&&v.el.readyState>=3),volume:Math.max(...(Snd.pools[k]?.slots||[]).filter(v=>v?.attached).map(v=>v.el.volume))}))};}finally{Snd.play=play;player._dr21Death=null;}}''')
  p.wait_for_function('keys=>keys.every(k=>Snd.pools[k].slots.some(v=>v?.attached&&v.el.readyState>=3))',arg=sounds['events'],timeout=30000);p.wait_for_timeout(200)
  sounds['ready']=p.evaluate('''keys=>keys.map(k=>({key:k,decoded:Snd.pools[k].slots.some(v=>v?.attached&&v.el.readyState>=3),volume:Math.max(...Snd.pools[k].slots.filter(v=>v?.attached).map(v=>v.el.volume)),played:Snd.pools[k].slots.some(v=>v?.el.currentTime>0)}))''',sounds['events'])
  ck('All four terminal transition cues use decoded mixer voices at audible gain',len(sounds['events'])==4 and all(q['decoded'] and q['volume']>0 and q['played'] for q in sounds['ready']),sounds)
  ck('No browser errors in edge cases',not errors,errors)
  (O/'edge-verification.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(dict(passed=sum(q['ok'] for q in checks),failed=sum(not q['ok'] for q in checks),errors=errors)),flush=True);raise SystemExit(bool(errors) or any(not q['ok'] for q in checks))
