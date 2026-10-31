"""Offline authoring only: reuse the actual level-4 white cannon and native optic mask.
No runtime rotation, stretching, filtering or generated geometry is required.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance,ImageDraw
import math,json,subprocess,hashlib,shutil
BASE=Path(__file__).parent;R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'assets/game/levels/stage_09/miniboss/horizon_white_optics_1031' if BASE.name=='_BUILD_SOURCE'else BASE
D=W if BASE.name=='_BUILD_SOURCE'else W/'art';D.mkdir(exist_ok=True)
REL='assets/game/levels/stage_09/miniboss/horizon_white_optics_1031'
manifest={}
def bank(name,frames,pivot,cols=32):
 cw,ch=frames[0].size;assert cw%2==ch%2==0
 sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(frames)/cols)))
 for i,f in enumerate(frames):assert f.size==(cw,ch);sheet.alpha_composite(f,((i%cols)*cw,(i//cols)*ch))
 sheet.save(D/(name+'.png'))
 manifest[name]=dict(key='eh91_'+name,path=REL+'/'+name+'.png',cw=cw,ch=ch,cols=cols,frames=len(frames),pivot=pivot)
src=Image.open(W/'inputs/laser_4_pulse_long.png').convert('RGBA')
# Take the intact middle cross-section of the actual white cannon pulse. Its
# centre is continuous; export square, fixed-pivot direction frames offline.
cross=src.crop((0,src.height//2,src.width,src.height//2+1)).rotate(90,expand=True)
base=Image.new('RGBA',(64,64));strip=cross.resize((32,src.width),Image.Resampling.NEAREST);base.alpha_composite(strip,(16,32-src.width//2))
frames=[]
for direction in range(64):
 for phase in range(16):
  f=base.copy();# Subtle travelling highlights retain the original white palette.
  for x in range(16,48):
   if (x-phase*2)%24<2:
    for y in range(28,36):
     r,g,b,a=f.getpixel((x,y))
     if a:f.putpixel((x,y),(min(255,r+12),min(255,g+10),min(255,b+6),a))
  frames.append(f.rotate(-direction*360/64,Image.Resampling.NEAREST,center=(32,32)))
bank('beam',frames,[32,32])
old=json.loads((R/'assets/game/levels/stage_09/miniboss/horizon_symbiote_1029/manifest.json').read_text())
a=old['eye_glow'];sheet=Image.open(R/a['path']).convert('RGBA');frames=[]
for i in range(a['frames']):
 cell=sheet.crop(((i%a['cols'])*80,(i//a['cols'])*80,(i%a['cols']+1)*80,(i//a['cols']+1)*80))
 pix=cell.load()
 for y in range(80):
  for x in range(80):
   r,g,b,al=pix[x,y]
   if al:
    l=max(r,g,b);pix[x,y]=(max(0,l-6),max(0,l-3),l,al)
 frames.append(cell)
bank('eye_glow',frames,[40,40],16)
frames=[]
for i in range(8):
 src=Image.open(W/f'inputs/white_muzzle_{i}.png').convert('RGBA')
 f=Image.new('RGBA',(80,80));f.alpha_composite(src.resize((64,64),Image.Resampling.NEAREST),(8,8));frames.append(f)
bank('muzzle',frames,[40,40],8)
(D/'manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'provenance.json').write_text(json.dumps(dict(beam='spaceLaserPulseCanvas(laser_4_pulse_long), intact centre cross section',muzzle='roundLaserMuzzleArt(#f5f7ff, 0..7), uniform 0.5 scale',core='Original EH57 optical mask, per-pose 32 x 8, white palette',render='Fixed native frame blits only',inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in(W/'inputs').glob('*.png')}),indent=2))
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local banks=json.decode(f:read('*a'));f:close()
for name,a in pairs(banks)do local im=Image{fromFile=D..'/'..name..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB);s.layers[1].name='Authored level-4 white cannon / '..name
for n=0,a.frames-1 do if n>0 then s:newEmptyFrame()end;local cell=Image(im,Rectangle(n%a.cols*a.cw,math.floor(n/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],n+1,cell,Point(0,0));s.frames[n+1].duration=1/30 end
local slice=s:newSlice(Rectangle(0,0,a.cw,a.ch));slice.name='optical-pivot';slice.pivot=Point(a.pivot[1],a.pivot[2]);s:saveAs(D..'/'..name..'.aseprite');s:close()end
"""
(D/'author.lua').write_text(lua)
subprocess.run([r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe','--batch','--script-param','out='+str(D),'--script',str(D/'author.lua')],check=True)
# Inspection plate: the exact native pixels plus a readable enlarged copy.
p=Image.new('RGBA',(768,384),(7,12,20,255));draw=ImageDraw.Draw(p)
for i in range(8):
 for j,name in enumerate(['eye_glow','muzzle','beam']):
  a=manifest[name];n=i*32 if name=='eye_glow'else i if name=='muzzle'else i*128
  sh=Image.open(D/(name+'.png'));c=sh.crop(((n%a['cols'])*a['cw'],(n//a['cols'])*a['ch'],(n%a['cols']+1)*a['cw'],(n//a['cols']+1)*a['ch']))
  p.alpha_composite(c,(i*96+8,j*112+20))
draw.text((10,354),'WHITE CORE / LEVEL-4 MUZZLE / ROTATING WHITE CANNON SHAFT',fill='white');p.save(W/'authored-optics.png')
print(json.dumps({k:{x:a[x]for x in['cw','ch','frames','pivot']}for k,a in manifest.items()}))
