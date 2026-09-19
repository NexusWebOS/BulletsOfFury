import os,sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
out=root/'_shots'/'widescreen_0918';out.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(root))
errs=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
  pg.on('pageerror',lambda e:errs.append(str(e)[:250]));pg.on('console',lambda m:errs.append(m.text[:250]) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
  pg.wait_for_function("typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=45000)
  pg.evaluate("""() => {document.body.classList.add('fs');__bofFit();run.mode='campaign';run.pilot='yuri';run.stage=4;run.score=231450;run.lives=3;diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.unlockedMax=5;campaign.rank={1:'S',2:'A',3:'B'};openStageSelect(4,{});} """)
  pg.wait_for_timeout(2500)
  pg.screenshot(path=str(out/'campaign_map.png'))
  mapInfo=pg.evaluate("""() => ({left:document.getElementById('wide-left').getBoundingClientRect().toJSON(),right:document.getElementById('wide-right').getBoundingClientRect().toJSON(),clock:document.getElementById('wide-clock').getBoundingClientRect().toJSON(),hud:document.getElementById('hud-row').getBoundingClientRect().toJSON(),hudBg:getComputedStyle(document.getElementById('hud-row')).backgroundImage,classes:document.body.className,frame:document.getElementById('game-frame').getBoundingClientRect().toJSON(),visible:getComputedStyle(document.getElementById('wide-left')).display})""")
  pg.evaluate("""() => {campPick='load';campHubIndex=23;setState(GS.CAMPHUB);} """)
  pg.wait_for_timeout(1000);pg.screenshot(path=str(out/'save_slots_page5.png'))
  pg.evaluate("""() => {campPick=null;run.mode='campaign';menuIndex=4;setState(GS.DIFF);} """)
  pg.wait_for_timeout(1000);pg.screenshot(path=str(out/'insanity_locked.png'))
  pg.evaluate("""() => {beginStage(2);setState(GS.PLAY);} """)
  pg.wait_for_timeout(2000);pg.screenshot(path=str(out/'gameplay.png'))
  save=pg.evaluate("""() => {localStorage.clear();run.mode='campaign';run.pilot='yuri';run.stage=2;run.score=100;campaign.unlockedMax=2;campaign.rank={1:'S'};const manual=campWriteSlot(23);const checkpoint=campAutoAfterClear(2,3,'A');campSession=null;const recovered=campCanContinue();const next=campSession&&campSession.stage;localStorage.removeItem(campSlotKey(23));const autoOnlyLoad=campHubEnabled('load');localStorage.setItem(campSlotKey(23),JSON.stringify(campSession));campBeginFresh();return {manual,checkpoint,recovered,next,autoOnlyLoad,slots:CAMP_SLOTS,manualSurvives:campSlotUsed(23),autoCleared:!localStorage.getItem(CAMP_AUTO_KEY),rankCleared:Object.keys(campaign.rank).length===0};}""")
  fresh=pg.evaluate("""() => {run.mode='campaign';campaign.rank={1:'S'};localStorage.setItem(CAMP_AUTO_KEY,JSON.stringify({...campSnapshot(),mode:'campaign'}));startRun(1);return {autoCleared:!localStorage.getItem(CAMP_AUTO_KEY),rankCleared:Object.keys(campaign.rank).length===0,stage:run.stage};}""")
  print(json.dumps({'map':mapInfo,'save':save,'freshStart':fresh,'errors':errs[:10]},indent=2))
  b.close()
finally:stop()
