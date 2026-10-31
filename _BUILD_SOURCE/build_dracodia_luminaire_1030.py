"""RD78: original generated orb, authored expanding/flooding FOV and void light.
Fixed native680x512 arena graphics; all fill/brightness/fade is baked offline.
"""
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/dracodia_luminaire_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent
D=R/'_ART_SOURCES/dracodia_luminaire_1030';O=R/'assets/game/levels/stage_08/boss/luminaire_1030';D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
raw=W/'luminaire-generated.png';shutil.copyfile(raw,D/'luminaire-generated.png')if raw.resolve()!=(D/'luminaire-generated.png').resolve()else None
im=Image.open(raw).convert('RGBA');CW,CH=680,512;X,Y=np.meshgrid(np.arange(CW),np.arange(CH));CX=340;CY=160;art={'banks':{},'world':[CW,CH],'centre':[CX,CY],'safeHints':[[166,226],[514,226]],'orbOffsets':[]};audit=[]
def bank(name,frames,w,h,pivot,cols=4):
 limit=16 if w==680 else len(frames);pages=[]
 for start in range(0,len(frames),limit):
  group=frames[start:start+limit];sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(group)/cols)))
  for i,f in enumerate(group):sheet.paste(f,((i%cols)*w,(i//cols)*h))
  suffix='_'+str(start//limit).zfill(2)if len(frames)>limit else'';p=O/(name+suffix+'.webp');sheet.save(p,lossless=True,method=6);pages.append({'key':'rd78_'+name+suffix,'path':p.relative_to(R).as_posix(),'start':start,'frames':len(group)})
  audit.append({'bank':name,'start':start,'frames':len(group),'cell':[w,h],'sheet':list(sheet.size)})
 art['banks'][name]={'key':pages[0]['key'],'path':pages[0]['path'],'w':w,'h':h,'pivot':pivot,'cols':cols,'frames':len(frames),'pages':pages}
def source_cell(i):
 x=i%4;y=i//4;box=(round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4));cell=im.crop(box);out=Image.new('RGBA',(360,360));out.paste(cell,((360-cell.width)//2,(360-cell.height)//2));return out
# Common proportional units preserve the generated growth within each bank.
charge=[]
for i in range(48):
 phase=i/47*7;f=int(phase);mix=phase-f;cell=Image.blend(source_cell(f),source_cell(min(7,f+1)),mix).rotate(5*math.sin(i/47*math.pi*4),Image.Resampling.NEAREST).resize((124,124),Image.Resampling.NEAREST);out=Image.new('RGBA',(160,160));out.paste(cell,(18,18));charge.append(out)
bank('orb_charge',charge,160,160,[80,80],8)
release=[]
for i in range(12):
 phase=i/11*3;f=8+int(phase);cell=Image.blend(source_cell(f),source_cell(min(11,f+1)),phase-int(phase)).resize((240,240),Image.Resampling.NEAREST);out=Image.new('RGBA',(256,256));out.paste(cell,(8,8));release.append(out)
bank('orb_release',release,256,256,[128,128],4)
def ease(v):v=np.clip(v,0,1);return v*v*(3-2*v)
def region(u):
 r=10+154*ease(u);circle=(X-CX)**2+(Y-CY)**2<=r*r
 fill=ease((u-.2)/.8);front=CH-(CH-CH*.49)*fill+6*np.sin(X/37+u*3.1)
 flood=(Y>=front)&(u>.2)
 return(circle|flood)&(u>.01)
warnings=[]
for i in range(48):
 u=i/47;m=region(u);inner=np.array(Image.fromarray(m.astype('uint8')*255).filter(ImageFilter.MinFilter(5)))>0;edge=m&~inner
 colour=[54,245,86]if u<.36 else[255,218,45]if u<.74 else[255,55,66]
 a=np.zeros((CH,CW,4),dtype=np.uint8);a[m,:3]=colour;a[m,3]=76;a[edge,3]=220
 scan=m&((Y+int(u*64))%17<2);a[scan,3]=116;warnings.append(Image.fromarray(a))
bank('warning',warnings,CW,CH,[0,0],4)
final=region(1);inner=np.array(Image.fromarray(final.astype('uint8')*255).filter(ImageFilter.MinFilter(5)))>0;edge=final&~inner;spans=[]
for row in final:spans.append(np.flatnonzero(np.diff(np.pad(row.astype('int8'),(1,1)))).tolist())
art['dangerSpans']=spans
blasts=[]
for i in range(24):
 t=i/23;texture=(np.sin(X*.085+np.sin(Y*.042)*3-i*.6)+np.cos(Y*.09+X*.017+i*.6));veins=((X//3*71+Y//11*23+i*7)%179<2)&((Y+i*5)%19<11)
 pulse=.5+.5*math.sin(t*math.pi*3);peak=i<4 or 9<=i<12
 a=np.zeros((CH,CW,4),dtype=np.uint8);a[final]=[249,242,255,250]if peak else[221,194,255,220]
 hot=final&(texture>.3);a[hot]=[255,253,255,255]if peak else[241,222,255,240];a[edge]=[204,133,255,255]
 crack=final&veins;a[crack]=[139,62,211,220]
 glints=final&(((X//3*17+Y//3*23+i*19)%127)<3);a[glints]=[255,255,255,255]
 blasts.append(Image.fromarray(a))
bank('blast',blasts,CW,CH,[0,0],4)
recovery=[]
for i in range(16):
 a=np.array(blasts[-1]);a[:,:,3]=(a[:,:,3].astype(float)*(1-i/15)**1.5).astype('uint8');recovery.append(Image.fromarray(a))
bank('recovery',recovery,CW,CH,[0,0],4)
# Same-frame chest sockets from the actual raised-claw source poses.
s=(R/'assets/stage8_identity_art_1018.js').read_text();V=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]['clips']['colossus_scythe']['frames'];sources={}
for i in range(16):
 f=round(ease(i/15)*6);p=R/V[f]['layers']['core']['path'];v=np.array(Image.open(p).convert('RGBA'));yy,xx=np.indices(v.shape[:2]);m=(xx>140)&(xx<181)&(yy>135)&(yy<195)&(v[:,:,0]>220)&(v[:,:,1]>180)&(v[:,:,2]>150)&(v[:,:,3]>50);art['orbOffsets'].append([round((xx[m].mean()-160)*410/320),round((yy[m].mean()-160)*410/320)]);sources[V[f]['layers']['core']['path']]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'assets/dracodia_luminaire_art_1030.js').write_text('"use strict";\nconst RD78_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
for x,y in art['safeHints']:assert not final[y,x]
assert final[450,202]and final[226,340]
audit={'banks':audit,'generatedSourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'bodySources':sources,'dangerPixels':int(final.sum()),'safePixels':int((~final).sum()),'nativeArena':[CW,CH],'evenCells':True,'sourceMode':'Built-in image generation with Dracodia chest reference; offline fixed-frame normalization and authored field/alpha levels.','safeHints':art['safeHints']};(D/'provenance.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit['banks']))
preview=Image.new('RGBA',(680*3,512));preview.paste(warnings[16],(0,0));preview.paste(warnings[-1],(680,0));preview.paste(blasts[2],(1360,0));preview.save(W/'field-preview.png')
