"""Native Chromium: floating art, live attachments, whole-island input and routes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_stagex_1004g';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def init(p):
 p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
 p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.stageX1004=null;campaign.rivalScattered=false;CF4.focus=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;MAP4E.focus=false;Input.mouse.moved=false;map4eWarm();}')
 p.wait_for_function('()=>MAP4E.readiness&&XART.rdy("map4f_flagx_lock")&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000)
 p.wait_for_timeout(1700)
def pointer(p):
 return p.evaluate('()=>{const h=map4eHubPose(),q=cmap2ToScreen(h.x,h.y-80),r=cv.getBoundingClientRect();return {x:r.left+(q.x+campaignViewOffset())/campaignViewWidth()*r.width,y:r.top+q.y/VH*r.height};}')
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?build=stagex-1004g',timeout=120000);init(p)
  p.evaluate('()=>{window.__hubDraw=[];const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){for(const key of ["map4e_region_hub","map4e_region_hub_shadow","map4f_flagx_lock"]){if(XART.rdy(key)&&im===XART.get(key))__hubDraw.push({key,args:a,alpha:ctx.globalAlpha});}return save(im,...a);};}')
  p.wait_for_timeout(200);p.screenshot(path=str(O/'overview.png'))
  ck(p.evaluate('()=>__hubDraw.some(v=>v.key==="map4e_region_hub"&&v.alpha===1&&v.args.every(Number.isFinite))'),'generated floating city draws in the actual game context')
  ck(p.evaluate('()=>__hubDraw.some(v=>v.key==="map4e_region_hub_shadow"&&v.args[3]<v.args[2]*.3)'),'authored shadow stays below the elevated island')
  ck(p.evaluate('()=>XART._src.map4e_region_hub.includes("campaign_stagex_1004g")&&cmap2World("hub").y-map4eHubPose().y>100'),'new rocky island has permanent elevation above the continent')
  h=p.evaluate('()=>map4eHubPose().y');p.wait_for_timeout(900)
  ck(p.evaluate('(h)=>Math.abs(map4eHubPose().y-h)>1',h),'floating city visibly bobs in the uninterrupted game loop')
  q=pointer(p);p.mouse.move(q['x'],q['y']);p.wait_for_timeout(650)
  ck(p.evaluate('()=>MAP4E.hover==="hub"&&cmap2.lift.hub>.9'),'hovering the city lifts Stage X itself')
  p.mouse.click(q['x'],q['y'],delay=100);p.wait_for_timeout(2000);p.screenshot(path=str(O/'floating-stage-x.png'))
  ck(p.evaluate('()=>MAP4E.xPreview&&state===GS.STAGESEL&&!cf4Pending()'),'clicking the island opens the locked Stage X briefing')
  ck(p.evaluate('()=>MAPG.typing?.key==="map4f-x-locked"&&MAPG.typing.count>25'),'locked Stage X briefing types without the selected stage resetting its letters')
  ck(p.evaluate('()=>{const h=map4eHubPose(),q=cmap2ToScreen(h.x,h.y),half=h.s*cmap2.cam.z/2;return q.y-half>CM2_BAND_TOP&&q.y+half<CM2_BAND_BOT;}'),'focused Stage X fits entirely below the menu and above progression')
  p.keyboard.press('Enter');p.wait_for_timeout(100)
  ck(p.evaluate('()=>state===GS.STAGESEL&&!campaign.stageX1004'),'inspecting locked Stage X grants no encounter')
  ck(p.evaluate('()=>{const h=map4eHubPose(),f=map4eStageXPoint(),o=fr27CoreMapPosition(),q=cmap2ToScreen(h.x,h.y-80);return f.y===h.y+55&&Math.abs(o.y-q.y)<.001&&Math.abs(o.x-q.x)<.001;}'),'flag and fighter orbit use the same elevated city pose')
  for route in ['left','right']:
   p.evaluate('(route)=>{campaign.stageX1004={route,done:false};MAP4E.xPreview=false;CF4.focus=false;CF4.flight=4;Input.mouse.moved=false;}',route)
   p.wait_for_function('()=>XART.rdy("gp4_ace_top")&&REBEL_SHIPS.every(k=>XART.rdy("rr_ship_"+k))',timeout=120000)
   p.evaluate('()=>{window.__ships=new Set();const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){for(const key of ["gp4_ace_top",...REBEL_SHIPS.map(k=>"rr_ship_"+k)])if(XART.rdy(key)&&im===XART.get(key)&&a.every(Number.isFinite)&&ctx.globalAlpha===1)__ships.add(key);return save(im,...a);};}')
   q=pointer(p);p.mouse.click(q['x'],q['y'],delay=100);p.wait_for_timeout(2000)
   ck(p.evaluate('()=>CF4.focus&&state===GS.STAGESEL'),'whole-island click selects earned '+route+' route')
   ck(p.evaluate('(r)=>r==="left"?__ships.has("gp4_ace_top"):REBEL_SHIPS.every(k=>__ships.has("rr_ship_"+k))',route),'complete authored encounter hulls orbit floating Stage X on '+route)
   p.screenshot(path=str(O/('stage-x-'+route+'.png')))
   p.keyboard.press('Enter');p.wait_for_timeout(200)
   ck(p.evaluate('(r)=>state===GS.PLAY&&run._gp4StageX===r',route),'real confirm launches '+route+' Stage X encounter')
   p.evaluate('()=>{storySkip();BOFCinematicDirector.cancel();Audio.stopMusic();openStageSelect(7,{});sselBoot=0;sselUnlockCine=null;}')
  p.set_viewport_size({'width':1000,'height':900});p.reload(timeout=120000);init(p)
  p.evaluate('()=>{MAP4E.xPreview=true;}');p.wait_for_timeout(2500);p.screenshot(path=str(O/'compact-stage-x.png'))
  ck(p.evaluate('()=>{const h=map4eHubPose(),q=cmap2ToScreen(h.x,h.y);return q.x>0&&q.x<campaignViewWidth()&&q.y>CM2_BAND_TOP&&q.y<CM2_BAND_BOT&&map4eStageXAt(q.x,q.y);}'),'floating Stage X remains visible and clickable in compact viewport')
  # Check the supplied review, not just its game fixture.
  p.goto(f'http://127.0.0.1:{port}/_shots/campaign_stagex_1004g/review.html',timeout=120000)
  p.wait_for_function('()=>document.getElementById("game").contentWindow.eval("MAP4E.xPreview&&MAP4E.readiness")',timeout=120000);p.wait_for_timeout(2000)
  ck(p.evaluate('()=>document.getElementById("game").contentWindow.eval("state===GS.STAGESEL&&!cf4Pending()")'),'new review opens directly on floating Stage X without altering saves')
  ck(not errors,'zero page and console errors');b.close()
finally:stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
