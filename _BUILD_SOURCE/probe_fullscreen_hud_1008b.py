"""Native fullscreen, maximum-fit geometry, fallback, sharp backing and menu cleanup."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/fullscreen_hud_1008/acceptance';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch()
   page=browser.new_page(viewport={'width':1920,'height':1080})
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
   page.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
   page.wait_for_function('window.__bofFrames>4',timeout=120000)
   page.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
   page.evaluate('BAL7.setup({stage:4,kind:debugFightFor(4,"boss").kind,pilot:"cole",diff:"normal",seconds:10});player.invuln=999999;')
   for _ in range(1200):
    if page.evaluate('()=>{stageLoadTick();return stageLoadInfo(4).ready;}'):break
    page.wait_for_timeout(30)
   else:raise RuntimeError('Stage assets not ready')
   if engine=='chromium':
    page.keyboard.press('f');page.wait_for_function('!!document.fullscreenElement');page.wait_for_timeout(300)
    check(engine+' F enters real fullscreen',page.evaluate('document.fullscreenElement.id==="room"&&document.body.classList.contains("fs")'))
    page.keyboard.press('f');page.wait_for_function('!document.fullscreenElement&&!document.body.classList.contains("fs")')
    check(engine+' F exits real fullscreen',True)
   # Exercise the real fallback handler under a rejected browser API.
   page.evaluate('()=>{document.getElementById("room").requestFullscreen=()=>Promise.reject(new Error("QA unavailable fullscreen"));}')
   page.keyboard.press('f');page.wait_for_function('document.body.classList.contains("fs")');page.wait_for_timeout(300)
   check(engine+' rejected fullscreen uses full-browser fallback',page.evaluate('!document.fullscreenElement'))
   page.evaluate(shoot.TRAP_RAF)
   for width,height in [(1920,1080),(1366,768),(2560,1440),(3440,1440),(390,844)]:
    page.set_viewport_size({'width':width,'height':height})
    page.evaluate('()=>{document.body.classList.add("fs","wide-playing");__bofFit();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);}')
    q=page.evaluate('()=>{const a=document.getElementById("game-frame").getBoundingClientRect(),b=cv.getBoundingClientRect();return{top:a.top,bottom:a.bottom,left:a.left,right:a.right,height:a.height,width:a.width,ratio:b.width/b.height,backing:[hudcv.width,hudcv.height]};}')
    check(f'{engine} {width}: largest aspect-preserving bay without clipping',q['left']>=-.1 and q['right']<=width+.1 and (abs(q['top'])<.1 and abs(q['bottom']-height)<.1 if width>=1150 else abs(q['width']-width)<.1) and abs(q['ratio']-480/512)<.005,q)
    check(f'{engine} {width}: dense backing with stable HUD geometry',q['backing']==[960,208])
    page.screenshot(path=str(OUT/f'{engine}_{width}.png'))
   page.keyboard.press('f');check(engine+' F exits CSS fallback',page.evaluate('!document.body.classList.contains("fs")'))
   page.set_viewport_size({'width':1920,'height':1080});page.evaluate('__bofFit()')
   check(engine+' browser mode also fills available height',page.evaluate('(()=>{const f=document.getElementById("game-frame");return Math.abs(f.getBoundingClientRect().height+parseFloat(getComputedStyle(f).marginBottom||0)-innerHeight)<1;})()'))   # 1009: the control-hint strip keeps its own 30px under the bottom HUD
   page.evaluate('setState(GS.TITLE)');page.evaluate(shoot.STEP,2)
   check(engine+' menu clears the full dense HUD backing',page.evaluate('()=>!Array.from(hudctx.getImageData(0,0,hudcv.width,hudcv.height).data).some(Boolean)'))
   page.evaluate('document.body.classList.add("fs");__bofFit()');page.evaluate(shoot.STEP,2)
   check(engine+' fullscreen menu retains its aspect without a hidden HUD reserve',page.evaluate('()=>{const r=cv.getBoundingClientRect();return Math.abs(r.width/r.height-480/512)<.005&&Math.abs(r.height-innerHeight)<1;}'))
   page.screenshot(path=str(OUT/f'{engine}_menu.png'))
   page.evaluate('document.body.classList.remove("fs");');page.set_viewport_size({'width':390,'height':844});page.evaluate('__bofFit()')
   check(engine+' narrow browser mode uses the full available width',page.evaluate('Math.abs(document.getElementById("game-frame").getBoundingClientRect().width-innerWidth)<1'))
   browser.close()
finally:stop()
check('zero browser or missing-asset errors',not errors,errors)
result={'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'errors':errors,'checks':checks}
(OUT/'verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'}),flush=True)
if result['failed'] or errors:sys.exit(1)
