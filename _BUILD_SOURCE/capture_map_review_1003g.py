"""Final screenshots with all native animation callbacks, plus review media validation."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/map_briefing_1003g';errors=[]
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  setup="()=>{run.mode='campaign';run.pilot='lizzie';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.rivalScattered=false;campaign.bonusUnlocked=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;}"
  p.evaluate(setup);p.wait_for_timeout(5500);p.screenshot(path=str(O/'desktop.png'))
  p.evaluate("()=>{campaign.rivalScattered=true;campaign.rivalDefeated=[];Input.injectTap('arrowdown');}")
  p.wait_for_timeout(4500);p.screenshot(path=str(O/'stage_x.png'))
  p.evaluate("()=>{Rival24.mapBack();campaign.rivalScattered=false;openStageSelect(4,{});sselBoot=0;sselUnlockCine=null;}")
  p.set_viewport_size({'width':1000,'height':900});p.wait_for_timeout(4500);p.screenshot(path=str(O/'compact.png'))
  p.set_viewport_size({'width':480,'height':800});p.wait_for_timeout(500);p.screenshot(path=str(O/'narrow.png'))
  p.set_viewport_size({'width':1920,'height':1080});p.evaluate("()=>{setState(GS.PILOT);pilotIndex=PILOTS.findIndex(p=>p.key==='lizzie');}")
  p.wait_for_timeout(4000);p.screenshot(path=str(O/'lizzie_pilot.png'))
  p.goto(f'http://127.0.0.1:{port}/_shots/map_briefing_1003g/review.html');p.wait_for_function("()=>Array.from(document.querySelectorAll('img')).every(i=>i.complete&&i.naturalWidth>0)&&Array.from(document.querySelectorAll('video')).every(v=>v.readyState>=1)",timeout=30000)
  media=p.evaluate("()=>Array.from(document.querySelectorAll('video')).map(v=>({file:v.getAttribute('src'),duration:v.duration,width:v.videoWidth,height:v.videoHeight}))")
  assert all(v['duration']>4 and v['width']>0 for v in media)
  p.screenshot(path=str(O/'review-desktop.png'))
  p.set_viewport_size({'width':420,'height':900});p.wait_for_timeout(100)
  assert p.evaluate('()=>document.documentElement.scrollWidth<=innerWidth')
  (O/'review-checks.json').write_text(json.dumps({'errors':errors,'media':media,'mobileOverflow':False},indent=2),encoding='utf-8')
  b.close()
finally:stop()
print(json.dumps({'errors':errors,'media':media}))
assert not errors,errors
