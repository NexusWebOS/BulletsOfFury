from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,argparse,io
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'hammer-native';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--candidate',action='store_true');ap.add_argument('--video',action='store_true');ap.add_argument('--stage',type=int,default=8);args=ap.parse_args();errors=[];rows=[];port,stop=shoot.serve(str(R));label=('candidate'if args.candidate else'active')+f'-s{args.stage}'
playlist=([('skystrike','normal',6),('skystrike','hard',8),('skystrike','furious',9),('side','furious',5),('throw','furious',7),('redrage','furious',4),('charge','hard',6),('spin','hard',6),('shield','hard',6),('pickup','hard',6),('break','furious',8),('punch','furious',5),('fists','furious',5),('ball','furious',6),('dance','normal',5)]if args.stage==8 else[('jump','normal',7),('jump','hard',9),('jump','furious',10),('throw','furious',9),('storm','furious',10),('whirlwind','hard',8),('giant','hard',10),('pickup','hard',7),('chaingun','hard',8),('spell','hard',8),('rage','furious',4),('beam','furious',8),('ball','hard',8),('stun','hard',5),('heal','hard',10)])
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(240000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  if args.candidate:p.add_script_tag(path=str(W/'candidate/candidate.js'))
  p.add_script_tag(path=str(Path(__file__).parent/'hammer_review_lab_1023.js'));p.evaluate('s=>BAL7.setup({stage:s,kind:s===8?"vileexistence":"chromehammer",pilot:"cole",diff:"normal",fire:false,seconds:60})',args.stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&(run.stage===8?v18Warm():ha21Ready());}');p.evaluate('()=>run.stage===8?HR23.corrupt():HR23.blue()');p.wait_for_function('()=>hf22WarmRed(B)');p.evaluate('()=>Audio.startMusic(curStage.music)')
  contacts=[]
  for name,diff,dur in playlist:
   p.evaluate('([n,d])=>HR23.start(n,d)',[name,diff]);snaps=[]
   if args.video:
    r=p.evaluate('''async seconds=>{const canvas=cv.captureStream(30),audio=await HR23.audio(),stream=new MediaStream([...canvas.getVideoTracks(),...audio.getAudioTracks()]),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:2500000}),chunks=[];rec.ondataavailable=e=>e.data.size&&chunks.push(e.data);const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});rec.start();let last=performance.now(),start=last,frames=0;await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();HR23.step(Math.min(.035,(now-last)/1000));last=now;frames++;if(now-start>seconds*1000){clearInterval(timer);resolve();}},1000/60);});rec.stop();const video=await done;HR23.audioRestore();canvas.getTracks().forEach(t=>t.stop());return{video,frames,audioTracks:audio.getAudioTracks().length,result:HR23.step(0),audioErrors:HR23.audioErrors||[]};}''',dur)
    path=O/f'{label}-{name}-{diff}.webm';path.write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r['file']=str(path);rows.append({'action':name,'difficulty':diff,'seconds':dur,**r});print(json.dumps({'video':path.name,'frames':r['frames'],'audioTracks':r['audioTracks'],'states':r['result']['states']}),flush=True)
   else:
    for frame in range(round(dur*60)):
     result=p.evaluate('()=>HR23.step()')
     if frame in [0,24,48,72,100,140,200,280]:
      im=Image.open(io.BytesIO(base64.b64decode(p.evaluate('()=>HR23.capture()'))));im.thumbnail((240,300));snaps.append(im.copy())
    row={'action':name,'difficulty':diff,'result':result};rows.append(row);c=Image.new('RGB',(240*len(snaps),320),'#111b29');d=ImageDraw.Draw(c)
    for j,im in enumerate(snaps):c.paste(im,(j*240,0));d.text((j*240+2,302),f'{name} {diff} / {j}',fill='white')
    c.save(O/f'{label}-{name}-{diff}.jpg');print(json.dumps({'action':name,'diff':diff,'states':result['states'],'finite':result['finite'],'bad':len(result['bad'])}),flush=True)
   (O/f'{label}-'+Path('report.json')if False else O/f'{label}-report.json').write_text(json.dumps({'rows':rows,'errors':errors,'candidate':args.candidate,'video':args.video},indent=2))
  br.close()
finally:stop();(O/f'{label}-report.json').write_text(json.dumps({'rows':rows,'errors':errors,'candidate':args.candidate,'video':args.video},indent=2))
