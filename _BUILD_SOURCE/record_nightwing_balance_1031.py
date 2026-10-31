from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='nightwing-health-review-1031',stage=6,role='boss',kind='warhive',name='Carrier and Nightwing / Furious / native modular hull and revised ace budget',limit=260,demonstrate=24)
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"futureAce:b?._whv?.aceMax,target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("'s=>{run.stage=s;stageLoadBegin(s);}'","'s=>{diffKey=\"furious\";run.stage=s;stageLoadBegin(s);}'")
exec(src,rec.__dict__);print('FINAL',rec.record(6,260),flush=True)
