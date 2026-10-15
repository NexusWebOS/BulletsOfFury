from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_atlas_1013/overdrive';O.mkdir(parents=True,exist_ok=True)
data=json.loads((R/'assets/data/enemy_atlas_1013.json').read_text(encoding='utf-8'));entries=[e for e in data['entries'] if e['game']=='overdrive']
checks=[];errors=[];rows=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='chrome',args=['--mute-audio']);p=b.new_page(viewport={'width':960,'height':720})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and not m.location.get('url','').endswith('/favicon.ico') else None)
  p.add_init_script("window.__rawGet=Storage.prototype.getItem;localStorage.setItem('bof_atlas_storage_probe','before');window.__rawKeys=Object.keys(localStorage);")
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?enemyAtlas=1')
  p.wait_for_function('window.BOF_ENEMY_ATLAS?.ready',timeout=180000)
  for e in entries:
   r=p.evaluate('async e=>await BOF_ENEMY_ATLAS.start(e,"normal")',e);check('spawn '+e['id'],not r.get('error') and r.get('actor') is not None)
   p.evaluate('BOF_ENEMY_ATLAS.pause(true)');before=p.evaluate('TD.game.t');seen=set();peaks=0
   for k in range(24):
    p.evaluate('()=>{TDGAME.step(20);BOF_ATLAS_CLOCK.after?.();}');p.wait_for_timeout(5)
    s=p.evaluate('BOF_ENEMY_ATLAS.snapshot()');seen.update(s['projectiles']);peaks=max(peaks,s['liveProjectiles'])
   after=p.evaluate('BOF_ENEMY_ATLAS.snapshot()');check('native animation '+e['id'],p.evaluate('TD.game.t')>before and after['actor'] is not None and not after.get('error'))
   if e['spawn'].get('type') not in ['camera',None]:check('native attacks observed '+e['id'],bool(seen))
   check('isolated protected target '+e['id'],p.evaluate('!TD.game.player.dead&&TD.game.player.hp===TD.game.player.max') and (after['unitCount']<=1 or e['spawn'].get('kind')=='fortress'))
   if e['spawn'].get('phase'):check('selected Exhibit form '+str(e['spawn']['phase']),p.evaluate('TD.game.boss.form')==e['spawn']['phase'])
   if e['spawn'].get('member'):check('selected Machinist '+e['spawn']['member'],p.evaluate('TD.game.boss.tanks.filter(q=>!q.dead).map(q=>q.crew)')==[e['spawn']['member']])
   rows.append({'id':e['id'],'seen':list(seen),'peak':peaks,'snapshot':after})
   if e['id'] in ['overdrive-enemy-jackal','overdrive-enemy-odElite','overdrive-enemy-convoyJet','overdrive-boss-warrior','overdrive-boss-gosfer','overdrive-boss-machinists','overdrive-form-exhibit-3']:
    p.screenshot(path=str(O/(e['id']+'.png')))
   print(json.dumps({'id':e['id'],'shots':list(seen),'phase':after['actor']['phase']}),flush=True)
  for diff in ['easy','normal','hard','furious']:
   for eid in ['overdrive-enemy-odElite','overdrive-boss-warrior']:
    e=next(v for v in entries if v['id']==eid);r=p.evaluate('async q=>BOF_ENEMY_ATLAS.start(q[0],q[1])',[e,diff]);p.evaluate('BOF_ENEMY_ATLAS.pause(true)');p.evaluate('()=>{TDGAME.step(120);BOF_ATLAS_CLOCK.after?.();}');check(diff+' native difficulty '+eid,p.evaluate('TD.difficulty')==diff and not r.get('error'))
  p.evaluate('BOF_ENEMY_ATLAS.target(.4,.8)');check('target reposition control',p.evaluate('Number.isFinite(TD.game.player.x)&&Number.isFinite(TD.game.player.y)'))
  p.evaluate('BOF_ENEMY_ATLAS.pause(true)');t=p.evaluate('TD.game.t');p.wait_for_timeout(200);check('pause freezes native clock',p.evaluate('TD.game.t')==t)
  p.evaluate('BOF_ENEMY_ATLAS.step()');check('single step advances exactly one native update',p.evaluate('TD.game.t')==t+1)
  p.evaluate('BOF_ENEMY_ATLAS.speed(.5)');check('speed control',p.evaluate('BOF_ENEMY_ATLAS.snapshot().speed')==.5)
  p.evaluate('BOF_ENEMY_ATLAS.hp(.4)');check('health control',p.evaluate('BOF_ENEMY_ATLAS.snapshot().actor.health')<=.401)
  check('progress writes remain ephemeral',p.evaluate("__rawGet.call(localStorage,'bof_atlas_storage_probe')==='before'&&Object.keys(localStorage).length===__rawKeys.length"))
  canvas=p.evaluate('()=>{const c=document.createElement("canvas");c.width=c.height=96;BOF_ENEMY_ATLAS.projectiles([{kind:"laser",canvas:c}]);return Array.from(c.getContext("2d").getImageData(0,0,96,96).data).some((v,i)=>i%4===3&&v>0);}')
  check('projectile tile renders native pixels',canvas)
  normal=b.new_page();normal.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html');normal.wait_for_function('window.TDGAME',timeout=60000)
  check('normal Overdrive has no guide bridge or RAF hook',normal.evaluate('!window.BOF_ENEMY_ATLAS&&!window.BOF_ATLAS_CLOCK'));normal.close()
  check('no browser errors',not errors);b.close()
finally:
 stop();(O/'qa.json').write_text(json.dumps({'checks':checks,'entries':rows,'errors':errors},indent=2),encoding='utf-8')
print(json.dumps({'passed':sum(q['pass'] for q in checks),'checks':len(checks),'errors':errors}),flush=True)
sys.exit(0 if all(q['pass'] for q in checks) and not errors else 1)
