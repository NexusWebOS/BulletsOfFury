from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/host_whole_arms_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='whole-arms-ball-1031',stage=8,role='boss',kind='vileexistence',name='Dracodia / whole-arm strikes and complete torso-to-ball transformation',limit=400,demonstrate=45)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.6')
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const arms=list.filter(t=>/^rb23-(left|right)$/.test(t._retinaId||''));if(arms.length)list=arms;
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const liveArms=b&&rb23Host(b)?rb23Arms(b):[];const exposed=!!b&&rb23Host(b)&&!liveArms.length;
 if(exposed&&A.coreAt==null)A.coreAt=elapsed;
 const armWaiting=liveArms.length===1&&!RD96.events.some(e=>e.event==='whole-arm-strike'&&e.side===liveArms[0].id);
 const demonstrate=elapsed<(cfg.demonstrate??45)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(exposed&&elapsed-A.coreAt<13)||armWaiting;""")
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", "K.j=!demonstrate&&!rd29Own(b)&&elapsed%1.0<.76;K.c=!demonstrate&&!rd29Own(b)&&!!b;")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"wholeArm:{events:RD96.events.slice(-100),draws:RD96.draws,side:rd96Physical(b)?.side,f:rd96Physical(b)?.rd96?.f,fold:rd96Fold(b)?.f,ballReady:b?._r30?.v18?.r25BallReady,parts:b?.parts?.map(p=>({id:p.id,hp:p.hp,max:p.maxhp,destroyed:p.destroyed})),drops:rd73Attack(b)?._rd73?.drops},hostCleared:!!b?._r30&&b._r30.mode==='dr5er23rebirth',target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('hostCleared') and completed_at is None:").replace("'native defeat'","'native first-host defeat'")
exec(src,rec.__dict__);print('FINAL',rec.record(8,400),flush=True)
