"""Real Chromium, native spawn/AI/collision/rendering. Isolated fixtures select
legal terrain; no actor HP, attack/flight timers are written after spawn."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/stage1_amplify_1031';W.mkdir(exist_ok=True);http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));errors=[];checks=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:600]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,5):
  e=p.evaluate(STEP,min(5,n-i));assert not e,e;p.wait_for_timeout(1)
SETUP="""([type,mode])=>{diffKey=mode;DIFF=difficultyForRun('arcade',mode);stagePlan=[];waveIdx=999;_adaptiveSpawnT=9999;spawnClock=9999;subBossDone=true;bossWarned=true;stageTimer=0;boss=null;subBoss=null;bossActive=subBossActive=false;enemies=[];eBullets=[];pBullets=[];powerups=[];playerLocks=[];groundTargetingFx=[];S1A.fx=[];S1A.events=[];S1A.draws={};_navalFlashes=[];player.invuln=1e9;player.dead=player.out=false;player.x=worldWidth()/2;player.y=VH-65;Input.keys.j=Input.keys.c=false;run.mode='campaign';debugFight=null;BOFCinematicDirector.cancel();setState(GS.PLAY);
 const heavy=type==='s1tankheavy';mapScroll=heavy?levelScrollRange()*.52:0;drawWorld(0);for(let i=0;i<6;i++){window.__bofStepNow=(window.__bofStepNow||performance.now())+1000/60;loop(window.__bofStepNow);}window.chosen={x:worldWidth()/2,y:heavy?160:100};
 if(heavy){let found=false;for(let y=110;y<260&&!found;y+=10)for(let x=70;x<worldWidth()-70;x+=10)if(groundTrafficLegal({x,y,w:103,h:103},x,y)){chosen={x,y};found=true;break;}if(!found)throw Error('No legal ground fixture');player.x=clamp(chosen.x+170,50,worldWidth()-50);}
 const y=type==='s1jetdelta'||type==='s1jetbomber'?viewTopY()-80:chosen.y;window.E=spawnEnemy(type,chosen.x,y,{route:'straight'});window.trace=[];window.firstShot=false;window.firstTurn=false;window.firstLate=false;
 if(typeof VP12!=='undefined')VP12.next=99999;if(typeof CP12!=='undefined')CP12.next=99999;
 return{type,x:E.x,y:E.y,w:E.w,h:E.h,hp:E.hp,atk:E._atk,naval:E._naval,initialPlayerX:player.x,chosen};}"""
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof S1A!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);s1mWarm();stageLoadBegin(1)}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(S1A_ART).every(a=>XART.rdy(a.key))&&XART.rdy("air13_s1_s1jetdelta_heading")}',timeout=180000)
  ck('Nine fixed even-cell banks preload with1089 directional frames',p.evaluate('Object.values(S1A_ART).length===9&&Object.values(S1A_ART).every(a=>a.cell%2===0&&a.pivot.every(v=>v===a.cell/2))&&Object.values(S1A_ART).reduce((s,a)=>s+a.dirs*a.frames,0)===1089'))
  summaries=[]
  for mode in ['normal','furious']:
   for kind in ['s1boatgun','s1corvette','s1jetdelta','s1jetbomber','s1tankheavy']:
    initial=p.evaluate(SETUP,[kind,mode]);print('FIXTURE',mode,initial,flush=True);rows=[];saved=False;turned=False;late=False
    for f in range(0,840,3):
     step(p,3)
     q=p.evaluate("()=>({t:E.t,x:E.x,y:E.y,dead:!!E.dead,hp:E.hp,flash:E.flash,angle:s1aPlaneHead(E),frame:E._air13Frame,phase:E._s1aFlight?.phase,shots:S1A.events.filter(q=>q.event==='shot').length,bombs:S1A.events.filter(q=>q.event==='bomb-drop').length,pairs:S1A.events.filter(q=>q.event==='tank-dual').length,locks:playerLocks.length,fx:S1A.fx.length,drop:E._fb9Bomber?.n,liveBombs:groundTargetingFx.filter(q=>q._s1aBomb&&!q.impact).length,draws:{...S1A.draws}})")
     rows.append(q)
     if not saved and(q['shots']or q['bombs']or q['pairs']):p.screenshot(path=str(W/(mode+'-'+kind+'-release.png')));saved=True
     if kind=='s1jetdelta'and not turned and q.get('frame',0)!=0 and q['t']>1:p.screenshot(path=str(W/(mode+'-delta-turn.png')));turned=True
     if kind=='s1jetbomber'and not late and q.get('drop',0)>8:p.screenshot(path=str(W/(mode+'-bomber-late-drop.png')));late=True
     if q['dead']:break
    events=p.evaluate('S1A.events');r=dict(mode=mode,type=kind,initial=initial,rows=rows,events=events);summaries.append(r)
    shots=[q for q in events if q['event']=='shot'];bombs=[q for q in events if q['event']=='bomb-drop'];pairs=[q for q in events if q['event']=='tank-dual']
    ck(mode+' '+kind+' executes its native attack',len(bombs)>0 if kind=='s1jetbomber'else len(shots)>0,dict(shots=len(shots),bombs=len(bombs),pairs=len(pairs),end=rows[-1]))
    if kind=='s1boatgun':
     ck(mode+' Gunboat fires only straight solid MG rounds',len(shots)>=3 and all(q['kind']=='s1bullet'and abs(q['angle']-1.5707963267948966)<.001 for q in shots),shots[:3])
     ck(mode+' Gunboat draws attached muzzle frames',rows[-1]['draws'].get('muzzle',0)>0)
    if kind=='s1corvette':ck(mode+' Corvette flashes use compact animated frames at the barrels',any(q['fx']>0 for q in rows)and rows[-1]['draws'].get('muzzle',0)>0)
    if kind=='s1jetdelta':
     frames={q.get('frame')for q in rows if q.get('frame')is not None};ck(mode+' Delta banks through actual directional frames and exits',len(frames)>=3 and rows[-1]['dead'],list(frames))
     ck(mode+' Delta has animated thrusters and muzzle flashes',rows[-1]['draws'].get('thruster',0)>50 and rows[-1]['draws'].get('muzzle',0)>0)
     moving=[(a,z)for a,z in zip(rows,rows[1:])if not z['dead']and a.get('phase')and z['t']>a['t']]
     speeds=[((z['x']-a['x'])**2+(z['y']-a['y'])**2)**.5/(z['t']-a['t'])for a,z in moving]
     ck(mode+' Delta flies with consistent forward airspeed',bool(speeds)and max(speeds)-min(speeds)<8,dict(low=min(speeds)if speeds else None,high=max(speeds)if speeds else None))
    if kind=='s1jetbomber':
     ck(mode+' Bomber keeps dropping through the lower screen',len(bombs)>=6 and any(q['y']>512*.68 for q in bombs),dict(count=len(bombs),last=bombs[-1]if bombs else None))
     ck(mode+' Falling authored bombs are visibly drawn and sortie exits',rows[-1]['draws'].get('bomb',0)>40 and rows[-1]['dead'])
    if kind=='s1tankheavy':
     ck(mode+' Heavy tank fires paired missiles from its two barrels',len(pairs)>0 and len([q for q in shots if q['kind']=='s1jungleMissile'])==len(pairs)*2,dict(pairs=len(pairs),shots=shots[:4]))
     ck(mode+' Tank attack works beyond the old120px player column',len(pairs)>0 and abs(initial['initialPlayerX']-initial['x'])>120)
     ck(mode+' Tank keeps native locks, directional turret and rocket flashes',any(q['locks']for q in rows)and rows[-1]['draws'].get('tank_turret',0)>0 and rows[-1]['draws'].get('rocket_muzzle',0)>0)
  (W/'native-events.json').write_text(json.dumps(summaries,indent=2))
  # Revised renderer uses cell selection only; never static-sprite rotation.
  p.evaluate(SETUP,['s1jetdelta','normal']);step(p,120)
  count=p.evaluate("()=>{const old=ctx.rotate;let n=0;ctx.rotate=function(){n++;return old.apply(this,arguments)};try{drawEnemy(E)}finally{ctx.rotate=old}return n;}");ck('Delta hull/exhaust rendering uses no runtime canvas rotation',count==0,count)
  # Actual native damaged pixels and expiry for the two custom render owners.
  for kind in ['s1jetdelta','s1tankheavy']:
   p.evaluate(SETUP,[kind,'normal']);step(p,90)
   colors=p.evaluate("()=>{const draw=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;},white=a=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>160&&a[i]>235&&a[i+1]>235&&a[i+2]>235)n++;return n;};E.flash=0;const clean=white(draw()),old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y,lv:1};hitEnemy(E,1);_dmgBullet=old;const hit=white(draw());window.__s1aPixelWhite=()=>white(draw());return{clean,hit};}")
   step(p,30);colors.update(p.evaluate('()=>({expired:__s1aPixelWhite(),flash:E.flash})'))
   ck(kind+' actual native pixels flash white then recover',colors['hit']>colors['clean']+20 and colors['expired']<colors['hit']*.5 and colors['flash']<=0,colors)
  r=p.evaluate("()=>{const e={x:240,y:100,type:'s1boatgun',hp:10,maxhp:10},a=s1aRound(e,{x:240,y:100,angle:Math.PI/2},4.5,'s1bullet',{silent:true}),m=s1aRound(e,{x:240,y:100,angle:Math.PI/2},3.05,'s1jungleMissile',{silent:true});return{bullet:enemyOrdnanceCanIntercept(a),missile:enemyOrdnanceCanIntercept(m),beforeUpdate:a.t===0};}")
  ck('Ordinary MG rounds resist interception before first update; missiles stay shootable',not r['bullet']and r['missile']and r['beforeUpdate'],r)
  ck('No page/console/render errors',not errors,errors);b.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
