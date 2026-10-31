from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_possession_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W
rec.CONFIG=dict(id='dracodia-possession-final-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Toxic portals, UFO possession and whole-arm destruction',limit=480,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const arms=list.filter(t=>/^rb23-(left|right)$/.test(t._retinaId||''));if(arms.length)list=arms;
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", "K.j=!demonstrate&&!rd29Own(b)&&elapsed%1.0<.76;K.c=!demonstrate&&!rd29Own(b)&&!!b;")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"possession:{events:RD71.events.slice(-100),last:RD71.last,time:rd29Own(b)?rd71Time(b):null,breaks:RD71.breaks.map(f=>({side:f.side,t:f.t,next:f.next}))},hostCleared:!!b?._r30&&b._r30.mode==='dr5er23rebirth',target:reviewBot.targetInfo,")
import inspect
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('hostCleared') and completed_at is None:").replace("reason='native defeat'","reason='native first-host defeat'")
exec(source,rec.__dict__)
print('FINAL',rec.record(8,480),flush=True)
