"""Native difficulty and damage checks for the shipped password encounters."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/siege_passwords_1010';OUT.mkdir(exist_ok=True)
checks=[];errors=[];budgets={}
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def step(p,seconds):
 for _ in range(round(seconds*10)):
  p.evaluate('()=>{for(let i=0;i<6;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);if(typeof fb9HudSplit==="function")fb9HudSplit();}')
  p.wait_for_timeout(5)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1180,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('ASSETS.ready&&typeof SG10!=="undefined"',polling=50);p.evaluate(shoot.TRAP_RAF)
  for code in ['SONIC','ORDOS','HARK']:
   budgets[code]=[]
   for diff in ['easy','normal','hard','furious']:
    p.evaluate('''(q)=>{BOFCinematicDirector.cancel();story=null;run.mode="arcade";setState(GS.PASSWORD);pwInput=q.code;submitPassword();
     diffKey=q.diff;DIFF=difficultyForRun("arcade",q.diff);pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");startRun(PENDING_STAGE);player.invuln=999;Input.clearTaps?.();}''',{'code':code,'diff':diff})
    p.wait_for_function('subBoss?._sg10&&sg10Ready(subBoss)',polling=50);step(p,4)
    info=p.evaluate('()=>({hp:subBoss.maxhp,w:subBoss.w,h:subBoss.h,top:subBoss.y+subBoss._sg10.top,bottom:subBoss.y+subBoss._sg10.bot,playTop:PLAY.y,playBot:PLAY.y+PLAY.h,enter:subBoss.enter})')
    budgets[code].append(info['hp'])
    check(code+' '+diff+' arrives with complete visible art and a live HP budget',not info['enter'] and info['hp']>0 and info['top']>=info['playTop'] and info['bottom']<info['playBot']-20,info)
    p.evaluate('()=>{subBoss._sg10.attack=null;subBoss._sg10.rest=0;eBullets=[];sg10StartAttack(subBoss);}')
    event=p.evaluate('SG10.clock');step(p,4)
    info=p.evaluate('(n)=>({shots:SG10.events.filter(q=>q.t>=n&&q.name==="shot").length,count:subBoss._sg10.attack?.count,missiles:eBullets.filter(q=>q._sg10Unit==="deviator").map(q=>q.hp),lockPoints:Object.keys(subBoss._sg10.lockPixels||{}).length})',event)
    check(code+' '+diff+' completes its first live attack with southbound shots',info['shots']>=4 and p.evaluate('eBullets.filter(q=>q._sg10Unit).every(q=>q.vy>0)'),info)
    if diff=='furious':p.screenshot(path=str(OUT/(code.lower()+'-furious.png')))
   check(code+' HP scales monotonically across all four difficulties',all(a<b for a,b in zip(budgets[code],budgets[code][1:])),budgets[code])
  # Use the actual ship shield/death handlers. No playerHit replacement is used.
  p.evaluate('''()=>{subBoss._sg10.attack=null;subBoss._sg10.rest=999;eBullets=[];pBullets=[];enemies=[];powerups=[];
   player.dead=false;player.out=false;player.invuln=0;run.shield=3;special=null;player.x=camLeftX()+20;player.y=PLAY.y+PLAY.h-25;}''')
  info=p.evaluate('''()=>{const b=subBoss,q={x:player.x,y:player.y,_sg10Unit:b._sg10.unit,_sg10Owner:b,_sg10Charged:false};sg10Detonate(q,true);
   const before=run.shield;sg10FXTick(.10);const after=run.shield;player.invuln=0;sg10FXTick(.10);return {before,after,again:run.shield};}''')
  check('Live blast spends one ship shield and cannot hit that seat twice',info['after']==info['before']-1 and info['again']==info['after'],info)
  p.evaluate('''()=>{SG10.fx=[];player.invuln=0;run.shield=3;sg10Detonate({x:subBoss.x,y:subBoss.y,_sg10Unit:subBoss._sg10.unit,_sg10Owner:subBoss,_sg10Charged:false},true);sg10FXTick(.1);}''')
  check('A ship outside the visible small blast keeps its shield',p.evaluate('run.shield===3&&!player.dead'))
  p.evaluate('''()=>{setState(GS.PASSWORD);pwInput="SONIC";submitPassword();diffKey="furious";DIFF=difficultyForRun("arcade",diffKey);startRun(PENDING_STAGE);player.invuln=999;}''')
  p.wait_for_function('sg10Ready(subBoss)',polling=50);step(p,4)
  info=p.evaluate('''()=>{const b=subBoss,S=b._sg10;S.attack=null;S.rest=999;SG10.fx=[];eBullets=[];pBullets=[];enemies=[];powerups=[];
   let gap=null;for(let y=b._drawY+b.h*.15;y<b._drawY+b.h*.45&&!gap;y+=2)if(sg10At(b,b.x,y,6)===null)gap={x:b.x,y};
   if(!gap)return null;player.x=gap.x;player.y=gap.y;player.invuln=0;run.shield=3;updatePlay(1/60);return {gap,shield:run.shield,dead:player.dead};}''')
  check('Sonic fork opening causes no invisible rectangle collision',info is not None and info['shield']==3 and not info['dead'],info)
  info=p.evaluate('''()=>{const b=subBoss,q=sg10Point(b,SG10_RIG[0]);player.x=q.x;player.y=q.y;player.invuln=0;run.shield=3;updatePlay(1/60);return {shield:run.shield,dead:player.dead,point:q};}''')
  check('Contact with an actual tank module damages the ship',info['shield']==2 and not info['dead'],info)
  info=p.evaluate('''()=>{const b=subBoss,m=SG10_RIG.at(-1),a=sg10Point(b,m),cached=b._sg10.lockPixels.weapon;sg10Point(b,m);return !!cached&&b._sg10.lockPixels.weapon===cached&&sg10At(b,a.x,a.y)!==null;}''')
  check('Missile lock pixels are cached on opaque authored metal',info)
  br.close()
finally:stop()
check('No browser, console or asset errors in difficulty/damage checks',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'checks':checks,'errors':errors,'hp':budgets}
(OUT/'difficulty.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
