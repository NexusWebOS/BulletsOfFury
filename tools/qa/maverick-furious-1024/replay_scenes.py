"""Supplementary native story replays; explicitly separate from campaign footage."""
from pathlib import Path
import asyncio,functools,http.server,threading,json,base64
from playwright.async_api import async_playwright
import record_campaign as C
W=Path(__file__).resolve().parent;O=W/'review';C.SLUG='Maverick-Story-Replays'
async def main():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(C.Handler,directory=str(C.R)));server.daemon_threads=True;threading.Thread(target=server.serve_forever,daemon=True).start()
 errors=[]
 async with async_playwright()as pw:
  b=await pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  p=await b.new_page(viewport={'width':1280,'height':720});p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(f'http://127.0.0.1:{server.server_address[1]}',wait_until='load',timeout=180000);await p.wait_for_function('window.__bofFrames>5')
  await p.keyboard.press('Shift',delay=90)
  await p.add_script_tag(content=(W/'campaign_bot.js').read_text(encoding='utf-8'))
  # Updated robust capture adapter, leaving the native game mixer unchanged.
  await p.add_script_tag(content=(W/'audio_capture.js').read_text(encoding='utf-8'))
  await p.evaluate('''()=>{
   const begin=startRun;window.replayNativeStart=begin;
   startRun=function(){run.pilot='maverick';pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');const P=PILOTS[pilotIndex];PILOTMOD={spd:P.spd||0,fire:P.fire||0,range:P.range||0,tint:P.tint};run.mode='campaign';FURYBOT.sceneIndex=1;};
   FURYBOT.pre=function(){};
   FURYBOT.post=function(now){if(!this.started||this.finished)return;this.frames++;if(!(this.nextPaint>now)){this.paint();this.nextPaint=(this.nextPaint||now)+1000/30;if(this.nextPaint<now-100)this.nextPaint=now+1000/30;}const t=this.age();if(this.sceneEndAt&&t>this.sceneEndAt+2){if(this.sceneIndex===1){this.events.push({t,type:'story-replay',stage:3});this.sceneIndex=3;this.sceneEndAt=null;run.stage=3;hqTrigger('post',3,()=>{this.sceneEndAt=this.age();});}else{this.completed=true;this.stop('complete-native-story-replays');}}if(t>300)this.stop('replay-time-limit');};
   FURYBOT.events.push({t:0,type:'story-replay',stage:1});
  }''')
  await p.evaluate('(c)=>FURYBOT.start(c)',{'id':C.SLUG,'limit':300,'role':'story-replay'})
  await p.evaluate("()=>{startRun=replayNativeStart;run.stage=1;hqSeen={};hqTrigger('post',1,()=>{FURYBOT.sceneEndAt=FURYBOT.age();});}")
  for n in range(310):
   await asyncio.sleep(1);s=await p.evaluate('()=>({t:FURYBOT.age(),scene:FURYBOT.sceneIndex,done:FURYBOT.finished,saved:FURYBOT.saved,error:FURYBOT.error,beat:BOFCinematicDirector.current?.i})')
   if n%15==0:print('REPLAY',json.dumps(s),flush=True);await p.screenshot(path=str(O/f'story-replay-{int(s["t"]):03}.png'))
   if s['done']and s['saved']:break
  r=await p.evaluate('()=>({completed:FURYBOT.completed,elapsed:FURYBOT.elapsed,events:FURYBOT.events,frames:FURYBOT.frames,bytes:FURYBOT.bytes,error:FURYBOT.error,audioErrors:FURYBOT.audioErrors})');r['pageErrors']=errors
  (O/'story-replays.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print('REPLAY DONE',json.dumps(r),flush=True);await b.close();server.shutdown()
if __name__=='__main__':asyncio.run(main())
