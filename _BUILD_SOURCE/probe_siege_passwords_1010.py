"""Real Chromium password entry, modular weapons, live attacks and defeat."""
from pathlib import Path
import json,sys,base64,io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/siege_passwords_1010';OUT.mkdir(exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def shot(p,name):
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);if(typeof fb9HudSplit==="function")fb9HudSplit();}')
 p.screenshot(path=str(OUT/(name+'.png')))
def step(p,seconds):
 for _ in range(round(seconds*10)):
  p.evaluate('()=>{for(let i=0;i<6;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);if(typeof fb9HudSplit==="function")fb9HudSplit();}')
  p.wait_for_timeout(5)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1180,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('ASSETS.ready&&typeof SG10!=="undefined"',polling=50);p.evaluate(shoot.TRAP_RAF)
  for code,unit in [('sonic','sonic'),('ordos','deviator'),('hark','devastator')]:
   p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;setState(GS.PASSWORD);drawPassword.typing=true;pwInput="";diffKey="normal";Input.clearTaps?.();}')
   p.keyboard.type(code);p.keyboard.press('Enter');p.evaluate('drawPassword(0)')
   check(code+' typed from keyboard enters difficulty selection',p.evaluate('state===GS.DIFF&&ON5.pending?.stage===1&&PENDING_STAGE===1'))
   p.evaluate('()=>{pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");startRun(PENDING_STAGE);player.invuln=999;player.dead=false;player.out=false;}')
   p.wait_for_function('subBoss?._sg10&&sg10Ready(subBoss)',polling=50);p.evaluate('()=>{Input.clearTaps?.();}')
   step(p,4)
   check(code+' live production miniboss arrives intact',p.evaluate('(unit)=>state===GS.PLAY&&run.stage===1&&subBossActive&&subBoss?._sg10.unit===unit&&!subBoss.enter&&Object.values(subBoss._sg10.parts).every(q=>!q.gone)',unit))
   shot(p,code+'-arrival')
   check(code+' reuses the actual Level 1 miniboss HUD',p.evaluate('()=>{drawSubBossBar(subBoss);return subBoss.maxhp>0&&subBoss.hp/subBoss.maxhp>0&&Object.keys(EH7_ART).includes("stage_01");}'))
   # Test the engine's actual projectile route at a visible metal pixel.
   for weapon in ['mg','spread','laser','missile','shard']:
    q=p.evaluate('''()=>{const b=subBoss,m=SG10_RIG.find(m=>m.id==="trackL"),a=sg10Box(b,m),mask=sg10Mask(a.a);let best=null;
     for(let y=a.a.bounds[1];y<a.a.bounds[3]&&!best;y++)for(let x=a.a.bounds[0];x<a.a.bounds[2];x++)if(mask[y*a.a.w+x]>=160){const px=a.ox+(x+.5)*a.k,py=a.oy+(y+.5)*a.k;if(sg10At(b,px,py)==="trackL"){best={x:px,y:py,hp:b.hp};break;}}return best;}''')
    check(code+' '+weapon+' has a visible module target',bool(q))
    if not q:continue
    p.evaluate('(q)=>{pBullets=[{kind:q.kind,x:q.x,y:q.y,vx:0,vy:0,w:8,h:12,dmg:8,lv:1,t:0,seat:1,life:2}];}',{**q,'kind':weapon})
    step(p,.1)
    check(code+' '+weapon+' damages the module through gameplay collision',p.evaluate('(hp)=>subBoss.hp<hp',q['hp']))
   # Held beam: finite geometry and the normal engine branch, not hit injection.
   q=p.evaluate('()=>{const b=subBoss,q=sg10Box(b,SG10_RIG.at(-1));return{x:(q.l+q.r)/2,hp:b.hp};}')
   p.evaluate('(q)=>{player.x=q.x;pBullets=[{kind:"beam",x:q.x,y:player.y-14,top:PLAY.y,bot:player.y-14,w:14,h:300,dmg:6,t:0,life:1,_sbt:0,_hit:[],seat:1}];}',q);step(p,.1)
   check(code+' held laser damages finite exposed geometry',p.evaluate('(hp)=>subBoss.hp<hp',q['hp']))
   p.evaluate('pBullets=[]')
   # Retina targeting must follow the exact live part and retire with that part.
   q=p.evaluate('()=>{const b=subBoss,t=retinaBossTargets(b).find(t=>t._retinaId==="podL"),hp=b._sg10.parts.podL.hp;retinaMissileDamage(t,12,{kind:"missile",dmg:12});return{hp,now:b._sg10.parts.podL.hp,valid:retinaTargetValid(t)};}')
   check(code+' missile Retina targets are live and damage the selected module',q['valid'] and q['now']<q['hp'],q)
   # The incoming orb rework must connect with these new modular encounters.
   if p.evaluate('typeof FB10_ORB!=="undefined"'):
    for variant in ['iceorb','fireorb']:
     info=p.evaluate('''(variant)=>{const b=subBoss,point=sg10Point(b,SG10_RIG[4]);window.__siegeOrbFixture={
      pilot:run.pilot,weapon:run.weapon,wlevel:run.wlevel,wlevels:[...run.wlevels],wvars:[...(run.wvars||[])],
      x:player.x,y:player.y,hp:b.hp,parts:Object.fromEntries(Object.entries(b._sg10.parts).map(([k,v])=>[k,{...v}]))};
      run.pilot="cole";run.weapon=5;run.wlevel=3;run.wlevels[5]=3;run.wvars[5]=variant;player._orbCd=0;pBullets=[];pShoot();
      const orb=pBullets.find(q=>q.kind==="orb");if(orb){orb.x=point.x;orb.y=point.y+2;window.__siegeOrb=orb;}
      return {launched:!!orb,hp:b.hp};}''',variant)
     check(code+' '+variant+' launches through the incoming weapon code',info['launched'])
     step(p,.1)
     check(code+' '+variant+' damages live modules through the merged orb collision',p.evaluate('(hp)=>subBoss.hp<hp',info['hp']))
     p.evaluate('''()=>{const q=window.__siegeOrbFixture;run.pilot=q.pilot;run.weapon=q.weapon;run.wlevel=q.wlevel;run.wlevels=q.wlevels;run.wvars=q.wvars;
      player.x=q.x;player.y=q.y;player._orbCd=0;subBoss.hp=q.hp;subBoss._sg10.parts=q.parts;pBullets=[];sg10Sync(subBoss);}''')
   # Current-silhouette white hits; native drawImage on real decoded frames.
   p.evaluate('()=>{subBoss.flash=.13;for(const v of Object.values(subBoss._sg10.parts))v.flash=.13;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);sg10Draw(subBoss,false);}')
   im=np.array(Image.open(io.BytesIO(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))).convert('RGB'));mask=im.max(2)>120
   check(code+' all surviving modules flash white',mask.sum()>1000 and np.mean(np.ptp(im[mask].astype(int),axis=1)<3)>.98)
   # Observe a whole live attack book. Player protection is explicit QA only.
   event=p.evaluate('SG10.clock');step(p,15);shot(p,code+'-combat')
   info=p.evaluate('(n)=>({attacks:SG10.events.filter(q=>q.t>=n&&q.name==="attack").map(q=>q.kind),shots:SG10.events.filter(q=>q.t>=n&&q.name==="shot").length,bursts:SG10.events.filter(q=>q.t>=n&&q.name==="detonation").length})',event)
   check(code+' live fight fires authored projectiles and detonations',info['shots']>=6 and info['bursts']>=1,info)
   if unit=='sonic':check('Sonic includes its charged large-blast pattern','charge' in info['attacks'])
   elif unit=='deviator':check('Ordos includes staggered missile and lock patterns','missiles' in info['attacks'] or 'lock' in info['attacks'])
   else:check('Hark includes its alternating heavy cannon pattern','cannons' in info['attacks'])
   p.evaluate('()=>{sg10Break(subBoss,"weapon");subBoss._sg10.rest=0;sg10StartAttack(subBoss);}')
   check(code+' broken weapon retires its lock and main attack',p.evaluate('subBoss._sg10.attack.kind==="pods"&&!retinaBossTargets(subBoss).some(t=>t._retinaId==="weapon")'))
   step(p,.3);shot(p,code+'-weapon-break')
   check(code+' detached weapon spins without fading',p.evaluate('SG10.debris.some(q=>q.part==="weapon"&&Math.abs(q.spin)>0&&!Object.hasOwn(q,"alpha"))'))
   p.evaluate('sg10Death(subBoss)');step(p,.6);shot(p,code+'-defeat')
   check(code+' death keeps remaining delayed modules visible',p.evaluate('SG10.debris.length>0&&SG10.debris.every(q=>!Object.hasOwn(q,"alpha"))'))
   step(p,2.1);check(code+' cleared fight releases the Level 1 miniboss slot',p.evaluate('!subBoss&&!subBossActive&&subBossDone&&state===GS.PLAY'))
  # Defaults and pinned reference remain usable after all three special fights.
  check('Campaign Level 1 still uses its existing miniboss',p.evaluate('SUBBOSS[1].kind==="razorback"'))
  check('All new passwords are pinned exactly once with their tank names',p.evaluate('Object.keys(SG10.routes).every(c=>pc5Pages().flatMap(p=>p.rows).filter(r=>r[0]===c).length===1)'))
  br.close()
finally:stop()
check('No browser, console or asset errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'checks':checks,'errors':errors}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
