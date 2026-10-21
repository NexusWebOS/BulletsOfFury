from pathlib import Path
import ast,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text());SETUP=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SETUP' for x in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+' '+json.dumps(data),flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=1,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}')
  p.evaluate('''()=>{story=special=null;BOFCinematicDirector.cancel();H3.ending=null;fb2Talk=fb2Intro=s6Opening=null;stagePlan=[];spawnClock=999999;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;boss=null;bossActive=false;subBoss=null;subBossActive=false;run.bombs=run2.bombs=99;run.pilot=run2.pilot="cole";p2Index=pilotIndex=PILOTS.findIndex(p=>p.key==="cole");player2.reset();player2.out=player2.dead=false;player2.invuln=99999;player2.x=worldWidth()/2+60;player2.y=VH-100;window.E=spawnEnemy("delta",worldWidth()/2,130,{});E.hp=E.maxhp=999999;E.vy=0;window.DODGE20=[];const roll=startRoll,somer=startSomersault;startRoll=function(dir){const q={seat:_seat,dir,at:performance.now()/1000,held:retinaScanHeld(),cool:player._rollCool,dead:player.dead};const r=roll.apply(this,arguments);q.active=!!player.roll;DODGE20.push(q);return r;};startSomersault=function(){const r=somer.apply(this,arguments);DODGE20.push({seat:_seat,type:"somer",active:!!player.somer});return r;};}''')
  for seat in [1,2]:
   p.evaluate('seat=>{coopOn=seat===2;}',seat)
   for mode in ['acquiring','locked','queued']:
    for action in ['left','right','up']:
     keys=p.evaluate('seat=>({scan:keybindFor(seat).multilock[0],left:keybindFor(seat).left[0],right:keybindFor(seat).right[0],up:keybindFor(seat).up[0]})',seat);key=keys[action]
     p.evaluate('''([seat,mode])=>withSeat(seat,()=>{player.roll=player.somer=null;player._rollCool=player._somerCool=0;player._tapL=player._tapR=player._tapU=-9;player._retinaScan=null;player.dead=player.out=false;player.invuln=99999;player.fireCd=99999;player.x=worldWidth()/2;player.y=VH-100;retinaScanAdd(E);if(mode!=="acquiring")retinaScanTick(.46);if(mode==="queued"){retinaScanFire();if(player._retinaScan.queue)player._retinaScan.queue.next=.5;}DODGE20=[];})''',[seat,mode]);p.evaluate(shoot.STEP,2)
     p.keyboard.down(keys['scan']);p.keyboard.down(key);p.evaluate(shoot.STEP,1);p.keyboard.up(key);p.evaluate(shoot.STEP,1);first=p.evaluate('seat=>withSeat(seat,()=>({tap:player._tapL,now:performance.now()/1000}))',seat);p.wait_for_timeout(20);p.keyboard.down(key);p.evaluate(shoot.STEP,1);p.keyboard.up(key);row=p.evaluate('seat=>withSeat(seat,()=>({roll:!!player.roll,somer:!!player.somer,tap:player._tapL,now:performance.now()/1000,scan:!!player._retinaScan,attempts:DODGE20}))',seat);ck(f'P{seat} {mode} real {action} double tap',row['somer' if action=='up' else 'roll'] and row['scan'],dict(first=first,**row));p.keyboard.up(keys['scan']);p.evaluate(shoot.STEP,45)
   # Cooldowns are still mandatory; multi-lock cannot reset or bypass them.
   row=p.evaluate('''seat=>withSeat(seat,()=>{player.roll=player.somer=null;player._rollCool=player._somerCool=3;startRoll(1);startSomersault();return !player.roll&&!player.somer;})''',seat);ck(f'P{seat} both native dodge cooldowns remain enforced',row)
  ck('No input/runtime errors',not errors,errors);b.close()
finally:stop()
(O/'input-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
