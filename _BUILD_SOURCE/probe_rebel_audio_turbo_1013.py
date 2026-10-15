"""Native rebel transport and turbo checks; isolated encounter fixtures, not human playthroughs."""
from pathlib import Path
import sys,json,base64,os
from playwright.sync_api import sync_playwright
R=Path(os.environ.get('BOF_ROOT',str(Path(__file__).resolve().parents[1])))
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot as sh
O=R/'_shots/rebel_audio_turbo_1013';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'fixtures':[],'audio':'Native media transport and output energy are measured; no claim of human listening.'};errors=[]
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(30,n-i));p.wait_for_timeout(5)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  channel=os.environ.get('BOF_BROWSER','msedge')
  browser=pw.firefox.launch(firefox_user_prefs={'media.autoplay.default':0}) if channel=='firefox' else pw.chromium.launch(channel=channel,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=browser.new_page(viewport={'width':1100,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:900]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  for route in (['stage6'] if os.environ.get('BOF_QUICK') else ['stage6','stageX']):
   for diff in (['normal'] if os.environ.get('BOF_QUICK') else ['easy','normal','hard','furious']):
    label=route+'-'+diff
    p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':diff,'pilot':'yuri'})
    p.evaluate('route=>{window.R=B._rebels;R.frStageX=route==="stageX";run._gp4StageX=route==="stageX"?"right":null;fb2Talk=null;H3.release=false;player.invuln=1e9+2;h3RebelMusic();}',route)
    p.wait_for_function('()=>Snd.music.stagex.readyState>=3&&!Snd.music.stagex.paused&&Snd.music.stagex.currentTime>0',timeout=20000)
    before=p.evaluate('()=>Snd.music.stagex.currentTime');p.wait_for_timeout(220)
    ck(p.evaluate('(t)=>Snd.cur===Snd.music.stagex&&Snd.cur.currentTime>t&&Snd.cur.volume>0',before),label+' music starts and advances through native intro')
    p.evaluate('()=>{window.savedVol={...Snd.vol};window.savedTime=Snd.cur.currentTime;Snd.cur.pause();H3_REBEL_AUDIO.next=0;h3RebelMusic();}')
    p.wait_for_timeout(140)
    ck(p.evaluate('()=>!Snd.cur.paused&&Snd.cur.currentTime>=savedTime-.05&&Object.keys(savedVol).every(k=>savedVol[k]===Snd.vol[k])'),label+' paused soundtrack resumes without reset or volume edits')
    p.evaluate('()=>{H3_REBEL_AUDIO.time=Snd.cur.currentTime;window.savedTime=Snd.cur.currentTime;Audio.stopMusic();H3_REBEL_AUDIO.next=0;h3RebelMusic();}')
    p.wait_for_timeout(140)
    ck(p.evaluate('()=>Snd.cur===Snd.music.stagex&&!Snd.cur.paused&&Snd.cur.currentTime>=savedTime-.05'),label+' stopped transport recovers without restarting song')
    # Full original introduction, including the final turbo exhibition.
    p.evaluate('()=>{window.demoSamples=[];window.demoDone=false;}')
    for i in range(150):
     p.evaluate('()=>{for(let j=0;j<30;j++){if(R.frIntro?.done){demoDone=true;break;}updatePlay(1/60);drawWorld(1/60);const D=R.h3Intro?.showcase?.current;if(D?.kind==="turbo"&&D.released){const q=D.q,fx=R.h3Intro.showcase.fx.filter(f=>f.kind==="dash");demoSamples.push({x:q.x,y:q.y,a:q.rfHeading,fx:fx.some(f=>Math.hypot(f.x-q.x,f.y-q.y)<.1)});}}}')
     p.wait_for_timeout(3)
     if p.evaluate('()=>demoDone'):break
    ck(p.evaluate('()=>demoDone&&demoSamples.length>50&&demoSamples.filter(s=>s.a!=null).every(s=>s.fx)'),label+' full turbo exhibition keeps wake attached to final native pose')
    ck(p.evaluate('()=>{const a=demoSamples;return a.slice(1).every((q,i)=>Math.hypot(q.x-a[i].x,q.y-a[i].y)<50);}'),label+' exhibition has no teleport between visible poses')
    p.evaluate('()=>{window.G=rg4Init(B);G.scene=null;G.rescueDone=true;G.gang=false;G.releaseAt=1e9;R.frIntro.done=true;B._noHit=false;H3.release=false;stagePlan=[];enemies=[];s6Wing=null;for(const q of R.ships){q.mode="fight";q.rg4.cd=999;q.rg4.gunCd=999;q.rg4.act=null;q.rg4.supply=null;q.rg4.trace=[];q.x=camLeftX()+viewW()/2+(q.i-2)*65;q.y=PLAY.y+100;}window.Q=R.ships.find(q=>q.key==="voss");rg4Warm();rg4Attack(Q,R,G,"turbo");}')
    p.wait_for_function('()=>XART.rdy("ra4_fx")&&air13Pose("voss","heading",Math.PI/2)',timeout=60000)
    # Move target after the warning has committed; launch must retain its aim.
    p.evaluate('()=>{rg4AttackTick(Q,R,G,Q.rg4.act.warm*.72);window.warnAim=Q.rg4.act.a;player.x=camRightX()-40;rg4AttackTick(Q,R,G,Q.rg4.act.warm*.3);}')
    ck(p.evaluate('()=>Math.abs(Q.rg4.act.a-warnAim)<.0001'),label+' turbo launch respects locked warning direction')
    p.evaluate('()=>{window.turboSamples=[];window.phases=new Set();window.finished=false;}')
    captured=False
    for i in range(50):
     p.evaluate('()=>{for(let j=0;j<20;j++){if(!Q.rg4.act){finished=true;break;}updatePlay(1/60);drawWorld(1/60);const A=Q.rg4.act;phases.add(A?.phase||"done");turboSamples.push({x:Q.x,y:Q.y,phase:A?.phase||"done",trace:Q.rg4.trace.length,angle:Q.rfHeading,playerGap:Math.hypot(Q.x-player.x,Q.y-player.y)});}}')
     p.wait_for_timeout(3)
     if not captured and p.evaluate('()=>Q.rg4.act?.phase==="return"&&Q.rg4.act.returnAt===3&&Q.y>PLAY.y+5'):
      shot(p,label+'-return');captured=True
     if p.evaluate('()=>finished'):break
    data=p.evaluate('()=>({phases:[...phases],samples:turboSamples,voices:Snd._sfxVoices.length,recovery:H3_REBEL_AUDIO.recoveries,music:{paused:Snd.cur?.paused,time:Snd.cur?.currentTime,ready:Snd.cur?.readyState},final:{x:Q.x,y:Q.y,py:player.y}})')
    report['fixtures'].append({'name':label,**data})
    ck(p.evaluate('()=>finished&&phases.has("row")&&phases.has("return")'),label+' turbo completes all passes and returns physically')
    ck(p.evaluate('()=>turboSamples.filter(s=>s.phase==="return"&&s.angle!=null).every(s=>s.trace>0)'),label+' return movement retains authored turbo wake')
    ck(p.evaluate('()=>turboSamples.filter(s=>s.phase==="return"&&s.y>PLAY.y).every(s=>s.x<camLeftX()||s.x>camRightX()||s.y<=PLAY.y+101)'),label+' return never crosses the lower player arena')
    ck(p.evaluate('()=>turboSamples.slice(1).every((s,i)=>s.phase!=="return"||Math.hypot(s.x-turboSamples[i].x,s.y-turboSamples[i].y)<15)'),label+' return stays below 15 pixels per frame without teleporting')
    ck(p.evaluate('()=>Snd._sfxVoices.length<=64&&Snd.cur===Snd.music.stagex&&!Snd.cur.paused'),label+' music remains active and sound decoders stay bounded')
    shot(p,label+'-recovered')
  # Cold transient never queues a stale play request; real running cues remain audible.
  p.evaluate('()=>{Snd.stopCue("av3_module_break");const P=Snd.pools.av3_module_break;for(const v of P.slots){if(v?.attached){v.el.pause();v.el.removeAttribute("src");v.el.load();v.attached=false;const i=Snd._sfxVoices.indexOf(v);if(i>=0)Snd._sfxVoices.splice(i,1);}}window.skipBefore=H3_REBEL_AUDIO.coldSkipped;window.coldResult=Snd.play("av3_module_break");}')
  ck(p.evaluate('()=>coldResult===false&&H3_REBEL_AUDIO.coldSkipped===skipBefore+1&&Snd.pools.av3_module_break.slots.every(v=>!v||v.el.paused)'), 'cold Rebel transient loads without queuing delayed playback')
  p.wait_for_function('()=>Snd.pools.av3_module_break.slots.some(v=>v?.el.readyState>=3)',timeout=15000)
  p.evaluate('()=>{Snd._last.av3_module_break=0;window.warmResult=Snd.play("av3_module_break");}')
  p.wait_for_timeout(100)
  ck(p.evaluate('()=>warmResult&&Snd.pools.av3_module_break.slots.some(v=>v?.el.currentTime>0&&!v.el.paused)'), 'decoded Rebel transient plays immediately')
  p.evaluate('async()=>{const c=Snd._audioCtx();await c.resume();await c.suspend();H3_REBEL_AUDIO.next=0;h3RebelMusic();}')
  p.wait_for_timeout(150)
  ck(p.evaluate('()=>Snd._ctx.state==="running"'),'Rebel playback recovers a suspended real audio context')
  energy=p.evaluate('''async()=>{const m=Snd.music.stagex,C=window.AudioContext||window.webkitAudioContext,c=new C();await c.resume();const stream=(m.captureStream||m.mozCaptureStream).call(m),src=c.createMediaStreamSource(stream),an=c.createAnalyser();an.fftSize=2048;src.connect(an);const a=new Float32Array(an.fftSize);let peak=0,rms=0,n=0;for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,25));an.getFloatTimeDomainData(a);for(const x of a){peak=Math.max(peak,Math.abs(x));rms+=x*x;n++;}}src.disconnect();await c.close();return {peak,rms:Math.sqrt(rms/n)};}''')
  report['musicEnergy']=energy
  ck(energy['peak']>.001,'native music stream contains nonzero decoded audio samples')
  ck(not errors,'zero page or console errors');report['errors']=errors
  (O/(channel+'-report.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
  browser.close()
finally:stop()
sys.exit(any(not c['ok'] for c in report['checks']))
