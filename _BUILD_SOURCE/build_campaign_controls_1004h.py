"""Import authored save-slot cartridge and derive luminance-preserving accents."""
from pathlib import Path
from PIL import Image, ImageFilter
import json,hashlib,shutil,colorsys
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/campaign_controls_1004h';O=R/'assets/game/campaign_controls_1004h'
A.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
src=A/'slot_source.png'
if not src.exists():shutil.copy2(Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-f6caf1f8-2156-4aac-b7ad-77e65317f4b8.png'),src)
im=Image.open(src).convert('RGBA');assert im.getchannel('A').getextrema()[0]==0
bb=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();im=im.crop(bb);im.thumbnail((1086,256),Image.Resampling.NEAREST)
for color in ['red','white','blue']:
 out=im.copy();px=out.load()
 for y in range(out.height):
  for x in range(out.width):
   r,g,b,a=px[x,y];h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
   if a and s>.35 and (h<.075 or h>.94):
    if color=='blue':r,g,b=[round(c*255) for c in colorsys.hsv_to_rgb(.60,s,v)]
    elif color=='white':r=g=b=round(v*255)
    px[x,y]=(r,g,b,a)
 out.save(O/('slot_'+color+'.png'))
 glow=Image.new('RGBA',out.size,(235,244,255));glow.putalpha(out.getchannel('A').filter(ImageFilter.MaxFilter(5)))
 glow.alpha_composite(out);glow.save(O/('slot_'+color+'_hi.png'))
flash=Image.new('RGBA',im.size,(255,255,255));flash.putalpha(im.getchannel('A'));flash.save(O/'slot_flash.png')
m={'generator':'OpenAI built-in imagegen','sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source':src.name,'size':im.size,'crop':bb,'prompt':json.loads((A/'prompt.json').read_text()),'normalization':'Original RGBA alpha; nearest crop/contain. Only saturated red accents swapped to blue/white; metal and inner screen retained.'}
for d in [A,O]:(d/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text())
d['map4h_slot_']={'role':'campaign_save_slot','sheet':None,'note':'Generated blank chrome cartridges; red/white/blue accent variants preserve metal, dark screens and alpha. Source/prompt campaign_controls_1004h; builder build_campaign_controls_1004h.py.'}
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('Generated cartridge art imported with original source and prompt.')
