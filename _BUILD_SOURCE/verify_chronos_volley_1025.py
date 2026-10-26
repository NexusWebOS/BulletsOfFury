"""Decode the delivered video/audio and exercise its browser review page."""
from pathlib import Path
import json,subprocess,wave,numpy as np,imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_volley_1025';D=O/'video';checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(D/'chronos-volley.mp4'),'-vn','-ac','1','-ar','22050',str(D/'decoded.wav')],check=True)
with wave.open(str(D/'decoded.wav')) as w:a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
ck('Delivered MP4 contains decoded audible sound',np.sqrt(np.mean(a*a))>.01,dict(peak=float(np.max(np.abs(a))),rms=float(np.sqrt(np.mean(a*a)))))
r=json.loads((D/'review.json').read_text(encoding='utf8'));ck('Native recording has no page or console errors',not r['errors'],r['errors'])
ck('Recording includes red charge, palm volleys and energy wave',all(any(q['state']==s for q in r['timeline'])for s in ['hf22_rage_charge','c30_volley_fire','c30_beam']) and any(q['red']for q in r['timeline']))
ck('Recorded volleys fire from both foreground and background',all(any(q.get('depth')==depth and q['state']=='c30_volley_fire' for q in r['timeline'])for depth in ['foreground','background']))
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(R/'assets/game/shared/combat/combat_1003i/laser_release.mp3'),'-ac','1','-ar','22050',str(D/'laser-cue.wav')],check=True)
with wave.open(str(D/'laser-cue.wav'))as w:cue=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
ck('Shared alien laser cue decodes with audible waveform',np.sqrt(np.mean(cue*cue))>.005)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_frames_1025/index.html');p.wait_for_function('fight.readyState>=1&&Object.values(images).every(i=>i.complete&&i.naturalWidth>0)',timeout=90000)
  p.get_by_text('Play with sound',exact=True).click();p.wait_for_function('prepared&&!fight.paused&&fight.currentTime>.5',timeout=60000);q=p.evaluate('({time:fight.currentTime,duration:fight.duration,muted:fight.muted,paused:fight.paused})');ck('Review plays the actual 32-second MP4 with audio enabled',q['time']>.3 and q['duration']>30 and not q['muted'] and not q['paused'],q)
  p.evaluate('fight.pause();fight.currentTime=24.2');p.wait_for_function('Math.abs(fight.currentTime-24.2)<.3&&!fight.seeking&&fight.readyState>=2',timeout=60000);p.screenshot(path=str(O/'review-page.png'))
  p.locator('.banks').scroll_into_view_if_needed();p.wait_for_timeout(180);p.screenshot(path=str(O/'animation-banks.png'))
  q=p.evaluate("[...document.querySelectorAll('canvas')].map(c=>{const a=c.getContext('2d').getImageData(0,0,448,448).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==20||a[i+1]!==34||a[i+2]!==52)n++;return n})")
  ck('Foreground, background and dual palm previews display authored pixels',all(n>1000 for n in q),q)
  ck('Review page has no console or page errors',not errors,errors);b.close()
finally:stop()
(O/'delivery.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');raise SystemExit(any(not c['passed']for c in checks))
