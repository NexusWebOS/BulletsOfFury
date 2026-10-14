from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/flight_variants_1012';port,stop=shoot.serve(str(R));rows=[];errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://localhost:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage in [1,4,6,8]:
   p.evaluate('()=>{diffKey="furious";DIFF=DIFFS.furious;}');p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'axel','invuln':False});p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&XART.rdy(VP12_ART[n].key)}',arg=stage,timeout=120000)
   p.evaluate('()=>{VP12.events=[];VP12.next=10;player.invuln=0;run.lives=3;run.shield=5;run.speedLevel=5;run.weapon=1;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);Input.keys={};s6Opening=null;s6Wing=null;story=null;run._mission29OpeningDone=true;for(const k of keybindFor(1).fire||[])Input.keys[k]=true;}')
   for i in range(48):
    p.evaluate('i=>{for(const name of ["left","right"])for(const k of keybindFor(1)[name]||[])Input.keys[k]=(name==="right")===((Math.floor(i/4)%2)===0)}',i);p.evaluate(shoot.STEP,30);p.wait_for_timeout(10)
   row=p.evaluate('()=>({stage:run.stage,state,elapsedStageTime:stageTimer,lives:run.lives,shield:run.shield,formations:VP12.events.filter(e=>e.event==="formation"),shots:VP12.events.filter(e=>e.event==="volley"||e.event==="bomb-drop").length,finite:Number.isFinite(player.x)&&Number.isFinite(player.y)})');rows.append(row);assert row['finite'];print(json.dumps(row),flush=True);p.screenshot(path=str(O/f'live-stage{stage}.png'))
  b.close()
finally:stop()
(O/'live-verification.json').write_text(json.dumps({'results':rows,'errors':errors},indent=2));assert not errors,errors
