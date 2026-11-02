"""Stage4–9 guide refresh: actual controllers, real RAF and shared mixer.
Each isolated authored sortie runs with an invulnerable movement-only observer.
No enemy HP, attack clock, phase or projectile writes during the filmed case.
"""
from pathlib import Path
import sys,json,ast,base64,subprocess,http.server,hashlib,argparse,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
P=argparse.ArgumentParser();P.add_argument('--stages',nargs='+',type=int,default=list(range(4,10)));P.add_argument('--ids',nargs='+');a=P.parse_args()
W=R/'_shots/enemy_flight_1031/video';W.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'_shots/stage3_amplify_1031/guide-manifest-current.json').read_text())
files=['assets/game.js','assets/enemy_flight_1031.js','assets/enemy_flight_art_1031.js','assets/enemy_static_art_1031.js','assets/enemy_ordnance_art_1031.js','assets/enemy_feedback_art_1031.js','assets/enemy_module_contact_1031.js','assets/encounters_0930.js']
hashes={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files}
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe()
FIXTURE=r'''q=>{
 window.recordFixtureSpawn=true;
 window.reviewCase=q;for(const e of enemies)e.dead=true;
 aiQueue=[];playerLocks=[];for(const b of R46.pending)b.dead=true;R46.pending.clear();R46.fx=[];R46.events=[];R46.glyphMisses.clear();
 EA11.case(q.spec);bossWarned=false;story=thaw=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;
 if(q.special){
  for(const e of enemies)e.dead=true;enemies=[];aiQueue=[];fb2Flights=[];
  if(q.special==='dasher'){const free=cp22Free;cp22Free=()=>true;try{window.E=cp22DashSpawn(1,PLAY.y+165);}finally{cp22Free=free;}}
  else{window.E=fb2FlightSpawn({direction:'south',role:'red',x:worldWidth()/2,_cp22Mode:q.special});}
 }
 if(!E)throw Error('Missing native actor '+q.id);
 r46Attach(E);window.caseEnemy=E;window.caseStarted=performance.now();
 player.invuln=40002;Input.mouse.active=false;DBGT.god=true;DBGT.speed=1;
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 drawWorld(0);window.recordFixtureSpawn=false;return {type:E.type,hp:E.hp,maxhp:E.maxhp,pattern:E.pattern,model:E._r46?.model,stage:run.stage,special:q.special||null};
}'''
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26')
i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){
  Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;
  const t=(performance.now()-caseStarted)/1000;
  K.a=t%5<1.5;K.d=t%5>2.2&&t%5<4.2;
 }'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE SORTIE / INVULNERABLE OBSERVER'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i)
script=script[:i]+" const entry={stage:cfg.stage,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]

def choose(item,specs):
 typ=item['type'];special=None
 if 'tempest-dasher'in item['id']:typ='s6dart';special='dasher'
 elif '-flyby-'in item['id']:typ='s1jetbomber_b';special=item['id'].split('-flyby-')[1]
 elif 'brood-escort'in item['id']:typ='ll18brood'
 candidates=[s for s in specs if s['type']==typ]
 if typ=='modturret':candidates=[s for s in candidates if s['opt'].get('_modWeapon')==item['title'].split()[0].lower()]
 if item['stage']==9 and' / 'in item['title']:candidates=[s for s in candidates if s['opt'].get('_s9Role')==item['title'].split(' / ')[-1].lower()]
 if not candidates:raise ValueError(('No native spec',item['id']))
 spec=candidates[1 if item['id']=='stage8-s8gunship-2'and len(candidates)>1 else 0]
 return dict(id=item['id'],spec=spec,special=special)

try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  for stage in a.stages:
   folder=W/f'stage{stage}';folder.mkdir(exist_ok=True);errors=[];cards=[q for q in manifest['items']if q['stage']==stage and(not a.ids or q['id']in a.ids)];specs=json.loads((R/f'_shots/enemy_flight_1031/before/stage{stage}-specs.json').read_text())
   if not cards:continue
   p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
   p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('(s)=>EA11.setup(s,"furious")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
   p.evaluate('()=>{const spawn=spawnEnemy,release=ll18Release;ll18Release=function(e){const old=window.recordNativeOwner;window.recordNativeOwner=e;try{return release.apply(this,arguments);}finally{window.recordNativeOwner=old;}};spawnEnemy=function(){if(!window.recordFixtureSpawn&&ai27Context!==window.E&&window.recordNativeOwner!==window.E)return null;return spawn.apply(this,arguments);};}')
   # Collecting is unnecessary here: use the retained authored-wave audit specs.
   p.evaluate('()=>{stagePlan=[];bossWarned=false;player.invuln=40002;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;}')
   cuts=[];lastPlaying={};rawPath=folder/('retake-'+str(int(time.time()))+'.webm'if a.ids else'capture.webm')
   with rawPath.open('wb')as raw:
    p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
    for i,item in enumerate(cards):
     case=choose(item,specs);setup=p.evaluate(FIXTURE,case)
     if i==0:
      p.evaluate('()=>{window.savedReviewRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
      p.evaluate(script,dict(name=item['title'],kind=item['type'],stage=stage,role='enemy'))
      p.evaluate('()=>{if(window.savedReviewRAF)requestAnimationFrame(window.savedReviewRAF);window.savedReviewRAF=null;}')
     else:p.evaluate('t=>{reviewConfig.name=t}',item['title'])
     start=p.evaluate('(performance.now()-captureStart)/1000');timeline=[];deadAt=None
     limit=15 if item['type'].startswith('ll18')or'brood-escort'in item['id']else 14 if item['type']in['s4interceptor','s4rocket']else 12
     print('START',item['id'],'hp',setup['hp'],flush=True)
     while True:
      p.wait_for_timeout(400)
      q=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,elapsed:(performance.now()-caseStarted)/1000,frames:__bofFrames,state,hp:E.hp,dead:!!E.dead,dying:E._dyingT,x:E.x,y:E.y,phase:E._cp22Flight?.phase||E._cp22Dash?.phase||E._cp22Sewer?.phase||E._phase||E._ep13?.phase||E.phase,key:E._r46Rendered?.key,pose:E._r46Rendered?.frame,events:R46.events.length,actors:enemies.filter(e=>!e.dead).map(e=>e.type),playerDead:player.dead,peak:captureStats.peak})");timeline.append(q)
      if q['dead']or q.get('dying')is not None:
       if deadAt is None:deadAt=q['elapsed']
      if q['elapsed']>limit or deadAt is not None and q['elapsed']-deadAt>1.2 or errors:break
     end=p.evaluate('(performance.now()-captureStart)/1000');details=p.evaluate('()=>({events:R46.events,glyphMisses:[...R46.glyphMisses],pending:R46.pending.size,playing:{...captureStats.playing},peak:captureStats.peak})')
     report=dict(id=item['id'],type=item['type'],title=item['title'],stage=stage,setup=setup,start=start,end=end,timeline=timeline,details=details,errors=list(errors),sourceHashes=hashes,method=__doc__)
     report['played']={k:v-lastPlaying.get(k,0)for k,v in details['playing'].items()if v>lastPlaying.get(k,0)};lastPlaying=details['playing'].copy()
     (folder/(item['id']+'.json')).write_text(json.dumps(report,indent=2));cuts.append(report)
     print('CUT',item['id'],round(end-start,2),'events',len(details['events']),'glyphMisses',len(details['glyphMisses']),flush=True)
     if errors:raise RuntimeError(errors)
    stats=p.evaluate('async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,botErrors:reviewBot.errors};}')
   p.close();group=dict(stage=stage,cuts=cuts,stats=stats,errors=errors)
   if a.ids and(folder/'report.json').exists():
    old=json.loads((folder/'report.json').read_text());prior={}
    for c in old['cuts']:
     if'played'not in c:c['played']={k:v-prior.get(k,0)for k,v in c['details']['playing'].items()if v>prior.get(k,0)}
     prior=c['details']['playing'].copy();(folder/(c['id']+'.json')).write_text(json.dumps(c,indent=2))
    fresh={c['id']:c for c in cuts};group['cuts']=[fresh.get(c['id'],c)for c in old['cuts']]
    for c in cuts:(folder/(c['id']+'.json')).write_text(json.dumps(c,indent=2))
    group['previousCaptureStats']=old['stats']
   (folder/'report.json').write_text(json.dumps(group,indent=2))
   assert not stats['tapErrors']and not stats['botErrors'],stats
   for cut in cuts:
    out=folder/(cut['id']+'.mp4');duration=cut['end']-cut['start']
    subprocess.run([ff,'-y','-ss',str(cut['start']),'-i',str(rawPath),'-t',str(duration),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],stdout=subprocess.DEVNULL,stderr=(folder/'encode.log').open('w'),check=True)
    subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
   print('DONE STAGE',stage,len(cuts),'decoded clips',flush=True)
  br.close()
finally:stop()
assert hashes=={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files},'Production source changed while recording'
