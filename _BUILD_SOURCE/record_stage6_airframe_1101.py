"""Current Stage6 enemy guide: fixed hulls, native sorties and real mixer.
Movement-only, invulnerable observer. No enemy HP, phase or clock writes.
The native Tempest helper may self-destruct at its authored departure.
"""
from pathlib import Path
import sys,json,ast,base64,subprocess,hashlib,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/stage6_airframe_1101/video';W.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
tree=ast.parse((R/'_BUILD_SOURCE/probe_stage6_airframe_1101.py').read_text());SETUP=next(ast.literal_eval(a.value)for a in tree.body if isinstance(a,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SETUP'for t in a.targets))
guide=json.loads((R/'_shots/stage6_airframe_1101/before-guide.json').read_text());fixtures=json.loads((R/'_shots/stage6_airframe_1101/cases.json').read_text());CASES=[];bomber=0
for item in guide['items']:
 if item['stage']!=6 or item['type']=='modturret':continue
 typ=item['type'];cid=typ
 if 'tempest-dasher'in item['id']:cid='dasher'
 elif '-flyby-'in item['id']:cid=item['id'].split('-flyby-')[1]
 elif typ=='s1jetbomber_b':cid=['s1jetbomber_b','strike-east','strike-west'][bomber];bomber+=1
 case=next(q for q in fixtures if q['id']==cid);CASES.append(dict(item=item,case=case))
if len(sys.argv)>1:CASES=[c for c in CASES if c['item']['id']in sys.argv[1:]]
files=['assets/game.js','assets/stage6_airframe_1101.js','assets/stage6_airframe_art_1101.js'];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files};errors=[]
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26').replace('4500000','3200000');i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;const t=(performance.now()-caseStarted)/1000;K.a=t%5<1.65;K.d=t%5>2.3&&t%5<4.4;}'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE INPUTS / INVULNERABLE PILOT'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i);script=script[:i]+" const entry={stage:6,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(S611_ART.banks).every(B=>XART.rdy(B.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 cuts=[];partial=len(sys.argv)>1;previous=json.loads((W/'report.json').read_text())if partial and(W/'report.json').exists()else None;rawPath=W/('capture-'+str(int(time.time()))+'.webm'if partial else'capture.webm')
 with rawPath.open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
  for idx,entry in enumerate(CASES):
   item=entry['item'];case=entry['case'];cid=item['id'];p.evaluate('()=>{for(const q of R46.pending)q.dead=true;R46.pending.clear();}')
   setup=p.evaluate(SETUP,case);title=setup['model'].replace('_',' ').title()+' / '+('Native '+item['title']if item['type']!='s1jetbomber_b'else case['special'])
   p.evaluate('()=>{player.x=worldWidth()/2;player.y=VH-65;player.invuln=40002;DBGT.god=true;DBGT.speed=1;Input.mouse.active=false;window.caseStarted=performance.now();drawWorld(0);}')
   if idx==0:
    p.evaluate('()=>{window.savedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}');p.evaluate(script,dict(name=title,kind=item['type'],stage=6,role='enemy'));p.evaluate('()=>{if(window.savedRAF)requestAnimationFrame(window.savedRAF);window.savedRAF=null;}')
   else:p.evaluate('q=>{reviewConfig.name=q[0];reviewConfig.kind=q[1]}',[title,item['type']])
   start=p.evaluate('(performance.now()-captureStart)/1000');timeline=[];deadAt=None;limit=11 if setup['model'].startswith('wind')else 10;print('START',cid,setup['model'],'HP',setup['hp'],flush=True)
   while True:
    p.wait_for_timeout(350);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,elapsed:(performance.now()-caseStarted)/1000,frames:__bofFrames,state,hp:E.hp,dead:E.dead,dying:E._dyingT,x:E.x,y:E.y,camX,phase:E._cp22Flight?.phase||E._cp22Dash?.phase||E._phase,key:E._s611Rendered?.key,frame:E._s611Rendered?.frame,dir:E._s611Rendered?.dir,playerDead:player.dead,events:S611.events.length})');timeline.append(q)
    if(q['dead']or q.get('dying')is not None)and deadAt is None:deadAt=q['elapsed']
    if q['elapsed']>limit or deadAt is not None and q['elapsed']-deadAt>1.1 or errors:break
   end=p.evaluate('(performance.now()-captureStart)/1000');details=p.evaluate('()=>({events:S611.events,peak:captureStats.peak,playing:{...captureStats.playing},god:DBGT.god})')
   r=dict(id=cid,type=item['type'],title=title,setup=setup,start=start,end=end,timeline=timeline,details=details,errors=list(errors),sourceHashes=hashes,method=__doc__);cuts.append(r);(W/(cid+'.json')).write_text(json.dumps(r,indent=2));print('CUT',cid,round(end-start,2),'events',len(details['events']),flush=True);assert not errors,errors
  stats=p.evaluate('async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,botErrors:reviewBot.errors};}')
 group=dict(cuts=cuts,stats=stats,errors=errors)
 if previous:
  current={c['id']:c for c in cuts};group['cuts']=[current.get(c['id'],c)for c in previous['cuts']];group['previousCaptureStats']=previous['stats']
 (W/'report.json').write_text(json.dumps(group,indent=2));p.close();b.close()
 for cut in cuts:
  out=W/(cut['id']+'.mp4');subprocess.run([ff,'-y','-ss',str(cut['start']),'-i',str(rawPath),'-t',str(cut['end']-cut['start']),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],stdout=subprocess.DEVNULL,stderr=(W/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
print('Completed',len(cuts),'native decoded Stage6 films',flush=True);assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files},'Production changed during recording'
