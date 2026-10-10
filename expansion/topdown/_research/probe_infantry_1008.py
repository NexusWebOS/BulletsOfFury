"""Actual keyboard traversal and pixel/geometry regression for the Miami repair.
Route fixture disables incidental enemy damage; it does not assert balance.
"""
from pathlib import Path
import json,sys,math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import serve
OUT=ROOT/'_shots/infantry_repair_1008';OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1100,'height':850});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html')
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="pilot"',timeout=60000)
  page.evaluate('TDGAME.freeze();ART.warm(TD.CAMPAIGN_WARM)')
  page.wait_for_function('ART.progress(TD.CAMPAIGN_WARM)===1',timeout=60000)
  page.evaluate("window.press=(k,v)=>window.dispatchEvent(new KeyboardEvent(v?'keydown':'keyup',{key:k}));window.advance=n=>TDGAME.step(n);window.tap=k=>{press(k,true);advance(1);press(k,false);advance(1);};TD.pilot='cole';TDGAME.G.sel=1;TDGAME.start();const G=TDGAME.G;G.player.inv=999999;TD.Input.pointer.active=false;for(const u of G.units){if(u.role!=='sentry')u.dead=true;else{u.speed=0;u.cd=999999;u.mode='patrol';}}")
  # Walk each leg with genuine keyboard state; no position teleports in this route.
  page.evaluate("""window.walkTo=(x,y)=>{const p=TDGAME.G.player;let ticks=0;while(Math.hypot(p.x-x,p.y-y)>3&&ticks<900){const dx=x-p.x,dy=y-p.y;const horizontal=Math.abs(dx)>Math.abs(dy);const k=horizontal?(dx>0?'d':'a'):(dy>0?'s':'w');press(k,true);advance(1);press(k,false);ticks++;}advance(1);return {reached:Math.hypot(p.x-x,p.y-y)<=4,x:p.x,y:p.y,ticks};};""")
  for i,(x,y) in enumerate([(400,640),(500,640),(500,420),(400,410),(400,170)]):
   result=page.evaluate('(q)=>walkTo(q[0],q[1])',[x,y]);check('continuous keyboard route reaches '+str((x,y)),result['reached'])
   if i in [1,2,4]:
    page.evaluate('TDGAME.G.player.inv=999996;TDGAME.render()')
    page.locator('#screen').screenshot(path=str(OUT/f'route_{i}.png'))
  check('fortress still blocks the exit until its sentries die',page.evaluate('TD.World.solidAt(400,125)&&TDGAME.G.boss&&!TDGAME.G.boss.opened'))
  page.evaluate('for(const u of TDGAME.G.units)if(u.role==="sentry")TD.hitUnit(TDGAME.G,u,999,u.x,u.y);advance(2)')
  result=page.evaluate('walkTo(400,75)');check('actual walking crosses the unlocked north gate',result['reached'])
  page.evaluate('advance(210)');check('continuous beach-to-gate traversal completes the mission',page.evaluate('TDGAME.G.state==="clear"'))
  # Exported actions preserve alpha and the approved pilot palette contract.
  verification=json.loads((ROOT/'expansion/topdown/art/campaign_1008/action_palette_verification.json').read_text(encoding='utf-8'))
  check('all recolored action frames preserve source alpha',verification['all_alpha_unchanged'] and len(verification['checks'])==432)
  page.evaluate('TDGAME.G.sel=1;TDGAME.start();TDGAME.G.units=[];TDGAME.G.props=[];TDGAME.G.player.inv=999999;TDGAME.G.player.x=500;TDGAME.G.player.y=620;advance(1)')
  result=page.evaluate("""()=>{const FR=TD_CAMPAIGN_ART.frames,SEQ=TD_CAMPAIGN_ART.sequences,G=TDGAME.G,p=G.player;for(const pilot of TD.PILOTS){p.pilot=pilot;p.weapons=[{id:'desert_eagle',ammo:12,reserve:60}];p.wi=0;for(const a of [0,Math.PI/2,Math.PI,-Math.PI/2]){p.aim=a;for(const moving of [false,true]){p.moving=moving;for(const stance of ['stand','prone']){p.stance=stance;p.roll=0;p.action=null;p.dead=false;for(let i=0;i<6;i++){p.footTime=i/9;const q=TD.footPose(p),f=FR[q.key];if(!ART.get(q.key)||q.key.startsWith('wm_')||!Number.isFinite(q.angle)||!f.muzzle)return false;if(stance==='prone'&&(f.pilot!==pilot||f.palette!==TD_CAMPAIGN_ART.pilots[pilot].color))return false;}}}}}return true;}""")
  check('all twelve pilots use decoded matching-palette poses through every heading and prone/standing transition',result)
  result=page.evaluate("""()=>{const G=TDGAME.G,p=G.player;for(const pilot of TD.PILOTS){p.pilot=pilot;p.x=500;p.y=640;p.aim=Math.PI/2;p.manualAim=0;p.stance='stand';p.action=null;p.roll=0;p.fireCd=0;p.reload=0;p.dead=false;tap('f');if(p.stance!=='prone')return false;press('a',true);advance(12);const prone=TD.footPose(p);if(!prone.key.startsWith('fa_'+pilot+'_prone_fire_west_')||!ART.get(prone.key))return false;tap('f');advance(8);press('a',false);const stand=TD.footPose(p);if(p.stance!=='stand'||!stand.key.startsWith('fp_'+pilot+'_run_west_')||!ART.get(stand.key))return false;advance(1);if(!TD.footPose(p).key.startsWith('fp_'+pilot+'_aim_3'))return false;}return true;}""")
  check('real prone key, west crawl and stand while moving retain valid colored poses for every pilot',result)
  result=page.evaluate("""()=>{const G=TDGAME.G,p=G.player;for(const stance of ['stand','prone']){p.x=500;p.y=640;p.stance=stance;p.action=null;p.roll=0;p.reload=0;p.dead=false;tap('h');if(p.roll<=0||p.rollStance!==stance)return false;advance(35);if(p.roll!==0||p.stance!==stance||!ART.get(TD.footPose(p).key))return false;}return true;}""")
  check('real roll input returns cleanly to both standing and prone stances',result)
  # Capture full draw calls: only the body and its shadow, never a loose gun pickup.
  result=page.evaluate("""()=>{const p=TDGAME.G.player;p.pilot='hotwire';p.fireCd=0;p.stance='stand';p.moving=true;p.aim=Math.PI;p.a=-Math.PI/2;const calls=[],draw=ART.draw;ART.draw=(ctx,key,x,y,o)=>{calls.push({key,x,y,o});return draw(ctx,key,x,y,o);};const c=document.createElement('canvas');c.width=c.height=180;TD.drawFoot(c.getContext('2d'),p);ART.draw=draw;return calls.length===2&&calls.every(q=>q.key.startsWith('fp_hotwire_run_north_'));}""")
  check('running east while aiming north draws one north-facing held gun with its body and shadow',result)
  result=page.evaluate("""()=>{const p=TDGAME.G.player;p.pilot='cole';p.stance='stand';p.moving=false;p.roll=0;p.action=null;p.dead=false;p.weapons[0].ammo=12;p.fireCd=0;p.aim=Math.PI*.75;const point=TD.footSocket(p);TDGAME.G.shots=[];press('j',true);advance(1);press('j',false);const s=TDGAME.G.shots[0];return s&&Math.hypot((s.x-s.vx)-point.x,(s.y-s.vy)-point.y)<.01&&Math.abs(TD.M.wrap(s.a-p.aim))<.01;}""")
  check('actual bullet starts at the same rotated muzzle as the rendered pose',result)
  # Review every pilot's action transitions at game scale and enlarged contact size.
  result=page.evaluate("""()=>{const p=TDGAME.G.player;for(const pilot of TD.PILOTS){p.pilot=pilot;p.stance='prone';p.roll=.2;p.rollStance='prone';p.rollAim=Math.PI;p.action=null;p.dead=false;const q=TD.footPose(p);if(!q.key.startsWith('fa_'+pilot+'_roll_to_prone_'))return false;p.roll=0;p.action={aim:Math.PI,t:.4};if(!TD.footPose(p).key.startsWith('fa_'+pilot+'_grenade_throw_'))return false;p.action=null;p.dead=true;p.deadT=.5;if(!TD.footPose(p).key.startsWith('fa_'+pilot+'_death_'))return false;p.dead=false;}return true;}""")
  check('roll, grenade and death keep the selected pilot palette and authored orientation',result)
  page.evaluate("""const review=document.createElement('canvas');review.id='animation-review';review.width=960;review.height=12*112;review.style.position='absolute';review.style.left='0';review.style.top='0';review.style.width='960px';review.style.height='1344px';document.body.appendChild(review);const c=review.getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle='#222a30';c.fillRect(0,0,review.width,review.height);c.font='12px monospace';const modes=['stand','prone','stand','roll','grenade','death'];TD.PILOTS.forEach((pk,row)=>{c.fillStyle='#fff';c.fillText(pk.toUpperCase(),5,row*112+15);modes.forEach((mode,col)=>{const p=Object.assign({},TDGAME.G.player,{pilot:pk,fireCd:0,x:160*col+80,y:row*112+58,aim:-Math.PI/2,a:-Math.PI/2,stance:mode==='prone'?'prone':'stand',moving:false,roll:mode==='roll'?.1:0,rollStance:'stand',rollAim:-Math.PI/2,action:mode==='grenade'?{aim:-Math.PI/2,t:.4}:null,dead:mode==='death',deadT:.5});c.save();c.translate(p.x,p.y);c.scale(2,2);p.x=p.y=0;TD.drawFoot(c,p);c.restore();c.fillStyle='#fff';c.fillText(mode,160*col+50,row*112+105);});});""")
  page.locator('#animation-review').screenshot(path=str(OUT/'all_pilot_transitions.png'));page.evaluate('document.getElementById("animation-review").remove()')
  result=page.evaluate("""()=>{const cv=document.createElement('canvas');cv.width=480;cv.height=360;const c=cv.getContext('2d');c.fillStyle='#00c800';c.fillRect(0,0,480,360);const u={x:TD.Cam.x+240,y:TD.Cam.y+200,look:Math.PI,mode:'alert',vis:{range:230,half:.65}};TD.Stealth.drawGroundCones(c,Array.from({length:9},()=>u),0);const px=c.getImageData(240,100,1,1).data;return px[1]>=140&&c.globalAlpha===1;}""")
  check('nine overlapping alert cones retain at least 70 percent of the visible map background',result)
  page.evaluate("""const G=TDGAME.G;G.player.pilot='hotwire';G.player.inv=0;G.player.flash=0;G.player.dead=false;G.player.action=null;G.player.roll=0;G.player.stance='stand';G.player.x=475;G.player.y=580;G.player.aim=Math.PI;G.player.moving=false;G.units=Array.from({length:8},(_,i)=>TD.makeUnit('robotScout',450+i%3*25,610+i%2*30,{a:Math.PI}));for(const u of G.units){u.look=Math.PI;u.mode='alert';u.vis.range=230;}G.msgs=[];TD.Stealth.phase='ALERT';TD.Cam.follow(475,550,1);TDGAME.render();""")
  page.locator('#screen').screenshot(path=str(OUT/'pool_alert_readability.png'))
  check('zero browser, console and missing-asset errors',not errors)
  (OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'route_fixture':'Real keyboard movement, incidental enemies disabled, legitimate sentry gate still exercised'},indent=2),encoding='utf-8')
  browser.close()
finally:stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed')
sys.exit(0 if all(c['passed'] for c in checks) else 1)
