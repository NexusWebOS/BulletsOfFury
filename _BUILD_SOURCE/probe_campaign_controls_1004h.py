"""Real keyboard/pointer input and persistent save/load through browser reload."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_controls_1004h';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def key(p,k,ms=240):p.keyboard.press('Space' if k==' ' else k);p.wait_for_timeout(ms)
def fire(p,ms=500):key(p,p.evaluate('()=>keybind.fire.find(k=>!/^mouse|^pad_|^enter$/.test(k))||" "'),ms)
def init(p,stage=1,pending=None):
 p.wait_for_function('()=>window.__bofFrames>4&&typeof map4hWarm==="function"',timeout=120000)
 p.evaluate('([stage,route])=>{ht27Stop();debugFight=null;coopOn=false;run.mode="campaign";run.pilot="yuri";pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");diffKey="furious";DIFF=difficultyForRun("campaign",diffKey);run.score=54321;run.stage=stage;campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.stageX1004=route?{route,done:false}:null;campaign.rivalScattered=false;CF4.focus=false;CF4.flight=4;campPause=null;_selFlash=null;s9MapCine=null;riftReturn=null;openStageSelect(stage,{});sselBoot=0;sselUnlockCine=null;Input.clearTaps();Input.mouse.moved=false;map4hWarm();}',[stage,pending])
 p.wait_for_function('()=>MAP4E.readiness&&XART.rdy("map4h_slot_red")&&XART.rdy("ship_yuri")&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000);p.wait_for_timeout(900)
def menu(p,button):
 key(p,'Enter');ck(p.evaluate('()=>cmap2.focus==="bar"&&!campPause&&state===GS.STAGESEL'),'Start opens bar instead of deploying stage')
 p.evaluate('(i)=>{cmap2.bar=i;Input.mouse.moved=false;}',button);fire(p,850)
 ck(p.evaluate('(mode)=>campPause?.bar&&campPause.mode===mode', 'save' if button==0 else 'load' if button==1 else 'exit'),'bar confirmation opens '+['save','load','exit'][button]+' panel')
def back(p):key(p,'Escape',180)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  url=f'http://127.0.0.1:{port}/index.html?build=campaign-controls-1004h';p.goto(url,timeout=120000);init(p,1)
  for expected in [8,7,6,5,4,3,2,1]:
   key(p,'ArrowLeft',180);ck(p.evaluate('(k)=>sselCursor===k&&state===GS.STAGESEL',expected),'Left mission ring reaches '+str(expected))
  for expected in [2,3,4,5,6,7,8,1]:
   key(p,'ArrowRight',180);ck(p.evaluate('(k)=>sselCursor===k&&state===GS.STAGESEL',expected),'Right mission ring reaches '+str(expected))
   if expected==4:ck(p.evaluate('()=>sselShip.head===Math.PI'),'actual 3 to 4 hull faces downward')
  for route in [None,'left','right']:
   init(p,6,route);key(p,'ArrowUp',1200)
   ck(p.evaluate('()=>map4hXFocused()&&cmap2.focus==="map"&&state===GS.STAGESEL'),'Up from VI selects '+str(route)+' Stage X')
   ck(p.evaluate('()=>sselShip.cur==="x"&&sselShip.head===0'),'ship travels upward from VI to '+str(route)+' X')
   key(p,'ArrowDown',700);ck(p.evaluate('()=>sselCursor===6&&!map4hXFocused()&&state===GS.STAGESEL'),'Down from '+str(route)+' X returns to VI')
   ck(p.evaluate('()=>sselShip.cur===6&&sselShip.head===Math.PI'),'ship returns downward from '+str(route)+' X to VI')
   key(p,'ArrowUp',700);menu(p,0);key(p,'ArrowUp');ck(p.evaluate('()=>campPause?.mode==="save"&&campPause.sel===23'),'open save panel owns Up over '+str(route)+' X')
   key(p,'ArrowDown');key(p,'ArrowDown');ck(p.evaluate('()=>campPause?.mode==="save"&&campPause.sel===1'),'open save panel owns Down over '+str(route)+' X')
   back(p);ck(p.evaluate('()=>!campPause&&cmap2.focus==="bar"&&state===GS.STAGESEL'),'Back closes slots to top menu without leaving map')
  init(p,3);menu(p,0);key(p,'ArrowDown');key(p,'ArrowDown');fire(p,350)
  ck(p.evaluate('()=>campPause?.mode==="save"&&campPause.sel===2&&campReadSlot(2)?.score===54321&&campReadSlot(2).stage===3'),'real slot confirmation saves the selected stage and score to slot 3')
  ck(p.evaluate('()=>campPause.msg==="SAVED TO SLOT 3"&&campSlotUsed(2)'),'verified save remains visible with correct receipt')
  p.screenshot(path=str(O/'save-slots.png'))
  # Observe generated slot frames and their saved ship in the actual game context.
  p.evaluate('()=>{window.__slotArt=new Set();const save=ctx.drawImage.bind(ctx);ctx.drawImage=function(im,...a){for(const key of ["map4h_slot_red","map4h_slot_white","map4h_slot_blue_hi","ship_yuri"])if(XART.rdy(key)&&im===XART.get(key)&&a.every(Number.isFinite))__slotArt.add(key);return save(im,...a);};}')
  p.wait_for_timeout(250);ck(p.evaluate('()=>__slotArt.has("map4h_slot_blue_hi")&&__slotArt.has("ship_yuri")'),'selected generated cartridge and saved pilot hull draw in native renderer')
  key(p,'ArrowRight');ck(p.evaluate('()=>campPause.sel===6'),'Right pages four slots without returning to the map')
  for i in range(5):key(p,'ArrowRight',70)
  ck(p.evaluate('()=>campPause.sel===23'),'last save slot stays reachable')
  fire(p,250);ck(p.evaluate('()=>campReadSlot(23)?.pilot==="yuri"'),'last slot 24 actually writes')
  # Silent write failure must retain selection, say failure and leave prior bytes.
  p.evaluate('()=>{window.__storeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){};run.score=99999;}');fire(p,250)
  ck(p.evaluate('()=>campPause?.sel===23&&campPause.msg.includes("SAVE FAILED")&&campReadSlot(23).score===54321'),'silent blocked write reports failure and preserves previous save')
  p.evaluate('()=>{Storage.prototype.setItem=window.__storeSet;}')
  p.reload(timeout=120000);init(p,1)
  ck(p.evaluate('()=>campReadSlot(2)?.stage===3&&campReadSlot(23)?.score===54321'),'both manual slots survive real browser reload')
  menu(p,1);key(p,'ArrowDown');key(p,'ArrowDown');fire(p,700)
  ck(p.evaluate('()=>!campPause&&state===GS.STAGESEL&&sselCursor===3&&run.pilot==="yuri"&&run.score===54321&&diffKey==="furious"'),'load slot 3 restores stage, pilot, score and difficulty to the map')
  menu(p,1);fire(p,250);ck(p.evaluate('()=>campPause?.mode==="load"&&campPause.msg==="THAT SLOT IS EMPTY"'),'loading an empty slot keeps the load panel open')
  p.screenshot(path=str(O/'load-slots.png'));back(p);key(p,'ArrowRight');fire(p,600)
  ck(p.evaluate('()=>campPause?.mode==="exit"'),'top-menu Exit remains selectable after load')
  fire(p,250);ck(p.evaluate('()=>!campPause&&state===GS.STAGESEL'),'safe default Exit choice stays on the campaign map')
  # Both earned X fights now deploy via FIRE, while Start belongs to the bar.
  for route in ['left','right']:
   init(p,6,route);key(p,'ArrowUp',600);fire(p,450)
   ck(p.evaluate('(r)=>state===GS.PLAY&&run._gp4StageX===r',route),'FIRE launches the earned '+route+' Stage X fight')
   p.evaluate('()=>{storySkip();BOFCinematicDirector.cancel();Audio.stopMusic();}')
  # Save/load X focus and bonus access through the same real storage store.
  init(p,6,'left');key(p,'ArrowUp',600);menu(p,0);fire(p,250);back(p)
  init(p,1);menu(p,1);fire(p,650)
  ck(p.evaluate('()=>CF4.focus&&campaign.stageX1004?.route==="left"&&sselCursor===6'),'loading saved Stage X restores its city focus and earned Harrier route')
  init(p,9);p.evaluate('()=>{campaign.bonusUnlocked=true;openStageSelect(9,{});sselBoot=0;s9MapCine=null;sselUnlockCine=null;}');p.wait_for_timeout(500)
  key(p,'ArrowLeft');key(p,'ArrowRight');key(p,'ArrowUp');key(p,'ArrowDown')
  ck(p.evaluate('()=>sselCursor===9&&!map4hXFocused()&&cmap2.focus==="map"'),'all D-pad directions preserve the earned Stage IX gate')
  menu(p,0);key(p,'ArrowDown');key(p,'ArrowDown');key(p,'ArrowDown');fire(p,450);back(p)
  init(p,1);menu(p,1);key(p,'ArrowDown');key(p,'ArrowDown');key(p,'ArrowDown');fire(p,650)
  ck(p.evaluate('()=>sselCursor===9&&campaign.bonusUnlocked&&state===GS.STAGESEL'),'saved Stage IX access survives the real load flow')
  p.set_viewport_size({'width':1000,'height':900});p.reload(timeout=120000);init(p,3);menu(p,0);p.screenshot(path=str(O/'compact-save.png'))
  ck(p.evaluate('()=>MAP4H.rows.every(r=>r.x>=0&&r.x+r.w<=VW&&r.y>=CM2_BAR.y+CM2_BAR.h&&r.y+r.h<VH)'),'all cartridge rows fit compact screen below the top menu')
  # Review fixture uses a real persistent namespace without touching live slots.
  p.goto(f'http://127.0.0.1:{port}/_shots/campaign_controls_1004h/review.html',timeout=120000)
  p.wait_for_function('()=>document.getElementById("game").contentWindow.__map4hPreviewStorage',timeout=120000);p.wait_for_timeout(1500)
  p.locator('button[data-stage="save"]').click();p.wait_for_timeout(950)
  frame=p.frame_locator('#game');canvas=frame.locator('#screen');canvas.click(position={'x':5,'y':5})
  # Focus actual frame and use its own FIRE key; keep click outside rows.
  w=p.frames[-1];f=w.evaluate('()=>keybind.fire.find(k=>!/^mouse|^pad_|^enter$/.test(k))||" "');key(p,f,300)
  ck(w.evaluate('()=>campSlotUsed(0)&&campPause?.msg==="SAVED TO SLOT 1"'),'review save persists instead of silently discarding slot writes')
  p.reload(timeout=120000);p.wait_for_function('()=>document.getElementById("game").contentWindow.__map4hPreviewStorage',timeout=120000)
  ck(p.frames[-1].evaluate('()=>campReadSlot(0)?.pilot==="lizzie"'),'review slot survives page reload in its separate namespace')
  ck(not errors,'zero page and console errors');b.close()
finally:stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
