"""Native Chromium frame pixels, physical landmarks and complete depth chronology."""
from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_final_1025';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000,polling=100);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000,polling=100)
  p.evaluate("""()=>{window.seedMotion=(chrome=true)=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=260;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h.c27Combo=null;h._hf22Charge=h._hj22Pair=h._hf22StormPair=null;h.hammerDestroyed=false;h._hf22Red=false;h.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]}:null;debugUnlocked=true;DBGT.god=true;player.invuln=0;player.x=320;player.y=430;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedMotion();}""")
  p.wait_for_function('hf22WarmRed(boss)',timeout=90000,polling=100)
  for ratio in [.35,.16]:
   r=p.evaluate("""ratio=>{seedMotion();boss.hp=boss.maxhp*ratio;boss._hammer.frArmor.hp=0;boss._hammer.frArmor.checkpoints=[.75,.5,.35];for(let i=0;i<12;i++)hammerBossTick(boss,1/60);return{red:boss._hammer._hf22Red,charge:!!boss._hammer._hf22Charge,state:boss._hammer.state}}""",ratio)
   ck('No rage at '+str(int(ratio*100))+' percent HP',not r['red'] and not r['charge'],r)
  r=p.evaluate("""()=>{seedMotion();boss.hp=boss.maxhp*.15;boss._hammer.frArmor.hp=0;hammerBossTick(boss,1/60);return{red:boss._hammer._hf22Red,charge:!!boss._hammer._hf22Charge,state:boss._hammer.state}}""")
  ck('15 percent HP begins the charge before permanent rage',r['charge'] and not r['red'] and r['state']=='hf22_rage_charge',r)
  for i in range(9):p.evaluate(STEP,10);p.wait_for_timeout(3)
  p.evaluate('drawWorld(0)');p.screenshot(path=str(O/'red-charge.png'))
  for i in range(4):p.evaluate(STEP,10);p.wait_for_timeout(3)
  ck('The completed charge activates permanent red armor',p.evaluate('boss._hammer._hf22Red&&!boss._hammer._hf22Charge'))
  r=p.evaluate("""()=>{boss.hp=boss.maxhp*.5;hammerState(boss,'hammer');for(let i=0;i<30;i++)hammerBossTick(boss,1/60);return {red:boss._hammer._hf22Red,key:ha21Blue(boss)?.a.key}}""")
  ck('Rage persists even if he subsequently regains health',r['red'] and '_red_' in r['key'],r)
  p.evaluate('drawWorld(0)');p.screenshot(path=str(O/'red-permanent.png'))
  p.evaluate("""()=>{seedMotion(false);boss._hammer.openingJump1003=false;boss._hammer.c27RagePending=false;fr27BeginArmor(boss);}""")
  frames=[]
  for i in range(205):
   p.evaluate(STEP,1)
   q=p.evaluate("()=>({t:boss._hammer.t,s:boss._hammer.state,key:ha21Blue(boss)?.a.key,head:hammerHeadPoint(boss),body:{x:boss.x,y:boss.y},armor:fr27Armor(boss)?.activated,red:hf22Red(boss)})");frames.append(q)
   if i in [30,65,110,160]:p.screenshot(path=str(O/('armor-'+str(i)+'.png')))
   if i%12==0:p.wait_for_timeout(2)
  held=[q for q in frames if q['s']=='fr_activation' and q['t']>.7]
  ck('Chromium charge keeps the actual hammer above him',len(held)>100 and all(q['head']['y']<q['body']['y']-160 for q in held),{'count':len(held),'minHeadY':min(q['head']['y']for q in held)})
  ck('Overhead chromium charge uses its distinct animated bank',len(set(q['key']for q in held))>=20 and not any(q['red']for q in held),None)
  ck('Chromium activation completes before the next attack',p.evaluate("fr27Armor(boss)?.activated&&boss._hammer.state!=='fr_activation'&&!boss._noHit"))
  p.evaluate("""()=>{seedMotion();boss._hammer.c27RagePending=false;C27.events.length=0;window.laserCount=0;window.missileCues=[];const old=hammerLaser;hammerLaser=function(){laserCount++;return old.apply(this,arguments)};const cue=b20Cue;b20Cue=function(k){missileCues.push(k);return cue.apply(this,arguments)};hammerState(boss,'nova_charge');}""")
  released=[];keys=[]
  for i in range(315):
   p.evaluate(STEP,1);q=p.evaluate("()=>({s:boss._hammer.state,t:boss._hammer.t,shots:boss._hammer.novaShots,key:ha21Blue(boss)?.a.key,events:C27.events.filter(e=>e.type==='hammer-missile-impact')})");keys.append(q['key'])
   if len(q['events'])>len(released):released=q['events'];p.screenshot(path=str(O/('missile-impact-'+str(len(released))+'.png')))
   if i%12==0:p.wait_for_timeout(2)
  data=p.evaluate("()=>({events:C27.events.filter(e=>e.type==='hammer-missile-impact'),lasers:laserCount,cues:missileCues,missiles:eBullets.filter(q=>q._c27Missile).map(q=>({kind:q.kind,shootable:q._shootable,volley:q._c27Volley,angle:q.ang}))})")
  ck('Three physical down-strikes each launch one circular missile ring',len(data['events'])==3 and [e['index']for e in data['events']]==[1,2,3] and all(e['count']==16 for e in data['events']),data['events'])
  ck('Former laser-volley attack launches no lasers',data['lasers']==0)
  ck('Every missile ring has its impact and launch cue',data['cues'].count('missile')==3 and data['cues'].count('hammerImpact')==3,data['cues'])
  ck('Ring ordnance uses the native shootable missile owner',len(data['missiles'])>0 and all(q['kind']=='emissile' and q['shootable']for q in data['missiles']),{'remaining':len(data['missiles'])})
  ck('All three volleys use the actual overhead strike and retraction frames',any('windup' in k for k in keys) and any('strike' in k for k in keys) and any('retract' in k for k in keys))
  for mat in ['regular','chrome','red']:
   p.evaluate("""mat=>{seedMotion(mat!=='regular');boss._hammer._hf22Red=mat==='red';boss._hammer.c27RagePending=false;hammerWhirlStart(boss);boss._hammer.state='whirlwind';}""",mat)
   for f in [0,5,10,16,22]:
    p.evaluate("f=>{boss._hammer.c26SpinClock=f/1.8;drawWorld(0)}",f);p.screenshot(path=str(O/(mat+'-spin-'+str(f)+'.png')))
  p.evaluate("""()=>{seedMotion();const h=boss._hammer;h.c27RagePending=false;h.ballSeen=h.whirlSeen=h.hb20PickupDone=true;h.mode='chaingun';h.phaseTwo=true;h.hammerDestroyed=true;h.frArmor.hp=0;boss.hp=boss.maxhp*.15;hammerState(boss,'chain_cool');}""")
  forms=[]
  for i in range(1500):
   p.evaluate(STEP,1)
   if i%12==0:
    p.wait_for_timeout(2);forms.append(p.evaluate("()=>({red:boss._hammer._hf22Red,s:boss._hammer.state,key:ha21Blue(boss)?.a.key})"))
  active=[q for q in forms if q['red']]
  ck('Rage entered from the late chaingun phase stays in red hammer combat',len(active)>100 and not any(q['s'].startswith('chain') or q['s'] in ['hb20_pickup','recharge1002'] for q in active),{'states':sorted(set(q['s']for q in active))})
  ck('Late-fight rage never falls back to blue humanoid or ball plates',all(q.get('key') and ('_red_' in q['key'] or q['key'].startswith('c27_rage')) for q in active),{'keys':sorted(set(q.get('key','none')for q in active))})
  ck('New15-percent charge satisfies the old rage completion gate',p.evaluate('boss._hammer._fb2RageDone===true'))
  ck('No page or console errors',not errors,errors)
  (O/'results.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2)+'\n')
  br.close()
finally:stop()
print(json.dumps({'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks)}),flush=True)
