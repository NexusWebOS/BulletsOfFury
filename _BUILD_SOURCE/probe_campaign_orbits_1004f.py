"""Check visible Stage X orbit art and the actual generated HQ frontage."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_markers_1004f';errors=[];rows=[];checks=[]
def ck(value,name):checks.append({'ok':bool(value),'name':name});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();run.mode="campaign";campaign.unlockedMax=8;campaign.stageX1004={route:"right",done:false};campaign.rivalScattered=false;openStageSelect(7,{});sselBoot=0;sselUnlockCine=null;CF4.flight=4;CF4.focus=true;}')
  p.wait_for_function('()=>REBEL_SHIPS.every(k=>XART.rdy("rr_ship_"+k))&&XART.rdy("map4e_region_hq")&&XART.rdy("gp4_ace_top")',timeout=120000);p.wait_for_timeout(3000)
  rows.append(p.evaluate('()=>({keys:REBEL_SHIPS.map(k=>({key:"rr_ship_"+k,src:XART._src["rr_ship_"+k],ready:XART.rdy("rr_ship_"+k)})),pending:cf4Pending(),focus:CF4.focus,flight:CF4.flight})'))
  p.evaluate('()=>{window.__orbitDraw=[];const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){for(const k of REBEL_SHIPS.map(k=>"rr_ship_"+k)){if(XART.rdy(k)&&im===XART.get(k))__orbitDraw.push({key:k,alpha:ctx.globalAlpha,args:a,transform:Array.from([ctx.getTransform().a,ctx.getTransform().d,ctx.getTransform().e,ctx.getTransform().f])});}return save(im,...a);};}')
  p.wait_for_timeout(200);rows.append(p.evaluate('()=>__orbitDraw'))
  ck(p.evaluate('()=>new Set(__orbitDraw.filter(v=>v.alpha===1&&v.args.every(Number.isFinite)).map(v=>v.key)).size===5'),'all five rebels draw at full opacity in their Stage X orbit')
  p.screenshot(path=str(O/'stage-x-native-orbits-screen.png'))
  ck(p.evaluate('()=>CF4.flight>4&&cf4Pending()&&CF4.focus'),'Stage X orbit remains animated in the normal game loop')
  p.evaluate('()=>{campaign.stageX1004.route="left";window.__harrierSeen=false;const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){if(XART.rdy("gp4_ace_top")&&im===XART.get("gp4_ace_top")&&a.every(Number.isFinite))__harrierSeen=true;return save(im,...a);};}')
  p.wait_for_timeout(1200);p.screenshot(path=str(O/'stage-x-native-harrier-screen.png'))
  ck(p.evaluate('()=>__harrierSeen'),'escaped Harrier draws its actual hull over Stage X')
  # HQ close-up stays on the actual engine camera and draw pipeline.
  p.evaluate('()=>{campaign.stageX1004=null;CF4.focus=false;MAP4E.xPreview=false;sselBoot=0;window.__hqSeen=false;const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){if(XART.rdy("map4e_region_hq")&&im===XART.get("map4e_region_hq")&&a.every(Number.isFinite)&&a[2]>0&&a[3]>0)__hqSeen=true;return save(im,...a);};cmap2CameraTick=function(){cmap2.cam={...cmap2World("hq"),z:.55};};}')
  p.wait_for_timeout(1100);p.screenshot(path=str(O/'hq-native-screen.png'))
  ck(p.evaluate('()=>__hqSeen'),'generated HQ building draws with finite geometry in the actual game context')
  ck(not errors,'zero page and console errors during the uninterrupted orbit and HQ captures')
  rows.append({'errors':errors});b.close()
finally:stop()
(O/'orbit-inspection.json').write_text(json.dumps({'checks':checks,'details':rows,'errors':errors},indent=2)+'\n',encoding='utf-8');print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
