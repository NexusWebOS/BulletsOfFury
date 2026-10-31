from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/luminaire_plasma_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='luminaire-plasma-mine-1031',stage=8,role='boss',kind='vileexistence',name='Dracodia / Full final main life / Ground Retina, thrown plasma mine and rising red dome',limit=240,demonstrate=22)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace('  let list=b&&!b.dead?', '''  const L=b&&rd78Act(b);
  if(L?._rd97){const tx=L.land.x,ty=RD97_ART.safeY;K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;K.j=K.c=false;A.targetInfo={kind:'Ground Retina / escape north above rising plasma dome',x:tx,y:ty};return;}
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);","const demonstrate=elapsed<(cfg.demonstrate??22)||(J&&A.firstVisit&&elapsed-A.formAt<5)||!RD97.events.some(e=>e.event==='plasma-recovery');")
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==0)J.hp[i]=0;
 v18Enter(boss,2,0);boss._r30.mode='fight';boss.enter=boss._noHit=false;
 const warm=document.createElement('canvas');warm.width=3328;warm.height=928;const wc=warm.getContext('2d');for(const a of Object.values(RD97_ART.banks))for(const p of a.pages)wc.drawImage(XART.get(p.key),0,0);warm.width=warm.height=1;
 RD97.events=[];RD78.events=[];RD78.draws={};captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Native full5330HP final-main-life checkpoint, intact limbs; preceding copied lives cleared before capture. No recorder HP, phase or timer writes during filming.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"mainCleared:!!b&&b.hp<=0,plasma:{phase:rd78Act(b)?.phase,t:rd78Act(b)?.t,serial:rd78Act(b)?.serial,land:rd78Act(b)?.land,radius:rd78Act(b)?.radius,height:rd78Act(b)?.height,events:RD97.events.slice(-160),draws:RD97.draws,retired:RD78.draws},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('mainCleared') and completed_at is None:").replace("'native defeat'","'native full-HP final-main-life defeat'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,240),flush=True)
