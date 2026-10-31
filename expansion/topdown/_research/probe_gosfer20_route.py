"""Arena entry fixture; only ordinary control input after entry, normal armor."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/bastion20/gosfer_route';O.mkdir(parents=True,exist_ok=True);errors=[];port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000)
  p.evaluate('''TDGAME.freeze();TD.pilot='yuri';TD.difficulty='normal';TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.fortress.relays=3;TD.game.player.x=400;TD.game.player.y=428;TD.game.boss=TD.makeGosfer(TD.game,400,195);TD.Achievements.queue=[];
  window.bot20={last:null,states:[],minHP:3,shots:0,rolls:0,locks:0,lastLock:false};
  TD.Input.aim=()=>{const p=TD.game.player,b=TD.game.boss;return b?TD.M.angTo(p.x,p.y,b.x,b.y):Math.PI;};
  TD.Input.update=function(){this.last=this.state;this.pulses=new Set();this.raw={};this.pointer.active=false;const G=TD.game,p=G.player,b=G.boss,r=bot20;let s={};if(b&&!b.dead&&!p.dead&&!['enter','dialogue','transform'].includes(b.state)){
   if(!p.prone&&p.roll<=0)s.prone=true;s.A=true;r.shots++;if(b.retina){if(!r.lastLock){r.locks++;r.direction=p.x<400?1:-1;}s.left=r.direction<0;s.right=r.direction>0;if(b.retina.locked&&p.rollCd<=0&&Math.abs(p.x-b.retina.x)<60&&p.x>255&&p.x<545){s.X=true;r.rolls++;}}r.lastLock=!!b.retina;
  }r.minHP=Math.min(r.minHP,p.hp);if(b&&!r.states.includes(b.state+':'+b.phase))r.states.push(b.state+':'+b.phase);this.state=s;};void 0;''')
  captured=set()
  for i in range(360):
   p.evaluate('TDGAME.step(40)');p.wait_for_timeout(1)
   q=p.evaluate('({state:TD.game.state,dead:TD.game.player.dead,bossDead:TD.game.boss.dead,bossState:TD.game.boss.state,phase:TD.game.boss.phase,hp:TD.game.boss.hp,time:TD.game.time,armor:TD.game.player.hp,deaths:TD.game.deaths})')
   if q['bossState']not in captured:
    captured.add(q['bossState']);p.evaluate('TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(q['bossState']+'.png')))
   if i%24==0:print(q,flush=True)
   if q['bossDead']or q['deaths']or q['state']=='gameover':break
  result=p.evaluate('({state:TD.game.state,time:TD.game.time,hp:TD.game.player.hp,deaths:TD.game.deaths,score:TD.game.score,boss:{hp:TD.game.boss.hp,dead:TD.game.boss.dead,phase:TD.game.boss.phase,barrierLog:TD.game.boss.barrierLog,dialogueLog:TD.game.boss.dialogueLog},bot:bot20})');result['errors']=errors;result['scope']='Normal armor, arena entry fixture. Only ordinary firing, prone, lateral movement and roll control input during fight. No health writes or boss kill calls.';(O/'report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result));b.close()
finally:stop()
sys.exit(0 if result['boss']['dead']and result['deaths']==0 and not errors else 1)
