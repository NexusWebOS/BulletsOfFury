"""Native full Current Breaker cycle, then real-input missile/primary counters.
No enemy HP/phase/attack-clock writes. Labelled invulnerable observer pilot.
Other waves and unrelated pickups are held for this focused preview.
"""
from pathlib import Path
import sys,json,base64,hashlib,subprocess,re,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
O=R/'_shots/current_breaker_1102';V=O/'video';V.mkdir(exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe();errors=[];timeline=[]
paths=['index.html']+[s.split('?')[0]for s in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8'))if(R/s.split('?')[0]).is_file()];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in paths}
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.24');a=script.index(' function aim(elapsed){');z=script.index(' function render(){',a);script=script[:a]+' function aim(elapsed){}\n'+script[z:];a=script.index(" diffKey='furious';debugUnlocked=true;");z=script.index(' return {entry,difficulty:',a);script=script[:a]+" const entry={stage:9,role:'enemy',kind:'cbreak'};setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[z:];script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","'CURRENT BREAKER / '+(E._cb112?.phase||'arrival').toUpperCase()+' / FURIOUS / INVULNERABLE OBSERVER'")
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None);p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(9,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&Object.values(CB112_ART.banks).every(b=>XART.rdy(b.key))}',timeout=180000)
 setup=p.evaluate('''()=>{const old=spawnEnemy;spawnEnemy=function(){return window.fixtureSpawn?old.apply(this,arguments):null;};stagePlan=[];waveIdx=0;bossWarned=true;subBossTriggered=subBossDone=aminiTriggered=true;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;powerups=[];playerLocks=[];
  window.fixtureSpawn=true;E=spawnEnemy('cbreak',worldWidth()/2,-124,{});window.fixtureSpawn=false;debugUnlocked=true;DBGT.god=true;DBGT.speed=1;player.invuln=0;run.bombs=40;run.weapon=0;run.wlevel=1;run.wlevels=WEAPONS.map(()=>1);run.spaceWeapon=0;run.spaceLevels=[1,1,1];player.x=worldWidth()/2;player.y=VH-65;CB112.events=[];window.reviewCues=[];const cue=combatAudio0927;combatAudio0927=function(owner,key,gap){const r=cue.apply(this,arguments);if(owner===E&&r)reviewCues.push({key,t:efxClock});return r;};return{hp:E.hp,max:E.maxhp,kind:E.type};}''')
 p.evaluate('()=>{drawWorld(0);requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
 with(V/'capture.webm').open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate(script,dict(name='Current Breaker',stage=9,role='enemy',kind='cbreak'))
  p.evaluate('''()=>{let last=performance.now(),debt=0;window.currentFilmLive=true;window.currentFilmInput={nextMissile:0};
   function input(dt){Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;const q=E._cb112,events=CB112.events,reflected=events.filter(x=>x.event==='roller-reflected').length,burst=events.filter(x=>x.event==='roller-safe-splash').length;
    const incoming=CB112.balls.filter(f=>!f.done&&!f.returning&&f.q&&!f.q.dead&&f.q.y>160&&f.q.y<player.y-25).sort((a,b)=>b.q.y-a.q.y)[0];let tx=worldWidth()/2+Math.sin(q.age*.8)*105;
    if(q.phase==='depth-spin'||q.phase==='depth-linger'){if(incoming)tx=incoming.q.x;const aligned=incoming&&Math.abs(player.x-incoming.q.x)<16&&incoming.q.y>player.y-240;
     if(aligned&&reflected<3&&q.age>currentFilmInput.nextMissile){Input.injectTap(keybindFor(1).bomb.find(k=>!k.startsWith('mouse'))||'k');currentFilmInput.nextMissile=q.age+.75;}
     else if(aligned&&reflected>=3&&burst<4)K.j=true;
    }K.a=player.x>tx+4;K.d=player.x<tx-4;K.w=player.y>VH-65+4;K.s=player.y<VH-65-4;
   }
   function frame(now){if(!currentFilmLive)return;debt+=Math.max(0,Math.min(.05,(now-last)/1000));last=now;let n=0;stageLoadTick();while(debt+1e-9>=1/60&&n<3&&state===GS.PLAY){input(1/60);stateT+=1/60;updatePlay(1/60);debt-=1/60;n++;}ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;window.__bofFrames++;powerups=[];drawWorld(n/60);drawEncounterClocks();requestAnimationFrame(frame);}requestAnimationFrame(frame);
  }''')
  print('START',setup,flush=True);beg=time.monotonic();endAt=None
  while True:
   p.wait_for_timeout(250);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,frames:__bofFrames,age:E._cb112.age,phase:E._cb112.phase,hp:E.hp,dead:E.dead,dying:E._dyingT,playerDead:player.dead,view:E._s911Rendered?.view,x:E.x,y:E.y,scale:E._cb112.scale})');timeline.append(q)
   if len(timeline)%40==0:print(round(q['seconds'],1),q['phase'],'HP',q['hp'],flush=True)
   if(q['dead']or q.get('dying')is not None)and endAt is None:endAt=q['seconds']
   if errors or endAt is not None and q['seconds']>endAt+1.5 or time.monotonic()-beg>90:break
  details=p.evaluate('()=>({events:CB112.events,cues:reviewCues,finalHP:E.hp,finalPhase:E._cb112.phase})');stats=p.evaluate('async()=>{currentFilmLive=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,botErrors:reviewBot.errors};}')
 report=dict(setup=setup,timeline=timeline,details=details,stats=stats,errors=errors,sourceHashes=hashes,method=__doc__);(V/'report.json').write_text(json.dumps(report,indent=2));b.close()
 assert not errors and not stats['tapErrors']and not stats['botErrors']and not any(t['playerDead']for t in timeline),(errors,stats)
 assert any(e['event']=='arsenal-complete'for e in details['events']),details
 assert any(e['event']=='roller-counter-hit'for e in details['events'])and any(e['event']=='roller-safe-splash'for e in details['events']),'Native inputs did not demonstrate both counter responses'
 assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in paths},'Production changed during film'
 movie=V/'current-breaker.mp4';subprocess.run([ff,'-y','-i',str(V/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],stdout=subprocess.DEVNULL,stderr=(V/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,check=True);print('DONE',q['seconds'],'seconds',len(details['events']),'events',flush=True)
