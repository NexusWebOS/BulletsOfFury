from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_gothic_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W
rec.CONFIG=dict(id='herald-gothic-counters-final-1030',stage=8,role='mini',kind='heralddeath',name='Herald / Gothic skulls, missile counters, lethal glass and 3D spiral',limit=480,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const modules=list.filter(t=>/^herald-(gun|wing)/.test(t._retinaId||''));if(modules.length)list=modules;
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const final=b?._hd1003?.hd54,depth=final?hd54Own(b):null;
 if(final&&A.finalAt==null)A.finalAt=elapsed;
 const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(final&&elapsed-A.finalAt<26.5);""")
rec.CAPTURE=rec.CAPTURE.replace("if(elapsed-A.lastEvade>8||A.lastEvade==null)","""if(depth?.phase==='spin'&&depth.t<12){K.j=false;K.c=true;if((run.bombs|0)>0&&elapsed-A.lastMissile>1.3){Input.injectTap('k');A.lastMissile=elapsed;}}
 if(depth?.phase==='spin'&&depth.t>=12&&depth.t<16.5){K.j=true;K.c=false;}
 if(elapsed-A.lastEvade>8||A.lastEvade==null)""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"gothic:{events:HG70.events.slice(-240)},desperation:{events:HD54.events.slice(-220),phase:hd54Own(subBoss)?.phase,t:hd54Own(subBoss)?.t,bank:hd54Own(subBoss)?.bank,frame:hd54Own(subBoss)?.frame,flights:HD54.flights.length},chaos:{events:HH52.events.slice(-120),kind:subBoss?._hd1003?.er28?.kind,phase:subBoss?._hd1003?.er28?.phase},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,480),flush=True)
