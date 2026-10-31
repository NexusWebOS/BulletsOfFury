from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video'
rec.CONFIG=dict(id='dracodia-evil-chronos-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Corrupted Chronos / Native copied-life checkpoint',limit=180,demonstrate=22)
rec.CAPTURE=rec.CAPTURE.replace("recorder.start(1000);",'')
rec.CAPTURE=rec.CAPTURE.replace("return {entry,difficulty:diffKey,", """v18Enter(boss,2,8);boss._r30.mode='fight';boss.enter=false;boss._noHit=false;
 // Valid final copied-life checkpoint, prepared before the recorder starts.
 const J=j3State(boss);for(const key of Object.keys(J.hp))if(+key!==8)J.hp[key]=0;
 captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'last copied life; form8 retains full native maxHP',entry,difficulty:diffKey,""")
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """if(b&&hb20Own(b))list=list.filter(t=>!/hammer$/.test(t._retinaId||''));
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const Q=b&&hb20Own(b)?hb20State(b):null;
 if(Q?.rage&&A.rageAt==null)A.rageAt=elapsed;
 const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(A.rageAt!=null&&elapsed-A.rageAt<25);""")
# Keep the entire game view, without the old31px footer covering its south edge.
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'")
end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start)
rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"copiedCleared:!!b?._r30&&j3State(b).hp[8]<=0,rd74:{phase:hb20Own(b)?hb20State(b)?.action?.type:null,events:RD74.events.slice(-200),rageAt:reviewBot.rageAt},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('copiedCleared') and completed_at is None:").replace("reason='native defeat'","reason='native copied-hammer-life defeat'")
source=source.replace("'completed': False, 'reason': 'starting'", "'completed': False, 'reason': 'starting', 'checkpoint': 'Final copied-life checkpoint: other lives cleared before capture; active hammer life retains full native HP. No enemy HP/phase/clock writes during footage.'")
exec(source,rec.__dict__)
print('FINAL',rec.record(8,180),flush=True)
