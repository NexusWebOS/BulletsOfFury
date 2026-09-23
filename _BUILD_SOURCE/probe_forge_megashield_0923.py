"""Real browser verification of one-time recipes, isolated level-one previews and Axel's bubble."""
import base64,json,sys,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/forge_megashield_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];results={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(TRAP_RAF)
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':False})
  pg.evaluate("()=>{story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;run.forge={};run.forgeForms={};achievementState.owned={};run.forgeElems={fire:1,ice:1};run.forgeCombos=5;player.invuln=0;}")
  results['recipes']=pg.evaluate("""()=>{const a=forgeCombine(0,'fire'),before=run.forgeCombos,b=forgeCombine(0,'fire'),after=run.forgeCombos,c=forgeCombine(0,'ice');
    run.forgeForms[0].fire.lv=5;run.forge[0]=run.forgeForms[0].fire;ensureForgeForms();const migrated=run.forge[0].lv;
    const balance=furiousBalance(),purchase=forgeLevelBuy('fire',0),unchanged=furiousBalance()===balance;
    const whip=forgeCombine(3,'fire');return {a,b,c,before,after,migrated,purchase,unchanged,whip,variant:run.wvars[3]};}""")
  assert results['recipes']=={'a':'ok','b':'owned','c':'ok','before':4,'after':4,'migrated':1,'purchase':'maxed','unchanged':True,'whip':'ok','variant':'firewhip'},results
  # Start from a hostile-to-preview live state. It must neither influence nor be changed by previews.
  pg.evaluate("()=>{run.weapon=7;run.wlevel=8;run.wlevels=WEAPONS.map(()=>8);run.spaceMode=true;run.stage=5;special={pilot:'maverick',t:9,mavCharging:true,mavCharge:2};run._chainHeat=1;run._chainOverheat=9;window.previews=[];window.liveBefore=JSON.stringify({run,player,special,pImpacts,explosions,smokeTrails});}")
  results['previews']={}
  for weapon in range(9):
   for element in [None,'fire','ice','lightning','prism','toxic','kinetic','chrome','water','dark']:
    key=f'{weapon}_{element or "bare"}'
    pg.evaluate("o=>{window.P=forgePreviewNew(o.w,o.e,5)}",{'w':weapon,'e':element})
    for batch in range(3):
     pg.evaluate("()=>{for(let i=0;i<50;i++)forgePreviewTick(P,200,180,1/60);forgePreviewDraw(P,0,0,200,180)}");pg.wait_for_timeout(25)
    data=pg.evaluate("()=>({level:P.lv,error:P.err,fired:P.fired,kinds:[...new Set(P.bullets.map(b=>b.kind))],count:P.bullets.length,effects:P.bursts.length,unchanged:liveBefore===JSON.stringify({run,player,special,pImpacts,explosions,smokeTrails})})")
    results['previews'][key]=data
    assert data['error'] is None and data['level']==1 and data['fired']>0 and data['unchanged'],(key,data)
    if weapon==3 and element=='fire':assert 'firewhip' in data['kinds'],data
  pg.evaluate("()=>{window.gallery=[['FIRE WHIP',3,'fire'],['MAGMA ORB',5,'fire'],['GLACIER ORB',5,'ice'],['VOID ORB',5,'dark'],['LIGHTNING SPHERE',8,'lightning'],['ICE LASER',3,'ice']].map(([name,w,e])=>({name,p:forgePreviewNew(w,e,1)}));}")
  for i in range(5):
   pg.evaluate("()=>{for(let i=0;i<15;i++)for(const q of gallery)forgePreviewTick(q.p,160,225,1/60);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);gallery.forEach((q,i)=>{const x=i%3*320,y=Math.floor(i/3)*490;forgePreviewDraw(q.p,x,y+35,320,440);ctx.fillStyle='#fff';ctx.font='18px monospace';ctx.fillText(q.name,x+160,y+24)});ctx.restore();}");pg.wait_for_timeout(100)
  def capture(name):
   (OUT/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")))
  capture('weapon_previews')
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':False})
  pg.evaluate("()=>{story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;player.invuln=0;player.x=240;player.y=390;run.weapon=0;run.wlevel=1;run.wlevels=WEAPONS.map(()=>1);run.spaceMode=false;run._chainHeat=0;run._chainOverheat=0;particles=[];efxBursts=[];pilotFx=[];floaters=[];zaps=[];startSpecial();floaters=[];}")
  pg.wait_for_function("()=>[0,1,2,3,4,5,6,7].every(f=>XART.rdy('axel_mega_shield_'+f))")
  pg.evaluate("()=>{shake=0;drawWorld(0)}");capture('axel_bubble_active')
  results['expiry']=pg.evaluate("()=>{updateSpecial(15.1);floaters=[];return {shield:run.shield,active:axelMegaShieldActive(),special:special};}")
  assert results['expiry']=={'shield':5,'active':True,'special':None},results['expiry']
  pg.evaluate("()=>{shake=0;drawWorld(0)}");capture('axel_bubble_after_15_seconds')
  results['saved']=pg.evaluate("()=>{const snapshot=campSnapshot();run._megaShield=false;run.shield=0;campApply(snapshot);return {shield:run.shield,active:axelMegaShieldActive()};}")
  assert results['saved']=={'shield':5,'active':True}
  results['reflect']=pg.evaluate("""()=>{const enemy={x:240,y:160,w:35,h:35,hp:20,dead:false};enemies=[enemy];
    const q={x:240,y:player.y-95,vx:0,vy:100,w:8,h:8,kind:'s1bullet',dmg:4};eBullets=[q];const hit=axelMegaReflect(q),shield=run.shield,surface=Math.abs(q.y-(player.y-axelMegaShieldRadius()-4))<.001;
    const real=hitEnemy;let damage=0;hitEnemy=(e,d)=>{damage+=d};for(let i=0;i<20&&!q.dead;i++)axelMegaReturnTick(q,1/60);hitEnemy=real;
    const returned=q.vy<0&&q._megaReflected;return {hit,shield,returned,damage,surface,dead:!!q.dead};}""")
  assert results['reflect']['hit'] and results['reflect']['shield']==4 and results['reflect']['returned'] and results['reflect']['damage']==4 and results['reflect']['surface'],results['reflect']
  results['charges']=pg.evaluate("""()=>{for(let i=0;i<4;i++){player._megaGrace=0;axelMegaReflect({x:player.x,y:player.y-30,vx:0,vy:3,w:6,h:6});}return {shield:run.shield,active:axelMegaShieldActive()};}""")
  assert results['charges']=={'shield':0,'active':False}
  results['coop']=pg.evaluate("""()=>{coopOn=true;run.pilot='axel';run._megaShield=false;run.shield=0;run2.pilot='axel';run2._megaShield=true;run2.shield=5;player2.dead=false;player2.x=350;player2.y=380;player2._megaGrace=0;
    const q={x:350,y:360,vx:0,vy:0,w:8,h:8};const hit=withSeat(2,()=>axelMegaReflect(q));const result={hit,p1:run.shield,p2:run2.shield,seat:q._megaSeat,returned:q._megaReflected};coopOn=false;return result;}""")
  assert results['coop']=={'hit':True,'p1':0,'p2':4,'seat':2,'returned':True},results['coop']
  # Exercise the actual Forge menu while equipped at level eight.
  pg.evaluate("()=>{run.stage=3;run.spaceMode=false;run.weapon=3;run.wlevel=8;run.wlevels=WEAPONS.map(()=>8);run.loadout=[3,0,1,2,4,5];run.forgeElems=Object.fromEntries(Object.keys(INFUSIONS).map(e=>[e,1]));forgeStart();forge.row=1;forge.sel=run.loadout.indexOf(3);forge.esel=forgeElemsFor(3).indexOf('fire');}")
  for batch in range(8):
   pg.evaluate("()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);for(let i=0;i<20;i++)drawForge(1/60);ctx.restore();}");pg.wait_for_timeout(100)
  capture('forge_firewhip_owned')
  results['menu']=pg.evaluate("()=>({level:forge.preview.lv,variant:forge.preview.variant,name:forgeComboName('fire',3),equipped:run.wlevel})")
  assert results['menu']=={'level':1,'variant':'firewhip','name':'FIRE WHIP','equipped':8},results['menu']
  assert not errors,errors
  results['errors']=errors;(OUT/'results.json').write_text(json.dumps(results,indent=2));print('PASS: 90 level-one previews; one-time recipes and legacy migration; persistent five-charge shield, swept reflection and return damage.');br.close()
finally:stop()
