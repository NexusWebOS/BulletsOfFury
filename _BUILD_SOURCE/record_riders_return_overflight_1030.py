from pathlib import Path
import sys,inspect,http.server
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/returns-record';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'returns-video';rec.CONFIG=dict(id='teal-return-overflight-1030',stage=6,role='boss',kind='rebelsquad',name='Golden Aegis / Teal energy-ball overflight / Native effect checkpoint',limit=9,demonstrate=999)
rec.CAPTURE=rec.CAPTURE.replace('recorder.start(1000);','')
setup="""await new Promise(resolve=>setTimeout(resolve,8000));BOFCinematicDirector.cancel();setState(GS.PLAY);
 const R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;
 const G=rg4Init(boss);G.scene=null;G.releaseAt=999;G.rescueDone=true;if(G.rd21)G.rd21.fleet=null;
 for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;q.x=camLeftX()+70+q.i*85;q.y=PLAY.y+110+(q.i%2)*65;}
 const S=rr26State(G);S.wall=null;rr26Deploy(G);if(!S.wall)throw Error('Native Decker shield unavailable');S.wall.t=4;S.returns=[];G.ord=[];pBullets=[];eBullets=[];
 for(const q of R.ships)for(const offset of[-10,10]){const o=rr26Energy(q,G,Math.PI/2,false,q.x+offset,q.y+35);o.vx=0;o.vy=125+q.i*18;}
 captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Active native Golden Aegis and ten native enemy energy rounds; no health or phase changes during footage',entry,difficulty:diffKey,"""
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,',setup)
rec.CAPTURE=rec.CAPTURE.replace('  A.targetInfo=target?',"  K.a=K.d=K.w=K.s=false;\n  A.targetInfo=target?")
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,','teal:{events:RR75.events,orbs:RR75.orbs,shadows:RR75.shadows,live:rg4State()?.rr26?.returns?.length},target:reviewBot.targetInfo,')
source=inspect.getsource(rec.record).replace("report['reason'] = 'recording time limit'","report.update(completed=True,reason='native teal-energy flyover effect demonstration')")
exec(source,rec.__dict__);print('FINAL',rec.record(6,9),flush=True)
