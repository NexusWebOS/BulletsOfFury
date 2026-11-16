from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlsplit
import asyncio,json,sys,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/hard4-watch';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
async def main():
 report={'errors':[],'warnings':[],'failed':[],'samples':[],'paused':None,'timeouts':[]}
 async with async_playwright()as w:
  b=await w.chromium.launch(args=['--no-sandbox']);p=await b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['warnings'].append(m.text)if m.type in['error','warning']else None);p.on('requestfailed',lambda q:report['failed'].append({'path':urlsplit(q.url).path,'failure':q.failure}))
  await p.goto('http://127.0.0.1:8765/index.html?hard4-watch=1116');await p.wait_for_function('window.__bofFrames>6');await p.evaluate(shoot.TRAP_RAF);await p.evaluate("()=>{BOFOnline.submitScore=()=>{};debugUnlocked=true;BOSSMODE.start(4,'boss','cole',false,'hard');DBGT.god=true;DBGT.speed=1;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;}");await p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)}')
  cdp=await p.context.new_cdp_session(p);await cdp.send('Debugger.enable');cdp.on('Debugger.paused',lambda e:report.update(paused=e));await cdp.send('Profiler.enable');await cdp.send('Profiler.start')
  started=time.monotonic()
  for i in range(600):
   try:e=await asyncio.wait_for(p.evaluate(shoot.STEP,6),15)
   except asyncio.TimeoutError:
    report['timeouts'].append({'atSim':i*.1,'wall':time.monotonic()-started});print('TIMEOUT '+str(i*.1),flush=True)
    try:await asyncio.wait_for(cdp.send('Debugger.pause'),5);await p.wait_for_timeout(300)
    except Exception as err:report['pauseError']=str(err)
    break
   if e:report['errors'].append(e);break
   if i%50==0:
    q=await p.evaluate('({state,t:stageTimer,hp:boss?.hp,kind:boss?.kind,enemies:enemies.length,bullets:eBullets.length,frames:__bofFrames})');q['at']=i*.1;q['wall']=time.monotonic()-started;report['samples'].append(q);print(json.dumps(q),flush=True);(O/'progress.json').write_text(json.dumps(report,indent=2),encoding='utf8')
   await p.wait_for_timeout(1)
  try:
   if report['paused']:await cdp.send('Debugger.resume')
   prof=await asyncio.wait_for(cdp.send('Profiler.stop'),5);(O/'profile.json').write_text(json.dumps(prof['profile']),encoding='utf8');await asyncio.wait_for(p.screenshot(path=str(O/'final.png')),5)
  except Exception as e:report['finishError']=str(e)
  (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');await asyncio.wait_for(b.close(),10)
asyncio.run(main())
