from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,base64,math,argparse
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/pursuit_bomber_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];console=[];http=[];checks=[];profiles=[];shots=set()
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks-partial.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert v,name
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof PB28!=="undefined"&&pm27Live()',timeout=120000);p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000,polling=100);print('STAGE6 ASSETS READY',flush=True);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
   assert not errors,errors
  def setup(diff='furious'):
   p.evaluate('''d=>{diffKey=d;coopOn=false;run.ngplus=false;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(6);BOFCinematicDirector.cancel();story=null;debugUnlocked=true;debugStartFight({stage:6,role:'mini',kind:'siegebomber',name:'Pursuit bomber'},{pilot:'cole',record:false});DBGT.god=true;player.invuln=0;spawnSubBoss('siegebomber');debugFight.spawned=true;warnT=0;setState(GS.PLAY);subBossActive=true;PB28.events=[];for(const k of ['j','c','k','w','s','a','d'])Input.keys[k]=false;}''',diff)
  for diff in ['easy','normal','hard','furious']:
   setup(diff);points=[];paused=False
   for i in range(110):
    step(15);q=p.evaluate('''()=>{const b=subBoss,M=b?._pb28;return b?{mode:M?.mode||'entry',hidden:!!M?.hidden,x:b.x,y:b.y,clock:M?.clock||0,hp:b.hp,maxhp:b.maxhp,parts:b._bomber.parts.map(p=>({id:p.id,hp:p.hp})),live:pb28Count(b),targets:siegeBomberTargets(b).length,missiles:eBullets.filter(q=>q._pb28Owner===b&&q._pb28Type==='missile').length,bombs:groundTargetingFx.filter(q=>q._pb28Owner===b&&!q.dead).length}:null}''');
    if not q:break
    points.append(q)
    if diff=='furious'and q['mode']not in shots and q['mode']in ['weave','boost','ahead','reacquire','ambush','recover']:
     p.screenshot(path=str(W/('mode-'+q['mode']+'.png')));shots.add(q['mode'])
    if q['hidden']and not paused:
     old=p.evaluate('({hp:subBoss.hp,t:subBoss._pb28.t,clock:HUD28.stage.seconds})');p.evaluate("()=>{siegeBomberHit(subBoss,9999,subBoss.x,subBoss.y,'core');setState('paused');}");step(30);new=p.evaluate('({hp:subBoss.hp,t:subBoss._pb28.t,clock:HUD28.stage.seconds})');check(diff+' offscreen bomber rejects direct and locked damage',new['hp']==old['hp']);check(diff+' paused pursuit and both HUD clocks hold',old==new);p.evaluate('setState(GS.PLAY)');paused=True
   events=p.evaluate('PB28.events');modes={q['mode']for q in points};releases=[e for e in events if e['event']in ['bomb-release','missile-release']];waves=[e for e in events if e['event']=='ambush-wave'];profile={'difficulty':diff,'points':points,'events':events};profiles.append(profile)
   check(diff+' completes weave, throttle, offscreen pursuit and return barrage',{'weave','spool','boost','ahead','reacquire','ambush','recover'}<=modes,sorted(modes))
   xs=[q['x']for q in points if q['mode']=='weave'];check(diff+' visible weaving demands lateral pursuit',max(xs)-min(xs)>55,max(xs)-min(xs))
   check(diff+' releases actual bombs and physical missile volleys',any(e['event']=='bomb-release'for e in releases)and any(e['event']=='missile-release'for e in releases))
   check(diff+' every release comes from a live bomb rack or centre bay',all(e['part']in ['laserL','laserR','core']and e['mode']not in ['boost','ahead','reacquire']for e in releases),len(releases))
   check(diff+' releases never originate at either thruster',all(abs(abs(e['x']-e['actorX'])-72)>16 for e in releases))
   check(diff+' physical missile lanes leave a committed escape corridor',all(62<=e['gap']<=418 for e in waves))
   check(diff+' attack population stays bounded',max(q['live']for q in points)<=128,max(q['live']for q in points))
   check(diff+' offscreen hull has no Retina targets',all(q['targets']==0 for q in points if q['hidden']))
   print('PROFILE',diff,'modes',sorted(modes),'releases',len(releases),flush=True)
  setup();step(180)
  # A closer player catches the visible-distance manoeuvre sooner. Native inputs
  # are used in the film; this fixture isolates the perception boundary.
  times=p.evaluate('''()=>{const b=subBoss,out=[];for(const y of[VH-60,VH*.35]){b.y=viewTopY()-b.h-32;pb28Mode(b,'ahead');player.y=y;let ticks=0;while(b._pb28.mode==='ahead'&&ticks<300){pb28Tick(b,1/60);ticks++;}out.push(ticks/60);}return out}''');check('Forward pursuit materially shortens the catch-up interval',times[1]<times[0]*.6,times)
  p.evaluate("()=>{pb28Mode(subBoss,'weave');subBoss.y=subBoss.ty;subBoss._pb28.hidden=false;}");step(8)
  # Sample actual rendered white pixels before/after a native module hit.
  hit=p.evaluate('''()=>{const b=subBoss,q=siegeBomberParts(b).find(p=>p.id==='laserL'),sample=()=>{const d=ctx.getImageData(Math.max(0,Math.floor(q.x-camLeftX()-24)),Math.max(0,Math.floor(q.y-52)),48,104).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>245&&d[i+1]>245&&d[i+2]>245)n++;return n};return{before:sample(),x:q.x,y:q.y,hp:b._bomber.parts.find(p=>p.id==='laserL').hp}}''');p.evaluate("h=>siegeBomberHit(subBoss,20,h.x,h.y,'laserL')",hit);step(1);after=p.evaluate('''h=>{const d=ctx.getImageData(Math.max(0,Math.floor(h.x-camLeftX()-24)),Math.max(0,Math.floor(h.y-52)),48,104).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>245&&d[i+1]>245&&d[i+2]>245)n++;return{white:n,hp:subBoss._bomber.parts.find(p=>p.id==='laserL').hp}}''',hit);check('New bomb rack visibly flashes through the native module-hit path',after['white']>hit['before']+80 and after['hp']==hit['hp']-20,{'before':hit,'after':after});p.screenshot(path=str(W/'rack-hit.png'))
  eligibility=p.evaluate('''()=>{const b=subBoss,f=pb28Fragment(b,220,220,Math.PI/2),m=eShootT(200,200,Math.PI/2,3,'emissile',{silent:true,noMuzzle:true});m._pb28Type='missile';m._pb28Owner=b;const initial={fragment:enemyOrdnanceCanIntercept(f),missile:enemyOrdnanceCanIntercept(m)};s3kOrdnanceRules(f);s3kOrdnanceRules(m);return{initial,fragment:{shootable:f._shootable,proof:f._weaponProof,hp:f.hp??null},missile:{shootable:m._shootable,proof:m._weaponProof,hp:m.hp}}}''');check('Fragments cannot be shot down and physical missiles remain interceptable',not eligibility['initial']['fragment']and eligibility['initial']['missile']and not eligibility['fragment']['shootable']and eligibility['fragment']['proof']and eligibility['missile']['shootable']and not eligibility['missile']['proof'],eligibility)
  cancelled=p.evaluate('''()=>{const b=subBoss,p=pb28Port(b,'laserL'),q=pb28Bomb(b,p,{x:100,y:420},1.5);const prior=groundTargetingFx.filter(q=>q._pb28Owner===b&&q._pb28Part==='laserL'&&!q._pb28Released).length;const hp=b._bomber.parts.find(p=>p.id==='laserL').hp;siegeBomberHit(b,hp+1,p.x,p.y,'laserL');pb28BombTick(b);return{prior,remaining:groundTargetingFx.filter(q=>q._pb28Owner===b&&q._pb28Part==='laserL'&&!q._pb28Released&&!q.dead).length,pool:b.hp,expected:b._bomber.core+b._bomber.parts.reduce((s,p)=>s+p.hp,0)}}''');check('Breaking a rack cancels its pending drops without discarding other HP',cancelled['prior']>0 and cancelled['remaining']==0 and abs(cancelled['pool']-cancelled['expected'])<.001,cancelled)
  p.evaluate('''()=>{const b=subBoss;for(const part of b._bomber.parts.slice())if(part.hp>0)siegeBomberHit(b,part.hp+1,b.x,b.y,part.id);siegeBomberHit(b,b._bomber.core+1,b.x,b.y,'core');}''');check('Native modular exhaustion reaches death and cancels owned hazards',p.evaluate('subBoss.dead&&subBoss.hp===0&&!eBullets.some(q=>q._pb28Owner===subBoss&&!q.dead)&&!groundTargetingFx.some(q=>q._pb28Owner===subBoss&&!q.dead)'));step(300);check('Native death sequence exits the encounter',p.evaluate('subBossDone||state===GS.FLYOVER||state===GS.DEBUG||state==="debugfade"'))
  p.evaluate("()=>{run.stage=5;beginStage(5);spawnSubBoss('spacebomber');}");check('Space bomber is outside this Stage6-only change',p.evaluate('!pb28Own(subBoss)&&!subBoss._pb28'));br.close()
finally:
 stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'profiles':profiles,'pageErrors':errors,'consoleErrors':console,'HTTPerrors':http},indent=2),encoding='utf-8')
assert not errors and not http;print(json.dumps({'checksPassed':len(checks),'pageErrors':errors,'consoleErrors':console[:8],'HTTPerrors':http},indent=2),flush=True)
