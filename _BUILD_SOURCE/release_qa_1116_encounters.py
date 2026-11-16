from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/encounters';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];rows=[]
SNAP="""role=>{const b=role==='boss'?boss:subBoss;if(!b)return {state,stage:run.stage,missing:true};const phases={};for(const[k,v]of Object.entries(b)){if(v&&typeof v==='object'&&!Array.isArray(v)){const q={};for(const[n,a]of Object.entries(v))if(/phase|mode|attack|state|stage/.test(n)&&['string','number','boolean'].includes(typeof a))q[n]=a;if(Object.keys(q).length)phases[k]=q;}}return {state,stage:run.stage,curStage:STAGES.indexOf(curStage)+1,kind:b.kind,ship:b._ship||null,hp:b.hp,max:b.maxhp,enter:b.enter,dead:b.dead,x:b.x,y:b.y,player:{x:player.x,y:player.y,dead:player.dead},phases,bullets:eBullets.filter(q=>!q.dead).length,kinds:[...new Set(eBullets.filter(q=>!q.dead).map(q=>q.kind||q.type||'standard'))],finite:[b.x,b.y,b.hp,player.x,player.y,camX].every(Number.isFinite),scene:BOFCinematicDirector.current?.id||null,clock:stageTimer,view:[viewZoom(),viewW(),viewH()]};}"""
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-encounters=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')
 for diff in ['normal','hard','furious']:
  for stage in range(1,6 if diff=='normal'else 10):
   for role in ['mini','boss']:
    ident=f'{diff}-s{stage}-{role}';e0=len(errors);start=time.monotonic();row={'id':ident,'difficulty':diff,'stage':stage,'role':role,'scope':'Native developer encounter start/warnings, stationary protected Cole, default primary held for 30 simulated seconds. No campaign win or full-pattern/balance certification.','samples':[]}
    try:
     p.evaluate("q=>{BOSSMODE.start(q.stage,q.role,'cole',false,q.diff);player.invuln=1e8;player._spawnClearT=1e8;playerHit._q=0;run.lives=30;}",{'stage':stage,'role':role,'diff':diff})
     p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50)
     p.evaluate("()=>{const k=keybindFor(1).fire.find(k=>!k.startsWith('mouse'));window.QA16Fire=k||'j';Input.keys[QA16Fire]=true;}")
     for i in range(60):
      e=p.evaluate(shoot.STEP,30)
      if e:raise RuntimeError(e)
      p.wait_for_timeout(1)
      if i%5==0 or i==59:
       s=p.evaluate(SNAP,role);s['at']=(i+1)*.5;row['samples'].append(s)
      if i in [19,59]:
       p.evaluate('()=>SC12.refresh()');p.screenshot(path=str(O/f'{ident}-{i}.jpg'),type='jpeg',quality=83)
     p.evaluate('()=>{Input.keys[QA16Fire]=false;}')
     living=[s for s in row['samples']if not s.get('missing')]
     row['checks']={'nativeActorAppears':bool(living),'correctStage':all(s['stage']==stage and s['curStage']==stage for s in living),'finiteState':all(s.get('finite')for s in living),'playerSurvivesFixture':all(not s['player']['dead']for s in living),'noBrowserErrors':len(errors)==e0}
     row['peakProjectiles']=max([s.get('bullets',0)for s in living]or[0]);row['observedKinds']=sorted(set(k for s in living for k in s.get('kinds',[])));row['errors']=errors[e0:]
    except Exception as e:row['exception']=str(e)
    row['seconds']=round(time.monotonic()-start,2);rows.append(row)
    (O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Prepared encounter smoke coverage, not full campaign or unassisted fight wins.'},indent=2),encoding='utf8')
    print(json.dumps({k:row[k]for k in ['id','checks','peakProjectiles','seconds','exception']if k in row}),flush=True)
 b.close()
