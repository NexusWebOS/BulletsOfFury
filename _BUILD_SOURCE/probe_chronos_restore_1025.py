"""Native Chromium frame pixels, physical landmarks and complete depth chronology."""
from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_restore_1025';O.mkdir(exist_ok=True)
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
  for red in [False,True]:
   p.evaluate("v=>{seedMotion();boss._hammer._hf22Red=v;boss._hammer.giantLeft=1;hammerState(boss,'giant_idle');C27.events.length=0;}",red)
   states=[];keys=[];shots=set()
   for i in range(800):
    p.evaluate(STEP,1)
    q=p.evaluate("()=>({s:boss._hammer.state,key:ha21Blue(boss)?.a.key,t:boss._hammer.c27Combo?.clock,scale:ha21Blue(boss)?.k})")
    states.append(q['s']);keys.append(q['key'])
    label='second' if q.get('t',0) and .4<q['t']<.6 else 'left' if q.get('t',0) and 1.0<q['t']<1.2 else 'right' if q.get('t',0) and 1.6<q['t']<1.8 else None
    if label and label not in shots:shots.add(label);p.screenshot(path=str(O/(('red-' if red else 'chrome-')+label+'.png')))
    if i>30 and q['s']=='hammer':break
    if i%12==0:p.wait_for_timeout(2)
   events=p.evaluate('C27.events')
   ck(('Red' if red else 'Chrome')+' native depth attack includes second overhead, left and right',all(any(e['type']==name for e in events) for name in ['second-down','left-swing','right-swing']),events)
   ck(('Red' if red else 'Chrome')+' displays distinct overhead and both twist banks',all(any(k and part in k for k in keys) for part in ['strike_','left_','right_']),None)
   if red:red_frames=len(states)
   else:chrome_frames=len(states)
  ck('Rage hammer sequence runs at twice attack speed',abs(chrome_frames/red_frames-2)<.12,{'normal':chrome_frames,'rage':red_frames})
  p.evaluate("()=>{seedMotion();hammerState(boss,'ball');window.ballShots=0;const f=hammerLaser;hammerLaser=function(){ballShots++;return f.apply(this,arguments)};}")
  for _ in range(12):p.evaluate(STEP,15);p.wait_for_timeout(3)
  ck('Ball phase fires no lasers',p.evaluate('ballShots===0&&boss._hammer.state===\'ball\''))
  for missile in [False,True]:
   r=p.evaluate("""missile=>{boss.flash=0;_dmgBullet={kind:missile?'missile':'bullet',x:boss.x,y:boss.y};hammerBossDamage(boss,1);_dmgBullet=null;const q=ha21Blue(boss);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ha21Body(boss,q);const a=ctx.getImageData(0,0,cv.width,cv.height).data;let red=0,white=0;for(let i=0;i<a.length;i+=4){if(a[i+3]<100)continue;if(a[i]>200&&a[i+1]<100&&a[i+2]<100)red++;if(a[i]>240&&a[i+1]>240&&a[i+2]>240)white++;}ctx.restore();return{red,white,flash:boss.flash}}""",missile)
   ck(('Missile flashes white' if missile else 'Projectile flashes red')+' in actual ball pixels',r['white']>500 if missile else r['red']>500 and r['white']==0,r)
  p.evaluate(STEP,16);ck('Ball hit flash expires',p.evaluate('boss.flash<=0'))
  for red in [False,True]:
   p.evaluate("v=>{seedMotion();boss._hammer._hf22Red=v;fr27Restore(boss,.1,false,true);boss.y=boss._hammer.c25ChargeY;boss._drawY=boss.y;boss._hammer.t=1.6;drawWorld(0);}",red)
   p.screenshot(path=str(O/('shield-red.png' if red else 'shield-chrome.png')))
   r=p.evaluate("()=>({key:ha21Blue(boss).a.key,head:hammerHeadPoint(boss),body:boss.y,open:c25Counter(boss),prompt:C26.objective})")
   ck('Raised healing hammer is above body, visible and missile-counterable',r['head']['y']<r['body']-150 and r['open'] and r['prompt']['bottom']<r['prompt']['hammerTop'],r)
   r=p.evaluate("""()=>{const h=boss._hammer;_dmgBullet={kind:'bullet'};boss._hammerModuleHit='hammer';hammerBossDamage(boss,100);_dmgBullet=null;return {charging:h.recovery.status,knock:!!h.c25Knock}}""")
   ck('Ordinary shot cannot interrupt healing',r['charging']=='charging' and not r['knock'],r)
   r=p.evaluate("""()=>{const h=boss._hammer;_dmgBullet={kind:'missile'};boss._hammerModuleHit='hammer';hammerBossDamage(boss,100);_dmgBullet=null;return {charging:h.recovery.status,knock:!!h.c25Knock}}""")
   ck('Missile on overhead hammer cancels healing and knocks tool away',r['charging']=='cancelled' and r['knock'],r)
  p.evaluate("()=>{seedMotion();boss.hp=boss.maxhp*.15;hf22BeginBlueRage(boss);boss._hammer._hf22Charge.t=1.15;drawWorld(0);}")
  p.screenshot(path=str(O/'red-transformation.png'))
  ck('Rage charge selects red animated transformation',p.evaluate("ha21Blue(boss).a.key.startsWith('c27_rage_charge_')"))
  ck('No page/console errors',not errors,errors)
  br.close()
finally:stop()
out={'checks':checks,'errors':errors,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(O/'results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':out['passed'],'failed':out['failed']}));raise SystemExit(bool(out['failed']))
