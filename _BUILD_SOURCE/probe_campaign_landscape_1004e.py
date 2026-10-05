"""Native Chromium campaign landscape, navigation, unlocks and authored draw keys."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_landscape_1004e';O.mkdir(parents=True,exist_ok=True)
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
  p.wait_for_function('()=>XART.rdy("map4e_landscape")&&MAP4E.keys.every(k=>XART.rdy("map4e_region_"+k))&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000)
  p.wait_for_function('()=>sselBoot===0',timeout=30000);p.wait_for_timeout(2000);shot(p,'live-overview')
  ck(p.evaluate('()=>state===GS.STAGESEL&&MAP4E.readiness&&document.body.classList.contains("wide-map")'),'uninterrupted native loop finishes boot and renders the widescreen map')
  cloud=p.evaluate('()=>cmap2.t');p.wait_for_timeout(700)
  ck(p.evaluate('(t)=>cmap2.t>t+.4',cloud),'cloud and floating-world animation continue in the real loop')
  p.keyboard.press('ArrowRight');p.wait_for_timeout(2400);shot(p,'live-focused-volcano')
  ck(p.evaluate('()=>sselCursor===2&&MAP4E.focus'),'live map and briefing follow a real keyboard selection')
  p.evaluate('()=>{openStageSelect(1,{});sselUnlockCine=null;Input.mouse.moved=false;}');p.wait_for_timeout(1200)
  p.evaluate(sh.TRAP_RAF)
  # Observe actual authored keys through this game context's drawImage.
  p.evaluate('()=>{window.__mapSeen=new Set();const native=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...args){for(const k of ["map4e_landscape",...MAP4E.keys.map(k=>"map4e_region_"+k),"map30_hq","cm2_ocean"]){if(XART.rdy(k)&&im===XART.get(k))__mapSeen.add(k);}return native(im,...args);};}')
  step(p,510);p.wait_for_timeout(1600);step(p,100);shot(p,'overview')
  ck(p.evaluate('()=>sselBoot===0&&MAP4E.readiness'),'boot finishes with all generated land regions ready')
  ck(p.evaluate('()=>__mapSeen.has("map4e_landscape")&&MAP4E.keys.filter(k=>k!=="islets").every(k=>__mapSeen.has("map4e_region_"+k))'),'terrain, all stages, city, HQ and cosmic region use authored XART pixels')
  ck(p.evaluate('()=>__mapSeen.has("cm2_ocean")&&__mapSeen.has("map30_hq")'),'original blue ocean and Fury HQ icon are drawn')
  ck(p.evaluate('()=>Math.abs(cmap2.cam.z-map30Overview().z)<.002&&!MAP4E.focus'),'initial settled map shows the complete connected continent')
  ck(p.evaluate('()=>Object.keys(SSEL_POS).length===9&&cmap2World(9).x>cmap2World(3).x&&cmap2World(9).y<cmap2World(3).y'),'nine stages retained; bonus cosmic region is offshore northeast')
  p.keyboard.press('ArrowRight');step(p,150);p.wait_for_timeout(900);step(p,90);shot(p,'focused-volcano')
  ck(p.evaluate('()=>sselCursor===2&&MAP4E.focus&&cmap2.cam.z>map30Overview().z*2'),'real directional input selects a stage and zooms to its region')
  ck(p.evaluate('()=>cmap2.lift[2]>.98&&cmap2.lift[1]<.02'),'selected landmark lifts while adjacent terrain stays anchored')
  for key,n in [('ArrowRight',3),('ArrowRight',4),('ArrowRight',5),('ArrowLeft',6),('ArrowLeft',7),('ArrowLeft',8)]:
   p.keyboard.press(key);step(p,30);ck(p.evaluate('(n)=>sselCursor===n',n),'real D-pad path reaches Stage '+str(n))
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
  ck(p.evaluate('()=>Rival24.mapFocused&&Math.hypot(cmap2.cam.x-MAP4E.hub[0],cmap2.cam.y-MAP4E.hub[1])<3'),'Stage X stays anchored to the new central city')
  # A fresh live boot lets the real resize loop reset its backing canvas width.
  # Stretching a trapped widescreen canvas into a compact CSS viewport is not a
  # valid pixel proof of the compact layout.
  p.set_viewport_size({'width':1000,'height':900});p.reload(timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.stageX1004=null;campaign.rivalScattered=false;CF4.focus=false;openStageSelect(1,{});sselUnlockCine=null;Input.mouse.moved=false;}')
  p.wait_for_function('()=>MAP4E.readiness&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000);p.wait_for_timeout(2000);shot(p,'compact')
  ck(p.evaluate('()=>{const t=map30Overview();return Number.isFinite(t.z)&&t.z>0&&cmap2.cam.z<=.2;}'),'compact viewport retains finite full-world framing')
  ck(not errors,'zero page and console errors');b.close()
finally: stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
