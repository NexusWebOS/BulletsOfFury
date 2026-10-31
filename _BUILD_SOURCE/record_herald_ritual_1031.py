from pathlib import Path
import sys,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/herald_ritual_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;focused='full'not in sys.argv
rec.OUT=W/('ritual-video'if focused else'full-video');rec.CONFIG=dict(id='herald-ritual-1031'if focused else'herald-full-ritual-1031',stage=8,role='mini',kind='heralddeath',name='Herald / red warning, six blade inscriptions, chaotic seal and tornado release',limit=24 if focused else 360,demonstrate=999 if focused else 38)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.6').replace('||Object.entries(Snd.music).find',"||Object.entries(Snd.loops).find(([k,v])=>v.el===this)?.[0]||Object.entries(Snd.music).find")
if focused:
 rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
 rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,',"""await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));subBoss.enter=false;hr28Start(subBoss,'storm');run.bombs=0;HR92.events=[];HH52.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Native attack begins before filming, full HP and native simulation. No HP/phase/timer writes during recording.',entry,difficulty:diffKey,""")
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"ritual:{events:HR92.events.slice(-120),draws:HR92.draws,kind:b?._hd1003?.er28?.kind,t:b?._hd1003?.er28?.t,phase:b?._hd1003?.er28?._hr92?.phase,dark:b?._hd1003?.er28?._hr92?.dark,chaos:HH52.events.slice(-180),stars:PW5.threats.length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,rec.CONFIG['limit']),flush=True)
