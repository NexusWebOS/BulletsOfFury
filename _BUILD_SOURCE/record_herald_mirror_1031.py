"""Native complete Herald fight with the opening mirrored bomber pair."""
from pathlib import Path
import sys,json,hashlib,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_mirror_1031/video';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='herald-mirrored-bombs-1031',stage=8,role='mini',kind='heralddeath',name='Herald / opposite entry and mirrored bomb landings',limit=300,demonstrate=24)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.30')
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"bomber:{kind:b?._hd1003?._hb25?.kind,pass:b?._hd1003?._hb25?.pass,phase:b?._hd1003?._hb25?.phase,path:b?._hd1003?._hb25?.path,escape:b?._hd1003?._hb25?.escapeX,plan:b?._hd1003?._hb25?.plan,events:HB25.events.slice(-180),landings:HL51.events.slice(-100)},target:reviewBot.targetInfo,")
files=['index.html','assets/herald_chaos_1029.js','assets/herald_bomber_1025.js','assets/herald_bomb_landing_1029.js']
def hashes():return{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in files}
before=hashes();folder=rec.record(8,rec.CONFIG['limit']);after=hashes();(folder/'source-hashes.json').write_text(json.dumps(dict(before=before,after=after,unchanged=before==after),indent=2));print('FINAL',folder,flush=True)
