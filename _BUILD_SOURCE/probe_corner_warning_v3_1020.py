from pathlib import Path
from PIL import Image,ImageChops
from io import BytesIO
import ast,base64,json,math,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';errors=[];checks=[];navigating=False;navigationCancels=[]
def literal(file,key):
 return next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE'/file).read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets))
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda route:route.fulfill(status=204,body=''))
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(dict(message=m.text[:500],location=m.location)) if m.type=='error' else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('requestfailed',lambda r:(navigationCancels if navigating and r.failure=='net::ERR_ABORTED' else errors).append(dict(url=r.url,failure=r.failure)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.evaluate(literal('probe_feedback_1002.py','SETUP'),dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'))
  p.evaluate('()=>{pw5Warm();}');p.wait_for_function('()=>{stageLoadTick();return b20Ready(PH21_ART);}',polling=80)
  p.evaluate(literal('probe_boss_redesign_1020.py','BOOT'))
  p.evaluate('''()=>{window.iconDraws=[];const original=b20Image;b20Image=function(a,x,y,k,rot){if(a?.key==='ph21_corner_warning'){const t=ctx.getTransform();iconDraws.push({x,y,k,rot,matrix:[t.a,t.b,t.c,t.d,t.e,t.f]});}return original.apply(this,arguments);};}''')
  for corner in range(4):
   row=p.evaluate('''corner=>{setup20(2);for(const id of ['cannonL','cannonR'])ph21Part(B,id).destroyed=true;Q.stage='swoon';let route;for(let i=0;i<100;i++){route=ph21Corner(B);if(route.corner===corner)break;}ph21Set(B,'corner',{...route,tell:1.1});tick20(24);iconDraws.length=0;paint20();const d=iconDraws.at(-1),t=d.matrix;return{corner:Q.action.corner,draw:d,key:K20.keys.has('ph21_corner_warning'),screen:[t[0]*d.x+t[2]*d.y+t[4],t[1]*d.x+t[3]*d.y+t[5]],size:[cv.width,cv.height],path:XART._src.ph21_corner_warning};}''',corner)
   raw=Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB');raw.save(O/f'corner-warning-v3-native-{corner}.png')
   p.evaluate('()=>{window.savedWarning=PH21_ART.warning;PH21_ART.warning=null;paint20();PH21_ART.warning=savedWarning;}')
   absent=Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB')
   diff=ImageChops.difference(raw,absent);changed=sum(max(v)>5 for v in diff.getdata())
   ck(f'Corner {corner}: regenerated art drawn by native renderer',row['corner']==corner and row['key'] and changed>20 and 'corner_warning_v3.png' in row['path'],dict(changed=changed,**row))
   expected=[0,math.pi/2,-math.pi/2,-math.pi][corner]
   ck(f'Corner {corner}: arrow rotates toward opposite corner',abs(row['draw']['rot']-expected)<.001)
   x,y=row['screen'];w,h=row['size'];ck(f'Corner {corner}: warning stays inside playfield and clear of HUD',20<x<w-20 and h*.14<y<h*.86)
  # Review at actual enlarged display size; capture the regenerated tile.
  p.wait_for_load_state('networkidle',timeout=60000)
  navigating=True
  p.goto(f'http://127.0.0.1:{port}/_shots/boss_redesign_1020/review.html')
  tile=p.locator('figure').filter(has_text='Corner dive warning / BOF chevrons');tile.scroll_into_view_if_needed();p.wait_for_function("()=>document.querySelector('img[src*=corner_warning_v3]').naturalWidth===64");tile.screenshot(path=str(O/'corner-warning-v3-review.png'))
  p.goto(f'http://127.0.0.1:{port}/_shots/boss_redesign_1020/warning-variants-v3.html');p.wait_for_function('()=>Array.from(document.images).every(i=>i.complete&&i.naturalWidth===64)');p.set_viewport_size(dict(width=760,height=260));p.screenshot(path=str(O/'warning-variants-v3.png'))
  ck('No browser, draw or missing-asset errors',not errors,errors)
  br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),checks=len(checks),errors=errors,navigationCancels=navigationCancels,results=checks);(O/'corner-warning-v3-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True);raise SystemExit(not all(c['passed'] for c in checks))
