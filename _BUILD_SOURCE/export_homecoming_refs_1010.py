"""Current pilot jets and the actual final-fight return gate, through native game ctx."""
from pathlib import Path
import base64, hashlib, json, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/homecoming_1010/references';OUT.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
records=[];errors=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page();p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  keys=['ship_'+pk for pk in PILOTS]+p.evaluate("AP10_CIN_ART.void.filter((a,i)=>[0,7,8,15,23,31].includes(i)).map(a=>a.key)")
  for key in keys:
   p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
   q=p.evaluate('''key=>{const im=XART.get(key),w=im.width||im.naturalWidth,h=im.height||im.naturalHeight,
    old={w:cv.width,h:cv.height};try{cv.width=w;cv.height=h;ctx.setTransform(1,0,0,1,0,0);
     ctx.clearRect(0,0,w,h);ctx.drawImage(im,0,0);return {w,h,png:cv.toDataURL().split(',')[1]};
    }finally{cv.width=old.w;cv.height=old.h;ctx.setTransform(SS,0,0,SS,0,0);}}''',key)
   dest=OUT/(key+'.png');dest.write_bytes(base64.b64decode(q.pop('png')))
   records.append(dict(key=key,**q,path=dest.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),route='XART.get / game ctx.drawImage'))
  br.close()
finally:stop()
sheet=Image.new('RGBA',(864,864),(8,13,22,255));d=ImageDraw.Draw(sheet)
for i,pk in enumerate(PILOTS):
 im=Image.open(OUT/('ship_'+pk+'.png'));x=(i%3)*288+(288-im.width)//2;y=(i//3)*288+24
 sheet.alpha_composite(im,(x,y));d.text(((i%3)*288+14,(i//3)*288+8),pk.upper(),fill='#ffffff')
sheet.convert('RGB').save(OUT/'all_nine_native_jets.png')
(OUT/'native-manifest.json').write_text(json.dumps(dict(records=records,errors=errors),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(exported=len(records),errors=errors)),flush=True)
sys.exit(1 if errors else 0)
