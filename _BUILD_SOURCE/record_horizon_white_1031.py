from pathlib import Path
import sys,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/horizon_white_optics_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W/'video';rec.CONFIG=dict(id='horizon-white-optics-1031',stage=9,role='mini',kind='voidhorizon',name='Black Event Horizon / white core cannon and synchronous continuous spin',limit=360,demonstrate=34)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.6')
rec.CAPTURE=rec.CAPTURE.replace('||Object.entries(Snd.music).find',"||Object.entries(Snd.loops).find(([k,v])=>v.el===this)?.[0]||Object.entries(Snd.music).find")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const half=b?._eh57?.half;if(half&&A.halfAt==null)A.halfAt=elapsed;
 const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(half&&elapsed-A.halfAt<27);""")
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"horizon:{revision:EH91.revision,events:EH57.events.slice(-180),mode:b?._eh57?.mode,phase:b?._eh57?.phase,half:b?._eh57?.half,angle:b?._eh57?.angle,clock:b?._eh57?.clock,frame:b?._eh57?.frame,eye:b?s5924Eye(b):null,beams:b?._eh57?.beams.length,stars:PW5.threats.length,markerDraws:PW5.draws},target:reviewBot.targetInfo,")
print('FINAL',rec.record(9,360),flush=True)
