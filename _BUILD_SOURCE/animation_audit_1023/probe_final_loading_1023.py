from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  p.evaluate('EA11.setup(8,"normal")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8);}')
  loading=p.evaluate('''()=>({retired:PH23_RETIRED.size,decodedBytesAvoided:PH23_RETIRED_BYTES,retiredKeys:[...PH23_RETIRED],requestedRetired:hf22Keys(8).filter(k=>PH23_RETIRED.has(k)),activeReady:Object.values(PH23_ART.sheets).every(s=>XART.rdy(s.key)),stage5Unchanged:JSON.stringify(hf22Keys(5))===JSON.stringify(PH23_KEYS(5))})''')
  specs=json.loads((W/'roster/catalog.json').read_text());spec=next(s for r in specs['stages']if r['stage']==8 for s in r['specs']if s['type']=='s8carrier')
  p.evaluate('''s=>{AQ23.begin(s);bossWarned=false;E.hp=E.maxhp=10000;E.x=worldWidth()/2;E.y=120;E._frArrival=false;E._noHit=false;camX=E.x-viewW()/2;window.EXTRA23=[];const base=AT23.base.shot;AT23.base.shot=function(x,y,a,v,row){if(AT23.actor===E&&!AT23.target)EXTRA23.push({x,y,a,v,row,stack:new Error().stack});return base.apply(this,arguments);};for(let i=0;i<420;i++){E.y=120;player.invuln=40002;AQ23.step(1);}}''',spec)
  extras=p.evaluate('EXTRA23');out={'loading':loading,'nonVolleyShots':extras,'errors':errors};(W/'final-loading.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert not loading['requestedRetired']and loading['activeReady']and loading['stage5Unchanged']and not errors
  br.close()
finally:stop()
