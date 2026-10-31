from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_chaos_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='herald-chaos-verified',stage=8,role='mini',kind='heralddeath',name='Herald of Death / Re-authored chaos attacks',limit=480,demonstrate=85)
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", """K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;
  const E=b?._hd1003?.er28;
  if(demonstrate&&E?.kind==='nuke'&&E.emitted>=5&&E.emitted<=12){
   const skull=[...HH52.skulls].filter(q=>!q.dead&&q.y>VH*.48&&q.y<VH-25).sort((a,b)=>b.y-a.y)[0];
   if(skull){K.a=player.x>skull.x+6;K.d=player.x<skull.x-6;K.j=elapsed%1.0<.65;}
  }""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"chaos:{events:HH52.events.slice(-120),kind:subBoss?._hd1003?.er28?.kind,age:subBoss?._hd1003?.er28?.t,phase:subBoss?._hd1003?.er28?.phase,clip:subBoss?._hd1003?.er28?.clip,flight:subBoss?._hd1003?._hb25?.phase,skulls:[...HH52.skulls].filter(q=>!q.dead).map(q=>({x:q.x,y:q.y,level:q._hh52Level})),bolts:subBoss?._hd1003?.er28?.bolts,projectiles:eBullets.filter(q=>q._heraldOwner1003===subBoss&&!q.dead).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,480),flush=True)
