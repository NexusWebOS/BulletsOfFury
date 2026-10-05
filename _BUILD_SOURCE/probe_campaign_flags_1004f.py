"""Native flag pixels, anchors, campaign states and real keyboard navigation."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_markers_1004f';checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.rank={1:"S",2:"A",3:"B"};campaign.stageX1004=null;campaign.rivalScattered=false;s9MapCine=null;riftReturn=null;openStageSelect(4,{boot:true});sselUnlockCine=null;Input.mouse.moved=false;}')
  p.wait_for_function('()=>MAP4F_FLAG_STATES.every(v=>Object.keys(MAP4F_FLAGS).every(n=>XART.rdy("map4f_flag"+n+"_"+v)))',timeout=120000)
  p.wait_for_function('()=>sselBoot===0',timeout=30000);p.wait_for_timeout(1500)
  p.evaluate('()=>{window.__flagsSeen=new Set();const native=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){for(let n=1;n<=9;n++)for(const v of MAP4F_FLAG_STATES){const key="map4f_flag"+n+"_"+v;if(XART.rdy(key)&&im===XART.get(key)&&a.every(Number.isFinite))__flagsSeen.add(key);}return native(im,...a);};}')
  p.wait_for_timeout(400);p.screenshot(path=str(O/'roman-overview-screen.png'))
  ck(p.evaluate('()=>__flagsSeen.has("map4f_flag1_done_gold")&&__flagsSeen.has("map4f_flag2_done_silver")&&__flagsSeen.has("map4f_flag3_done_green")'),'actual renderer uses authored rank flags for S, A and cleared stages')
  ck(p.evaluate('()=>__flagsSeen.has("map4f_flag4_hi0")&&__flagsSeen.has("map4f_flag4_hi1")'),'selected IV animates between both silhouette-highlight states')
  ck(p.evaluate('()=>[5,6,7,8].every(n=>__flagsSeen.has("map4f_flag"+n+"_av"))&&__flagsSeen.has("map4f_flag9_lock")'),'all remaining stages and locked IX draw new Roman flag pixels')
  for key,n,head in [('ArrowRight',5,3.141592653589793),('ArrowLeft',6,None),('ArrowLeft',7,None),('ArrowLeft',8,0),('ArrowRight',1,0)]:
   p.keyboard.press(key);p.wait_for_timeout(500)
   ck(p.evaluate('(n)=>sselCursor===n',n),'real keyboard navigation reaches '+str(n)+' with new flags')
   if head is not None:ck(p.evaluate('(h)=>sselShip.head===h',head),'real keyboard flight retains the approved heading into '+str(n))
  p.evaluate('()=>{campaign.unlockedMax=1;campaign.bonusUnlocked=false;campaign.rank={};openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;__flagsSeen.clear();}');p.wait_for_timeout(600)
  p.screenshot(path=str(O/'roman-locked-screen.png'))
  ck(p.evaluate('()=>[2,3,4,5,6,7,8,9].every(n=>__flagsSeen.has("map4f_flag"+n+"_lock"))'),'locked II–IX use grayscale flags while preserving campaign locks')
  p.keyboard.press('ArrowRight');p.wait_for_timeout(200);ck(p.evaluate('()=>sselCursor===1&&!campaign.bonusUnlocked'),'new IX marker grants no bonus unlock')
  p.evaluate('()=>{campaign.unlockedMax=8;campaign.rank={};openStageSelect(4,{});sselBoot=0;sselUnlockCine={stage:4,phase:"ding",t:.12,z:1};__flagsSeen.clear();}');p.wait_for_timeout(500)
  ck(p.evaluate('()=>__flagsSeen.has("map4f_flag4_white")'),'original unlock cinematic uses the new white silhouette flag')
  p.evaluate('()=>{sselUnlockCine=null;MAP4E.xPreview=true;sselCursor=7;MAP4E.focus=true;}');p.wait_for_timeout(500);p.keyboard.press('ArrowRight');p.wait_for_timeout(250)
  ck(p.evaluate('()=>!MAP4E.xPreview&&sselCursor!==7'),'directional exit from the locked X preview preserves its navigation tap')
  ck(not errors,'zero page and console errors for flag load, animation and controls');b.close()
finally:stop()
(O/'flag-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
