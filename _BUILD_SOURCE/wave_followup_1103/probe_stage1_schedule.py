from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
W=Path(__file__).parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102');tag=sys.argv[1]if len(sys.argv)>1 else 'baseline'
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
trace=[];errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800})
 p.on('pageerror',lambda e:errors.append(str(e)))
 if tag=='candidate':p.route('**/assets/stage1_followup_1031.js*',lambda route:route.fulfill(path=str(W/'stage1-schedule-candidate.js'),content_type='application/javascript'))
 p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
 for f in [R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js',O/'reference_wave_maps.js',O/'wave_observe_1102.js']:p.add_script_tag(path=str(f))
 p.evaluate('''()=>{wo16Start(1);WO16.mode='CLEANUP';WO16.targetIndex=0;WO16.targetProgress=0;WO16.targetHp=null;}''');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
 for batch in range(36):
  q=p.evaluate('''()=>{for(let i=0;i<300;i++){wo16Input(1/60);stateT+=1/60;updatePlay(1/60);drawWorld(1/60);}const next=stagePlan[waveIdx];return {clock:WO16.clock,stageTimer,waveIdx,total:stagePlan.length,map:mapScroll,source:levelSrcY(),length:curStage.length,gap:_waveGap,groundHold:_s1GroundHold,next:next?{t:next.t,ground:next.fn._s1Ground,pressure:next.fn._s1Pressure}:null,input:WO16.lastInput,live:enemies.filter(e=>!e.dead).map(e=>({type:e.type,hp:e.hp,x:e.x,y:e.y,pattern:e.pattern,prop:e.prop,ground:e.ground,gt:e._gt18,entry:e._entrySweep,s1:e._s1a}))};}''')
  trace.append(q);print('SCHEDULE',round(q['clock']),q['waveIdx'],'/',q['total'],'map',round(q['map']),flush=True);p.wait_for_timeout(20)
  if q['waveIdx']==q['total']:break
 p.screenshot(path=str(W/('stage1-schedule-'+tag+'.png')))
 extra=p.evaluate('''()=>({state,blocked:vp12Blocked(),flags:{dead:player.dead,boss:bossActive,mini:subBossActive,warn:warnT,story:!!story,debug:!!debugFight,fseq:!!wfx?.fseq,opening:!!s6Opening,h3:h3Locked(),director:BOFCinematicDirector.live},groups:VP12.groups.map(g=>({id:g.id,age:g.age,type:g.type,duration:g.duration})),units:enemies.filter(e=>e._vp12).map(e=>({type:e.type,noHit:e._noHit,hp:e.hp,group:e._vp12.g.id,age:e._vp12.g.age,listed:VP12.groups.includes(e._vp12.g)}))})''')
 report={'trace':trace,'final':trace[-1],'extra':extra,'errors':errors}
 (W/('stage1-schedule-'+tag+'.json')).write_text(json.dumps(report,indent=2),encoding='utf8');b.close()
 print(json.dumps(trace[-1],indent=2),flush=True)
