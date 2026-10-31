"""Native-browser tests using the connected receiver's documented raw HID layout.
Synthetic button presses verify game behavior; this is not physical-button QA.
"""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/bastion18_m30';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,v):
 checks.append({'name':name,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.add_init_script('''window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};
  Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[testPad]});
  if(!localStorage.m30Fixture){localStorage.m30Fixture='1';localStorage.bof_td_controllers=JSON.stringify({[testPad.id]:{A:0,B:1,C:5,X:2,Y:3,Z:4,mode:8,start:9,L:6,R:7}});}
  window.pad=(...ids)=>testPad.buttons.forEach((v,i)=>{v.pressed=ids.includes(i);v.value=+v.pressed;});''')
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1013-bastion17-r1',timeout=90000,wait_until='domcontentloaded')
  p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
  def ev(s):return p.evaluate(s)
  def frames(n=1):ev(f'TDGAME.step({n})')
  def pad(*ids):p.evaluate('v=>pad(...v)',list(ids))
  def fresh():
   ev('pad();testPad.axes=[0,0];TDGAME.freeze();TD.Input.update();TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=5;TDGAME.start();TD.Input.pointer.active=false;TD.Achievements.queue=[];TD.game.msgs=[];TD.game.player.inv=999;TDGAME.step(2)')
  fresh()
  check('legacy generic preset migrates to receiver physical letters',ev('JSON.stringify(TD.Input.padProfile())===JSON.stringify({A:2,B:1,C:5,X:3,Y:0,Z:4,mode:8,start:9,L:6,R:7})'))
  check('migrated receiver layout persists with explicit six-button style',ev('JSON.parse(localStorage.bof_td_controllers)[testPad.id].style==="six"&&JSON.parse(localStorage.bof_td_controllers)[testPad.id]._source==="m30-24g-v1"'))
  pad(2);frames(2)
  check('physical M30 A fires actual Level7 rifle projectiles',ev('TD.game.bastion.bullets.length>0&&TD.game.player.smoke===5&&!TD.game.player.prone'))
  ev('TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/'m30_A_fires_level7.png'))
  fresh();pad(0);frames(2)
  check('physical M30 Y throws grenade without firing rifle',ev('TD.game.player.smoke===4&&TD.game.bastion.bullets.length===0'))
  fresh();pad(3);frames(15)
  check('physical M30 X toggles duck without firing',ev('TD.game.player.prone&&TD.game.player.rise===0&&!TD.game.bastion.bullets.length'))
  fresh();pad(4);ev('testPad.axes[0]=1;window.x=TD.game.player.x;window.aimX=TD.game.bastion.cursor.x');frames(12)
  check('physical Z plus D-pad free aims without moving Yuri',ev('TD.game.player.freeAim&&TD.game.player.x===x&&TD.game.bastion.cursor.x>aimX'))
  fresh();ev('TD.game.bastion.cursor={x:320,y:170};window.px=TD.game.player.x');pad(1);ev('testPad.axes[0]=-1');frames(1)
  check('physical M30 B plus left performs immediate side fire without foot movement',ev('TD.game.player.quickSide===-1&&TD.game.player.x===px&&TD.game.bastion.quickShots===1'))
  pad();ev('testPad.axes[0]=0');frames(1)
  check('releasing physical B restores the original Retina target',ev('TD.game.bastion.cursor.x===320&&TD.game.bastion.cursor.y===170&&!TD.game.player.quickSide'))
  fresh();pad(8);frames(15)
  check('physical Mode takes cover',ev('TD.game.player.rise===0'))
  fresh();pad(2);frames();ev('TD.Input.holdCombat();TD.game.bastion.bullets=[];TD.game.player.fireCd=0');frames(2)
  check('held physical A is latched through cutscene boundary',ev('TD.game.bastion.bullets.length===0'))
  pad();frames();pad(2);frames(2)
  check('physical A fires again after release',ev('TD.game.bastion.bullets.length>0'))
  fresh();ev('TD.Input.setPadStyle("six")')
  check('resetting six-button controls retains receiver-correct A',ev('TD.Input.padProfile().A===2&&TD.Input.padProfile().Y===0'))
  ev('TD.Input.setPadStyle("standard")');fresh();pad(2);frames(2)
  check('standard control scheme on the raw M30 still uses printed A to fire',ev('TD.Input.padStyle()==="standard"&&TD.game.bastion.bullets.length>0&&TD.game.player.smoke===5'))
  ev('pad();TD.Input.setPadStyle("six")');frames()
  ev('TD.Input.setPadBinding("A",10);TD.Input.setPadBinding("up",11);testPad.connected=false;TD.Input.update();testPad.connected=true;TD.Input.update()')
  check('custom receiver bindings survive reconnect',ev('TD.Input.padProfile().A===10&&TD.Input.padProfile().up===11'))
  p.reload(wait_until="domcontentloaded");p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000);ev('TDGAME.freeze();TD.Input.update()')
  check('custom receiver bindings survive page reload',ev('TD.Input.padProfile().A===10&&TD.Input.padProfile().up===11&&TD.Input.padStyle()==="six"'))
  ev('testPad.id="Other unknown six-button pad";TD.Input.update();TD.Input.setPadStyle("six")')
  check('unknown controller retains generic six-button preset',ev('TD.Input.padProfile().A===0&&TD.Input.padProfile().Y===3'))
  ev('testPad.id="Standard M30 (Vendor: 0ca3 Product: 0024)";testPad.mapping="standard";TD.Input.update();TD.Input.setPadStyle("six")')
  check('browser-standardized M30 report avoids raw receiver remapping',ev('TD.Input.padProfile().A===0&&TD.Input.padProfile().X===2'))
  ev('testPad.id="Mode changing 6B controller (Vendor: 0ca3 Product: 0024)";testPad.mapping="";TD.Input.update();testPad.mapping="standard";TD.Input.update()')
  check('built-in raw receiver layout does not leak across a standardized mode change',ev('TD.Input.padProfile().A===0&&TD.Input.padProfile().X===2'))
  ev('testPad.id="Legacy calibrated six-button pad";testPad.mapping="";TD.Input.update();TD.Input.setPadStyle("six");TD.Input.beginSetup();TD.Frontend.go("padsetup")')
  frames(20)
  # Existing full learning flow, with physical letters in receiver order.
  for index in [12,13,14,15,2,1,5,3,0,4,8,9,6,7]:
   ev('testPad.buttons=Array.from({length:16},()=>({pressed:false,value:0}))');frames(2);pad(index);frames(1)
  check('learned six-button profile records explicit style and custom ownership',ev('TD.Input.setup.done&&JSON.parse(localStorage.bof_td_controllers)[testPad.id].style==="six"&&JSON.parse(localStorage.bof_td_controllers)[testPad.id]._source==="custom"'))
  check('zero browser or asset errors',not errors)
  result={'build':'overdrive1013-bastion17-r1','checks':checks,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks),'errors':errors,'hardware':'Windows confirms receiver VID_0CA3/PID_0024. Button presses here are synthetic, using the documented Windows HID mapping.'}
  (OUT/'report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  (ROOT/'docs/qa/overdrive_bastion18_m30.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True);b.close()
finally:stop()
sys.exit(0 if all(q['passed'] for q in checks) and not errors else 1)
