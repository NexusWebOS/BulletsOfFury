"""Native canvas and actual keyboard proof for Cole and protected Rebel introductions."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/cole_rebel_1004l';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[];port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
def cole(p,lv=8):
 p.evaluate(SETUP,{'stage':6,'pilot':'cole','diff':'furious'})
 p.evaluate('lv=>{H3.release=false;fb2Talk=null;run._primary1003b="mg";run.weapon=0;run.wlevel=lv;run.wlevels=WEAPONS.map(()=>0);run.wlevels[0]=8;run._cfTier=lv;run._cfUnlocked=8;Input.clearTaps();player.invuln=0;cf1004Warm();XART.rdy("nhud_bar");}',lv)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  cole(p);p.wait_for_function('()=>XART.rdy("cf1004_weapons")&&XART.rdy("cf1004_cloak")',timeout=120000,polling=50)
  p.evaluate('''()=>{window.nativeArt={};const get=XART.get,draw=ctx.drawImage,palette=xartPalette,map=new Map();xartPalette=function(k){const im=palette.apply(this,arguments);if(im)map.set(im,k);return im;};XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)nativeArt[k]=(nativeArt[k]||0)+1;return draw.apply(this,arguments);};}''')
  ck(p.evaluate('()=>{const hud=document.querySelector("#hud-row"),cv=document.querySelector("#screen");return !hud||hud.getBoundingClientRect().bottom<=cv.getBoundingClientRect().top+2;}'),'primary HUD returns to the top')
  fire=p.evaluate('()=>keybindFor(1).fire[0]');scan=p.evaluate('()=>keybindFor(1).multilock[0]')
  for lv in [6,7]:
   cole(p,lv);p.keyboard.down(fire);frames(p,12);p.keyboard.up(fire);shot(p,'cole-tier-'+str(lv))
   ck(p.evaluate('lv=>pBullets.some(q=>q._cfLaser===lv)&&pBullets.some(q=>q.kind==="coletri")',lv),'tier '+str(lv)+' actual fire uses laser lanes and homing rounds')
  cole(p,8);p.keyboard.down(fire);frames(p,15);p.keyboard.down(scan);frames(p,1)
  ck(p.evaluate('()=>run.wlevel===6&&player._fuse===0&&!retinaScanHeld()&&!Input.hold(1,"fire")'),'real Fire + Y switches once and cancels charge and scan')
  frames(p,15);ck(p.evaluate('()=>run.wlevel===6'),'held chord does not cycle repeatedly');p.keyboard.up(fire);p.keyboard.up(scan);frames(p,1)
  for lv in [7,8]:
   p.keyboard.down(scan);p.keyboard.down(fire);frames(p,1);p.keyboard.up(scan);p.keyboard.up(fire);frames(p,1);ck(p.evaluate('lv=>run.wlevel===lv',lv),'second chord selects tier '+str(lv))
  p.keyboard.down(fire);frames(p,145);
  for _ in range(14):
   if p.evaluate('()=>Math.floor(CF1004.clock*6)%2&&Math.floor(CF1004.clock*(3+(cf1004Percent()-2)*2))%2'):break
   frames(p,1)
  shot(p,'fusion-overcharge-210')
  ck(p.evaluate('()=>cf1004Percent()>2&&cf1004Percent()<3&&player._cfRumble>0&&shake>0'),'held Fusion enters rising rumble and pink danger band')
  p.evaluate('()=>player._fuse=FUSE_FULL*3.04;');shot(p,'fusion-release-304');ck(p.evaluate('()=>cf1004Percent()>3&&!player.dead'),'304 percent shows last-chance release band')
  p.keyboard.up(fire);frames(p,1);shot(p,'fusion-triple-helix')
  ck(p.evaluate('()=>pBullets.filter(q=>q._cfFusion&&!q._cfChild).length===2&&pBullets.some(q=>q.scale>3)&&player._fuse===0'),'real release fires over-three-times helix beams without gunfire underneath')
  cole(p);p.evaluate('()=>{player._fuse=FUSE_FULL*3.14;run.shield=5;player.invuln=999;}');p.keyboard.down(fire);frames(p,1);p.keyboard.up(fire);shot(p,'fusion-overload-death')
  ck(p.evaluate('()=>player.dead&&run.shield===0&&!pBullets.some(q=>q._cfFusion)'),'315 percent overload enters original ship death despite shield and invulnerability')
  cole(p);p.evaluate('''()=>{enemies=[{type:'fighter',x:player.x,y:player.y-170,w:32,h:32,hp:1000,max:1000,t:0,vy:0,vx:0},{type:'fighter',x:player.x+48,y:player.y-170,w:32,h:32,hp:1000,max:1000,t:0,vy:0,vx:0}];coleFuseRelease(FUSE_FULL*3);window.targets=enemies.slice();}''')
  frames(p,15);shot(p,'fusion-impact-shrapnel');ck(p.evaluate('()=>targets.every(q=>q.hp<1000)&&CF1004.hits>0&&pBullets.some(q=>q._cfChild)'),'native projectile update damages targets, splash neighbors and releases shards')
  # Actual modular boss targets, not invented target objects.
  cole(p);p.evaluate('''()=>{run.stage=3;spawnBoss('cryospear');B=boss;B._be=null;B.enter=false;B._noHit=false;B.x=player.x;B.y=200;B._drawY=200;er26Set(B,'recover');B._er26.dur=99;window.part=mr27Part(B,'gunL');window.partHP=part.hp;const q=mr27Shape(B,'gunL');player.x=q.x;player.y=q.y+160;coleFuseRelease(FUSE_FULL*3);}''')
  frames(p,12);ck(p.evaluate('()=>part.hp<partHP'),'swept Fusion beam damages actual deployed boss module')
  # Full protected intro: advance normal clock, inspect authored rendering on each line.
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('''()=>{H3.release=false;fb2Talk=null;window.R=B._rebels;rf28Init(B,R);B.enter=false;B._be=null;delete R.h3Intro;R.frIntro={done:false};window.G=rg4Init(B);s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;for(const q of s6Wing.ships){q.phase='fight';q.specialCd=q.missileCd=q.fcd=999;}rg4Warm();h3Warm();wm26Warm();XART.rdy('repair30_chaingun_round');XART.rdy('port_cf_decker_talk-o');window.friendHP=s6Wing.ships.map(q=>q.hp);window.rebelHP=R.ships.map(q=>q.hp);window.seen=new Set();}''')
  p.wait_for_function('()=>XART.rdy("ra4_fx")&&XART.rdy("ra4_nhxsb_g_2")&&XART.rdy("ra4_fchgc_2")&&XART.rdy("repair30_chaingun_round")',timeout=120000,polling=50)
  captured=set()
  for i in range(200):
   frames(p,20)
   line=p.evaluate('()=>({demo:R.h3Intro.rows[R.h3Intro.i]?.demo,t:R.h3Intro.t,done:R.frIntro.done,release:R.h3Intro.showcase?.current?.released})')
   if line.get('demo') and line['demo'] not in captured and line['t']>1.3:
    shot(p,'rebel-intro-'+line['demo']);captured.add(line['demo'])
   if line['done']:break
  ck(p.evaluate('()=>R.frIntro.done'),'entire unskippable introduction completes normally')
  ck(p.evaluate('()=>["cloakDemo","helixDemo","slugDemo","turboDemo"].every(k=>RS1004.events.some(q=>q.event===k))'),'all stolen-tech demonstrations run on their dialogue cues')
  ck(p.evaluate('()=>s6Wing.ships.every((q,i)=>q.hp===friendHP[i])&&R.ships.every((q,i)=>q.hp===rebelHP[i])'),'all ten ships retain HP throughout harmless demonstrations')
  ck(p.evaluate('()=>s6Wing.ships.length===4&&s6Wing.ships.every(q=>q.y>=VH*.60)'),'four allies hold the lower arena beside the player')
  shot(p,'rebel-fight-lower-wing')
  report['nativeArt']=p.evaluate('()=>nativeArt');
  p.evaluate('()=>{hudctx.clearRect(0,0,VW,HUDH);drawHUDStrip(hudctx);}');
  ck(p.evaluate('()=>{const d=hudctx.getImageData(0,0,VW,HUDH).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n>VW*HUDH*.5;}'),'authored HUD pixels render in the top canvas');
  p.screenshot(path=str(O/'full-hud-top.png'));report['screens'].append('full-hud-top');
  ck(p.evaluate('()=>nativeArt.cf1004_weapons>0&&nativeArt.cf1004_cloak>0&&nativeArt.ra4_nhxsb_g_2>0&&nativeArt.repair30_chaingun_round>0'),'new lasers, crystal cloak, full ball and actual slug art render through game drawImage')
  # Each review button must start a genuine playable state with independent storage.
  p.goto(f'http://127.0.0.1:{port}/_shots/cole_rebel_1004l/review.html',timeout=120000)
  for label,tier in [('Cole VI',6),('Cole VII',7),('Cole Fusion',8),('Rebel introduction',0),('Rebel dogfight',-1)]:
   p.get_by_role('button',name=label,exact=True).click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Practice ready."',timeout=120000)
   f=p.locator('#arena').element_handle().content_frame();f.evaluate(sh.TRAP_RAF);frames(f,1)
   ck(f.evaluate('tier=>tier>0?run.wlevel===tier&&run.weapon===0:tier===0?!!boss._rebels&&!boss._rebels.frIntro?.done:!!boss._rebels.frIntro?.done',tier),label+' review opens the requested playable state')
  ck(not errors,'zero page and console errors');b.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
