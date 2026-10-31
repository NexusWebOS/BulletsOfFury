from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_roll_type_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='rough-riders-roll-gasline-final-1030',stage=6,role='boss',kind='rebelsquad',name='Rough Riders / Barrel rolls / Aligned dialogue / Original Gasline',limit=480,demonstrate=10)
rec.CAPTURE=rec.CAPTURE.replace(' const audio=Snd._audioCtx();'," const rrBG=drawBG;drawBG=function(){const m=ctx.getTransform();window.rrFilmMatrix=[m.a,m.b,m.c,m.d,m.e,m.f];return rrBG.apply(this,arguments);};\n const audio=Snd._audioCtx();")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"intro:{phase:boss?._rebels?.rough33?.phase,t:boss?._rebels?.rough33?.t,ships:boss?._rebels?.ships.map(q=>({key:q.key,x:q.x,y:q.y,frame:q._rr33Frame})),dialogue:CD27.history.at(-1)},steady:{active:RR43.scope(),frames:RR43.frames,camX,matrix:window.rrFilmMatrix,shake},music:{path:Snd.cur?.currentSrc,key:H3.lastMusic,clock:Snd.cur?.currentTime,paused:Snd.cur?.paused,stagexPaused:Snd.music.stagex?.paused},target:reviewBot.targetInfo,")
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed',"const demonstrate=(!!b?._rebels&&!b._rebels.frIntro?.done)||elapsed")
rec.CAPTURE=rec.CAPTURE.replace('K.c=!demonstrate&&!!b;',"K.c=!demonstrate&&!!b&&elapsed%1.5<.8;if(!demonstrate&&b&&elapsed-(A.lastScan??-10)>1.6){Input.injectTap('c');A.lastScan=elapsed;}")
rec.CAPTURE=rec.CAPTURE.replace('(run.bombs|0)>0','(run.bombs|0)>5')
rec.SNAPSHOT=rec.SNAPSHOT.replace('intro:{phase:', 'nyx:NY46.events.slice(-20),intro:{phase:')
print('FINAL',rec.record(6,480),flush=True)
