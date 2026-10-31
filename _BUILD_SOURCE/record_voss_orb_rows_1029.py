from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/voss_orb_rows_1029';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='rough-riders-voss-fixed-columns',stage=6,role='boss',kind='rebelsquad',name='Rough Riders / Voss parallel spinning cannon rows',limit=480,demonstrate=75)
rec.CAPTURE=rec.CAPTURE.replace(' const audio=Snd._audioCtx();'," const rrBG=drawBG;drawBG=function(){const m=ctx.getTransform();window.rrFilmMatrix=[m.a,m.b,m.c,m.d,m.e,m.f];return rrBG.apply(this,arguments);};\n const audio=Snd._audioCtx();")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"steady:{active:RR43.scope(),camX,matrix:window.rrFilmMatrix},music:{path:Snd.cur?.currentSrc,key:H3.lastMusic,clock:Snd.cur?.currentTime,paused:Snd.cur?.paused,stagexPaused:Snd.music.stagex?.paused},orbRows:{rows:OR44.rows,rounds:OR44.rounds,events:OR44.events.slice(-8),live:(rg4State()?.ord||[]).filter(p=>p._or44&&!p.dead).map(p=>({row:p._or44Row,side:p._or44Side,x:p.x,y:p.y,t:p.t,vx:p.vx,vy:p.vy,origin:p._or44Origin,initial:p._or44Velocity}))},pilotActs:b?._rebels?.ships.map(q=>({key:q.key,act:q.rg4?.act?.kind,phase:q.rg4?.act?.phase,hp:q.hp})),target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,480),flush=True)


