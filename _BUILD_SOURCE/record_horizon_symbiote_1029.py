from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/horizon_symbiote_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='horizon-symbiote-final-fight',stage=9,role='mini',kind='voidhorizon',name='Black Event Horizon / symbiote lasers, 360 eye sweep, aqua spinning dashes',limit=420,demonstrate=37)
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const half=b?._eh57?.half;if(half&&A.halfAt==null)A.halfAt=elapsed;
 const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(half&&elapsed-A.halfAt<24);""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"horizon:{events:EH57.events.slice(-180),mode:b?._eh57?.mode,phase:b?._eh57?.phase,half:b?._eh57?.half,frame:b?._eh57?.frame,eye:b?s5924Eye(b):null,body:b?{x:b._s9rift?.core.x,y:b._s9rift?.core.y}:null,beams:b?._eh57?.beams.length,projectiles:eBullets.filter(q=>q._eh57Owner&&!q.dead).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(9,420),flush=True)
