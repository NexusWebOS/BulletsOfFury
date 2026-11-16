from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/scroll';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(120000);p.goto('http://127.0.0.1:8765/index.html?freezer-scroll-pixels=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{BOFOnline.submitScore=()=>{};run.mode='campaign';run.stage=1;run.pilot='freezer';coopOn=false;const text=PILOT_OPENINGS.axel.beats.find(b=>b.who==='freezer').text;window.FZROW={id:'FREEZER-SCROLL-PIXELS',who:'FREEZER',text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people:['freezer','axel'],fpLocations:{freezer:'cockpit-sky',axel:'cockpit-sky'},duration:text.length/30+5,readings:[],_cueSet:new Set(),cm3:{group:'freezer-scroll-pixels',readAt:.42,newStrip:true,baseDuration:text.length/30+5}};d1110Play('freezer-scroll-pixels',[FZROW],()=>{});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys||[])');p.evaluate("()=>{for(let i=0;i<600;i++){BOFCinematicDirector.tick(1/60);if(BOFCinematicDirector.current)BOFCinematicDirector.draw();}}")
 p.locator('#screen').screenshot(path=str(O/'freezer-final-line.png'));q=p.evaluate('DS15.last');(O/'freezer-final-line.json').write_text(json.dumps(q,indent=2),encoding='utf8');b.close();assert q['offset']==q['max']and q['visible'][-1]['row']==len(q['rows'])-1
