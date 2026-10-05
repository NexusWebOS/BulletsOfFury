from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'_BUILD_SOURCE/probe_campaign_landscape_1004e.py';s=p.read_text()
s=s.replace('campaign_landscape_1004e','campaign_markers_1004f')
s=s.replace('&&bmfReady("game")','&&XART.rdy("map4f_flagx")&&XART.rdy("map4f_flagx_lock")&&bmfReady("game")')
s=s.replace('"map30_hq","cm2_ocean"','"map4f_flagx","map4f_flagx_lock","cm2_ocean"')
s=s.replace('__mapSeen.has("map30_hq")','__mapSeen.has("map4f_flagx_lock")').replace('original blue ocean and Fury HQ icon are drawn','original blue ocean and permanent locked Stage X flag are drawn')
s=s.replace('im===XART.get(k))','im===XART.get(k)&&args.every(Number.isFinite))')
s=s.replace("  # Pointer selection",'''  # The approved vertical headings are verified in the live renderer, with
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
  # Pointer selection''')
marker='  # A fresh live boot'
s=s.replace(marker,'''  # Locked X is inspectable but never deploys or consumes a campaign route.
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
  # A fresh live boot''')
(R/'_BUILD_SOURCE/probe_campaign_markers_1004f.py').write_text(s,encoding='utf-8')
print('Prepared native marker/travel probe.')
