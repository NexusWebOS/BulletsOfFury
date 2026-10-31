from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
W=Path(__file__).resolve().parent;O=W/'review'
async def main():
 url=json.loads((W/'viewer.json').read_text())['url'];out=[]
 async with async_playwright()as pw:
  b=await pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=await b.new_page()
  for name,seeks in [('Maverick-Furious-Beta-Playthrough.mp4',[190,1618,2750,3488,3589]),('Maverick-Story-Replays.mp4',[5,80,127]),('Maverick-Complete-Ending-Replay.mp4',[5,90,148])]:
   await p.goto(url+'/index.html');await p.evaluate('n=>{const v=document.querySelector("video");v.src=n;v.load();}',name)
   await p.wait_for_function('document.querySelector("video").readyState>=1',timeout=30000)
   meta=await p.evaluate('()=>{const v=document.querySelector("video");return{duration:v.duration,width:v.videoWidth,height:v.videoHeight}}')
   tests=[]
   for t in seeks:
    await p.evaluate('t=>{const v=document.querySelector("video");v.currentTime=t;v.play();}',t)
    await p.wait_for_function('t=>{const v=document.querySelector("video");return !v.seeking&&v.currentTime>t+.3&&v.readyState>=2}',arg=t,timeout=30000)
    tests.append(await p.evaluate('()=>{const v=document.querySelector("video");return{time:v.currentTime,error:v.error?.message||null,readyState:v.readyState,decodedFrames:v.webkitDecodedFrameCount}}'))
   out.append({'file':name,**meta,'seekPlayback':tests})
  await b.close()
 (O/'browser-media-check.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out),flush=True)
if __name__=='__main__':asyncio.run(main())
