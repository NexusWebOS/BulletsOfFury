from pathlib import Path
import sys,json,base64,hashlib
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;V=W/'references';V.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
errors=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(5))updatePlay(0);return stageLoadReady(5)&&!bp119Pending()&&c31Warm()}',timeout=180000)
  for k in range(36):
   data=p.evaluate("""k=>{const im=XART.get('c31_rotor_'+k),c=document.createElement('canvas');c.width=104;c.height=208;c.getContext('2d').drawImage(im,0,0);return c.toDataURL()}""",k);(V/f'rotor-{k:02}.png').write_bytes(base64.b64decode(data.split(',')[1]))
  spec=p.evaluate("()=>({cell:ch23Cell('barrel',boss,0),gunSocket:CH23_ART.gunSocket,muzzle:CH23_ART.muzzle,mechanicalPhases:36})");(V/'canonical-gun.json').write_text(json.dumps(spec,indent=2));br.close()
finally:stop()
(W/'export-errors.json').write_text(json.dumps(errors));assert not errors,errors
print('Exported 36 actual canonical rotary phases. New game rendering will select static authored cells.',flush=True)
