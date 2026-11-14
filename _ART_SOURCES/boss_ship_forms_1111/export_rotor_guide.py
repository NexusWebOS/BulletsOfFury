from pathlib import Path
import sys,json,base64
from PIL import Image,ImageDraw
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;V=W/'references';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
errors=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss')
  p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()&&c31Warm()}',arg=5,timeout=180000)
  for i in range(8):
   data=p.evaluate("i=>{const im=XART.get('c31_rotor_'+i),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png')}",i);(V/f'canonical-rotor-{i}.png').write_bytes(base64.b64decode(data.split(',')[1]))
  br.close()
finally:stop()
out=Image.new('RGBA',(832,832));d=ImageDraw.Draw(out)
for i in range(8):out.alpha_composite(Image.open(V/f'canonical-rotor-{i}.png').convert('RGBA').resize((208,416),Image.Resampling.NEAREST),(i%4*208,i//4*416))
out.save(V/'canonical-rotor-phases.png');(V/'rotor-export.json').write_text(json.dumps(dict(source='Actual native C31 rotor views0..7',errors=errors),indent=2));assert not errors,errors;print('Exported exact five-bore native rotor phase guide.',flush=True)
