"""Regular-wave-only Furious native inputs; no enemy HP/phase/attack-clock writes.
Only encounter entry disabled in review; original level length/scroll retained.
Pilot invulnerability labelled.
One continuous in-game film per level; every successful native wave gets a chapter.
"""
from pathlib import Path
import json,sys,base64,hashlib,re,subprocess,time
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
O=R/'_shots/waves_all_1101';ff=imageio_ffmpeg.get_ffmpeg_exe();stages=[(int(x.rstrip('r')),'right'if x.endswith('r')else'left')for x in sys.argv[1:]]or[(s,r)for s in range(1,10)for r in(['left','right']if s==6 else['left'])]
paths=['index.html']+[m.split('?')[0]for m in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8'))if(R/m.split('?')[0]).is_file()]
hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in paths};script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.24');a=script.index(' function aim(elapsed){');z=script.index(' function render(){',a);script=script[:a]+' function aim(elapsed){}\n'+script[z:]
a=script.index(" diffKey='furious';debugUnlocked=true;");z=script.index(' return {entry,difficulty:',a);script=script[:a]+" const entry={stage:cfg.stage,role:'waves',kind:'regular'};setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[z:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / AUTHORED WAVE '+Math.min(WR15.expected,WR15.events.length)+'/'+WR15.expected+' / FURIOUS / INVULNERABLE OBSERVER'")
with sync_playwright()as pw:
 for stage,route in stages:
  label='stage-'+str(stage)+('-right'if stage==6 and route=='right'else'');V=O/label;V.mkdir(exist_ok=True);errors=[];trace=[];method=(R/'_BUILD_SOURCE/wave_review_1101.js').read_bytes();(V/'wave-review-source.js').write_bytes(method)
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(V/'wave-review-source.js'));setup=p.evaluate('q=>WR15.start(q.stage,q.route)',dict(stage=stage,route=route));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
  p.evaluate('()=>{drawWorld(0);requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
  with(V/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate(script,dict(name='Stage '+str(stage)+' / Regular waves',stage=stage,role='waves',kind='regular'))
   # Native 60 Hz updates and native renderer share one simulation delta. The
   # outer app loop has a separate wall-time scenery clock; resuming it after
   # a trapped/preloaded fixture can exhaust terrain before queued ground rows.
   # No actor HP, phase, attack timer or wave callback is synthesized here.
   p.evaluate('''()=>{let previous=performance.now(),debt=0;window.waveFilmLive=true;
    function frame(now){if(!waveFilmLive)return;debt+=Math.max(0,Math.min(.05,(now-previous)/1000));previous=now;let steps=0;
     stageLoadTick();while(debt+1e-9>=1/60&&steps<3&&state===GS.PLAY){WR15.input(1/60);stateT+=1/60;updatePlay(1/60);debt-=1/60;steps++;}
     ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;window.__bofFrames=(window.__bofFrames|0)+1;drawWorld(steps/60);
     requestAnimationFrame(frame);
    }requestAnimationFrame(frame);}''');beg=time.monotonic();print('START',stage,setup,flush=True)
   while True:
    p.wait_for_timeout(1000);q=p.evaluate('()=>({...WR15.snapshot(),wall:(performance.now()-captureStart)/1000,frames:__bofFrames})');trace.append(q)
    if len(trace)%20==0:
     (V/'progress.json').write_text(json.dumps(q,indent=2));print('Stage',stage,round(q['wall']),q['events'],'/',q['expected'],q['input'],flush=True)
    if q['done']or errors or q['state']!='play'or time.monotonic()-beg>650:break
   detail=p.evaluate('()=>({events:WR15.events,attempts:WR15.attempts,spawns:WR15.spawned})');stats=p.evaluate('async()=>{waveFilmLive=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,botErrors:reviewBot.errors};}')
  report=dict(stage=stage,route=route,label=label,setup=setup,result=q,trace=trace,**detail,stats=stats,errors=errors,sourceHashes=hashes,method=__doc__,methodSourceHash=hashlib.sha256(method).hexdigest());(V/'report.json').write_text(json.dumps(report,indent=2));p.close();b.close()
  assert not errors and q['done']and not q['boss']and not q['mini'],(stage,q,errors)
  movie=V/('stage-'+str(stage)+'-waves.mp4');subprocess.run([ff,'-y','-i',str(V/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],stdout=subprocess.DEVNULL,stderr=(V/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
  assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in paths},'Production changed during recording'
  print('DONE',stage,round(q['wall'],2),'seconds',len(detail['events']),'wave chapters',flush=True)
