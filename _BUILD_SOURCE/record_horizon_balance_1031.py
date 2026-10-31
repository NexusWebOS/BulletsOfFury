from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='horizon-burst-balance-1031',stage=9,role='mini',kind='voidhorizon',name='Event Horizon / Furious / white laser bursts and UFO phase',limit=170,demonstrate=24)
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"horizon:b?._eh57?{mode:b._eh57.mode,phase:b._eh57.phase,angle:b._eh57.angle,beams:b._eh57.beams.length,half:b._eh57.half,profile:b._eh57.profile,events:EH57.events.slice(-60)}:null,target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("'s=>{run.stage=s;stageLoadBegin(s);}'","'s=>{diffKey=\"furious\";run.stage=s;stageLoadBegin(s);}'")
exec(src,rec.__dict__);print('FINAL',rec.record(9,170),flush=True)
