from pathlib import Path
import json,sys,math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage4_amplify_1101';checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 for diff in['normal','hard','furious']:
  p.evaluate('d=>EA11.setup(4,d)',diff);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)}',timeout=180000)
  q=p.evaluate('''()=>{bossWarned=false;stagePlan=[];CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;const original=spawnEnemy;window.allowEdge=true;spawnEnemy=function(){if(!window.allowEdge)return null;return original.apply(this,arguments);};window.edgeEnemies=[];
   for(const t of ['sandtank','s4sam','s4missile','s4tanker','s4tractor','s4tanker','s4missile','s4sam'])edgeEnemies.push(spawnEnemy(t,worldWidth()/2,-70));window.allowEdge=false;const start=edgeEnemies.map(e=>({type:e.type,x:e.x,hp:e.hp}));let overlaps=0,drift=0,nonfinite=0;const shots=S411.events.length;
   for(let i=0;i<1500;i++){updatePlay(1/60);const live=edgeEnemies.filter(e=>!e.dead&&e._dyingT==null);for(let a=0;a<live.length;a++){if(!Number.isFinite(live[a].x+live[a].y))nonfinite++;if(live[a]._armor17)drift=Math.max(drift,Math.abs(live[a].x-start[edgeEnemies.indexOf(live[a])].x));for(let z=a+1;z<live.length;z++)if(groundTrafficTouch(live[a],live[z]))overlaps++;}if(i%120===0)drawWorld(0);}
   spawnEnemy=original;return{overlaps,drift,nonfinite,start,traffic:GT18.stats,shots:S411.events.filter(e=>e.event==='shot').length};}''')
  ck(diff+' full visible vehicle hulls never stack',q['overlaps']==0 and q['nonfinite']==0,q)
  ck(diff+' highway tank stays in its original lane',q['drift']<.001,q['drift'])
 # Generation/export contract; actual frame alpha must contain both weapon mounts.
 q=p.evaluate('''()=>{const rows=[];for(const[name,M]of Object.entries(S411_ART.models)){const bank=M.banks.heading;if(!bank)continue;const im=XART.get(bank.key),c=document.createElement('canvas');c.width=c.height=192;const g=c.getContext('2d');for(let d=0;d<16;d++){g.clearRect(0,0,192,192);g.drawImage(im,...bank.cells[d],0,0,192,192);const a=g.getImageData(0,0,192,192).data;rows.push({name,d,mounts:M.gunPoses[d].map(([x,y])=>a[(y*192+x)*4+3])});}}return rows;}''');ck('All32 aircraft heading poses keep both firing mounts on authored pixels',len(q)==32 and all(all(a>80 for a in row['mounts'])for row in q),q)
 ck('No browser errors in crowded/difficulty checks',not errors,errors);b.close()
(O/'edge-checks.json').write_text(json.dumps(checks,indent=2));assert all(c['passed']for c in checks)
