from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102')
tag=sys.argv[1]if len(sys.argv)>1 else 'baseline'
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 p=b.new_page(viewport={'width':1280,'height':800})
 if tag=='candidate':p.route('**/assets/game.js*',lambda route:route.fulfill(path=str(W/'game-side-entry-candidate.js'),content_type='application/javascript'))
 p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
 for f in [R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js',O/'reference_wave_maps.js',O/'wave_observe_1102.js']:p.add_script_tag(path=str(f))
 p.evaluate('WO16.start(6)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000)
 result=p.evaluate('''()=>{
   const ref=WO16.references['6'];stageTimer=ref.time;mapScroll=ref.map;_prevMapScroll=mapScroll;drawWorld(0);
   stagePlan[6].fn();const e=enemies.find(e=>e.type==='s6skimmer');const trace=[],kills=[];
   let value=e.dead;Object.defineProperty(e,'dead',{configurable:true,get(){return value},set(v){if(v&&!value)kills.push({x:e.x,y:e.y,stack:new Error().stack});value=v;}});
   const born={x:e.x,y:e.y,w:e.w,camLeft:camLeftX(),camRight:camRightX(),J:{...e._jetManeuver}};
   for(let i=0;i<120&&!e.dead;i++){stateT+=1/60;updatePlay(1/60);drawWorld(1/60);trace.push({t:i/60,x:e.x,y:e.y,dead:e.dead,camLeft:camLeftX(),camRight:camRightX(),J:{...e._jetManeuver}});}
   return {born,trace,kills};
 }''')
 (W/('missing-entry-'+tag+'.json')).write_text(json.dumps(result,indent=2),encoding='utf8')
 print(json.dumps(result,indent=2)[:7000])
 if tag=='candidate':
  cases=[]
  for difficulty in ['normal','hard','furious']:
   for side in [-1,1]:
    q=p.evaluate('''q=>{WO16.start(6);diffKey=q.difficulty;DIFF=difficultyForRun('arcade',q.difficulty);const e=spawnEnemy('s6skimmer',q.side<0?worldWidth()+90:-90,VH*.25,{_side:q.side<0?-1:1,_jetManeuver:'bomb'});let visible=0,t=0;
      for(let i=0;i<420&&!e.dead;i++){stateT+=1/60;updatePlay(1/60);drawWorld(1/60);if(e.x>=camLeftX()&&e.x<=camRightX())visible++;t+=1/60;}
      return{difficulty:q.difficulty,side:q.side,visibleFrames:visible,racks:e._jetManeuver.racks||0,departed:!!e.dead,endX:e.x,seconds:t,hp:e.hp};}''',{'difficulty':difficulty,'side':side})
    cases.append(q);p.wait_for_timeout(20)
  (W/'side-entry-boundaries.json').write_text(json.dumps(cases,indent=2),encoding='utf8')
  assert all(q['visibleFrames']>30 and {'normal':1,'hard':2,'furious':2}[q['difficulty']]<=q['racks']<={'normal':1,'hard':2,'furious':3}[q['difficulty']] and q['departed']for q in cases),cases
  print('PASS six native side-entry/attack/exit cases',flush=True)
 b.close()
