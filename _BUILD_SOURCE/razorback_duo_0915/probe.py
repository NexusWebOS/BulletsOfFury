"""Real Chromium proof for the Stage-1 Hard Razorback duo."""
from pathlib import Path
import base64,hashlib,http.server,json,subprocess,sys
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'razorback_duo_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright

checks=[];errors=[];details={}
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200})
  page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_timeout(5000)
  boot=page.evaluate("()=>({assets:typeof ASSETS,stage:typeof setState,draw:typeof drawWorld,frames:window.__bofFrames||0})")
  print('boot '+json.dumps(boot)+' errors '+json.dumps(errors),flush=True)
  ok(boot['assets']=='object' and boot['stage']=='function' and boot['draw']=='function','production game API boots before the encounter probe')
  page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(1,'mini','yuri')");ok(fight.get('ok'),'native Stage-1 miniboss route opens in Chromium')
  page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];
    state=GS.PLAY;stateT=1;run.stage=1;curStage=STAGES[0];diffKey='hard';DIFF=DIFFS.hard;camX=100;player.x=340;player.y=VH-72;player.invuln=999;player.dead=false;player.alive=true;
    subBoss=null;subBossActive=false;spawnSubBoss('razorback');subBossActive=true;window.__rzbGets=[];const get=XART.get.bind(XART);XART.get=function(k){if(k.indexOf('rzb_')===0)__rzbGets.push(k);return get(k);};}""")
  ok(page.evaluate("()=>!!subBoss._rzbPair&&subBoss._rzbPair.actors.length===2&&!subBoss._rzb"),'Hard creates two real Razorback actors in the campaign miniboss slot')
  keys=['rzb_hull_0','rzb_machinegun','rzb_turret','rzb_sonic_ring','rzb_sonic_bullet','rzb_razor_missile']
  ready=False
  for _ in range(260):
    ready=page.evaluate("ks=>ks.every(k=>XART.rdy(k))",keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Razorback hull, guns and ordnance decode before capture')
  def step(n):
    for i in range(0,n,20):page.evaluate('n=>__step(n)',min(20,n-i));page.wait_for_timeout(8)
  def shot(name):
    page.evaluate('()=>{shake=0;drawWorld(0)}');p=OUT/(name+'.png');p.write_bytes(base64.b64decode(page.evaluate('()=>document.querySelector("#screen").toDataURL("image/png").split(",")[1]')));return p
  entered=False
  for _ in range(180):
    entered=page.evaluate("()=>subBoss._rzbPair.actors.every(p=>p._rzb.state==='guns'&&p._rzb.trans<=0)")
    if entered:break
    step(4)
  ok(entered,'both tanks complete their authored arrival and materialize into combat')
  state=page.evaluate("""()=>{const a=subBoss._rzbPair.actors;return {states:a.map(p=>p._rzb.state),attacks:a.map(p=>p._rzb.attack),xs:a.map(p=>p.x),ys:a.map(p=>p.y),w:a[0].w,h:a[0].h,max:a.map(p=>p.maxhp),bar:subBoss.maxhp,targets:retinaBossTargets(subBoss).map(t=>t._retinaId)}}""")
  details['entered']=state
  ok(state['states']==['guns','guns'] and state['attacks']==['suppression','sonic'],'the pair enters together with offset suppression and sonic attack books')
  ok(state['xs'][1]-state['xs'][0]>state['w'],'the two complete tank silhouettes keep separate lanes')
  ok(len(state['targets'])==4 and len(set(state['targets']))==4,'Retina exposes both destructible guns on each tank')
  arrival=shot('razorback_duo_01_offset_attacks')
  # Five seconds of the live update loop: two independent attacks, bullets and movement.
  ff=imageio_ffmpeg.get_ffmpeg_exe();movie=OUT/'Razorback_Duo_Hard_0915.mp4'
  proc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for f in range(150):
    page.evaluate('()=>__step(2)');proc.stdin.write(base64.b64decode(page.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.92).split(",")[1]')))
    if f in (28,48,84,120):shot('razorback_duo_%02d'%(2+(28,48,84,120).index(f)))
    if f%30==0:page.wait_for_timeout(8)
  proc.stdin.close();fferr=proc.stderr.read();ok(proc.wait()==0,'native five-second duo capture encodes cleanly')
  subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
  pressure=page.evaluate("""()=>{const a=subBoss._rzbPair.actors,b=eBullets.filter(q=>q._rzb&&!q.dead);return {owners:a.map(p=>b.filter(q=>q._rzbOwner===p).length),kinds:Array.from(new Set(b.map(q=>q.kind))),gap:!razorbackPairContact(subBoss,(a[0].x+a[1].x)/2,(a[0].y+a[1].y)/2),gets:Array.from(new Set(__rzbGets)),hp:a.map(p=>p.hp),sum:subBoss.hp}}""")
  details['pressure']=pressure
  ok(all(n>0 for n in pressure['owners']),'both tanks independently own live hostile ordnance')
  ok('rzbSonic' in pressure['kinds'] and 'mg' in pressure['kinds'],'the simultaneous pressure includes sonic fire and machine rounds')
  ok(pressure['gap'],'the open lane between the two hulls remains non-colliding')
  # A real component hit damages only the selected actor; one destroyed actor cannot end the encounter.
  result=page.evaluate("""()=>{const a=subBoss._rzbPair.actors,L=rzbWorld(a[0],-57,96),before=a.map(p=>p.hp);_dmgBullet=null;hitSubBoss(13,L.x,L.y);const after=a.map(p=>p.hp);a[0].dead=true;a[0].hp=0;a[0].dying=0;for(let i=0;i<70;i++)updateSubBoss(1/60);return {before,after,firstGone:a[0]._rzbGone,secondAlive:!a[1].dead,pairAlive:!subBoss.dead};}""")
  details['damage']=result
  ok(result['after'][0]<result['before'][0] and result['after'][1]==result['before'][1],'a gun hit routes to only the tank under the impact point')
  ok(result['firstGone'] and result['secondAlive'] and result['pairAlive'],'destroying one tank leaves the second tank and encounter active')
  one=shot('razorback_duo_06_one_tank_remaining')
  ok(page.evaluate("()=>__rzbGets.filter(k=>k.indexOf('rzb_hull_')===0).length>=2"),'the native renderer draws authored Razorback hull plates')
  ok(arrival.stat().st_size>20000 and one.stat().st_size>15000 and movie.stat().st_size>50000,'screenshots and video contain non-empty native gameplay frames')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors')
  details['runtimeSha256']=hashlib.sha256((ROOT/'assets/game.js').read_bytes()).hexdigest();br.close()
stop()
result={'checks':checks,'errors':errors,'details':details,'fight':fight,'shots':[str(p.relative_to(ROOT)) for p in OUT.glob('*.png')],'video':str(movie.relative_to(ROOT))}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
