"""Pinned code coverage, real menu ownership, keyboard/pad entry and native pixels."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/password_catalog_1005';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R));report={'checks':[],'errors':[]}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def draw(p):p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawPassword(1/60);}')
def pointer(p,x,y):
 rect=p.locator(p.evaluate('()=>"#"+cv.id')).bounding_box()
 p.mouse.move(rect['x']+x/480*rect['width'],rect['y']+y/512*rect['height']);p.mouse.down();draw(p);p.mouse.up();draw(p)
def shot(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};setState(GS.PASSWORD);pwInput="";drawPassword.typing=false;Input.clearTaps();uiFontWarm();pilotFont(2);}')
  p.wait_for_function('()=>{const a=pilotFont(2);return !!(a&&stageGlyph(a,"A"));}',timeout=120000,polling=50)
  draw(p);shot(p,'password-entry')
  ck(p.evaluate('()=>pwHotspots(16,42,VW-32,VH-94).some(h=>h.c==="__PC5__"&&h.y+h.h<312)'),'permanent catalog button occupies free space above keypad')
  # The actual mouse location uses the existing canvas transform/event handler.
  selector=p.evaluate('()=>"#"+cv.id');rect=p.locator(selector).bounding_box()
  p.mouse.move(rect['x']+240/480*rect['width'],rect['y']+202/512*rect['height']);p.mouse.down();draw(p);p.mouse.up();draw(p)
  report['mouse']=p.evaluate('()=>({x:Input.mouse.x,y:Input.mouse.y,open:PC5.open,canvas:cv.id})')
  ck(p.evaluate('()=>PC5.open&&state===GS.PASSWORD'),'mouse opens pinned catalog from existing password menu');shot(p,'catalog-open')
  pointer(p,425,58);ck(p.evaluate('()=>PC5.page===1&&PC5.open'),'mouse Next changes catalog page')
  pointer(p,355,117);ck(p.evaluate('()=>!PC5.open&&pwInput==="HARR6"&&state===GS.PASSWORD'),'mouse row fills code without submission')
  p.evaluate('()=>{drawPassword.sel=pwHotspots(16,42,VW-32,VH-94).findIndex(h=>h.c==="__PC5__");Input.injectTap("pad_b0");}');draw(p)
  ck(p.evaluate('()=>PC5.open'),'D-pad selected catalog button opens with pad A')
  p.evaluate('()=>{pc5Close();pwInput="";Input.injectTap((keybind.retina||[]).find(k=>/^pad_/.test(k)));}');draw(p)
  ck(p.evaluate('()=>PC5.open'),'bound pad Retina shortcut opens catalog without typing a letter')
  groups=p.evaluate('()=>pc5Pages()');report['pages']=groups
  expected=p.evaluate('()=>[...new Set([...Object.keys(PASSWORDS),...Object.keys(COLE_SCENE),"HAMMER","HAMA","COLE4U","BOMBER","SPCBOY"])]')
  codes=[r[0] for g in groups for r in g['rows']]
  ck(sorted(codes)==sorted(expected) and len(codes)==len(set(codes)),'every current/new stage, fight, scene and unlock code appears exactly once')
  ck(all(len(c)<=6 for c in codes),'all listed codes fit native six-character input')
  for i,g in enumerate(groups):
   p.evaluate('(i)=>{PC5.open=true;PC5.page=i;PC5.row=0;Input.clearTaps();}',i);draw(p);shot(p,'page-'+str(i))
   ck(p.evaluate('()=>PC5.rendered.every(r=>r.x>=24&&r.x+r.w<=VW-24&&r.h>=11&&r.y-r.h/2>=12&&r.y+r.h/2<VH-40)'),g['title']+' renders readable text inside panel')
  # Keyboard arrows / physical-pad semantics share the existing Input owner.
  p.evaluate('()=>{PC5.page=0;PC5.row=0;}');p.keyboard.press('ArrowRight');draw(p)
  ck(p.evaluate('()=>PC5.page===1&&pwInput===""'),'arrow right pages without typing into entry')
  p.evaluate('()=>Input.injectTap("pad_b0")');draw(p)
  ck(p.evaluate('()=>!PC5.open&&pwInput==="HARR6"&&state===GS.PASSWORD&&!ON5.pending'),'pad A fills selected code without launching or granting anything')
  p.evaluate('()=>{pc5Open();}');p.keyboard.press('k');p.evaluate('()=>menuBackTick()');draw(p)
  ck(p.evaluate('()=>!PC5.open&&state===GS.PASSWORD&&pwInput==="HARR6"'),'logical Back closes catalog to entry and preserves typed password')
  p.evaluate('()=>{pc5Open();}');p.keyboard.press('Backspace');draw(p)
  ck(p.evaluate('()=>PC5.open&&state===GS.PASSWORD'),'Backspace never exits catalog')
  p.evaluate('()=>{pc5Close();pwInput="";}');p.keyboard.type('CRYO8',delay=12);draw(p)
  ck(p.evaluate('()=>pwInput==="CRYO8"&&!PC5.open'),'typing C remains ordinary password text')
  p.keyboard.press('Backspace');draw(p);ck(p.evaluate('()=>pwInput==="CRYO"&&state===GS.PASSWORD'),'Backspace deletes entry text')
  p.evaluate('()=>{pwInput="";drawPassword.typing=true;_pwTyped=[];Input.clearTaps();}')
  p.keyboard.type('KNIGHT',delay=12);draw(p)
  ck(p.evaluate('()=>pwInput==="KNIGHT"&&drawPassword.typing&&state===GS.PASSWORD'),'explicit typing mode inserts each raw letter exactly once')
  p.keyboard.press('Backspace');draw(p)
  ck(p.evaluate('()=>pwInput==="KNIGH"'),'explicit typing mode deletes exactly one letter')
  p.evaluate('()=>drawPassword.typing=false')
  # Every row goes through the same real pad-A selection path, never submission.
  for pi,g in enumerate(groups):
   for ri,(code,label) in enumerate(g['rows']):
    p.evaluate('([pi,ri])=>{PC5.open=true;PC5.page=pi;PC5.row=ri;_pwTyped=[];Input.clearTaps();Input.injectTap("pad_b0");}',[pi,ri]);draw(p)
    ck(p.evaluate('(c)=>pwInput===c&&!PC5.open&&state===GS.PASSWORD&&!ON5.pending',code),code+' selection fills entry without automatic action')
  p.evaluate('()=>{pc5Open();PC5.page=5;PC5.row=1;Input.injectTap("pad_b0");}');draw(p)
  p.keyboard.press('Enter');draw(p)
  ck(p.evaluate('()=>state===GS.DIFF&&ON5.pending?.phase===1'),'picked FINAL2 submits through unchanged difficulty/pilot route')
  ck(p.evaluate('()=>!PC5.open'),'leaving password menu clears catalog state')
  p.goto(f'http://127.0.0.1:{port}/_shots/password_catalog_1005/review.html',timeout=120000)
  frame=p.frames[1];frame.wait_for_function('()=>typeof PC5!=="undefined"&&PC5.open&&state===GS.PASSWORD',timeout=120000)
  ck(frame.evaluate('()=>pc5Pages().flatMap(p=>p.rows).length===59'),'playable review opens the actual pinned list')
  ck(frame.evaluate('()=>{localStorage.setItem("pc5-practice-proof","x");return localStorage.getItem("pc5-practice-proof")===null;}'),'playable review blocks campaign save writes')
  ck(not report['errors'],'zero page and console errors');b.close()
finally:stop();(O/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if all(q['ok'] for q in report['checks']) and not report['errors'] else 1)
