from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import base64,json
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/level36';O.mkdir(parents=True,exist_ok=True)
errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1016-base36-r1',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000)
 p.evaluate('TDGAME.freeze();TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();ART.warm(Object.keys(TD_LEVEL36_ART.assets));');p.wait_for_function('Object.keys(TD_LEVEL36_ART.assets).every(k=>ART.get(k))',timeout=120000)
 for name,x,y in [('start',400,2680),('columns',350,2250),('alcoves',400,1690),('route',400,1230),('gate',400,760),('arena',400,450)]:
  p.evaluate(f'TD.game.player.x={x};TD.game.player.y={y};TD.game.player.inv=0;TD.game.units=[];TD.game.fortress.pending=[];TD.Cam.zoom=1.25;TD.Cam.follow({x},{y},1);TD.game.msgs=[];TD.Achievements.queue=[];TDGAME.render();');p.locator('#screen').screenshot(path=str(O/(name+'.png')))
 data=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=800;c.height=2800;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;const a=ART.get('l36_ground');ctx.drawImage(a.im,a.sx,a.sy,a.sw,a.sh,0,0,800,2800);const m=TD.MISSIONS.find(m=>m.id===3);for(let y=0;y<2800;y+=400){TD.Cam.y=y;ctx.save();ctx.beginPath();ctx.rect(0,y,800,400);ctx.clip();m.drawFloor(ctx,TD.game);TD.Depth35.drawActors(ctx,TD.game);ctx.restore();}return c.toDataURL('image/png').split(',')[1]}''');(O/'map_overview.png').write_bytes(base64.b64decode(data))
 print(json.dumps({'errors':errors,'assets':p.evaluate('Object.keys(TD_LEVEL36_ART.assets).length')}));b.close()
cells=Image.new('RGB',(1200,900))
for i,n in enumerate(['start','columns','alcoves','route','gate','arena']):
 im=Image.open(O/(n+'.png'));im.thumbnail((400,450),Image.Resampling.NEAREST);cells.paste(im,((i%3)*400,(i//3)*450))
cells.save(O/'native_review.png')
