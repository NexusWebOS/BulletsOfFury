from pathlib import Path
from PIL import Image,ImageOps
from collections import deque
import json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';S=R/'_ART_SOURCES/city_rescue_1115';A=R/'assets/game/shared/cinematics/city_rescue_1115'
S.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
sources={'pursuit-furious':'exec-61728f7e-5fef-4269-83c8-43414a8ef2b4.png','pursuit-hard':'exec-9e0eb160-19ed-491d-819d-9dd50ce21d8a.png','rural':'exec-0718605e-050e-458d-8a6d-37c362f64600.png','thruster':'exec-af00853b-8724-45e4-a0fd-83363a5bcbfd.png','album':'exec-709a039d-aec6-480e-bb9f-81a83c72df12.png'}
M={'version':1,'images':{},'banks':{},'sockets':[[172,93],[236,66],[340,66],[404,93]],'sources':sources}
def reg(name,im):
 assert im.width%2==im.height%2==0
 path=(R/'assets/game/shared/cinematics/cockpit_castB_1115/album.png')if name=='album'and(R/'_ART_SOURCES/cockpit_castB_1115/album.png').exists()else A/(name+'.png');path.parent.mkdir(parents=True,exist_ok=True);im.save(path);M['images'][name]={'key':'city16_'+name,'path':str(path.relative_to(R)).replace('\\','/'),'w':im.width,'h':im.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def contain(im,size):
 k=min(size[0]/im.width,size[1]/im.height);p=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',size,(0,0,0,255));c.alpha_composite(p,((size[0]-p.width)//2,(size[1]-p.height)//2));return c
assert all((S/('generated-'+n+'.png')).is_file()for n in sources), 'Retained generated masters are required'
for n in ['pursuit-furious','pursuit-hard']:reg(n,contain(Image.open(S/('generated-'+n+'.png')).convert('RGBA'),(912,512)))
albumMaster=R/'_ART_SOURCES/cockpit_castB_1115/album.png'
reg('album',contain(Image.open(albumMaster if albumMaster.exists()else S/'generated-album.png').convert('RGBA'),(912,512)))
if albumMaster.exists():M['images']['album']['family']='castB-1115'
im=Image.open(S/'generated-rural.png').convert('RGBA');im=im.resize((680,1020),Image.Resampling.NEAREST)
tile=Image.new('RGBA',(680,2040));tile.alpha_composite(im);tile.alpha_composite(ImageOps.flip(im),(0,1020));reg('rural',tile)
reg('shade',Image.new('RGBA',(480,512),(0,3,12,168)))
raw=Image.open(S/'generated-thruster.png').convert('RGBA');cells=[];registration=[]
for i in range(16):
 x0=round(i%4*raw.width/4);x1=round((i%4+1)*raw.width/4);y0=round(i//4*raw.height/4);y1=round((i//4+1)*raw.height/4)
 p=raw.crop((x0,y0,x1,y1));data=list(p.getdata());ww,hh=p.size
 # Discard low-alpha generator haze and detached dust; retain the connected
 # plume containing its white core. This is cleanup, not invented animation.
 good=bytearray(1 if a>=160 else 0 for r,g,b,a in data);seen=bytearray(ww*hh);best=[];bestScore=0
 for start in range(ww*hh):
  if not good[start]or seen[start]:continue
  stack=[start];seen[start]=1;component=[];score=0
  while stack:
   at=stack.pop();component.append(at);r,g,b,a=data[at];score+=int(r>160 and g>190 and b>200)
   xx=at%ww;yy=at//ww
   for k in ([at-1]if xx else[])+([at+1]if xx+1<ww else[])+([at-ww]if yy else[])+([at+ww]if yy+1<hh else[]):
    if good[k]and not seen[k]:seen[k]=1;stack.append(k)
  if score>bestScore:bestScore=score;best=component
 keep=set(best);clean=Image.new('RGBA',p.size);clean.putdata([(r,g,b,255)if j in keep else(0,0,0,0)for j,(r,g,b,a)in enumerate(data)])
 bright=[(j%ww,j//ww)for j in best if data[j][0]>160 and data[j][1]>190 and data[j][2]>200];bottom=max(y for x,y in bright);mouth=[x for x,y in bright if y>=bottom-5];cx=sum(mouth)/len(mouth)
 # One fixed 1/2 scale for all cells; only physical mouth registration changes.
 canvas=Image.new('RGBA',(224,444));canvas.alpha_composite(clean);small=canvas.resize((112,222),Image.Resampling.NEAREST);c=Image.new('RGBA',(128,256));dx=64-round(cx*.5);dy=224-round(bottom*.5);c.alpha_composite(small,(dx,dy));cells.append(c);registration.append({'sourceRect':[x0,y0,x1-x0,y1-y0],'sourceMouth':[cx,bottom],'scale':.5,'translation':[dx,dy],'pivot':[64,224]})
 # Retain uncooked normalized cells as editable lossless source.
 c.save(S/('thruster-normalized-%02d.png'%i))
palette=Image.new('RGB',(128*16,256),(0,0,0))
for i,c in enumerate(cells):palette.paste(c.convert('RGB'),(128*i,0))
palette=palette.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
for i,c in enumerate(cells):
 rgb=c.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(c.getchannel('A'));cells[i]=rgb;rgb.save(S/('thruster-%02d.png'%i))
sheet=Image.new('RGBA',(512,1024))
for i,c in enumerate(cells):sheet.alpha_composite(c,(i%4*128,i//4*256))
reg('thruster-source',sheet);M['thrusterRegistration']=registration;M['thrusterTimingMs']=[62,63]*8
cells[0].save(O/'thruster.gif',save_all=True,append_images=cells[1:],duration=M['thrusterTimingMs'],loop=0,disposal=2)
def bank(name,frames,pivot,bodyWidth=None):
 w,h=frames[0].size;assert w%2==h%2==0 and all(p.size==(w,h)for p in frames)
 B={'w':w,'h':h,'pivot':pivot,'frames':len(frames),'pages':[],'cells':[]}
 if bodyWidth:B['bodyWidth']=bodyWidth
 per=64 if w<=128 else 16
 for start in range(0,len(frames),per):
  chunk=frames[start:start+per];cols=min(8 if per==64 else 4,len(chunk));out=Image.new('RGBA',(cols*w,math.ceil(len(chunk)/cols)*h));key='city16_'+name+'_'+str(start//per)
  for j,p in enumerate(chunk):out.alpha_composite(p,((j%cols)*w,(j//cols)*h));B['cells'].append([key,(j%cols)*w,(j//cols)*h])
  path=A/(name+'-'+str(start//per)+'.webp');out.save(path,lossless=True);B['pages'].append({'key':key,'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'w':out.width,'h':out.height})
 M['banks'][name]=B
# Directly export every actual TC119 depth and heading from the same normalized
# master. Fixed even canvases and one nozzle pivot per bank; no runtime rotation.
for di,scale in enumerate([1,.96,.92,.88,.84,.8,.76,.72,.68,.64,.6,.56,.52,.48,.44,.4]):
 size=math.ceil(448*.46*scale/2)*2;pivot=[size//2,size//2];page=Image.new('RGBA',(2048,2048));px=py=rowH=0;key='city16_thrusters_d'+str(di);names=[]
 for d in range(16):
  frames=[]
  for c in cells:
   c=c.resize((round(128*.46*scale),round(256*.46*scale)),Image.Resampling.NEAREST);base=Image.new('RGBA',(size,size));base.alpha_composite(c,(pivot[0]-round(64*.46*scale),pivot[1]-round(224*.46*scale)))
   # Direction0 is the south-facing ship: its rear flame points north.
   frames.append(base.rotate(-d*22.5,resample=Image.Resampling.NEAREST,center=tuple(pivot)))
  bounds=[c.getbbox()for c in frames];left=min(b[0]for b in bounds)//2*2;top=min(b[1]for b in bounds)//2*2;right=math.ceil(max(b[2]for b in bounds)/2)*2;bottom=math.ceil(max(b[3]for b in bounds)/2)*2;crop=[left,top,right,bottom];cw=right-left;ch=bottom-top
  if px+cw*4>2048:px=0;py+=rowH;rowH=0
  assert py+ch*4<=2048
  name='thrust-d'+str(di)+'-r'+str(d);B={'w':cw,'h':ch,'pivot':[pivot[0]-left,pivot[1]-top],'frames':16,'sourceCell':[size,size],'sharedCrop':crop,'sourcePivot':pivot,'depthScale':scale,'pages':[],'cells':[]}
  for j,c in enumerate(frames):
   x=px+j%4*cw;y=py+j//4*ch;page.alpha_composite(c.crop(crop),(x,y));B['cells'].append([key,x,y])
  M['banks'][name]=B;names.append(name);px+=cw*4;rowH=max(rowH,ch*4)
 bbox=page.getbbox();pw=math.ceil(bbox[2]/2)*2;ph=math.ceil(bbox[3]/2)*2;page=page.crop((0,0,pw,ph));path=A/('thrusters-d'+str(di)+'.webp');page.save(path,lossless=True)
 pageMeta={'key':key,'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'w':pw,'h':ph}
 for name in names:M['banks'][name]['pages']=[pageMeta]
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n')
(R/'assets/city_rescue_art_1115.js').write_text('"use strict";\nconst CITY16_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
print(json.dumps({'images':list(M['images']),'banks':len(M['banks']),'frames':sum(b['frames']for b in M['banks'].values()),'registration':registration}),flush=True)
