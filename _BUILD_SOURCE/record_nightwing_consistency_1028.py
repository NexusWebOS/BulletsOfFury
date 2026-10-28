from pathlib import Path
import sys,json,http.server,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_consistency_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='nightwing-identity',stage=6,role='boss',kind='warhive',name='Nightwing / Consistent Hull / Native Ace Life',limit=200,demonstrate=35)
rec.CAPTURE=rec.CAPTURE.replace(' return {entry,difficulty:'," delete boss._carrier17;boss._whv.mode='ace';boss._whv.jets=[];enemies=[];whvAceSpawn(boss);\n return {entry,difficulty:")
rec.SNAPSHOT=rec.SNAPSHOT.replace('P=b?._pb28;','P=b?._pb28,N=b?._whv?.ace;').replace('mode:P?.mode||',"mode:N?.dash?.st||N?._nw28?.mode||P?.mode||").replace('pursuitEvents:typeof PB28',"nightwing:N?{intro:N._nw28?.mode,pose:N._nf29Pose,frame:nw28Frame(b),flash:b.flash,roll:N.roll,somer:N.somer,view:NW30.last,shots:NW30.events.filter(e=>e.event==='turret-shot').length,wind:NW30.events.some(e=>e.event==='wind-release'),events:NF29.events.slice(-20)}:null,pursuitEvents:typeof PB28")
files=['index.html','assets/game.js','assets/nightwing_wind_1028.js','assets/nightwing_flight_1027.js','assets/nightwing_entrance_1027.js','assets/nightwing_wind_art_1028.js','assets/game/levels/stage_06/boss/nightwing_wind_1028/whole_identity_1028b.png'];(W/'source-hashes.json').write_text(json.dumps({k:hashlib.sha256((R/k).read_bytes()).hexdigest()for k in files},indent=2));print('FINAL',rec.record(6,200),flush=True)
