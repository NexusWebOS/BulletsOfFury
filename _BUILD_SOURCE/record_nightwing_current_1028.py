"""Current native Nightwing life, without the retired Carrier replay frames.
Native ace-spawn setup skips the Carrier. Enemy HP, phases and timers are not
written afterward. Furious GOD/input bot, level5 laser and40 native missiles;
the bot withholds its own fire for35s, while normal allies remain active.
"""
from pathlib import Path
import json,time,http.server,hashlib,subprocess,re,sys
import imageio_ffmpeg
import rough_riders_capture_base_1028 as rec
R=Path(__file__).resolve().parents[1];O=R/'_shots/nightwing_shape_1028';(O/'video').mkdir(parents=True,exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=O/'video';rec.CONFIG=dict(id='current-'+time.strftime('%H%M%S'),stage=6,role='boss',kind='warhive',name='Nightwing / Current source-locked aircraft',limit=240,demonstrate=35)
rec.CAPTURE=rec.CAPTURE.replace(' return {entry,difficulty:'," delete boss._carrier17;boss._whv.mode='ace';boss._whv.jets=[];enemies=[];whvAceSpawn(boss);\n return {entry,difficulty:")
rec.SNAPSHOT=rec.SNAPSHOT.replace('P=b?._pb28;','P=b?._pb28,N=b?._whv?.ace;').replace('mode:P?.mode||',"mode:N?.dash?.st||N?._nw28?.mode||P?.mode||").replace('pursuitEvents:typeof PB28',"nightwing:N?{intro:N._nw28?.mode,pose:N._nf29Pose,frame:nw28Frame(b),flash:b.flash,roll:N.roll,somer:N.somer,view:NW30.last,windState:b._nw30?.action?{kind:b._nw30.action.kind,phase:b._nw30.action.phase}:null,wind:NW30.events.some(e=>e.event==='wind-release'),events:NF29.events.slice(-20)}:null,pursuitEvents:typeof PB28")
files=['assets/game.js','assets/nightwing_wind_1028.js','assets/nightwing_wind_art_1028.js','assets/nightwing_flight_1027.js','assets/nightwing_entrance_1027.js']
before={k:hashlib.sha256((R/k).read_bytes()).hexdigest()for k in files}
F=Path(sys.argv[2])if len(sys.argv)>2 and sys.argv[1]=='--finalize'else rec.record(6,240);report=json.loads((F/'report.json').read_text());video=F/'stage6-furious.mp4';FF=imageio_ffmpeg.get_ffmpeg_exe()
decode=subprocess.run([FF,'-hide_banner','-nostats','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(F/'decode.log').write_text(decode.stderr);peak=float(re.search(r'max_volume: ([\-\d.inf]+) dB',decode.stderr)[1]);rows=report['timeline'];duration=rows[-1]['seconds'];shots=[]
for label,condition in [('turn',lambda q:q.get('mode')=='drift'),('cruise',lambda q:q.get('nightwing',{}).get('intro')=='fight'and not q['nightwing'].get('pose')and q['nightwing'].get('flash',0)==0),('hit',lambda q:q.get('nightwing',{}).get('flash',0)>0),('wind',lambda q:(q.get('nightwing',{}).get('windState')or{}).get('kind')=='wind')]:
 candidates=[q for q in rows if q.get('nightwing')and condition(q)]
 if candidates:
  at=candidates[min(2,len(candidates)-1)]['seconds'];subprocess.run([FF,'-v','error','-y','-ss',str(at),'-i',str(video),'-frames:v','1',str(F/(label+'.png'))],check=True);shots.append(dict(name=label,time=at))
cancelled=[q for q in report['failedRequests']if q['failure']=='net::ERR_ABORTED'];failed=[q for q in report['failedRequests']if q['failure']!='net::ERR_ABORTED']
checks=dict(nativeDefeat=report['completed'],decoded=decode.returncode==0,audibleUnclipped=-60<peak<0,realTime=report['audio']['frames']/duration>45,sourceStable=before=={k:hashlib.sha256((R/k).read_bytes()).hexdigest()for k in files},flightObserved=any(s['name']=='turn'for s in shots),normalAndHitObserved={'cruise','hit'}.issubset({s['name']for s in shots}),windObserved=any(s['name']=='wind'for s in shots),noErrors=not report['pageErrors']and not report['consoleErrors']and not report['assetErrors']and not failed and not report['audio']['tapErrors'])
proof=dict(method=__doc__,checks=checks,sourceHashes=before,film=report,expectedRequestCancellations=cancelled,failedRequests=failed,video=video.relative_to(R).as_posix(),decodedPeakDb=peak,duration=duration,shots=shots)
(F/'current-proof.json').write_text(json.dumps(proof,indent=2));(O/'video/latest.json').write_text(json.dumps(dict(folder=F.relative_to(R).as_posix())))
print(json.dumps(dict(video=proof['video'],duration=duration,checks=checks,peak=peak)),flush=True);raise SystemExit(0 if all(checks.values())else 1)
