"""Verify Arcade's Stage-5 narrative omission and all co-op results routes."""
import base64, hashlib, json, sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'_shots/arcade_dialogue_coop_0915';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
checks=[];errors=[];shots=[]
def ok(v,name):checks.append({'name':name,'ok':bool(v)});print(('ok  'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1000})
 pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate("()=>{__auto=function(){};debugFight=null;_coleScene=0;diffKey='normal';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');window.__dlg=[];const d=dlgBox;dlgBox=function(o){__dlg.push({who:o&&o.who,full:o&&o.full});return d.apply(this,arguments);};}")
 def step(n):
  for i in range(0,n,20):pg.evaluate('n=>__step(n)',min(20,n-i));pg.wait_for_timeout(12)
 def enter():pg.keyboard.down('Enter');step(1);pg.keyboard.up('Enter');step(1)
 def shot(name):
  path=O/(name+'.png');path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")));shots.append(path)
 # Campaign and Arcade use the same transformation; only Campaign shows the HQ dispatch.
 pg.evaluate("()=>{coopOn=false;run.mode='campaign';beginStage(5);proceedIntro();__dlg=[];}");step(95);shot('campaign_stage5_dispatch')
 ok(pg.evaluate("()=>__dlg.some(x=>x.who==='FURY HQ'&&/dispatching a kit/i.test(x.full||''))"),'Campaign Stage 5 transformation retains HQ dispatch')
 pg.evaluate("()=>{coopOn=false;run.mode='arcade';beginStage(5);proceedIntro();__dlg=[];}");step(95);shot('arcade_stage5_no_dispatch')
 ok(pg.evaluate("()=>gravityMode&&gravityMode.narrative===false&&gravityMode.dialogueDone&&!__dlg.some(x=>x.who==='FURY HQ')"),'Arcade Stage 5 transformation omits HQ cutscene dialogue without waiting on it')
 ok(pg.evaluate("()=>state===GS.LAUNCH&&drawLaunch._furyIntro&&drawLaunch._furyIntro.scroll>=1500&&!run.gravityShipReady"),'Arcade keeps fast sky travel and the unfinished authored transformation')
 # Let the actual animation move from sky to its next phase; assets may decide the exact frame.
 for _ in range(75):
  if pg.evaluate("()=>drawLaunch._furyIntro&&drawLaunch._furyIntro.phase!=='sky'"):break
  step(20)
 ok(pg.evaluate("()=>drawLaunch._furyIntro&&drawLaunch._furyIntro.phase!=='sky'"),'Arcade transformation progresses beyond sky without dialogue gating')
 # Every normal co-op results route pays both seats and retains run-wide resources.
 for stage in range(1,8):
  pg.evaluate("""n=>{coopOn=true;run.mode='arcade';beginStage(n);run.score=1000+n;run2.score=2000+n;run.lives=4;run2.lives=3;run.bombs=17;run2.bombs=11;run.contUsed=2;
    stageStats={kills:2,shots:8,hits:5,livesStart:4,scoreStart:0,spawned:3,deaths:0,missiles:1,dmgDealt:100,dmgTaken:0,mslHits:1,spShots:0,spHits:0,spDmg:0,pickups:0,pickupsSeen:0,wpn:{}};
    stageStats2={kills:1,shots:6,hits:4,livesStart:3,scoreStart:0,spawned:3,deaths:0,missiles:2,dmgDealt:80,dmgTaken:0,mslHits:1,spShots:0,spHits:0,spDmg:0,pickups:0,pickupsSeen:0,wpn:{}};
    setState(GS.STAGECLEAR);drawStageClear._init=false;}""",stage)
  step(20);enter();step(2)
  expected=pg.evaluate("()=>({a:run.score+drawStageClear._res.bonus,b:run2.score+drawStageClear._res.seats[1].bonus})")
  enter()
  ok(pg.evaluate("a=>run.stage===a[0]&&state===GS.INTRO&&run.score===a[1]&&run2.score===a[2]&&run.lives===4&&run2.lives===3&&run.bombs===17&&run2.bombs===11&&run.contUsed===2",[stage+1,expected['a'],expected['b']]),'co-op Stage %d results pay both seats and advance to Stage %d'%(stage,stage+1))
 # Stage 8 pays both seats then uses the Arcade final card.
 pg.evaluate("()=>{coopOn=true;run.mode='arcade';beginStage(8);run.score=8100;run2.score=8200;setState(GS.STAGECLEAR);drawStageClear._init=false;}");step(20);enter();step(2)
 final_expected=pg.evaluate("()=>({a:run.score+drawStageClear._res.bonus,b:run2.score+drawStageClear._res.seats[1].bonus})");enter();step(10);shot('coop_arcade_final')
 ok(pg.evaluate("a=>state===GS.VICTORY&&drawVictory._ready&&run.score===a.a&&run2.score===a.b",final_expected),'co-op Stage 8 pays both seats and reaches the Arcade final card')
 # Direct co-op bonus results have no map or campaign fallback.
 pg.evaluate("()=>{coopOn=true;run.mode='arcade';beginStage(9);run.score=9100;run2.score=9200;setState(GS.STAGECLEAR);drawStageClear._init=false;}");step(20);enter();step(2)
 bonus_expected=pg.evaluate("()=>({a:run.score+drawStageClear._res.bonus,b:run2.score+drawStageClear._res.seats[1].bonus})");enter()
 ok(pg.evaluate("a=>run.stage===6&&state===GS.INTRO&&run.score===a.a&&run2.score===a.b",bonus_expected),'direct co-op bonus results pay both seats and continue to Stage 6 without the campaign map')
 loop_error=pg.evaluate('()=>window.__err||null');ok(not errors and not loop_error,'zero page, console and controlled-loop errors');b.close()
stop()
board=Image.new('RGB',(960,570),'#10131c');d=ImageDraw.Draw(board)
for i,path in enumerate(shots):
 im=Image.open(path).convert('RGB');im.thumbnail((320,540));board.paste(im,(i*320,25));d.text((i*320+6,5),path.stem,fill='white')
board.save(O/'contact.png')
result={'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'checks':checks,'errors':errors,'loopError':loop_error,'screenshots':[str(s)for s in shots]}
(O/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
n=sum(c['ok']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)
