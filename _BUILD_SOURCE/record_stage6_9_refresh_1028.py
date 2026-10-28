"""Sequential fresh Stage6–9 native fight recording and decoded-media checks.
Furious, Cole level5 Laser/40 missiles and labelled GOD/input bot. Native
entrances, HP/parts, attack books, transformations and defeats are retained.
No enemy HP/phase/timer writes after the fresh native encounter spawn.
"""
from pathlib import Path
import argparse,json,time,hashlib,subprocess,re,http.server,traceback
import imageio_ffmpeg
import rough_riders_capture_base_1028 as rec

R=Path(__file__).resolve().parents[1];BASE=R/'_shots/stage6_9_refresh_1028';BASE.mkdir(parents=True,exist_ok=True)
JOBS=[
 dict(id='stage6-miniboss',stage=6,role='mini',kind='siegefortress17',name='Siege Fortress / Native batteries and reactor',limit=480,demonstrate=25),
 dict(id='stage6-carrier-nightwing',stage=6,role='boss',kind='warhive',name='Harrier Carrier and Nightwing / Complete native fight',limit=600,demonstrate=35),
 dict(id='stage6-rough-riders',stage=6,role='boss',kind='rebelsquad',name='The Rough Riders / Current entrance and full fight',limit=720,demonstrate=230),
 dict(id='stage7-miniboss',stage=7,role='mini',kind='dualscoopdredger',name='Caustic Dredger / Current ram and toxic turrets',limit=480,demonstrate=30),
 dict(id='stage7-boss',stage=7,role='boss',kind='sludgeemperor',name='Toxic Portal Warden / Current lunge, shadow and escape',limit=600,demonstrate=30),
 dict(id='stage8-miniboss',stage=8,role='mini',kind='heralddeath',name='Herald of Death / Complete current fight',limit=600,demonstrate=30),
 dict(id='stage8-final',stage=8,role='boss',kind='vileexistence',name='Dracodia / First host, rebirth and all final forms',limit=1800,demonstrate=35),
 dict(id='stage9-miniboss',stage=9,role='mini',kind='voidhorizon',name='Event Horizon / Complete current fight',limit=600,demonstrate=30),
 dict(id='stage9-boss',stage=9,role='boss',kind='tidalfusion',name='Warp Sentinels and Tidal Fusion / Complete native fight',limit=720,demonstrate=30),
]
parser=argparse.ArgumentParser();parser.add_argument('--run');parser.add_argument('--jobs',default='all');args=parser.parse_args()
O=Path(args.run).resolve()if args.run else BASE/time.strftime('%H%M%S');assert O.is_relative_to(BASE.resolve());O.mkdir(parents=True,exist_ok=True)
(BASE/'latest.json').write_text(json.dumps(dict(folder=O.relative_to(R).as_posix())))
stateFile=O/'batch.json';state=json.loads(stateFile.read_text())if stateFile.exists()else dict(method=__doc__,jobs={})
runtime=['index.html']+[str(p.relative_to(R))for p in(R/'assets').glob('*.js')]
def hashes():return{f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in runtime}
if not(O/'runtime-before.json').exists():(O/'runtime-before.json').write_text(json.dumps(hashes(),indent=2))
originalCap=rec.CAPTURE;originalSnap=rec.SNAPSHOT;FF=imageio_ffmpeg.get_ffmpeg_exe();selected={j['id']for j in JOBS}if args.jobs=='all'else set(args.jobs.split(','))
http.server.ThreadingHTTPServer.request_queue_size=256
for job in JOBS:
 if job['id']not in selected:continue
 if state['jobs'].get(job['id'],{}).get('passed'):continue
 rec.OUT=O;rec.CONFIG=job;rec.CAPTURE=originalCap
 # Reduces capture clipping only; the game's shared audio mix is unchanged.
 rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.30')
 rec.SNAPSHOT=originalSnap.replace('stage:run.stage,difficulty:diffKey,',"stage:run.stage,difficulty:diffKey,name:b?.name,")
 rec.SNAPSHOT=rec.SNAPSHOT.replace('pursuitEvents:typeof PB28',"carrierState:b?._whv?{mode:b._whv.mode,phase:b._carrier17?.phase,fanMask:b._hc32?.fanMask,exposed:b._hc32?.exposed,core:b._hc32?.core,ace:b._whv.ace?{mode:b._whv.ace._nw28?.mode,dash:b._whv.ace.dash?.st,pose:b._whv.ace._nf29Pose,frame:nw28Frame(b),flash:b.flash,view:NW30.last,wind:b._nw30?.action?.kind}:null}:null,rebelState:b?._rebels?{intro:RR33.last?.phase,fleet:b._rebels.gang1004?.rd21?.fleet?.phase,wall:b._rebels.gang1004?.rr26?.wall?{t:b._rebels.gang1004.rr26.wall.t}:null,attacks:b._rebels.ships.map(q=>({key:q.key,kind:q.rg4?.act?.kind,phase:q.rg4?.act?.phase,hp:q.hp,dead:q.dead}))}:null,pursuitEvents:typeof PB28")
 rec.SNAPSHOT=rec.SNAPSHOT.replace('hp:q.hp,dead:q.dead}))}:null,pursuitEvents', 'hp:q.hp,dead:q.dead,cd:q.rg4?.cd,armed:q.rg4?.armed,role:q.rg4?.role,stun:q.stun}))}:null,pursuitEvents')
 before=hashes();state['active']=job['id'];stateFile.write_text(json.dumps(state,indent=2));print('JOB_START',job['id'],flush=True)
 try:
  folder=rec.record(job['stage'],job['limit']);report=json.loads((folder/'report.json').read_text());video=folder/f'stage{job["stage"]}-furious.mp4'
  decoded=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(folder/'decode.log').write_text(decoded.stderr)
  match=re.search(r'max_volume: ([\-\d.inf]+) dB',decoded.stderr);peak=float(match[1])if match else-999;rows=report['timeline'];seconds=rows[-1]['seconds'];fps=report['audio']['frames']/seconds
  aborted=[q for q in report['failedRequests']if q['failure']=='net::ERR_ABORTED'];failed=[q for q in report['failedRequests']if q['failure']!='net::ERR_ABORTED']
  checks=dict(nativeComplete=report['completed'],decoded=decoded.returncode==0,audibleUnclipped=-60<peak<0,realTime=fps>45,sourceStable=before==hashes(),noGameErrors=not report['pageErrors']and not report['consoleErrors']and not report['assetErrors']and not failed and not report['audio']['tapErrors']and not rows[-1].get('botErrors'))
  if job['id']=='stage6-carrier-nightwing':checks['carrierAndNightwingSeen']=any(q.get('carrierState',{}).get('mode')=='ace'for q in rows if q.get('carrierState'))and any(q.get('carrierState',{}).get('exposed')for q in rows if q.get('carrierState'))
  if job['id']=='stage6-rough-riders':
   checks['allFiveNativePilotsSeen']=any(len(q.get('rebels')or[])==5 for q in rows)
   seen={(a['key'],a.get('kind'))for q in rows for a in(q.get('rebelState')or{}).get('attacks',[])if a.get('kind')}
   checks['allFivePersonalBooksSeen']=all(any(a==key for a,k in seen)for key in['voss','nyx','rook','kaia','jace'])
   checks['rookDashAndSpinSeen']=('rook','rk38dash')in seen and('rook','rk38spin')in seen
  if job['id']=='stage8-final':checks['nativeFormLedgerSeen']=any(q.get('dracodia',{}).get('pools')for q in rows if q.get('dracodia'))
  proof=dict(job=job,video=video.relative_to(R).as_posix(),seconds=seconds,fps=fps,decodedPeakDb=peak,checks=checks,expectedRequestCancellations=aborted,failedRequests=failed,sourceHashes=before,report=report)
  (folder/'proof.json').write_text(json.dumps(proof,indent=2));state['jobs'][job['id']]=dict(folder=folder.relative_to(R).as_posix(),video=proof['video'],seconds=seconds,fps=fps,peak=peak,checks=checks,passed=all(checks.values()))
  print('JOB_DONE',job['id'],json.dumps(state['jobs'][job['id']]),flush=True)
 except Exception as e:
  state['jobs'][job['id']]=dict(passed=False,error=str(e));(O/(job['id']+'-exception.txt')).write_text(traceback.format_exc());print('JOB_ERROR',job['id'],str(e),flush=True)
 stateFile.write_text(json.dumps(state,indent=2))
state['active']=None;state['runtimeAfter']=hashes();stateFile.write_text(json.dumps(state,indent=2));print('BATCH_DONE',json.dumps({k:v.get('passed')for k,v in state['jobs'].items()}),flush=True)
raise SystemExit(0 if all(state['jobs'].get(k,{}).get('passed')for k in selected)else 1)
