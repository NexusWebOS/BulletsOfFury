from pathlib import Path
import sys,json,time,base64,subprocess,hashlib,http.server
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/rough_riders_guide_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,rough_riders_capture_base_1028 as source
http.server.ThreadingHTTPServer.request_queue_size=256
CAP=source.CAPTURE[:source.CAPTURE.index(" diffKey='furious';debugUnlocked=true;")]+" return {capture:true};}"
CAP=CAP.replace('enabled:true,target:null','enabled:false,target:null').replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '","(GUIDE.label||cfg.name)+' / FURIOUS / ISOLATED NATIVE MOVE / '")
CAP=CAP.replace('async cfg => {','async cfg => {const captureID=(window.guideCaptureID||0)+1;window.guideCaptureID=captureID;').replace('if(!captureLive)return;','if(!captureLive||window.guideCaptureID!==captureID)return;').replace(' render();\n const stream',' window.guideRender=render;render();\n const stream')
CAP=CAP.replace('const seen=new WeakSet(), originalPlay=HTMLMediaElement.prototype.play;', 'const seen=new WeakSet(), originalPlay=window.guideOriginalPlay||(window.guideOriginalPlay=HTMLMediaElement.prototype.play);').replace('else{const source=audio.createMediaElementSource(this);','else{const source=this._guideMediaNode||(this._guideMediaNode=audio.createMediaElementSource(this));')
BOOT=r'''key=>{
 diffKey='furious';run.ngplus=false;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;
 const b=boss,R=b._rebels;R.frIntro={done:true};R.h3Intro=null;R.frRadio=null;b.enter=false;b._noHit=false;const G=rg4Init(b);G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=Infinity;G.rd21.next=Infinity;
 H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;AP10_X.intro=null;story=null;P2M.active=null;
 if(s6Wing){s6Wing.ships=[];s6Wing.boxes=[];s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.supplyIndex=9;}
 VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=Infinity;stagePlan=[];spawnClock=Infinity;subBossTriggered=aminiTriggered=true;
 player.x=camLeftX()+viewW()/2;player.y=VH-74;player.fireCd=999;player.invuln=0;powerups=[];enemies=[];eBullets=[];pBullets=[];for(const k of ['a','d','w','s','j','k','c'])Input.keys[k]=false;
 for(const q of R.ships){q.rg4.cd=999;q.rg4.gunCd=999;q.mode='fight';q.warp=0;q.rg4.act=null;q.rg4.supply=null;q.x=camLeftX()+viewW()/2+(q.i-2)*Math.min(82,(viewW()-112)/4);q.y=PLAY.y+95+(q.i%2)*46;}
 window.GUIDE={key,t:0,label:'Cruise / drift',events:[],plan:[],done:new Set(),health:R.ships.map(q=>({key:q.key,hp:q.hp,max:q.max})),samples:[],playerStart:player.x};RR26.events=[];RD21.events=[];RA4.events=[];RA7.events=[];
 rr26Warm();rg4Warm();SC12.refresh();__bofFit();return {health:GUIDE.health,view:{width:viewW(),height:VH},key};
}'''
DRIVER=r'''()=>{
 if(window.guideUpdateBase)return;window.guideUpdateBase=updatePlay;
 window.guideAction=(a)=>{
  const R=boss._rebels,G=R.gang1004,q=R.ships.find(q=>q.key===GUIDE.key);
  GUIDE.label=a.label;GUIDE.events.push({t:GUIDE.t,label:a.label,request:a.kind});
  if(a.kind==='gun'){GUIDE.guns=true;q.rg4.gunCd=0;return;}
  GUIDE.guns=false;
  if(a.kind==='drift')return;
  if(a.kind==='roll'){
   for(const z of R.ships){z.evadeCd=0;pBullets.push({kind:'mg',x:z.x+.5,y:z.y+110,px:z.x+.5,py:z.y+110,vx:0,vy:-7,w:4,h:10,dmg:1,t:0});}return;
  }
  if(a.kind.startsWith('formation:')){G.rd21.cycle=['star','bowling','H','X'].indexOf(a.kind.split(':')[1]);rd21FleetStart(boss,G,G.rd21);return;}
  if(a.kind==='reveal'){rd21Reveal(q,'retina');return;}
  if(a.kind==='intercept'){const o=G.ord.find(o=>!o.dead&&o.kind==='helix');if(o){rg4OrdnanceHit(G,o,o.hp);GUIDE.events.push({t:GUIDE.t,nativeCounterburst:true});}return;}
  for(const z of R.ships){z.rg4.act=null;z.rg4.supply=null;z.rg4._rbal19Gun=null;}
  G.rd21.fleet=null;G.rebelBoxes=[];q._rd21Cloak=false;q.frCloak=0;q._rd21Visible=999;q.rfHeading=Math.PI/2;q._rd21Scale=1;
  rg4Attack(q,R,G,a.kind);GUIDE.events.push({t:GUIDE.t,resolved:q.rg4.act?.kind||null,warm:q.rg4.act?.warm});
 };
 updatePlay=function(dt){const C=window.GUIDE;if(!C)return guideUpdateBase.apply(this,arguments);const G=boss?._rebels?.gang1004;
  if(G){G.releaseAt=G.age+999;G.rd21.next=Infinity;G.rescueDone=true;for(const q of boss._rebels.ships){q.rg4.cd=999;if(!(GUIDE.guns&&q.key===C.key))q.rg4.gunCd=999;}}
  for(const k of ['j','k','c'])Input.keys[k]=false;C.t+=Math.max(0,dt);
  // The observer moves by ordinary input. A late sidestep demonstrates committed aim.
  const moving=C.plan.some(a=>a.kind==='sidestep'&&C.t>=a.at&&C.t<a.at+2);
  Input.keys.a=moving&&player.x>camLeftX()+65;Input.keys.d=!moving&&player.x<camLeftX()+viewW()/2-4;Input.keys.w=Input.keys.s=false;
  for(let i=0;i<C.plan.length;i++){const a=C.plan[i];if(a.at<=C.t&&!C.done.has(i)){C.done.add(i);if(a.kind!=='sidestep')guideAction(a);}}
  const r=guideUpdateBase.apply(this,arguments);return r;
 };
}'''
JOBS=[
 dict(id='voss',seconds=29,plan=[(0,'drift','Voss / cruise and drift'),(2,'gun','Voss / aimed energy round'),(5,'turbo','Voss / turbo pursuit and lateral passes'),(17,'fusion','Voss / charged rush and north return'),(18.5,'sidestep',''),(24,'drift','Voss / recovery')]),
 dict(id='nyx',seconds=24,plan=[(0,'drift','Nyx / spectre cloak'),(3,'reveal','Nyx / native Retina reveal'),(4,'cloak','Nyx / shadow charge volleys'),(11,'reveal','Nyx / reveal and retaliate'),(12,'cloak','Nyx / shadow charge volleys'),(19,'drift','Nyx / recloak and drift')]),
 dict(id='rook',seconds=23,plan=[(0,'drift','Rook / heavy gunship drift'),(2,'slug','Rook / committed dual chaingun'),(10,'ram','Rook / ram selection currently resolves to chaingun'),(11.4,'sidestep',''),(18,'drift','Rook / recovery')]),
 dict(id='kaia',seconds=19,plan=[(0,'drift','Kaia / teal roller gunship'),(2,'rockets','Kaia / sixteen-round roller burst'),(10,'rockets','Kaia / repeat burst and recovery'),(11,'sidestep','')]),
 dict(id='jace',seconds=29,plan=[(0,'drift','Jace / agile drift'),(1,'gun','Jace / aimed energy round'),(4,'helix','Jace / swerve and Helix charge'),(12,'helix','Jace / Helix counterburst'),(13.8,'intercept','Jace / native Helix interception event'),(20,'ram','Jace / charge dash'),(21,'sidestep','')]),
 dict(id='formations',seconds=38,plan=[(1,'formation:star','Star call / current shared volley layout'),(10,'formation:bowling','Bowling call / current shared volley layout'),(19,'formation:H','H call / current shared volley layout'),(28,'formation:X','X call / current shared volley layout')]),
 dict(id='evasion',seconds=12,plan=[(0,'drift','Shared / cruising and banking'),(3,'roll','Shared / incoming fire triggers barrel rolls'),(7,'roll','Shared / evade, bank and recover')])
]
def main():
 selected=set(sys.argv[1:]);jobs=[q for q in JOBS if not selected or q['id']in selected];port,stop=shoot.serve(str(R));summary=[]
 try:
  with sync_playwright()as pw:
   b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000);errors=[];console=[];http=[]
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}',wait_until='load');p.wait_for_function('window.__bofFrames>5&&typeof RR33!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6);rr26Warm();rg4Warm();}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}');p.evaluate(shoot.TRAP_RAF);p.evaluate(BOOT,'voss');p.evaluate(DRIVER)
   inventory=p.evaluate('''()=>{const R=boss._rebels,G=R.gang1004,out={};for(const q of R.ships){out[q.key]={book:Array.from({length:6},()=>ra4AttackKind(q,G)),moves:{}};for(const kind of ['turbo','fusion','rookhook','slug','ram','rockets','helix','cloak']){for(const z of R.ships)z.rg4.act=null;q._rd21Cloak=false;rg4Attack(q,R,G,kind);out[q.key].moves[kind]=q.rg4.act?.kind||null;}}return out;}''');(W/'inventory.json').write_text(json.dumps(inventory,indent=2));print('INVENTORY',json.dumps(inventory),flush=True)
   p.wait_for_function('()=>{rr26Warm();return REBEL_KEYS.every(k=>XART.rdy(AM13_ART[k].heading.key)&&XART.rdy(AM13_ART[k].roll.key)&&Object.values(AF21_ART.models[k].banks).every(a=>XART.rdy(a.key)))}')
   # One registered bridge writes the currently open recording; no reload between pilots.
   holder={};p.expose_function('saveCaptureChunk',lambda data:holder['raw'].write(base64.b64decode(data)))
   for job in jobs:
    folder=W/'videos'/job['id'];folder.mkdir(parents=True,exist_ok=True);assert not(folder/'capture.webm').exists(),'Keep existing evidence; select a fresh output folder'
    setup=p.evaluate(BOOT,job['id']if job['id']in ['voss','nyx','rook','kaia','jace']else'voss');p.evaluate('a=>{GUIDE.plan=a;}',[dict(at=a,kind=k,label=l)for a,k,l in job['plan']]);holder['raw']=(folder/'capture.webm').open('wb');p.evaluate(CAP,dict(name=job['id'].upper(),role='boss',stage=6,kind='rebelsquad'));p.evaluate('()=>{Audio.startMusic("stagex");for(const el of Object.values(Snd.music))if(el&&!el.paused)el.play().catch(()=>{});window.requestAnimationFrame=window.__bofRealRAF;requestAnimationFrame(loop);requestAnimationFrame(guideRender)}');start=time.monotonic();timeline=[];last=None
    print('START',job['id'],flush=True)
    while True:
     p.wait_for_timeout(400);q=p.evaluate('''()=>({t:GUIDE.t,wall:(performance.now()-captureStart)/1000,label:GUIDE.label,hp:boss.hp,ships:boss._rebels.ships.map(q=>({key:q.key,hp:q.hp,x:q.x,y:q.y,heading:q.rfHeading,evade:q.evadeT,cloak:q._rd21Cloak,fade:q._rr26Fade,act:q.rg4.act?{kind:q.rg4.act.kind,phase:q.rg4.act.phase,t:q.rg4.act.t,shot:q.rg4.act.shot}:null})),ord:rg4State().ord.map(o=>({kind:o.kind,hp:o.hp,dead:o.dead,owner:o.owner?.key})),missiles:eBullets.filter(q=>q._ra4Rocket&&!q.dead).length,fleet:rg4State().rd21.fleet?{name:rg4State().rd21.fleet.name,phase:rg4State().rd21.fleet.phase}:null,events:GUIDE.events.slice(-5),frames:captureStats.frames})''');timeline.append(q);(folder/'live.json').write_text(json.dumps(q,indent=2));tag=(q['label'],q.get('fleet',{}).get('phase')if q.get('fleet')else None)
     if tag!=last:print('MOVE',job['id'],round(q['t'],2),tag,flush=True);last=tag
     if q['t']>=job['seconds']or errors:break
     if time.monotonic()-start>job['seconds']*2.5:raise RuntimeError('Native timeline stalled')
    stats=p.evaluate('''async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,events:GUIDE.events,rr26:RR26.events,rd21:RD21.events,ra4:RA4.events,god:DBGT.god};}''');holder['raw'].close();p.screenshot(path=str(folder/'final.png'));p.evaluate(shoot.TRAP_RAF)
    report=dict(id=job['id'],setup=setup,timeline=timeline,stats=stats,pageErrors=errors[:],consoleErrors=console[:],httpErrors=http[:],method='Isolated native-controller demonstration on Furious. Scheduled native attack selection and native reveal/interception events; ordinary live game update/draw/audio and GOD observer. Automatic other-pilot attacks/allies/supply events suppressed. No combat code modified; this is not an unassisted playthrough.')
    (folder/'report.json').write_text(json.dumps(report,indent=2));summary.append(dict(id=job['id'],seconds=timeline[-1]['wall'],errors=errors[:],frames=stats['frames']));print('CAPTURED',job['id'],timeline[-1]['wall'],flush=True)
   b.close()
 finally:stop()
 for job in jobs:
  folder=W/'videos'/job['id'];subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-threads','2','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(folder/'preview.mp4')],check=True)
 (W/'capture-summary.json').write_text(json.dumps(summary,indent=2));print('FINISHED',json.dumps(summary),flush=True)
if __name__=='__main__':main()
