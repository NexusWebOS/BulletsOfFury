"""Native Furious full fight, with a deliberate input-only observation turn.
The bot defeats both sentinels, observes all six water attacks, then resumes fire.
No enemy HP/phase writes. GOD prevents player damage. Real RAF and audible audio.
"""
from pathlib import Path
import http.server,json
import record_furious_789_1025 as native
R=Path(__file__).resolve().parents[1]
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1'
http.server.ThreadingHTTPServer.request_queue_size=128
native.OUT=R/'_shots/warden_tidal_1025/full'
native.CAPTURE=native.CAPTURE.replace('A.tick++;',r'''A.tick++;
  const water=boss?._wt25;
  if(cfg.stage===9&&water&&new Set(WT25.events.filter(e=>e.event==='water-attack-complete').map(e=>e.kind)).size<6){
   for(const k of ['a','d','w','s','j','k','c'])K[k]=false;
   const next=water.walls.filter(w=>w.y<player.y+70).sort((a,z)=>z.y-a.y)[0],P=water.attack;
   let tx=next?.gapX??P?.gapX??worldWidth()/2+Math.sin(elapsed*.65)*120;
   for(const g of water.geysers)if(Math.abs(g.x-tx)<50)tx=clamp(tx+(g.x<worldWidth()/2?90:-90),camLeftX()+50,camRightX()-50);
   const ty=VH-65;K.a=player.x>tx+6;K.d=player.x<tx-6;K.w=player.y>ty+6;K.s=player.y<ty-6;return;
  }
''')
native.SNAPSHOT=native.SNAPSHOT.replace('parts:M?',r'''water:b?._wt25?{attack:b._wt25.attack?.kind,age:b._wt25.attack?.t,clock:b._wt25.clock,
   done:WT25.events.filter(e=>e.event==='water-attack-complete').map(e=>e.kind),events:WT25.events.filter(e=>['water-attack-start','water-attack-complete'].includes(e.event)),
   walls:b._wt25.walls.length,geysers:b._wt25.geysers.length,mortars:b._wt25.mortars.length}:null,
  parts:M?''')
folder=native.record(9,600)
p=folder/'report.json';q=json.loads(p.read_text(encoding='utf8'));q['method']=__doc__;p.write_text(json.dumps(q,indent=2),encoding='utf8')
print('FINAL',json.dumps({'folder':str(folder),'complete':q['completed'],'reason':q['reason'],'errors':q['pageErrors']+q['consoleErrors'],'waterKinds':sorted({v for s in q['timeline']for v in (s.get('water')or{}).get('done',[])})}),flush=True)
raise SystemExit(0 if q['completed']and not q['pageErrors']and not q['consoleErrors']and not q['assetErrors']else 1)
