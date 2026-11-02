"""Current native full fight; hold fire through first natural lightning cycle."""
from pathlib import Path
import sys,http.server,json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_retina_1031/video';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W
rec.CONFIG=dict(id='herald-electric-1031',stage=8,role='mini',kind='heralddeath',
 name='Herald / ground Retinas and red electric impacts',limit=360,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.30')
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed<(cfg.demonstrate??25)',
 "const demonstrate=elapsed<(cfg.demonstrate??25)||!HH52.events.some(e=>e.event==='lightning-strike')||b?._hd1003?.er28?.kind==='rage'")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',
 "chaos:{events:HH52.events.slice(-200),bolts:b?._hd1003?.er28?.bolts,clock:b?._hd1003?.clock},target:reviewBot.targetInfo,")
files=['index.html','assets/herald_chaos_1029.js','assets/herald_electric_art_1031.js','assets/game/levels/stage_08/miniboss/herald_electric_1031/electric_red.png']
def hashes():return{f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in files}
before=hashes();folder=rec.record(8,rec.CONFIG['limit']);after=hashes()
(folder/'source-hashes.json').write_text(json.dumps(dict(before=before,after=after,unchanged=before==after),indent=2))
print('FINAL',folder,flush=True)
