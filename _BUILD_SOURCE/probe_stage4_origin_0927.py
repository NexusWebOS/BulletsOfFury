import json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/furious_0927';out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page();p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';beginStage(4);setState(GS.PLAY);story=null;player.invuln=99999;for(const k in Input.keys)Input.keys[k]=false;Input.keys.j=true;window.trace=[];window.lastP=null;const draw=drawPlayer;drawPlayer=function(){const m=ctx.getTransform(),v={x:player.x,y:player.y,sx:m.a*player.x+m.c*player.y+m.e,sy:m.b*player.x+m.d*player.y+m.f,stack:new Error().stack,ww:worldWidth(),vw:viewW(),base:_wdScreenM?{a:_wdScreenM.a,e:_wdScreenM.e}:null,scale:m.a,cam:camX,scroll:mapScroll,kill:stageStats.kills,frame:window.f};if(window.lastP){v.delta=Math.hypot(v.sx-window.lastP.sx,v.sy-window.lastP.sy);if(v.delta>5)window.trace.push(v);}window.lastP=v;return draw();};}")
  p.wait_for_function("()=>XART.rdy(stageMasterKey(_levelCfg()))")
  for i in range(60):
   p.evaluate("()=>{for(let i=0;i<180;i++){window.f=(window.f||0)+1;updatePlay(1/60);drawWorld(1/60);}}")
   p.wait_for_timeout(50)
  report=p.evaluate('()=>({jumps:trace,last:lastP,kills:stageStats.kills,enemies:enemies.map(e=>({type:e.type,x:e.x,y:e.y}))})');report['errors']=errors
  (out/'stage4-origin.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
