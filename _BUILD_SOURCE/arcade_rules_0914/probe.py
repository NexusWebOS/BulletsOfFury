"""Arcade difficulty and continue flow through the real game and keyboard."""
import base64,json,sys,threading,http.server
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'_shots/arcade_rules_0914';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps,ImageDraw
checks=[];errors=[];shots=[];details={}
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate("()=>{__auto=function(){};window.__labels=[];const f=stageText;stageText=function(a,t){__labels.push(String(t));return f.apply(this,arguments);};window.__blits=0;const d=ctx.drawImage;ctx.drawImage=function(){__blits++;return d.apply(this,arguments);};}")
 def step(n):
  for i in range(0,n,30):pg.evaluate('n=>__step(n)',min(30,n-i));pg.wait_for_timeout(12)
 def shot(name):
  path=O/(name+'.png');path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")));shots.append(path)
 def enter():
  pg.keyboard.down('Enter');step(1);pg.keyboard.up('Enter');step(1)
 for i,(key,lives,credits) in enumerate([('easy',7,7),('normal',5,5),('hard',3,3),('furious',3,1)]):
  pg.evaluate("a=>{run.mode='arcade';diffKey=a[0];menuIndex=a[1];diffPending=null;diffFlash=0;setState(GS.DIFF);menuIndex=a[1];__labels=[];}",[key,i]);step(2)
  for _ in range(100):
   if pg.evaluate('()=>artReady(pilotFont(1))'):break
   pg.wait_for_timeout(50);step(1)
  step(3);shot('difficulty_'+key)
  ok(pg.evaluate('a=>__labels.includes(a[0]+" LIVES")&&__labels.includes(a[1]+(a[1]===1?" CONTINUE":" CONTINUES"))',[lives,credits]),key+' authored difficulty screen draws the actual lives and credits')
  pg.evaluate("()=>{pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');startRun(1);__auto=function(){};}");step(4)
  ok(pg.evaluate('a=>run.lives===a[0]&&DIFF.continues===a[1]&&run.contUsed===0',[lives,credits]),key+' native startRun initializes the correct stock')
  if key=='normal':
   for _ in range(80):
    if pg.evaluate('()=>state===GS.PLAY'):break
    step(30)
   step(4)
   ok(pg.evaluate('()=>state===GS.PLAY&&run.lives===5'),'Normal reaches actual gameplay with five starting lives')
   path=O/'normal_start_hud.png';pg.locator('#game-frame').screenshot(path=str(path));shots.append(path)
  pg.evaluate('n=>{run.contUsed=n-1;run.lives=0;player.dead=true;setState(GS.CONTINUE);}',credits);step(32);shot('continue_'+key)
  enter()
  ok(pg.evaluate('a=>state===GS.PLAY&&run.lives===a[0]&&run.contUsed===a[1]&&!player.dead',[lives,credits]),key+' real Enter spends the final credit and restores the selected stock')
  pg.evaluate("()=>{run.lives=0;player.dead=true;setState(GS.CONTINUE);}");step(32)
  if key=='normal':shot('no_credits_remaining')
  enter()
  ok(pg.evaluate('n=>state===GS.GAMEOVER&&run.contUsed===n&&run.lives===0',credits),key+' another real Enter cannot exceed its credit bank')
 pg.evaluate("()=>{run.mode='campaign';diffKey='hard';startRun(3);__auto=function(){};}");step(2)
 ok(pg.evaluate("()=>run.mode==='arcade'&&DIFF.startLives===3&&DIFF.continues===3"),'password/direct stage entry resolves Arcade mode before assigning difficulty')
 # Verify a returning campaign save cannot inherit the preceding Arcade configuration.
 pg.evaluate("()=>{run.mode='arcade';diffKey='furious';DIFF=difficultyForRun(run.mode,diffKey);const snap=campSnapshot();snap.diff='normal';snap.lives=2;campApply(snap);}")
 ok(pg.evaluate("()=>run.mode==='campaign'&&DIFF===DIFFS.normal&&DIFF.continues===-1&&run.lives===2"),'campaign load restores its own difficulty without overwriting saved lives')
 pg.evaluate("()=>{run.mode='arcade';diffKey='normal';startRun(9);__auto=function(){};run.contUsed=3;run.lives=0;player.dead=true;setState(GS.CONTINUE);}");step(32);enter()
 ok(pg.evaluate("()=>state===GS.PLAY&&run.contUsed===4&&run.lives===5"),'Stage 9 retains the same Arcade bank and can spend its fourth credit')
 pg.evaluate("()=>{run.contUsed=5;run.lives=0;player.dead=true;setState(GS.CONTINUE);}");step(32);enter();step(12);shot('stage9_arcade_gameover')
 ok(pg.evaluate("()=>state===GS.GAMEOVER&&run.contUsed===5&&run.lives===0&&!_riftFallback"),'exhausted Stage-9 Arcade ends without campaign map or a refunded bank')
 details['labels']=pg.evaluate('()=>Array.from(new Set(__labels))');details['blits']=pg.evaluate('()=>__blits');details['loopError']=pg.evaluate('()=>window.__err||null')
 ok(details['blits']>0 and not errors and not details['loopError'],'native canvas renders with zero page, console and controlled-loop errors')
 b.close()
srv.shutdown()
(O/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'screenshots':[str(s)for s in shots]},indent=2),encoding='utf-8')
chosen=[O/('difficulty_'+k+'.png') for k in ['easy','normal','hard','furious']]+[O/'continue_normal.png',O/'no_credits_remaining.png']
board=Image.new('RGB',(960,1056),'#12151c');d=ImageDraw.Draw(board)
for i,path in enumerate(chosen):
 im=Image.open(path).convert('RGB');im.thumbnail((320,510));x=(i%3)*320;y=(i//3)*528;board.paste(im,(x,y+18));d.text((x+8,y+2),path.stem,fill='white')
board.save(O/'contact.png')
n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)

