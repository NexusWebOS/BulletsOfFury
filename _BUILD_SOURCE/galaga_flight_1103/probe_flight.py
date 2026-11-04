from pathlib import Path
import sys,json,ast,base64,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'));SETUP=next(ast.literal_eval(n.value)for n in t.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='SETUP'for x in n.targets))
inventory=json.loads((W/'inventory.json').read_text())['rows'];errors=[];checks=[];cases=[]
def check(ok,name):
 checks.append({'ok':bool(ok),'name':name})
 if not ok:print('FAIL '+name,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disk-cache-size=1','--media-cache-size=1'])
 p=b.new_page(viewport={'width':1280,'height':800})
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'))
 cdp=p.context.new_cdp_session(p);cdp.send('Network.enable');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
 p.on('pageerror',lambda e:(errors.append(str(e)),print('PAGE ERROR '+str(e)[:500],flush=True)));p.on('console',lambda m:errors.append(m.text[:250])if m.type=='error' or 'DRAW ERROR' in m.text else None)
 p.on('response',lambda r:print('HTTP '+str(r.status)+' '+r.url,flush=True)if r.status>=400 else None)
 p.on('requestfailed',lambda r:print('REQUESTFAIL '+r.url+' '+str(r.failure),flush=True))
 p.goto('http://127.0.0.1:65042/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=60000);p.evaluate(TRAP_RAF)
 if p.evaluate('typeof GF113==="undefined"'):p.add_script_tag(path=str(W/'galaga_flight_1103.js'))
 print('BOOT '+str(p.evaluate('({ph:typeof ph8Values,ui:typeof ui20Seat,GF:typeof GF113,errors:window.__bofDrawError})')),flush=True)
 stages=[int(x)for x in sys.argv[1:]] if len(sys.argv)>1 else list(range(1,10))
 for stage in stages:
  for diff in (['normal','hard','furious']if stage<=5 else ['hard','furious']):
   p.evaluate(SETUP,{'stage':stage,'diff':diff})
   p.evaluate('()=>{CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=999999;_adaptiveSpawnT=999999;tryAdaptiveReinforcement=()=>{};subBossDone=subBossTriggered=aminiTriggered=true;curStage={...curStage,length:99999};player.x=worldWidth()/2;player.y=VH-55;camX=player.x-VW/2;}')
   if stage in [5,9]:p.evaluate('()=>{run.spaceMode=true;gravityMode={...GRAVITY_SHIP_ACTIVE,narrative:false};furyShipWarm();}')
   p.evaluate('''s=>{const keys=new Set(),seen=new Set();function visit(v){if(!v||typeof v!=='object'||seen.has(v))return;seen.add(v);if(typeof v.key==='string'&&XART._src[v.key])keys.add(v.key);for(const x of Object.values(v))if(x&&typeof x==='object')visit(x);}const root={1:S1A_ART,2:V31_ART,3:I31_ART,4:S411_ART,5:S511_ART,6:S611_ART,7:S711_ART,8:S811_ART,9:S911_ART}[s];visit(root);for(const m of Object.values(R46_ART.models))if(m.stages?.includes(s))visit(m);window.qaFlightKeys=[...keys];for(const k of qaFlightKeys)XART.rdy(k);}''',stage)
   for warm in range(1200):
    ready=p.evaluate('()=>{stageLoadTick();return qaFlightKeys.every(k=>XART.rdy(k));}')
    if ready:break
    p.wait_for_timeout(25)
   if not ready:
    print('LOAD '+json.dumps(p.evaluate('(s)=>({n:s,L:_stageLoads[s]?{cursor:_stageLoads[s].cursor,total:_stageLoads[s].total,pending:_stageLoads[s].keys.filter(k=>!XART.rdy(k)).slice(0,50)}:null})',stage)),flush=True)
   assert ready,'Stage loading did not finish: '+str(stage)
   types=[q['request']for q in inventory if q['stage']==stage and not q.get('empty')]
   for typ in types:
    data=p.evaluate('''t=>{enemies=[];eBullets=[];pBullets=[];groundTargetingReset();GF113.groups=[];GF113.serial=0;GF113.events=[];S711.events=[];S811.events=[];S911.events=[];window.E=spawnEnemy(t,worldWidth()*.28,-190,{});if(!E?._gf113)return{type:t,stage:run.stage,skipped:true};window.FQ={type:t,stage:run.stage,diff:diffKey,initialHP:E.hp,size:E._gf113.size,trace:[],shots:0,maxStep:0,maxAngle:0,maxShots:0,maxBeams:0,firstVisible:null,last:{x:E.x,y:E.y,head:gf113Head(E)},bad:[],phases:[],model:gf113Model(E)};return FQ;}''',typ)
    if data.get('skipped'):continue
    # Real update/render owners at deterministic60Hz, yielding between batches.
    for batch in range(64):
     got=p.evaluate('''n=>{for(let i=0;i<n;i++){const dt=1/60;stateT+=dt;updatePlay(dt);if(E.dead)break;const A=E._gf113,step=Math.hypot(E.x-FQ.last.x,E.y-FQ.last.y),da=Math.abs(s1aAngle(gf113Head(E)-FQ.last.head));FQ.maxStep=Math.max(FQ.maxStep,step);FQ.maxAngle=Math.max(FQ.maxAngle,da);FQ.last={x:E.x,y:E.y,head:gf113Head(E)};if(!Number.isFinite(E.x+E.y+gf113Head(E)))FQ.bad.push('nonfinite');if(E.y>viewTopY()&&E.y<VH&&E.x>camLeftX()&&E.x<camRightX()&&FQ.firstVisible==null)FQ.firstVisible=A.age;FQ.maxShots=Math.max(FQ.maxShots,eBullets.length);FQ.maxBeams=Math.max(FQ.maxBeams,gf113State(E)?.beams?.length||0);if(!FQ.phases.includes(A.phase))FQ.phases.push(A.phase);}ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;drawWorld(0);FQ.trace.push({t:E._gf113.age,x:E.x,y:E.y,head:gf113Head(E),phase:E._gf113.phase,native:gf113State(E)?.phase,dead:E.dead,render:E._s911Rendered||E._s811Rendered||E._s711Rendered||E._s611Rendered||E._s511Rendered||E._s411Rendered||E._r46Rendered||{frame:E._air13Frame},shots:eBullets.length});return {dead:E.dead,phase:E._gf113.phase};}''',30)
     if diff=='furious' and typ==types[0] and batch in [11,27]:
      name=f'{stage}-{typ}-{batch}.png';raw=p.evaluate('cv.toDataURL()');(W/name).write_bytes(base64.b64decode(raw.split(',')[1]))
     p.wait_for_timeout(12)
     if got['dead']:break
    case=p.evaluate('()=>({...FQ,age:E._gf113.age,departed:!!E.dead,finalHP:E.hp,events:GF113.events,nativeEvents:[...S711.events,...S811.events,...S911.events]})');cases.append(case)
    label=f'{stage}/{typ}/{diff}'
    check(not case['bad'],label+' finite')
    check(case['firstVisible']is not None,label+' visible arrival')
    check(case['maxStep']<16,label+' continuous motion')
    check(case['finalHP']>=case['initialHP'],label+' native HP preserved without player fire (Stage1 applies native elite boost on first flight)')
    check(case['maxShots']>0 or case['maxBeams']>0 or any(q['event']=='spin' for q in case['nativeEvents']),label+' native attack release or authored depth-spin present')
    check(case['departed'],label+' finite departure')
    check('station' in case['phases'] or 'dive' in case['phases'],label+' loop reaches formation/dive')
    print(label+' '+str({k:case[k]for k in ['size','maxStep','maxAngle','maxShots','age','departed','phases']}),flush=True)
    (W/'probe-progress.json').write_text(json.dumps({'checks':checks,'cases':cases,'errors':errors},indent=2),encoding='utf8')
  print('STAGE COMPLETE '+str(stage),flush=True)
 b.close()
report={'checks':checks,'cases':cases,'errors':errors}
(W/('probe-'+('-'.join(map(str,stages)))+'.json')).write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({'checks':len(checks),'failed':sum(not q['ok']for q in checks),'cases':len(cases),'errors':errors}),flush=True)
