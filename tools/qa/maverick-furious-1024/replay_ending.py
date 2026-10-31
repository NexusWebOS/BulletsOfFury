"""Separate native ending replay, labelled as a supplement, never a campaign win."""
from pathlib import Path
import asyncio,functools,http.server,threading,json
from playwright.async_api import async_playwright
import record_campaign as C
W=Path(__file__).resolve().parent;O=W/'review';C.SLUG='Maverick-Complete-Ending-Replay'
async def main():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(C.Handler,directory=str(C.R)));server.daemon_threads=True
 threading.Thread(target=server.serve_forever,daemon=True).start();errors=[]
 async with async_playwright()as pw:
  b=await pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  p=await b.new_page(viewport={'width':1280,'height':720});p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(f'http://127.0.0.1:{server.server_address[1]}',wait_until='load',timeout=180000);await p.wait_for_function('window.__bofFrames>5')
  await p.keyboard.press('Shift',delay=90)
  await p.add_script_tag(content=(W/'campaign_bot.js').read_text(encoding='utf-8'));await p.add_script_tag(content=(W/'audio_capture.js').read_text(encoding='utf-8'))
  await p.evaluate('''()=>{const native=startRun;window.restoreEndingStart=native;startRun=function(){run.pilot='maverick';run.mode='campaign';};FURYBOT.pre=function(){};FURYBOT.post=function(now){if(!this.started||this.finished)return;this.frames++;if(!(this.nextPaint>now)){this.paint();this.nextPaint=(this.nextPaint||now)+1000/30;if(this.nextPaint<now-100)this.nextPaint=now+1000/30;}if(drawVictory._t>INV20.end+8){this.completed=true;this.stop('complete-native-ending-replay');}if(this.age()>240)this.stop('ending-replay-time-limit');};}''')
  await p.evaluate('(c)=>FURYBOT.start(c)',{'id':C.SLUG,'limit':240,'role':'ending-replay'})
  # Official native cinematic preview, after the actual campaign is already beaten.
  # Final score is presentation metadata copied from the completed take, never a grant.
  score=json.loads((O/'report.json').read_text(encoding='utf-8'))['score']
  await p.evaluate('''async score=>{startRun=restoreEndingStart;run.score=score;await C22.preview('ending','maverick');}''',score)
  while True:
   await asyncio.sleep(10);s=await p.evaluate('()=>({t:FURYBOT.age(),endingTime:drawVictory._t,scene:INV20.last?.scene,done:FURYBOT.finished,saved:FURYBOT.saved})');print('ENDING',json.dumps(s),flush=True)
   if s['done']and s['saved']:break
  await p.screenshot(path=str(O/'ending-complete-card.png'))
  r=await p.evaluate('()=>({completed:FURYBOT.completed,elapsed:FURYBOT.elapsed,frames:FURYBOT.frames,bytes:FURYBOT.bytes,error:FURYBOT.error,audioErrors:FURYBOT.audioErrors,endingTime:drawVictory._t,scene:INV20.last?.scene})');r['pageErrors']=errors;r['presentationScore']=score;r['method']='Official C22.preview ending; separate from continuous campaign take.'
  (O/'ending-replay.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print('ENDING DONE',json.dumps(r),flush=True);await b.close();server.shutdown()
if __name__=='__main__':asyncio.run(main())
