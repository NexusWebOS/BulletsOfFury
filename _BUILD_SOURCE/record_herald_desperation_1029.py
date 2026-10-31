from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_desperation_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='herald-final-desperation-clean',stage=8,role='mini',kind='heralddeath',name='Herald of Death / 20% skull desperation and depth rollers',limit=480,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const modules=list.filter(t=>/^herald-(gun|wing)/.test(t._retinaId||''));if(modules.length)list=modules;
  let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const final=b?._hd1003?.hd54;
  if(final&&A.finalAt==null)A.finalAt=elapsed;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(final&&elapsed-A.finalAt<21.8);""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"desperation:{events:HD54.events.slice(-170),phase:subBoss?._hd1003?.er28?._hd54?subBoss._hd1003.er28.phase:null,t:subBoss?._hd1003?.er28?.t,pulse:subBoss?._hd1003?.er28?.pulse,spin:subBoss?._hd1003?.er28?.spin,bank:subBoss?._hd1003?.er28?.bank,frame:subBoss?._hd1003?.er28?.frame,flights:HD54.flights.length,rounds:eBullets.filter(q=>q._hd54&&!q.dead).length},spell:{events:HS53.events.slice(-100),caster:!!subBoss?._hd1003?.hs53Caster,phase:subBoss?._hd1003?.er28?._hs53?subBoss._hd1003.er28.phase:null},chaos:{kind:subBoss?._hd1003?.er28?.kind,phase:subBoss?._hd1003?.er28?.phase,flight:subBoss?._hd1003?._hb25?.phase},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,480),flush=True)
