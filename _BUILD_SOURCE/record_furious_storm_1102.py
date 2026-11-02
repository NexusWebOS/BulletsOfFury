"""Complete native-input Furious storm fights; no boss HP/phase/timer writes."""
from pathlib import Path
import sys,json,hashlib,http.server,argparse
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
P=argparse.ArgumentParser();P.add_argument('--role',choices=['mini','boss','all'],default='all');args=P.parse_args()
O=R/'_shots/furious_encounters_1102/video';O.mkdir(parents=True,exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=256
base=rec.CAPTURE;rec.OUT=O
rec.CAPTURE=base.replace('gain.gain.value=.5','gain.gain.value=.30')
rec.CAPTURE=rec.CAPTURE.replace('debugFight.spawned=true;warnT=0;', 'debugFight.spawned=true;warnT=0;if(cfg.stage===6){s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;}')
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"storm:b?._fb112?{model:b._fb112.model,phase:b._fb112.phase,attack:b._fb112.attack,open:b._fb112.open,core:b._fb112.core.hp,parts:b._fb112.parts.map(p=>({id:p.id,hp:p.hp})),events:FB112.events.slice(-24)}:null,target:reviewBot.targetInfo,")
for role in ['mini','boss']:
 if args.role not in ['all',role]:continue
 rec.CONFIG=dict(id='razorwake-final'if role=='mini'else'thunderhead-final',stage=6,role=role,kind='siegefortress17'if role=='mini'else'warhive',name='Razorwake / Wind Falcon'if role=='mini'else'Thunderhead / Storm Containment Dreadnought',limit=480,demonstrate=30 if role=='mini'else 35)
 hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in ['index.html','assets/game.js','assets/furious_encounters_art_1102.js','assets/furious_encounters_1102.js']}
 folder=rec.record(6,480);report=json.loads((folder/'report.json').read_text());report['sourceHashes']=hashes;report['sourceStable']=all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items());(folder/'report.json').write_text(json.dumps(report,indent=2))
 print('COMPLETE',role,folder,report['completed'],report['sourceStable'],flush=True)
