from pathlib import Path
import sys,json,time,base64,hashlib,subprocess,shutil
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Stage5-bomber-assault';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
errors=[];timeline=[];chapters=[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe();probe=shutil.which('ffprobe');raw=O/'bomber-native-capture.mp4';movie=O/'stage5-bomber-furious-final.mp4';assert not raw.exists()and not movie.exists()
audio=(W.parent/'draconus_rotor_stages_1111/record-audio-init.js').read_text();capture=(W.parent/'restore_boss_1112/capture.js').read_text().replace("(window.reviewLabel||'Recovered animations')+' / NATIVE ANIMATION CHECKPOINT / INVULNERABLE REVIEW'","(window.reviewLabel||'STAGE 5 BOMBER')+' / FURIOUS / INVULNERABLE ATTACK REVIEW'")
(W/'capture-audio.js').write_text(audio);(W/'capture.js').write_text(capture)
names=['index.html','assets/game.js','assets/stage5_bomber_assault_1114.js','assets/stage5_bomber_assault_art_1114.js'];hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in names}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--js-flags=--expose-gc']);c=br.new_context(viewport={'width':1280,'height':800});c.add_init_script(audio);c.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p=boot(c,port,5,errors,'mini');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&s5b14Warm()}',timeout=180000)
  p.evaluate("""()=>{diffKey='furious';run.ngplus=false;spawnSubBoss('siegebomber');subBossActive=true;subBossDone=false;window.B=subBoss;boss=null;bossActive=false;enemies=[];l5Rocks=[];powerups=[];eBullets=[];pBullets=[];groundTargetingFx=[];S5B14.events=[];DBGT.god=true;Input.mouse.active=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;player.dead=player.out=false;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);window.reviewLabel='ECLIPSE SIEGE BOMBER / NATIVE ENTRY';const original=updatePlay;updatePlay=function(dt){const m=B._s5b14,phase=m?.phase||'entry';const tx=camLeftX()+viewW()/2+Math.sin(efxClock*.55)*75,ty=phase==='catch'?PLAY.y+100:VH-75;for(const [a,yes]of Object.entries({left:player.x>tx+7,right:player.x<tx-7,up:player.y>ty+7,down:player.y<ty-7,fire:false})){for(const k of keybind[a]||[])Input.keys[k]=yes;}return original.apply(this,arguments);};}""")
  saved=set();seen=set();complete=False;endpoint=None;last_print=-15
  with raw.open('wb')as f:
   p.expose_function('saveReviewChunk',lambda b:f.write(base64.b64decode(b)));setup=p.evaluate(capture,5);start=time.monotonic()
   while time.monotonic()-start<180:
    p.wait_for_timeout(150);elapsed=time.monotonic()-start
    q=p.evaluate("""()=>{const m=B._s5b14;return{phase:m?.phase||'entry',t:m?.t,cycle:m?.cycle||0,depth:m?.depth,fore:m?.fore,air:m?.air,hp:B.hp,max:B.maxhp,x:B.x,y:B.y,player:{x:player.x,y:player.y},rounds:s5b14Owned(B),bombs:groundTargetingFx.filter(q=>q._s5b14Owner===B&&!q.dead).length,target:m?.target,locked:m?.locked}}""");q['wall']=elapsed;timeline.append(q);(O/'recording-live.json').write_text(json.dumps(q,indent=2))
    if errors:raise RuntimeError(errors)
    phase=q['phase']
    if phase not in seen:seen.add(phase);chapters.append(dict(at=elapsed,phase=phase));p.evaluate('s=>reviewLabel="ECLIPSE SIEGE BOMBER / "+s.toUpperCase()',phase)
    label=None
    if phase=='lock'and q.get('locked'):label='target-committed'
    if phase=='burst'and q.get('t',0)>.2:label='cannon-burst'
    if phase=='cool'and .25<q.get('t',0)<1.4:label='cannons-cooling'
    if phase=='boost'and q.get('t',0)>.5:label='thrust-away'
    if phase=='charge'and 1.3<q.get('depth',0)<1.6:label='bombing-overflight'
    if phase=='return'and .95<q.get('depth',0)<1.2:label='shadowed-return'
    if phase=='catch'and q.get('t',0)>.35:label='catching-up'
    if label and label not in saved:p.screenshot(path=str(O/('native-'+label+'.png')));saved.add(label)
    if elapsed-last_print>12:print('NATIVE',json.dumps(q),flush=True);last_print=elapsed;p.evaluate('()=>{if(window.gc)window.gc()}')
    if q['cycle']>=2 and endpoint is None:endpoint=elapsed
    if endpoint is not None and elapsed-endpoint>1.0:complete=True;break
   assert complete,'Two native flight cycles did not finish'
   stats=p.evaluate("async()=>{await new Promise(r=>{reviewRec.onstop=r;reviewRec.stop()});await reviewPending;reviewLive=false;return{...reviewStats,events:S5B14.events}}")
   p.screenshot(path=str(O/'recording-end.png'));br.close()
finally:stop()
assert not errors and not stats['tapErrors']and stats['peak']>.001
assert all(n in seen for n in ['lock','burst','cool','boost','turn-in','charge','pass','return','catch']),seen
assert all(abs(q['hp']-q['max'])<.01 for q in timeline),'The review must retain native HP without simulated damage/healing'
subprocess.run([ff,'-v','error','-i',str(raw),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],capture_output=True,check=True)
subprocess.run([ff,'-v','error','-threads','2','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
media=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(movie)]));unchanged=hashes=={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in names};assert unchanged
playback='''<!doctype html><meta charset="utf-8"><title>Stage 5 bomber — Furious preview</title><style>body{margin:24px;background:#08121c;color:#e5edf6;font:16px system-ui}video{display:block;width:min(100%,1280px);height:auto}p{max-width:1000px}</style><h1>Stage 5 bomber — Furious</h1><p>Actual game capture: native entry, two complete targeting/burst/cooldown and bombing/overflight/catch-up cycles. Invulnerable keyboard review pilot. Full original health; no attack-phase skips. This preview shows behavior and graphics, not a survival or balance verdict.</p><video controls preload="metadata" src="stage5-bomber-furious-final.mp4"></video>'''
(O/'playback.html').write_text(playback,encoding='utf-8')
port,stop=serve(str(O));seeks=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True);p=br.new_page();p.goto(f'http://127.0.0.1:{port}/playback.html');p.wait_for_function('document.querySelector("video").readyState>=2');duration=p.evaluate('document.querySelector("video").duration')
  for f in [.05,.33,.67,.94]:
   t=duration*f;p.evaluate('async t=>{const v=document.querySelector("video");await new Promise(r=>{v.onseeked=r;v.currentTime=t})}',t);q=p.evaluate('()=>{const v=document.querySelector("video");return{at:v.currentTime,ready:v.readyState,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null}}');assert q['ready']>=2 and q['width']==1280 and not q['error'];seeks.append(q)
  br.close()
finally:stop()
report=dict(complete=complete,setup=setup,timeline=timeline,chapters=chapters,stats=stats,errors=errors,media=media,phases=sorted(seen),nativeSourcesUnchanged=unchanged,sourceHashes=hashes,playbackSeeks=seeks,sha256=hashlib.sha256(movie.read_bytes()).hexdigest());(O/'recording-verification.json').write_text(json.dumps(report,indent=2))
assert raw.resolve().parent==O.resolve();raw.unlink();print('COMPLETE',media['format']['duration'],str(movie),flush=True)
