from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,base64,json,http.server
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_finish_1020';checks=[];errors=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=720));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(100,100)
  p.evaluate("()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==='yuri');run2.pilot='yuri';run.score=123456;run2.score=654321;setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._sfx={};drawVictory._t=0;Input.clearTaps();Input.mouse.down=false;victoryEndingWarm();}")
  p.wait_for_function('ce20Warm()&&hl10Warm()&&hl10Warm("yuri")',polling=75)
  p.evaluate("()=>{window.seekC20=t=>{drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);return{partner:CE20.partnerShip,actor:CE20.partnerActor,last:CE20.last};};}")
  def shot(name): (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  for t,name in [(1.5,'coop-portal'),(11.5,'coop-landing'),(15.7,'coop-exit'),(22.5,'coop-walk'),(65,'coop-final-card')]:
   row=p.evaluate('seekC20',t);shot(name)
   if t<26:ck(name+' uses P2 actual aircraft',row['partner']['key']=='ship_yuri_so'+('6' if t<3 else '2'),row)
   if t in [15.7,22.5]:ck(name+' P2 physically disembarks/walks with its own frames',bool(row['actor']),row)
   if t==65:ck('Co-op final score combines both actual player scores',row['last']['total']==777777,row)
  # Native A/Start logic, using keyboard events rather than replacing input APIs.
  p.evaluate("()=>{coopOn=false;window.doneC20=0;window.scoreBeforeC20=run.score;BOFCinematicDirector.play('ce20-input',[{who:'COLE',text:'The signal is gone. We are bringing everyone home.'},{who:'DECKER',text:'Manual control restored.'}],()=>doneC20++);BOFCinematicDirector.tick(.2);}")
  fire=p.evaluate("keybind.fire.find(k=>!k.startsWith('mouse'))||'z'");start=p.evaluate("keybind.start?.find(k=>!k.startsWith('mouse'))||'enter'");keymap={' ':'Space','enter':'Enter'}
  p.keyboard.press(keymap.get(fire,fire));p.evaluate('BOFCinematicDirector.tick(.01)');ck('Real confirm reveals current dialogue before advancing',p.evaluate('BOFCinematicDirector.current.i===0&&BOFCinematicDirector.current.shown===BOFCinematicDirector.current.beats[0].text.length&&doneC20===0'))
  p.keyboard.press(keymap.get(start,start));p.evaluate('BOFCinematicDirector.tick(.01)');ck('Real Start skips the scene with one native callback and no reward changes',p.evaluate('!BOFCinematicDirector.active&&doneC20===1&&run.score===scoreBeforeC20'))
  p.evaluate("()=>{setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._t=65;drawVictory._md=false;Input.mouse.down=false;Input.clearTaps();}")
  p.keyboard.press(keymap.get(start,start));p.evaluate('drawVictory(.01)');ck('Real Start leaves final card for the title',p.evaluate('state===GS.TITLE'))
  # Exercise the actual Stage8 monologue/death/portal/reunion reward chain.
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}',polling=75)
  p.evaluate("()=>{window.B=boss;v18Budget(B);v18Enter(B,2,0);v18Fight(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;stagePlan=[];spawnClock=999999;enemies=[];eBullets=[];pBullets=[];B.x=worldWidth()/2;B.y=PLAY.y+168;B._r30.mode='dr5Monologue';B._r30.t=2;B._r30.clock=2;B.enter=B._noHit=true;dr5Say(B,'DRACODIA',DR5.intro[0][0],3);dr5State(B).radio.t=1;}")
  p.evaluate("()=>{dr5State(B).radio.t=2;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}");shot('dracodia-monologue')
  p.evaluate("()=>{const im=dr5Portrait(3,1);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,0,0);}");shot('dracodia-native-portrait')
  p.evaluate("()=>{dr5State(B).radio.face=5;dr5State(B).radio.t=1;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}");shot('dracodia-native-roar')
  ck('Dracodia monologue uses actual combat core, both limbs and native roar acting',p.evaluate("Object.keys(CE20.draws).some(k=>k.startsWith('v18_colossus_core_'))&&Object.keys(CE20.draws).some(k=>k.startsWith('v18_colossus_left_'))&&Object.keys(CE20.draws).some(k=>k.startsWith('v18_colossus_right_'))&&CE20.draws[v19ClipFrame('colossus_roar',1,2.5).layers.core.key]>0"))
  ck('Dracodia head portrait comes from the native combat model',p.evaluate('CE20.portraits.size>0'))
  ck('New monologue explains a demonic will occupying machinery',p.evaluate("DR5.intro.some(q=>q[0].includes('will without a body'))&&DR5.intro.some(q=>q[0].includes('inside your code'))"))
  p.evaluate("()=>{B._r30.t=1;dr5State(B).line=0;dr5State(B).radio.t=.1;window.speechHP20=B.hp;window.speechScore20=run.score;Input.clearTaps();}")
  p.keyboard.press(keymap.get(fire,fire));p.evaluate('r30Tick(B,.01)');ck('Real confirm reveals Dracodia speech without skipping the line',p.evaluate('dr5State(B).line===0&&dr5State(B).radio.t>=dr5State(B).radio.text.length/34'))
  p.keyboard.press(keymap.get(start,start));p.evaluate('r30Tick(B,.01)');ck('Real Start skips Dracodia speech through its native combat handoff',p.evaluate("B._r30.mode==='fight'&&dr5State(B).introSeen&&!B._noHit&&B.hp===speechHP20&&run.score===speechScore20"))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate("diff=>{diffKey=diff;DIFF=DIFFS[diff];B._r30.mode='fight';B._r30.v18.form=0;dr5State(B).deathStarted=false;dr5State(B).bodyGone=false;j3FinalDeath(B);}",diff)
   ck(diff+' final death starts protected with no rewards yet',p.evaluate("B._r30.mode==='dr5Death'&&dr5Locked()&&!run._trueFinaleCleared"))
   if diff=='normal':
    err=p.evaluate(shoot.STEP,620);ck('Complete native engine advances the final death without update errors',err is None,err)
   else:p.evaluate('()=>{for(let i=0;i<620;i++)r30Tick(B,1/60);}')
   ck(diff+' native defeat enters the escape portal',p.evaluate("B._r30.mode==='dr5Portal'"),p.evaluate('B._r30.mode'))
   if diff=='normal':
    p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}");shot('dracodia-defeat-portal')
    ck('Final armor debris expires before the escape portal, without restoring the boss',p.evaluate('dr5State(B).bodyGone&&(B._r30.v18.shards||[]).every(q=>!D27_MODULE_DEBRIS.includes(q))'))
   # The original reunion is tested on the final difficulty once; it owns the reward.
  p.evaluate('()=>{for(let i=0;i<900&&state===GS.PLAY;i++)r30Tick(B,1/60);}')
  ck('Original reunion sets true-ending flag and reaches stage clear',p.evaluate('run._trueFinaleCleared&&state===GS.STAGECLEAR&&B._r30.rewarded'))
  score=p.evaluate('run.score');p.evaluate('()=>{for(let i=0;i<20;i++)r30Tick(B,1/60);}')
  ck('Reunion rewards cannot pay twice',p.evaluate('run.score')==score)
  # triggerVictory keeps its native unlock/high-score path; suppress network posting in fixture.
  p.evaluate("()=>{if(window.BOFOnline)window.BOFOnline.submitScore=()=>{};triggerVictory();}")
  ck('Native victory entry inherits the earned complete-ending branch',p.evaluate('state===GS.VICTORY&&drawVictory._trueEnding&&drawVictory._t===0'))
  for cue in ['blip','select','crackle']:
   row=p.evaluate("""async key=>{Audio.resume();await Snd._audioCtx().resume();Snd.prepare(key);await new Promise(r=>setTimeout(r,300));Snd.stopCue(key);Snd._last[key]=0;if(typeof AV3!=='undefined')AV3.last.clear();Snd.play(key);await new Promise(r=>setTimeout(r,75));return{key,voices:(Snd.pools[key]?.slots||[]).filter(Boolean).map(s=>({ready:s.el.readyState,volume:s.el.volume,muted:s.el.muted,time:s.el.currentTime,error:s.el.error?.code}))};}""",cue)
   ck(cue+' cue is decoded at positive native mixer volume',any(v['ready']>=2 and v['volume']>0 and not v['muted'] and v.get('error') is None for v in row['voices']),row)
  ck('No browser/draw/asset errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),checks=len(checks),errors=errors,results=checks);(O/'mechanics-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(c['passed'] for c in checks))
