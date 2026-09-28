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
  p.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';beginStage(4);setState(GS.PLAY);story=null;player.invuln=99999;for(const k in Input.keys)Input.keys[k]=false;Input.keys.j=true;window.trace=[];window.lastP=null;const draw=drawPlayer;drawPlayer=function(){const m=ctx.getTransform(),v={x:player.x,y:player.y,sx:m.a*player.x+m.c*player.y+m.e,sy:m.b*player.x+m.d*player.y+m.f,scale:m.a,cam:camX,scroll:mapScroll,kill:stageStats.kills,frame:window.f};if(window.lastP){v.delta=Math.hypot(v.sx-window.lastP.sx,v.sy-window.lastP.sy);if(v.delta>5)window.trace.push(v);}window.lastP=v;return draw();};}")
  p.evaluate("""async()=>{const source=await(await fetch('assets/game.js')).text();window.leaks=[];const names=[...source.matchAll(/function\s+((?:draw|.*Draw)[A-Za-z0-9_]*)\s*\(/g)].map(m=>m[1]);for(const n of new Set(names)){if(['drawWorld','drawBG','drawPlayer','worldXformEscape'].includes(n))continue;try{const original=eval(n);eval(n+'=function(...a){const b=ctx.getTransform();let r,err;try{r=original.apply(this,a);}catch(e){err=String(e);}const c=ctx.getTransform();if((b.e!==c.e||b.f!==c.f||b.a!==c.a)&&leaks.length<40)leaks.push({name:n,frame:window.f,from:[b.a,b.e,b.f],to:[c.a,c.e,c.f],enemy:a[0]?.type,error:err});if(err)throw new Error(err);return r;}');}catch(e){}}}""")
  p.wait_for_function("()=>XART.rdy(stageMasterKey(_levelCfg()))")
  for i in range(60):
   p.evaluate("()=>{for(let i=0;i<180;i++){window.f=(window.f||0)+1;updatePlay(1/60);drawWorld(1/60);}}")
   p.wait_for_timeout(50)
  report=p.evaluate('()=>({leaks:window.leaks,jumps:trace,last:lastP,kills:stageStats.kills,enemies:enemies.map(e=>({type:e.type,x:e.x,y:e.y}))})');report['errors']=errors
  (out/'stage4-leaks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
