"""Author fixed-size Thunderhead storm frames from approved BOF source art.
No runtime palette, opacity, scale or rotation animation is needed by this pack.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json, math, hashlib, random, shutil
import numpy as np

W=Path(__file__).resolve().parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O=W/'authored';O.mkdir(exist_ok=True)
F=O/'frames';F.mkdir(exist_ok=True)
P=R/'assets/game/levels/stage_06/boss/thunderhead_storm_1104';P.mkdir(parents=True,exist_ok=True)
text=(R/'assets/furious_encounters_art_1102.js').read_text()
old=json.loads(text[text.index('{'):text.rindex('}')+1])
M={'version':'1104','banks':{},'sources':{},'contract':{'owner':'Stage6 Furious Thunderhead only','blend':'source-over','fixedSize':True,'pivot':'cell centre','clock':'simulation seconds','cleanup':'owner death/cancel/stage exit','maxStormObjects':12}}
def oldframes(name):
 b=old['banks'][name];im=Image.open(R/b['path']).convert('RGBA');s=b['cell']
 return [im.crop((i%b['cols']*s,i//b['cols']*s,i%b['cols']*s+s,i//b['cols']*s+s))for i in range(b['frames'])]
def fade(im,a):
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda p:round(p*min(1,max(0,a)))));return im
def center(im,size,scale=1,angle=0):
 if angle:im=im.rotate(angle,resample=Image.Resampling.NEAREST,expand=True)
 if scale!=1:im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.NEAREST)
 out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out
def light(im,power=.4):
 a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb.max(2)
 rgb[:,:,0]=np.minimum(255,rgb[:,:,0]+lum*power*.5);rgb[:,:,1]=np.minimum(255,rgb[:,:,1]+lum*power*.3);rgb[:,:,2]=np.minimum(255,rgb[:,:,2]+lum*power*.3)
 a[:,:,:3]=rgb.astype('uint8');return Image.fromarray(a)
def bank(name,frames,fps=16,notes=''):
 cw,ch=frames[0].size;cols=max(1,min(len(frames),1536//cw));rows=(len(frames)+cols-1)//cols
 # Every page is bounded; metadata contains explicit per-frame source rectangles.
 cells=[];pages=[]
 per=cols*max(1,1536//ch)
 for start in range(0,len(frames),per):
  part=frames[start:start+per];h=math.ceil(len(part)/cols)*ch;sheet=Image.new('RGBA',(cols*cw,h));key='ths114_'+name+'_'+str(start//per)
  for j,im in enumerate(part):
   sheet.alpha_composite(im,(j%cols*cw,j//cols*ch));cells.append([key,j%cols*cw,j//cols*ch])
  path=P/(name+'_'+str(start//per)+'.png');sheet.save(path,optimize=True)
  pages.append({'key':key,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':sheet.size})
 src=F/name;src.mkdir(exist_ok=True)
 for i,im in enumerate(frames):im.save(src/(str(i).zfill(3)+'.png'))
 M['banks'][name]={'cw':cw,'ch':ch,'frames':len(frames),'fps':fps,'cells':cells,'pages':pages,'notes':notes}
 return frames

tw=oldframes('tornado');disc=oldframes('hurricane');burst=oldframes('storm_burst')
# Fixed 112x192 travel cell: 4 materialising, 12 fully formed, 4 dispersing.
tornado=[]
bounds=tw[0].getbbox()
for im in tw[1:]:
 b=im.getbbox();bounds=(min(bounds[0],b[0]),min(bounds[1],b[1]),max(bounds[2],b[2]),max(bounds[3],b[3]))
twscale=min(100/(bounds[2]-bounds[0]),180/(bounds[3]-bounds[1]))
for i in range(20):
 grow=[.25,.48,.72,.9][i]if i<4 else [1,.78,.5,.24][i-16]if i>=16 else 1
 im=tw[(i-4)%6].crop(bounds)
 tornado.append(fade(center(im,(112,192),twscale*grow),min(1,grow*1.2)))
bank('tornado',tornado,20,'4 grow /12 loop /4 dissipate; pressure tower socket; hitbox38x100')
cyclone=[]
for i in range(16):
 im=disc[i%4].resize((80,80),Image.Resampling.NEAREST)
 cyclone.append(center(im,(96,96),1,i*22.5))
bank('cyclone',cyclone,24,'Core-born electric wind disc; 42px contact diameter')
# Giant discharge is a cloud/wind front, not a laser or a screen-sized opaque flash.
giant=[]
for i in range(24):
 out=Image.new('RGBA',(304,304));d=disc[i%4].resize((288,288),Image.Resampling.NEAREST)
 out.alpha_composite(center(d,out.size,1,i*15))
 heart=burst[i%4].resize((192,192),Image.Resampling.NEAREST);out.alpha_composite(fade(heart,.85),(56,56))
 giant.append(out)
bank('tempest',giant,24,'Giant core storm front; 180x180 contact; two camera-safe flank corridors')
bank('muzzle',[center(light(x,.25),(144,144),144/256)for x in burst],24,'Core discharge socket; no gameplay damage')
bank('impact',[fade(center(burst[i%4],(144,144),(.16+min(i,7)*.05)),min(1,(14-i)/5))for i in range(14)],24,'Ground lightning impact;44x22px danger ellipse for first0.22s; full authored fringe retained')
retina=Image.open(R/'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030/retina.png').convert('RGBA')
bank('retina',[retina.crop((i%8*64,i//8*32,i%8*64+64,i//8*32+32)).resize((88,44),Image.Resampling.NEAREST)for i in range(24)],16,'Actual authored ground warning;3colours x8frames;44x22px matching contact ellipse')

# Preserve the chromium ribs: the overlay contains only the original cyan glass.
body=oldframes('thunder_body')[0];panel=body.crop((288,292,480,548));raw=np.array(panel);rgb=raw[:,:,:3].astype(float)
mask=(rgb[:,:,1]>rgb[:,:,0]*1.28)&(rgb[:,:,2]>rgb[:,:,0]*1.4)&(raw[:,:,3]>30)
yy,xx=np.mgrid[:256,:192];core=[]
for i in range(32):
 level=i//8;phase=i%8;wave=(np.sin(yy*.16+xx*.04-phase*math.pi/4)+1)/2
 a=np.zeros_like(raw);boost=.1+level*.2;v=np.clip(rgb*(1+boost)+wave[:,:,None]*(15+level*12),0,255)
 a[:,:,:3]=v.astype('uint8');a[:,:,3]=np.where(mask,raw[:,:,3],0)
 im=Image.fromarray(a).resize((140,186),Image.Resampling.NEAREST)
 # Offline soft rim is baked into the PNG and never additive at render time.
 rim=im.filter(ImageFilter.GaussianBlur(2+level));rim=fade(rim,.22+level*.1)
 rim.alpha_composite(im);core.append(rim)
bank('core',core,16,'4 charge levels x8 loop frames; exact native core anchor, chromium ribs excluded')

# Reuse actual BOF lightning, recoloured offline to the core's cyan/white palette.
bolts=[]
for i in range(8):
 im=Image.open(W/'sources'/('c42_bolt_'+str(i)+'.png')).convert('RGBA');a=np.array(im);lum=a[:,:,:3].max(2).astype(float)
 white=(a[:,:,:3].min(2)>160)
 a[:,:,0]=np.where(white,lum,lum*.54).astype('uint8');a[:,:,1]=np.minimum(255,lum*1.04).astype('uint8');a[:,:,2]=np.minimum(255,lum*1.1).astype('uint8')
 bolts.append(Image.fromarray(a).resize((96,512),Image.Resampling.NEAREST))
bank('bolt',bolts,24,'Full-height cyan-white lightning; impact at marked ground point')
orbs=[]
for i in range(16):
 im=Image.open(W/'sources'/('s4w_lightning_ball_'+str(i)+'.png')).convert('RGBA');a=np.array(im);r=a[:,:,0].copy();g=a[:,:,1].copy();a[:,:,1]=np.maximum(g,a[:,:,2]*.82).astype('uint8');a[:,:,0]=np.maximum(r,g*.4).astype('uint8')
 orbs.append(Image.fromarray(a).resize((48,48),Image.Resampling.NEAREST))
bank('orb',orbs,24,'Core lightning hail, unshootable ordinary energy')

# Source-authored cloud layers remain translucent and leave the city readable.
for family,label,size,alpha in [('nl6c_low_rolling_bank_','cloud_far',(288,216),.43),('nl6c_heavy_rain_cloud_','cloud_near',(384,288),.52)]:
 frames=[]
 for i in range(6):
  im=Image.open(W/'sources'/(family+str(i)+'.png')).convert('RGBA').resize(size,Image.Resampling.NEAREST)
  a=np.array(im);a[:,:,:3]=(a[:,:,:3].astype(float)*np.array([.55,.7,.88])).astype('uint8');frames.append(fade(Image.fromarray(a),alpha))
 bank(label,frames,4,'Parallax world-space cloud bank, baked blue storm palette/opacity')
grades=[]
for i in range(7):grades.append(Image.new('RGBA',(340,256),(2,10,28,round(i*22))))
bank('grade',grades,1,'7 authored storm lighting steps; city visible at maximum intensity')
rain=[];random.seed(114)
streaks=[(random.randrange(340),random.randrange(256),random.randrange(4,11),random.randrange(32,95))for _ in range(70)]
for density in range(2):
 for f in range(8):
  im=Image.new('RGBA',(340,256));d=ImageDraw.Draw(im)
  for x,y,n,a in streaks[:35+density*35]:
   x=(x-f*3)%340;y=(y+f*32)%256;d.line((x,y,x-2,y+n),fill=(160,208,238,a),width=1)
  rain.append(im)
bank('rain',rain,24,'Two8frame density loops; visual only; simulation clock')

for src in [W/'sources/export.json',R/'_BUILD_SOURCE/furious_encounters_1102/storm_source.png',R/'_BUILD_SOURCE/furious_encounters_1102/thunderhead_source.png']:
 M['sources'][src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(M,indent=2));(P/'manifest.json').write_text(json.dumps(M,indent=2))
(R/'assets/thunderhead_storm_art_1104.js').write_text('"use strict";\nconst THS114_ART='+json.dumps(M,separators=(',',':'))+';\n')
# Editable Aseprite sources retain every fixed cell and timeline duration.
lua='local root=app.params.root\nlocal banks='+ '{'+','.join('{name="'+name+'",n='+str(b['frames'])+',fps='+str(b['fps'])+'}'for name,b in M['banks'].items())+'}\n'
lua+='for _,b in ipairs(banks)do\nlocal first=Image{fromFile=root.."/frames/"..b.name.."/000.png"}\nlocal s=Sprite(first.width,first.height,ColorMode.RGB);s.layers[1].name=b.name.." / authored fixed cells"\nfor i=0,b.n-1 do if i>0 then s:newEmptyFrame(i+1)end\nlocal im=Image{fromFile=root.."/frames/"..b.name.."/"..string.format("%03d",i)..".png"}\ns:newCel(s.layers[1],i+1,im,Point(0,0));s.frames[i+1].duration=1/b.fps end\ns:saveAs(root.."/"..b.name..".aseprite");s:close()end\n'
(O/'author.lua').write_text(lua)
contact=Image.new('RGB',(1024,768),'#12202e');d=ImageDraw.Draw(contact)
for i,name in enumerate(['core','tornado','cyclone','tempest','bolt','orb','cloud_far','cloud_near']):
 b=M['banks'][name];im=Image.open(F/name/(str(min(8,b['frames']-1)).zfill(3)+'.png'));im.thumbnail((250,330));x=i%4*256;y=i//4*384;contact.paste(im,(x+(256-im.width)//2,y+30),im);d.text((x+8,y+7),name,fill='white')
contact.save(O/'contact.jpg',quality=95)
print('Authored',len(M['banks']),'banks;',sum(b['frames']for b in M['banks'].values()),'frames;',round(sum(p.stat().st_size for p in P.glob('*.png'))/1048576,2),'MB')
