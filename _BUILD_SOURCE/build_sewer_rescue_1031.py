from pathlib import Path
from PIL import Image,ImageEnhance
import json,subprocess,hashlib
BASE=Path(__file__).parent;R=BASE.parent if BASE.name=='_BUILD_SOURCE'else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'assets/game/levels/stage_07/effects/escape_rescue_1031'if BASE.name=='_BUILD_SOURCE'else BASE;D=W if BASE.name=='_BUILD_SOURCE'else W/'art';D.mkdir(parents=True,exist_ok=True);I=W/'inputs';banks={}
def bank(name,frames):
 w,h=frames[0].size;cols=4;im=Image.new('RGBA',(w*cols,h*((len(frames)+cols-1)//cols)))
 for i,f in enumerate(frames):im.alpha_composite(f,(i%cols*w,i//cols*h))
 im.save(D/(name+'.png'));banks[name]=dict(key='sr93_'+name,path='assets/game/levels/stage_07/effects/escape_rescue_1031/'+name+'.png',cw=w,ch=h,cols=cols,frames=len(frames),pivot=[w//2,h//2])
for name,family,size in [('dense','nxp_dense',192),('barrage','nxp_barrage',288),('radial','nxp_radial',288),('engulf','nxp_dense',352)]:
 raw=[Image.open(I/(family+'_'+str(i)+'.png')).convert('RGBA')for i in range(8)];scale=size/max(max(f.size)for f in raw);frames=[]
 for f in raw:
  f=f.resize((round(f.width*scale),round(f.height*scale)),Image.Resampling.NEAREST);out=Image.new('RGBA',(size,size));out.alpha_composite(f,((size-f.width)//2,(size-f.height)//2));frames.append(out)
 bank(name,frames)
raw=[Image.open(I/f'nsd_ring_{i}.png').convert('RGBA')for i in range(8)];scale=1/max(max(im.size)for im in raw);frames=[]
for f in range(24):
 u=f/23;im=raw[min(7,f//3)];s=(120+u*292)*scale;im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.NEAREST);im.putalpha(im.getchannel('A').point(lambda a:round(a*min(1,(1-u)*3))));out=Image.new('RGBA',(448,448));out.alpha_composite(im,((448-im.width)//2,(448-im.height)//2));frames.append(out)
bank('ring',frames)
(D/'manifest.json').write_text(json.dumps(banks,indent=2));(D/'provenance.json').write_text(json.dumps(dict(source='Actual current XART nxp_dense/barrage/radial and nsd_ring; native toxic palette exported offline',inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in I.glob('*.png')}),indent=2))
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local banks=json.decode(f:read('*a'));f:close();for name,a in pairs(banks)do local im=Image{fromFile=D..'/'..name..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB);s.layers[1].name='Actual ColeForge escape / '..name;for n=0,a.frames-1 do if n>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(n%a.cols*a.cw,math.floor(n/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],n+1,c,Point(0,0));s.frames[n+1].duration=name=='ring'and 1/24 or .075 end;local p=s:newSlice(Rectangle(0,0,a.cw,a.ch));p.name='blast-center';p.pivot=Point(a.pivot[1],a.pivot[2]);s:saveAs(D..'/'..name..'.aseprite');s:close()end"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe','--batch','--script-param','out='+str(D),'--script',str(D/'author.lua')],check=True);print('Authored56 native explosion/smoke frames, five Aseprite sources.')
