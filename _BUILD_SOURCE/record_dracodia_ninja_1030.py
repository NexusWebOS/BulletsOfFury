from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_ninja_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='dracodia-ninja-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Final main life / Physical ninja claws',limit=130,demonstrate=13)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==0)J.hp[i]=0;
 v18Enter(boss,2,0);boss._r30.mode='fight';boss.enter=boss._noHit=false;
 // Native full5330HP final-main-life checkpoint. Only preceding lives are cleared before capture.
 const warm=document.createElement('canvas');warm.width=warm.height=2048;const warmCtx=warm.getContext('2d');for(const [key,a]of Object.entries(RD77_ART.pages)){warmCtx.drawImage(XART.get(key),0,0);warmCtx.drawImage(XART.get(a.hitKey),0,0);}
 RD77.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Final main life retains native full5330HP and intact limbs; prior copied lives cleared before capture.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"mainCleared:!!b&&b.hp<=0,rd77:{stage:rd77Act(b)?.stage,bank:rd77Act(b)?.bank,frame:rd77Act(b)?.frame,events:RD77.events.slice(-200)},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('mainCleared') and completed_at is None:").replace("reason='native defeat'","reason='native full-HP final-main-life defeat'")
source=source.replace("'completed': False, 'reason': 'starting'","'completed': False, 'reason': 'starting', 'checkpoint':'Final main life, full native5330HP and both limbs; preceding copied lives cleared before filming. No recorder HP/phase/clock writes during capture.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,130),flush=True)
