from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_pilot_1115';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];checks=[]
def ck(n,v,data=None):
 checks.append(dict(name=n,ok=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,flush=True)
def step(p,n=6):
 q=p.evaluate(shoot.STEP,n)
 if q:raise RuntimeError(q)
 p.wait_for_timeout(1)
with sync_playwright()as pw:
 browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?water-pilot-qa=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 p.evaluate("()=>{BAL7.setup({stage:9,kind:'tidalfusion',pilot:'cole',diff:'normal',mode:'campaign',fire:false});player.invuln=999;DBGT.god=true;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;}")
 p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(9).ready&&Object.values(CB112_ART.banks).every(a=>XART.rdy(a.key))&&s911Keys().every(k=>XART.rdy(k));}',polling=50)
 ck('ship is stage9 first form',p.evaluate("boss?._w9p15?.phase==='ship'&&boss?._ship==='tidalsovereign'"))
 q=p.evaluate("()=>{const plan=buildStagePlan(9);return {tag:plan.some(w=>w._currentBreaker112),spawn:!!spawnEnemy('cbreak',320,100,{}),pending:currentBreakerPending112(),hp:boss.hp,max:boss.maxhp};}");ck('Current reserved for boss and no early progression hold',not q['tag']and not q['spawn']and not q['pending'],q)
 p.evaluate("()=>{window.rewardCount={award:0,mist:0,forge:0};const a=achievementEncounterDefeat,m=laserMistUnlock,f=forgeBossDrop;achievementEncounterDefeat=function(b,k){if(b===boss)rewardCount.award++;return a.apply(this,arguments)};laserMistUnlock=function(){rewardCount.mist++;return m.apply(this,arguments)};forgeBossDrop=function(){rewardCount.forge++;return f.apply(this,arguments)};boss._ts58.protected=false;boss._ts58.half=true;boss.enter=false;boss.x=worldWidth()/2;boss.y=boss._drawY=155;}")
 p.locator('#screen').screenshot(path=str(O/'ship.png'))
 q=p.evaluate("()=>{let n=0;while(boss._w9p15.phase==='ship'&&n++<1000){efxClock+=1/60;_lastHitX=boss.x;_lastHitY=boss.y;hitBoss(5000);}return {phase:boss._w9p15.phase,dead:boss.dead,defeated:bossDefeated,rewards:rewardCount,n};}")
 ck('native ship damage starts ejection without completion or rewards',q['phase']=='eject'and not q['dead']and not q['defeated']and not any(q['rewards'].values()),q)
 snapshots={}
 for i in range(45):
  step(p,6)
  if i in [2,9,18,29,40]:
   key='ejection-'+str(i);p.locator('#screen').screenshot(path=str(O/(key+'.png')));snapshots[key]=p.evaluate('({phase:boss._w9p15.phase,t:boss._w9p15.t,actor:boss._w9p15.actor&&{x:boss._w9p15.actor.x,y:boss._w9p15.actor.y,phase:boss._w9p15.actor._cb112.phase},hp:boss.hp,max:boss.maxhp})')
 q=p.evaluate("()=>{const b=boss,e=b._w9p15.actor;return{phase:b._w9p15.phase,hp:b.hp,max:b.maxhp,actorHP:e?.hp,inEnemies:enemies.includes(e),locks:_lockTargets().filter(t=>t._retinaOwner===b).length,space:spaceTargets().filter(t=>t._retinaOwner===b).length,x:e?.x,y:e?.y};}")
 ck('pilot is live boss with synchronized HP and Retina/space target',q['phase']=='pilot'and q['hp']==q['max']==q['actorHP']and not q['inEnemies']and q['locks']>0 and q['space']>0,q)
 q=p.evaluate("()=>{const e=boss._w9p15.actor,hp=e.hp;_lastHitX=e.x;_lastHitY=e.y;hitBoss(20);return{loss:hp-e.hp,flash:e.flash,host:boss.hp,actor:e.hp};}")
 ck('boss weapons damage and flash current body',q['loss']>0 and q['flash']>0 and q['host']==q['actor'],q);p.locator('#screen').screenshot(path=str(O/'pilot-hit.png'))
 phases={};
 for i in range(650):
  step(p,6);q=p.evaluate('({phase:boss._w9p15.actor._cb112.phase,cycles:boss._w9p15.cycles,hp:boss.hp,dead:boss.dead,defeated:bossDefeated,t:boss._w9p15.t})')
  if q['phase']not in phases:phases[q['phase']]=q;p.locator('#screen').screenshot(path=str(O/('pilot-'+q['phase']+'.png')))
  if q['cycles']>0 and q['phase']=='grenades':break
 ck('real boss retains water book and loops instead of fleeing',all(k in phases for k in ['grenades','flight-n','flight-s','marble','tidal','depth-spin'])and q['cycles']>0 and not q['dead']and not q['defeated'],{'phases':list(phases),'end':q})
 q=p.evaluate("()=>{const e=boss._w9p15.actor;cb112Set(e,'grenade-charge');e._cb112.t=0;const hp=e.hp,t=retinaBossTargets(boss)[0];retinaMissileDamage(t,45,{kind:'gmiss',_isMissile:true});return{loss:hp-e.hp,hp:boss.hp,actor:e.hp};}");ck('Retina missiles damage the real pilot pool',q['loss']>0 and q['hp']==q['actor'],q)
 q=p.evaluate("()=>{const e=boss._w9p15.actor;cb112Set(e,'depth-spin');const hp=e.hp;cb112Roller(e,{x:e.x,y:e.y+40,index:0,angle:Math.PI/2});cb112Weapon(CB112.balls.at(-1),{kind:'gmiss',dead:false});for(let i=0;i<50;i++)cb112Effects(1/60);return{loss:hp-e.hp,host:boss.hp,actor:e.hp};}");ck('physical missile roller counter reaches boss pool in depth',q['loss']>0 and q['host']==q['actor'],q)
 q=p.evaluate("()=>{const b=boss,e=b._w9p15.actor;cb112Set(e,'grenade-charge');let n=0;while(!b.dead&&n++<1000){efxClock+=1/60;hitBoss(5000);}return{dead:b.dead,defeated:bossDefeated,phase:b._w9p15.phase,rewards:rewardCount,hazards:eBullets.filter(q=>q._s911Owner===e&&!q.dead).length,n};}")
 ck('only pilot defeat ends boss and awards exactly once',q['dead']and q['defeated']and q['phase']=='defeat'and all(n==1 for n in q['rewards'].values())and q['hazards']==0,q)
 # Long native Freezer line with present cockpit art and original dialogue clock.
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.stage=1;run.pilot='freezer';diffKey='normal';const raw=PILOT_OPENINGS.axel.beats.find(b=>b.who==='freezer'),text=raw.text,readAt=.42;window.FREEZER_TEXT=text;window.FREEZER_ROW={id:'SCROLL-FREEZER',who:'FREEZER',text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people:['freezer','axel'],fpLocations:{freezer:'cockpit-sky',axel:'cockpit-sky'},duration:text.length/30+4,readings:[],_cueSet:new Set(),cm3:{group:'scroll-freezer',readAt,newStrip:true,baseDuration:text.length/30+4}};window.FREEZER_KEYS=d1110Keys([FREEZER_ROW]);d1110Ready(FREEZER_KEYS);}")
 p.wait_for_function('()=>d1110Ready(FREEZER_KEYS)',polling=50);p.evaluate("()=>{d1110Play('scroll-freezer-review',[FREEZER_ROW],()=>{});}")
 scroll=[]
 for i in range(105):
  step(p,6)
  if i%10==0:
   scroll.append(p.evaluate('DS15.last'));p.locator('#screen').screenshot(path=str(O/('freezer-scroll-'+str(i)+'.png')))
 valid=[s for s in scroll if s and s['text']==p.evaluate('FREEZER_TEXT')];ck('Freezer overflow scrolls to reveal final line inside original box',bool(valid)and max(s['offset']for s in valid)>0 and any(s['visible']and s['visible'][-1]['row']==len(s['rows'])-1 and s['budget']>=len(s['text'])for s in valid),{'samples':valid})
 ck('no page console or HTTP errors',not errors,errors);browser.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'snapshots':snapshots,'phases':phases,'scope':'Native prepared encounter tests, not unassisted campaign wins. Only ship/pilot health depletion uses scripted native damage. Full pilot arsenal advances at native clocks; dialogue uses exact retained Freezer text.'},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' checks passed',flush=True);assert all(c['ok']for c in checks)
