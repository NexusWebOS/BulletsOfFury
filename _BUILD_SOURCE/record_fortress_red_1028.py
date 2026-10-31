from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/fortress_red_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='stage6-miniboss-red-core',stage=6,role='mini',kind='siegefortress17',name='Stage6 Fortress / 8 MODULES / Passive fans + red reactor',limit=300,demonstrate=18)
# Input-only pause on first exposed-core sighting shows both real attack books.
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed<',"if(b?._cargo17Mini&&sc13Open(b)&&A.coreSeenAt==null)A.coreSeenAt=elapsed;\n  const demonstrate=(A.coreSeenAt!=null&&elapsed-A.coreSeenAt<9)||elapsed<")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"fortress:b?._cargo13?{core:b._cargo13.core,open:sc13Open(b),mode:b._cargo13.mode,parts:s6f28Parts(b).map(p=>({id:p.id,hp:p.hp,dead:p.dead})),missiles:SC13.stats.missiles,events:S6F28.events.slice(-12)}:null,solo:{wing:s6Wing?.ships.length||0,ally:!!ally,shots:pBullets.filter(p=>p.ally||p._wingKey).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(6,300),flush=True)
