from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/tidal_warning_signs_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='tidal-metal-warning-signs-1030',stage=9,role='boss',kind='tidalfusion',name='Tidal Sovereign / Stage2 metal warning signs / water-wall attack excerpt',limit=45,demonstrate=45)
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const half=b?._ts58?.half;if(half&&A.halfAt==null)A.halfAt=elapsed;
 const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(half&&elapsed-A.halfAt<23);""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"tidal:{events:TS58.events.slice(-200),mode:b?._ts58?.mode,phase:b?._ts58?.phase,half:b?._ts58?.half,charge:b?._ts58?.charge,protected:b?._ts58?.protected,x:b?.x,y:b?.y,markers:b?._ts58?.markers.length,geysers:b?._ts58?.geysers.length,waves:b?._ts58?.waves.length,largeWaves:b?._ts58?.waves.filter(w=>!w.small).map(w=>({x:w.x,y:w.y,t:w.t,speed:w.speed,frame:ts58WaveFrame(w)})),grenades:b?._ts58?.grenades?.length,pendingRain:b?._ts58?.pendingRain?.length,bursts:b?._ts58?.bursts?.length,fanPhase:b?Math.floor(b._ts58.clock*16)%16:0,projectiles:eBullets.filter(q=>q._ts58Owner&&!q.dead).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(9,45),flush=True)
