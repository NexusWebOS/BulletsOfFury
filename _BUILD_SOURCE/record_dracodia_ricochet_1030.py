from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_ricochet_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W
rec.CONFIG=dict(id='dracodia-ricochet-framed-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Rebounding core and rapid code bombs',limit=400,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const arms=list.filter(t=>/^rb23-(left|right)$/.test(t._retinaId||''));if(arms.length)list=arms;
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const exposed=!!b&&rb23Host(b)&&!rb23Arms(b).length;if(exposed&&A.coreAt==null)A.coreAt=elapsed;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(exposed&&elapsed-A.coreAt<13);""")
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", "K.j=!demonstrate&&!rd29Own(b)&&elapsed%1.0<.76;K.c=!demonstrate&&!rd29Own(b)&&!!b;")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"ricochet:{events:RD73.events.slice(-250),mode:rd73Attack(b)?._rd73?.phase,cycle:rd73Attack(b)?._rd73?.cycle,drops:rd73Attack(b)?._rd73?.drops,bounces:rd73Attack(b)?._rd73?.bounces,live:enemies.filter(e=>!e.dead&&e._d20?.owner===b&&e._d20?.kind==='bomb'&&e._d20.phase!=='erase').length,coreAt:reviewBot.coreAt},hostCleared:!!b?._r30&&b._r30.mode==='dr5er23rebirth',target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('hostCleared') and completed_at is None:").replace("reason='native defeat'","reason='native first-host defeat'")
exec(source,rec.__dict__)
print('FINAL',rec.record(8,400),flush=True)

