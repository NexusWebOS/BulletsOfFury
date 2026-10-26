"""Native GPT-bank, shootable-tool, three-volley and continuous-retreat checks.
Explicit checkpoints, not a claimed continuous gameplay recording.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_frames_1025/probe';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&c25Warm()&&c26Warm()}',timeout=180000)
  p.evaluate("""()=>{window.seedC26=(chrome=true)=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=300;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.ballSeen=true;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h.hammerDestroyed=false;h.c26HitGate=0;h.c26SpinClock=0;h._hf22Red=false;delete h.er23DepthCombo;delete h._hf22StormPair;delete h._hj22Pair;h.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]}:null;player.invuln=999;player.x=400;player.y=650;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedC26();}""")
  r=p.evaluate("""()=>Object.entries(C26_ART.banks).map(([bank,a])=>({bank,count:a.count,ready:Array.from({length:a.count},(_,f)=>{const k='c26_'+bank+'_'+f,im=XART.get(k);return XART.rdy(k)&&XART.rdy(k+'_hit')&&im.width===576&&im.height===576}).every(Boolean)}))""")
  ck('All 64 whole GPT frames and white hit banks decode on fixed even cells',sum(q['count'] for q in r)==64 and all(q['ready'] for q in r),r)
  p.evaluate("()=>{seedC26();boss._hammer.state='unfold';drawWorld(0);}");r=p.evaluate('ha21Blue(boss).a.key');ck('Opening dialogue always uses the dark regular armor plate',r=='c26_shield_regular_0',r);p.screenshot(path=str(O/'regular-opening.png'))
  for chrome in [False,True]:
   material='chrome' if chrome else 'regular';p.evaluate('v=>seedC26(v)',chrome)
   r=p.evaluate("""()=>{const out=[];for(let f=0;f<8;f++){const q=c26Pose(boss,'spin',f);out.push({key:q.a.key,tip:q.a.tip,bounds:q.a.bounds});}return out;}""")
   ck(material+' extended rotation has distinct complete poses and measured hammer travel',len({q['key'] for q in r})==8 and max(q['tip'][0] for q in r)-min(q['tip'][0] for q in r)>280,r)
   p.evaluate("()=>{boss._hammer.state='whirlwind';boss._hammer.c26SpinClock=4;drawWorld(0);}");p.screenshot(path=str(O/(material+'-extended.png')))
   p.evaluate("()=>{boss._hammer.state='shield';boss._hammer.t=.95;drawWorld(0);}");r=p.evaluate('ha21Blue(boss).a.key');ck(material+' shield formation reaches its authored foreground shield',r=='c26_shield_'+material+'_7',r);p.screenshot(path=str(O/(material+'-shield.png')))
   p.evaluate("()=>{boss._hammer.state='giant_sweep';boss._hammer.t=.2;boss.x=210;boss.y=540;hammerState(boss,'giant_recover');}")
   samples=[]
   for i in range(64):
    p.evaluate(STEP,1)
    samples.append(p.evaluate('()=>({x:boss.x,y:boss.y,k:ha21Blue(boss)?.k,key:ha21Blue(boss)?.a.key,state:boss._hammer.state})'))
    if i in [8,30,50]:p.screenshot(path=str(O/(material+'-retreat-'+str(i)+'.png')))
    if i%12==0:p.wait_for_timeout(2)
   step=max(((b['x']-a['x'])**2+(b['y']-a['y'])**2)**.5 for a,b in zip(samples,samples[1:]));keys={q['key'] for q in samples if q['key']}
   ck(material+' retreat uses recoil/brake poses with continuous position and scale',step<18 and all('c26_jump_'+material+'_'+str(f) in keys for f in [5,6,7]),dict(maxStep=step,keys=sorted(keys),end=samples[-1]))
  p.evaluate("()=>{seedC26();boss.x=120;boss.y=-60;window.giantBefore={x:boss.x,y:boss.y};hammerGiantArm(boss);}");r=p.evaluate('()=>({before:giantBefore,after:{x:boss.x,y:boss.y},state:boss._hammer.state})');ck('Orbital arm never teleports the actor to a different screen position',r['before']==r['after'] and r['state']=='giant_warn',r)
  p.evaluate("()=>{seedC26();hammerState(boss,'spin');hammerBoomerangRelease(boss);}")
  r=p.evaluate("""()=>{const h=boss._hammer,T=h.throw,at=hammerHeadPoint(boss),dir=T.er23Direction||1;_dmgBullet={kind:'bullet',x:at.x,y:at.y};const hit=bossHitTest(at.x,at.y);if(hit)hitBoss(1);_dmgBullet=null;drawWorld(0);return{hit,before:dir,after:T.er23Direction,state:h.state,destroyed:h.hammerDestroyed,flash:boss.flash};}""")
  ck('Regular shots physically hit and reverse the detached hammer without stunning or destroying it',r['hit'] and r['after']==-r['before'] and r['state']=='throw' and not r['destroyed'] and r['flash']>0,r)
  p.screenshot(path=str(O/'shot-hammer-reversed.png'))
  p.evaluate("()=>{seedC26();boss._hammer.state='whirlwind';boss._hammer.c26SpinClock=2;}")
  r=p.evaluate("""()=>{const at=hammerHeadPoint(boss);_dmgBullet={kind:'bullet',x:at.x,y:at.y};const hit=bossHitTest(at.x,at.y);if(hit)hitBoss(1);_dmgBullet=null;return{hit,back:boss._hammer.c26Backspin,state:boss._hammer.state};}""")
  ck('Held rotating hammer reverses briefly when shot while Chronos keeps attacking',r['hit'] and r['back']>0 and r['state']=='whirlwind',r)
  p.evaluate("""()=>{seedC26();window.ballShots=[];const laser=c26BallLaser;c26BallLaser=function(x,y,a,s,silent){ballShots.push({state:boss._hammer.state,t:boss._hammer.t,silent});return laser.apply(this,arguments)};boss._hammer.vx=150;boss._hammer.vy=165;C26.events.length=0;hammerState(boss,'ball');}""")
  trans=set()
  for i in range(340):
   p.evaluate(STEP,1)
   q=p.evaluate('()=>({state:boss._hammer.state,t:boss._hammer.t,key:ha21Blue(boss)?.a.key})')
   if q['state']=='uncurl':
    trans.add(q['key'])
    if len(trans) in [1,2,3,4]:
     if q['key'] not in getattr(ck,'shots',set()):
      ck.shots=getattr(ck,'shots',set())|{q['key']};p.screenshot(path=str(O/('unfold-'+str(len(trans))+'.png')))
   if i%18==0:p.wait_for_timeout(3)
  r=p.evaluate("()=>({events:C26.events,shots:ballShots})");volleys=[q for q in r['events'] if q['type']=='ball-laser-volley'];end=[q for q in r['events'] if q['type']=='ball-unfold']
  ck('Ball fires exactly three native laser volleys before unfolding',len(volleys)==3 and [q['volley'] for q in volleys]==[1,2,3] and len(r['shots'])==15 and all(q['state']=='ball' for q in r['shots']) and end and end[0]['time']>volleys[-1]['time'],r)
  ck('Return from ball displays four physical unfolding/glow plates',len(trans)==4,sorted(trans))
  ck('Only each volley leader requests the shared laser sound',sum(not q['silent'] for q in r['shots'])==3,r['shots'])
  p.evaluate("()=>{seedC26();fr27Restore(boss,.1,false,true);boss.y=boss._hammer.c25ChargeY;boss._drawY=boss.y;boss._hammer.t=1.6;drawWorld(0);}")
  r=p.evaluate('C26.objective');ck('SHOOT objective is drawn in front and fully above the raised hammer',r and r['y']>=50 and r['bottom']<=r['hammerTop']-8,r);p.screenshot(path=str(O/'shoot-above-hammer.png'))
  r=p.evaluate("""()=>{const b=boss;b.flash=0;b._gp4FlashNext=0;drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(b);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)n++;return n;}""");ck('New complete armored shield actor visibly flashes with real damaged pixels',r>100,r)
  p.evaluate(STEP,20);ck('Hit flash expires on new armor plates',p.evaluate('boss.flash<=0'))
  ck('No Chromium page or console errors',not errors,errors);br.close()
finally:stop()
out=dict(checks=checks,errors=errors,passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks));(O/'results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(passed=out['passed'],failed=out['failed'])),flush=True);raise SystemExit(0 if not out['failed'] else 1)
