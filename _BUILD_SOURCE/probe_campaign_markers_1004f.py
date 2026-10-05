"""Native Chromium campaign landscape, navigation, unlocks and authored draw keys."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_markers_1004f';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(v,n): checks.append({'ok':bool(v),'name':n}); print(('PASS ' if v else 'FAIL ')+n,flush=True)
def step(p,n=120):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){stateT+=1/60;ctx.setTransform(SS,0,0,SS,0,0);ctx.translate(campaignViewOffset(),0);drawStageSelect(1/60);}}',min(20,n-i));p.wait_for_timeout(10)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
 p.screenshot(path=str(O/(name+'-screen.png')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.rivalScattered=false;campaign.stageX1004=null;Rival24.reset?.();s9MapCine=null;riftReturn=null;openStageSelect(1,{boot:true});sselUnlockCine=null;Input.mouse.moved=false;window.sselCommitted=false;map4eWarm();}')
  p.wait_for_function('()=>XART.rdy("map4e_landscape")&&MAP4E.keys.every(k=>XART.rdy("map4e_region_"+k))&&XART.rdy("map4f_flagx")&&XART.rdy("map4f_flagx_lock")&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000)
  p.wait_for_function('()=>sselBoot===0',timeout=30000);p.wait_for_timeout(2000);shot(p,'live-overview')
  ck(p.evaluate('()=>state===GS.STAGESEL&&MAP4E.readiness&&document.body.classList.contains("wide-map")'),'uninterrupted native loop finishes boot and renders the widescreen map')
  cloud=p.evaluate('()=>cmap2.t');p.wait_for_timeout(700)
  ck(p.evaluate('(t)=>cmap2.t>t+.4',cloud),'cloud and floating-world animation continue in the real loop')
  p.keyboard.press('ArrowRight');p.wait_for_timeout(2400);shot(p,'live-focused-volcano')
  ck(p.evaluate('()=>sselCursor===2&&MAP4E.focus'),'live map and briefing follow a real keyboard selection')
  p.evaluate('()=>{openStageSelect(1,{});sselUnlockCine=null;Input.mouse.moved=false;}');p.wait_for_timeout(1200)
  p.evaluate(sh.TRAP_RAF)
  # Observe actual authored keys through this game context's drawImage.
  p.evaluate('()=>{window.__mapSeen=new Set();const native=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...args){for(const k of ["map4e_landscape",...MAP4E.keys.map(k=>"map4e_region_"+k),"map4f_flagx","map4f_flagx_lock","cm2_ocean"]){if(XART.rdy(k)&&im===XART.get(k)&&args.every(Number.isFinite))__mapSeen.add(k);}return native(im,...args);};}')
  step(p,510);p.wait_for_timeout(1600);step(p,100);shot(p,'overview')
  ck(p.evaluate('()=>sselBoot===0&&MAP4E.readiness'),'boot finishes with all generated land regions ready')
  ck(p.evaluate('()=>__mapSeen.has("map4e_landscape")&&MAP4E.keys.filter(k=>k!=="islets").every(k=>__mapSeen.has("map4e_region_"+k))'),'terrain, all stages, city, HQ and cosmic region use authored XART pixels')
  ck(p.evaluate('()=>__mapSeen.has("cm2_ocean")&&__mapSeen.has("map4f_flagx_lock")'),'original blue ocean and permanent locked Stage X flag are drawn')
  ck(p.evaluate('()=>Math.abs(cmap2.cam.z-map30Overview().z)<.002&&!MAP4E.focus'),'initial settled map shows the complete connected continent')
  ck(p.evaluate('()=>Object.keys(SSEL_POS).length===9&&cmap2World(9).x>cmap2World(3).x&&cmap2World(9).y<cmap2World(3).y'),'nine stages retained; bonus cosmic region is offshore northeast')
  p.keyboard.press('ArrowRight');step(p,150);p.wait_for_timeout(900);step(p,90);shot(p,'focused-volcano')
  ck(p.evaluate('()=>sselCursor===2&&MAP4E.focus&&cmap2.cam.z>map30Overview().z*2'),'real directional input selects a stage and zooms to its region')
  ck(p.evaluate('()=>cmap2.lift[2]>.98&&cmap2.lift[1]<.02'),'selected landmark lifts while adjacent terrain stays anchored')
  for key,n in [('ArrowRight',3),('ArrowRight',4),('ArrowRight',5),('ArrowLeft',6),('ArrowLeft',7),('ArrowLeft',8)]:
   p.keyboard.press(key);step(p,30);ck(p.evaluate('(n)=>sselCursor===n',n),'real D-pad path reaches Stage '+str(n))
  # The approved vertical headings are verified in the live renderer, with
  # their actual pilot pixels. Frame batches still yield for lazy assets.
  for a,z,head in [(4,5,3.141592653589793),(7,8,0),(8,1,0)]:
   p.evaluate('([a,z])=>{sselCursor=a;const q=sselFlagXY(a);sselShip={...q,cur:a,t:0,phase:"idle",head:Math.PI/2,trail:0};sselCursor=z;cmap2.cam={...cmap2Frame(a,z)};}',[a,z]);step(p,12);shot(p,'travel-'+str(a)+'-'+str(z))
   ck(p.evaluate('()=>{const p=cmap2ToScreen(sselShip.x,sselShip.y);return p.x>0&&p.x<campaignViewWidth()&&p.y>CM2_BAND_TOP&&p.y<CM2_BAND_BOT;}'),'travelling hull is inside the visible map band on '+str(a)+' to '+str(z))
   ck(p.evaluate('(h)=>sselShip.head===h',head),'rendered ship faces '+('down' if head else 'up')+' on '+str(a)+' to '+str(z))
   step(p,200);ck(p.evaluate('(h)=>sselShip.head===h&&!sselShip.moving',head),'ship settles without a heading snap on '+str(a)+' to '+str(z))
  # Every pilot uses a fully sized authored sprite in both vertical headings.
  v=p.evaluate('()=>{const saved=ctx.drawImage.bind(ctx),out=[];for(const pilot of PILOTS){for(const h of [0,Math.PI]){const k="ship_"+pilot.key;XART.rdy(k);}}return PILOTS.map(p=>p.key);}')
  p.wait_for_function('()=>PILOTS.every(p=>XART.rdy("ship_"+p.key))',timeout=120000)
  p.evaluate('()=>{window.__shipPixels=[];const saved=ctx.drawImage.bind(ctx);for(const pilot of PILOTS){run.pilot=pilot.key;pilotIndex=PILOTS.findIndex(p=>p.key===pilot.key);for(const h of [0,Math.PI]){sselShip.head=h;let painted=false;ctx.drawImage=function(im,...a){painted=im===map4eShipFrame("ship_"+pilot.key,h)&&a[2]>0&&a[3]>0;return saved(im,...a);};sselShipDraw();__shipPixels.push({key:pilot.key,heading:h,painted});}}ctx.drawImage=saved;}')
  ck(p.evaluate('()=>__shipPixels.length===18&&__shipPixels.every(s=>s.painted)'),'all nine pilots render their own intact authored up/down hulls')
  p.evaluate('()=>{sselCursor=8;}');step(p,15)
  # Pointer selection from the overview, using the engine's actual view conversion.
  p.evaluate('()=>{MAP4E.focus=false;MAP4E.last=sselCursor;cmap2.cam={...map30Overview()};Input.mouse.moved=false;}');step(p,90)
  pos=p.evaluate('()=>{const q=cmap2ToScreen(...SSEL_POS[4]),r=cv.getBoundingClientRect();return {x:r.left+(q.x+campaignViewOffset())/campaignViewWidth()*r.width,y:r.top+q.y/VH*r.height};}')
  p.mouse.move(pos['x'],pos['y']);step(p,30)
  ck(p.evaluate('()=>MAP4E.hover===4&&cmap2.lift[4]>.9&&sselCursor===8'),'pointer hover lifts the desert without changing the chosen mission')
  p.mouse.down();step(p,1);p.mouse.up();step(p,180);shot(p,'focused-desert')
  ck(p.evaluate('()=>sselCursor===4&&!sselZoom'),'pointer selects the visible desert region without deploying on the first click')
  p.evaluate('()=>{campaign.unlockedMax=1;campaign.bonusUnlocked=false;openStageSelect(1,{});Input.mouse.moved=false;}');step(p,120);shot(p,'locked-world')
  p.keyboard.press('ArrowRight');step(p,30)
  ck(p.evaluate('()=>sselCursor===1&&!campaign.bonusUnlocked'),'locked stage and bonus portal cannot be selected by navigation')
  p.evaluate('()=>{campaign.unlockedMax=8;campaign.bonusUnlocked=true;openStageSelect(9,{});s9MapCine=null;Input.mouse.moved=false;}');step(p,240);p.wait_for_timeout(1000);step(p,60);shot(p,'bonus-rift')
  ck(p.evaluate('()=>sselCursor===9&&cmap2Unlocked(9)&&cmap2IslandAt(...Object.values(cmap2ToScreen(...SSEL_POS[9])),9,9)===9'),'unlocked bonus portal focuses and remains selectable')
  p.evaluate('()=>{campaign.bonusUnlocked=false;campaign.stageX1004={route:"right",done:false};CF4.flight=4;CF4.focus=true;openStageSelect(7,{});CF4.focus=true;sselUnlockCine=null;Input.mouse.moved=false;}');step(p,240);shot(p,'stage-x')
  ck(p.evaluate('()=>Rival24.mapFocused&&Math.hypot(cmap2.cam.x-MAP4E.hub[0],cmap2.cam.y-(MAP4E.hub[1]-150))<3'),'Stage X camera frames the elevated central city')
  # Locked X is inspectable but never deploys or consumes a campaign route.
  p.evaluate('()=>{campaign.stageX1004=null;campaign.rivalScattered=false;CF4.focus=false;MAP4E.xPreview=false;MAP4E.focus=false;sselCursor=1;MAP4E.last=1;cmap2.cam={...map30Overview()};Input.mouse.moved=false;}');step(p,20)
  pos=p.evaluate('()=>{const p=map4eStageXPoint(),q=cmap2ToScreen(p.x,p.y),r=cv.getBoundingClientRect();return {x:r.left+(q.x+campaignViewOffset())/campaignViewWidth()*r.width,y:r.top+(q.y-12)/VH*r.height};}')
  p.mouse.move(pos['x'],pos['y']);p.mouse.down();step(p,1);p.mouse.up();step(p,200);shot(p,'stage-x-locked')
  ck(p.evaluate('()=>MAP4E.xPreview&&!cf4Pending()&&state===GS.STAGESEL'),'permanent Stage X flag opens an informational locked briefing')
  p.keyboard.press('Enter');step(p,2)
  ck(p.evaluate('()=>state===GS.STAGESEL&&!campaign.stageX1004&&!run._gp4StageX'),'confirming locked Stage X cannot manufacture a fight')
  p.keyboard.press('Escape');step(p,2)
  # Both earned routes keep their real launch controller and full wing roster.
  for route in ['left','right']:
   p.evaluate('(r)=>{run.mode="campaign";campaign.unlockedMax=8;campaign.stageX1004={route:r,done:false};CF4.flight=4;CF4.focus=true;sselCursor=7;sselBoot=0;}',route);step(p,220);shot(p,'stage-x-'+route)
   ck(p.evaluate('(r)=>cf4LaunchX()&&run._gp4StageX===r&&state===GS.PLAY',route),'central Stage X launches the earned '+('Harrier' if route=='left' else 'Rebel')+' fight')
   p.evaluate('()=>{storySkip();BOFCinematicDirector.cancel();Audio.stopMusic();openStageSelect(7,{});sselUnlockCine=null;sselBoot=0;}')
  # A fresh live boot lets the real resize loop reset its backing canvas width.
  # Stretching a trapped widescreen canvas into a compact CSS viewport is not a
  # valid pixel proof of the compact layout.
  p.set_viewport_size({'width':1000,'height':900});p.reload(timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.stageX1004=null;campaign.rivalScattered=false;CF4.focus=false;openStageSelect(1,{});sselUnlockCine=null;Input.mouse.moved=false;}')
  p.wait_for_function('()=>MAP4E.readiness&&XART.rdy("map4f_flagx")&&XART.rdy("map4f_flagx_lock")&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000);p.wait_for_timeout(2000);shot(p,'compact')
  ck(p.evaluate('()=>{const t=map30Overview();return Number.isFinite(t.z)&&t.z>0&&cmap2.cam.z<=.2;}'),'compact viewport retains finite full-world framing')
  ck(not errors,'zero page and console errors');b.close()
finally: stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
