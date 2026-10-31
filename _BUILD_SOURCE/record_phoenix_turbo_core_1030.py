from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/phoenix_turbo_core_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='phoenix-turbo-core-1030',stage=8,role='boss',kind='vileexistence',name='Corrupted Phoenix / Twin turbo cannons and single core beam',limit=250,demonstrate=14)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace("  let list=b&&!b.dead?",'''  const P=b&&ph82Full(b)&&ph21State(b).action;
  if(P?._ph82&&P.kind==='core'&&P.locked){
   const at=ph82Socket(b,'core'),angle=PH82_ART.directions[P.dir]*Math.PI/180,lane=at.x+Math.cos(angle)/Math.sin(angle)*(player.y-at.y);
   if(A.coreP!==P){A.coreP=P;A.coreGoal=clamp(lane+(player.x<lane?-90:90),camLeftX()+35,camRightX()-35);}
   const tx=A.coreGoal,ty=VH-65;K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;K.j=false;K.c=elapsed>cfg.demonstrate;
   A.targetInfo={kind:'visible committed core warning / move out of beam lane',x:tx,y:ty};return;
  }
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==2)J.hp[i]=0;
 v18Enter(boss,2,2);boss._r30.mode='fight';boss.enter=boss._noHit=false;boss._r30.v18.arenaPhase=2;boss.x=worldWidth()/2;boss.y=174;boss._r30.v18.home={x:boss.x,y:boss.y};ph21State(boss).cool=.35;
 const warm=document.createElement('canvas');warm.width=1024;warm.height=1024;const wc=warm.getContext('2d');for(const key of ph82Keys())wc.drawImage(XART.get(key),0,0);warm.width=warm.height=1;
 PH82.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Full native4100HP Phoenix. Other copied/main lives cleared before filming. No recorder HP/phase/clock writes during capture.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"phoenixCleared:!!b&&j3State(b).hp[2]<=0,phoenix:{stage:ph21State(b)?.stage,type:ph21State(b)?.action?.kind||ph21State(b)?.action?.mode,t:ph21State(b)?.action?.t,tell:ph21State(b)?.action?.tell,events:PH82.events.slice(-500),arena:PH82.arena,draws:PH82.draws},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('phoenixCleared') and completed_at is None:").replace("reason='native defeat'","reason='native full-HP Phoenix defeat'")
source=source.replace("'completed': False, 'reason': 'starting'","'completed': False, 'reason': 'starting', 'checkpoint':'Full native4100HP Phoenix; other lives cleared before filming. Invulnerable input-only observer follows visible core warnings and uses normal weapon/Retina inputs. No recorder HP/phase/clock writes during filming.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,250),flush=True)
