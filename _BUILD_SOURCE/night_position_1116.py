from pathlib import Path
from playwright.async_api import async_playwright
import asyncio,json,sys,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/position';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
async def main():
 rows=[]
 async with async_playwright()as w:
  b=await w.chromium.launch(args=['--no-sandbox'])
  for stage,diff in [(1,'hard'),(4,'normal'),(4,'hard'),(4,'furious'),(6,'hard'),(9,'hard')]:
   p=await b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000);err=[];p.on('pageerror',lambda e:err.append(str(e)));p.on('console',lambda m:err.append(m.text)if m.type=='error'else None)
   await p.goto('http://127.0.0.1:8765/index.html?night-position=1116');await p.wait_for_function('window.__bofFrames>6');await p.evaluate(shoot.TRAP_RAF)
   await p.evaluate('''q=>{BOFOnline.submitScore=()=>{};debugUnlocked=true;diffKey=q.diff;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(1);run.mode='arcade';beginStage(q.stage);setState(GS.PLAY);DBGT.god=true;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;}''',{'stage':stage,'diff':diff})
   await p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
   await p.evaluate('''()=>{if(!run.spaceMode)debugScenarioEquip(0,3);window.QPOS16={frames:0,kills:[],moves:[],samples:[],previous:null};const kill=killEnemy;killEnemy=function(e){const a={x:player.x,y:player.y,cam:camX};const r=kill.apply(this,arguments);QPOS16.kills.push({frame:QPOS16.frames,type:e?.type,before:a,after:{x:player.x,y:player.y,cam:camX}});return r;};const fire=keybindFor(1).fire.find(k=>!k.startsWith('mouse'));Input.keys[fire||'j']=true;window.__qaTick=()=>{const Q=QPOS16,q={frame:Q.frames++,x:player.x,y:player.y,cam:camX,zoom:viewZoom(),screen:[cv.width,cv.height],state,scene:BOFCinematicDirector.current?.id||null,opening:!!s6Opening,dead:player.dead,shake};if(Q.previous){const d=Math.hypot(q.x-Q.previous.x,q.y-Q.previous.y);if(d>.01)Q.moves.push({...q,delta:d});}Q.previous=q;if(Q.frames%60===0)Q.samples.push(q);};}''')
   row={'stage':stage,'difficulty':diff,'scope':'Stationary primary-fire native arcade waves with protected Cole and level3 machine gun (native space loadout in space); no forced enemy HP or kills. Tracks exact coordinates inside killEnemy and every simulated frame.'};start=time.monotonic()
   try:
    for i in range(900):
     e=await asyncio.wait_for(p.evaluate(shoot.STEP,6),20)
     if e:raise RuntimeError(e)
     if i%200==199:await p.screenshot(path=str(O/f'{stage}-{diff}-{i}.jpg'),type='jpeg',quality=84)
     await p.wait_for_timeout(1)
   except Exception as e:row['exception']=str(e)
   try:
    q=await asyncio.wait_for(p.evaluate('()=>QPOS16'),5);row.update(q);row['checks']={'nativeKillsObserved':len(q['kills'])>=3,'killCallsNeverMovePlayer':all(a['before']==a['after']for a in q['kills']),'fixedViewport':len(set(tuple(a['screen'])+(a['zoom'],)for a in q['samples']if a['state']=='play'))<=1,'noBrowserErrors':not err}
   except Exception as e:row['readError']=str(e)
   row['errors']=err;row['wallSeconds']=time.monotonic()-start;rows.append(row);(O/'report.json').write_text(json.dumps({'rows':rows},indent=2),encoding='utf8');print(json.dumps({k:row[k]for k in['stage','difficulty','checks','exception','readError']if k in row}),flush=True);await p.close()
  await b.close()
asyncio.run(main())
