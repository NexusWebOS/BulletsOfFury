from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/ngplus_1027';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  result=p.evaluate((R/'_BUILD_SOURCE/check_ngplus_1027.js').read_text())
  result['errors']=errors;result['checks']['noRuntimeErrors']=not errors
  p.wait_for_function("()=>Object.values(NG27_ART).every(a=>XART.rdy(a.key))",timeout=60000)
  p.evaluate("()=>{ctx.clearRect(0,0,VW,VH);for(const [i,el]of Object.keys(NG27_ART).entries())for(let n=0;n<5;n++)ng27ShotDraw({_ng27Shot:true,_ng27Element:el,x:52+n*78,y:42+i*48,vx:Math.sin(n)*2,vy:3,t:n*.13});}")
  p.screenshot(path=str(W/'elemental-native.png'))
  (W/'checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);br.close()
finally:stop()
