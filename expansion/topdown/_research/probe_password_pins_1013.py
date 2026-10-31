from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_password_pins_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':1000})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.add_init_script("window.testPad={id:'Password pin QA',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0')
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('TD.FRONT_WARM.every(k=>!!ART.get(k))',timeout=60000)
  def frames(n=20):page.evaluate('n=>TDGAME.step(n)',n)
  def tap(k):page.keyboard.down(k);frames(1);page.keyboard.up(k);frames()
  def go():page.evaluate("TD.Frontend.pending=null;TD.Frontend.returnTo='title';TD.Frontend.go('password')");frames()
  def click(kind,i=None):
   q=page.evaluate("([kind,i])=>TD.Frontend.rects.find(r=>r.kind===kind&&(i===null||r.i===i))",[kind,i])
   b=page.locator('#screen').bounding_box();v=page.evaluate('TD.Display');page.mouse.move(b['x']+(q['x']+q['w']/2)*b['width']/v['w'],b['y']+(q['y']+q['h']/2)*b['height']/v['h']);page.mouse.down();frames(1);page.mouse.up();frames()
  def pad(i):page.evaluate('i=>{testPad.buttons[i].pressed=true;testPad.buttons[i].value=1}',i);frames(1);page.evaluate('i=>{testPad.buttons[i].pressed=false;testPad.buttons[i].value=0}',i);frames()
  frames();tap('Enter');tap('Enter');tap('ArrowDown');tap('Enter')
  check('title Password opens the pinned menu through actual inputs',page.evaluate('TDGAME.G.state==="password"&&TD.Frontend.pwSel===0'))
  pins=page.evaluate('TD.Frontend.pinnedPasswords()');print(json.dumps(pins),flush=True)
  check('all five playable levels have visible pins and valid Yuri Normal Hotwire passwords',page.evaluate("TD.Frontend.pinnedPasswords().map(p=>p.id).join(',')==='2,3,4,5,6'&&TD.Frontend.pinnedPasswords().every(p=>{const d=TD.Password.decode(p.code);return d.sel===p.sel&&d.pilot==='yuri'&&d.difficulty==='normal'&&d.companion==='hotwire';})"))
  page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/'password_menu.png'))
  check('pin buttons and manual keypad all fit within the screen without overlapping',page.evaluate("(()=>{const r=TD.Frontend.rects;return r.length===45&&r.every(a=>a.x>=0&&a.y>=0&&a.x+a.w<=640&&a.y+a.h<475)&&r.every((a,i)=>r.slice(i+1).every(b=>a.x+a.w<=b.x||b.x+b.w<=a.x||a.y+a.h<=b.y||b.y+b.h<=a.y));})()"))
  for i,p in enumerate(pins):
   go();click('pin',i);check(f'clicking Level {p["id"]} loads its password and pilot screen',page.evaluate("sel=>TDGAME.G.state==='pilot'&&TDGAME.G.sel===sel&&TD.pilot==='yuri'&&TD.difficulty==='normal'&&TD.companion==='hotwire'",p['sel']))
   tap('Enter');check(f'confirming Level {p["id"]} reaches the matching briefing',page.evaluate("id=>TDGAME.G.state==='brief'&&TDGAME.G.mission===id",p['id']))
  go();pad(12);check('controller up wraps from first pin to last',page.evaluate('TD.Frontend.pwSel===4'))
  pad(13);check('controller down wraps back to first pin',page.evaluate('TD.Frontend.pwSel===0'))
  pad(15);check('controller right enters the manual keypad',page.evaluate('TD.Frontend.pwSel===5'))
  pad(0);check('controller A can still enter a manual character',page.evaluate("TD.Frontend.pw==='OD-A'"))
  pad(14);pad(13);pad(0);check('controller A selects the fortress pin',page.evaluate('TDGAME.G.state==="pilot"&&TDGAME.G.sel===1'))
  go();click('key',44);frames(1);check('TYPE still opens manual keyboard entry',page.evaluate('TD.Frontend.typing&&!!TD.Input.textSink'))
  page.keyboard.type('237E-5JXQ');frames(1);tap('Backspace');check('Backspace deletes a typed character without leaving the menu',page.evaluate("TD.Frontend.pw==='OD-237E-5JX'&&TDGAME.G.state==='password'"))
  page.keyboard.type('Q');frames(1);click('load');check('manual typed password loads Night Run',page.evaluate('TDGAME.G.state==="pilot"&&TDGAME.G.sel===4'))
  go();page.evaluate("TD.Frontend.pw='OD-2222-2222'");click('load');check('invalid manual passwords retain their error feedback',page.evaluate('TDGAME.G.state==="password"&&TD.Frontend.message.includes("INVALID")'))
  page.evaluate("TD.Frontend.pw=TD.Password.encode(1,'yuri','insanity','hotwire')");click('load');check('Insanity manual codes retain the existing unlock gate',page.evaluate('TDGAME.G.state==="password"&&TD.Frontend.message.includes("UNLOCK INSANITY")'))
  go();tap('b');check('B returns from pinned passwords to title',page.evaluate('TDGAME.G.state==="title"'))
  go();page.set_viewport_size({'width':520,'height':650});frames();page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/'password_menu_narrow.png'))
  check('password pins fit a narrow browser pane',page.evaluate('(()=>{const r=document.getElementById("screen").getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1;})()'))
  check('no page console or missing-asset errors',not errors)
  (OUT/'report.json').write_text(json.dumps({'pins':pins,'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8');browser.close()
finally:stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed');sys.exit(0 if all(c['passed'] for c in checks) else 1)
