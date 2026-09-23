from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP
from playwright.sync_api import sync_playwright
O=Path('_shots/campaign_full_0922');O.mkdir(exist_ok=True);errors=[];r={};port,stop=serve(GAME)
try:
 with sync_playwright() as p:
  b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page(viewport={'width':1920,'height':1080})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4')
  pg.evaluate("()=>{document.body.classList.add('fs');run.mode='campaign';run.pilot='yuri';run.stage=4;campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};openStageSelect(4,{});}")
  pg.wait_for_timeout(2000);pg.screenshot(path=str(O/'full_map.png'))
  r['viewport']=pg.evaluate("()=>({width:cv.width/SS,expected:Math.round(VH*innerWidth/innerHeight),rect:cv.getBoundingClientRect().toJSON(),extender:!!document.getElementById('wide-map-world'),offset:campaignViewOffset()})")
  points=pg.evaluate("()=>{let rr=cv.getBoundingClientRect(),k=rr.height/VH;return [1,2,3,4,5,6,7,8].map(st=>{let w=cmap2World(st),p=cmap2ToScreen(w.x,w.y);return {st,x:rr.left+(p.x+campaignViewOffset())*k,y:rr.top+p.y*k,nativeX:p.x};});}")
  point=next(q for q in points if q['nativeX']<0 and q['x']>30 and 150<q['y']<950)
  pg.mouse.move(point['x'],point['y']);pg.mouse.down();pg.wait_for_timeout(120);pg.mouse.up();pg.wait_for_timeout(500);r['outerClick']={'target':point['st'],'selected':pg.evaluate('()=>sselCursor'),'committed':pg.evaluate('()=>!!window.sselCommitted')}
  # Freeze the deploy animation at its midpoint to inspect the full-world transform.
  pg.evaluate("()=>{window.__zoomTick=sselZoomTick;sselZoomTick=()=>{};sselDeploy(sselCursor,()=>{});sselZoom.t=.65;}")
  pg.wait_for_timeout(250);pg.screenshot(path=str(O/'full_map_zoom.png'))
  pg.evaluate("()=>{sselZoom=null;sselZoomTick=window.__zoomTick;}");pg.wait_for_timeout(200)
  save=pg.evaluate("()=>{const r=cmap2BtnRects()[0],s=cv.getBoundingClientRect(),k=s.height/VH;return {x:s.left+(r.x+r.w/2+campaignViewOffset())*k,y:s.top+(r.y+r.h/2)*k};}")
  pg.mouse.move(save['x'],save['y']);pg.mouse.down();pg.wait_for_timeout(120);pg.mouse.up();pg.wait_for_timeout(450);r['save']=pg.evaluate('()=>campPause&&campPause.mode');r['clockHidden']=pg.evaluate("()=>getComputedStyle(document.getElementById('wide-clock')).display==='none'");pg.screenshot(path=str(O/'save_overlay.png'))
  pg.evaluate("()=>{campPauseClose();}")
  load=pg.evaluate("()=>{const r=cmap2BtnRects()[1],s=cv.getBoundingClientRect(),k=s.height/VH;return {x:s.left+(r.x+r.w/2+campaignViewOffset())*k,y:s.top+(r.y+r.h/2)*k};}")
  pg.mouse.move(load['x'],load['y']);pg.mouse.down();pg.wait_for_timeout(120);pg.mouse.up();pg.wait_for_timeout(450);r['load']=pg.evaluate('()=>campPause&&campPause.mode')
  pg.evaluate("()=>{campPauseClose();document.body.classList.remove('fs');}")
  pg.set_viewport_size({'width':1600,'height':1200});pg.wait_for_timeout(500);pg.screenshot(path=str(O/'map_4_3.png'))
  r['fourThree']=pg.evaluate('()=>({width:cv.width/SS,expected:Math.round(VH*innerWidth/innerHeight),rect:cv.getBoundingClientRect().toJSON()})')
  pg.set_viewport_size({'width':1280,'height':720});pg.wait_for_timeout(500);pg.screenshot(path=str(O/'map_1280.png'))
  r['resize']=pg.evaluate('()=>({width:cv.width/SS,expected:Math.round(VH*innerWidth/innerHeight),height:cv.height/SS})')
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'yuri','invuln':True});pg.wait_for_timeout(150)
  r['exit']=pg.evaluate("()=>({width:cv.width/SS,full:document.body.classList.contains('campaign-full')})")
  r['errors']=errors;b.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors
assert r['viewport']['width']==r['viewport']['expected'] and not r['viewport']['extender']
assert r['outerClick']['target']==r['outerClick']['selected'] and not r['outerClick']['committed']
assert r['save']=='save' and r['load']=='load' and r['clockHidden']
assert r['fourThree']['width']==r['fourThree']['expected'] and r['fourThree']['rect']['width']==1600
assert r['resize']['width']==r['resize']['expected'] and r['resize']['height']==512
assert r['exit']=={'width':480,'full':False}
