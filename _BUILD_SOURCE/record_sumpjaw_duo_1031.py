from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/sumpjaw_duo_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='sumpjaw-duo-1031',stage=7,role='mini',kind='dualscoopdredger',name='Sumpjaw pair / Two independent gill-heart budgets and local health bars',limit=180,demonstrate=25)
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"sumpjaw:b?._sj98?{actors:b._sj98.actors.map(a=>({i:a.i,hp:a.hp,maxhp:a.maxhp,phase:a.phase,x:a.x,y:a.y,pools:a.pools,dead:a.dead})),events:SJ98.events.slice(-80),draws:SJ98.draws}:null,target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("'s=>{run.stage=s;stageLoadBegin(s);}'","'s=>{diffKey=\"furious\";run.stage=s;stageLoadBegin(s);}'")
exec(src,rec.__dict__);print('FINAL',rec.record(7,180),flush=True)
