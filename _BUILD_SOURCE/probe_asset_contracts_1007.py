from pathlib import Path
import sys,json,time,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/asset_layout_1007/contracts';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));out={'checks':[],'errors':[],'cadence':[]}
def ck(ok,name):
 out['checks'].append({'ok':bool(ok),'name':name});print(('OK ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   br=getattr(pw,engine).launch();p=br.new_page();p.set_default_timeout(120000)
   p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
   p.on('pageerror',lambda e:out['errors'].append(str(e)))
   p.on('response',lambda r:out['errors'].append(str(r.status)+' '+r.url) if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
   ck(p.evaluate('()=>{const a="assets/game/logo.png",b=bofAssetPath(a);XART._src.qa_alias_a=a;XART._src.qa_alias_b=b;return XART.get("qa_alias_a")===XART.get("qa_alias_b");}'),engine+' aliases share one Image object')
   p.wait_for_function('()=>XART.rdy("qa_alias_a")')
   ck(p.evaluate('()=>{const im=XART.get("qa_alias_a");XART.releaseRoot("qa_alias_a");const same=XART.get("qa_alias_b");delete XART._src.qa_alias_a;delete XART._src.qa_alias_b;return im!==same;}'),engine+' release invalidates all aliases and reloads cleanly')
   for stage in [1,4,8,1]:
    p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
    deadline=time.monotonic()+100
    while time.monotonic()<deadline:
     p.evaluate('()=>stageLoadTick()');p.wait_for_timeout(30)
     if p.evaluate('()=>stageLoadInfo(run.stage).ready'):break
    ck(p.evaluate('()=>stageLoadInfo(run.stage).ready&&stageLoadInfo(run.stage).failed===0'),engine+' transition/reentry stage '+str(stage))
   ck(p.evaluate('()=>BOF_MEMORY.history.some(h=>h.released>0)'),engine+' stage changes retire owned textures')
   ck(p.evaluate('()=>{setRenderScale(2);_renderScaleChanged=false;_renderQuality="auto";_renderSlowT=0;stateT=10;for(let i=0;i<90;i++)renderPerformanceTick(1/60);return SS===2;}'),engine+' 60 Hz preserves supersampling')
   ck(p.evaluate('()=>{for(let i=0;i<65;i++)renderPerformanceTick(.025);return SS===1;}'),engine+' sustained 40 Hz switches to native pixels')
   p.evaluate('()=>{_renderQuality="high";setRenderScale(2);_renderScaleChanged=false;_renderSlowT=0;for(let i=0;i<80;i++)renderPerformanceTick(.04);}')
   ck(p.evaluate('()=>SS===2'),engine+' explicit high quality remains locked')
   # Observe real scheduling, not a tight synchronous draw loop. This fixture is
   # one protected encounter on this machine; it does not prove other hardware.
   cadence=p.evaluate('''()=>new Promise(resolve=>{let last=0,n=0;const intervals=[];function frame(t){if(last)intervals.push(t-last);last=t;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);if(++n<121)__bofRealRAF(frame);else{intervals.sort((a,b)=>a-b);resolve({medianMs:intervals[60],p95Ms:intervals[114],ss:SS});}}__bofRealRAF(frame);})''')
   out['cadence'].append({'engine':engine,**cadence})
   for quality,expected in [('auto',1),('high',2),('performance',1)]:
    q=br.new_page();q.add_init_script('Object.defineProperty(navigator,"deviceMemory",{get:()=>2});Object.defineProperty(navigator,"hardwareConcurrency",{get:()=>2});')
    q.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
    q.goto(f'http://127.0.0.1:{port}/index.html?quality={quality}');q.wait_for_function('()=>window.__bofFrames>2');ck(q.evaluate('()=>SS')==expected,engine+' low-spec '+quality+' quality');q.close()
   br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');assert all(c['ok'] for c in out['checks']) and not out['errors'];print('CONTRACTS PASSED',len(out['checks']),json.dumps(out['cadence']))
