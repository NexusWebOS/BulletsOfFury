from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/warden_spin_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='warden-front-guns-spin-hops-smooth',stage=7,role='boss',kind='sludgeemperor',name='Toxic Warden / front guns, spinning slams, back-forward hops / no pipe hazards',limit=480,demonstrate=25)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const modules=list.filter(t=>(t._retinaId||'')!=='core');if(modules.length)list=modules;
  let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const core=ws56Ready(b)&&!s7mLive(b._s7mod,'gun').length;if(core&&A.coreAt==null)A.coreAt=elapsed;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(core&&elapsed-A.coreAt<16);""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"warden:{events:WS56.events.slice(-160),mode:boss?._s7mod?.mode,core:boss?._s7mod?.core,parts:boss?._s7mod?.parts.map(p=>({id:p.id,hp:p.hp})),canisters:boss?._s7mod?.er28Canisters.map(p=>({id:p.id,hp:p.hp})),kind:boss?._s7mod?.ws56?.kind,frame:boss?._s7mod?.ws56?.frame,height:boss?._s7mod?.height,phase:boss?._s7mod?.ws56?.cycle,pipeEvents:stage7SluiceEvents().length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(7,480),flush=True)
