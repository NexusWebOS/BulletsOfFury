"""Native mechanics fixtures, separately labeled from input-only full route."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion_cover_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1280,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',timeout=90000);p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
  ev=p.evaluate
  def frames(n=1):
   while n:
    z=min(60,n);ev(f'TDGAME.step({z})');p.wait_for_timeout(1);n-=z
  def snap(name):ev('TD.Achievements.queue=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def fresh():
   ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Input.pointer.active=false;window.fixtureInput={};TD.Achievements.queue=[];')
  ev('window.fixtureInput={};TD.Input.update=function(){this.last=this.state;this.state={...window.fixtureInput};this.raw={};};')
  fresh();frames(100)
  check('first live wave has own cover and no immediate second-wave stack',ev('TD.game.bastion.totalWave===1&&TD.game.bastion.cover.length===4&&TD.game.units.length===3'))
  ev('TD.game.player.inv=999');frames(1200)
  check('wave cannot progress while even one attacker remains alive',ev('TD.game.bastion.totalWave===1&&TD.game.bastion.phase==="fight"&&TD.game.units.some(u=>!u.dead)'))
  fresh();frames(100);ev('window.fixtureInput={cover:true};TD.game.bastion.turrets=[];TD.game.units=[];TD.game.bastion.phase="fixture"');frames(15)
  ev('window.hp=TD.game.player.hp;window.wall=TD.Bastion.coverAt(TD.game,320);TD.Bastion.resolveEnemyShot(TD.game,{tx:320,kind:"mg",damage:1});')
  check('ducked solid wall intercepts incoming fire and itself takes damage',ev('TD.game.player.hp===hp&&wall.hp===wall.max-1.5&&TD.game.bastion.coverStops===1'))
  ev('TD.Bastion.damageCover(TD.game,320,20)')
  check('cover visibly advances into cracked art stage',ev('TD.Bastion.wallPhase(wall)===1'))
  ev('TD.Bastion.damageCover(TD.game,320,18)')
  check('cover advances into critical damaged art stage',ev('TD.Bastion.wallPhase(wall)===2'));snap('cover_damage')
  ev('TD.Bastion.damageCover(TD.game,320,99);TD.game.player.inv=0;TD.Bastion.resolveEnemyShot(TD.game,{tx:320,kind:"mg",damage:1})')
  check('broken cover no longer protects a crouched player',ev('TD.Bastion.wallPhase(wall)===3&&TD.game.player.hp===hp-1'));snap('cover_broken')
  ev('TD.game.bastion.phase="fight";window.gen=TD.game.bastion.wallGeneration');frames(100)
  check('cleared wave advances to next distinct wave with completely fresh wall',ev('TD.game.bastion.totalWave===2&&TD.game.bastion.wallGeneration===gen+1&&TD.game.bastion.cover.every(w=>w.hp===w.max)'))
  ev('window.fixtureInput={cover:true,A:true};TD.game.bastion.cursor={x:500,y:170}');frames(15)
  check('cover plus fire shoots from low blindfire pose',ev('TD.game.player.rise===0&&TD.game.player.blindfire&&TD.game.bastion.bullets.some(b=>b.blindfire)'));snap('blindfire')
  ev('window.fixtureInput={cover:true,left:true};window.px=TD.game.player.x');frames(20)
  check('crouched side stepping preserves low stance and moves at reduced speed',ev('TD.game.player.rise===0&&TD.game.player.x<px-30&&TD.game.player.x>px-40'))
  ev('window.fixtureInput={retina:true,down:true};window.px=TD.game.player.x;TD.game.bastion.cursor={x:520,y:295}');frames(40)
  check('free aim reaches close side targets without moving body',ev('TD.game.player.x===px&&TD.game.player.rise===1&&TD.game.bastion.cursor.y>440'))
  fresh();frames(100);ev('TD.game.bastion.phase="fixture";TD.game.units=[];TD.game.bastion.totalWave=3;window.vaulter=TD.Bastion.spawn(TD.game,"rifle",140);TD.game.player.inv=999;');frames(380)
  check('later rifle troops vault the wall onto camera side',ev('vaulter.phase==="flank"&&vaulter.y>432&&TD.game.bastion.vaults===1'));snap('side_vaulter')
  ev('window.fixtureInput={cover:true};TD.game.player.inv=0;TD.game.player.hp=6;');frames(15)
  ev('TD.Bastion.resolveEnemyShot(TD.game,{tx:TD.game.player.x,kind:"mg",near:true,damage:1})')
  check('vaulted attacker bypasses otherwise intact wall cover',ev('TD.game.player.hp===5'))
  ev('const q=TD.Bastion.unitBody(vaulter);window.hp0=vaulter.hp;TD.Bastion.fireHits(TD.game,{oldX:q.x,oldY:q.y,x:q.x,y:q.y,damage:2})')
  check('close attacker takes side-aim damage using rendered body bounds',ev('vaulter.hp===hp0-2'))
  fresh();frames(100);ev('TD.game.bastion.phase="fixture";TD.game.units=[];window.target=TD.Bastion.spawn(TD.game,"rifle",175);target.y=335;target.scale=.52;target.phase="attack";window.bars=TD.game.bastion.barrels;TD.Bastion.explodeBarrel(TD.game,bars[0]);')
  check('barrel explosion damages nearby infantry and chains into neighboring barrel',ev('target.dead&&bars[0].dead&&bars[1].dead&&!bars[2].dead&&TD.game.bastion.barrelKills===1'));snap('barrel_chain')
  fresh();frames(100);ev('TD.game.bastion.phase="fixture";TD.game.units=[];TD.game.bastion.totalWave=6;TD.Bastion.startBoss(TD.game)');frames(105)
  check('six-wave end retains full-health Prism Heart and fresh boss cover',ev('TD.game.bastion.room===2&&TD.game.boss.form==="core"&&TD.game.boss.hp===220&&TD.game.bastion.cover.every(w=>w.hp===52)'))
  ev('TD.Bastion.coreHit(TD.game,999)');frames(62)
  check('Prism Heart still produces complete white transformation flash',ev('TD.game.bastion.flash===1'));frames(52)
  check('Helios second form begins with 360HP double-fill phase',ev('TD.game.boss.form==="helios"&&TD.game.boss.hp===360&&TD.game.boss.state==="enter"'))
  check('zero browser errors',not errors)
  report={'checks':checks,'errors':errors,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'Isolated gameplay fixtures; not a normal difficulty playthrough.'}
  (OUT/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));browser.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
