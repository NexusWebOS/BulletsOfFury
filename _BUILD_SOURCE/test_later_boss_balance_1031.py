from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'later-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:700]if not v else'',flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,9,errors)
  for rank,hp in [('hard',3960),('furious',4680)]:
   q=p.evaluate('''rank=>{run.stage=6;curStage=STAGES[5];diffKey=rank;DIFF=difficultyForRun('campaign',rank);run.ngplus=false;coopOn=false;spawnBoss('warhive');roster17Budget(boss);return{ace:boss._whv.aceMax,hp:boss.hp,max:boss.maxhp,parts:boss._carrier17.parts.map(p=>({hp:p.hp,max:p.maxhp})),core:boss._hc32.core};}''',rank)
   ck(rank+' has the intended Nightwing second-life health',q['ace']==hp,q)
   ck(rank+' carrier budget still equals every part plus its hull',q['hp']==q['max']==sum(x['max']for x in q['parts'])+q['core'] and all(x['hp']==x['max']for x in q['parts']),q)
  rows=[]
  for rank in ['hard','furious']:
   for mode in ['bullets','mortars','rain','lamp']:
    q=p.evaluate('''([rank,mode])=>{run.stage=9;curStage=STAGES[8];diffKey=rank;DIFF=difficultyForRun('campaign',rank);spawnBoss('tidalfusion');const b=boss,T=b._ts58;b.enter=false;T.protected=false;T.mode='recover';T.half=mode==='lamp';ts58Move(b,340,158);ts58ClearShots(b);TS58.events=[];window.rainCounter=0;const base=ts60LaunchRain;ts60LaunchRain=function(){rainCounter++;return base.apply(this,arguments);};ts58Set(b,mode);const warm=T.warm,live=T.live;for(let t=0;t<warm+live-.02;t+=1/60)ts58Tick(b,1/60);ts60LaunchRain=base;return{rank,mode,warm,live,slugs:eBullets.filter(q=>q._ts58Owner===b&&q._ts58==='slug').length,rain:rainCounter,lamps:TS58.events.filter(e=>e.event==='lamp-bubble').length};}''',[rank,mode]);rows.append(q)
  for mode,field in [('bullets','slugs'),('mortars','rain'),('rain','rain'),('lamp','lamps')]:
   a,b=[r for r in rows if r['mode']==mode];ck('Tidal '+mode+' is measurably lighter on Hard',0<a[field]<b[field],{'hard':a,'furious':b})
  p.evaluate("()=>{const b=boss,T=b._ts58;ts58Set(b,'slide');T.t=T.warm+2.31;ts58Tick(b,1/60);}");ck('Tidal offscreen re-entry is protected and cannot be targeted',p.evaluate('boss._ts58.protected&&retinaBossTargets(boss).length===0'))
  times=[]
  for rank in ['hard','furious']:
   times.append(p.evaluate("rank=>{diffKey=rank;ts58Set(boss,'tidal');return boss._ts58.warm;}",rank))
  ck('Both ranks preserve all three native water-wall beeps and their full tell',times[0]==times[1] and times[0]>2,times)
  p.evaluate("()=>{debugFight=null;diffKey='normal';run.mode='campaign';run.stage=5;run._normalComplete100={version:1,phase:'settled',mode:'campaign'};nf100Open(false,true);nf100Choose(0);}")
  for i in range(12):p.evaluate(STEP,12)
  p.evaluate('startRun(1)')
  ck('Actual fresh Hard operation resets progression without losing Normal archive',p.evaluate('diffKey==="hard"&&run.stage===1&&run.mode==="campaign"&&Object.keys(campaign.rank).length===0'))
  ck('No runtime errors in later balance tests',not errors,errors)
  br.close()
finally:stop()
(W/'tidal-profiles.json').write_text(json.dumps(rows,indent=2));print('RESULT',len(checks),'passed',flush=True)
