from pathlib import Path
from playwright.sync_api import sync_playwright
import json,http.server,sys
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_roll_type_1030/music';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'music-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.bgOwner=drawBG;window.bgMatrices=[];drawBG=function(){const m=ctx.getTransform();bgMatrices.push([m.a,m.b,m.c,m.d,m.e,m.f]);return bgOwner.apply(this,arguments);};}")
  def stable(label):
   q=p.evaluate('''()=>{bgMatrices=[];const b=boss;window.nativeHP=b.hp;shake=0;drawWorld(1/60);const base=bgMatrices.at(-1);shake=18;for(let i=0;i<24;i++)drawWorld(1/60);const n=bgMatrices.length;return{base,samples:bgMatrices.slice(1),saved:shake,hp:b.hp,before:nativeHP,n,frames:RR43.frames,scope:RR43.scope(),cam:camX,world:worldWidth(),view:viewW()};}''')
   ck(label+' camera matrix stays fixed under repeated large impacts',q['scope']and len(q['samples'])==24 and all(v==q['base']for v in q['samples']),q)
   ck(label+' render does not consume HP or impact simulation state',q['saved']==18 and q['hp']==q['before'])
  stable('Airshow intro');step(900);stable('Protected dialogue');p.screenshot(path=str(W/'steady-intro.png'))
  p.evaluate('''()=>{const R=boss._rebels;R.frIntro.done=true;boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;R.rough33.scroll=1;}R.h3Intro=null;R.frRadio=null;R.t=0;R.releaseAt=0;}''');step(90);stable('Combat')
  p.evaluate('''()=>{const q=boss._rebels.ships[0];q.flash=.16;window.keepQ=q;}''');step(3);ck('Ship hit feedback still runs while the field is steady',p.evaluate('keepQ.flash>0&&boss._rebels.ships.length===5'))
  step(40);ck('Hit flash expires normally',p.evaluate('keepQ.flash===0'))
  q=p.evaluate('''()=>{const old=camX,px=player.x;player.x=worldWidth()-10;RR43.dt=1/60;updateCamX();const delta=camX-old;player.x=px;return{delta,limit:180/60};}''');ck('Horizontal tracking is speed-limited rather than jumping to a new target',abs(q['delta'])<=q['limit']+.001,q)
  q=p.evaluate('''()=>{const px=player.x;player.x=10;for(let i=0;i<600;i++)updateCamX();const left=camX;player.x=worldWidth()-10;for(let i=0;i<600;i++)updateCamX();const right=camX,max=worldWidth()-viewW();player.x=px;return{left,right,max};}''');ck('Gentle tracking still reaches both complete arena edges',q['left']<.01 and abs(q['right']-q['max'])<.01,q)
  p.evaluate("()=>{H3_REBEL_AUDIO.next=0;h3RebelMusic();}");p.wait_for_function('Snd.cur===Snd.music.roughriders6&&!Snd.cur.paused&&Snd.cur.readyState>=3',timeout=60000)
  q=p.evaluate('''()=>({key:H3.lastMusic,path:Snd.cur.currentSrc,loop:Snd.cur.loop,duration:Snd.cur.duration,stagexPaused:Snd.music.stagex.paused,clock:Snd.cur.currentTime})''');ck('Rough Riders play the original Gasline file',q['path'].endswith('/stage_x/audio/music/LevelX.mp3')and q['loop']and q['stagexPaused'],q)
  p.evaluate('''async()=>{const C=new AudioContext();await C.resume();const source=C.createMediaStreamSource(Snd.cur.captureStream()),an=C.createAnalyser();source.connect(an);an.fftSize=2048;window.rrMusicMeter={C,an};}''');rms=[]
  for i in range(4):p.wait_for_timeout(220);rms.append(p.evaluate('''()=>{const a=new Float32Array(rrMusicMeter.an.fftSize);rrMusicMeter.an.getFloatTimeDomainData(a);return Math.sqrt(a.reduce((s,v)=>s+v*v,0)/a.length);}'''))
  ck('Decoded live boss music contains an audible waveform',max(rms)>.001,rms);p.evaluate('rrMusicMeter.C.close()')
  p.evaluate('''()=>{window.beforeMusicRequest=Snd.cur.currentTime;Audio.startMusic('stagex');}''');p.wait_for_timeout(250);q=p.evaluate('''()=>({same:Snd.cur===Snd.music.roughriders6,time:Snd.cur.currentTime,before:beforeMusicRequest,path:Snd.cur.currentSrc,paused:Snd.cur.paused,stagexPaused:Snd.music.stagex.paused,scope:RR43.scope(),key:H3.lastMusic})''');ck('Legacy StageX requests stay on the boss track without restarting it',q['same']and q['time']>=q['before']and q['stagexPaused'],q)
  p.evaluate('''()=>{window.savedMusicClock=Snd.cur.currentTime;Snd.cur.pause();H3_REBEL_AUDIO.next=0;h3RebelMusic();}''');p.wait_for_timeout(250);ck('Interrupted transport resumes the same boss track and position',p.evaluate('Snd.cur===Snd.music.roughriders6&&!Snd.cur.paused&&Snd.cur.currentTime>=savedMusicClock'))
  p.evaluate('''()=>{run._gp4StageX=true;bgMatrices=[];shake=0;drawWorld(1/60);window.baseX=bgMatrices.at(-1);shake=18;drawWorld(1/60);}''');ck('Stage X retains its normal camera effects',p.evaluate('!RR43.scope()&&bgMatrices.at(-1).some((v,i)=>Math.abs(v-baseX[i])>.01)'))
  p.evaluate("Audio.startMusic('stagex')");p.wait_for_function('Snd.cur===Snd.music.stagex&&!Snd.cur.paused&&Snd.cur.readyState>=3',timeout=30000);q=p.evaluate('''()=>({path:Snd.cur.currentSrc,oldPaused:Snd.music.roughriders6.paused,expected:BOFA.music.stagex,scope:RR43.scope()})''');ck('Real StageX routing remains separate',q['path'].endswith(q['expected'])and q['oldPaused'],q)
  p.evaluate("()=>{run._gp4StageX=false;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});spawnBoss('warhive');debugFight.spawned=true;warnT=0;bgMatrices=[];shake=0;drawWorld(1/60);window.baseOther=bgMatrices.at(-1);shake=18;drawWorld(1/60);}");ck('Harrier fight keeps its independent camera behavior',p.evaluate('!RR43.scope()&&bgMatrices.at(-1).some((v,i)=>Math.abs(v-baseOther[i])>.01)'))
  ck('No native render or game errors',not errors,errors);br.close()
finally:stop()
print(len(checks),'camera scope and native matrix checks passed')
