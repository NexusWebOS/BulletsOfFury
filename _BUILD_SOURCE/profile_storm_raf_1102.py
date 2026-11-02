"""Two native RAF samples; cache candidate is confined to this QA browser."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];out={}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate('''()=>{window.rafSetup=()=>{EA11.setup(6,'furious');stagePlan=[];waveIdx=999;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;s6Wing.ships=[];ally=null;spawnSubBoss('siegefortress17');};rafSetup();}''');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000)
 for mode in ['base','cellCache']:
  if mode=='cellCache':p.evaluate('''()=>{const cells=new Map();fb112Blit=function(name,f,x,y,k=1,a=Math.PI/2,flash=false,alpha=1){const B=FB112_ART.banks[name];if(!B||!XART.rdy(B.key))return false;const n=clamp(f|0,0,B.frames-1)*B.dirs+(B.dirs>1?fb112Dir(a,B.dirs):0),tag=B.key+':'+n;let c=cells.get(tag);if(!c){c=document.createElement('canvas');c.width=c.height=B.cell;c.getContext('2d',{willReadFrequently:true}).drawImage(XART.get(B.key),n%B.cols*B.cell,Math.floor(n/B.cols)*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);cells.set(tag,c);}ctx.save();ctx.globalAlpha*=alpha;const s=B.cell*k;ctx.drawImage(c,x-s/2,y-s/2,s,s);ctx.restore();return true;};}''')
  p.evaluate('rafSetup()');start=p.evaluate('({frames:__bofFrames,t:performance.now()})');p.wait_for_timeout(18000);end=p.evaluate('({frames:__bofFrames,t:performance.now(),phase:subBoss?._fb112?.phase})');out[mode]=dict(fps=(end['frames']-start['frames'])*1000/(end['t']-start['t']),end=end);print(mode,out[mode],flush=True)
 b.close()
(R/'_shots/furious_encounters_1102/raf-profile.json').write_text(json.dumps(out,indent=2))
