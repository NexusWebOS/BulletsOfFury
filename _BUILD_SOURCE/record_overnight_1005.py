"""Record live Chromium render with keyboard flight; no replacement rendering."""
from pathlib import Path
import base64,json,math,sys,time
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];report={'clips':[],'checks':[]}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n):
 for i in range(0,n,20):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return cv.toDataURL().split(",")[1];}')))
def record(p,name,seconds):
 print('RECORD '+name,flush=True)
 p.evaluate('()=>{window.chunks=[];window.rec=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1400000});rec.ondataavailable=e=>chunks.push(e.data);rec.start();window.sample={maxHostile:0,damageAttempts:0,states:[],enemyFamilies:[],frames:0};window.captureHit=playerHit;playerHit=function(){sample.damageAttempts++;return captureHit.apply(this,arguments);};}')
 fire=p.evaluate('()=>keybindFor(1).fire[0]');firing='waves' not in name
 if firing:p.keyboard.down(fire)
 direction=None
 for i in range(seconds*30):
  if 'waves' in name:
   want=i%360>=240
   if want!=firing:
    (p.keyboard.down if want else p.keyboard.up)(fire);firing=want
  desired='ArrowLeft' if (i//90)%2==0 else 'ArrowRight'
  if direction!=desired:
   if direction:p.keyboard.up(direction)
   direction=desired;p.keyboard.down(direction)
  p.evaluate('()=>{for(let i=0;i<2;i++){updatePlay(1/60);drawWorld(1/60);sample.maxHostile=Math.max(sample.maxHostile,eBullets.filter(q=>!q.dead).length);for(const e of enemies)if(!sample.enemyFamilies.includes(e.type))sample.enemyFamilies.push(e.type);sample.frames++;const s=boss?._r30?.attack?.type||boss?._r30?.mode||state;if(!sample.states.includes(s))sample.states.push(s);}}')
  if i%(30*5)==0:shot(p,name+'-'+str(i//30))
  p.wait_for_timeout(28)
 p.keyboard.up(fire)
 if direction:p.keyboard.up(direction)
 p.evaluate('()=>{playerHit=captureHit;}')
 data=p.evaluate('()=>new Promise(resolve=>{rec.onstop=async()=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(",")[1]);r.readAsDataURL(new Blob(chunks,{type:"video/webm"}));};rec.stop();})')
 (O/(name+'.webm')).write_bytes(base64.b64decode(data));result=p.evaluate('()=>sample');result.update({'file':name+'.webm','simulatedSeconds':seconds,'recording':'canvas 30fps VP9, silent; actual updatePlay and keyboard flight'})
 report['clips'].append(result);print('DONE '+name+' '+json.dumps(result),flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B._noHit=false;window.G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;for(const q of R.ships){q.mode="fight";q.warp=0;q.x=player.x+(q.i-2)*80;q.y=170;q.rg4.cd=9999;q.rg4.act=null;}run._primary1003b="mg";run.weapon=0;run._cfTier=6;run._cfUnlocked=8;run.wlevel=6;run.wlevels[0]=8;cf1004Warm();rg4Warm();fb2Warm();r30Warm();}')
  p.wait_for_function('()=>XART.rdy("cf1004_weapons")&&ON5_ART.knight.every(a=>XART.rdy(a.key))',timeout=120000)
  # Actual emitted VI/VII lanes and Fusion pass through ordinary updatePlay.
  lasers=[]
  for tier in [6,7,8]:
   for pilot in ['voss','nyx','rook','kaia','jace']:
    value=p.evaluate('([tier,pilot])=>{const q=R.ships.find(q=>q.key===pilot);for(const s of R.ships){s.x=-1500;s.frCloak=0;}q.flash=0;q.x=player.x=worldWidth()/2;q.y=190;const old=q.hp;run._cfTier=tier;run.wlevel=tier;player.fireCd=0;pBullets=[];if(tier===8)coleFuseRelease(FUSE_FULL);else pShoot();const kinds=pBullets.map(p=>p.kind);for(const t of pBullets){t.x=t.cx=q.x;t.y=q.y;t.vx=0;if(t._cfFusion)t.vy=0;else t.vy=-.01;}updatePlay(1/60);return{tier,pilot,kinds,before:old,after:q.hp};}',[tier,pilot]);lasers.append(value)
  report['laserHP']=lasers;ck(all(q['after']<q['before'] for q in lasers),'actual Cole VI, VII and Fusion damage every Rebel hull')
  for stage in ([7,8] if '--waves' in sys.argv else [6,7,8]):
   p.evaluate(SETUP,{'stage':stage,'pilot':'cole','diff':'furious'})
   p.evaluate('(stage)=>{stagePlan=buildStagePlan(stage).sort((a,b)=>a.t-b.t);subBossDone=subBossTriggered=true;stageTimer=stage===6?38:25;waveIdx=stagePlan.filter(q=>q.t<stageTimer).length;spawnClock=0;mapScroll=stage===6?900:700;player.invuln=0;run.lives=9;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run._cfTier=6;run._cfUnlocked=8;run.wlevels[0]=8;player.x=worldWidth()/2;player.y=VH-90;}',stage)
   record(p,'stage'+str(stage)+'-furious-waves',22)
   ck(report['clips'][-1]['maxHostile']>0,'Stage '+str(stage)+' sample includes actual hostile ammunition')
  # Restore uninjured fighters, let their complete specials run with actual input.
  if '--waves' in sys.argv:raise StopIteration()
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B._noHit=false;G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run._cfTier=6;run._cfUnlocked=8;run.wlevels[0]=8;player.invuln=0;s6WingInit();s6WingLaunch(4,true);for(const q of R.ships){q.mode="fight";q.warp=0;q.x=player.x+(q.i-2)*80;q.y=150;q.rg4.cd=1+q.i*1.2;}}')
  record(p,'rebel-furious-dogfight',35)
  # Phase clips include warning/active/recovery cycles, with harmless entry protection.
  for phase in ([] if '--late' in sys.argv else [0,1,2]):
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
   p.evaluate('(phase)=>{j3Encounter(B,phase);if(phase===0)on5FightStart(B);player.invuln=0;run.lives=9;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run._cfTier=6;run._cfUnlocked=8;run.wlevels[0]=8;}',phase)
   record(p,'finale-phase'+str(phase+1),22 if phase<2 else 32)
  if '--late' not in sys.argv:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
   p.evaluate('()=>{j3Encounter(B,2);j3Mimic(B,5);B._r30.mode="fight";B.enter=false;B._noHit=false;player.invuln=0;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run._cfTier=6;run._cfUnlocked=8;run.wlevels[0]=8;}')
   record(p,'knight-hammer-donor',24)
  ck(p.evaluate('()=>ON5.draws["bomber-red"]>0&&ON5.draws["bomber-green"]>0'),'both genuine red/green stealth palettes render in live Stage 6')
  ck(p.evaluate('()=>ON5.draws.tracers>0'),'authored high-contrast late-stage rounds render')
  ck(not errors,'zero page/console errors during recordings');b.close()
except StopIteration:ck(not errors,'zero page/console errors during wave recordings')
finally:
 stop();report['errors']=errors;(O/('recordings-waves.json' if '--waves' in sys.argv else 'recordings-late.json' if '--late' in sys.argv else 'recordings.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(q['ok'] for q in report['checks']) and not errors else 1)
