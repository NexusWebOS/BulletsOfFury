from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_luminaire_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='dracodia-luminaire-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Full final main life / Claws and Luminaire',limit=180,demonstrate=12)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace("  let list=b&&!b.dead?",'''  const L=b&&rd78Act(b);
  if(L){
   if(A.lumaSerial!==L.serial){A.lumaSerial=L.serial;A.lumaSide=((A.lumaCount||0)%2)?1:0;A.lumaCount=(A.lumaCount||0)+1;}
   const goal=RD78_ART.safeHints[A.lumaSide],tx=L.left+goal[0],ty=goal[1];
   K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;K.j=K.c=false;
   A.targetInfo={kind:'visible Luminaire warning / move to upper side pocket',x:tx,y:ty};return;
  }
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==0)J.hp[i]=0;
 v18Enter(boss,2,0);boss._r30.mode='fight';boss.enter=boss._noHit=false;
 // Full native final-main-life checkpoint; only preceding lives are cleared before filming.
 const warm=document.createElement('canvas');warm.width=2720;warm.height=2048;const wc=warm.getContext('2d');for(const a of Object.values(RD78_ART.banks))for(const p of a.pages)wc.drawImage(XART.get(p.key),0,0);warm.width=warm.height=1;
 RD78.events=[];RD77.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Final main life retains native5330HP and intact limbs; preceding copied lives cleared before recording.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"mainCleared:!!b&&b.hp<=0,luminaire:{phase:rd78Act(b)?.phase,t:rd78Act(b)?.t,serial:rd78Act(b)?.serial,events:RD78.events.slice(-180),side:reviewBot.lumaSide},clawEvents:RD77.events.slice(-160),target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('mainCleared') and completed_at is None:").replace("reason='native defeat'","reason='native full-HP final-main-life defeat'")
source=source.replace("'completed': False, 'reason': 'starting'","'completed': False, 'reason': 'starting', 'checkpoint':'Full native5330HP final-main-life checkpoint. Preceding copies cleared before capture. Invulnerable input-only bot reacts to Luminaire by ordinary movement to alternate upper side pockets; no recorder HP/phase/clock writes during footage.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,180),flush=True)
