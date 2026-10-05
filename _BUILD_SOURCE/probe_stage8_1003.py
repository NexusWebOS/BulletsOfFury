"""Real Chromium motion/render checks; isolated encounters, not campaign wins."""
from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_1003';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];report={'checks':[],'scenes':[],'limitations':'Controlled native encounter fixtures; not completed campaign runs.'}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('OK ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(10)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
def knight(p,d):
 p.evaluate(SETUP,{'stage':8,'diff':d,'kind':'vileexistence'})
 p.evaluate('()=>{r30Form(B,1);B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);window.seen1003=[];}')
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50);p.mouse.click(500,500)
  p.evaluate('()=>{s81003Warm();r30Warm();}')
  p.wait_for_function('()=>Object.values(S81003_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000,polling=50)
  ck(p.evaluate('()=>Object.values(S81003_ART).every(a=>XART.get(a.key).width===a.cw*a.cols)'),'all generated sheets load at registered dimensions')
  for d in ['normal','hard','furious']:
   knight(p,d)
   for i in range(0,780,6):
    phase=p.evaluate('()=>B._r30.attack?.k1003?.phase||"finished"')
    if phase=='finished':break
    if phase not in report.get('captured_'+d,[]):
     report.setdefault('captured_'+d,[]).append(phase)
     if d=='normal':shot(p,'knight-'+phase)
    frames(p,6)
   ck(p.evaluate('()=>["guard","slash","jump","land","sweep","recover","out","in"].every(k=>B._r30.history.some(h=>h.phase===k))'),'native complete knight sequence '+d)
   ck(p.evaluate('()=>Number.isFinite(B.hp)&&B.hp>0&&state===GS.PLAY'),'knight remains live and finite '+d)
   knight(p,d);frames(p,83);shot(p,'binary-wall-'+d)
   r=p.evaluate('()=>{const q=r30ShieldBounds(B),hp=B.hp,s=B._r30.shield;bossHitTest(q.x+q.w*.46,q.y+q.h*.46);hitBoss(7);return{corner:B._lastPart?.id==="shield",hp:B.hp===hp,shield:B._r30.shield<s,w:q.w,h:q.h};}')
   ck(r['corner'] and r['hp'] and r['shield'],'visible rectangular wall absorbs native boss-hit route '+d)
   p.evaluate('()=>{B._r30.shield=0;s81003KnightEnter(B,"recover");B._r30.attack.k1003.x=player.x;B._r30.attack.k1003.y=150;window.hp1003=B.hp;run.bombs=20;run.missileTier="standard";window.lock1003=retinaBossTargets(B)[0];window.missile1003=useBomb(lock1003);}')
   frames(p,75)
   ck(p.evaluate('()=>missile1003&&B.hp<hp1003'),'actual Retina missile damages exposed animated knight '+d)
   for type in ['s8leech','s8hunter','s8solar']:
    p.evaluate(SETUP,{'stage':8,'diff':d});p.evaluate('(type)=>{window.E=spawnEnemy(type,player.x,80,{});window.last1003={x:E.x,y:E.y};window.maxStep1003=0;window.peak1003=0;window.orbs1003=0;window.phases1003=[];}',type)
    for j in range(28):
     frames(p,24,'updatePlay(1/60);maxStep1003=Math.max(maxStep1003,Math.hypot(E.x-last1003.x,E.y-last1003.y));last1003={x:E.x,y:E.y};peak1003=Math.max(peak1003,S81003.beams.length);orbs1003=Math.max(orbs1003,eBullets.filter(q=>q._alienOrb1003).length);drawWorld(1/60);')
     phase=p.evaluate('()=>E._orbit1003.phase')
     if phase in ['tell','fire'] and phase not in p.evaluate('()=>phases1003'):
      shot(p,type+'-'+d+'-'+phase);p.evaluate('(v)=>phases1003.push(v)',phase)
    r=p.evaluate('()=>({role:E._alien1003,max:maxStep1003,peak:peak1003,orbs:orbs1003,finite:Number.isFinite(E.x+E.y),angle:E.spin})');report['scenes'].append({'diff':d,**r})
    ck(r['finite'] and r['max']<3 and r['angle']==0,'native orbit stays smooth and hull straight '+type+' '+d)
    ck((r['orbs']>0 if type=='s8leech' else r['peak']>0),'native alien attack actually releases '+type+' '+d)
   # Actual campaign plan callbacks, no synthetic new waves.
   p.evaluate(SETUP,{'stage':8,'diff':d});r=p.evaluate('()=>{enemies=[];const plan=buildStagePlan(8);for(const v of plan){const f=v.f||v.fn||v.spawn;if(typeof f==="function")f();}return{keys:Object.keys(plan[0]),roles:[...new Set(enemies.map(e=>e._alien1003).filter(Boolean))]};}')
   report.setdefault('waves',[]).append(r)
   ck(len(r['roles'])==3,'all three new designs appear in actual Stage8 plan '+d)
  # Mid-fight transformation and full colossus wall.
  knight(p,'normal');p.evaluate('()=>{r30Form(B,2);B._r30.fx=[];B._r30.mode="fight";B.enter=false;B._r30.shield=B._r30.shieldMax=90;B._r30.wallAge1003=2;B._r30.cd=999;}');shot(p,'colossus-full-wall')
  p.evaluate('()=>{B._r30.shield=0;B._r30.seq=9;r30Attack(B);}');frames(p,20);shot(p,'form-transformation')
  # Native damage pipeline: a warning is harmless; the committed live beam hits.
  p.evaluate(SETUP,{'stage':8,'diff':'normal'})
  p.evaluate('()=>{window.E=spawnEnemy("s8prism1003",player.x,130,{});const A=E._orbit1003;A.phase="tell";A.age=0;A.warm=1.3;A.lanes=s81003EnemyLanes(E,A);player.invuln=0;run.shield=0;window.hitCalls1003=0;window.hitBase1003=playerHit;playerHit=function(){hitCalls1003++;return hitBase1003.apply(this,arguments);};}')
  frames(p,65);ck(p.evaluate('()=>hitCalls1003===0&&!player.dead'),'new FOV warning does not damage the player')
  frames(p,25);ck(p.evaluate('()=>hitCalls1003>0&&(player.dead||player.invuln>0)'),'live code beam uses native player-hit pipeline')
  p.evaluate('()=>{playerHit=hitBase1003;}')
  p.evaluate(SETUP,{'stage':8,'diff':'normal'})
  p.evaluate('()=>{window.E=spawnEnemy("s8prism1003",player.x,130,{});const A=E._orbit1003;A.phase="tell";A.age=.55;A.warm=1.3;A.lanes=s81003EnemyLanes(E,A);A.locked=true;window.beforeLane1003=JSON.stringify(A.lanes);player.x+=125;player.invuln=0;run.shield=0;}')
  frames(p,65);ck(p.evaluate('()=>JSON.stringify(E._orbit1003.lanes)===beforeLane1003&&!player.dead'),'moving after lock escapes the beam without retargeting')
  p.evaluate('()=>{for(let i=0;i<4&&!E.dead&&E._dyingT==null;i++)hitEnemy(E,1e6);}')
  report['emitterKill']=p.evaluate('()=>({hp:E.hp,dead:!!E.dead,dying:E._dyingT,shield:E._esh,beams:S81003.beams.length})')
  frames(p,2);ck(p.evaluate('()=>(E.dead||E._dyingT!=null||E.hp<=0)&&S81003.beams.length===0'),'killing an emitter removes its beam in native combat')
  p.evaluate(SETUP,{'stage':8,'diff':'normal','kind':'vileexistence'})
  p.evaluate('()=>{r30Form(B,0);B._r30.mode="fight";B.enter=false;B._r30.seq=3;r30Attack(B);B._r30.fx=[];}');frames(p,50);shot(p,'boss-code-lance-warning');frames(p,39);shot(p,'boss-code-lance-live')
  ck(p.evaluate('()=>S81003.beams.some(q=>q.owner===B&&q.kind==="code")'),'possessed host fires generated paired code lasers')
  knight(p,'normal');frames(p,83)
  p.evaluate('()=>{B._lastPart={id:"shield"};window.shatterHP1003=B.hp;modularHit(5);}');frames(p,6);shot(p,'shield-impact')
  p.evaluate('()=>{window.shatterOrigin1003=r30ShieldBounds(B);B._lastPart={id:"shield"};modularHit(1e6);}')
  ck(p.evaluate('()=>S81003.effects.filter(f=>f.kind==="shards").length===16&&B.hp===shatterHP1003'),'native shield break emits 16 harmless generated shards')
  frames(p,12);shot(p,'shield-shatter');frames(p,24);shot(p,'shield-shards-outward')
  ck(p.evaluate('()=>{const a=S81003.effects.filter(f=>f.kind==="shards"),q=shatterOrigin1003;return a.some(f=>f.x<q.x-q.w*.5)&&a.some(f=>f.x>q.x+q.w*.5)&&a.some(f=>f.y<q.y-q.h*.5)&&a.some(f=>f.y>q.y+q.h*.5); }'),'shards travel beyond all four shield edges')
  # A controlled real-canvas motion recording of the complete combo and three emitters.
  knight(p,'hard');p.evaluate('()=>{window.recChunks1003=[];window.rec1003=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1800000});rec1003.ondataavailable=e=>{if(e.data.size)recChunks1003.push(e.data);};rec1003.start();}')
  for i in range(300):frames(p,2);p.wait_for_timeout(21)
  p.evaluate(SETUP,{'stage':8,'diff':'hard'});p.evaluate('()=>{for(const [i,k]of ["s8gravity1003","s8stalker1003","s8prism1003"].entries())spawnEnemy(k,camLeftX()+viewW()*([.22,.5,.78][i]),100+i*12,{});player.invuln=1e9;}')
  for i in range(270):frames(p,2);p.wait_for_timeout(21)
  p.evaluate('()=>new Promise(resolve=>{rec1003.onstop=async()=>{const b=new Blob(recChunks1003,{type:"video/webm"});const r=new FileReader();r.onload=()=>{window.video1003=r.result;resolve();};r.readAsDataURL(b);};rec1003.stop();})')
  (O/'knight-combo.webm').write_bytes(base64.b64decode(p.evaluate('()=>video1003.split(",")[1]')))
  ck(not errors,'zero page and console errors');browser.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(x['ok'] for x in report['checks']) and not errors else 1)
