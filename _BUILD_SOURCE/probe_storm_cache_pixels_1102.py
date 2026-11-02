"""Compare source-sheet and cached-cell pixels in the actual game context."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
out=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('''()=>{EA11.setup(6,'furious');spawnSubBoss('siegefortress17');window.B=subBoss;window.sheetBlit=fb112Blit;}''');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000);p.add_script_tag(path=str(R/'_BUILD_SOURCE/storm_frame_cache_candidate_1102.js'))
 out=p.evaluate('''()=>{window.cellBlit=fb112Blit;B.x=VW/2;B.y=200;B.t=4;B.enter=false;B.sub=false;const q=B._fb112,rows=[];const pixels=fn=>{fb112Blit=fn;ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,VW,VH);fb112Draw(B);const data=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return data;};for(let pose=0;pose<9;pose++){q.phase=pose?'attack':'recover';q.attack=pose?'pass':'guns';q.pose=pose?q.M.clips.roll[pose-1]:0;q.heading=pose?Math.atan2(45,790):Math.PI/2;for(const hit of [false,true]){q.parts.forEach(p=>p.flash=hit?.06:0);const a=pixels(sheetBlit);if(!pose&&!hit)window.cacheBefore=cv.toDataURL();const z=pixels(cellBlit);if(!pose&&!hit)window.cacheAfter=cv.toDataURL();let changed=0,max=0,alpha=0;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-z[i]);if(d){changed++;max=Math.max(max,d);if(i%4===3)alpha++;}}rows.push({pose,hit,changed,max,alpha});}}return{rows,cacheBytes:FB112.cellBytes,cells:FB112.cells.size};}''');
 for key in ['cacheBefore','cacheAfter']:(R/'_shots/furious_encounters_1102'/('idle-'+key+'.png')).write_bytes(base64.b64decode(p.evaluate('k=>window[k].split(",")[1]',key)))
 b.close()
(R/'_shots/furious_encounters_1102/cache-pixels.json').write_text(json.dumps(out,indent=2));print(out)
