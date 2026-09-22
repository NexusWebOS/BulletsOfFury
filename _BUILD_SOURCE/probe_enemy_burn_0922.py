import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/burn_0922');O.mkdir(exist_ok=True)
port,stop=serve(GAME);r={};errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_context(storage_state={'cookies':[],'origins':[]},viewport={'width':1280,'height':1080}).new_page()
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,arg=None):return pg.evaluate(s,arg)
  def step(n):
   while n>0:
    err=ev(STEP,min(n,60));assert not err,err;n-=60;pg.wait_for_timeout(25)
  def cap(n): (O/(n+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  ev('''()=>{stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;boss=null;bossActive=false;subBoss=null;subBossActive=false;
    enemies=[];eBullets=[];pBullets=[];powerups=[];run.pilot='cole';run.weapon=4;run.wvars=run.wvars||{};run.wvars[4]='flamethrower';
    player.x=VW/2;player.y=VH*.8;player.invuln=1e9;
    for(let i=0;i<8;i++)XART.rdy('enemy_burn_0922_'+i);
    for(let i=0;i<4;i++)XART.rdy('nfw2_'+i);
    XART.rdy('magma_orb_0918');}''')
  pg.wait_for_function("()=>Array.from({length:8},(_,i)=>XART.rdy('enemy_burn_0922_'+i)).every(Boolean)&&XART.rdy('nfw2_2')&&XART.rdy('magma_orb_0918')")
  # Actual held flame collision ignites a live spawned target.
  ev('''()=>{spawnEnemy('tank',player.x,player.y-100);window.victim=enemies[enemies.length-1];
    victim.hp=victim.maxhp=500;victim.fireCd=999;victim.vx=victim.vy=0;flameFire(3);}''')
  step(5)
  r['flameContact']=ev('()=>({burn:victim._burn,palette:victim._burnPalette,hp:victim.hp})')
  cap('flame_contact')
  # Apply forged fire through the real infusion hit boundary, then change held weapon.
  r['retention']=ev('''()=>{dkIgnite(victim,{_inf:'toxic'});let phase=victim._burnPhase;
    run.weapon=0;victim.x+=50;let col=victim._burnPalette;
    enemyBurnApply(victim,2);return {toxic:col,fire:victim._burnPalette,phaseStable:phase===victim._burnPhase};}''')
  r['damageTick']=ev('''()=>{pBullets=[];_dmgBullet=null;let hp=victim.hp;victim._burnTick=0;dkBurnTick(victim,.1);return {before:hp,after:victim.hp};}''')
  r['excluded']=ev('''()=>{const e={_boss:true,w:100,h:100};dkIgnite(e);return !(e._burn>0);}''')
  # Native gameplay view: differing hull sizes, all normal orange burn.
  ev('''()=>{enemies=[];pBullets=[];particles=[];
    ['tank','htank','scout'].forEach((kind,i)=>{spawnEnemy(kind,camLeftX()+110+i*130,210+i*45);
      const e=enemies[enemies.length-1];e.hp=e.maxhp=500;e.fireCd=999;e.vx=e.vy=0;dkIgnite(e);e._burn=9;});}''')
  step(8)
  pg.wait_for_timeout(500)
  step(2);cap('enemy_burn_gameplay')
  for i in range(8):
   ev('(i)=>{efxClock=i/14;for(const e of enemies)e._burnPhase=0;}',i)
   step(1);cap('loop_'+str(i))
  # Source and mapped colors resolved by XART and the actual game context.
  ev('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#131820';ctx.fillRect(0,0,cv.width,cv.height);
    const palette=['#ff6924',INFUSIONS.toxic.body,INFUSIONS.water.body,INFUSIONS.dark.body];
    for(let row=0;row<4;row++)for(let i=0;i<8;i++){
      const k='enemy_burn_0922_'+i;const im=xartPalette(k,palette[row])||XART.get(k);
      ctx.drawImage(im,10+i*115,15+row*150,110,110);}
    ctx.drawImage(xartPalette('nfw2_2','#ff6924'),120,650,70,240);
    ctx.drawImage(XART.get('magma_orb_0918'),320,670,180,180);ctx.restore();}''')
  cap('palette_and_weapons')
  r['expiry']=ev('''()=>{pBullets=[];for(const e of enemies)e._burn=0;
    let calls=0;const draw=ctx.drawImage;ctx.drawImage=function(){calls++;return draw.apply(this,arguments);};
    // Isolate status rendering from unrelated world effects.
    geysers=[];efxBursts=[];const vents=s2VentDraw;s2VentDraw=()=>{};
    try{efxDraw();}finally{ctx.drawImage=draw;s2VentDraw=vents;}return calls===0;}''')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert r['flameContact']['burn']>0 and r['flameContact']['palette']=='#ff6924'
assert r['retention']=={'toxic':'#8de23a','fire':'#ff6924','phaseStable':True}
assert r['damageTick']['after']<r['damageTick']['before']
assert r['excluded']
assert r['expiry']
