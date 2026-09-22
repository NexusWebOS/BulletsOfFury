import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/supplies_0922');O.mkdir(exist_ok=True)
port,stop=serve(GAME);r={};errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  qa=br.new_context(storage_state={'cookies':[],'origins':[]},viewport={'width':1280,'height':900})
  pg=qa.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,arg=None):return pg.evaluate(s,arg)
  def step(n):
   while n>0:
    z=ev(STEP,min(60,n));assert not z,z;n-=60;pg.wait_for_timeout(30)
  def tap(k):
   pg.keyboard.down(k);step(1);pg.keyboard.up(k);step(2)
  def cap(n): (O/(n+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':2,'pilot':'cole','invuln':True})
  ev('''()=>{run.mode='arcade';diffKey='hard';DIFF=difficultyForRun('arcade','hard');run.score=2500000;run.lives=3;run.contUsed=0;run.contBonus=0;
    stageStats.scoreStart=0;stageStats.kills=90;stageStats.spawned=100;stageStats.shots=500;stageStats.hits=320;
    run._fpLevelDone=false;drawStageClear._init=false;drawStageClear._unShown=false;run._forgeShown=true;setState(GS.STAGECLEAR);}''')
  step(51)
  r['tally']=ev('''()=>({t:stateT,score:drawStageClear._scoreShown,target:drawStageClear._res.score+drawStageClear._res.bonus,ready:drawStageClear._fast,fp:run._fpLevel.fp,conversions:furiousLedger().levels.length})''')
  pg.wait_for_function("()=>XART.rdy('statpanel_full_0916')");step(1);cap('quick_tally')
  step(100);r['conversionsAfter']=ev('()=>furiousLedger().levels.length')
  # Follow the real debrief callbacks, skipping optional forging without buying weapons.
  r['route']=[]
  for i in range(12):
   st=ev('()=>state');r['route'].append(st)
   if st=='supplies':break
   step(100);tap('Enter' if st in ['forge','loadout'] else 'j');step(45)
  assert ev('()=>state')=='supplies',r['route']
  pg.wait_for_function("()=>XART.rdy('mode_life_up_0915')&&XART.rdy('mode_continue_up_0915')");step(20);cap('shop')
  # One A press buys exactly one life, even when held for many frames.
  before=ev('()=>({fp:furiousBalance(),lives:run.lives,bonus:run.contBonus,score:run.score})')
  pg.keyboard.down('j');step(30);pg.keyboard.up('j');step(3)
  after=ev('()=>({fp:furiousBalance(),lives:run.lives,bonus:run.contBonus,score:run.score})')
  r['life']={'before':before,'after':after}
  tap('ArrowDown');tap('j');r['continue']=ev('()=>({fp:furiousBalance(),bonus:run.contBonus,cap:continueCap()})');cap('purchased')
  r['persist']=ev('''()=>{const bal=furiousBalance(),stock=campSnapshot(),orig=achievementState;achievementState=achievementLoad();const loaded=furiousBalance();achievementState=orig;
    return {bal,loaded,lives:stock.lives,bonus:stock.contBonus};}''')
  # Native B goes back to loadout; Start returns to supplies with stock intact.
  back=ev("()=>keybind.bomb.find(k=>!/^mouse|^pad_/.test(k))");tap(back);r['back']=ev('()=>state');step(40);tap('Enter');step(45);r['return']=ev('()=>({state,lives:run.lives,fp:furiousBalance()})')
  r['guards']=ev('''()=>{const out={},L=furiousLedger();run.lives=9;let b=furiousBalance();out.full=supplyBuy('life',1);out.fullNoCharge=furiousBalance()===b;
    const old=DIFF;DIFF=Object.assign({},DIFF,{continues:-1});out.unlimited=supplyBuy('continue',1);out.unlimitedNoCharge=furiousBalance()===b;DIFF=old;
    const save=achievementSave;achievementSave=()=>false;run.lives=3;out.save=supplyBuy('life',1);out.rollback=run.lives===3&&furiousBalance()===b;achievementSave=save;
    const oldProfile=achievementState;achievementState=achievementEmpty();out.poor=supplyBuy('life',1);out.poorNoGrant=run.lives===3;achievementState=oldProfile;
    return out;}''')
  # Pointer purchase, coordinates transformed through the actual canvas rectangle.
  step(20)
  rect=ev('''()=>{const c=cv.getBoundingClientRect(),q=supplyScr.rects[0];return{x:c.left+(q.x+q.w/2)/cutsceneViewWidth()*c.width,y:c.top+(q.y+q.h/2)/VH*c.height};}''')
  pg.mouse.move(rect['x'],rect['y']);pg.mouse.down();step(2);pg.mouse.up();step(2);r['mouse']=ev('()=>run.lives')
  # Portrait viewport and co-op each retain readable rows.
  pg.set_viewport_size({'width':900,'height':1400});step(4);cap('shop_portrait')
  ev('()=>{coopOn=true;run2.lives=2;suppliesStart(()=>setState(GS.TITLE),null);}');step(20);cap('shop_coop')
  r['coop']=ev("()=>{const before=run2.lives,fp=furiousBalance(),q=supplyBuy('life',2);return {q,before,after:run2.lives,cost:fp-furiousBalance()};}")
  # Start skips purchase and calls the next-stage continuation exactly once.
  ev('()=>{coopOn=false;window.leftShop=0;suppliesStart(()=>{leftShop++;setState(GS.TITLE);},null);}');step(20);tap('Enter');r['exit']=ev('()=>({state,count:leftShop,closed:supplyBuy("life",1)})')
  # Co-op tally and immediate A skip share the same cap.
  ev('()=>{coopOn=true;run2.score=500000;drawStageClear._init=false;setState(GS.STAGECLEAR);}');step(51)
  r['coopTally']=ev('()=>({fast:drawStageClear._fast,score:drawStageClear._scoreShown2,target:drawStageClear._res.seats[1].score+drawStageClear._res.seats[1].bonus})')
  ev('()=>{coopOn=false;drawStageClear._init=false;setState(GS.STAGECLEAR);}');step(15);tap('j');r['skip']=ev('()=>({state,fast:drawStageClear._fast,score:drawStageClear._scoreShown,target:drawStageClear._res.score+drawStageClear._res.bonus})')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert r['tally']['ready'] and r['tally']['score']==r['tally']['target'] and r['tally']['t']<1
assert r['tally']['conversions']==r['conversionsAfter']
assert 'loadout' in r['route'] and r['route'][-1]=='supplies'
assert after['lives']==before['lives']+1 and after['fp']==before['fp']-250 and after['score']==before['score']
assert r['continue']['bonus']==before['bonus']+1 and r['continue']['fp']==after['fp']-750
assert r['persist']['bal']==r['persist']['loaded'] and r['persist']['bonus']==r['continue']['bonus']
assert r['back']=='loadout' and r['return']['state']=='supplies'
assert r['guards']=={'full':'maxed','fullNoCharge':True,'unlimited':'unlimited','unlimitedNoCharge':True,'save':'save','rollback':True,'poor':'poor','poorNoGrant':True}
assert r['mouse']==4
assert r['coop']['q']=='ok' and r['coop']['after']==3 and r['coop']['cost']==250
assert r['exit']=={'state':'title','count':1,'closed':'closed'}
assert r['coopTally']['fast'] and r['coopTally']['score']==r['coopTally']['target']
assert r['skip']['state']=='stageclear' and r['skip']['fast'] and r['skip']['score']==r['skip']['target']
