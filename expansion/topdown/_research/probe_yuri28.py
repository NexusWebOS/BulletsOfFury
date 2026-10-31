"""Native M30 inputs for upward travel with independent side aim/fire."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/yuri28';O.mkdir(exist_ok=True);checks=[];errors=[];measured={}
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  p.add_init_script('''window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});''')
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-yuri28-r1',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate
  ev('TDGAME.freeze();TD.Input.setPadPreset("m30");ART.warm(Object.keys(TD_YURI28_ART.assets));');p.wait_for_function('Object.keys(TD_YURI28_ART.assets).every(k=>!!ART.get(k))',timeout=90000)
  def frames(n):
   while n:k=min(n,30);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  def fresh():
   ev('pad();testPad.axes=[0,0];TD.Input.pointer.active=false;TD.Input.update();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.units=[];TD.game.fortress.pending=[];TD.Achievements.queue=[];TD.game.msgs=[];Object.assign(TD.game.player,{x:400,y:2360,inv:0});');frames(1)
  def shot(name):ev('TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(name+'.png')))
  check('all58new images decode through native ART',ev('Object.keys(TD_YURI28_ART.assets).length===58'))
  check('common even192x224cells and root96,160',ev('Object.values(TD_YURI28_ART.assets).every(m=>m.size[0]===192&&m.size[1]===224&&m.anchor[0]===96&&m.anchor[1]===160&&m.drawScale===1)'))
  check('both facings have16movement and12firing drawings',ev('["east","west"].every(d=>TD_YURI28_ART.sequences["y28_"+d+"_up_step"].frames.length===16&&TD_YURI28_ART.sequences["y28_"+d+"_up_fire"].frames.length===12)'))
  draws=ev('''()=>{const c=document.createElement('canvas');c.width=192;c.height=224;const ctx=c.getContext('2d');let count=0,empty=[];for(const key of Object.keys(TD_YURI28_ART.assets)){ctx.clearRect(0,0,192,224);TD.AssaultArt.draw(ctx,key,96,160,{s:1});const d=ctx.getImageData(0,0,192,224).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;if(n<200)empty.push(key);count++;}return{count,empty};}''')
  check('every frame draws actual nonempty native pixels',draws['count']==58 and not draws['empty'])
  for direction,button,sign in [('east',1,1),('west',0,-1)]:
   fresh();ev(f'testPad.axes[1]=-1;pad({button});');frames(1)
   check(direction+' side-fire spawns bullets from the measured barrel',ev('''(()=>{const G=TD.game,s=G.shots[0],m=TD.footVisualSocket(G.player);return s&&Math.hypot(s.x-s.vx-m.x,s.y-s.vy-(s.drawLift||0)-m.y)<.01;})()'''))
   check(direction+' flash follows the current animated gun socket',ev('''(()=>{const p=TD.game.player,f=TD.FX.list.find(f=>f.k==='attached'&&f.actor===p),m=TD.footVisualSocket(p);if(!f)return false;const q=f.socket(p);return Math.hypot(q.x-m.x,q.y-m.y)<.01;})()'''))
   seen=set()
   for i in range(20):frames(1);seen.add(ev('TD.footPose(TD.game.player).key'))
   state=ev('({pose:TD.footPose(TD.game.player),x:TD.game.player.x,y:TD.game.player.y,aim:TD.game.player.aim,shots:TD.game.shots.map(s=>s.vx)})');measured[direction]=state
   check('M30 up+'+('B'if direction=='east'else'Y')+' selects '+direction+' upward firing',state['pose']['bank']=='y28_'+direction+'_up_fire'and state['x']==400 and state['y']<2310)
   check(direction+' firing keeps an advancing gait',len(seen)>=6)
   check(direction+' shots keep the side aim',bool(state['shots'])and all(v*sign>0 for v in state['shots']))
   shot(direction+'_up_fire')
   ev('pad();');frames(12);seen=set()
   for i in range(12):frames(1);seen.add(ev('TD.footPose(TD.game.player).key'))
   check(direction+' release fire keeps the side aim and selects the movement bank',ev('TD.footPose(TD.game.player).bank==="y28_'+direction+'_up_step"')and len(seen)>=5);shot(direction+'_up_step')
   ev('testPad.axes[1]=0');frames(1);check(direction+' stopping does not keep walking feet',ev('!TD.game.player.moving&&!TD.footPose(TD.game.player).key.startsWith("y28_")'))
  fresh();ev('TD.game.player.y=2180;testPad.axes[1]=-1;pad(1)');frames(35);y=ev('TD.game.player.y');frames(10)
  check('barrier collision stops the new gait instead of walking in place',ev('!TD.game.player.moving&&!TD.footPose(TD.game.player).key.startsWith("y28_")&&Math.abs(TD.game.player.y-'+str(y)+')<.01'));shot('barrier_stop')
  fresh();ev('testPad.axes[0]=1;pad(1)');frames(10);check('ordinary horizontal running retains its existing animation',ev('TD.game.player.moving&&!TD.footPose(TD.game.player).key.startsWith("y28_")'))
  fresh();ev('testPad.axes[1]=-1;pad(1)');frames(6);ev('pad(8,3)');frames(1);ev('pad(1)');frames(8);check('prone/crawl retains its authored bank',ev('TD.game.player.prone&&!TD.footPose(TD.game.player).key.startsWith("y28_")'))
  fresh();ev('testPad.axes[1]=-1;pad(1)');frames(6);ev('pad(5)');frames(1);check('roll retains its authored bank',ev('TD.game.player.roll>0&&!TD.footPose(TD.game.player).key.startsWith("y28_")'))
  fresh();ev('testPad.axes[1]=-1;pad(1)');frames(6);ev('pad(1,9)');frames(1);ev('pad(1)');frames(1);phase=ev('TD.game.player.gaitPhase');frames(12);check('pause freezes the new gait',ev('TD.game.state==="pause"&&TD.game.player.gaitPhase==='+str(phase)))
  # Probe actual hit feedback through the new pose/draw path, on the native renderer.
  fresh();ev('testPad.axes[1]=-1;pad(1)');frames(3);ev('TD.game.player.inv=0;TD.hurtPlayer(TD.game,1,TD.game.player.x,TD.game.player.y);TDGAME.render()');check('new side-step keeps the actual damage flash timer',ev('TD.game.player.hp===2&&TD.game.player.flash>0'));frames(3);check('damaged new pose draws visible white hit pixels',ev('(()=>{TDGAME.render();const c=document.getElementById("screen"),s=c.width/640,d=c.getContext("2d").getImageData(0,Math.floor(100*s),c.width,Math.floor(350*s)).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>245&&d[i+1]>245&&d[i+2]>245)n++;return n>400;})()'));frames(13);check('damage flash expires on the normal clock',ev('TD.game.player.flash===0'))
  old=json.loads((R/'_shots/lighting22/retained_art.json').read_text(encoding='utf-8'));check('all820previous PNGs remain unchanged',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==h for k,h in old.items()))
  # Stage7's fixed-depth combat/traversal retains its own player-pose owner.
  ev('pad();testPad.axes=[0,0];TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Achievements.queue=[];');frames(120);shot('stage7_retained');check('stage7 retains cover/HUD/exposure and its authored player',ev('TD.game.player.pseudo3D&&TD.Hud27.roomBrightness===.75&&TD.CornerHUD26.last.font==="Overdrive Arcade HUD"&&!TD.Bastion.playerPose(TD.game).startsWith("y28_")'))
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/yuri28/preview.html',wait_until='domcontentloaded');p.wait_for_function('typeof data!=="undefined"&&data&&Object.keys(images).length===60',timeout=90000);p.locator('#review').screenshot(path=str(O/'review.png'));p.locator('#onion').check();p.locator('#old').check();p.locator('#slow').check();p.wait_for_timeout(150);p.locator('#review').screenshot(path=str(O/'onion.png'));check('native viewer supports onion, half-speed and old-size overlay',p.evaluate('document.getElementById("onion").checked&&document.getElementById("old").checked&&document.getElementById("slow").checked'))
  check('no browser, shader or asset errors',not errors)
  report={'build':'overdrive1015-yuri28-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'measurements':measured,'nativeFrames':draws,'scope':'Real game renderer with synthetic raw M30 inputs in isolated stage3 fixtures; not physical hardware or a full campaign playthrough.'};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));b.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
