from pathlib import Path
import sys,json,time,base64,hashlib,subprocess,shutil
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Recovered-boss-animations';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
sys.stdout.reconfigure(encoding='utf-8');errors=[];stages=[8]if'--stage8'in sys.argv else[5,8];reports=[json.loads((O/'stage5-recording.json').read_text())]if stages==[8]else[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe();probe=shutil.which('ffprobe')
audio=(W.parent/'draconus_rotor_stages_1111/record-audio-init.js').read_text();(W/'capture-audio.js').write_text(audio)
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','assets/boss_restore_1112.js','assets/boss_restore_art_1112.js','assets/whole_hammer_1110.js','assets/rage_palm_1110.js','assets/draconus_modular_1111.js']}
try:
 with sync_playwright()as pw:
  for stage in stages:
   raw=O/f'stage{stage}-native-capture.mp4';movie=O/('chronus-restored-rage-and-swings.mp4'if stage==5 else'draconus-restored-side-swings.mp4');assert not raw.exists()and not movie.exists()
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--js-flags=--expose-gc','--disable-background-timer-throttling']);context=br.new_context(viewport={'width':1280,'height':800});context.add_init_script(audio);p=boot(context,port,stage,errors,'boss');p.on('console',lambda m:errors.append(m.text)if'draw error'in m.text or'update error'in m.text else None)
   p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()&&ba119Warm(s)}',arg=stage,timeout=180000)
   if stage==5:p.evaluate((W/'seed5.js').read_text())
   else:p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=B._noHit=B.dead=false;window.Q=hb20State(B);BOFCinematicDirector.cancel();}")
   p.evaluate('''s=>{window.reviewPhases=new Set();window.beginSide=mat=>{reviewLabel=(s===5?'Chronus':'Draconus')+' / '+mat+' / recovered left and right sweeps';if(s===5){seed119('furious',mat);hammerState(B,'recover');B._hammer._hj22Pair=hj22Pair(B,'blue',{x:player.x,y:player.y});}else{Q.action=null;Q.rf1110=null;Q.rage=false;Q.chrome=mat==='chrome';Q.cool=999;Q.hammerDestroyed=false;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;B._r30.mode='fight';B._r30.v18.donorAge=0;B._noHit=B.enter=B.dead=false;hb20Start(B,'side');}player.dead=false;player.invuln=999;DBGT.god=true;};beginSide('regular');}''',stage)
   timeline=[];chapters=[]
   with raw.open('wb')as stream:
    p.expose_function('saveReviewChunk',lambda b:stream.write(base64.b64decode(b)));setup=p.evaluate((W/'capture.js').read_text(),stage);start=time.monotonic();checkpoints=[('regular',0),('regular',1),('chrome',0),('chrome',1)];idx=0;checkpoint_start=0;rage_started=False;complete=False
    chapters.append(dict(at=0,label='Normal recovered side sweeps'))
    while time.monotonic()-start<150:
     p.wait_for_timeout(180);elapsed=time.monotonic()-start
     q=p.evaluate('''s=>{const h=B._hammer,R=h?.c30,Q=s===8?hb20State(B):null;const phase=s===5?(h._hf22Charge?'formation':R?.phase||h.state):Q.action?.type||'recovery';reviewPhases.add(phase);return{stage:s,phase,charge:s===5&&!!h._hf22Charge,done:s===5&&!!h._c46Done,group:R?.volley?.group,combo:s===5?!!(h._hj22Pair||h.c27Combo||h._hf22StormPair):!!Q.action,hp:B.hp,dead:B.dead};}''',stage);q['wall']=elapsed;timeline.append(q)
     if errors:raise RuntimeError(errors)
     if not rage_started and not q['combo']and elapsed-checkpoint_start>1:
      idx+=1
      if idx<len(checkpoints):
       mat,_=checkpoints[idx];p.evaluate('m=>beginSide(m)',mat);checkpoint_start=elapsed
       if idx==2:chapters.append(dict(at=elapsed,label='Chromium recovered side sweeps'))
      elif stage==8:complete=True;break
      else:
       p.evaluate("()=>{seed119('furious','chrome');reviewLabel='Chronus / ORIGINAL rage formation and Kamehameha';const h=B._hammer;h._hf22Red=false;h._hf22Charge=null;h.c29Break=null;h.c27RagePending=true;B.hp=B.maxhp*.15;C45.events=[];C46.events=[];CF49.events=[];hf22BeginBlueRage(B);}");chapters.append(dict(at=elapsed,label='Original rage formation, opener wave and return'));rage_started=True
     if rage_started and q['done']and q['phase']=='volley_fire'and(q.get('group')or 0)>=1:complete=True;break
    assert complete,'Native animation checkpoints did not finish'
    stats=p.evaluate("async()=>{await new Promise(r=>{reviewRec.onstop=r;reviewRec.stop()});await reviewPending;reviewLive=false;return{...reviewStats,phases:[...reviewPhases],energy:CF49.events,formation:C45.events,kame:C46.events}}")
    p.screenshot(path=str(O/f'stage{stage}-recording-end.png'));br.close()
   assert not errors and not stats['tapErrors']and stats['peak']>.001
   subprocess.run([ff,'-v','error','-i',str(raw),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],capture_output=True,check=True)
   subprocess.run([ff,'-v','error','-threads','2','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
   media=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(movie)]));assert raw.resolve().parent==O.resolve();raw.unlink()
   report=dict(stage=stage,complete=complete,setup=setup,timeline=timeline,chapters=chapters,stats=stats,errors=errors,media=media,sha256=hashlib.sha256(movie.read_bytes()).hexdigest());reports.append(report);(O/f'stage{stage}-recording.json').write_text(json.dumps(report,indent=2));print('Finished native restoration clip:',stage,media['format']['duration'],flush=True)
finally:stop()
assert hashes=={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in hashes};(O/'recording-verification.json').write_text(json.dumps(dict(reports=reports,nativeSourcesUnchanged=True),indent=2))
