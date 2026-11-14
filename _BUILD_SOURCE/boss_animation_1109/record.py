"""Focused native-engine checkpoints, captured live with the actual SFX bus."""
from pathlib import Path
import sys,ast,json,time,base64,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;O=R/'_shots/boss_animation_1109';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
seed=next(n.args[0].value for n in ast.walk(ast.parse((W/'verify.py').read_text()))if isinstance(n,ast.Call)and n.args and isinstance(n.args[0],ast.Constant)and isinstance(n.args[0].value,str)and 'window.seed119='in n.args[0].value)
CAPTURE="""async()=>{const a=Snd._audioCtx();await a.resume();const dest=a.createMediaStreamDestination(),an=a.createAnalyser();an.fftSize=1024;const bus=aq112Bus();bus.output.connect(an);an.connect(dest);
 window.captureStats={peak:0,frames:0,starts:AL116.stats.starts};const c=document.createElement('canvas');c.width=1280;c.height=800;const g=c.getContext('2d');window.live119=true;
 function render(){if(!live119)return;g.fillStyle='#02060c';g.fillRect(0,0,1280,800);for(const v of document.querySelectorAll('canvas')){const r=v.getBoundingClientRect(),s=getComputedStyle(v);if(v!==c&&v.width&&v.height&&r.width&&r.height&&s.display!=='none'&&s.visibility!=='hidden'&&s.opacity!=='0'){g.imageSmoothingEnabled=false;g.drawImage(v,r.x,r.y,r.width,r.height);}}
 g.fillStyle='#041222';g.fillRect(290,755,700,38);g.textAlign='center';g.fillStyle='#b9edff';g.font='16px sans-serif';g.fillText(window.label119||'',640,780);captureStats.frames++;const d=new Float32Array(1024);an.getFloatTimeDomainData(d);for(const v of d)captureStats.peak=Math.max(captureStats.peak,Math.abs(v));requestAnimationFrame(render);}
 const stream=c.captureStream(30);for(const t of dest.stream.getAudioTracks())stream.addTrack(t);window.rec119=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9,opus',videoBitsPerSecond:6500000,audioBitsPerSecond:160000});window.pending119=Promise.resolve();rec119.ondataavailable=e=>{if(e.data.size)pending119=pending119.then(async()=>{const b=new Uint8Array(await e.data.arrayBuffer());let s='';for(let i=0;i<b.length;i+=32768)s+=String.fromCharCode(...b.subarray(i,i+32768));await save119(btoa(s));});};requestAnimationFrame=__bofRealRAF;requestAnimationFrame(loop);render();rec119.start(500);}"""
errors=[];reports=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  old=[]
  only='chronos-planted-combo.mp4'if '--stage5-only'in sys.argv else 'dracodia-claws.mp4'if '--claws-only'in sys.argv else None
  if any(k in sys.argv for k in ['--hammer-only','--claws-only','--stage5-only']) and (O/'recordings.json').exists():old=[r for r in json.loads((O/'recordings.json').read_text())['recordings']if r['video']!=only]if only else[r for r in json.loads((O/'recordings.json').read_text())['recordings']if r['video']=='dracodia-claws.mp4']
  for stage,name in ([(5,'chronos-planted-combo')]if '--stage5-only'in sys.argv else[(8,'dracodia-claws')]if '--claws-only'in sys.argv else[(5,'chronos-planted-combo'),(8,'dracodia-hammer-combo')]if '--hammer-only'in sys.argv else[(5,'chronos-planted-combo'),(8,'dracodia-hammer-combo'),(8,'dracodia-claws')]):
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
   ctx=br.new_context(viewport={'width':1280,'height':800});p=boot(ctx,port,stage,errors,'boss');p.wait_for_function('(s)=>{stageLoadTick();return ba119Warm(s)}',arg=stage,polling=50,timeout=180000)
   if stage==5:
    p.evaluate(seed)
    p.evaluate("()=>{const hold=Input.hold;Input.hold=function(...args){return args.includes('fire')?false:hold.apply(this,args)};const init=seed119;seed119=function(...args){init(...args);B.flash=0;B._lastPart=null;for(const part of B.parts||[])part.flash=0;};}")
   else:p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;B._noHit=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
   raw=O/(name+'.webm');out=raw.open('wb');p.expose_function('save119',lambda b:out.write(base64.b64decode(b)))
   p.evaluate(CAPTURE);chapters=[];segments=[];start=time.monotonic()
   if name=='dracodia-claws':
    for side in ['left','right']:
     label='Drac-drone / '+side+' whole-arm swipe / native checkpoint'
     p.evaluate("([side,label])=>{v18Clear(B);v18Enter(B,0,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=viewTopY()+180;player.x=worldWidth()/2;player.y=VH-65;rd72Start(B,'swipe').side=side;window.label119=label;}",[side,label]);chapters.append(dict(label=label,seconds=round(time.monotonic()-start,2)));p.wait_for_timeout(2900)
    label='Drac-drone / connected arm catch, lift and release / invulnerable observer'
    p.evaluate("label=>{v18Clear(B);v18Enter(B,0,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=viewTopY()+180;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;DBGT.god=true;rd72Start(B,'grab');window.label119=label;}",label);chapters.append(dict(label=label,seconds=round(time.monotonic()-start,2)));p.wait_for_timeout(5200)
    label='Dracodia / articulated side rakes and depth-jump twin claws'
    p.evaluate("label=>{v18Clear(B);v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=viewTopY()+180;rd77Start(B);window.label119=label;}",label);chapters.append(dict(label=label,seconds=round(time.monotonic()-start,2)));p.wait_for_timeout(13500)
   for diff,mat,duration in ([] if name=='dracodia-claws' else [('normal','regular',4.1),('hard','regular',5.4),('furious','regular',6.2),('furious','chrome',6.2)]+([]if stage==5 else[('furious','red',6.2)])):
    label=f'Stage {stage} / {diff.title()} / {mat} / native attack checkpoint'
    if stage==5:p.evaluate('([d,m,label])=>{seed119(d,m);window.label119=label;}',[diff,mat,label])
    else:p.evaluate("([d,m,label])=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);Q.chrome=m!=='regular';Q.rage=m==='red';B.x=worldWidth()/2;B.y=viewTopY()+180;Q.action=null;Q.cool=999;hb20Start(B,'skystrike');window.label119=label;}",[diff,mat,label])
    chapters.append(dict(label=label,seconds=round(time.monotonic()-start,2)));print(label,flush=True);p.evaluate('BA119.events=[]');roots=[];end=time.monotonic()+duration
    while time.monotonic()<end:
     p.wait_for_timeout(65)
     pos=p.evaluate("()=>{const h=B._hammer,A=rd74Own(B)?hb20State(B).action:null;return{active:run.stage===5?h?.state==='recover':A?.type==='skystrike'&&A.t-A.tell>=.55,x:B.x,y:B.y}}")
     if pos['active']:roots.append([pos['x'],pos['y']])
     if stage==5:
      if p.evaluate("!['warn','leap','recover'].includes(B._hammer.state)"):break
     elif p.evaluate("Q.action?.type!=='skystrike'"):break
    events=p.evaluate('BA119.events');drift=max([((r[0]-roots[0][0])**2+(r[1]-roots[0][1])**2)**.5 for r in roots]or[0]);segments.append(dict(label=label,landedRootSamples=len(roots),maxDrift=drift,contacts=[e for e in events if e['type']=='planted-contact']))
   if stage==5:
    p.evaluate("()=>{seed119('furious','regular');hammerState(B,'curl');window.label119='Stage 5 / native fold, compact ball and rolling frames';}");chapters.append(dict(label='Ball transformation',seconds=round(time.monotonic()-start,2)));p.wait_for_timeout(6000)
   stats=p.evaluate("async()=>{await new Promise(r=>{rec119.onstop=r;rec119.stop()});await pending119;live119=false;return{...captureStats,sfxStarts:AL116.stats.starts-captureStats.starts,events:BA119.events,errors:AL116.errors};}");out.close();p.screenshot(path=str(O/(name+'-end.png')));ctx.close();br.close()
   video=O/(name+'.mp4');subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-af','volume=0.9','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
   reports.append(dict(stage=stage,video=video.name,chapters=chapters,segments=segments,audio=stats));(O/'recordings.json').write_text(json.dumps(dict(route='Focused, explicitly triggered attack checkpoints; native live game simulation, renderer and mixer; invulnerable observer; not a continuous full fight.',recordings=reports+old,errors=errors),indent=2))
finally:stop()
print(json.dumps({'videos':[r['video']for r in reports],'errors':errors}),flush=True)
