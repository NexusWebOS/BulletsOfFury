from pathlib import Path
import urllib.request,json,hashlib
from PIL import Image,ImageEnhance,ImageOps
import colorsys
W=Path(__file__).resolve().parent
R=W.parent if W.name=='_BUILD_SOURCE'else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
raw=R/'_ART_SOURCES/hq_forge_1023'if W.name=='_BUILD_SOURCE'else W/'raw';raw.mkdir(exist_ok=True)
jobs={'hq':'images/d965b9de-238e-4e49-9be3-abe7c1c2f8b5','forge':'images/b5a6c1ab-23a1-4ed4-b8ee-69130064537b','button':'images/f67623f8-f0c6-484d-9d8d-f42972a9b8d2','menu':'ui-assets/98864ffe-b628-433d-8e1f-b99030702d80'}
out=R/'assets/game/shared/ui/hq_forge_1023';out.mkdir(parents=True,exist_ok=True)
manifest={'owner':'_BUILD_SOURCE/build_hq_forge_1023.py','provider':'PixelLab','jobs':jobs,'assets':{},'fee':300,'pointsPerCompletedStage':2,'claudeReference':'a59a2e0704476aa3bf794bd5c11ff5da0d2192a1'}
def save(im,name):
 p=out/(name+'.webp');im.save(p,lossless=True)
 manifest['assets']['hf23_'+name]={'path':p.relative_to(R).as_posix(),'width':im.width,'height':im.height,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for name,job in jobs.items():
 p=raw/(name+'.png')
 if not p.exists():urllib.request.urlretrieve('https://api.pixellab.ai/mcp/'+job+'/download',p)
 im=Image.open(p).convert('RGBA')
 if name in ('hq','forge'):
  save(im.resize((256,256),Image.Resampling.NEAREST),name)
 elif name=='menu':
  save(im.resize((456,340),Image.Resampling.NEAREST),name)
 else:
  for w,h,tag in [(324,40,'row'),(160,30,'small'),(300,34,'start')]:
   # Offline cap slicing; runtime draws a fixed complete button, without distortion.
   dst=Image.new('RGBA',(w,h));cap=38;right=16;dh=h;dc=round(cap*h/im.height);dr=round(right*h/im.height)
   dst.paste(im.crop((0,0,cap,im.height)).resize((dc,h),Image.Resampling.NEAREST),(0,0))
   dst.paste(im.crop((cap,0,im.width-right,im.height)).resize((w-dc-dr,h),Image.Resampling.NEAREST),(dc,0))
   dst.paste(im.crop((im.width-right,0,im.width,im.height)).resize((dr,h),Image.Resampling.NEAREST),(w-dr,0))
   if tag=='start':
    pixels=[]
    for r,g,b,a in dst.getdata():
     hue,sat,value=colorsys.rgb_to_hsv(r/255,g/255,b/255)
     if sat>.28 and hue<.18:r,g,b=[round(c*255)for c in colorsys.hsv_to_rgb(0,sat,value)]
     pixels.append((r,g,b,a))
    dst.putdata(pixels)
   for state,factor in [('idle',.75),('selected',1.25),('disabled',.38)]:
    alpha=dst.getchannel('A');rgb=ImageEnhance.Brightness(dst.convert('RGB')).enhance(factor);rgb.putalpha(alpha);save(rgb,tag+'_'+state)
source=R/'_ART_SOURCES/hq_forge_1023';source.mkdir(parents=True,exist_ok=True)
# Exact-size workshop plate from BOF's existing avatar-free generated window.
im=Image.open(R/'assets/game/shared/ui/menu_windows_1021/xl.webp').convert('RGBA');dst=Image.new('RGBA',(456,366))
sx=[0,64,im.width-64,im.width];sy=[0,74,im.height-32,im.height];dx=[0,64,392,456];dy=[0,74,334,366]
for row in range(3):
 for col in range(3):dst.paste(im.crop((sx[col],sy[row],sx[col+1],sy[row+1])).resize((dx[col+1]-dx[col],dy[row+1]-dy[row]),Image.Resampling.NEAREST),(dx[col],dy[row]))
save(dst,'workshop')
save(Image.new('RGBA',(480,512),(6,12,22,255)),'backdrop')
for p in raw.glob('*.png'):(source/p.name).write_bytes(p.read_bytes())
(source/'manifest.json').write_text(json.dumps(manifest,indent=2))
(W/'art.json').write_text(json.dumps(manifest,indent=2))
js="'use strict';\nconst HF23_ART="+json.dumps(manifest,separators=(',',':'))+";\nfor(const [k,a] of Object.entries(HF23_ART.assets))XART._src[k]=a.path;\n"
(R/'assets/hq_forge_art_1023.js').write_text(js,encoding='utf-8',newline='\n')
print(json.dumps({'generated':len(manifest['assets']),'sources':str(source)}))
