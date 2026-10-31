from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_allied_overflight_1030/record';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='rough-riders-allied-overflight-1030',stage=6,role='boss',kind='rebelsquad',name='Rough Riders / Allied overflight / Depth + shadows / Original Gasline',limit=480,demonstrate=10)
observer="""
 window.flightFilm={ticks:0,maxCruiseStep:0,maxTurboStep:0,outliers:[]};
 const ft=rebelSquadTick;rebelSquadTick=function(b,dt){const protectedIntro=rr33Protected(b),before=b._rebels.ships.map(q=>({q,x:q.x,y:q.y,fast:rr65Fast(q)||vs41Safe(q)}));const r=ft.apply(this,arguments);
 if(!protectedIntro&&!b.dead){flightFilm.ticks++;for(const a of before){const q=a.q;if(!rd21Live(q)||a.y<PLAY.y-30||a.y>VH+30||q.y<PLAY.y-30||q.y>VH+30)continue;const fast=a.fast||rr65Fast(q)||vs41Safe(q),d=Math.hypot(q.x-a.x,q.y-a.y);if(fast)flightFilm.maxTurboStep=Math.max(flightFilm.maxTurboStep,d);else{flightFilm.maxCruiseStep=Math.max(flightFilm.maxCruiseStep,d);if(d>10&&flightFilm.outliers.length<20)flightFilm.outliers.push({key:q.key,d,kind:q.rg4?.act?.kind,phase:q.rg4?.act?.phase});}}}return r;};
 const rrBG=drawBG;drawBG=function(){const m=ctx.getTransform();window.rrFilmMatrix=[m.a,m.b,m.c,m.d,m.e,m.f];return rrBG.apply(this,arguments);};
"""
rec.CAPTURE=rec.CAPTURE.replace(' const audio=Snd._audioCtx();',observer+'\n const audio=Snd._audioCtx();')
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed',"const demonstrate=(!!b?._rebels&&!b._rebels.frIntro?.done)||elapsed")
rec.CAPTURE=rec.CAPTURE.replace('K.c=!demonstrate&&!!b;',"K.c=!demonstrate&&!!b&&elapsed%1.5<.8;if(!demonstrate&&b&&elapsed-(A.lastScan??-10)>1.6){Input.injectTap('c');A.lastScan=elapsed;}")
rec.CAPTURE=rec.CAPTURE.replace('(run.bombs|0)>0','(run.bombs|0)>5')
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"overflight:{events:RR66.events,hulls:RR66.hulls,shadows:RR66.shadows,ships:s6Wing?.ships.map(q=>({key:q.key,x:q.x,y:q.y,phase:q._rm49Flight?.phase,depth:q._rm49Flight?rr66Depth(q):null}))},flight:flightFilm,grid:{t:rg4State()?.rr26?.wall?.t,cast:rg4State()?.rr26?.wall?.cast,dur:rg4State()?.rr26?.wall?.dur},intro:{phase:boss?._rebels?.rough33?.phase,t:boss?._rebels?.rough33?.t,ships:boss?._rebels?.ships.map(q=>({key:q.key,x:q.x,y:q.y,frame:q._rr33Frame})),dialogue:CD27.history.at(-1)},steady:{active:RR43.scope(),frames:RR43.frames,camX,matrix:window.rrFilmMatrix,shake},music:{path:Snd.cur?.currentSrc,key:H3.lastMusic,clock:Snd.cur?.currentTime,paused:Snd.cur?.paused,stagexPaused:Snd.music.stagex?.paused},target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,480),flush=True)
