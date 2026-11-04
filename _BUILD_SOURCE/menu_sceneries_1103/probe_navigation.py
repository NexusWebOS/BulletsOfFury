from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/menu_scrolling_1103';errors=[];events=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.route('**/assets/online-config.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'));p.goto('http://127.0.0.1:65041/game/index.html?quality=high',wait_until='load');p.wait_for_function('window.BOF_MENU_SCENERIES_1103&&__bofFrames>5',timeout=180000);p.wait_for_load_state('networkidle');p.mouse.click(2,2);p.evaluate('()=>{run.mode="arcade";P2M.choice=null;menuIndex=0;modeIndex=0;setState(GS.TITLE);stateT=2;}')
 def step(n=30):p.wait_for_timeout(n*1000/60)
 def action(k):
  p.keyboard.press(k);p.wait_for_timeout(800);q=p.evaluate('()=>({state,choice:P2M.choice,mode:run.mode,scene:MS113.last?.scene})');events.append({'action':k,**q});return q
 step(2);q=action('Enter');assert q['state']=='modesel',q
 p.evaluate('()=>{modeIndex=modeList().findIndex(m=>m.mode==="arcade");stateT=2;}');q=action('Enter');assert q['state']=='diff' or q['choice']=='arcade',q
 if q['choice']=='arcade':q=action('Enter')
 assert q['state']=='diff',q
 p.evaluate('()=>{menuIndex=0;stateT=2;}');q=action('Enter');assert q['state']=='pilot',q
 backKey=p.evaluate('()=>((keybind.bomb||[]).find(k=>k.length===1&&!keybind.fire.includes(k))||"Escape")');blocked=p.evaluate('SM22.blocked');q=action(backKey);assert q['state']=='pilot'and p.evaluate('SM22.blocked')>blocked,q
 startKey=p.evaluate('()=>((keybind.start||[]).find(k=>k!=="enter"&&!k.startsWith("mouse"))||"p")');q=action(startKey);assert p.evaluate('SM22.open')and q['state']=='pilot',q;before=p.evaluate('({...MS113.last})');p.wait_for_timeout(1000);assert p.evaluate('MS113.last.time')==before['time'];q=action(backKey);assert not p.evaluate('SM22.open')and q['state']=='pilot',q;after=p.evaluate('({...MS113.last})');assert after['time']-before['time']<1.6,(before,after)
 p.evaluate('()=>{setState(GS.MODESEL);modeIndex=modeList().findIndex(m=>m.mode==="coop");stateT=2;}');q=action('Enter');assert q['choice']=='coop',q
 q=action(backKey);assert q['state']=='modesel'and q['choice']is None,q
 scope=p.evaluate('()=>{const old=state;state=GS.PLAY;const before=JSON.stringify(MS113.draws),returned=menuScenery113("orbit");state=old;return {returned,unchanged:before===JSON.stringify(MS113.draws)}}');assert not scope['returned']and scope['unchanged'],scope
 p.goto('http://127.0.0.1:65041/game/index.html?quality=high&menubg=classic',wait_until='load');p.wait_for_function('window.BOF_MENU_SCENERIES_1103&&__bofFrames>5');p.wait_for_timeout(600);classic=p.evaluate('()=>({enabled:MS113.enabled,draws:MS113.draws})');assert not classic['enabled']and not classic['draws'],classic;assert not errors,errors;b.close()
result={'nativeKeyboardNavigation':events,'gameplayGuard':scope,'modeBackLockPreserved':True,'startMenuFreeze':{'before':before,'after':after},'classicFallback':classic,'errors':errors,'physicalControllerTested':False};(O/'navigation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
