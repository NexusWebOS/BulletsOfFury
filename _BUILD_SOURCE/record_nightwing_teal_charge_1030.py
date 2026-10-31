from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_teal_charge_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='carrier-nightwing-teal-charge-1030',stage=6,role='boss',kind='warhive',name='Harrier to Nightwing / Smaller wind swirl / Teal 1015 charge',limit=360,demonstrate=22)
rec.CAPTURE=rec.CAPTURE.replace('const demonstrate=elapsed<',"const demonstrate=(b?._whv?.mode==='ace'&&elapsed-A.formAt<32)||elapsed<")
rec.SNAPSHOT=rec.SNAPSHOT.replace('P=b?._pb28;','P=b?._pb28,N=b?._whv?.ace;').replace('mode:P?.mode||',"mode:N?.dash?.st||N?._nw28?.mode||b?._carrier17?.phase||P?.mode||").replace('pursuitEvents:typeof PB28',"nightwing:N?{intro:N._nw28?.mode,pose:N._nf29Pose,frame:nw28Frame(b),flash:b.flash,roll:N.roll,somer:N.somer,view:NW30.last,glow:nw32Glow(b),aura:NW32.auraLast,swirl:NW32_ART.wind_rear.cw,windState:b._nw30?.action?{kind:b._nw30.action.kind,phase:b._nw30.action.phase,n:b._nw30.action.n}:null,gusts:eBullets.filter(q=>q._nw30Wind&&!q.dead).map(q=>({x:q.x,y:q.y})),events:NF29.events.slice(-16)}:null,pursuitEvents:typeof PB28")
print('FINAL',rec.record(6,360),flush=True)
