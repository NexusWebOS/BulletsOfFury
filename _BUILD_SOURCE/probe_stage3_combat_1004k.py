"""Real Chromium checks and pixel evidence for the Oct 4 Stage 3 recording pass."""
from pathlib import Path
import sys, json, base64
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage3_combat_1004k';O.mkdir(parents=True,exist_ok=True)
errors=[];report={'checks':[],'shots':[]};port,stop=sh.serve(str(R))
SETUP="""c=>{ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.pilot=c.pilot||'yuri';run.mode='campaign';run._freezerL2Cleared=false;beginStage(c.stage||3);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;thaw=null;s6Opening=null;s6Wing=null;stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;groundTargetingReset();tb28Reset();polishLanes=[];stageTimer=0;s3kResidue=[];player.x=worldWidth()/2;player.y=VH-110;camX=player.x-VW/2;player.invuln=1e9;if(c.kind){if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);window.B=c.mini?subBoss:boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=B._er26.home;B._drawY=B.y;B._er26.neutralOpening=false;B._er26.nuclearRevealed=true;B._er26.form="ice";B._s3Nuclear={mode:"ice",introDone:true};B._scene=null;}return true;}"""
def check(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){storySkip();BOFCinematicDirector.cancel();'+expr+'}}',min(20,n-i));p.wait_for_timeout(10)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['shots'].append(name+'.png')
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1200,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate('()=>{fb1002Warm();er26Warm();wm26Warm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);for(const k of ["efx_burst_fire","efx_burst_ice",...PILOTS.map(q=>"ship_"+q.key)])XART.rdy(k);}')
  p.wait_for_function('()=>XART.rdy("mr27_rime")&&XART.rdy("efx_burst_fire")&&XART.rdy("efx_burst_ice")&&XART.rdy("ndk_muz_0")&&XART.rdy("fb1002_frost_hull")',timeout=120000,polling=50)
  # Actual bullet update paths, including the formerly separate rising ground shot collision.
  for kind in ['mg','groundup','shell']:
   for weapon in ['mg','spread','beam','flame','orb','missile']:
    p.evaluate(SETUP,{'stage':1})
    p.evaluate('''c=>{const x=player.x,y=player.y-135;if(c.kind==='mg'){eMG(x,y,Math.PI/2,0);window.Q=eBullets.at(-1);Q.vx=Q.vy=0;}else if(c.kind==='groundup'){eGroundUp(x,y,true);window.Q=eBullets.at(-1);Q.vx=Q.vy=0;}else{window.Q=eShootT(x,y,Math.PI/2,0,'shell',{w:8,h:16,silent:true});Q._shootable=true;}pBullets=[{x,y,vx:0,vy:0,w:22,h:32,dmg:5,t:0,kind:c.weapon,bot:player.y,top:PLAY.y,life:1,lv:5,_hit:[],_ht:1,spd:0,ang:-Math.PI/2}];}''',{'kind':kind,'weapon':weapon})
    frames(p,1);check(p.evaluate('()=>!Q.dead&&Q._weaponProof'),kind+' survives '+weapon)
  p.evaluate(SETUP,{'stage':1,'pilot':'axel'})
  check(p.evaluate('''()=>{run._megaShield=true;run.shield=3;eMG(player.x,player.y-20,Math.PI/2,2);const q=eBullets.at(-1);s3kOrdnanceRules(q);return axelMegaReflect(q)&&q._megaReflected;}'''),'Axel shield retains its gun-pellet reflection')
  p.evaluate(SETUP,{'stage':1})
  check(p.evaluate('''()=>{eMG(player.x,player.y-90,Math.PI/2,2);const q=eBullets.at(-1);s3kOrdnanceRules(q);return chromeMirror(q.x,q.y,30,1)===1;}'''),'chrome defense retains its gun-pellet reflection')
  p.evaluate(SETUP,{'stage':1})
  check(p.evaluate('''()=>{eMG(player.x,player.y-90,Math.PI/2,2);const q=eBullets.at(-1);s3kOrdnanceRules(q);detonateBomb({x:q.x,y:q.y});return !eBullets.includes(q);}'''),'bomb blast retains its gun-pellet clear')
  for elem in ['fire','ice']:
   for weapon in ['mg','spread','beam','flame','orb','missile']:
    p.evaluate(SETUP,{'kind':'frostcruiser','mini':True})
    p.evaluate('''c=>{er26Set(B,'recover');B._er26.dur=20;window.Q=er26Shot(B,'L',Math.PI/2,0,{large:true});Q._er26Art=c.elem;Q.x=player.x;Q.y=player.y-45;Q.vx=Q.vy=Q.spd=0;window.oldBursts=efxBursts.length;pBullets=[{x:Q.x,y:Q.y,vx:0,vy:0,w:22,h:32,dmg:5,t:0,kind:c.weapon,bot:player.y,top:PLAY.y,life:1,lv:5,_hit:[],_ht:1,spd:0,ang:-Math.PI/2}];}''',{'elem':elem,'weapon':weapon})
    frames(p,1);check(p.evaluate('()=>Q.dead&&Q._fbImpact1002&&efxBursts.length===oldBursts+1&&s3kResidue.at(-1).elem===Q._er26Art'),elem+' ball intercepted by '+weapon)
    if weapon=='spread':frames(p,5);shot(p,elem+'-interception')
  p.evaluate(SETUP,{'kind':'frostcruiser','mini':True})
  p.evaluate('''()=>{er26Set(B,'recover');B._er26.dur=20;window.Q=er26Shot(B,'L',Math.PI/2-.35,3.2,{});Q.x=player.x-150;Q.y=player.y-90;window.ballVelocity=[Q.vx,Q.vy];}''')
  frames(p,1);check(p.evaluate('()=>Math.abs(Q.vx-ballVelocity[0])+Math.abs(Q.vy-ballVelocity[1])<.0001'),'making elemental balls shootable preserves authored velocity')
  # Continuous weapons must use their actual authored collision shape, not a dummy bullet box.
  p.evaluate(SETUP,{'stage':1,'pilot':'cole'})
  p.evaluate('''()=>{run.weapon=4;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.wvars=[];run.wvars[4]='flamethrower';run.forge={};run.infusion=null;player.fireCd=0;pShoot();window.Q=eShootT(player.x,player.y-190,Math.PI/2,0,'s3mortar',{w:24,h:24,silent:true});Q._er26Art='ice';Q._energyOrdnance=true;Q._er26Draw=44;}''')
  frames(p,2);check(p.evaluate('()=>Q.dead&&Q._fbImpact1002&&pBullets.some(q=>q.kind==="flame")'),'real held flamethrower intercepts across its entire visible plume');shot(p,'real-flame-interception')
  p.evaluate(SETUP,{'kind':'cryospear'});p.evaluate('()=>{er26Set(B,"rime-orbit1004k");window.startHP=B.maxhp;}')
  frames(p,70);shot(p,'rime-orbit-warning')
  check(p.evaluate('()=>["gunL","gunR"].some(id=>Math.hypot(mr27Shape(B,id).x-S3K_BASE.shape(B,id).x,mr27Shape(B,id).y-S3K_BASE.shape(B,id).y)>30)'),'actual turret geometry moves into orbit')
  frames(p,50);shot(p,'rime-orbit-stream')
  check(p.evaluate('()=>eBullets.some(q=>q._coldTracer1002)&&eBullets.filter(q=>q._coldTracer1002).every(q=>q._weaponProof)'),'orbit uses real undestroyable gun streams')
  check(p.evaluate('()=>{const q=mr27Shape(B,"gunL");return mr27At(B,q.x,q.y)==="gunL";}'),'orbiting gun remains hittable')
  p.evaluate('''()=>{window.Gun=mr27Part(B,'gunR');window.gunHP=Gun.hp;const q=mr27Shape(B,'gunR');pBullets=[{x:q.x,y:q.y,vx:0,vy:0,w:12,h:20,dmg:40,t:0,kind:'mg'}];}''')
  frames(p,1);check(p.evaluate('()=>Gun.hp<gunHP'),'actual player shot damages a deployed orbital turret')
  p.evaluate('()=>{er26Set(B,"recover");B._er26.dur=10;}');frames(p,110)
  check(p.evaluate('()=>!mr27Part(B,"gunL")._s3kPos&&B.maxhp===startHP'),'turrets return without changing HP')
  p.evaluate('()=>{eBullets=[];er26Set(B,"rime-missile1004k");}');frames(p,80);shot(p,'rime-missile-volley')
  check(p.evaluate('()=>eBullets.filter(q=>q.kind==="emissile").length===4'),'four real missiles launch from paired rocket banks')
  p.evaluate('()=>{B._l23Beam=null;er26Set(B,"cannon-relay");}');frames(p,30);shot(p,'rime-laser-charge')
  before=p.evaluate('()=>B._l23Beam.angles[0]');p.evaluate('()=>player.x-=130;');frames(p,25)
  check(abs(p.evaluate('()=>B._l23Beam.angles[0]')-before)>.05,'charged laser FOV tracks during early warmup')
  frames(p,110);locked=p.evaluate('()=>B._l23Beam.angles.slice()');p.evaluate('()=>player.x+=200;');frames(p,8)
  check(p.evaluate('a=>B._l23Beam.angles.every((v,i)=>Math.abs(v-a[i])<.001)',locked),'laser locks its heading before release')
  frames(p,45);shot(p,'rime-laser-release')
  p.evaluate(SETUP,{'kind':'frostcruiser','mini':True});p.evaluate('()=>{er26Set(B,"elite-ram1004k");window.oldY=B.y;}');frames(p,55);shot(p,'cruiser-charge-warning')
  check(p.evaluate('()=>B.y===oldY&&!B._er26.s3kDash'),'miniboss holds through charge warning')
  frames(p,33);shot(p,'cruiser-charge-dash')
  check(p.evaluate('()=>B._er26.s3kDash&&B.y>oldY+50'),'miniboss makes an actual high-speed charge')
  # Render every current pilot with the real game drawImage and fitted muzzle anchor.
  p.evaluate(SETUP,{'stage':1})
  r=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=900;c.height=360;const g=c.getContext('2d');g.fillStyle='#172631';g.fillRect(0,0,c.width,c.height);g.imageSmoothingEnabled=false;const result=[];
    PILOTS.forEach((q,i)=>{run.pilot=q.key;player._bank=0;player.x=50+i*100;player.y=150;const key=shipGlowKey('ship_'+q.key);XART.rdy(key);const im=XART.get(key);if(!im)return;const nose=wm26PlayerNose(),h=120,w=h*(im.width||im.naturalWidth)/(im.height||im.naturalHeight);g.drawImage(im,player.x-w/2,150-h/2,w,h);g.fillStyle='white';g.fillText(q.key,player.x-25,30);wm26Draw(g,'spread',player.x+(nose.x-player.x)*2,150+(nose.y-player.y)*2,-Math.PI/2,.4,68,null);result.push({key:q.key,nose,offset:nose.y-player.y});});return {png:c.toDataURL().split(',')[1],result};}''')
  (O/'spread-all-pilots.png').write_bytes(base64.b64decode(r['png']));report['muzzleAnchors']=r['result'];report['shots'].append('spread-all-pilots.png')
  check(len(r['result'])==9 and all(-31<=q['offset']<=-15 for q in r['result']),'all nine spread flashes attach to authored noses')
  for kind,mini in [('frostcruiser',True),('cryospear',False)]:
   p.evaluate(SETUP,{'kind':kind,'mini':mini});p.evaluate('()=>{B._er26.neutralOpening=false;window.seen=new Set();window.shots=0;}')
   frames(p,2400,'updatePlay(1/60);seen.add(B._er26.mode);shots=Math.max(shots,eBullets.length);drawWorld(1/60);')
   report[kind] = p.evaluate('()=>({modes:[...seen],shots,hp:B.hp,max:B.maxhp})');shot(p,kind+'-sustained')
   check(report[kind]['shots']>0 and any(s.endswith('1004k') for s in report[kind]['modes']),kind+' completes live old and new attacks')
  check(not errors,'zero page and console errors');b.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
