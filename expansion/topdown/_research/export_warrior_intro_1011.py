from pathlib import Path
import sys,base64
from playwright.sync_api import sync_playwright
root=Path.cwd();sys.path.insert(0,str(root/'_BUILD_SOURCE'))
from shoot import serve
port,stop=serve(str(root))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page()
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0')
  p.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000)
  p.evaluate('TDGAME.freeze();TDGAME.start()')
  p.wait_for_function('Object.keys(TD_WARRIOR_ART.assets).every(k=>!!ART.get(k))')
  data=p.evaluate('''()=>{const B=TD.makeWarrior(TDGAME.G,0,0);B.x=B.y=0;B.a=B.upper=0;B.state='recover';
   const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d');
   x.imageSmoothingEnabled=false;x.translate(256,290);B.draw(x);return c.toDataURL('image/png').split(',')[1];}''')
  (root/'expansion/topdown/art/boss_intro_1011/source/warrior_in_game_front.png').write_bytes(base64.b64decode(data))
  print('Exported current Warrior through its own draw method into a fixed 512x512 transparent reference.');b.close()
finally:stop()
