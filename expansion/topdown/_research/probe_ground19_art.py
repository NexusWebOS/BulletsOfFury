from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/bastion19/gallery';O.mkdir(parents=True,exist_ok=True);d=json.loads((R/'expansion/topdown/art/bastion19/manifest.json').read_text());keys=[a['key']for a in d['audit']];errors=[]
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate;ev('TDGAME.freeze();TD.Achievements.queue=[];window.newKeys='+json.dumps(keys));p.wait_for_function('newKeys.every(k=>ART.get(k))',timeout=60000)
  ev('''window.gallery=document.createElement('canvas');gallery.width=1280;gallery.height=960;gallery.style.cssText='position:fixed;inset:0;z-index:10;width:1280px;height:960px;background:#0c121b';document.body.appendChild(gallery);window.renderGallery=(keys)=>{const ctx=gallery.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.fillStyle='#101721';ctx.fillRect(0,0,1280,960);keys.forEach((k,i)=>{const x=i%8*160,y=Math.floor(i/8)*240,m=TD_ASSAULT_ART.assets[k],r=m.bounds,w=r[2]-r[0],h=r[3]-r[1],s=Math.min(1,148/w,200/h);ctx.fillStyle='#e2e7ef';ctx.font='10px monospace';ctx.fillText(k.replace('pb19_',''),x+3,y+14);TD.AssaultArt.draw(ctx,k,x+80+((m.anchor[0]-(r[0]+r[2])/2)*s),y+32+(m.anchor[1]-r[1])*s,{s});});};void 0;''')
  for n in range(0,len(keys),32):
   ev('renderGallery('+json.dumps(keys[n:n+32])+')');p.locator('canvas').last.screenshot(path=str(O/(f'page_{n//32:02}.png')))
  ev('gallery.remove();TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.World.load(800,2400,[]);TD.game.structures=[];TD.game.player.y=428;TD.game.boss=TD.makeGosfer(TD.game,400,195)')
  def frames(n):
   while n:
    k=min(40,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  frames(185);p.mouse.move(600,400);p.mouse.down();ev('TD.game.player.inv=999;window.initialHP=TD.game.boss.hp')
  for i in range(500):
   if ev('TD.game.boss.dead'):break
   ev('const g=TD.game.boss;TD.Input.pointer.x=g.x-TD.Cam.x;TD.Input.pointer.y=g.y-65-TD.Cam.y;TD.Input.pointer.active=true');frames(6)
  hit=ev('TD.game.boss.dead&&TD.game.boss.hp===0');ev('TDGAME.render()');p.locator('#screen').screenshot(path=str(O/'gosfer_actual_rifle_defeat.png'))
  result={'nativeFilesRendered':len(keys),'errors':errors,'gosferActualRifleDefeat':hit,'scope':'Native Art.draw rendering of every new PNG plus protected actual rifle/animated Gosfer collision fixture. Armor protected only in isolated boss fixture.'};(O/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));b.close()
finally:stop()
sys.exit(0 if hit and not errors else 1)
