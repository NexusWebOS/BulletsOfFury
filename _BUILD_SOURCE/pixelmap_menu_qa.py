from pathlib import Path
import json,sys,argparse
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--url');args=ap.parse_args();W=args.out;W.mkdir(parents=True,exist_ok=True)
R=Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name=='_BUILD_SOURCE'else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF,STEP,serve
stop=None
if args.url:url=args.url
elif(W/'game-server.json').exists():url=json.loads((W/'game-server.json').read_text())['url']
else:port,stop=serve(str(R));url=f'http://127.0.0.1:{port}'
errors=[];checks=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(url+'/index.html?pixelmap=1',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.wait_for_function('typeof pm27Live!=="undefined"&&pm27Live()',timeout=90000);p.evaluate(TRAP_RAF)
 def step(n=45):
  e=p.evaluate(STEP,n)
  if e:errors.append(e)
 def check(name,test):
  ok=p.evaluate(test);checks.append({'name':name,'pass':bool(ok),'value':ok});print(('PASS 'if ok else'FAIL ')+name,flush=True)
 def key(k,n=36):p.keyboard.down(k);step(1);p.keyboard.up(k);step(n)
 def setup(code):p.evaluate('()=>{Input.clearTaps?.();Input.mouse.down=false;_selFlash=null;diffPending=null;titlePending=null;P2M.choice=null;SM22.open=false;'+code+'}');step()
 def clickrow(group,index):
  q=p.evaluate('(a)=>PM27.rows[a[0]][a[1]]',[group,index]);box=p.locator('#screen').bounding_box();x=box['x']+q['cx']*box['width']/480;y=box['y']+q['cy']*box['height']/512
  p.mouse.move(x,y);step(1);p.mouse.down();step(1);p.mouse.up();step(45)
 setup('menuIndex=0;setState(GS.TITLE);')
 key('ArrowUp');check('Title wraps upward to Exit', 'menuIndex===TITLE_ITEMS.length-1')
 key('ArrowDown');check('Title wraps back to New Game','menuIndex===0')
 key('j');check('New Game opens mode selection through native confirmation','state===GS.MODESEL')
 setup('modeIndex=0;setState(GS.MODESEL);')
 key('j');check('Campaign opens campaign hub','state===GS.CAMPHUB&&run.mode==="campaign"')
 key('j');check('Campaign New Game opens difficulty','state===GS.DIFF')
 p.evaluate('window._pm27PriorDifficulty=menuIndex');key('ArrowDown');check('Difficulty moves exactly one row','menuIndex===(_pm27PriorDifficulty+1)%diffList().length')
 key('j');check('Difficulty confirmation opens pilot selection','state===GS.PILOT')
 setup('modeIndex=1;setState(GS.MODESEL);')
 key('j');check('Arcade opens difficulty without inventing an NG+ unlock','state===GS.DIFF&&!run.ngplus&&!coopOn')
 setup('modeIndex=2;setState(GS.MODESEL);')
 key('j');check('Co-op opens Local / Online text choices','P2M.choice==="coop"&&state===GS.MODESEL')
 key('ArrowDown');check('Co-op choice moves to Online','P2M.row===1')
 key('ArrowUp');key('j');check('Local Co-op preserves second-player setup','state===GS.DIFF&&coopOn&&run.mode==="arcade"')
 setup('modeIndex=1;setState(GS.MODESEL);')
 key('j');check('Returning to solo clears co-op flag','state===GS.DIFF&&!coopOn')
 setup('modeIndex=3;setState(GS.MODESEL);')
 key('j');check('Boss Rush remains locked without campaign completion','state===GS.MODESEL&&!P2M.active&&!P2M.choice')
 setup('modeIndex=2;setState(GS.MODESEL);')
 key('j');key('k');check('B cancels Co-op submenu','state===GS.MODESEL&&P2M.choice===null')
 setup('modeIndex=0;setState(GS.MODESEL);')
 clickrow('mode',1);check('Mouse activates Arcade text row','state===GS.DIFF')
 clickrow('diff',3);check('Mouse selects Furious and opens pilot selection','state===GS.PILOT&&diffKey==="furious"')
 # Full roster copy and fixed dialogue layout, using actual render owners.
 roster=p.evaluate('()=>{const out=[];for(const P of PILOTS){pcard={done:true};pilotPending=null;ctx.save();pt11PilotCard(P,0,58,800,266,0,false);ctx.restore();out.push({...PM27.pilotCopy});}return out;}')
 checks.append({'name':'All pilot biographies fit above stats','pass':all(q['used']<=q['available']for q in roster),'value':roster})
 metrics=p.evaluate("()=>{const out=[];for(const s of ['COLE','MAVERICK','JUGGERNAUT','DRACODIA','CHRONOS']){PM27.names=s;ui20Text(ctx,s,100,100,10,68,'center','#fff');out.push(PM27.events.at(-1));}PM27.names=null;return out;}")
 # Explicit measurement: no stale bounded event-buffer assumptions.
 check('Long dialogue names fit the 68px name plate', "['COLE','MAVERICK','JUGGERNAUT','DRACODIA','CHRONOS'].every(s=>{const f=pm27Width(s,8,'fury_strike')<=68?'fury_strike':'command_narrow',a=pm27Fit(s,10,68,f);return pm27Width(s,a.height,a.family)+a.cw-a.glyphs[77].advance<=68})")
 p.goto(url+'/index.html?classicfont=1',wait_until='load',timeout=180000);p.wait_for_function('typeof PM27!=="undefined"');check('Original typography remains available for comparison','!PM27.enabled&&!PM27.concept')
 p.goto(url+'/index.html',wait_until='load',timeout=180000);p.wait_for_function('typeof PM27!=="undefined"');check('New typography default keeps graphic menus until concept selected','PM27.enabled&&!PM27.concept')
 b.close()
(W/'menu-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2));print(json.dumps({'passed':sum(q['pass']for q in checks),'checks':len(checks),'errors':errors}))
if stop:stop()
