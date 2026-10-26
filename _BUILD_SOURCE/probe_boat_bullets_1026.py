from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/boat_bullets_1026';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  results=[]
  for weapon in ['mg','spread','missile','beam','sonic','orb']:
   results.append(p.evaluate("""kind=>{enemies=[];eBullets=[];pBullets=[];bossActive=subBossActive=false;const e=spawnEnemy('s1boatpatrol',340,180,{});for(const spread of [-.24,0,.24])eShootT(e.x,e.y,Math.PI/2+spread,4.5,'s1bullet',{silent:true,noMuzzle:true});const shots=eBullets.slice();const before=shots.every(q=>!enemyOrdnanceCanIntercept(q));for(const q of shots){q.y=300;pBullets.push({kind,x:q.x,y:q.y,vx:0,vy:0,w:20,h:20,dmg:50,lv:1,t:0,top:PLAY.y,bot:player.y,pierce:true,_hit:[],_ht:.1});}updatePlay(.00001);return {weapon:kind,count:shots.length,before,alive:shots.every(q=>!q.dead&&eBullets.includes(q))};}""",weapon))
  exceptions=p.evaluate("""()=>({magma:enemyOrdnanceCanIntercept({kind:'magma'}),ice:enemyOrdnanceCanIntercept({kind:'iceball'}),missile:enemyOrdnanceCanIntercept({kind:'missile'}),decoratedBullet:enemyOrdnanceCanIntercept({kind:'s1bullet',_er26Art:'fire'})})""")
  p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(O/'overlap.png'));b.close()
finally:stop()
report=dict(results=results,exceptions=exceptions,errors=errors);(O/'report.json').write_text(json.dumps(report,indent=2));print(report)
assert all(r['count']==3 and r['before'] and r['alive'] for r in results)
assert exceptions==dict(magma=True,ice=True,missile=True,decoratedBullet=False) and not errors
