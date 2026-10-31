from pathlib import Path
import sys,http.server,inspect,json
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_demon_1030/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W
grab='--grab' in sys.argv
rec.CONFIG=dict(id='dracodia-claw-grab-polished-1030'if grab else'dracodia-claw-optic-polished-1030',stage=8,role='boss',kind='vileexistence',name='Dracodia / Physical claw capture and fatal throw / native death'if grab else'Dracodia / Symbiote claws, inset missiles and rapid optic blasts',limit=300,demonstrate=500 if grab else 55)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const arms=list.filter(t=>/^rb23-(left|right)$/.test(t._retinaId||''));if(arms.length)list=arms;
 let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", "K.j=!demonstrate&&!rd29Own(b)&&elapsed%1.0<.76;K.c=!demonstrate&&!rd29Own(b)&&!!b;")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"demon:{events:RD72.events.slice(-300),kind:rd72Act(b)?.kind,t:rd72Act(b)?.t,held:!!player._rd72Grab,throwing:!!player._rd72Thrown},hostCleared:!!b?._r30&&b._r30.mode==='dr5er23rebirth',target:reviewBot.targetInfo,")
source=inspect.getsource(rec.record)
if grab:
 a=rec.CAPTURE.index('  const tx=clamp(');z=rec.CAPTURE.index('  A.targetInfo=',a)
 rec.CAPTURE=rec.CAPTURE[:a]+"""  const tx=worldWidth()/2,ty=VH-110;
  K.a=player.x>tx+3;K.d=player.x<tx-3;K.w=player.y>ty+3;K.s=player.y<ty-3;
  K.j=K.c=false;
  const P=rd72Act(b);DBGT.god=!(P?.kind==='grab');
 """+rec.CAPTURE[z:]
 rec.CAPTURE=rec.CAPTURE.replace(' / FURIOUS / GOD BOT / NATIVE HP & PHASES / ',' / FURIOUS / NO GOD DURING GRAB / NATIVE HP / ')
 source=source.replace("if q['bossDefeated'] and completed_at is None:","if any(e['event']=='grab-fatal-throw' for e in q['demon']['events']) and completed_at is None:").replace("q['seconds'] - completed_at > 7","q['seconds'] - completed_at > 4 and not q['player']['dead']").replace("reason='native defeat'","reason='native fatal claw throw'")
else:
 source=source.replace("if q['bossDefeated'] and completed_at is None:","if q.get('hostCleared') and completed_at is None:").replace("reason='native defeat'","reason='native first-host defeat'")
exec(source,rec.__dict__)
folder=rec.record(8,100 if grab else 300)
if grab:
 p=folder/'report.json';r=json.loads(p.read_text());r.update(invulnerable=False,method='Real native Furious attack rotation. Input-only stationary positioning, no firing or enemy HP/phase/timer writes. Native GOD disabled automatically for the entire grab attack; normal player death/weapon loss/life loss/respawn remains in the recording.');p.write_text(json.dumps(r,indent=2))
print('FINAL',folder,flush=True)


