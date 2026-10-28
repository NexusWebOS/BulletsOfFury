from pathlib import Path
import json,sys,argparse
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--url');args=ap.parse_args();W=args.out;W.mkdir(parents=True,exist_ok=True)
R=Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name=='_BUILD_SOURCE'else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF,STEP,serve
stop=None
if args.url:url=args.url
elif(W/'game-server.json').exists():url=json.loads((W/'game-server.json').read_text())['url']
else:port,stop=serve(str(R));url=f'http://127.0.0.1:{port}'
errors=[];console=[];out={}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None)
 p.goto(url+'/index.html?pixelmap=1',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.wait_for_function('typeof pm27Live!=="undefined"&&pm27Live()',timeout=90000);p.evaluate(TRAP_RAF)
 def step(n):
  e=p.evaluate(STEP,n)
  if e:errors.append(e)
 def shot(name):p.screenshot(path=str(W/(name+'.png')))
 def resize(w,h):p.set_viewport_size({'width':w,'height':h});p.evaluate('window.__bofResizeCinematic()');step(30)
 p.evaluate("()=>{setState(GS.TITLE);menuIndex=0;}");step(60);shot('title')
 p.evaluate("()=>{setState(GS.MODESEL);modeIndex=1;P2M.choice=null;}");step(30);shot('modes');out['modes']=p.evaluate('modeList().map(it=>({name:it.name,mode:it.mode,open:modeItemOpen(it)}))')
 p.evaluate("()=>{run.mode='campaign';campPick=null;campHubIndex=0;setState(GS.CAMPHUB);}");step(30);shot('campaign')
 p.evaluate("()=>{setState(GS.MODESEL);P2M.choice='coop';P2M.row=0;P2M.md=false;}");step(30);shot('coop')
 p.evaluate("()=>{P2M.choice='arcade';P2M.row=0;}");step(15);shot('arcade')
 p.evaluate("()=>{P2M.choice=null;run.mode='arcade';setState(GS.DIFF);menuIndex=2;}");step(30);shot('difficulty')
 p.evaluate("()=>{run.mode='arcade';pilotIndex=0;pilotPending=null;pilotComm=null;pcard=null;setState(GS.PILOT);}");step(300);shot('pilot')
 resize(390,844);shot('pilot-portrait');out['pilotPortrait']=p.evaluate('({card:PT11_UI.card,copy:PM27.pilotCopy})');resize(1280,800)
 p.evaluate("()=>{run.stage=1;stageLoadBegin(1);}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
 p.evaluate("()=>{pilotIndex=0;run.mode='arcade';startRun(1);beginStage(1);debugUnlocked=true;DBGT.god=true;BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);UI20.dirty=true;}");step(120);shot('hud')
 p.wait_for_function("()=>XART.rdy(commPortrait('cole','idle'))&&XART.rdy(commPortrait('juggernaut','idle'))",timeout=90000)
 p.evaluate("()=>{const s='STAY CLEAR OF THE INCOMING SHIPS! ROLL THROUGH THE FIRST WAVE. SAVE YOUR SOMERSAULT FOR THE SECOND VOLLEY.';dlgBox({who:'COLE',full:s,shown:s,portrait:'cole',y:300});}");shot('dialogue');out['dialogue']=p.evaluate('CD27.history.at(-1)');out['events']=p.evaluate('PM27.events');out['rows']=p.evaluate('PM27.rows');out['draws']=p.evaluate('PM27.draws')
 resize(390,844);shot('hud-portrait');p.evaluate("()=>{const s='WATCH YOUR SIX! TARGET THE REAR LAUNCHERS WITH MISSILES, THEN FINISH THE CORE.';dlgBox({who:'JUGGERNAUT',full:s,shown:s,portrait:'juggernaut',y:280});}");shot('dialogue-portrait')
 out['errors']=errors;out['console']=console;(W/'capture-report.json').write_text(json.dumps(out,indent=2));b.close();print(json.dumps({'errors':errors,'console':console[:6],'draws':out['draws']}))
if stop:stop()
