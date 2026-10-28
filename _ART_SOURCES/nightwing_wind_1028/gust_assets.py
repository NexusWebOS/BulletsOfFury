"""Normalize generated airflow frames and bake all directional views offline."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math,hashlib
def gust_banks(root):
 folder=Path(root)/'pixellab/gust_frames'
 if not folder.exists():folder=Path(root)/'gust_frames'
 paths=sorted(folder.glob('*.png'));assert len(paths)==16,'Require16 completed gust animation frames'
 raw=[Image.open(p).convert('RGBA')for p in paths];boxes=[q.getbbox()for q in raw];assert all(boxes)
 height=max(b[3]-b[1]for b in boxes)
 def authored_frames(visible,tip):
  size=round(64*visible/height/2)*2;frames=[]
  for q in raw:
   q=q.resize((size,size),Image.Resampling.NEAREST);a=np.array(q);alpha=a[:,:,3];ys,xs=np.where(alpha>128);bottom=int(ys.max());near=(ys>=bottom-2);weights=np.maximum(1,a[ys[near],xs[near],:3].sum(1));center=float(np.average(xs[near],weights=weights));out=Image.new('RGBA',(64,64));out.alpha_composite(q,(round(tip[0]-center),round(tip[1]-bottom)));frames.append(out)
  return frames,size/64
 travel,unit=authored_frames(36,(32,40));muzzle,mu=authored_frames(26,(32,58));muzzle=muzzle[::2]
 def directions(ff):return[q.rotate(-d*360/32,Image.Resampling.NEAREST,center=(32,32))for d in range(32)for q in ff]
 return dict(wind_bullet=directions(travel),wind_muzzle=directions(muzzle)),dict(directions=32,phaseFrames=16,muzzleFrames=8,pivot=[32,32],leadingTip=[32,40],sourceUnit=unit,muzzleUnit=mu,keyframeJob='b5986218-1399-4445-be0c-cf08ba36f449',selectedCandidate=4,animationJob='9c1789b8-64ba-4aa4-819d-195ecf675e54',sourceHashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in paths})
def contact(root,out):
 banks,m=gust_banks(root);im=Image.new('RGBA',(8*144,4*160),(9,24,32,255));d=ImageDraw.Draw(im)
 for row,(key,start,count)in enumerate([('wind_bullet',0,8),('wind_bullet',8,8),('wind_bullet',0,8),('wind_muzzle',0,8)]):
  for col in range(8):
   idx=(col*4*m['phaseFrames']if row==2 else start+col);q=banks[key][idx].resize((128,128),Image.Resampling.NEAREST);im.alpha_composite(q,(col*144+8,row*160));d.text((col*144+5,row*160+134),key.replace('wind_','')+' '+str(idx),fill='white')
 im.save(out)
