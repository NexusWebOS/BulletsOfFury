from pathlib import Path
import asyncio, argparse, functools, http.server, threading, json, time, sys, traceback, os
from playwright.async_api import async_playwright
W=Path(__file__).resolve().parent
candidate=W.parents[1]
R=Path(os.environ.get('BOF_GAME_ROOT',str(candidate if(candidate/'assets/game.js').exists()else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'))))
OUT=Path(os.environ.get('BOF_CAPTURE_DIR',str(W/'review')));OUT.mkdir(parents=True,exist_ok=True)
B=(W.parent/'furious_bot_1023') if (W.parent/'furious_bot_1023').exists() else W.parent/'BOF-Furious-Bot-1023'
JOBS=json.loads((B/'jobs.json').read_text())
http.server.ThreadingHTTPServer.request_queue_size=128
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  try:
   slug=self.path.removeprefix('/__capture/')
   if not self.path.startswith('/__capture/') or not slug.replace('_','').replace('-','').isalnum():self.send_error(400);return
   data=self.rfile.read(int(self.headers['Content-Length']))
   target=OUT/(slug+'.webm');offset=self.headers.get('X-Capture-Offset')
   size=target.stat().st_size if target.exists()else 0
   if offset is not None and size!=int(offset):
    with target.open('rb') as f:f.seek(int(offset));already=f.read(len(data))
    if already!=data:self.send_error(409);return
   else:
    with target.open('ab') as f:f.write(data)
   self.send_response(200);self.end_headers();self.wfile.write(b'ok')
  except Exception:self.send_error(500)
async def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only');ap.add_argument('--parallel',type=int,default=2);ap.add_argument('--limit',type=float);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
 jobs=[j for j in JOBS if not a.only or j['id'] in a.only.split(',')]
 if a.resume:jobs=[j for j in jobs if not (OUT/(j['id']+'.json')).exists() or not json.loads((OUT/(j['id']+'.json')).read_text()).get('completed')]
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R)));server.daemon_threads=True
 threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_address[1]}'
 print('SERVER',url,'JOBS',len(jobs),flush=True)
 sem=asyncio.Semaphore(a.parallel)
 async with async_playwright()as pw:
  browser=await pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
  async def record(c):
   async with sem:
    c=dict(c)
    if a.limit:c['limit']=a.limit
    slug=c['id'];errors=[];assets=[];console=[];failed=[]
    dest=OUT/(slug+'.webm')
    if dest.exists():dest.rename(OUT/(slug+f'-previous-{int(time.time())}.webm'))
    previous=OUT/(slug+'.json')
    if previous.exists():previous.rename(OUT/(slug+f'-previous-{int(time.time())}.json'))
    context=await browser.new_context(viewport={'width':1280,'height':720},accept_downloads=True)
    page=await context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    downloads=[]
    async def save_fallback(d):
     if d.suggested_filename==slug+'.webm':
      await d.save_as(dest)
      await page.evaluate('()=>{FURYBOT.saved=true;FURYBOT.downloadRecovered=true;FURYBOT.chunks=[];}')
      print('BUFFERED SAVE RECOVERED',slug,flush=True)
    page.on('download',lambda d:downloads.append(asyncio.create_task(save_fallback(d))))
    page.on('console',lambda m:console.append(m.text)if m.type=='error'else None)
    page.on('response',lambda r:assets.append({'status':r.status,'url':r.url.split('/')[-1]})if r.status>=400 else None)
    page.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}))
    print('START',slug,flush=True)
    try:
     await page.goto(url,wait_until='load',timeout=120000)
     await page.wait_for_function('window.__bofFrames>5',timeout=120000)
     await page.wait_for_function("typeof SK19_ART!=='undefined'&&typeof HM19_ART!=='undefined'&&typeof ER23_ART!=='undefined'&&typeof RB23!=='undefined'",timeout=15000)
     await page.add_script_tag(content=(B/'furious_bot.js').read_text())
     setup=await page.evaluate('(c)=>FURYBOT.start(c)',c);print('SETUP',slug,json.dumps(setup),flush=True)
     last_print=0;next_shot=12
     while True:
      await asyncio.sleep(5)
      control=W/(slug+'-control.js')
      if control.exists():
       code=control.read_text();control.rename(W/(slug+f'-applied-{int(time.time())}.js'));print('CONTROL',slug,await page.evaluate(code),flush=True)
      s=await page.evaluate('()=>({t:FURYBOT.age(),done:FURYBOT.finished,saved:FURYBOT.saved,hp:FURYBOT.health(),phase:FURYBOT.phase(),state,stats:FURYBOT.stats,frames:FURYBOT.frames,errors:FURYBOT.error,director:BOFCinematicDirector.current?{id:BOFCinematicDirector.current.id,t:BOFCinematicDirector.current.t,age:BOFCinematicDirector.current.age,shown:BOFCinematicDirector.current.shown,i:BOFCinematicDirector.current.i}:null,fbIntro:typeof fb2Intro!=="undefined"&&fb2Intro?{i:fb2Intro.i,t:fb2Intro.t,done:fb2Intro.done}:null,clock:typeof BOF_COMBAT_CLOCK!=="undefined"?BOF_COMBAT_CLOCK:null,keys:{j:Input.down("j"),k:Input.down("k")},px:player.x,py:player.y,stun:player._stun,command:FURYBOT.commands})')
      parts=await page.evaluate('()=>{const b=bossActive?boss:subBoss;return b?{hp:b.hp,x:b.x,y:b.y,player:{x:player.x,y:player.y},shield:b._s4war?.shield?.active,nodes:b._s4war?.shield?.nodes?.map(p=>({x:p.x,y:p.y,hp:p.hp,dead:p.dead})),core:b._s4war?.coreTurrets?.map(p=>({x:p.x,y:p.y,hp:p.hp,dead:p.dead,materialize:p.materialize})),modules:b._bomber?.parts?.map(p=>({id:p.id,hp:p.hp}))}:null}')
      with (OUT/(slug+'-parts.jsonl')).open('a') as f:f.write(json.dumps({'t':s['t'],'parts':parts})+'\n')
      (OUT/(slug+'-live.json')).write_text(json.dumps(s,indent=2))
      if s['t']-last_print>24:
       print('PROGRESS',slug,json.dumps(s),flush=True);last_print=s['t']
      if s['t']>next_shot:
       import base64
       raw=await page.evaluate('()=>FURYBOT.capture.toDataURL("image/png").split(",")[1]')
       (OUT/(slug+f'-{int(s["t"]):04}.png')).write_bytes(base64.b64decode(raw));next_shot+=35
      if s['done'] and(s.get('saved')or s['t']>c['limit']+20):break
      if s['t']>c['limit']+40:await page.evaluate('()=>FURYBOT.stop("watchdog")');break
     report=await page.evaluate('()=>FURYBOT.report()');report['pageErrors']=errors;report['assetErrors']=assets;report['consoleErrors']=console;report['failedRequests']=failed
     (OUT/(slug+'.json')).write_text(json.dumps(report,indent=2));print('DONE',slug,report['reason'],report['elapsed'],'errors',len(errors),flush=True)
    except Exception as e:
     print('ERROR',slug,repr(e),flush=True);traceback.print_exc()
     try:
      await page.evaluate('()=>FURYBOT.stop("host-error")');await asyncio.sleep(2)
      report=await page.evaluate('()=>FURYBOT.report()');report.update(hostError=str(e),pageErrors=errors,assetErrors=assets)
      (OUT/(slug+'.json')).write_text(json.dumps(report,indent=2))
     except:pass
    finally:await context.close()
  await asyncio.gather(*(record(j)for j in jobs));await browser.close()
 server.shutdown()
if __name__=='__main__':asyncio.run(main())
