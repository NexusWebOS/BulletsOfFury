"""Export a short visual preview from the actual live dossier renderer."""
from pathlib import Path
from io import BytesIO
import sys
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import serve
OUT=ROOT/'_shots/overdrive_intro_1011';OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();page=b.new_page(viewport={'width':1280,'height':964})
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0')
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=60000)
  page.evaluate('TDGAME.freeze();TDGAME.start();TDGAME.G.units=[];TDGAME.G.player.y=650;TDGAME.G.player.inv=99999;TDGAME.step()')
  page.wait_for_function('TD.BossIntro.warm.every(k=>!!ART.get(k))')
  for _ in range(30):
   if page.evaluate('TDGAME.G.bossIntro.phase==="card"'):break
   page.evaluate('TDGAME.step(24)');page.wait_for_timeout(1)
  for _ in range(11):page.evaluate('TDGAME.step(24)');page.wait_for_timeout(1)
  page.evaluate('TDGAME.G.bossIntro.yaw=0;TDGAME.G.player.inv=0;TDGAME.render()')
  images=[]
  for _ in range(32):
   raw=page.locator('#screen').screenshot()
   images.append(Image.open(BytesIO(raw)).convert('RGB').resize((800,600),Image.Resampling.NEAREST))
   page.evaluate('TDGAME.step(6)');page.wait_for_timeout(1)
  images[0].save(OUT/'warrior_card_preview.gif',save_all=True,append_images=images[1:],duration=100,loop=0,optimize=False)
  b.close()
finally:stop()
print('Saved native 800x600 animated dossier preview (32 frames, 3.2 seconds).')
