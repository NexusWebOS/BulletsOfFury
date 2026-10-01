import sys,json,base64,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
OUT=ROOT/'_shots/repair_0930';OUT.mkdir(parents=True,exist_ok=True);results=[];errors=[]
def ok(v,n,d=None):
 results.append(dict(ok=bool(v),name=n,detail=d));print(('OK ' if v else 'FAIL ')+n,d or '',flush=True)
def grab(p,n):
 (OUT/(n+'.png')).write_bytes(base64.b64decode(p.evaluate("() => cv.toDataURL('image/png')").split(',')[1]))
SETUP="""c=>{ht27Stop();diffKey=c.diff||'furious';DIFF=DIFFS[diffKey];run.pilot='yuri';run.mode='campaign';beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;
 stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;l5Rocks=[];return true;}"""
port,stop=sh.serve(str(ROOT))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1100})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' or 'draw error' in m.text else None)
 p.goto('http://127.0.0.1:%s/index.html'%port,timeout=120000);p.wait_for_function('()=>(window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
 p.evaluate(SETUP,{'stage':6})
 p.evaluate("() => {for(const k of ['shield','chaingun_mount_yuri_left','chaingun_mount_yuri_right','chaingun_barrel_top','chaingun_round',...['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water'].map(x=>'orb_'+x)])XART.rdy(REPAIR30_ART[k].key);}")
 p.wait_for_function("() => ['shield','chaingun_mount_yuri_left','chaingun_mount_yuri_right','chaingun_barrel_top','chaingun_round'].every(k=>XART.rdy(REPAIR30_ART[k].key))")
 p.evaluate("() => {run.weapon=7;run.wlevel=4;run.shield=3;player.x=VW/2;player.y=VH-120;player.invuln=0;player._spawnClearT=2;run._chainRev=1;chaingunPlayerFire(4);drawWorld(0);}");grab(p,'shield_chaingun')
 r=p.evaluate("() => {let ys=[];for(const lv of [1,2,3,4,5]){pBullets=[];chaingunPlayerFire(lv);ys.push({lv,damage:pBullets[0].dmg,w:pBullets[0].w,color:wlvGlow(lv),dps:pBullets.reduce((s,b)=>s+b.dmg,0)/CHAINGUN_LV.cad[lv-1]});}return ys;}")
 ok(all(r[i]['dps']>r[i-1]['dps'] for i in range(1,5)) and all(q['w']>=7 for q in r),'chaingun wider and damage scales upward',r)
 r=p.evaluate("() => {player.invuln=100;player._spawnClearT=2;player._spin=null;player.roll=null;player.somer=null;return chaingunMountsVisible();}")
 ok(r,'respawn grace keeps pod visibility matched to ship')
 r=p.evaluate("""() => {let hits=[];const old=ctx.drawImage;ctx.drawImage=function(im,...a){hits.push(a);return old.call(this,im,...a);};
 const m1=chaingunMountPoints();chaingunMountsDraw(.016);player.x+=77;player.y-=33;const at=hits.length;chaingunMountsDraw(.016);const m2=chaingunMountPoints();ctx.drawImage=old;
 return {blits:hits.length,dx:m2[0].x-m1[0].x,dy:m2[0].y-m1[0].y};}""")
 ok(r['blits']>=8 and abs(r['dx']-77)<1e-6 and abs(r['dy']+33)<1e-6,'both modular pods follow live ship coordinates',r)
 # Draw all authored orb families at their actual gameplay size.
 p.wait_for_function("() => ['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water'].every(x=>XART.rdy(REPAIR30_ART['orb_'+x].key))")
 r=p.evaluate("""() => {drawWorld(0);let count=0;['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water'].forEach((el,i)=>{if(repair30OrbDraw({kind:'orb',_inf:el,x:80+(i%3)*150,y:100+Math.floor(i/3)*95,w:22,t:.32,spin:.2}))count++;});return count;}""")
 ok(r==9,'all nine orb families draw authored frames');grab(p,'orb_families')
 p.evaluate(SETUP,{'stage':4})
 r=p.evaluate("""() => {spawnSubBoss('olivewarden');subBossActive=true;const b=subBoss;b.enter=false;b._noHit=true;const S=b._s4war;S.summoned=true;
 const d={x:b.x,y:b.y,size:92,hp:400,maxhp:400,dead:false,active:1,side:-1};S.drones=[d];
 const bullet={x:d.x,y:d.y,w:8,h:28,dmg:11,kind:'mg',dead:false};_dmgBullet=bullet;
 const routed=repair30DroneBullet(bullet,false,.016),after=d.hp;hitSubBoss(7,d.x,d.y);_dmgBullet=null;return {routed,dead:bullet.dead,first:after,second:d.hp,flash:d.flash,parentNoHit:b._noHit};}""")
 ok(r['routed'] and r['dead'] and r['first']<400 and r['second']<r['first'] and r['flash']>0,'overlapping helper receives bullets despite parent invulnerability',r)
 for route in ['regular','hammer','hama']:
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,{'stage':5,'diff':diff})
   r=p.evaluate("""c=>{if(c.route==='regular'){spawnBoss('chromehammer');bossActive=true;}else{ht27Pending=true;if(c.route==='hama')hamaPending=true;startRun(5);const d=boss._hammerTime;d.mode='attack';d.locked=false;d.shield=false;d.musicStarted=true;d.clock=40;}
    boss.enter=false;boss._noHit=false;boss.x=VW/2;boss.y=VH*.34;const h=boss._hammer;h.balance0922=true;h.state='warn';h.t=0;h.frArmor=null;
    if(boss._hammerTime)boss._hammerTime.mode='attack';hammerBossTick(boss,.016);
    return {state:h.state,armor:!!h.frArmor,ratio:h.frArmor?h.frArmor.hp/boss.maxhp:0,hama:!!(boss._hammerTime&&boss._hammerTime.hama)};}""",{'route':route})
   ok(r['state']=='fr_activation' and r['armor'] and (route!='hama' or r['hama']),route+' '+diff+' starts Chromium sequence',r)
   p.wait_for_function("() => XART.rdy('arch_storm_charge_0926') && XART.rdy('arch_hammer_lightning_0926')")
   r=p.evaluate("""() => {let keys=[];const xg=XART.get;XART.get=function(k){keys.push(k);return xg.call(this,k);};const h=boss._hammer;h.t=1.65;drawWorld(0);XART.get=xg;
    return {raised:keys.includes('arch_storm_charge_0926'),lightning:keys.includes('arch_hammer_lightning_0926'),state:h.state};}""")
   ok(r['raised'] and r['lightning'] and r['state']=='fr_activation',route+' '+diff+' renders raised hammer and lightning',r)
   if diff=='furious':grab(p,route+'_armor')
   r=p.evaluate("""() => {for(let i=0;i<90;i++)hammerBossTick(boss,1/60);const h=boss._hammer;const active=h.frArmor.activated;
    fr27Restore(boss,.1,false,true);fr27Reflect(boss,h.frArmor,1/60);
    return {activated:active,state:h.state,barrier:h.frArmor.barrier,breakHP:h.recovery.coreHP};}""")
   ok(r['activated'] and (diff!='normal' or (r['barrier']==0 and r['breakHP']==12)),route+' '+diff+' completes armor / Normal heal is exposed',r)
 for route in ['hammer','hama']:
  p.evaluate(SETUP,{'stage':5,'diff':'furious'})
  r=p.evaluate("""route=>{ht27Pending=true;hamaPending=route==='hama';startRun(5);boss.enter=false;boss._noHit=false;boss.hp=boss.maxhp*.5;
   const d=boss._hammerTime;d.mode='attack';d.locked=false;d.shield=false;d.musicStarted=true;d.clock=40;d.attack=0;if(d.hama)d.hama.attacks=0;
   const states=[];for(let i=0;i<(d.hama?16:8);i++){ht27Attack(boss,d);if(d.mode==='attack')states.push(boss._hammer.state);}
   hammerStormStart(boss);const protectedHeal=ht27CombatSequence(boss);return {states,protectedHeal};}""",route)
  ok(all(x in r['states'] for x in ['warn','spin','whirl_warn','curl','spell','chain_warn','storm_raise','mega_charge']) and r['protectedHeal'],route+' retains all eight combat families and protects active recovery from music cuts',r)
 ok(not errors,'no browser errors',errors[:10]);b.close()
stop();(OUT/'results.json').write_text(json.dumps(results,indent=2));sys.exit(0 if all(r['ok'] for r in results) else 1)
