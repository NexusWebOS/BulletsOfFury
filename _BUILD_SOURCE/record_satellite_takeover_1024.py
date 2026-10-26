from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/opening_storyboard_1024';port,stop=serve(str(R));errors=[]
with sync_playwright() as pw:
 br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000)
 p.mouse.click(5,5)
 p.evaluate("()=>{run.pilot='yuri';campaignIntroStart(()=>{});campaignIntroWarm();}");p.wait_for_function('campaignIntroReady()',timeout=180000)
 result=p.evaluate('''async()=>{
 const start=IP21.beats.find(b=>b.replay==='arrival').at,end=IP21.beats.find(b=>b.replay==='takeover').to;
 campaignIntro.t=start;drawCampaignIntro(0);
 const stream=cv.captureStream(0),mime=MediaRecorder.isTypeSupported('video/webm;codecs=vp9')?'video/webm;codecs=vp9':'video/webm';
 const rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:3500000}),chunks=[];
 const done=new Promise(resolve=>{rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};rec.onstop=async()=>{const blob=new Blob(chunks,{type:mime}),reader=new FileReader();reader.onload=()=>resolve({data:reader.result.split(',')[1],duration:end-start,mime});reader.readAsDataURL(blob);};});
 rec.start();const began=performance.now();await new Promise(resolve=>{const step=()=>{const elapsed=Math.min(end-start-.01,(performance.now()-began)/1000);campaignIntro.t=start+elapsed;drawCampaignIntro(0);stream.getVideoTracks()[0].requestFrame();if(performance.now()-began<(end-start)*1000)setTimeout(step,1000/30);else resolve();};step();});rec.stop();stream.getTracks().forEach(t=>t.stop());return await done;
 }''')
 (O/'dracodia-satellite-takeover.webm').write_bytes(base64.b64decode(result.pop('data')));print(json.dumps({'video':result,'errors':errors}));br.close()
stop()
(O/'video.html').write_text('''<!doctype html><meta charset="utf-8"><title>Dracodia satellite takeover</title><style>body{margin:0;background:#10161d;color:#eef4fa;font:18px system-ui;display:grid;place-items:center;min-height:100vh}main{width:min(1100px,96vw)}video{width:100%;background:black}a{color:#9fe7dc}</style><main><h2>Portal arrival → satellite takeover</h2><video controls autoplay loop src="dracodia-satellite-takeover.webm"></video><p>12-second capture of the actual game animation. Video only.</p><a href="index.html">Back to storyboard</a></main>''',encoding='utf8')
