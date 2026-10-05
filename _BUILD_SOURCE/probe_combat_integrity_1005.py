"""Real Chromium regression proof for Fusion ownership and collision integrity."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_integrity_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[];port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate(SETUP,{'stage':6,'pilot':'cole','diff':'furious'})
  p.evaluate('()=>{H3.release=false;fb2Talk=null;run._primary1003b="mg";run.weapon=0;run.wlevel=8;run.wlevels[0]=8;run._cfTier=8;run._cfUnlocked=8;cf1004Warm();}')
  p.wait_for_function('()=>XART.rdy("cf1004_weapons")',timeout=120000,polling=50)
  p.evaluate('()=>{window.artCalls=[];const get=XART.get,draw=ctx.drawImage,map=new Map();XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)artCalls.push({k,args:Array.from(arguments).slice(1)});return draw.apply(this,arguments);};}')
  p.evaluate('()=>{const t={type:"fighter",x:player.x,y:player.y-160,w:32,h:32,hp:1000,max:1000,t:0,vx:0,vy:0};enemies=[t];coleFuseRelease(FUSE_FULL*3);window.target=t;}')
  frames(p,12);shot(p,'fusion-impact')
  ck(p.evaluate('()=>target.hp<1000&&CF1004.effects.length>0'),'actual Fusion collision creates independent impact animation')
  ck(p.evaluate('()=>!pBullets.some(b=>b.kind==="colefusionfx")'),'visual impact never enters weapon collision pool')
  ck(p.evaluate('()=>artCalls.some(c=>c.k==="cf1004_weapons")'),'authored Fusion art renders through game drawImage')
  p.evaluate('()=>{pBullets=[];enemies=[];}');frames(p,25)
  ck(p.evaluate('()=>CF1004.effects.length===0'),'impact completes and expires through simulation')
  p.evaluate('()=>{coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==="cole");run2.pilot="cole";run2.weapon=0;run2.wlevel=6;run2.wlevels=WEAPONS.map(()=>0);run2.wlevels[0]=6;run2._primary1003b="mg";run2._cfTier=null;run2._cfUnlocked=0;player2.reset();player2.invuln=1e9;player2.x=player.x+100;player2.y=player.y;Input.clearTaps();}')
  fire=p.evaluate('()=>keybindFor(1).fire[0]');scan=p.evaluate('()=>keybindFor(1).multilock[0]');fire2=p.evaluate('()=>keybindFor(2).fire[0]')
  p.keyboard.down(fire);p.keyboard.down(scan);p.keyboard.down(fire2);frames(p,8)
  ck(p.evaluate('()=>run.wlevel===6&&run._cfTier===6&&run2._cfUnlocked===6&&run2._cfTier===null'),'real P1 chord leaves P2 unlocks and selection independent')
  ck(p.evaluate('()=>!Input.hold(1,"fire")&&Input.hold(2,"fire")&&pBullets.some(b=>b.seat===2)'),'real P2 fire continues during P1 equip chord')
  p.keyboard.up(fire);p.keyboard.up(scan);p.keyboard.up(fire2);shot(p,'independent-coop')
  p.evaluate('()=>{withSeat(2,()=>{run.wlevel=8;run._cfUnlocked=8;run._cfTier=8;coleFuseRelease(FUSE_FULL);});const b=pBullets.find(b=>b._cfFusion&&b.seat===2);window.t={type:"fighter",x:b.x,y:b.y,w:32,h:32,hp:1000,max:1000};enemies=[t];b.vy=0;cf1004BulletTick(b,0);}')
  ck(p.evaluate('()=>pBullets.filter(b=>b._cfChild).length===10&&pBullets.filter(b=>b._cfChild).every(b=>b.seat===2)'),'P2 ricochets and shrapnel retain shooter ownership')
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{run._gp4StageX="right";H3.release=false;fb2Talk=null;window.R=B._rebels;rf28Init(B,R);B._noHit=false;R.frIntro={done:true};window.G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;s6WingInit();s6WingLaunch(4,true);Object.assign(s6Wing,{all:true,route:"right",beats:3,fakeDone:true,supplyIndex:3,choice:false,boxes:[]});for(const q of R.ships){q.mode="fight";q.warp=0;q.x=worldWidth()/2;q.y=130;q.rg4.cd=9999;q.rg4.act=null;}rg4Warm();h3Warm();}')
  frames(p,180);shot(p,'stagex-five-fighters')
  ck(p.evaluate('()=>R.ships.length===5&&Math.max(...R.ships.map(q=>q.x))-Math.min(...R.ships.map(q=>q.x))>200'),'actual Stage X rematch has five spread-out fighters')
  p.evaluate('()=>{window.nyx=R.ships.find(q=>q.key==="nyx");nyx.frCloak=5;nyx.x=worldWidth()/2;nyx.y=300;window.nyxHP=nyx.hp;run._primary1003b="mg";run.weapon=0;run.wlevel=8;pBullets=[];coleFuseRelease(FUSE_FULL);window.blind=pBullets[0];blind.x=blind.cx=nyx.x;blind.y=nyx.y;blind.vy=0;cf1004BulletTick(blind,0);}')
  ck(p.evaluate('()=>nyx.hp<nyxHP&&nyx.flash>0&&!spaceTargets().some(t=>t._retinaId==="nyx-hull")'),'Fusion physically hits cloaked Nyx while missile acquisition excludes her')
  shot(p,'fusion-hits-cloaked-nyx')
  p.evaluate('()=>{window.onceHP=nyx.hp;nyx.frCloak=0;cf1004BulletTick(blind,0);}')
  ck(p.evaluate('()=>nyx.hp===onceHP'),'cloak reveal cannot duplicate a piercing beam hit')
  p.evaluate('()=>{const q=R.ships[0];q.x=player.x-100;q.y=player.y-100;ra4Supply(q,G);window.box=G.rebelBoxes[0];pBullets=[];enemies=[];const beam={_cfChild:true,scale:3,seat:1,dmg:120,x:box.x,y:box.y};cf1004Impact(beam,box,box.x,box.y);window.boxHP=box.hp;ra4SupplyTick(G,0);}')
  ck(p.evaluate('()=>box.hp===boxHP&&!box.dead'),'authored impact overlapping real Rebel ability crate does not damage it')
  shot(p,'harmless-impact-at-crate')
  p.evaluate('()=>{run._cfTier=8;run._cfUnlocked=8;run2._cfTier=8;run2._cfUnlocked=8;pilotIndex=PILOTS.findIndex(p=>p.key==="cole");startRun(1);}')
  ck(p.evaluate('()=>run._cfTier===null&&run._cfUnlocked===0&&run2._cfTier===null&&run2._cfUnlocked===0'),'new game clears both players saved laser state')
  p.goto(f'http://127.0.0.1:{port}/_shots/combat_integrity_1005/review.html',timeout=120000)
  for label,tier in [('Cole VI',6),('Cole VII',7),('Cole Fusion',8),('Rebel introduction',0),('Rebel dogfight',-1),('Stage X dogfight',-2)]:
   p.get_by_role('button',name=label,exact=True).click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Practice ready."',timeout=120000)
   f=p.locator('#arena').element_handle().content_frame();f.evaluate(sh.TRAP_RAF);frames(f,1)
   ck(f.evaluate('tier=>tier>0?run.wlevel===tier&&run.weapon===0:tier===0?!!boss._rebels&&!boss._rebels.frIntro?.done:tier===-2?run._gp4StageX==="right"&&boss._rebels.ships.length===5:!!boss._rebels.frIntro?.done',tier),label+' practice opens the correct state')
  ck(not errors,'zero page and console errors');b.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
