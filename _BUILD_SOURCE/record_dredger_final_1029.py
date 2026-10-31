from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/dredger_final_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='dredger-final-retinas-wall',stage=7,role='mini',kind='dualscoopdredger',name='Caustic Dredger / protected hull, twin slugs, wall ram and magma',limit=360,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const guns=list.filter(t=>/^gun[LR]$/.test(t._retinaId||''));if(guns.length)list=guns;
  let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const hull=b?._s7mod?.df55Hull;if(hull&&A.hullAt==null)A.hullAt=elapsed;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(hull&&elapsed-A.hullAt<17);""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"dredger:{events:DF55.events.slice(-200),mode:subBoss?._s7mod?.mode,core:subBoss?._s7mod?.core,coreMax:subBoss?._s7mod?.coreMax,parts:subBoss?._s7mod?.parts.map(p=>({id:p.id,hp:p.hp,max:p.max})),hull:subBoss?._s7mod?.df55Hull,phase:subBoss?._s7mod?.dc40?.phase,track:subBoss?._s7mod?.dc40Track,y:subBoss?.y,flights:DF55.flights.length,projectiles:eBullets.filter(q=>q._df55Owner&&!q.dead).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(7,360),flush=True)
