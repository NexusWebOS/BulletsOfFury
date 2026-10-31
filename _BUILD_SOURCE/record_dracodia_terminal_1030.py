from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_terminal_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='dracodia-terminal-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Terminal collapse and Fury flight reunion',limit=80,demonstrate=0)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','').replace('  let list=b&&!b.dead?', '''
  if(b&&dr5State(b)?.deathStarted){for(const key of ['a','d','w','s','j','c'])K[key]=false;A.targetInfo={kind:'Observe native protected terminal death, blue gate and squad return'};return;}
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''const J=j3State(boss);for(const i of V18.forms)J.hp[i]=0;J.hp[0]=55;
 v18Enter(boss,2,0);boss._r30.mode='fight';boss.enter=boss._noHit=false;boss._r30.v18.arenaPhase=0;boss.x=worldWidth()/2;boss.y=190;boss._r30.v18.home={x:boss.x,y:boss.y};boss._r30.cd=2;boss.hp=55;boss.parts[0].hp=55;
 for(const part of boss.parts)if(part.id!=='core'){part.hp=0;part.destroyed=true;}
 debugFight=null;run.mode='campaign';run.bombs=0;player.x=worldWidth()/2;player.y=VH-65;RD84.events=[];
 const warm=document.createElement('canvas');warm.width=1024;warm.height=1024;const warmCtx=warm.getContext('2d');for(const k of rd84Keys())warmCtx.drawImage(XART.get(k),0,0);warm.width=warm.height=1;
 captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Native final-hit checkpoint: main core55HP, all other life pools and limbs depleted before capture. Invulnerable input-only pilot fires the real final shots. No HP/phase/clock writes during filming.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"terminalComplete:!!b&&b._r30.mode==='done',terminal:{phase:dr5State(b)?.rd84?.phase,age:dr5State(b)?.rd84?.age,squad:dr5State(b)?.rd84?.squad,events:RD84.events.slice(-400),draws:RD84.draws,parallax:RD84.parallax,rewarded:b?._r30?.rewarded},target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('terminalComplete') and completed_at is None:").replace("reason='native defeat'","reason='native terminal death, reunion and victory handoff'")
exec(source,rec.__dict__);print('FINAL',rec.record(8,80),flush=True)
