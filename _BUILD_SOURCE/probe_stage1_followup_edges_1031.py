"""Native physical weapons/AI checks and source-pixel captures in Chromium."""
from pathlib import Path
import json,sys,ast,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/stage1_followup_1031';W.mkdir(exist_ok=True);port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];rows=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'edge-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:400]if not v else'',flush=True)
from stage1_followup_fixture_1031 import SETUP
def step(p,n):
 for i in range(0,n,5):assert not p.evaluate(STEP,min(5,n-i));p.wait_for_timeout(1)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof S1B!=="undefined"');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(1);}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(S1B_ART).every(a=>XART.rdy(a.key))&&Object.values(S1A_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  ck('All physical source banks have even cells, fixed pivots and preload',p.evaluate('Object.values(S1B_ART).every(a=>a.cell%2===0&&a.pivot[0]===a.cell/2&&a.pivot[1]===a.cell/2)'))
  for route in ['cornerLR','cornerRL']:
   fixture=SETUP.replace("route:'straight'","route:'"+route+"'")
   p.evaluate(fixture,['s1jetdelta_b','hard']);x0=p.evaluate('E.x');seen=[]
   for i in range(150):
    step(p,5);seen.append(p.evaluate('({x:E.x,y:E.y,dead:E.dead,head:E._air13Frame})'))
    if seen[-1]['dead']:break
   dx=seen[-1]['x']-x0;ck(route+' Strike Fighter follows its chosen arc and exits',seen[-1]['dead'] and(dx>40 if route=='cornerLR'else dx< -40)and len({q['head']for q in seen})>2,dict(dx=dx,final=seen[-1]))
  p.evaluate(SETUP,['s1boatpatrol','hard']);step(p,45)
  info=p.evaluate("()=>{const a=E._s1bNavy,m=a.module,pos=furyBoatPoint(E,m);furyBoatModuleDamage(E,999,pos);return{before:a.mode,hp:m.hp};}");step(p,3)
  info.update(p.evaluate("({after:E._s1bNavy.mode,shots:S1A.events.filter(e=>e.event==='shot').length})"));ck('Destroyed Patrol side module immediately cancels its tell and rounds',info['hp']==0 and info['before']=='tell'and info['after']=='wait'and info['shots']==0,info)
  for stage in [4,6,7]:
   for weapon in ['mg','missile']:
    p.evaluate(SETUP,['modturret-'+weapon,'hard']);p.evaluate('s=>{run.stage=s;E._modTurret.stage=s;XART.rdy("overhaul_ground_base_"+s);}',stage)
    p.wait_for_function('XART.rdy("overhaul_ground_base_"+run.stage)')
    for i in range(50):step(p,5)
    hits=p.evaluate('S1A.events.filter(e=>e.event==="shot")');ck('Stage'+str(stage)+' shared '+weapon+' emplacement emits twin mouths',len(hits)>=2 and len(hits)%2==0 and abs(hits[0]['x']-hits[1]['x'])>1,hits[:2])
    p.evaluate('run.stage=1')
  p.evaluate(SETUP,['s1tanklight','hard'])
  r=p.evaluate("""()=>{spawnEnemy=window.s1bProbeSpawn;enemies=[];const plan=buildStagePlan(1),waves=plan.filter(q=>q.fn._s1bCamo);let found=false;
   for(let f=.3;f<.8&&!found;f+=.02){mapScroll=levelScrollRange()*f;if(((_levelCfg(1)?.h||4212)-mapScroll)>S1_COAST-60)continue;for(let x=70;x<worldWidth()-70;x+=14)if(groundTrafficLegal({w:88,h:88,_drawW:93,_drawH:93},x,viewTopY()-92)){found=true;break;}}
   if(!found)return{found};waves[0].fn();waves[1].fn();const a=enemies.filter(e=>e._s1bReinforcement);return{found,count:a.length,separate:a.every((e,i)=>a.slice(i+1).every(o=>!groundTrafficTouch(e,o))),pos:a.map(e=>({x:e.x,y:e.y}))};}""")
  ck('Additional camo waves spawn through native terrain/traffic reservations',r.get('found')and r.get('count')==2 and r.get('separate'),r)
  r=p.evaluate("()=>{enemies=[];mapScroll=0;const w=buildStagePlan(1).find(q=>q.fn._s1bCamo);waveIdx=20;w.fn();return{count:enemies.length,queued:waveIdx===19};}");ck('Camo reinforcements wait when their arrival row is water',r['count']==0 and r['queued'],r)
  r=p.evaluate("()=>{run.stage=1;return ['s1tankheavy','s1tankapc','s1tanklight','s1truckmissile','sandtank','roadtank','s7tank'].map(type=>{const e={type,hp:10,_tank:true,_modTank:1};return{type,owns:eb11OwnsRoute(e)}});}")
  ck('Native ground vehicle owners reject the generic age-based aircraft push',all(q['owns']for q in r),r)
  ck('No edge-case browser errors',not errors,errors);b.close()
finally:stop()
print('RESULT',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
