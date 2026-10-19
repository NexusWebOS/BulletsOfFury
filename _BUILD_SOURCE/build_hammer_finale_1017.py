"""Own the fixed-pose Hammer ending banks; no shared atlas changes.

PixelLab animates energy, never the identity plate. Armor fragments contain
only the exact authored stunned pixels, partitioned once for the final burst.
"""
from pathlib import Path
import hashlib,json,shutil,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_shots/hammer_finish_1017';SRC=ROOT/'_ART_SOURCES/hammer_finale_1017'
DEST=ROOT/'assets/game/levels/stage_05/boss/hammer_finale_1017'
for p in [SRC,DEST,SRC/'references']:p.mkdir(parents=True,exist_ok=True)
for name in ['stunned.png','registration.json']:shutil.copy2(RAW/'references'/name,SRC/'references'/name)
jobs=json.loads((RAW/'jobs.json').read_text())
(SRC/'generation.json').write_text(json.dumps({'permission':'Mike explicitly approved sending only arch_stun_0920 pose1, exported centered256x256, to PixelLab on2026-10-17.','jobs':jobs},indent=2)+'\n')
ref=Image.open(SRC/'references/stunned.png').convert('RGBA');R=np.array(ref);art={};audit={}
def save(bank,i,im,pivot,extra=None):
 assert im.width%2==0 and im.height%2==0
 key=f'hf17_{bank}_{i:02d}';path=DEST/(key+'.png');im.save(path,optimize=True)
 a={'key':key,'path':path.relative_to(ROOT).as_posix(),'w':im.width,'h':im.height,'pivot':list(pivot),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 if extra:a.update(extra)
 art.setdefault(bank,[]).append(a);return a
save('stunned',0,ref,(128,128))
Y,X=np.mgrid[:256,:256];r,g,b=R[:,:,:3].astype(float).transpose(2,0,1)
emissive=(R[:,:,3]>0)&(b>75)&(b>r*1.16)&(b>g*1.05)
core=(X>=116)&(X<=139)&(Y>=134)&(Y<=157)
emissive|=core&(R[:,:,3]>0)&(b>95)&(b>r*1.03)
socket_mask=np.array(Image.fromarray((emissive*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
body_mask=np.array(ref.getchannel('A').filter(ImageFilter.MaxFilter(3)))>0
unlit=R.copy();unlit[emissive,:3]=(unlit[emissive,:3]*.22).astype('uint8');save('unlit',0,Image.fromarray(unlit),(128,128))
glow=R.copy();glow[:,:,3]=np.where(emissive&core,R[:,:,3],0);glow=Image.fromarray(glow)
spill=glow.getchannel('A').filter(ImageFilter.MaxFilter(5));layer=Image.new('RGBA',ref.size,(130,160,255,0));layer.putalpha(spill.point(lambda a:round(a*.18)));layer.alpha_composite(glow)
save('coreGlow',0,layer,(128,128))
# These measured anatomical seed points only decide which existing armor
# pixels leave together. Reassembling every cut is byte-identical to ref.
seeds=[(124,107),(95,120),(158,116),(79,151),(77,177),(72,211),
 (121,145),(138,159),(106,166),(99,188),(120,185),(106,210),
 (150,176),(154,195),(161,215),(172,152),(180,176),(187,190)]
distance=np.stack([(X-x)**2+(Y-y)**2 for x,y in seeds]);labels=distance.argmin(0);rebuild=np.zeros_like(R)
for i,point in enumerate(seeds):
 pix=np.zeros_like(R);mask=labels==i;pix[mask]=R[mask];rebuild[mask]=pix[mask]
 im=Image.fromarray(pix);box=im.getbbox();assert box
 cx=round((box[0]+box[2])/2);cy=round((box[1]+box[3])/2)
 cell=Image.new('RGBA',(96,96));cell.alpha_composite(im,(48-cx,48-cy))
 assert cell.getchannel('A').getbbox()[0]>0 and cell.getchannel('A').getbbox()[2]<96
 save('fragments',i,cell,(48,48),{'origin':[cx,cy],'sourcePixelCut':list(box)})
assert np.array_equal(rebuild,R)
audit['fragments']={'count':len(seeds),'reassemblesExactRGBA':True,'addedPixels':0,'purpose':'One-time post-impact armor breakup only; not a combat rig.'}
for name in ['drain','pulse','engulf','rupture']:
 if '--available' in sys.argv and len(list((RAW/'returned'/name).glob('frame_*.png')))!=33:continue
 target=SRC/'returned'/name;target.mkdir(parents=True,exist_ok=True)
 for f in sorted((RAW/'returned'/name).glob('frame_*.png')):shutil.copy2(f,target/f.name)
 files=sorted(target.glob('frame_*.png'))[1:];assert len(files)==32,(name,len(files))
 records=[]
 for i,path in enumerate(files):
  im=Image.open(path).convert('RGBA');assert im.size==(256,256)
  p=np.array(im);rr,gg,bb=p[:,:,:3].astype(float).transpose(2,0,1)
  blue=(bb>75)&(bb>rr*1.18)&(bb>gg*1.08)
  hot=(rr>105)&(rr>bb*1.25)&(rr>gg*1.07)
  white=(np.min(p[:,:,:3],2)>190)&(np.max(p[:,:,:3],2)>235)
  if name in ['drain','pulse']:
   # The generated chest ring is larger than the authored socket. Keep its
   # changing light inside the actual panel/core pixels, plus detached arcs
   # outside the armor; never paste a new reactor disk over this boss.
   keep=((blue|white)&socket_mask)
   if name=='drain':keep|=blue&~body_mask
  else:
   fire_mask=np.array(Image.fromarray((hot*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>0
   keep=blue|hot|(white&fire_mask)
   if name=='rupture' and i>=10:keep&=~(body_mask&blue&~fire_mask)
  # Discard generated armor/pose pixels. The real stunned plate below is
  # immutable, including all its fixtures; only actual generated energy ships.
  p[:,:,3]=np.where(keep,p[:,:,3],0)
  out=Image.new('RGBA',(320,320));out.alpha_composite(Image.fromarray(p),(32,32))
  save(name,i,out,(160,160))
  records.append({'source':path.name,'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'translation':[32,32],'scale':1,'energyPixels':int(np.count_nonzero(p[:,:,3]))})
 audit[name]=records
 # Full-bank contact and immediate-neighbor onion pairs use exported PNGs.
 sheet=Image.new('RGBA',(1280,768),'#0d1725');d=ImageDraw.Draw(sheet)
 onion=Image.new('RGBA',(1280,768),'#0d1725')
 for i,a in enumerate(art[name]):
  cell=Image.open(ROOT/a['path']);x=i%8*160;y=i//8*192
  # 160x160 proportional thumbnail, body shares exactly the same pivot.
  tile=Image.new('RGBA',(320,320));tile.alpha_composite(ref,(32,32));tile.alpha_composite(cell)
  sheet.alpha_composite(tile.resize((160,160),Image.Resampling.NEAREST),(x,y));d.text((x+4,y+163),str(i),fill='#ffffff')
  if i:
   prev=Image.open(ROOT/art[name][i-1]['path']);prev.putalpha(prev.getchannel('A').point(lambda n:n//3));tile.alpha_composite(prev)
  onion.alpha_composite(tile.resize((160,160),Image.Resampling.NEAREST),(x,y))
 sheet.convert('RGB').save(RAW/(name+'-contact.png'));onion.convert('RGB').save(RAW/(name+'-onion.png'))
audit['geometry']={'reference':[256,256],'energy':[320,320],'energyPivot':[160,160],'energyScale':1,'frameCount':32,'bodyImmutable':True}
(SRC/'export_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(DEST/'manifest.json').write_text(json.dumps(art,indent=2)+'\n')
(ROOT/'assets/hammer_finale_art_1017.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_hammer_finale_1017.py.\nconst HF17_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('EXPORTED',sum(map(len,art.values())),'PNGs;',sum(len(art.get(n,[])) for n in ['drain','pulse','engulf','rupture']),'PixelLab energy frames, exact authored stunned plate and18 lossless armor cuts; even fixed canvases and pivots')
