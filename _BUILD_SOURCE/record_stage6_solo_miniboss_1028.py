from pathlib import Path
import sys,http.server,json
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage6_solo_miniboss_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='stage6-miniboss-solo-final',stage=6,role='mini',kind='siegefortress17',name='Stage6 Siege Fortress / SOLO / No NPC allies',limit=300,demonstrate=20)
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"solo:{active:s6SoloActive(),wing:s6Wing?.ships.length||0,ally:!!ally,shots:pBullets.filter(p=>p.ally||p._wingKey).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,300),flush=True)
