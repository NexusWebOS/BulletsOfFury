from pathlib import Path
import subprocess,time,ctypes,shutil,json,datetime,wave
W=Path(__file__).resolve().parent;Q=W/('qa/preview-'+str(int(time.time())));Q.mkdir();EXE=W.parent/'Releases/BulletsOfFury-Windows-2026-11-06/BOF Launcher.exe';FF=shutil.which('ffmpeg');p=None;rec=None
try:
 p=subprocess.Popen([str(EXE),'--qa-tour','--qa-dir',str(Q),'--profile',str(Q/'profile')]);until=time.monotonic()+30;h=0
 while not h:
  h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury - Fury HQ')
  if time.monotonic()>until:raise RuntimeError('Preview window not found')
  time.sleep(.01)
 # Focus this task's own application; no other app is operated or recorded.
 ctypes.windll.user32.ShowWindow(h,9);ctypes.windll.user32.SetForegroundWindow(h)
 start=datetime.datetime.now(datetime.timezone.utc);raw=Q/'launcher-native-silent.mp4';f=(Q/'capture.log').open('w')
 rec=subprocess.Popen([FF,'-hide_banner','-loglevel','warning','-y','-f','gdigrab','-framerate','60','-draw_mouse','0','-i','title=Bullets of Fury - Fury HQ','-an','-c:v','libx264','-preset','ultrafast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(raw)],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT)
 p.wait(timeout=35)
 if rec.poll()is None:
  try:rec.communicate(b'q\n',timeout=15)
  except subprocess.TimeoutExpired:rec.terminate();rec.wait(timeout=10)
 f.close();rows=[json.loads(s)for s in(Q/'desktop.jsonl').read_text().splitlines()];events=[]
 for r in rows:
  if r['name']=='cue':
   t=(datetime.datetime.fromisoformat(r['time'])-start).total_seconds();events.append(dict(cue=r['data'],seconds=max(0,t)))
 # Match the app's one-voice SoundPlayer retrigger/cut semantics. The native
 # UI is captured live; its own exact PCM cues are mixed from its event log.
 args=[FF,'-hide_banner','-loglevel','error','-y','-i',str(raw)];filters=[];names=[]
 for i,event in enumerate(events):
  wav=W/'art'/(event['cue']+'.wav');args+=['-i',str(wav)]
  with wave.open(str(wav))as w:length=w.getnframes()/w.getframerate()
  if i+1<len(events):length=min(length,max(.001,events[i+1]['seconds']-event['seconds']))
  label=f'a{i}';filters.append(f'[{i+1}:a]atrim=0:{length},adelay={round(event["seconds"]*1000)}|{round(event["seconds"]*1000)}[{label}]');names.append(f'[{label}]')
 filters.append(''.join(names)+f'amix=inputs={len(names)}:normalize=0:dropout_transition=0[outa]');out=W.parent/'Releases/BOF-Fury-HQ-Launcher-Preview.mp4';args+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[outa]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(out)];subprocess.run(args,check=True)
 close=[r for r in rows if r['name']=='terminal-close'][-1]['data'];receipt=dict(video=str(out),captureDirectory=str(Q),events=events,performance=close,provenance='Live native launcher-window capture; original PCM cue timing reconstructed from actual app event log, not microphone/system audio capture.');(W/'qa/preview.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt),flush=True)
finally:
 if p and p.poll()is None:p.terminate();p.wait(timeout=15)
 if rec and rec.poll()is None:rec.terminate();rec.wait(timeout=15)
