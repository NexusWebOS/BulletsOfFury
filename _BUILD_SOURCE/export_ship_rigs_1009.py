"""Export original canvas dimensions and authored ink bounds, never guess rigs."""
from pathlib import Path
import sys,json,base64,io,argparse
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/smooth_motion_1009/reference';records={}
args=argparse.ArgumentParser();args.add_argument('--refresh-reference',action='store_true');opts=args.parse_args()
if (OUT/'ship-rigs.json').exists() and not opts.refresh_reference:
 sys.exit('Original ship reference rigs already exist. Use --refresh-reference only when intentionally replacing the source baseline.')
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page();p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>{if(typeof SM10!=="undefined"){XART.get=SM10.base.get;furyShipCanvas=SM10.base.fury;}}')
  for pk in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
   p.evaluate('(pk)=>XART.rdy("ship_"+pk)',pk);p.wait_for_function('(pk)=>XART.rdy("ship_"+pk)',arg=pk)
   data=p.evaluate('(pk)=>{const im=XART.get("ship_"+pk),c=document.createElement("canvas");c.width=im.width;c.height=im.height;c.getContext("2d").drawImage(im,0,0);return {w:im.width,h:im.height,data:c.toDataURL().split(",")[1],thr:SHIP_THR[pk].nf};}',pk)
   im=Image.open(io.BytesIO(base64.b64decode(data.pop('data')))).convert('RGBA');data['ink']=im.getchannel('A').point(lambda a:255 if a>160 else 0).getbbox();im.save(OUT/('native_pilot_'+pk+'.png'));records[pk]=data
  p.evaluate('furyShipWarm()');p.wait_for_function('furyShipReady()');data=p.evaluate('()=>{const im=furyShipCanvas("base","axel"),c=document.createElement("canvas");c.width=im.width;c.height=im.height;c.getContext("2d").drawImage(im,0,0);return {w:im.width,h:im.height,data:c.toDataURL().split(",")[1]};}')
  im=Image.open(io.BytesIO(base64.b64decode(data.pop('data')))).convert('RGBA');data['ink']=im.getchannel('A').point(lambda a:255 if a>160 else 0).getbbox();im.save(OUT/'native_furyship.png');records['furyship']=data;br.close()
finally:stop()
(OUT/'ship-rigs.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');print(records)
