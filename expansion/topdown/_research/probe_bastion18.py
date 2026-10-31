from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/bastion18_runtime';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
pack=json.loads((ROOT/'expansion/topdown/art/bastion18/manifest.json').read_text())
check('all new assets have even declared sizes and safe alpha gutters',all(all(v%2==0 for v in m['size'])and(Image.open(ROOT/m['file']).size==tuple(m['size']))and(m['bounds'][0]>=2 and m['bounds'][1]>=2 and m['bounds'][2]<=m['size'][0]-2 and m['bounds'][3]<=m['size'][1]-2 or k=='pb18_room')for k,m in pack['assets'].items()))
check('new graphics have binary alpha',all(set(np.asarray(Image.open(ROOT/m['file']).convert('RGBA'))[:,:,3].ravel()).issubset({0,255})for m in pack['assets'].values()))
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();ctx=browser.new_context(viewport={'width':1280,'height':960})
  ctx.add_init_script('''window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',connected:true,index:0,buttons:Array.from({length:16},()=>({pressed:false,value:0})),axes:[0,0,0,0]};navigator.getGamepads=()=>[testPad];window.pad=(...buttons)=>{testPad.buttons.forEach((b,i)=>{b.pressed=buttons.includes(i);b.value=b.pressed?1:0});};''')
  p=ctx.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1013-bastion18-r1',wait_until='domcontentloaded',timeout=90000)
  p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);p.wait_for_function('Object.keys(TD_BASTION18_ART.assets).every(k=>ART.get(k))',timeout=90000);ev=p.evaluate;ev('TDGAME.freeze()')
  def frames(n):
   while n:
    k=min(n,45);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  def key(k,n=2):p.keyboard.down(k);frames(1);p.keyboard.up(k);frames(n)
  def pad(*bs,n=1):ev('bs=>window.pad(...bs)',list(bs));frames(n)
  def go(state):ev('s=>{TD.Frontend.returnTo="title";TD.Frontend.go(s)}',state);frames(15)
  def select(act,who=2):ev('q=>TD.OriginalOptions.select(TD.OriginalOptions.rows().filter(r=>r.t!=="head").findIndex(r=>r.act===q.act&&r.who===q.who))',{'act':act,'who':who});frames(1)
  def snap(name):ev('TD.Achievements.queue=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  check('M30 auto preset preserves printed A/B/C/X/Y/Z receiver mapping',ev('TD.Input.padPreset()==="m30"&&JSON.stringify(["A","B","C","X","Y","Z"].map(k=>TD.Input.padProfile()[k]))==="[2,1,5,3,0,4]"'))
  go('options');select('A');pad(2);check('physical A arms controller capture',ev('TD.OriginalOptions.snapshot().capture==="A"&&TD.OriginalOptions.snapshot().who===2'));pad();pad(1)
  check('printed B can be captured without cancelling or rearming the row',ev('TD.game.state==="options"&&!TD.OriginalOptions.snapshot().capture&&TD.Input.padProfile().A===1&&TD.Input.padProfile().B===null'));pad()
  select('A',1);key('Enter');p.keyboard.press('F6');frames(1)
  check('a fast keyboard press is captured directly and stays out of navigation',ev('TD.BIND.A[0]==="f6"&&!TD.OriginalOptions.snapshot().capture&&TD.game.state==="options"'))
  ev('TD.OriginalOptions.select(TD.OriginalOptions.rows().filter(r=>r.t!=="head").length+1)');key('Enter');check('Apply saves both keyboard and physical controller bindings',ev('JSON.parse(localStorage.bof_od_keys).A[0]==="f6"&&JSON.parse(localStorage.bof_td_controllers)[testPad.id].A===1&&TD.game.state==="title"'))
  p.reload(wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev('TDGAME.freeze()');frames(15)
  check('bindings survive a fresh page load',ev('TD.BIND.A[0]==="f6"&&TD.Input.padProfile().A===1'))
  go('options');select('Y');pad(2);pad();pad(5);pad();check('another printed button binds after the first custom mapping',ev('TD.Input.padProfile().Y===5&&!TD.OriginalOptions.snapshot().capture'));key('Escape');check('Cancel restores the complete saved preset and bindings',ev('TD.Input.padPreset()==="m30"&&TD.Input.padProfile().Y===0&&TD.Input.padProfile().A===1'))
  ev('TD.Input.resetKeys();TD.Input.setPadPreset("m30")');go('options');select('preset');key('Enter');check('Genesis preset omits nonexistent shoulders in its settings and learning list',ev('TD.Input.padPreset()==="genesis"&&!TD.OriginalOptions.rows().some(r=>r.who===2&&["L","R"].includes(r.act))&&!TD.Input.padProfile().L'));snap('genesis_options')
  select('learn');key('Enter');frames(15);check('Genesis learning opens a twelve-input six-button wizard',ev('TD.game.state==="padsetup"&&TD.Input.setup.steps.length===12'));snap('genesis_setup')
  for axis,sgn in [(1,-1),(1,1),(0,-1),(0,1)]:ev('testPad.axes=[0,0,0,0];pad()');frames(1);ev('q=>testPad.axes[q[0]]=q[1]',[axis,sgn]);frames(1)
  ev('testPad.axes=[0,0,0,0]')
  for b in [2,1,5,3,0,4,8,9]:pad();pad(b,10) if b==8 else pad(b)
  pad();check('every Genesis input can be learned even when Mode also reports a mirrored button',ev('TD.Input.setup.done&&TD.Input.padProfile().A===2&&TD.Input.padProfile().up.axis===1&&TD.Input.padPreset()==="genesis"'));pad(9);pad();frames(15)
  check('learned Genesis mapping returns to settings without discarding changes',ev('TD.game.state==="options"&&TD.Input.padProfile().A===2&&TD.Input.padProfile().Z===4'))
  ev('TD.Input.setPadPreset("m30")');go('help');snap('m30_help');check('controller diagrams match M30 and original Genesis layouts',ev('!!ART.get("pb18_pad_m30")&&!!ART.get("pb18_pad_genesis")&&TD.Input.padName().includes("M30")'))
  def fresh(room=1):
   ev('pad();testPad.axes=[0,0,0,0];TD.Input.resetKeys();TD.Input.setPadPreset("m30");TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Input.pointer.active=false');frames(100)
   if room>1:ev(f'TD.game.units=[];TD.game.bastion.totalWave={room-1};TD.Bastion.wave(TD.game)')
  fresh();check('first room has a live animated door core and two mounted corner turrets',ev('TD.game.bastion.wallCore.hp>0&&TD.game.bastion.turrets.length===2&&TD.game.bastion.turrets[0].x===128&&TD.game.bastion.turrets[1].x===512'));frames(75);snap('room_1')
  ev('TD.game.player.inv=999;for(const u of TD.game.units)TD.Bastion.kill(TD.game,u);for(const t of TD.game.bastion.turrets)t.hp=0');frames(10);check('room cannot clear until its door core is destroyed',ev('TD.game.bastion.phase==="fight"&&TD.game.bastion.wallCore.hp>0'))
  ev('TD.game.bastion.wallCore.hp=0;window.coverGeneration=TD.game.bastion.wallGeneration');frames(1);frames(30);snap('wall_blast')
  while ev('TD.game.bastion.transition?.phase')!='hop':frames(1)
  frames(22);snap('cover_hop');check('Yuri hops while the protective wall retains its actual height',ev('TD.Bastion.playerPose(TD.game).startsWith("pb17_yuri_jump")&&TD.Bastion.transitionView(TD.game).wallY===440&&TD.Bastion.transitionView(TD.game).wallScale===1&&(()=>{const v=TD.Bastion.transitionView(TD.game),m=TD_ASSAULT_ART.assets[TD.Bastion.playerPose(TD.game)];return v.y+(m.bounds[3]-m.anchor[1])*m.drawScale<358})()'))
  while ev('TD.game.bastion.transition?.phase')!='walk':frames(1)
  frames(16);snap('wall_passes_camera');check('forward camera motion enlarges cover before it passes beneath the camera',ev('TD.Bastion.transitionView(TD.game).wallScale>1&&TD.Bastion.transitionView(TD.game).zoom>1'))
  while ev('TD.game.bastion.transition?.phase')!='black':frames(1)
  snap('black_passage');pix=np.asarray(Image.open(OUT/'black_passage.png').convert('RGB'));check('black passage really fades the whole scene to black',float(pix.mean())<1)
  frames(85);check('next room arrives with an intact new wall, door core and corners',ev('TD.game.bastion.totalWave===2&&TD.game.bastion.wallCore.hp>0&&TD.game.bastion.turrets.length===2&&TD.game.bastion.cover.every(w=>w.hp===w.max)&&TD.game.bastion.wallGeneration===coverGeneration+1&&TD.Cam.zoom===1'))
  for room in range(3,9):fresh(room);check(f'room {room} has its own compulsory core',ev('TD.game.bastion.wallCore?.hp>0||TD.game.boss?.form==="core"&&TD.game.bastion.totalWave===8'))
  frames(150);snap('master_core');first=ev('TD.game.bastion.coreRays.map(r=>r.angle)');frames(15);check('master core has three moving laser rays and eight rotating glass-core frames',ev('TD.game.bastion.coreRays.length===3&&TD_BASTION18_ART.sequences.pb18_master.frames.length===16')and first!=ev('TD.game.bastion.coreRays.map(r=>r.angle)'))
  ev('TD.Bastion.coreHit(TD.game,90)');snap('master_glass_cracked');check('real core damage selects fractured glass artwork',ev('TD.Bastion.masterPose(TD.game.boss)==="pb18_master_9"'))
  ev('TD.Bastion.coreHit(TD.game,999);TD.game.player.inv=0;window.hp=TD.game.player.hp;window.smoke=TD.game.player.smoke;TD.Bastion.harm(TD.game,4);pad(0,2)');frames(35);snap('master_glass_shatter');check('transformation has authored glass-shatter frames and protects the player',ev('TD.Bastion.masterPose(TD.game.boss).startsWith("pb18_master_1")&&TD.game.player.hp===hp&&TD.game.player.smoke===smoke'))
  frames(55);snap('white_energy');pix=np.asarray(Image.open(OUT/'white_energy.png').convert('RGB'));check('energy release is an actual blinding full-screen white-out',float(pix.mean())>250)
  pad();frames(215);snap('helios_reveal');check('animated Helios emerges after the light fades',ev('TD.game.boss.form==="helios"&&TD.game.bastion.flash===0&&TD.Bastion.heliosPose(TD.game.boss).key.startsWith("pb18_helios_")'))
  check('Helios has complete distinct walk/run/idle/throw/lightning/jump/hit/death banks',ev('["walk","run","idle","throw","lightning","jump","hit","death"].every(a=>TD_BASTION18_ART.sequences["pb18_helios_"+a].frames.length===8)'))
  ev('Object.assign(TD.game.boss,{state:"run",x:200,toX:735,fromX:200,t:0,gait:0});window.runKeys=[]');
  for i in range(16):frames(3);ev('runKeys.push(TD.Bastion.heliosPose(TD.game.boss).key)')
  check('actual boss running uses at least six unique gait frames',ev('new Set(runKeys).size>=6'));snap('helios_run')
  for state,name,n in [('return','helios_walk',18),('volley','helios_volley',25),('lightning','helios_cast',42),('jump','helios_jump',30)]:ev('q=>Object.assign(TD.game.boss,{state:q,x:320,y:320,fromX:320,toX:450,returnFrom:320,t:0,jumpX:320,jumpY:320,volley:0,lightning:false})',state);frames(n);snap(name)
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.structures=[];TD.game.player.y=430;TD.game.boss=TD.makeGosfer(TD.game,400,195);TD.Achievements.queue=[]');frames(200);snap('gosfer_live')
  check('Gosfer has eight new walk frames in each orientation plus fire/dash/death',ev('["south","north","east","west"].every(d=>TD_BASTION18_ART.sequences["pb18_gosfer_walk_"+d].frames.length===8)&&["fire_south","fire_east","dash_east","death"].every(a=>TD_BASTION18_ART.sequences["pb18_gosfer_"+a].frames.length===8)'))
  ev('window.gosferKeys=[];TD.game.player.inv=999;TD.game.boss.burst=0;TD.game.boss.cd=999')
  for i in range(20):frames(3);ev('gosferKeys.push(TD.gosferPose(TD.game.boss).key)')
  check('Gosfer movement actually advances multiple authored gait poses',ev('new Set(gosferKeys).size>=5'))
  # Every newly registered cell is rendered by the actual native ART registry.
  keys=list(pack['assets']);
  for page_index in range((len(keys)+47)//48):
   batch=keys[page_index*48:(page_index+1)*48];ev('ks=>{let c=document.getElementById("art-review");if(!c){c=document.createElement("canvas");c.id="art-review";document.body.appendChild(c)}c.width=1200;c.height=800;const g=c.getContext("2d");g.imageSmoothingEnabled=false;g.fillStyle="#101923";g.fillRect(0,0,1200,800);ks.forEach((k,i)=>{const a=ART.get(k),s=Math.min(140/a.sw,120/a.sh),x=(i%8)*150,y=Math.floor(i/8)*132;g.drawImage(a.im,a.sx,a.sy,a.sw,a.sh,x,y,a.sw*s,a.sh*s);g.fillStyle="#fff";g.font="8px monospace";g.fillText(k,x+2,y+124)})}',batch);p.locator('#art-review').screenshot(path=str(OUT/f'native_art_{page_index}.png'))
  check('all 193 new registered keys decode and render through native ART',ev('Object.keys(TD_BASTION18_ART.assets).length===193&&Object.keys(TD_BASTION18_ART.assets).every(k=>ART.get(k))'))
  check('no browser or resource errors',not errors)
  report={'build':'overdrive1013-bastion18-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'scope':'Fresh Chromium context, synthetic M30 and actual keyboard capture events; isolated native gameplay fixtures, not full unassisted difficulty.'};(OUT/'focused.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));browser.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
