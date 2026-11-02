"""Native Stage6 left/right carrier demonstration with shared mixer capture.
Movement-only invulnerable observer. No enemy HP, phase or clock writes.
"""
from pathlib import Path
import sys,json,ast,base64,subprocess,hashlib,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/cloud_carrier_1101/video';W.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
tree=ast.parse((R/'_BUILD_SOURCE/probe_cloud_carrier_1101.py').read_text());SETUP=next(ast.literal_eval(a.value)for a in tree.body if isinstance(a,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SETUP'for t in a.targets))
files=['assets/game.js','assets/cloud_carrier_1101.js','assets/cloud_carrier_art_1101.js'];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files};errors=[];timeline=[]
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26').replace('4500000','2800000');i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;const t=elapsed%5;Input.keys.a=t<.4;Input.keys.d=t>.8&&t<1.2;Input.mouse.active=false;}'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE INPUTS / INVULNERABLE OBSERVER'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i);script=script[:i]+" const entry={stage:6,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(CC111_ART.banks).every(B=>XART.rdy(B.key))&&XART.rdy(CC111_ART.beam.key)}',timeout=180000)
 initial=p.evaluate(SETUP);p.evaluate('()=>{player.invuln=40002;DBGT.god=true;DBGT.speed=1;Input.mouse.active=false;window.caseStarted=performance.now();drawWorld(0);}')
 rawPath=W/'capture.webm'
 with rawPath.open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
  p.evaluate('()=>{window.savedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}');p.evaluate(script,dict(name='Cloud carriers / five retractable laser bays',kind='cloudcarrier',stage=6,role='enemy'));p.evaluate('()=>{if(window.savedRAF)requestAnimationFrame(window.savedRAF);window.savedRAF=null;}');right=False
  while True:
   p.wait_for_timeout(350);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,frames:__bofFrames,state,playerDead:player.dead,carriers:CC111.carriers.map(c=>({id:c.id,side:c.side,hp:c.hp,maxhp:c.maxhp,phase:c.phase,x:c.x,y:c.y,bays:c.parts.map(e=>({hp:e.hp,phase:e._sc12Phase,frame:e._sc12Frame,angle:e._sc12Angle}))}))})');timeline.append(q)
   if q['seconds']>8 and not right:right=True;p.evaluate('window.RIGHT=sc12Spawn(1)')
   if q['seconds']>23 or errors:break
  stats=p.evaluate('async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,botErrors:reviewBot.errors};}')
  events=p.evaluate('CC111.events');p.screenshot(path=str(W/'last-frame.png'))
 b.close()
report=dict(initial=initial,timeline=timeline,events=events,stats=stats,errors=errors,sourceHashes=hashes,method=__doc__);(W/'report.json').write_text(json.dumps(report,indent=2));assert not errors,errors
out=W/'cloud-carriers.mp4';subprocess.run([ff,'-y','-i',str(rawPath),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],stdout=subprocess.DEVNULL,stderr=(W/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
print('Recorded',round(timeline[-1]['seconds'],2),'seconds; peak',stats['peak'],'events',len(events),'errors',errors,flush=True);assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files},'Production changed during recording'
