"""Native physical weapons/AI checks and source-pixel captures in Chromium."""
from pathlib import Path
import json,sys,ast,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/stage1_followup_1031';W.mkdir(exist_ok=True);port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];rows=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:400]if not v else'',flush=True)
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
  for mode in ['normal','hard','furious']:
   for kind in ['s1boatpatrol','s1corvette','s1tankheavy','s1tankapc','s1tanklight','s1jetdelta_b','s1jetbomber','s1truckmissile','modturret-missile','modturret-mg']:
    if mode=='normal'and kind=='s1tanklight':continue
    setup=p.evaluate(SETUP,[kind,mode]);print('START',mode,kind,setup,flush=True);saved=False;trace=[]
    for f in range(0,1080,5):
     step(p,5);q=p.evaluate("()=>({t:E.t,x:E.x,y:E.y,dead:!!E.dead,shots:S1A.events.filter(a=>a.event==='shot').length,bombs:S1A.events.filter(a=>a.event==='bomb-drop').length,fx:S1A.fx.length,heading:E._air13Frame,phase:E._s1bNavy?.mode,burst:E._s1bMG?.left,ground:E._modTurret?.mode,truck:MT18.shots})");trace.append(q)
     if not saved and(q['shots']>0 or q['bombs']>0 or kind=='s1truckmissile'and p.evaluate('eBullets.some(b=>b._mt18Missile)')):p.screenshot(path=str(W/(mode+'-'+kind+'-release.png')));saved=True
     if q['dead']:break
    events=p.evaluate('S1A.events');own=p.evaluate('S1B.events');shots=[a for a in events if a['event']=='shot'];rows.append(dict(mode=mode,type=kind,events=events,own=own,trace=trace))
    count=len([a for a in events if a['event']=='bomb-drop'])if kind=='s1jetbomber'else len(shots)if kind!='s1truckmissile'else trace[-1]['truck']
    ck(mode+' '+kind+' fires its physical attack',count>0,dict(count=count,trace=trace[-1],own=own[-3:]))
    if kind=='s1boatpatrol':ck(mode+' Patrol cycles both side spreads and main rapid burst',{a.get('side')for a in own if a['event']=='side-spread'}=={-1,1}and any(a['event']=='main-burst'for a in own),own)
    if kind=='s1corvette':ck(mode+' Corvette fires straight from the actual central cannon',bool(shots)and all(abs(a['angle']-1.5707963267948966)<.001 for a in shots)and len({round(a['x'])for a in shots})<3,shots[:4])
    if kind in ['s1tankapc','s1tanklight','modturret-mg','modturret-missile']:
     ck(mode+' '+kind+' releases two physical mouths per volley',len(shots)>=2 and len(shots)%2==0 and abs(shots[0]['x']-shots[1]['x'])>.5,shots[:2])
    if kind=='s1jetdelta_b':ck(mode+' Strike fighter uses turning frames and exits',len({q.get('heading')for q in trace if q.get('heading')is not None})>=3 and trace[-1]['dead'])
    if kind=='s1jetdelta_b':ck(mode+' Strike fighter preserves native difficulty HP',p.evaluate('E.maxhp')==p.evaluate('hp=>Math.ceil(hp*(S1_JET_ELITE[diffKey]?.hp||1))',setup['hp']))
  p.evaluate("()=>{spawnEnemy=window.s1bProbeSpawn;run.stage=1;diffKey='normal';}");ck('Black-camo light tank cannot spawn on Normal',p.evaluate("spawnEnemy('s1tanklight',300,100,{})===null&&spawnEnemy('s1tanklight_b',300,100,{})===null"))
  ck('Black-camo light tank is restricted to Hard/Furious only',p.evaluate("()=>['easy','normal','insanity'].every(k=>{diffKey=k;return spawnEnemy('s1tanklight',300,100,{})===null&&buildStagePlan(1).every(w=>!w.fn._s1bCamo)})"))
  counts=p.evaluate("()=>Object.fromEntries(['normal','hard','furious'].map(k=>{diffKey=k;DIFF=difficultyForRun('arcade',k);return[k,buildStagePlan(1).filter(w=>w.fn._s1bCamo).length]}))");ck('Hard has extra camo waves; Furious has more across the route',counts['normal']==0 and counts['hard']==5 and counts['furious']==8,counts)
  cadence={r['mode']:[e['at']for e in r['events']if e['event']=='tank-dual']for r in rows if r['type']=='s1tankheavy'}
  gaps={k:sum(z-a for a,z in zip(v,v[1:]))/max(1,len(v)-1)for k,v in cadence.items()};ck('Heavy tank real salvo intervals shorten on Hard, shortest on Furious',0<gaps['furious']<gaps['hard']<gaps['normal'],dict(gaps=gaps,releases=cadence))
  for kind in ['s1tanklight','s1tankapc','s1jetdelta_b','modturret-mg','modturret-missile']:
   p.evaluate(SETUP,[kind,'hard']);step(p,75)
   c=p.evaluate("()=>{window.pixelCount=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const d=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i+3]>160&&d[i]>235&&d[i+1]>235&&d[i+2]>235)n++;return n};const clean=pixelCount();hitEnemy(E,.1);return{clean,hit:pixelCount()};}");step(p,30);c.update(p.evaluate('()=>({expired:pixelCount(),flash:E.flash})'));ck(kind+' native damaged pixels flash and expire',c['hit']>c['clean']+10 and c['expired']<c['hit']*.6 and c['flash']<=0,c)
   n=p.evaluate('()=>{const old=ctx.rotate;let n=0;ctx.rotate=function(){n++;return old.apply(this,arguments)};try{drawEnemy(E)}finally{ctx.rotate=old}return n}');ck(kind+' body/head select cells without canvas rotation',n==0,n)
  r=p.evaluate("()=>{const e={x:200,y:100,type:'s1tanklight',hp:10},b=s1aRound(e,{x:200,y:100,angle:Math.PI/2},5,'s1bullet',{silent:true}),m=s1aRound(e,{x:200,y:100,angle:Math.PI/2},3,'s1jungleMissile',{silent:true});return{bullet:enemyOrdnanceCanIntercept(b),missile:enemyOrdnanceCanIntercept(m),before:b.t===0}}")
  ck('Ordinary rounds remain unshootable before update; physical missiles shootable',not r['bullet']and r['missile']and r['before'],r)
  ck('No page/console/render errors',not errors,errors);b.close()
finally:stop();(W/'native-events.json').write_text(json.dumps(rows,indent=2))
print('RESULT',sum(a['passed']for a in checks),'/',len(checks));assert all(a['passed']for a in checks)
