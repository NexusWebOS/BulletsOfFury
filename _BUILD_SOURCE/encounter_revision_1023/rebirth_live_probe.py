from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,time
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));rows=[];errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':720});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>5')
  p.evaluate("()=>{diffKey='furious';playerHit=()=>{};debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}")
  p.wait_for_function("boss?._r30?.mode==='fight'&&j3State(boss).encounter===0",timeout=60000)
  p.evaluate("()=>{for(const q of boss.parts.filter(p=>p.id!=='core')){boss._lastPart=q;modularHit(q.hp+1);}boss._lastPart=boss.parts[0];modularHit(boss.parts[0].hp+1);}")
  t=time.time()
  for mark in [1,5,10,15,20,25,27,29,31,34]:
   p.wait_for_timeout(max(1,mark-(time.time()-t))*1000)
   q=p.evaluate("()=>({mode:boss?._r30.mode,t:boss?._r30.t,encounter:j3State(boss).encounter,arena:boss?._r30.v18.arenaPhase,background:VOID17.last,download:AD20.last,assets:PXV17_ART.arenas.map(a=>({key:a.key,ready:XART.rdy(a.key)})),bolts:RB23.events.filter(e=>e.event==='corrupted-lightning').length})")
   rows.append(q);print(json.dumps(q),flush=True)
   if mark in [10,27,29,31]:p.screenshot(path=str(W/'visual'/('rebirth-live-'+str(mark)+'.png')))
  b.close()
finally:
 stop();(W/'rebirth-live.json').write_text(json.dumps({'states':rows,'errors':errors},indent=2))
