from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/neural_night_storm_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='neural-night-storm-1030',stage=8,role='boss',kind='vileexistence',name='Neural Archon / Night-cloud storm and thermal optics',limit=240,demonstrate=12)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace("  let list=b&&!b.dead?",'''  const storm=b&&nb81Act(b);
  if(storm){
   if(A.stormP!==storm){A.stormP=storm;A.stormGoal=player.x<=camLeftX()+viewW()/2?camLeftX()+55:camRightX()-55;}
   const tx=A.stormGoal,ty=VH-65;
   K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;K.j=false;K.c=elapsed>cfg.demonstrate;
   A.targetInfo={kind:'single visible caster asterisk / escape to nearest open flank',x:tx,y:ty};return;
  }
  const P=b&&nb80Act(b);
  if(P){
   if(A.opticP!==P){A.opticP=P;A.opticCount=(A.opticCount||0)+1;A.opticSide=A.opticCount%2?-1:1;}
   const tx=P.origin.x+A.opticSide*110,ty=VH-65;
   K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;K.j=false;K.c=elapsed>cfg.demonstrate;
   if(elapsed>cfg.demonstrate&&(run.bombs|0)>0&&elapsed-A.lastMissile>1.2){Input.injectTap('k');A.lastMissile=elapsed;}
   A.targetInfo={kind:'visible eye-laser warning / move to alternating safe flank',x:tx,y:ty};return;
  }
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==6)J.hp[i]=0;
 v18Enter(boss,2,6);boss._r30.mode='fight';boss.enter=boss._noHit=false;boss._r30.v18.arenaPhase=2;boss.x=worldWidth()/2;boss.y=220;boss._r30.v18.home={x:boss.x,y:boss.y};boss._r30.cd=.35;
 const warm=document.createElement('canvas');warm.width=1024;warm.height=1024;const wc=warm.getContext('2d');for(const key of [...nb80Keys(),...nb81Keys()])wc.drawImage(XART.get(key),0,0);warm.width=warm.height=1;
 NB80.events=[];NB81.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Full native4510HP Neural Archon. Other copied/main lives cleared before capture. No recorder HP/phase/clock writes during recording.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"brainCleared:!!b&&j3State(b).hp[6]<=0,storm:{events:NB81.events.slice(-160),dim:NB81.dim,scene:NB81.scene,draws:NB81.draws},optics:{type:b?._r30?.v18?.attack?.type,t:b?._r30?.v18?.attack?.t,tell:b?._r30?.v18?.attack?.tell,eyes:nb80Act(b)?nb23Eyes(b):[],events:NB80.events.slice(-120),side:reviewBot.opticSide,draws:NB80.draws},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('brainCleared') and completed_at is None:").replace("reason='native defeat'","reason='native full-HP Neural Archon defeat'")
source=source.replace("'completed': False, 'reason': 'starting'","'completed': False, 'reason': 'starting', 'checkpoint':'Full native4510HP Neural Archon; previous lives cleared before filming. Invulnerable input-only observer follows visible caster warnings to an open flank and eye warnings to alternate flanks, then fights with native weapons. No recorder HP/phase/clock writes.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,240),flush=True)
