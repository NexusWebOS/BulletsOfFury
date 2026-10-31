from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_helicopter_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='dracodia-helicopter-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Digital jungle helicopter / Modular aimed pods',limit=160,demonstrate=22)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace("  let list=b&&!b.dead?",'''  const H=b&&hc79Live(b)?hc79State(b):null,C=H?.action;
  if(C?.kind==='guns'){
   K.a=player.x>C.safeX+3;K.d=player.x<C.safeX-3;K.w=player.y>VH-65+3;K.s=player.y<VH-65-3;K.j=K.c=false;
   A.targetInfo={kind:'visible committed twin-gun lanes / move into gap',x:C.safeX,y:VH-65};return;
  }
  if(C?.kind==='sonic'){
   const tx=camLeftX()+34;K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>VH-65+3;K.s=player.y<VH-65-3;K.j=K.c=false;
   A.targetInfo={kind:'red pressure fronts / move outside broad wave',x:tx,y:VH-65};return;
  }
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)if(i!==1)J.hp[i]=0;
 v18Enter(boss,2,1);boss._r30.mode='fight';boss.enter=boss._noHit=false;boss.x=worldWidth()/2;boss.y=174;boss._r30.v18.home={x:boss.x,y:boss.y};boss._r30.cd=.5;
 // Full native3690HP helicopter checkpoint; other lives cleared before filming.
 const warm=document.createElement('canvas');warm.width=warm.height=2048;const wc=warm.getContext('2d');for(const a of Object.values(HC79_ART.pages)){wc.drawImage(XART.get(a.hitKey),0,0);wc.drawImage(XART.get(Object.keys(HC79_ART.pages).find(k=>HC79_ART.pages[k]===a)),0,0);}warm.width=warm.height=1;
 HC79.events=[];captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Full native3690HP copied helicopter. Other lives cleared before filming. Ordinary-input observer; native HP and clocks throughout capture.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"helicopterCleared:!!b&&j3State(b).hp[1]<=0,helicopter:{age:b?._r30?.v18?.hc79?.age,kind:b?._r30?.v18?.hc79?.action?.kind,t:b?._r30?.v18?.hc79?.action?.t,events:HC79.events.slice(-700)},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('helicopterCleared') and completed_at is None:").replace("reason='native defeat'","reason='native full-HP copied helicopter defeat'")
source=source.replace("'completed': False, 'reason': 'starting'","'completed': False, 'reason': 'starting', 'checkpoint':'Full native3690HP helicopter checkpoint. Other forms cleared before filming. Invulnerable input-only bot reacts to visible committed gun lanes and red pressure waves; no recorder HP/phase/clock writes during footage.'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,160),flush=True)
