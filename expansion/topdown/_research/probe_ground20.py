from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/bastion20/runtime';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate;ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal"')
  def frames(n):
   while n:
    k=min(40,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(2);n-=k
  def shot(n):
   old=ev('({inv:TD.game.player.inv,flash:TD.game.player.flash})');ev('TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(n+'.png')));p.evaluate('q=>Object.assign(TD.game.player,q)',old)
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.y=428;TD.game.player.x=400;TD.game.fortress.relays=3;TD.game.boss=TD.makeGosfer(TD.game,400,195)');frames(170)
  ev('ART.warm(Object.keys(TD_BASTION20_ART.assets))');p.wait_for_function('ART.progress(Object.keys(TD_BASTION20_ART.assets))===1',timeout=90000)
  check('all158 new graphics decode in native ART',ev('Object.keys(TD_BASTION20_ART.assets).length===158&&ART.progress(Object.keys(TD_BASTION20_ART.assets))===1'))
  ev('TD.game.player.inv=999;TD.game.boss.hit(TD.game.boss.x,TD.game.boss.y,4,999)');check('shield rejects boss damage while barriers stand',ev('TD.game.boss.hp===300&&TD.game.boss.shield&&TD.game.boss.remaining().length===3'))
  ev('TD.hitStructure(TD.game,TD.game.boss.barriers[0],999)');check('player cannot bypass shield by destroying linked barriers',ev('!TD.game.boss.barriers[0].dead'))
  shot('gosfer_shielded');seen=set();states=set()
  for i in range(150):
   q=ev('({state:TD.game.boss.state,line:TD.game.boss.line,phase:TD.game.boss.phase,barriers:TD.game.boss.remaining().length})');states.add(q['state'])
   if q['state']=='dialogue'and q['line']not in seen:seen.add(q['line']);shot('dialogue_'+str(q['line']))
   if q['state']=='transform'and'transform'not in seen:seen.add('transform');frames(65);shot('lightning_fear')
   if q['phase']==2:break
   ev('TD.game.player.inv=999');frames(30)
  check('actual Gosfer projectiles break all three barriers',ev('TD.game.boss.barrierLog.length===3&&TD.game.boss.barrierLog.every(q=>q.by==="gosfer")'))
  check('shield falls only after final barrier',ev('!TD.game.boss.shield&&TD.game.boss.remaining().length===0'))
  check('all three portrait dialogue turns precede phase2',ev('TD.game.boss.dialogueLog.length===3&&TD.game.boss.phase===2')and len(seen)>=4)
  shot('gosfer_duel');check('dialogue and lightning return movement control',ev('!TD.game.player.scripted'))
  frames(1);p.keyboard.press('f');frames(40);check('F toggles prone in duel',ev('TD.game.player.prone&&TD.game.player.stance==="prone"'))
  hp=ev('TD.game.player.hp');ev('TD.game.player.inv=0;TD.hurtPlayer(TD.game,1,400,428,{k:"laser"})');check('prone evades laser projectile damage',ev(f'TD.game.player.hp=={hp}'))
  ev('TD.game.player.inv=0;TD.hurtPlayer(TD.game,1,400,428,{k:"mg",hitsProne:true})');check('Retina machine gun hits prone',ev(f'TD.game.player.hp<{hp}'))
  ev('TD.game.player.inv=999');p.keyboard.down('d');p.keyboard.press('h');frames(10);check('roll starts and queues prone recovery',ev('TD.game.player.roll>0&&TD.game.player.rollProne&&TD.game.player.rollCd>4.7'));shot('roll_prone');frames(30);p.keyboard.up('d');check('roll finishes prone',ev('TD.game.player.prone&&TD.game.player.roll===0'));p.keyboard.press('h');frames(2);check('five second cooldown prevents immediate reroll',ev('TD.game.player.roll===0&&TD.game.player.rollCd>4'))
  frames(260);p.keyboard.press('h');frames(8);check('roll unlocks after five seconds',ev('TD.game.player.roll>0'))
  ev('TD.game.boss.state="windup";TD.game.boss.attack="retina";TD.game.boss.windup=.95;TD.game.boss.actionT=0;TD.game.boss.retina={x:TD.game.player.x,y:TD.game.player.y,t:0,locked:false};TD.game.boss.volleyTarget={x:TD.game.player.x,y:TD.game.player.y}');frames(45);shot('retina_warning');check('Retina aim locks before bullets',ev('TD.game.boss.retina.locked&&TD.game.boss.state==="windup"'));frames(23);check('Retina burst carries explicit prone hit flag',ev('TD.game.eshots.some(e=>e.owner===TD.game.boss&&e.k==="mg"&&e.hitsProne)'))
  ev('TD.game.eshots=[];TD.game.units=[];TD.game.boss=null;TD.game.fortress.relays=0;TD.game.player.y=402;TD.game.player.x=400;TD.game.player.prone=true;TD.game.player.roll=0;TD.game.structures.push(TD.makeStructure({kind:"od_bosswall",x:400,y:365}))');frames(3);p.keyboard.down('d');frames(12);p.keyboard.up('d');check('level3 wall-backed prone crawl uses new authored bank',ev('TD.game.player.cover&&TD.footPose(TD.game.player).key.startsWith("pb20_yuri_wall_prone")'));shot('fortress_wall_prone')
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start()');frames(100);shot('bastion_hud');p.keyboard.press('f');frames(30);p.keyboard.down('d');frames(12);p.keyboard.up('d');check('level7 supports actual prone and wall-backed crawl',ev('TD.game.player.prone&&TD.Bastion.playerPose(TD.game).startsWith("pb20_yuri_wall_prone")'));shot('bastion_wall_prone');p.keyboard.press('h');frames(10);check('level7 rolls into prone using eight frames',ev('TD.game.player.roll>0&&TD.game.player.rollProne&&TD.Bastion.playerPose(TD.game).includes("roll_prone")'));frames(30);check('level7 roll ends prone',ev('TD.game.player.prone&&TD.game.player.roll===0'));p.keyboard.press('h');frames(1);check('level7 also enforces five second roll cooldown',ev('TD.game.player.roll===0&&TD.game.player.rollCd>4'))
  hp=ev('TD.game.player.hp');ev('TD.game.player.inv=0;TD.Bastion.resolveEnemyShot(TD.game,{kind:"laser",tx:TD.game.player.x,damage:1,near:true})');check('base prone evades incoming direct laser',ev(f'TD.game.player.hp=={hp}'));ev('TD.Bastion.resolveEnemyShot(TD.game,{kind:"mg",tx:TD.game.player.x,damage:1,near:true,hitsProne:true})');check('base targeted machine gun can hit prone',ev(f'TD.game.player.hp<{hp}'))
  ev('TD.Bastion.startBoss(TD.game)');frames(100);ev('TD.Bastion.coreHit(TD.game,999)');frames(330);ev('Object.assign(TD.game.boss,{state:"run",t:.35,x:320,y:320,gait:.30,toX:735})');shot('helios_run');check('Helios run uses authored new gait',ev('TD.Bastion.heliosPose(TD.game.boss).key.startsWith("pb20_helios_run")'));ev('Object.assign(TD.game.boss,{state:"return",t:.4,gait:.40,toX:500})');shot('helios_walk');check('Helios walk uses authored new bank',ev('TD.Bastion.heliosPose(TD.game.boss).key.startsWith("pb20_helios_walk")'));ev('Object.assign(TD.game.boss,{state:"recover",t:.3,hitAge:1})');shot('helios_sidestep');check('Helios recovery uses new sidestep',ev('TD.Bastion.heliosPose(TD.game.boss).key.startsWith("pb20_helios_strafe")'))
  check('all new banks have eight distinct frames except four-frame portraits',ev('Object.entries(TD_BASTION20_ART.sequences).filter(([k,v])=>k.startsWith("pb20_")&&!k.includes("hud_")).every(([k,v])=>v.frames.length===(k.includes("portrait")?4:8)&&new Set(v.frames).size===v.frames.length)'))
  check('no page/console errors',not errors);result={'checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors};(O/'report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result));b.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
