"""Actual Chromium contract/pixels, with explicit checkpoint setups, not gameplay footage."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_contract_1025';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
 if not ok:print(json.dumps(d),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();if(typeof c25Warm==='function')c25Warm();}")
  p.wait_for_function("()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&(typeof c25Warm!=='function'||c25Warm())}",timeout=180000)
  p.evaluate("""()=>{window.seedC25=()=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=260;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='warn';h.t=.1;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=null;h.hammerDestroyed=false;delete h.er23DepthCombo;delete h._hf22StormPair;delete h._hj22Pair;h.frArmor={hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]};player.invuln=999;player.x=400;player.y=650;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedC25();window.c25Shoot=(x,y,kind='bullet',dmg=3)=>{const q={x,y,kind,vx:0,vy:-8};_dmgBullet=q;_dmgSrc=hammerMissile(q)?'missile':null;const hit=bossHitTest(x,y),part=boss._hammerModuleHit;if(hit){_lastHitX=x;_lastHitY=y;hitBoss(dmg);} _dmgBullet=null;_dmgSrc=null;return {hit,part,state:boss._hammer.state,hp:boss.hp,armor:fr27Armor(boss)?.hp};};}""")
  r=p.evaluate("""()=>{const out=[];for(const state of ['warn','spin','whirlwind','fr_twirl','storm_warn']){seedC25();boss._hammer.state=state;boss._hammer.hammerHP=1;const at=hammerHeadPoint(boss);for(let i=0;i<12;i++)c25Shoot(at.x,at.y,'missile',20);out.push({before:state,after:boss._hammer.state,destroyed:boss._hammer.hammerDestroyed,pending:boss._hammer.hm10BreakPending,flash:boss.flash});}return out;}""")
  ck('Gunfire and missiles during attacks never disarm or stun Chronos',all(q['before']==q['after'] and not q['destroyed'] and not q['pending'] and q['flash']>0 for q in r),r)
  p.evaluate("()=>{seedC25();hammerState(boss,'hammer');fr27Restore(boss,.1,false,true);boss.y=boss._hammer.c25ChargeY;boss._drawY=boss.y;boss._hammer.t=1.6;boss._hammer.recovery.elapsed=.2;drawWorld(0);}")
  r=p.evaluate("()=>{const b=boss;return c25Shoot(b.x+25,b.y,'missile',40);}");ck('A missile into the body cannot trigger the hammer counter',r['state']=='storm_raise',r)
  r=p.evaluate("()=>{const at=hammerHeadPoint(boss);return c25Shoot(at.x,at.y,'bullet',999);}");ck('Even heavy ordinary fire into the glowing hammer cannot stun him',r['state']=='storm_raise',r)
  r=p.evaluate("""()=>{const calls=[],old=ctx.drawImage;ctx.drawImage=function(im,...a){calls.push(HA21.tags.get(im)||'');return old.call(this,im,...a);};try{drawWorld(0)}finally{ctx.drawImage=old}return {calls:calls.filter(k=>/c27_windup|shield_wall/.test(k)),pose:ha21Blue(boss)?.a.key,frame:ha21Blue(boss)?.a.frame};}""")
  ck('One whole armored actor appears behind exactly one transparent foreground shield',r['pose']=='c27_windup_chrome_16' and r['frame']==16 and sum('shield_wall' in q for q in r['calls'])==1,r)
  p.screenshot(path=str(O/'charging-shield.png'))
  r=p.evaluate("()=>{const at=hammerHeadPoint(boss);_dmgBullet={kind:'missile',x:at.x,y:at.y,_auto:true};bossHitTest(at.x,at.y);hitBoss(100);_dmgBullet=null;return boss._hammer.state;}");ck('Passive homing missiles cannot trigger the deliberate counter',r=='storm_raise',r)
  r=p.evaluate("()=>{const at=hammerHeadPoint(boss);const r=c25Shoot(at.x,at.y,'missile',1);return {...r,knock:boss._hammer.c25Knock,wall:hm10WallActive(boss)};}");ck('One deliberate raised-hammer missile cancels charging and drops the shield',r['state'] in ['fr_stun','storm_stun'] and r['knock'] and not r['wall'],r)
  p.evaluate(STEP,12)
  poses=[];scales=[]
  for name,at in [('depart',.25),('distant',1.3),('recall',3.35),('catch',4.2)]:
   p.evaluate("t=>{const k=boss._hammer.c25Knock;k.t=t;boss._hammer.t=t;drawWorld(0)}",at);p.screenshot(path=str(O/(name+'.png')))
   poses.append(p.evaluate('ha21Blue(boss)?.kind'));scales.append(p.evaluate('C25.lastTool?.scale'))
  ck('Hammer visibly shrinks into space then grows back during magnetic recall',scales[1]<scales[0] and scales[2]>scales[1] and scales[3]>.95,scales)
  ck('Empty-handed chromium recovery frames remain selected throughout stun',all('c25_empty_armor' in q for q in poses),poses)
  r=p.evaluate("""()=>{const b=boss;b.flash=0;b._gp4FlashNext=0;drawWorld(0);const old=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(b);drawWorld(0);const now=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<now.length;i+=4)if(now[i]>240&&now[i+1]>240&&now[i+2]>240&&old[i]+old[i+1]+old[i+2]<650)white++;return{white,flash:b.flash};}""");ck('Armored kneeling actor visibly flashes when hit',r['white']>100,r)
  p.evaluate('()=>{boss._hammer.c25Knock.t=1;boss._hammer.t=1;}');p.evaluate(STEP,20);ck('Real hit flash expires while stunned',p.evaluate('boss.flash<=0'))
  p.evaluate('()=>{boss._hammer.c25Knock.t=4.29;}');p.evaluate(STEP,3);r=p.evaluate('()=>({state:boss._hammer.state,empty:!!boss._hammer.c25Knock,destroyed:boss._hammer.hammerDestroyed})');ck('Magnetic catch restores the held weapon and combat without another heal',not r['empty'] and not r['destroyed'] and r['state']=='hammer',r)
  p.evaluate("()=>{seedC25();hammerState(boss,'hammer');fr27Restore(boss,.1,false,true);}")
  for i in range(10):p.evaluate(STEP,9);p.wait_for_timeout(2)
  r=p.evaluate("()=>({open:c25Counter(boss),head:hammerHeadPoint(boss),y:boss.y})");ck('Native recharge moves the raised hammer inside the visible counter window',r['open'] and r['head']['y']>=55,r)
  p.evaluate("()=>{window.c25MissileLog=[];const old=hammerBossDamage;hammerBossDamage=function(b,d){c25MissileLog.push({d,hit:b._hammerModuleHit,q:_dmgBullet?{kind:_dmgBullet.kind,x:_dmgBullet.x,y:_dmgBullet.y}:null,open:c25Counter(b)});return old.apply(this,arguments)};const at=hammerHeadPoint(boss);player.x=at.x;player.y=PLAY.y+PLAY.h-60;run.bombs=2;retina.target=null;window.c25Launch={result:useBomb(null),count:pBullets.length,ap:ap10Charging(),h3:h3Locked(),release:H3.release,dead:player.dead,bombs:run.bombs,shots:pBullets.map(b=>({kind:b.kind,x:b.x,y:b.y}))};window.c25RealRocket=pBullets[0];}")
  for i in range(12):p.evaluate(STEP,6);p.wait_for_timeout(2)
  r=p.evaluate("()=>({knock:!!boss._hammer.c25Knock,state:boss._hammer.state,events:C25.events.filter(e=>e.type==='raised-hammer-missile-counter').length,log:c25MissileLog,shots:pBullets.map(b=>({kind:b.kind,x:b.x,y:b.y,t:b.t})),head:hammerHeadPoint(boss),rocket:{dead:c25RealRocket?.dead,x:c25RealRocket?.x,y:c25RealRocket?.y,t:c25RealRocket?.t},launch:c25Launch,cp:CP12.events.slice(-10)})");ck('A real launched manual missile reaches the glowing hammer through the body lane',r['knock'] and r['events']>=2,r);p.screenshot(path=str(O/'actual-missile-counter.png'))
  p.evaluate('()=>{seedC25();boss._hammer.c25ArmorAtDeath=true;boss.dead=true;boss.dying=.8;drawWorld(0);}');r=p.evaluate('ha21Blue(boss)?.kind');ck('Death uses the same whole chromium kneeling identity','c25_empty_armor' in r,r);p.screenshot(path=str(O/'death.png'))
  r=p.evaluate("""()=>{seedC25();boss._hammer.state='giant_warn';boss._hammer.t=.3;const old=C25.base.warning;let warnings=0;C25.base.warning=function(){warnings++;return old.apply(this,arguments)};try{drawWorld(0)}finally{C25.base.warning=old}return warnings;}""");ck('Depth entry renders no FOV warnings',r==0,r)
  r=p.evaluate("""()=>{seedC25();boss._hammer.state='spell';boss._hammer.t=1;boss._hammer.spellTargets=[{x:220,y:400},{x:420,y:400}];const old=C25.base.warning;let n=0;C25.base.warning=function(o,q){if(o===boss&&q.fieldOnly)n++;return old.apply(this,arguments)};try{drawWorld(0)}finally{C25.base.warning=old}return n;}""");ck('Ordinary casting columns keep authored FOV lanes after ground reticles are removed',r>=2,r)
  r=p.evaluate("""()=>{seedC25();s5RunInit();s5run.gates[0].y=160;const calls=[],old=ctx.drawImage;ctx.drawImage=function(im,...a){const k=HA21.tags.get(im)||'';if(/portal|s5gate/i.test(k))calls.push(k);return old.call(this,im,...a)};try{drawWorld(0)}finally{ctx.drawImage=old}return calls;}""");ck('No route portal or foreground portal rim survives during the boss fight',not r,r)
  # Check the real armor sequence still visibly draws authored connecting bolts.
  r=p.evaluate("""()=>{seedC25();delete boss._hammer.frArmor;fr27BeginArmor(boss);boss._hammer.t=1.1;const calls=[],old=ctx.drawImage;ctx.drawImage=function(im,...a){const k=HA21.tags.get(im)||'';if(/hammer_lightning/.test(k))calls.push({key:k,args:a});return old.call(this,im,...a)};try{drawWorld(0)}finally{ctx.drawImage=old}return calls;}""");ck('Armor activation visibly conducts authored energy into the hammer and armor',len(r)>=3,r);p.screenshot(path=str(O/'activation.png'))
  r=p.evaluate("""()=>{const b=boss,active=bossActive,d=debugFight,w=warnKind;boss=null;bossActive=false;debugFight=null;warnKind=null;s5RunInit();s5run.gates[0].y=160;const calls=[],old=ctx.drawImage;ctx.drawImage=function(im,...a){const k=HA21.tags.get(im)||'';if(/portal|s5gate/i.test(k))calls.push(k);return old.call(this,im,...a)};try{drawWorld(0)}finally{ctx.drawImage=old;boss=b;bossActive=active;debugFight=d;warnKind=w}return calls;}""");ck('The authored Stage9 route portal still renders outside boss encounters',bool(r),r)
  p.evaluate("()=>{for(const d of [0,.00001,.1,.9,1,2])c25Bolt({x:300,y:200},{x:300+d,y:200},0,12,.7);}")
  ck('Coincident magnetic recall endpoints never draw a zero-size energy canvas',not errors,errors)
  ck('No page or console errors',not errors,errors);br.close()
finally:stop()
out=dict(checks=checks,errors=errors,passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks));(O/'contract-results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(passed=out['passed'],failed=out['failed'])),flush=True);raise SystemExit(0 if not out['failed'] else 1)
