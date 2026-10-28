"""Offline source-pixel projection of the one approved Nightwing planform.
No legacy Part2 aircraft silhouettes or runtime transforms are used.
"""
from PIL import Image
import numpy as np,math
def belly(top,source):
 a=np.array(top).copy();b=np.array(source);inside=(a[:,:,3]>0)&(b[:,:,3]>0);a[inside,:3]=b[inside,:3]
 return Image.fromarray(a)
def locked_motion(top,under,axis,theta):
 # Extrude only existing occupied texels. Heights distinguish the two engine
 # barrels, canopy/fuselage and thin wings; the planform remains authored.
 a=np.array(top);b=np.array(under);yy,xx=np.indices(a.shape[:2]);valid=a[:,:,3]>48;x=(xx-136).astype(float);y=(yy-136).astype(float)
 height=np.full(x.shape,2.0)
 fuselage=8*np.sqrt(np.maximum(0,1-(x/13)**2));height=np.maximum(height,fuselage*((y>-64)&(y<85)))
 for ex in [-12.5,12.5]:height=np.maximum(height,14*np.sqrt(np.maximum(0,1-((x-ex)/9)**2))*((y>-65)&(y<-20)))
 height=np.maximum(height,6*((abs(abs(x)-58)<6)&(y>=0)&(y<45)))
 points=[];colors=[];alphas=[]
 H=np.rint(height).astype(int)
 for z in range(-3,15):
  mask=valid&(H>=z);X=x[mask];Y=y[mask];Z=np.full(len(X),z,dtype=float);rgb=a[mask,:3].copy();bottom=z==-3;topface=H[mask]==z
  if bottom:rgb=b[mask,:3].copy()
  elif not topface.all():rgb[~topface]=np.rint(rgb[~topface].astype(float)*.65).astype(np.uint8)
  points.append(np.stack([X,Y,Z],axis=1));colors.append(rgb);alphas.append(a[mask,3])
 P=np.concatenate(points);C=np.concatenate(colors);A=np.concatenate(alphas);c=math.cos(theta);s=math.sin(theta)
 if axis=='roll':X=P[:,0]*c+P[:,2]*s;Y=P[:,1];depth=-P[:,0]*s+P[:,2]*c
 else:X=P[:,0];Y=P[:,1]*c+P[:,2]*s;depth=-P[:,1]*s+P[:,2]*c
 ix=np.rint(X+136).astype(int);iy=np.rint(Y+136).astype(int);inside=(ix>=0)&(ix<272)&(iy>=0)&(iy<272);order=np.argsort(depth[inside],kind='stable');ix=ix[inside][order];iy=iy[inside][order];C=C[inside][order];A=A[inside][order]
 out=np.zeros((272,272,4),dtype=np.uint8);out[iy,ix,:3]=C;out[iy,ix,3]=A
 # Exact cardinal faces retain the original source pixels and metal palette.
 if abs(s)<1e-6:
  q=top if c>0 else under
  if c<0:q=q.transpose(Image.Transpose.FLIP_LEFT_RIGHT if axis=='roll'else Image.Transpose.FLIP_TOP_BOTTOM)
  result=q.copy()
 else:result=Image.fromarray(out)
 engines=[]
 for ex in [-12.5,12.5]:
  ey=-64;ez=6
  engines.append([ex*c+ez*s,ey]if axis=='roll'else[ex,ey*c+ez*s])
 return result,dict(engines=engines,angle=0 if axis=='roll'or c>=0 else math.pi,scale=1)
