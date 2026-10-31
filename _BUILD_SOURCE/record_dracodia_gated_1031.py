from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_gated_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='gated-possession-1031',stage=8,role='boss',kind='vileexistence',name='Dracodia / actual purple and red metal gates / UFO data-bomb and return',limit=60,demonstrate=999)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.6')
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"introComplete:!!b?._r30&&b._r30.mode==='fight'&&!rd29Own(b),possession:{events:RD71.events.slice(-100),last:RD71.last,time:rd29Own(b)?rd71Time(b):null},target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('introComplete') and completed_at is None:").replace("'native defeat'","'native entrance complete'")
exec(src,rec.__dict__);print('FINAL',rec.record(8,60),flush=True)
