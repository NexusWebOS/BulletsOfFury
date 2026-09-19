import base64, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
out=root/'_shots'/'shield_palette_0919';out.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(root))
errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  page=browser.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)[:200]))
  page.goto('http://127.0.0.1:%s/index.html'%port,wait_until='load',timeout=60000)
  page.wait_for_function("typeof XART!=='undefined'&&typeof drawShieldBarArt==='function'",timeout=45000)
  keys=['bmbar_frame_shield_v2','bmbar_frame_shield_volcano','bmbar_frame_shield_steel',
        'bmbar_sf2_hex','bmbar_shield_volcano_fill_hex','bmbar_shield_steel_fill_hex']
  page.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',keys)
  page.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=keys,timeout=45000)
  data=page.evaluate("""() => {const cv=ctx.canvas;ctx.save();ctx.fillStyle='#16191e';ctx.fillRect(0,0,480,512);
    drawShieldBarArt(.7,240,105,440,null);
    drawShieldBarArt(.7,240,250,440,{_mwBarrier:{active:true,maxhp:100,hp:70}});
    drawShieldBarArt(.7,240,395,440,{_shieldGaugeStyle:'level5_steel',_shieldMax:100,_shieldHp:70});
    ctx.restore();return {png:cv.toDataURL('image/png'),keys:['bmbar_frame_shield_volcano','bmbar_frame_shield_steel'].map(k=>XART._src[k])};}""")
  (out/'all_three.png').write_bytes(base64.b64decode(data['png'].split(',',1)[1]))
  print(json.dumps({'keys':data['keys'],'errors':errors,'image':str(out/'all_three.png')},indent=2))
  browser.close()
finally:stop()
