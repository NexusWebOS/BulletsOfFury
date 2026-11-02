from pathlib import Path
import sys,http.server,inspect,json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/sewer_escape_extended_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'route-video';rec.CONFIG=dict(id='sewer-extended-dodges-1031',stage=7,role='boss',kind='sludgeemperor',name='Stage7 / extended collapse, dodge flight and Here goes nothing',limit=75,demonstrate=0)
rec.CAPTURE=rec.CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.35').replace('recorder.start(1000);','')
rec.CAPTURE=rec.CAPTURE.replace('  let list=b&&!b.dead?', '''
  const Q=sc86State();if(Q){for(const key of ['a','d','w','s','j','c'])K[key]=false;A.targetInfo={kind:'Native scripted dodge flight and portal commitment',phase:Q.phase};return;}
  let list=b&&!b.dead?''')
rec.CAPTURE=rec.CAPTURE.replace('return {entry,difficulty:diffKey,', '''
 await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const b=boss,M=b._s7mod||s7mInit(b);for(const p of M.parts)p.hp=0;for(const p of M.er28Canisters||[]){p.hp=0;p.dead=true;}M.shield=0;M.core=12;b.hp=12;s7mSet(b,'recover');M._mission29Intro={done:true};b.enter=false;b._noHit=false;b._s7warden.noHit=false;debugFight=null;run.mode='campaign';player.x=worldWidth()/2;player.y=VH-65;run.bombs=0;mapScroll=levelScrollRange()-1800;drawWorld(0);SC86.events=[];SR93.events=[];
 captureStart=performance.now();recorder.start(1000);
 return {checkpoint:'Final Warden core12HP and all modules/canisters depleted before filming. Real player fire causes defeat; route, activation, rewards and Stage8 handoff proceed natively. No recorder HP/phase/time writes during filming.',entry,difficulty:diffKey,''')
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.SNAPSHOT=rec.SNAPSHOT.replace('target:reviewBot.targetInfo,',"routeComplete:run.stage===8,route:{phase:sr93State()?.phase,source:sc86State()?.source,age:sc86State()?.age,margin:sr93State()?.safeMargin,fx:SR93.fx.length,bank:player._bank,radio:boss?._s7warden?.final?.radio,events:SR93.events.slice(-100),draws:SR93.draws,gateDraws:SC86.draws,score:run.score},target:reviewBot.targetInfo,")
src=inspect.getsource(rec.record).replace("if q['bossDefeated'] and completed_at is None:","if q.get('routeComplete') and completed_at is None:")
files=['index.html','assets/sewer_rescue_1031.js','assets/sewer_portal_chamber_1031.js']
def hashes():return{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in files}
exec(src,rec.__dict__);before=hashes();folder=rec.record(7,75);after=hashes();(folder/'source-hashes.json').write_text(json.dumps(dict(before=before,after=after,unchanged=before==after),indent=2));print('FINAL',folder,flush=True)
