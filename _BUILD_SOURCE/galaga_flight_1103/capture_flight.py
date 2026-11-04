"""Short native-engine observation clips. Real wall-time rAF; no fire/god mode.
This selects representative groups, not the campaign wave schedule. Silent
canvas recording; original frame, motion, weapon and draw owners execute.
"""
import json,base64,time
from playwright.sync_api import sync_playwright
from native_flight import *
errors=[];clips=[]
with sync_playwright()as pw:
 for kind in ['small','medium','large']:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disk-cache-size=1','--media-cache-size=1'])
  p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  boot(p);setup(p);p.wait_for_timeout(100);spawnInfo=spawn(p,kind)
  p.evaluate('''()=>{window.clipStats={frames:0,start:stageTimer,last:performance.now(),gaps:[],peakShots:0};const original=window.__bofPendingRAF;
   const raf=window.__bofRealRAF;window.requestAnimationFrame=cb=>raf(t=>{const now=performance.now();clipStats.gaps.push(now-clipStats.last);clipStats.last=now;clipStats.frames++;clipStats.peakShots=Math.max(clipStats.peakShots,eBullets.length);cb(t);});
   const stream=cv.captureStream(30),mime=['video/webm;codecs=vp9','video/webm;codecs=vp8'].find(s=>MediaRecorder.isTypeSupported(s));
   const chunks=[],rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6000000});rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
   window.flightRecording={rec,chunks,mime};rec.start(500);original(performance.now());}''')
  start=time.monotonic()
  for second in range(0,32,4):
   p.wait_for_timeout(4000)
   status=p.evaluate('()=>({stage:stageTimer,live:fleet.filter(e=>!e.dead).length,frames:clipStats.frames,shots:clipStats.peakShots})')
   print(kind,round(time.monotonic()-start,1),status,flush=True)
   if second>20 and status['live']==0:break
  with p.expect_download(timeout=30000)as d:
   p.evaluate('''async kind=>{const R=flightRecording;await new Promise(resolve=>{R.rec.onstop=resolve;R.rec.stop();});const blob=new Blob(R.chunks,{type:R.mime});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=kind+'.webm';a.click();}''',kind)
  d.value.save_as(W/f'{kind}.webm')
  receipt=p.evaluate('()=>({frames:clipStats.frames,gameSeconds:stageTimer-clipStats.start,meanGap:clipStats.gaps.reduce((a,b)=>a+b,0)/clipStats.gaps.length,maxGap:Math.max(...clipStats.gaps),peakShots:clipStats.peakShots,backing:[cv.width,cv.height],state,departed:fleet.every(e=>e.dead),events:GF113.events,drawError:window.__bofDrawError})')
  receipt.update(kind=kind,wallSeconds=time.monotonic()-start,spawn=spawnInfo,bytes=(W/f'{kind}.webm').stat().st_size);clips.append(receipt)
  (W/'capture-receipt.json').write_text(json.dumps({'clips':clips,'errors':errors},indent=2),encoding='utf8')
  b.close()
assert not errors and all(not q.get('drawError')for q in clips)
