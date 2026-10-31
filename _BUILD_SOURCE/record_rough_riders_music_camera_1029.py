from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/rough_riders_music_camera_1029';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='rough-riders-boss6-steady',stage=6,role='boss',kind='rebelsquad',name='Rough Riders / Stage6 boss score / Steady camera',limit=480,demonstrate=10)
rec.CAPTURE=rec.CAPTURE.replace(' const audio=Snd._audioCtx();'," const rrBG=drawBG;drawBG=function(){const m=ctx.getTransform();window.rrFilmMatrix=[m.a,m.b,m.c,m.d,m.e,m.f];return rrBG.apply(this,arguments);};\n const audio=Snd._audioCtx();")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"steady:{active:RR43.scope(),frames:RR43.frames,camX,matrix:window.rrFilmMatrix,shake},music:{path:Snd.cur?.currentSrc,key:H3.lastMusic,clock:Snd.cur?.currentTime,paused:Snd.cur?.paused,stagexPaused:Snd.music.stagex?.paused},target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,480),flush=True)
