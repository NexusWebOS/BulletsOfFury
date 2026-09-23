import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/focus_0922');O.mkdir(exist_ok=True);errors=[];r={};port,stop=serve(GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1440,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,a=None):return pg.evaluate(s,a)
  def step(n):
   while n>0:
    v=ev(STEP,min(n,60));assert not v,v;n-=60;pg.wait_for_timeout(30)
  def cap(name):
   step(1);(O/(name+'.png')).write_bytes(base64.b64decode(ev("()=>cv.toDataURL().split(',')[1]")))
  def setup(stage):
   ev(SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   ev('()=>{stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];stageTimer=0;aminiTriggered=true;_sc1=true;_sc2=true;}')
  setup(6);step(180);cap('stage6_intro')
  r['continuous']=ev('''()=>{s6Wing.all=true;s6Wing.choice=true;s6Wing.choiceT=0;let before=stageTimer,sky=_stage6SkyScroll;for(let i=0;i<60;i++){updatePlay(1/60);drawBG(1/60);}return {elapsed:stageTimer-before,sky:_stage6SkyScroll-sky,scale:timeScale,choice:s6Wing.choiceT};}''')
  ev("()=>{s6Opening.phase='reveal';s6Opening.t=.5;}");step(30);cap('stage6_reveal')
  r['ownership']=ev('''()=>{s6WingInit();let W=s6Wing;W.ships=[{key:'yuri',phase:'fight',x:240,y:350}];W.boxes=[{key:'yuri',x:240,y:250,hp:6,t:0}];pBullets=[{x:240,y:250,w:8,h:14,dmg:10,kind:'mg'}];s6SupplyTick(W,0);const before=W.boxes[0].hp;pBullets[0]._wingKey='yuri';s6SupplyTick(W,0);return {before,open:W.boxes[0].open};}''')
  setup(6);ev("()=>{s6Opening=null;s6WingInit();s6Wing.beats=2;spawnBoss('rebelsquad');}");step(240);cap('five_rivals')
  r['rivals']=ev('()=>({n:boss._rebels.ships.length,shields:boss._rebels.ships.map(q=>q.shield),ready:boss._rebels.ships.every(q=>q.mode!=="entry")})')
  pg.wait_for_function("()=>REBEL_SHIPS.every(id=>Array.from({length:8},(_,f)=>XART.rdy('rr_roll_'+id+'_'+f)).every(Boolean))")
  ev("()=>{boss._rebels.ships.forEach(q=>{q.evadeT=.2;q.evadeX=q.x+20;q.bankDir=1;});}");cap('rival_rolls')
  r['childOwner']=ev("()=>{pBullets=[];yuriLightningOrbRelease({x:240,y:200,lv:3,_wingKey:'yuri',ally:true});return pBullets.every(q=>q._wingKey==='yuri'&&q.ally);}")
  setup(1);r['sonic']=ev('''()=>{let out={};for(const d of ['normal','hard','furious']){diffKey=d;eBullets=[];let b={x:240,y:120,_pivot:.5,_ovSonic:{phase:'waves',t:0,sent:0,angle:Math.PI/2}};ovSonicComboTick(b,3.5);out[d]={waves:eBullets.map(q=>({vertical:!!q.vertical,angle:q.ang,w:q.w,x:q.x})),pivot:b._pivot,x:b.x};}return out;}''')
  setup(4);ev("()=>{diffKey='furious';spawnBoss('stormsovereign');boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=boss._s4war.homeY;boss.hp=boss.maxhp*.49;stage4CoreTurretSpawnMissing(boss,.5);}");step(130);cap('stage4_socket_helpers')
  r['turrets']=ev('()=>boss._s4war.coreTurrets.map(q=>({x:q.x,y:q.y,ang:q.ang,side:q.side,target:stage4CoreTurretTarget(boss,q.side)}))')
  setup(5);ev("()=>{diffKey='furious';spawnBoss('chromehammer');boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=170;boss._hammer.state='warn';boss._hammer.tx=player.x;boss._hammer.ty=player.y;}");step(20)
  pg.wait_for_function("()=>XART.rdy('arch_leap_strike_0922')");cap('archmage_overhead')
  ev("()=>{boss._hammer.state='recover';boss._hammer.t=.08;}");cap('archmage_impact')
  ev("()=>{boss._hammer.state='spin';boss._hammer.t=1;boss._hammer.throwX=player.x;boss._hammer.throwY=player.y;}");pg.wait_for_function("()=>XART.rdy('arch_twirl_throw_0922')");cap('archmage_twirl')
  r['hammerImpact']=ev('''()=>{let old=playerHit,hits=0;playerHit=()=>hits++;try{player.invuln=0;boss.x=player.x;boss.y=player.y-32;let h=boss._hammer;h.state='leap';h.t=.28;h.ox=h.tx=player.x;h.oy=h.ty=player.y-32;hammerBossTick(boss,.01);return hits;}finally{playerHit=old;}}''')
  setup(2);ev("()=>{run.stage=2;run.loadout=[0,1,2,3,4,5];run.wlevels=WEAPONS.map(()=>3);run.forge={3:{elem:'fire',lv:3}};run.forgeForms={3:{fire:{lv:3,elem:'fire'}}};run.forgeElems={fire:1,ice:1};run.wvars=WEAPONS.map(()=>null);}")
  r['whipSelect']=ev("()=>weaponFormSelect(3,{kind:'variant',id:'firewhip'})")
  ev("()=>{run.weapon=3;run.wlevel=3;fireWhipFire(3,4);}");step(1)
  r['whip']=ev('''()=>{const b=pBullets.find(q=>q.kind==='firewhip');let a=fireWhipPoints(b,0),z=fireWhipPoints(b,1);player.x+=31;fireWhipFire(3,4);fireWhipTick(b,.1);return {left:a[16].x<a[0].x,right:z[16].x>z[0].x,anchor:b.x===player.x&&b.y===player.y-18};}''')
  cap('firewhip_live')
  ev("()=>{loadoutStart(()=>{});loadoutScr.sel=3;loadoutScr.row=2;loadoutScr.vsel=1;}");step(150);cap('firewhip_selection')
  r['previewError']=ev('()=>loadoutScr.preview&&loadoutScr.preview.err')
  ev("()=>{loadoutScr.row=0;}");cap('loadout')
  ev("()=>suppliesStart(()=>{},()=>{})");step(100);cap('supplies')
  ev("()=>unlocksStart([['MAGMA ORB','micon_forge_fire_5'],['FIRE WHIP','micon_firewhip_0919_3'],['FLAME BURST','micon_forge_fire_1'],['FIRE LASER','micon_forge_fire_3']],()=>{})");step(100);cap('unlocks')
  r['combos']=ev('''()=>{let out=[];for(const e of Object.keys(INFUSIONS))for(let w=0;w<9;w++){let P=forgePreviewNew(w,e,3);for(let i=0;i<90;i++)forgePreviewTick(P,180,220,1/60);out.push({e,w,error:P.err,kinds:[...new Set(P.bullets.map(q=>q.kind))],fired:P.fired});}return out;}''')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert r['childOwner']
assert r['continuous']['elapsed']>.9 and r['continuous']['sky']>700 and r['continuous']['scale']==1
assert r['ownership']=={'before':6,'open':True}
assert r['rivals']['n']==5 and not any(r['rivals']['shields'])
assert [len(r['sonic'][d]['waves']) for d in ['normal','hard','furious']]==[1,3,6]
assert r['hammerImpact']==1
assert r['whipSelect']=='ok' and all(r['whip'].values())
assert not r['previewError']
assert all(not q['error'] and q['fired'] for q in r['combos'])
