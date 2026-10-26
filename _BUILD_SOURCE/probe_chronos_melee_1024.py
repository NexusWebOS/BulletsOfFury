"""Native collision and pixel checkpoints for Furious melee; not the play recording."""
from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_melee_1024';O.mkdir(exist_ok=True)
checks=[];errors=[];cases=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("""()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();}""")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()}',timeout=180000)
  p.evaluate("""()=>{window.meleeHits=[];window.meleeCalls=[];window.meleeCues=[];const hit=b20HitSegment,cue=b20Cue;b20HitSegment=function(b,a,z,r,label,set){const q=ha21Blue(b);const head=q?.a?.tip?hb20World(q.a,q.a.tip,b,q.k,q.rot):null;const before=B20.events.length;const result=hit.apply(this,arguments);if(b===boss){const item={clock:b._hammer._hj22Pair?.clock,label,distance:s81003Distance(player.x,player.y,{x:a.x,y:a.y,ex:z.x,ey:z.y}),r,head,to:{...z},accepted:B20.events.slice(before).some(e=>e.kind==='contact'&&e.label===label)};meleeCalls.push(item);if(item.accepted)meleeHits.push(item);}return result;};b20Cue=function(key){meleeCues.push({key,clock:boss?._hammer?._hj22Pair?.clock});return cue.apply(this,arguments);};}""")
  for scenario in ['slam','left','right','dodge-left']:
   p.evaluate("""()=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.flash=0;b.hp=b.maxhp=11220;b.x=340;b.y=230;h.balance0922=true;h.state='recover';h.t=0;h.followCount=5;h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=null;h.hammerDestroyed=false;delete h.er23DepthCombo;delete h._hf22StormPair;h.frArmor={hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]};player.reset();player.x=220;player.y=420;player.invuln=0;run.shield=3;DBGT.god=false;eBullets=[];pBullets=[];l5Rocks=[];meleeHits.length=meleeCalls.length=meleeCues.length=0;B20.events.length=0;h._hj22Pair=hj22Pair(b,'blue',{x:80,y:160});window.testPair=h._hj22Pair;}""")
   frames=[];moved1=moved2=False;shots=set()
   for frame in range(150):
    clock=p.evaluate('testPair.clock')
    if scenario!='slam' and clock>=.20 and not moved1:
     moved1=True;p.evaluate('()=>{player.x=390;player.y=410;}')
    if scenario in ['right','dodge-left'] and clock>=.95 and not moved2:
     moved2=True;p.evaluate("kind=>{player.x=kind==='right'?150:390;player.y=kind==='right'?415:80;}",scenario)
    p.evaluate(STEP,1)
    r=p.evaluate('()=>({clock:testPair.clock,state:boss._hammer.state,frame:ha21Blue(boss)?.a.key,shield:run.shield,hits:meleeHits.length,left:testPair.leftAim,right:testPair.rightAim,target:testPair.target})');frames.append(r)
    if scenario=='left':
     for label,at in [('green',.81),('yellow',.99),('red',1.14),('contact',1.22)]:
      if r['clock']>=at and label not in shots:shots.add(label);p.screenshot(path=str(O/('left-'+label+'.png')))
    if r['clock']>=2.15 or r['state']!='recover' or scenario=='dodge-left' and r['clock']>=1.33:break
    if frame%12==0:p.wait_for_timeout(5)
   data=p.evaluate('()=>({hits:meleeHits,calls:meleeCalls,cues:meleeCues,shield:run.shield,target:testPair.target,left:testPair.leftAim,right:testPair.rightAim,duration:hf22PairDuration(testPair)})')
   label={'slam':'second downward slam','left':'left sweep','right':'right sweep'}.get(scenario)
   if label:ck(scenario+' actually damages a ship in the authored hammer path',any(label in q['label'] and q['accepted'] for q in data['hits']) and data['shield']<3,data)
   else:ck('Moving out of the committed warning lets the player evade',not data['hits'] and data['shield']==3,data)
   if scenario=='slam':ck('Second slam targets the current player instead of the first impact',data['target']=={'x':220,'y':420},data['target'])
   side=[q for q in data['calls'] if 'sweep' in q['label']]
   ck(scenario+' collision endpoints match the actually rendered hammer',bool(side) and all(q['head'] and abs(q['head']['x']-q['to']['x'])<.01 and abs(q['head']['y']-q['to']['y'])<.01 for q in side),dict(samples=len(side)))
   if scenario=='left':
    ck('Side-swing warning commits its aim instead of following the player',len({json.dumps(f.get('left'),sort_keys=True) for f in frames if f.get('left')})==1,data['left'])
    ck('Native Furious combo completes faster with both side cues retained',data['duration']==2.18 and [q['key'] for q in data['cues']].count('hammerThrow')==2,data['cues'])
   cases.append(dict(scenario=scenario,frames=frames,data=data))
  # Fixed-bank scale/flash still uses actual native body pixels.
  r=p.evaluate("""()=>{boss._noHit=false;boss.flash=0;for(const p of boss.parts||[])p.flash=0;drawWorld(0);const before=ctx.getImageData(0,0,cv.width,cv.height).data;hitBoss(1);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<after.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;return{white,flash:boss.flash};}""")
  ck('Boss retains actual white damaged pixels during the moving combo',r['white']>100 and r['flash']>0,r)
  p.evaluate(STEP,18);r=p.evaluate('boss.flash');ck('Native boss hit flash expires',r<=0,r)
  # Shared Stage8 and lower-difficulty timings retain their original owner.
  r=p.evaluate("""()=>{diffKey='hard';const hard=hj22Pair(boss,'blue',{x:200,y:300});diffKey='furious';const corrupt=hj22Pair(boss,'corrupt',{x:200,y:300});return{hard:hf22PairDuration(hard),corrupt:hf22PairDuration(corrupt)};}""")
  ck('Hard and corrupted-hammer cadence stay unchanged',r=={'hard':1.72,'corrupt':3.55},r)
  ck('No page or console errors',not errors,errors);br.close()
finally:stop()
out=dict(checks=checks,cases=cases,errors=errors,passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks));(O/'contact-results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(passed=out['passed'],failed=out['failed'])),flush=True);raise SystemExit(0 if not out['failed'] else 1)
