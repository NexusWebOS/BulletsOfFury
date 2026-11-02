from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
bad=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page();p.on('response',lambda r:bad.append([r.status,r.url])if r.status>=400 else None);p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(8,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&s811Keys().every(k=>XART.rdy(k))}',timeout=180000);p.wait_for_timeout(1000);print(json.dumps(bad,indent=2));print(p.evaluate('()=>({leech:S8MEGA.s8leech,src:Object.keys(XART._src).filter(k=>/armored_leech|s81003_gravity/.test(k)),flame:typeof Audio.SFX.flameThrowerStart,keys:s811Keys().length})'));b.close()
(R/'_shots/stage8_amplify_1101/load-errors.json').write_text(json.dumps(bad,indent=2))
