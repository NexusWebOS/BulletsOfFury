from pathlib import Path
import sys,json,time,base64,hashlib,subprocess,shutil
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-new-rage';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
sys.stdout.reconfigure(encoding='utf-8');errors=[];timeline=[];chapters=[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe();probe=shutil.which('ffprobe')
raw=O/'draconus-native-capture.mp4';movie=O/'draconus-new-rage-kamehameha-and-center-smash.mp4';assert not raw.exists()and not movie.exists()
audio=(W.parent/'draconus_rotor_stages_1111/record-audio-init.js').read_text();capture=(W.parent/'restore_boss_1112/capture.js').read_text();(W/'capture-audio.js').write_text(audio);(W/'capture.js').write_text(capture)
names=['assets/game.js','assets/draconus_cinematic_rage_1113.js','assets/draconus_cinematic_rage_art_1113.js','assets/draconus_front_rage_1113.js','assets/rage_palm_1110.js','assets/boss_restore_1112.js','assets/chronos_rageform_1026.js','assets/draconus_modular_1111.js'];hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in names}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--js-flags=--expose-gc']);context=br.new_context(viewport={'width':1280,'height':800});context.add_init_script(audio);context.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p=boot(context,port,8,errors,'boss');p.on('console',lambda m:errors.append(m.text)if'update error'in m.text or'draw error'in m.text else None)
  p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(8))updatePlay(0);return stageLoadReady(8)&&!bp119Pending()&&ba119Warm(8)&&rf1110Warm(8)}',timeout=180000);p.evaluate((W/'setup.js').read_text())
  p.evaluate('''()=>{Input.mouse.active=false;window.frontCheckpoint=(mat,direction)=>{seed13(mat);reviewLabel='DRACONUS / '+mat.toUpperCase()+' / FRONTAL '+direction.toUpperCase()+' STRIKES';Q._td1111Next={center:0,right:1,left:2}[direction]??0;hb20Start(B,direction==='side'?'side':'skystrike');};window.lowHealthCheckpoint=()=>{seed13('chrome',55);reviewLabel='DRACONUS / LOW-HEALTH RAGE TRANSFORMATION';hb20Start(B,'side');B._lastPart=Q.parts[0];GP4.clock+=1;modularHit(B.maxhp);};frontCheckpoint('regular','center');}''')
  queue=[('regular','center'),('chrome','center')];idx=0;rage=False;complete=False;saved=set();phase_marks=set();endpoint=None
  with raw.open('wb')as stream:
   p.expose_function('saveReviewChunk',lambda b:stream.write(base64.b64decode(b)));setup=p.evaluate(capture,8);start=time.monotonic();last_print=-20;chapters.append(dict(at=0,label='Normal: new straight-down center smash'))
   while time.monotonic()-start<240:
    p.wait_for_timeout(140);elapsed=time.monotonic()-start
    q=p.evaluate('''()=>{const A=Q.action,R=Q.rf1110,a=hb20Pose(B)?.a;return{state,mode:B._r30.mode,form:B._r30.v18.form,action:A?.type,actionTime:A?.t,u:A?A.t-A.tell:null,phase:R?.phase,phaseTime:R?.t,cycle:R?.cycle,depth:R?.volley?.depth,hp:B.hp,max:B.maxhp,donorAge:B._r30.v18.donorAge,front:a?.faceForward,bank:a?.bank,flash:B.flash,events:DFR13.events.filter(e=>e.type==='rage-book-complete').length,errors:[]};}''');q['wall']=elapsed;timeline.append(q);(O/'recording-live.json').write_text(json.dumps(q,indent=2))
    if errors:raise RuntimeError(errors)
    if elapsed-last_print>12:print('NATIVE',json.dumps({k:q.get(k)for k in ['wall','action','phase','cycle','depth','hp','events']}),flush=True);last_print=elapsed;p.evaluate('()=>{if(window.gc)window.gc()}')
    label=None
    if not rage and queue[idx][1]=='center'and q.get('u')is not None and .98<q['u']<1.15:label=queue[idx][0]+'-front-center-native'
    if rage:
     if q.get('action')=='rage'and(q.get('actionTime')or 0)>6.65:label='rage-red-formation-native'
     if q.get('phase')=='volley_fire':label='rage-'+str(q.get('depth'))+'-palms-native'
     if q.get('phase')=='beam':label='rage-repeat-wave-native'
     if q.get('phase')=='kame_charge'and q.get('phaseTime',0)>1.65:label='rage-two-hand-ball-gather-native'
     if q.get('phase')=='kame_thrust'and q.get('phaseTime',0)>.26:label='rage-two-hand-thrust-native'
     if q.get('phase')=='kame_fire'and q.get('phaseTime',0)>.25:label='rage-two-hand-opening-wave-native'
     for token,title in [('rage','Rage transformation'),('kame_fire','Rage opening wave'),('foreground','Rage foreground palm volleys'),('background','Rage background palm volleys'),('beam','Rage repeat wave')]:
      found=q.get('action')==token if token=='rage'else q.get('depth')==token and q.get('phase')=='volley_fire'if token in ['foreground','background']else q.get('phase')==token
      if found and token not in phase_marks:phase_marks.add(token);chapters.append(dict(at=elapsed,label=title))
    if label and label not in saved:p.screenshot(path=str(O/(label+'.png')));saved.add(label)
    if not rage and not q.get('action'):
     idx+=1
     if idx<len(queue):
      mat,direction=queue[idx];p.evaluate('q=>frontCheckpoint(...q)',[mat,direction])
      if idx==1:chapters.append(dict(at=elapsed,label='Chromium: new straight-down center smash'))
     else:p.evaluate('lowHealthCheckpoint()');rage=True;chapters.append(dict(at=elapsed,label='Late-fight low-health checkpoint: native rage entry'))
    if q['events']and endpoint is None:endpoint=elapsed
    if endpoint is not None and elapsed-endpoint>.45:complete=True;break
   assert complete,'Draconus did not complete the full native rage book'
   stats=p.evaluate("async()=>{await new Promise(r=>{reviewRec.onstop=r;reviewRec.stop()});await reviewPending;reviewLive=false;return{...reviewStats,newArtEvents:DCR13.events,cast:DCR13.lastCast,actorDraws:DCR13.draws.slice(-50),events:DFR13.events,shots:RF1110.events.filter(e=>e.type==='palm-shot')}}")
   p.screenshot(path=str(O/'recording-end.png'));br.close()
finally:stop()
assert not errors and not stats['tapErrors']and stats['peak']>.001
assert all(x in phase_marks for x in ['rage','kame_fire','foreground','background','beam']),phase_marks
subprocess.run([ff,'-v','error','-i',str(raw),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],capture_output=True,check=True)
subprocess.run([ff,'-v','error','-threads','2','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
media=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(movie)]));assert raw.resolve().parent==O.resolve();raw.unlink();unchanged=hashes=={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in hashes};assert unchanged
report=dict(complete=complete,setup=setup,timeline=timeline,chapters=chapters,stats=stats,errors=errors,media=media,phases=sorted(phase_marks),nativeSourcesUnchanged=unchanged,sourceHashes=hashes,sha256=hashlib.sha256(movie.read_bytes()).hexdigest());(O/'recording-verification.json').write_text(json.dumps(report,indent=2));print('COMPLETE',media['format']['duration'],str(movie),flush=True)
