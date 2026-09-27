"""Native damage routes, field reaction timing, ground anchors, and projectile pixels."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from probe_late_game_0927 import SETUP
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/late_game_0927');report={};errors=[];port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1100})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF);pg.wait_for_timeout(50)
  report['damage']=[]
  for case,(mini,kind) in enumerate([(True,'voidhorizon'),(False,'tidalfusion'),(False,'tidalfusion')]):
   pg.evaluate(SETUP,{'stage':9,'kind':kind,'mini':mini,'diff':'normal'})
   pg.evaluate('side=>{window.contractSide=side}', 'R' if case==2 else 'L')
   row=pg.evaluate(r'''mini=>{
    const b=testActor;for(let i=0;i<130;i++)if(mini)updateSubBoss(1/60);else updateBoss(1/60);
    const target=mini?b._s9rift.core:contractSide==='R'?b._s9fusion.right:b._s9fusion.left,hp=target.hp;
    run.spaceMode=true;run.spaceLevels=[5,5,5];player.x=target.x;player.y=VH-70;spaceVolleyFire();
    for(let i=0;i<160;i++){for(const p of pBullets)if(!p.dead)spaceBulletTick(p,1/60);pBullets=pBullets.filter(p=>!p.dead);}
    return {kind:b.kind,side:mini?null:contractSide,before:hp,after:target.hp,damaged:target.hp<hp};
   }''',mini);report['damage'].append(row)
  pg.evaluate(SETUP,{'stage':9,'kind':'tidalfusion','mini':False,'diff':'normal'})
  report['fusionDamage']=pg.evaluate(r'''()=>{
   const b=testActor;for(let i=0;i<130;i++)updateBoss(1/60);
   for(const w of [b._s9fusion.left,b._s9fusion.right]){b._s9fusion.hit=w;s9FusionHit(b,1e6);}
   for(let i=0;i<200;i++)updateBoss(1/60);
   const hp=b.hp;run.spaceMode=true;run.spaceLevels=[5,5,5];player.x=b.x;player.y=VH-70;spaceVolleyFire();
   for(let i=0;i<160;i++){for(const p of pBullets)if(!p.dead)spaceBulletTick(p,1/60);pBullets=pBullets.filter(p=>!p.dead);}
   return {phase:b._s9fusion.phase,before:hp,after:b.hp,damaged:b.hp<hp};
  }''')
  report['reactions']=[]
  for diff in ['normal','hard','furious']:
   pg.evaluate(SETUP,{'stage':3,'kind':'frostcruiser','mini':True,'diff':diff})
   row=pg.evaluate(r'''()=>{
    boss=null;subBoss=null;bossActive=false;subBossActive=false;bossWarned=true;subBossDone=true;stagePlan=[];spawnClock=9999;waveIdx=999;
    eBullets=[];pBullets=[];enemies=[];const e=spawnEnemy('sharddart',worldWidth()/2,125,{});e.hp=e.maxhp=10000;
    player.x=e.x;player.y=VH-70;const positions=[];let onset=null;
    for(let i=0;i<130;i++){
     if(i===55){e._ai27.cd=0;pBullets.push({kind:'mg',x:e.x,y:e.y+110,vx:0,vy:-5,w:4,h:12,dmg:1,t:0});}
     if(i===95)hitEnemy(e,1,true);
     updatePlay(1/60);if(e._ai27.read>0&&onset==null)onset=i/60;
     positions.push({x:e.x,y:e.y,dx:e._ai27.dx,flinch:e._ai27.flinch});
    }
    return {diff:diffKey,finite:positions.every(p=>Number.isFinite(p.x+p.y)),amp:e.amp,readAt:onset,dodgeDistance:positions.reduce((s,p)=>s+Math.abs(p.dx||0),0),hitReaction:positions.some(p=>p.flinch>0),reactions:e._ai27.reactions};
   }''');report['reactions'].append(row)
  pg.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','mini':False,'diff':'normal'})
  report['rivals']=pg.evaluate(r'''()=>{const b=testActor;for(let i=0;i<240;i++)rebelSquadTick(b,1/60);
   const q=b._rebels.ships[0];q.shield=q.shieldMax=12;b._rebels.hit=0;const before=q.shield;rebelSquadDamage(b,before);const initial=q.stun;
   rebelSquadTick(b,.1);return {shieldBroken:q.shield===0,stunInitial:initial,stunAfter:q.stun,retained:q.stun>.7};}''')
  pg.evaluate(SETUP,{'stage':7,'kind':'sludgeemperor','mini':False,'diff':'normal'})
  report['wardenEnding']=pg.evaluate(r'''()=>{const b=testActor;for(let i=0;i<700;i++)updateBoss(1/60);
   b._s7warden.final.phase='fight';b._s7warden.noHit=false;s7WardenHit(b,b.maxhp*2,b.x,b.y);
   const states=[];for(let i=0;i<500;i++){updateBoss(1/60);const phase=b._s7warden.final.phase;if(!states.includes(phase))states.push(phase);}
   return {states,finished:b._s7warden.final.finished,state};}''')
  pg.evaluate(SETUP,{'stage':7,'kind':'dualscoopdredger','mini':True,'diff':'normal'})
  report['mineTravel']=pg.evaluate(r'''()=>{const b=testActor;for(let i=0;i<100;i++)updateSubBoss(1/60);
   late27Init(b,'dredger');late27Set(b,'mine-gate');late27Emit(b);const q=eBullets.find(p=>p._wardenTravel);let maxStep=0;
   b.fireCd=999;late27Set(b,'recover');stagePlan=[];enemies=[];pBullets=[];
   for(let i=0;i<76;i++){const x=q.x,y=q.y;updatePlay(1/60);maxStep=Math.max(maxStep,Math.hypot(q.x-x,q.y-y));}
   return {maxStep,anchored:q._wardenAnchored,atAnchor:Math.hypot(q.x-q._wardenAnchor.x,q.y-q._wardenAnchor.y)<.01};}''')
  pg.evaluate('()=>{late27Warm();for(let i=0;i<12;i++)XART.rdy("s7spore_"+i);}')
  pg.wait_for_function('()=>Object.values(S9A).map(r=>XART.rdy(r[0]+"_3")).every(Boolean)&&XART.rdy("s7spore_3")',timeout=60000)
  data=pg.evaluate(r'''()=>{
   const oldW=ctx.canvas.width,oldH=ctx.canvas.height;ctx.canvas.width=1000;ctx.canvas.height=660;ctx.setTransform(1,0,0,1,0,0);
   ctx.fillStyle='#16232c';ctx.fillRect(0,0,1000,660);ctx.font='16px monospace';const invalid=[],rows=[],original=ctx.drawImage;
   ctx.drawImage=function(...args){if(args.slice(1).some(n=>!Number.isFinite(n)))invalid.push(args.slice(1));return original.apply(this,args);};
   Object.keys(S9A).forEach((kind,i)=>{const x=(i%5)*200+100,y=Math.floor(i/5)*200+115;
    ctx.fillStyle='white';ctx.fillText(kind,x-70,y-70);ctx.save();ctx.translate(x,y);ctx.scale(2,2);
    const drew=s9aProjectileDraw({_s9a:kind,x:0,y:0,vx:0,vy:1,t:3.1/13});ctx.restore();rows.push({kind,drew});});
   const key='s7spore_3',im=XART.get(key);ctx.drawImage(im,45,480,100,100);ctx.fillStyle='white';ctx.fillText('Dredger spore',40,460);
   ctx.drawImage=original;const png=ctx.canvas.toDataURL();ctx.canvas.width=oldW;ctx.canvas.height=oldH;return {png,invalid,rows};
  }''');(out/'ordnance.png').write_bytes(base64.b64decode(data.pop('png').split(',')[1]));report['art']=data
  report['errors']=errors;(out/'contracts.json').write_text(json.dumps(report,indent=2));br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert all(r['damaged'] for r in report['damage']) and report['fusionDamage']['damaged']
assert report['rivals']['retained']
assert report['wardenEnding']['finished'] and 'escape' in report['wardenEnding']['states']
assert report['mineTravel']['anchored'] and report['mineTravel']['atAnchor'] and report['mineTravel']['maxStep']<12
assert all(r['finite'] and r['dodgeDistance']>20 and r['hitReaction'] for r in report['reactions'])
assert not report['art']['invalid'] and all(r['drew'] for r in report['art']['rows'])
