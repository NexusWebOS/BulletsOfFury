from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/controls-modes';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);c=b.new_context(viewport={'width':1440,'height':1000});p=c.new_page();p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 def boot():p.goto('http://127.0.0.1:8765/index.html?release-controls=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')
 def step(n):
  for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(1)
 def tap(k='j'):p.evaluate('k=>Input.injectTap(k)',k);step(1);step(60)
 boot();step(30);p.keyboard.down('Enter');step(1);p.keyboard.up('Enter');step(420);ck('native boot reaches its opener after a real Start press',p.evaluate('state!==GS.BOOT'),p.evaluate('state'))
 for mode in ['campaign','arcade','coop','bossrush','timeattack']:
  p.evaluate("m=>{P2M.choice=null;_selFlash=null;debugFight=null;setState(GS.MODESEL);modeIndex=modeList().findIndex(q=>q.mode===m);Input.clearTaps();}",mode);step(30);tap()
  q=p.evaluate('({state,choice:P2M.choice,pending:P2M.pending,coop:coopOn})')
  good=q['state']=='camphub'if mode=='campaign'else q['state']=='diff'if mode=='arcade'else q['choice']=='coop'if mode=='coop'else q['state']=='modesel'and not q['pending']
  ck('fresh-profile '+mode+' menu route/lock',good,q)
  p.screenshot(path=str(O/(mode+'.jpg')),type='jpeg',quality=82)
 for mode in ['bossrush','timeattack']:
  p.evaluate("m=>{P2M.receipt={version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,8],pilot:'cole',difficulty:'hard'};P2M.choice=null;P2M.active=null;_selFlash=null;setState(GS.MODESEL);modeIndex=modeList().findIndex(q=>q.mode===m);}",mode);step(25);tap()
  ck('earned-profile '+mode+' enters native difficulty selection',p.evaluate('state===GS.DIFF&&P2M.pending===\''+mode+'\''))
  p.evaluate("()=>{diffKey='hard';pilotIndex=PILOTS.findIndex(q=>q.key==='cole');startRun(1);player.invuln=1e8;player._spawnClearT=1e8;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',polling=50);step(420)
  q=p.evaluate('({state,active:P2M.active,stage:run.stage,boss:!!boss,elapsed:P2M.elapsed})');ck(mode+' starts its native run owner',q['active']==mode and q['stage']==1 and(mode!='bossrush'or q['boss']),q)
  if mode=='timeattack'and q['state']!='play':step(1200);q=p.evaluate('({state,active:P2M.active,stage:run.stage,boss:!!boss,elapsed:P2M.elapsed})')
  if mode=='timeattack':ck('Time Attack completes its real launch into playable combat',q['state']=='play',q)
  if q['state']=='play':
   tap('enter');s=p.evaluate('({state,clock:stageTimer,elapsed:P2M.elapsed})');step(90);end=p.evaluate('({state,clock:stageTimer,elapsed:P2M.elapsed})');ck(mode+' native pause freezes stage and mode clock',s['state']=='paused'and end==s,{'start':s,'end':end});tap('enter')
  p.evaluate('()=>{P2M.active=null;P2M.pending=null;debugFight=null;}')
 # Synthetic raw Gamepad API data: native poll, bindings and live firing; no attached hardware claim.
 p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',polling=50)
 p.evaluate("()=>{stagePlan=[];enemies=[];boss=subBoss=null;bossActive=subBossActive=false;spawnClock=1e9;window.pad16=(index)=>({index,id:'8BitDo M30 raw D-input '+index,connected:true,mapping:'',axes:[0,0],buttons:Array.from({length:18},()=>({pressed:false,value:0}))});window.pad16a=pad16(2);window.pad16b=pad16(3);window.pad16list=[null,null,pad16a,null];Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>pad16list});coopOn=false;Input.pollGamepad();pad16a.buttons[0]={pressed:true,value:1};player.fireCd=0;pBullets=[];}")
 step(2);ck('raw first-present controller fires on its first default press without Options',p.evaluate('Input.hold(1,"fire")&&pBullets.length>0'))
 p.evaluate("()=>{pad16a.buttons[0]={pressed:false,value:0};Input.pollGamepad();coopOn=true;pad16list=[null,null,pad16a,pad16b];Input.pollGamepad();pad16b.buttons[0]={pressed:true,value:1};Input.pollGamepad();}")
 q=p.evaluate('({p1:Input.hold(1,"fire"),p2:Input.hold(2,"fire")})');ck('two raw controllers retain separate seats',not q['p1']and q['p2'],q)
 p.evaluate('()=>{pad16list=[null,null,null,pad16b];Input.pollGamepad();}');q=p.evaluate('({p1:Input.hold(1,"fire"),p2:Input.hold(2,"fire")})');ck('disconnecting controller1 never transfers controller2 to player1',not q['p1']and q['p2'],q)
 p.evaluate('()=>{pad16list=[null,null,pad16a,pad16b];Input.pollGamepad();}');q=p.evaluate('({p1:Input.hold(1,"fire"),p2:Input.hold(2,"fire")})');ck('reconnecting controller1 preserves controller2 ownership',not q['p1']and q['p2'],q)
 p.evaluate("()=>{const kb=JSON.parse(JSON.stringify(KEYBIND_DEFAULT));kb.fire=['pad_b5'];kb.retina=kb.retina.filter(k=>k!=='pad_b5');localStorage.setItem('bof_keys',JSON.stringify(kb));}")
 boot();q=p.evaluate("()=>{window.pad16a={index:2,id:'8BitDo M30 raw D-input',connected:true,mapping:'',axes:[0,0],buttons:Array.from({length:18},(_,i)=>({pressed:i===5,value:i===5?1:0}))};Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[null,null,pad16a]});Input.pollGamepad();return{bind:keybindFor(1).fire,held:Input.hold(1,'fire')};}")
 ck('saved raw controller fire mapping works immediately after reload',q['bind']==['pad_b5']and q['held'],q)
 ck('no page or console errors',not errors,errors);b.close()
(O/'report.json').write_text(json.dumps({'scope':'Real native menu/input/clock tests; earned bonus modes are prepared profiles, not natural completion unlocks. Gamepad data are synthetic raw-API samples: actual8BitDo hardware, wireless modes and OS driver behavior remain unverified.','checks':checks,'errors':errors},indent=2),encoding='utf8')
sys.exit(any(not q['ok']for q in checks))
