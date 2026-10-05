"""Additional actual-engine pointer, pad, autosave and campaign-hub checks."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_controls_1004h';checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def tap(p,k,ms=500):p.evaluate('(k)=>Input.injectTap(k)',k);p.wait_for_timeout(ms)
def realkey(p,k,ms=500):p.keyboard.press('Space' if k==' ' else k);p.wait_for_timeout(ms)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate('()=>{ht27Stop();run.mode="campaign";run.pilot="axel";pilotIndex=PILOTS.findIndex(p=>p.key==="axel");run.stage=4;run.score=32100;campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.rivalScattered=false;campaign.stageX1004={route:"right",done:false};CF4.focus=false;CF4.flight=4;openStageSelect(6,{});sselBoot=0;sselUnlockCine=null;Input.mouse.moved=false;map4hWarm();}')
  p.wait_for_function('()=>MAP4E.readiness&&XART.rdy("map4h_slot_red_hi")&&XART.rdy("ship_axel")&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000);p.wait_for_timeout(500)
  tap(p,'pad_b9');ck(p.evaluate('()=>cmap2.focus==="bar"&&state===GS.STAGESEL'),'controller Start selects the top menu')
  tap(p,'pad_b9');ck(p.evaluate('()=>campPause?.mode==="save"'),'second Start confirms highlighted top-menu action')
  tap(p,'pad_down',100);ck(p.evaluate('()=>campPause?.sel===1&&state===GS.STAGESEL'),'controller Down belongs to save slots')
  tap(p,'pad_up',100);ck(p.evaluate('()=>campPause?.sel===0'),'controller Up belongs to save slots')
  tap(p,'pad_b0');ck(p.evaluate('()=>campReadSlot(0)?.pilot==="axel"&&campPause.msg==="SAVED TO SLOT 1"'),'controller A writes selected manual slot')
  # Pointer selects another row and saves once, using actual visible bounds.
  q=p.evaluate('()=>{const r=MAP4H.rows[2],b=cv.getBoundingClientRect();return {x:b.left+(r.x+r.w*.55+campaignViewOffset())/campaignViewWidth()*b.width,y:b.top+(r.y+r.h*.5)/VH*b.height};}')
  p.mouse.click(q['x'],q['y'],delay=80);p.wait_for_timeout(400)
  ck(p.evaluate('()=>campPause?.sel===2&&campReadSlot(2)?.score===32100'),'pointer saves the clicked cartridge without switching map stages')
  p.screenshot(path=str(O/'pointer-save.png'))
  tap(p,'pad_b1',250);ck(p.evaluate('()=>!campPause&&cmap2.focus==="bar"'),'controller B closes slots to bar')
  p.evaluate('()=>{cmap2.bar=1;Input.mouse.moved=false;campAutoAfterClear(5,6,"S");}')
  tap(p,'pad_b0',650);tap(p,'pad_up',250)
  ck(p.evaluate('()=>campPause?.mode==="load"&&campPause.sel===CAMP_SLOTS'),'autosave is a selectable entry after the manual slots')
  p.screenshot(path=str(O/'auto-load.png'));tap(p,'pad_b0',700)
  ck(p.evaluate('()=>!campPause&&sselCursor===6&&run.pilot==="axel"&&run.score===32100'),'controller A loads the actual campaign autosave')
  # Campaign hub uses the same authored cartridge art and storage controller.
  p.evaluate('()=>{campPause=null;CF4.focus=false;MAP4E.xPreview=false;run.stage=4;run.score=67890;campPick="save";campHubIndex=1;campHubMsg="";campHubMsgT=0;setState(GS.CAMPHUB);Input.mouse.moved=false;Input.clearTaps();}')
  p.wait_for_timeout(400);tap(p,'pad_b0',500)
  ck(p.evaluate('()=>campReadSlot(1)?.stage===4&&campReadSlot(1).score===67890'),'hub save writes a real campaign checkpoint')
  ck(p.evaluate('()=>campHubMsg==="SAVED TO SLOT 2"&&campHubMsgT>0'),'hub save receipt survives the confirmation flash callback')
  p.screenshot(path=str(O/'hub-save.png'));p.wait_for_timeout(2300)
  ck(p.evaluate('()=>campHubMsgT===0'),'hub receipt expires without being reset each frame')
  tap(p,'pad_b1',200);ck(p.evaluate('()=>state===GS.CAMPHUB&&!campPick'),'hub Back returns to campaign hub without exiting campaign')
  p.evaluate('()=>{campPick="load";campHubIndex=1;run.score=0;}');tap(p,'pad_b0',500)
  ck(p.evaluate('()=>state===GS.STAGESEL&&sselCursor===4&&run.score===67890'),'hub load restores checkpoint to campaign map')
  # Actual Exit confirmation is deliberate, with Stay as the initial selection.
  realkey(p,'Enter',200);p.evaluate('()=>{cmap2.bar=2;Input.mouse.moved=false;}');tap(p,'pad_b0',650)
  ck(p.evaluate('()=>campPause?.mode==="exit"&&campPause.sel===1'),'Exit starts on the safe Stay choice')
  tap(p,'pad_up',150);tap(p,'pad_b0',600)
  ck(p.evaluate('()=>state===GS.TITLE&&run.mode==="arcade"'),'explicit Exit confirmation ends campaign and returns to title')
  ck(not errors,'zero page and console errors in pointer/pad/hub flows');b.close()
finally:stop()
(O/'slot-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
