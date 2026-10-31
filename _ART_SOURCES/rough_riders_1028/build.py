from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw,ImageFont
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;REF=W/'references';GEN=W/'generated'
O=R/'assets/game/levels/stage_06/boss/rough_riders_1028';O.mkdir(exist_ok=True,parents=True);S=R/'_ART_SOURCES/rough_riders_1028';S.mkdir(exist_ok=True,parents=True)
KEYS=['voss','nyx','rook','kaia','jace'];CHARS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?:;'\"-+()0123456789/%*=_$";assert len(CHARS)==80
banks={};sources={};fontGlyphs={};models={}
def save(name,im,**meta):
 p=O/(name+'.png');im.save(p);banks[name]=dict(key='rr33_'+name,path=p.relative_to(R).as_posix(),w=im.width,h=im.height,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),**meta)
def original(name,p):
 sources[name]=dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def ramp(im,color):
 a=np.array(im.convert('RGBA'));c=a[:,:,:3].astype(float);hi=c.max(2);lo=c.min(2);mask=(a[:,:,3]>0)&(hi-lo>25);peak=np.maximum(hi,1);sat=(hi-lo)/peak;col=np.array(color)/max(color)
 target=lo[:,:,None]+(hi-lo)[:,:,None]*col;a[:,:,:3]=np.where(mask[:,:,None],np.clip(target,0,255),c).astype('uint8');return Image.fromarray(a)
photo=Image.open(GEN/'crew-photo.png').convert('RGBA');save('crew_photo',photo,cw=1536,ch=1024,cols=1,frames=1,pivot=[768,512]);original('generated-group-photo',GEN/'crew-photo.png')
brand=Image.open(GEN/'brand-sheet.png').convert('RGBA');original('generated-brand-sheet',GEN/'brand-sheet.png')
rects={'wordmark':[0,180,970,465],'badge':[972,0,1536,554],'airspace_sign':[0,620,880,928],'crew_stamp':[880,550,1536,1024]}
for name,rect in rects.items():
 im=brand.crop(rect);a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0).astype('uint8');im=Image.fromarray(a);box=im.getbbox();assert box;im=im.crop(box);w=(im.width+17)//2*2;h=(im.height+17)//2*2;out=Image.new('RGBA',(w,h));out.alpha_composite(im,(8,8));save(name,out,cw=w,ch=h,cols=1,frames=1,pivot=[w//2,h//2],sourceRect=rect)
 # Fixed native-size versions for optional in-game signage/headers.
 target=384 if name in ['wordmark','airspace_sign']else 96 if name=='badge'else 256
 nw=target;nh=math.ceil(out.height*target/out.width/2)*2;small=out.resize((nw,nh),Image.Resampling.NEAREST);save(name+'_native',small,cw=nw,ch=nh,cols=1,frames=1,pivot=[nw//2,nh//2])
# Font source is an 8x10 bitmap, not the older documentation's 10x8 claim.
# Normalize horizontal bearing ONLY. Preserve each original baseline/vertical
# position, and include a four-pixel safety margin for the outlines.
src=Image.open(W/'font/source.png').convert('RGBA');assert src.size==(192,240);original('pixellab-font',W/'font/source.png')
colors={'chrome':[(242,249,254),(175,205,224),(84,107,130),(198,38,49)],'crimson':[(255,225,202),(255,106,73),(167,30,53),(78,22,37)],'signal':[(213,255,248),(77,225,209),(28,126,142),(26,64,84)]}
for variant,cols in colors.items():
 atlas=Image.new('RGBA',(320,256))
 for i,ch in enumerate(CHARS):
  cell=src.crop((i%8*24,i//8*24,i%8*24+24,i//8*24+24));bbox=cell.getbbox();assert bbox,ch;mask=cell.getchannel('A');ink=Image.new('L',(32,32));ink.paste(mask, (4-bbox[0],4));outline=ink.filter(ImageFilter.MaxFilter(5));out=Image.new('RGBA',(32,32),(0,0,0,0));dark=Image.new('RGBA',(32,32),(8,12,20,255));out.paste(dark,(0,0),outline)
  fill=Image.new('RGBA',(32,32));pix=fill.load()
  for y in range(32):
   c=cols[0]if y<11 else cols[1]if y<18 else cols[2]if y<23 else cols[3]
   for x in range(32):pix[x,y]=(*c,255)
  out.paste(fill,(0,0),ink);atlas.alpha_composite(out,(i%10*32,i//10*32));fontGlyphs[ch]=dict(frame=i,advance=bbox[2]-bbox[0]+6,ink=[4,bbox[1]+4,bbox[2]-bbox[0],bbox[3]-bbox[1]],baseline=28)
 save('font_'+variant,atlas,cw=32,ch=32,cols=10,frames=80,pivot=[0,0],baseline=28)
fontGlyphs[' ']=dict(frame=-1,advance=12,baseline=28)
(O/'RoughRidersIgnition.ttf').write_bytes((W/'font/RoughRidersIgnition.ttf').read_bytes())
def label(text,variant='chrome'):
 im=Image.open(O/('font_'+variant+'.png'));w=sum(fontGlyphs[c]['advance']for c in text)+4;canvas=Image.new('RGBA',((w+1)//2*2,36));x=0
 for c in text:
  a=fontGlyphs[c];i=a['frame']
  if i>=0:canvas.alpha_composite(im.crop((i%10*32,i//10*32,i%10*32+32,i//10*32+32)),(x,2))
  x+=a['advance']
 return canvas
for variant in colors:save('font_sample_'+variant,label('THE ROUGH RIDERS  R5 50/50',variant))
# Whole native craft and existing true pitch banks. No new runtime transforms.
meta=json.loads((REF/'manifest.json').read_text());nw=json.JSONDecoder().raw_decode((R/'assets/nightwing_wind_art_1028.js').read_text(encoding='utf-8').split('=',1)[1])[0]
boostMeta=nw['banks']['exhaust_boost'];plumes=Image.open(R/boostMeta['path']).convert('RGBA');sources['native-generated-boost']=dict(path=boostMeta['path'],sha256=hashlib.sha256((R/boostMeta['path']).read_bytes()).hexdigest())
engines={'voss':[[-13,-30],[-6,-30],[6,-30],[13,-30]],'nyx':[[-12,-30],[12,-30]],'rook':[[-12,-28],[12,-28]],'kaia':[[-9,-30],[9,-30]],'jace':[[-8,-30],[8,-30]]}
flameColors={'voss':[255,80,30],'nyx':[190,90,255],'rook':[255,150,45],'kaia':[50,245,220],'jace':[255,90,40]}
contact=Image.new('RGBA',(16*192,5*192),(10,18,28,255))
for row,key in enumerate(KEYS):
 base=Image.open(REF/(key+'-south.png')).convert('RGBA').crop((32,32,224,224));original(key+'-native-render',REF/(key+'-south.png'));frames=[];bounds=[]
 for d in range(32):frames.append(base.rotate(90-d*360/32,Image.Resampling.NEAREST))
 B=next(m for m in meta if m.get('pilot')==key and m.get('bank')=='somer');unit=90*B['ratio']/B['span'];size=round(128*unit/2)*2
 for f in range(16):
  im=Image.open(REF/(key+'-somer')/f'{f:02d}.png').convert('RGBA').resize((size,size),Image.Resampling.NEAREST);c=Image.new('RGBA',(192,192));c.alpha_composite(im,((192-size)//2,(192-size)//2));frames.append(c)
 for kind,north,small in [('cruise_s',False,True),('cruise_n',True,True),('boost_n',True,False)]:
  for f in range(8):
   c=Image.new('RGBA',(192,192));i=(16 if north else 0)*8+f;plume=plumes.crop((i%16*192,i//16*192,i%16*192+192,i//16*192+192));pSize=40 if small else 76;plume=ramp(plume,flameColors[key]).resize((pSize,pSize),Image.Resampling.NEAREST)
   for ex,ey in engines[key]:
    if north:ex,ey=-ex,-ey
    c.alpha_composite(plume,(round(96+ex-pSize/2),round(96+ey-pSize/2)))
   c.alpha_composite(base.rotate(180,Image.Resampling.NEAREST)if north else base);frames.append(c)
 assert len(frames)==72
 sheet=Image.new('RGBA',(16*192,5*192));folder=S/(key+'_frames');folder.mkdir(exist_ok=True)
 for i,im in enumerate(frames):
  sheet.alpha_composite(im,((i%16)*192,(i//16)*192));bounds.append(im.getbbox());im.save(folder/f'{i:02d}.png')
  a=np.array(im)[:,:,3];assert not a[0].any()and not a[-1].any()and not a[:,0].any()and not a[:,-1].any(),(key,i)
 save('flight_'+key,sheet,cw=192,ch=192,cols=16,frames=72,pivot=[96,96],headings=[0,32],somer=[32,16],cruise_s=[48,8],cruise_n=[56,8],boost_n=[64,8]);models[key]=dict(bank='flight_'+key,engines=engines[key],bounds=bounds,sourceUnit=unit)
 for j,i in enumerate([24,64,32,34,36,38,40,42,44,46,48,0,4,8,12,16]):contact.alpha_composite(frames[i],(j*192,row*192))
contact.save(S/'flight-contact.png')
art=dict(banks=banks,font=dict(chars=CHARS,glyphs=fontGlyphs,lineHeight=32),models=models)
(O/'manifest.json').write_text(json.dumps(dict(**art,sources=sources,crewName='The Rough Riders',members=KEYS),indent=2),encoding='utf-8');(R/'assets/rough_riders_art_1028.js').write_text('"use strict";\nconst RR33_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8');(S/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf-8');print('Built',len(banks),'banks, 360 whole flight cells, 80 glyphs x3 palettes')

# Preserve the October30 approved true-roll extension after rebuilding the original72 cells.
import subprocess,shutil
roll_builder=R/'_BUILD_SOURCE/build_riders_roll_type_1030.py'
aseprite=shutil.which('aseprite')or str(Path(r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'))
if roll_builder.exists():subprocess.run([__import__('sys').executable,str(roll_builder),'--aseprite',aseprite],check=True)
