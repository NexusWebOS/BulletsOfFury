from pathlib import Path
import sys,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_spellcaster_1029/record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256
rec.OUT=W;rec.CONFIG=dict(id='herald-spellcaster-committed',stage=8,role='mini',kind='heralddeath',name='Herald of Death / Skull caster and ruby-glass spell',limit=480,demonstrate=107)
rec.CAPTURE=rec.CAPTURE.replace("let target=list.find(t=>targetKey(t)===A.targetKey);", """const modules=list.filter(t=>/^herald-(gun|wing)/.test(t._retinaId||''));
  if(modules.length)list=modules;
  let target=list.find(t=>targetKey(t)===A.targetKey);""")
rec.CAPTURE=rec.CAPTURE.replace("const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);", """const caster=b?._hd1003?.hs53Caster;
  if(caster&&A.casterAt==null)A.casterAt=elapsed;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5)||(caster&&elapsed-A.casterAt<13);""")
rec.CAPTURE=rec.CAPTURE.replace("K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;", """K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;
  const E=b?._hd1003?.er28;
  if(demonstrate&&E?.kind==='nuke'&&E.emitted>=5&&E.emitted<=12&&!caster){
   const skull=[...HH52.skulls].filter(q=>!q.dead&&q.y>VH*.48&&q.y<VH-25).sort((a,b)=>b.y-a.y)[0];
   if(skull){K.a=player.x>skull.x+6;K.d=player.x<skull.x-6;K.j=elapsed%1.0<.65;}
  }""")
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"spell:{events:HS53.events.slice(-150),caster:!!subBoss?._hd1003?.hs53Caster,phase:subBoss?._hd1003?.er28?._hs53?subBoss._hd1003.er28.phase:null,t:subBoss?._hd1003?.er28?.t,orbs:[...HS53.orbs].filter(q=>!q.dead).length,rounds:eBullets.filter(q=>q._hs53&&!q.dead).length},chaos:{events:HH52.events.slice(-120),kind:subBoss?._hd1003?.er28?.kind,age:subBoss?._hd1003?.er28?.t,phase:subBoss?._hd1003?.er28?.phase,clip:subBoss?._hd1003?.er28?.clip,flight:subBoss?._hd1003?._hb25?.phase,skulls:[...HH52.skulls].filter(q=>!q.dead).map(q=>({x:q.x,y:q.y,level:q._hh52Level})),bolts:subBoss?._hd1003?.er28?.bolts,projectiles:eBullets.filter(q=>q._heraldOwner1003===subBoss&&!q.dead).length},target:reviewBot.targetInfo,")
print('FINAL',rec.record(8,480),flush=True)
