from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;S=W/'source';S.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
port,stop=serve(str(R))
try:
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1280,'height':800});page.goto(f'http://127.0.0.1:{port}/index.html?quality=high');page.wait_for_function('window.__bofFrames>3',timeout=180000)
  keys={'pilot':'cole_body_0922','ship':'ship_cole_pv2'}
  for name,key in keys.items():
   page.wait_for_function('k=>XART.rdy(k)',arg=key,polling=100,timeout=90000)
   out=page.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext('2d').drawImage(im,0,0);return {key:k,w:c.width,h:c.height,png:c.toDataURL('image/png'),source:XART._src[k]||BOFX.cells?.[k]||BOFX.ships?.[k]};}''',key)
   (S/(name+'.png')).write_bytes(base64.b64decode(out.pop('png').split(',')[1]));(S/(name+'.json')).write_text(json.dumps(out,indent=2));print(name,out)
  b.close()
finally:stop()
