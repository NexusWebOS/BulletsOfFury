import sys,json,base64
from pathlib import Path
sys.path.insert(0,'D:/BOF-Downloads/2026-11-14/RevG-source/_BUILD_SOURCE')
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[1]/'_shots/opening_1114';errors=[];report=json.loads((OUT/'recording.json').read_text())['clips'] if (OUT/'recording.json').exists() else []
RECORD="""async part=>{
 const C=Snd._audioCtx();await C.resume();const dest=C.createMediaStreamDestination(),anal=C.createAnalyser();aq112Bus().output.connect(dest);aq112Bus().output.connect(anal);anal.fftSize=2048;const bins=new Float32Array(2048);
 const capture=document.createElement('canvas');capture.width=1824;capture.height=1024;const captureCtx=capture.getContext('2d');captureCtx.imageSmoothingEnabled=false;
 const stream=capture.captureStream(30);for(const a of dest.stream.getAudioTracks())stream.addTrack(a);const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:3000000,audioBitsPerSecond:96000});const chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}))});let peak=0,frame=0,stages=[],prior='',start=performance.now(),mapConfirm=false,late=0;
 rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();loop(now);frame++;captureCtx.fillStyle='#000';captureCtx.fillRect(0,0,1824,1024);const k=Math.min(1824/cv.width,1024/cv.height);captureCtx.drawImage(cv,(1824-cv.width*k)/2,(1024-cv.height*k)/2,cv.width*k,cv.height*k);anal.getFloatTimeDomainData(bins);for(const v of bins)peak=Math.max(peak,Math.abs(v));
 const tag=state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'');if(tag!==prior){stages.push({at:(now-start)/1000,tag});prior=tag;}
 if(part==='stage1'&&state===GS.STAGESEL&&stateT>1.5&&!mapConfirm){mapConfirm=true;Input.injectTap('enter');}
 const ended=part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0;
 if(ended||(now-start)>170000){clearInterval(timer);resolve();}},1000/60)});rec.stop();const video=await done;aq112Bus().output.disconnect(dest);aq112Bus().output.disconnect(anal);stream.getTracks().forEach(t=>t.stop());return{video,seconds:(performance.now()-start)/1000,frames:frame,peak,stages,last:FURY14.last};}
"""
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(220000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.goto('http://127.0.0.1:8765/index.html?opening-record=1114');p.wait_for_function('()=>window.__bofFrames>6');p.evaluate(sh.TRAP_RAF)
 for part in (sys.argv[1:] or ['opening','stage1']):
  print('RECORD',part,flush=True)
  if part=='opening':
   p.evaluate("()=>{run.pilot='cole';run.mode='campaign';FURY14.preview('opening','cole');}");p.wait_for_function('()=>fury14Ready(FURY14.openKeys)');p.evaluate('()=>campaignIntro.t=0')
  else:
   p.evaluate("()=>{run.mode='campaign';run.pilot='cole';campaign.rank={};campaign.unlockedMax=1;openStageSelect(1,{});Input.clearTaps();}");p.wait_for_function('()=>fury14Ready(fury14Warm())');p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  r=p.evaluate(RECORD,part);(OUT/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r['part']=part;report=[q for q in report if q['part']!=part];report.append(r);(OUT/'recording.json').write_text(json.dumps({'clips':report,'errors':errors},indent=2),encoding='utf-8');print({k:r[k] for k in ['part','seconds','frames','peak','stages']},flush=True)
 b.close()
assert not errors,errors
assert all(q['peak']>.001 for q in report)
