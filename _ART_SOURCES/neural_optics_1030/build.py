"""NB80: re-author the existing PixelLab optical frames into aperture-filling
warm eye beams. Preserve source16-phase flow and each actual pose's eye pixels.
All palette, fill, expansion and dissipation artwork is exported offline.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,numpy as np,hashlib
from scipy.ndimage import binary_dilation
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_shots/neural_optics_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(exist_ok=True,parents=True)
O=R/'assets/game/levels/stage_08/boss/neural_optics_1030';D=R/'_ART_SOURCES/neural_optics_1030';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
s=(R/'assets/dracodia_brain_art_1023.js').read_text();N=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
A={'banks':{},'pages':{},'widths':[32,34,36,38,40,42],'beamLength':600,'source':'Original approved16-phase PixelLab laser and exact current brain/charge/focus poses; no new credit spent.','logicalBeam':[80,624],'beamPivot':[40,12]};sources={};page=Image.new('RGBA',(1024,1024));px=py=rh=pi=0
def flush():
 global page,px,py,rh,pi
 key='nb80_page_'+str(pi);h=max(2,min(1024,(py+rh+3)//2*2));im=page.crop((0,0,1024,h));p=O/(key+'.webp');im.save(p,lossless=True,method=6);A['pages'][key]={'path':p.relative_to(R).as_posix(),'w':1024,'h':h};pi+=1;page=Image.new('RGBA',(1024,1024));px=py=rh=0
def emit(bank,im,pivot,extra=None):
 global px,py,rh
 assert im.width%2==im.height%2==0
 b=im.getbbox()
 if b:x0=b[0]//2*2;y0=b[1]//2*2;x1=(b[2]+1)//2*2;y1=(b[3]+1)//2*2
 else:x0=y0=0;x1=y1=2
 crop=im.crop((x0,y0,x1,y1));w,h=crop.size
 if px+w+2>1024:px=0;py+=rh+2;rh=0
 if py+h+2>1024:flush()
 page.paste(crop,(px,py));mask=np.array(crop)[:,:,3]>48;spans=[np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1)))).tolist()for row in mask]
 a={'key':'nb80_page_'+str(pi),'rect':[px,py,w,h],'offset':[x0-pivot[0],y0-pivot[1]],'w':w,'h':h,'spans':spans,'logical':[im.width,im.height]}
 if extra:a.update(extra)
 A['banks'].setdefault(bank,[]).append(a);px+=w+2;rh=max(rh,h);return a
def frame(bank,f):
 a=N['banks'][bank][f];path=R/N['sheets'][a['sheet']]['path'];sources[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest();sh=Image.open(path).convert('RGBA');x,y,w,h=a['cell'];return sh.crop((x,y,x+w,y+h)),a
def heat(im):
 v=np.array(im.convert('RGBA'));rgb=v[:,:,:3].astype(float);lum=rgb[:,:,0]*.22+rgb[:,:,1]*.58+rgb[:,:,2]*.20;idx=np.digitize(lum,[45,85,135,195,235]);pal=np.array([[71,0,12],[153,5,17],[238,30,19],[255,105,27],[255,196,66],[255,251,217]],dtype=np.uint8);v[:,:,:3]=pal[idx];return Image.fromarray(v)
# Retain every source pose's actual warm eye pixels. These restore the emitting
# lenses over the standard white hit frame, without a stationary face patch.
for bank in ['brain','charge','focus']:
 for f in range(len(N['banks'][bank])):
  im,a=frame(bank,f);v=np.array(im);yy,xx=np.indices(v.shape[:2]);mask=np.zeros(v.shape[:2],bool)
  for cx,cy in a['eyes']:
   roi=((xx-cx)/22)**2+((yy-cy)/19)**2<1;warm=roi&(v[:,:,0]>110)&(v[:,:,0]>v[:,:,1]*1.08)&(v[:,:,0]>v[:,:,2]*1.04)&(v[:,:,3]>48)
   hot=roi&binary_dilation(warm,iterations=2)&(v[:,:,:3].min(2)>170)&(v[:,:,3]>48);mask|=warm|hot
  v[~mask,3]=0;emit('eyes_'+bank,Image.fromarray(v),(192,192),{'eyes':a['eyes']})
# A tight strip taken from the generated optical column. Every source row is
# filled with its own core material, eliminating detached/hollow hairlines.
flows=[]
for f in range(16):
 p=R/f'_ART_SOURCES/dracodia_brain_1023/raw/laser_new/{f+1:02}.png';sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();raw=heat(Image.open(p).convert('RGBA').crop((20,24,44,172)));v=np.array(raw);out=np.zeros((148,24,4),dtype=np.uint8)
 for y,row in enumerate(v):
  valid=np.flatnonzero((row[:,3]>48)&(np.arange(24)>=5)&(np.arange(24)<=18));assert len(valid),(f,y)
  center=valid[np.argmin(abs(valid-12))];lo=hi=int(center)
  while lo>0 and row[lo-1,3]>48:lo-=1
  while hi<23 and row[hi+1,3]>48:hi+=1
  segment=Image.fromarray(row[None,lo:hi+1,:]);segment=segment.resize((24,1),Image.Resampling.NEAREST);out[y]=np.array(segment)[0];out[y,:,3]=255
 # Eye-matched uninterrupted incandescent centre. Source motion remains in the
 # surrounding crimson/orange channels instead of dimming the whole column.
 for x in range(24):
  distance=abs(x-11.5)/11.5
  if distance<.43:out[:,x,:3]=[255,251,217]
  elif distance<.61:out[:,x,:3]=[255,203,73]
  elif distance<.73:
   bright=out[:,x,0]>210;out[:,x,:3]=[255,75,23];out[bright,x,:3]=[255,153,35]
 flows.append(Image.fromarray(out))
sourcestrip=Image.new('RGBA',(80*16,624*2));sp=ImageDraw.Draw(sourcestrip)
for level,width in enumerate(A['widths']):
 for f,flow in enumerate(flows):
  # One continuous full-aperture shaft; irregular generated packet colours move
  # through it. No transparent row can detach it from the eye.
  shaft=flow.resize((width,600),Image.Resampling.NEAREST);im=Image.new('RGBA',(80,624));im.alpha_composite(shaft,((80-width)//2,12));emit('beam_'+str(level),im,(40,12),{'width':width})
  if f<5:
   launch=im.copy();v=np.array(launch);length=[96,208,344,488,600][f];v[12+length:,:,3]=0;emit('start_'+str(level),Image.fromarray(v),(40,12),{'width':width,'length':length})
  if level in [0,5]:sourcestrip.alpha_composite(im,(80*f,624*(level==5)))
# Recovery uses stored alpha/dither phases and is explicitly harmless.
order=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])
for f in range(16):
 im=Image.new('RGBA',(80,624));im.alpha_composite(flows[f].resize((42,600),Image.Resampling.NEAREST),(19,12));v=np.array(im);yy,xx=np.indices(v.shape[:2]);rank=order[(yy//2)%4,(xx//2)%4];v[rank<=f,3]=0;emit('recover',Image.fromarray(v),(40,12))
for colour,file in [('green','fov-light-green.png'),('yellow','fov-yellow.png'),('red','fov-neon-red.png')]:
 p=R/'assets/bossmode/ui'/file;sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();src=Image.open(p).convert('RGBA').crop((0,0,640,640));src=src.crop(src.getbbox());band=src.crop((src.width//2-24,src.height//3,src.width//2+24,src.height-12)).resize((42,600),Image.Resampling.NEAREST);im=Image.new('RGBA',(80,624));im.alpha_composite(band,(19,12));emit('warning_'+colour,im,(40,12))
flush();(R/'assets/neural_optics_art_1030.js').write_text("'use strict';\nconst NB80_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
sourcestrip.save(D/'optic-flow-source-strip.png');(D/'provenance.json').write_text(json.dumps({'sources':sources,'pages':len(A['pages']),'frames':sum(len(v)for v in A['banks'].values()),'palette':'Eye-matched ember red, hot orange/yellow and ivory-white; no violet/blue optical energy.','beamWidths':A['widths'],'beamPivot':[40,12],'beamLength':600,'tool':'Offline authoring from approved PixelLab frames; frame/alpha/palette transforms baked, runtime fixed blits only.'},indent=2))
preview=Image.new('RGB',(384*2+160,624),(16,23,34));im,a=frame('focus',1);preview.paste(im,(0,0),im);v=np.array(flows[9].resize((42,380),Image.Resampling.NEAREST));beam=Image.fromarray(v)
for eye in a['eyes']:preview.paste(beam,(eye[0]-21,eye[1]),beam)
for f in [0,1,2,3]:preview.paste(flows[f].resize((42,600),Image.Resampling.NEAREST),(410+f*82,12));
preview.save(W/'new-optics-preview.png');print(json.dumps({'frames':sum(len(v)for v in A['banks'].values()),'pages':len(A['pages']),'widths':A['widths']}))
