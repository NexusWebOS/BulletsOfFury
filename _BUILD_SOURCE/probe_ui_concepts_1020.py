from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,ast,json,base64,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=Path(__file__).parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/ui_concepts_1020';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print(('PASS ' if v else 'FAIL ')+n,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000);p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/ui_concepts_1020/index.html');p.wait_for_function('preview.complete&&preview.naturalWidth>0')
  for tab in ['dialogue','hud']:
   p.locator(f'[data-tab="{tab}"]').click()
   for v in 'abc':
    p.locator(f'[data-variant="{v}"]').click();p.wait_for_function('preview.complete&&preview.naturalWidth>0');ck(tab+' '+v+' opens correct complete generated image',p.evaluate('preview.src.endsWith("'+tab+'-'+v+'.png")'))
   p.locator('[data-variant="b"]').click();p.locator('#choose').click()
  ck('Dialogue and HUD selections remain independent',p.evaluate("choices.dialogue==='b'&&choices.hud==='b'"))
  p.locator('[data-tab="portrait"]').click();p.wait_for_function('preview.complete&&preview.naturalWidth>0');ck('New Dracodia portrait is square and fully available',p.evaluate('preview.naturalWidth===preview.naturalHeight&&preview.naturalWidth>500'))
  p.set_viewport_size(dict(width=390,height=844));p.screenshot(path=str(O/'review-narrow.png'));ck('Narrow gallery has no horizontal page overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  p.set_viewport_size(dict(width=1440,height=1000));p.locator('[data-tab="hud"]').click();p.screenshot(path=str(O/'review-desktop.png'))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'normal'})
  p.wait_for_function('()=>{stageLoadTick();dr5Warm();return stageLoadReady(8)&&v18Warm()&&XART.rdy(DP20.key);}',polling=75)
  p.evaluate("()=>{window.B=boss;v18Budget(B);v18Enter(B,2,0);v18Fight(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;stagePlan=[];spawnClock=999999;enemies=[];eBullets=[];pBullets=[];B.x=worldWidth()/2;B.y=PLAY.y+168;B._r30.mode='dr5Monologue';B._r30.t=2;B._r30.clock=2;B.enter=B._noHit=true;dr5Say(B,'DRACODIA',DR5.intro[0][0],3);dr5State(B).radio.t=1;}")
  ck('All existing portrait aliases resolve to the dedicated illustration',p.evaluate("()=>{const im=XART.get(DP20.key);return Array.from({length:9},(_,f)=>[0,1,2].every(t=>dr5Portrait(f,t)===im)).every(Boolean);}"))
  p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}");(O/'dracodia-dialogue-native.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('Native dialogue requests the dedicated portrait',p.evaluate('DP20.draws>0'))
  p.evaluate("()=>{const im=dr5Portrait(3,1);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,0,0,512,512);}");(O/'dracodia-portrait-native.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('New portrait remains complete with even square dimensions',p.evaluate('()=>{const im=dr5Portrait(3,1);return im.width===im.height&&im.width%2===0&&im.naturalWidth>0;}'))
  ck('All requested HUD concepts remain outside gameplay runtime',p.evaluate("!Object.values(XART._src).some(s=>/ui_concepts_1020.*hud-/.test(s))"))
  ck('No browser/asset errors',not errors,errors);b.close()
finally:stop()
report={'passed':sum(q['passed'] for q in checks),'checks':len(checks),'errors':errors,'results':checks};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(q['passed'] for q in checks))
