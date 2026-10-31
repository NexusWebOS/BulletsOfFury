from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_return_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video'
rec.CONFIG=dict(id='dracodia-return-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Defeated copy to rebuilt main arena / Focused native checkpoint',limit=60,demonstrate=3)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''v18Enter(boss,2,0);const J=j3State(boss);
 // Focused checkpoint: a previously damaged home limb and280HP remaining on the brain copy.
 // All preparation precedes MediaRecorder. Other life pools remain at native full HP.
 const arm=J.modules[0].find(p=>p.id==='left');arm.hp=0;arm.destroyed=true;
 J.hp[6]=280;v18Enter(boss,2,6);boss._r30.mode='fight';boss.enter=boss._noHit=false;
 RD76.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Brain copy280HP; missing cached left arm; other lives full. Prepared before capture.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"returnComplete:RD76.events.some(e=>e.event==='return-complete'),returnEvents:RD76.events.slice(),returnTime:rd76State(b)?.t,target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('returnComplete') and completed_at is None:").replace("q['seconds'] - completed_at > 7","q['seconds'] - completed_at > 3").replace("reason='native defeat'","reason='native copied-life defeat and main-arena rebuild'")
source=source.replace("'completed': False, 'reason': 'starting'", "'completed': False, 'reason': 'starting', 'checkpoint': 'Focused native checkpoint: brain copy280HP and missing main left arm, prepared before recording. Other life pools full; no recorder HP/phase/clock writes during footage.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,60),flush=True)
