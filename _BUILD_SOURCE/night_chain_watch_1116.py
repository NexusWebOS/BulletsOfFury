from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlsplit
import asyncio,json,sys,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/chain-watch';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
async def main():
 report={'rows':[],'errors':[],'warnings':[],'failed':[],'timeout':None,'paused':None};started=time.monotonic()
 def save(): (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 async with async_playwright()as w:
  b=await w.chromium.launch(args=['--no-sandbox']);p=await b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['warnings'].append(m.text)if m.type in['error','warning']else None);p.on('requestfailed',lambda q:report['failed'].append({'path':urlsplit(q.url).path,'failure':q.failure}))
  await p.goto('http://127.0.0.1:8765/index.html?night-chain-watch=1116',timeout=150000);await p.wait_for_function('window.__bofFrames>6');await p.evaluate(shoot.TRAP_RAF);await p.evaluate('BOFOnline.submitScore=()=>{}')
  cdp=await p.context.new_cdp_session(p);await cdp.send('Debugger.enable');cdp.on('Debugger.paused',lambda e:report.update(paused={'reason':e.get('reason'),'frames':[{'function':q['functionName'],'url':q['url'],'location':q['location']}for q in e['callFrames']]}))
  stop=False
  for diff in ['normal','hard']:
   for stage in range(1,6 if diff=='normal'else 5):
    for role in ['mini','boss']:
     row={'id':f'{diff}-{stage}-{role}','samples':[],'phase':'start'};report['rows'].append(row);save();t=time.monotonic();print('START '+row['id'],flush=True)
     try:
      await asyncio.wait_for(p.evaluate("q=>{debugUnlocked=true;BOSSMODE.start(q.stage,q.role,'cole',false,q.diff);DBGT.god=true;DBGT.speed=1;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",{'stage':stage,'role':role,'diff':diff}),30)
      row['phase']='warm';save();await asyncio.wait_for(p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50,timeout=150000),155)
      row['phase']='step';save()
      for i in range(600):
       row['sim']=(i+1)*.1
       e=await asyncio.wait_for(p.evaluate(shoot.STEP,6),25)
       if e:raise RuntimeError(e)
       if i%100==0 or i==599:
        q=await asyncio.wait_for(p.evaluate('''()=>({state,clock:stageTimer,kind:boss?.kind||subBoss?.kind,hp:boss?.hp??subBoss?.hp,player:{x:player.x,y:player.y,dead:player.dead},frames:__bofFrames,enemies:enemies.length,bullets:eBullets.length,mem:XART.memoryInfo()})'''),10);q['sim']=(i+1)*.1;row['samples'].append(q);save()
       await p.wait_for_timeout(1)
      row['phase']='complete';row['wallSeconds']=time.monotonic()-t;print('DONE '+row['id']+' '+str(round(row['wallSeconds'],2)),flush=True);save()
     except Exception as e:
      row['exception']=str(e);report['timeout']={'id':row['id'],'phase':row['phase'],'sim':row.get('sim'),'elapsed':time.monotonic()-started};print('STOP '+str(report['timeout']),flush=True);save()
      try:await asyncio.wait_for(cdp.send('Debugger.pause'),5);await asyncio.sleep(.2);save()
      except Exception as e:report['pauseError']=str(e);save()
      stop=True;break
    if stop:break
   if stop:break
  if report['paused']:
   try:await asyncio.wait_for(cdp.send('Debugger.resume'),5)
   except Exception:pass
  report['completed']=not stop and len(report['rows'])==18;report['wallSeconds']=time.monotonic()-started;report['scope']='Same-tab repeated native boss-mode starts in original Normal1-5 thenHard1-4 order. Protected stationary no-fire60sim seconds each, bounded per-call waits and CDP stack capture on stall. Not campaign or balance certification.';save()
  try:await asyncio.wait_for(b.close(),10)
  except Exception as e:report['closeError']=str(e);save()
asyncio.run(main())
