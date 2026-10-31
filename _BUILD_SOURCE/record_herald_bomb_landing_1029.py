from pathlib import Path
import sys,http.server
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='herald-bomb-landing',stage=8,role='mini',kind='heralddeath',name='Herald of Death / Actual bomb landing retinas',limit=480,demonstrate=30)
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"landing:{events:HL51.events.slice(-80),kind:subBoss?._hd1003?._hb25?.kind,phase:subBoss?._hd1003?._hb25?.phase,bombs:eBullets.filter(q=>q._hl51&&!q.dead).map(q=>({id:q._hl51,x:q.x,y:q.y,target:q._hb25Bomb.target,at:q._hb25Bomb.at}))},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,480),flush=True)
