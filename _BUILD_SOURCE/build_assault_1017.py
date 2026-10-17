"""Export reviewed generated sheets with fixed even canvases and physical pivots.
No per-frame scale fit. Each bank records its raw rects, translation and one scale.
"""
from pathlib import Path
import argparse,json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
P=argparse.ArgumentParser();P.add_argument('--sources',default='_ART_SOURCES/assault_1017/sources.json');a=P.parse_args()
sources=json.loads((R/a.sources).read_text());out=R/'assets/game/shared/combat/assault_1017';out.mkdir(parents=True,exist_ok=True)
raw=R/'_ART_SOURCES/assault_1017';raw.mkdir(parents=True,exist_ok=True)
qa=R/'_shots/assault_revision_1017/art';qa.mkdir(parents=True,exist_ok=True)
configs={k:(4,4,256,256) for k in ['stormJet','tankHull','tankTurret']}
configs.update({k:(4,4,64,96) for k in ['windBullets','windSpread','windHeavy','tankShell']});configs['windLaser']=(8,2,128,512)
manifest={};audit={}
for name,path in sources.items():
 path=Path(path);path=path if path.is_absolute() else R/path
 im=Image.open(path).convert('RGBA')
 if path.resolve()!=(raw/(name+'.png')).resolve():shutil.copy2(path,raw/(name+'.png'))
 cols,rows,w,h=configs[name]
 frames=[];rects=[];anchors=[]
 for i in range(16):
  x,y=i%cols,i//cols;box=(round(x*im.width/cols),round(y*im.height/rows),round((x+1)*im.width/cols),round((y+1)*im.height/rows))
  q=im.crop(box);pix=np.array(q);alpha=pix[:,:,3];mask=alpha>40
  # Genuine alpha is retained. Near-transparent export noise is not sprite ink.
  pix[alpha<8,3]=0;q=Image.fromarray(pix);ys,xs=np.nonzero(mask)
  if not len(xs):raise ValueError(name+' empty cell')
  if name in ['tankHull','tankTurret']:
   # Register the dark circular mounting socket, not the moving tread/barrel.
   cy=q.height*(.53 if name=='tankHull' else .40);cx=q.width*.5
   yy,xx=np.indices(alpha.shape);rgb=pix[:,:,:3].astype(float)
   socket=mask&(abs(xx-cx)<q.width*.14)&(abs(yy-cy)<q.height*.12)&(rgb.max(2)<110)&(rgb[:,:,2]<rgb[:,:,1]+8)
   sy,sx=np.nonzero(socket);anchor=(float(np.mean(sx)) if len(sx) else cx,float(np.mean(sy)) if len(sy) else cy)
  elif name.startswith('wind') and name!='windLaser':
   rgb=pix[:,:,:3].astype(float);yy,xx=np.indices(alpha.shape)
   metal=mask&(rgb.max(2)-rgb.min(2)<35)&(rgb.mean(2)>95)&(abs(xx-q.width*.5)<q.width*.23)
   my,mx=np.nonzero(metal);anchor=((float(mx.min()+mx.max())/2,float(my.min()+my.max())/2) if len(mx) else ((xs.min()+xs.max())/2,(ys.min()+ys.max())/2))
  elif name=='windLaser':anchor=((xs.min()+xs.max())/2,float(ys.max()-8))
  elif name=='tankShell':
   rgb=pix[:,:,:3].astype(float);metal=mask&(rgb[:,:,2]>25)&(rgb.max(2)-rgb.min(2)<110);my,mx=np.nonzero(metal)
   anchor=((mx.min()+mx.max())/2,(my.min()+my.max())/2) if len(mx) else ((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)
  else:
   rgb=pix[:,:,:3].astype(float);metal=mask&(rgb.max(2)-rgb.min(2)<95)&(rgb.mean(2)>45);my,mx=np.nonzero(metal)
   anchor=((mx.min()+mx.max())/2,(my.min()+my.max())/2) if len(mx) else ((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)
  frames.append(q);rects.append(box);anchors.append(anchor)
 pivot=(w//2,h-24 if name=='windLaser' else h//2)
 # Solve a SINGLE proportional scale against all source extents about the pivot.
 ext=[0,0,0,0]
 for q,(ax,ay) in zip(frames,anchors):
  ar=np.array(q.getchannel('A'));ys,xs=np.nonzero(ar>40)
  ext=[max(ext[0],ax-xs.min()),max(ext[1],xs.max()-ax),max(ext[2],ay-ys.min()),max(ext[3],ys.max()-ay)]
 scale=min((pivot[0]-6)/max(1,ext[0]),(w-pivot[0]-6)/max(1,ext[1]),(pivot[1]-6)/max(1,ext[2]),(h-pivot[1]-6)/max(1,ext[3]))
 sheet=Image.new('RGBA',(w*cols,h*rows));cells=[]
 for i,(q,(ax,ay)) in enumerate(zip(frames,anchors)):
  # Resize every source cell with the same scale, never reshape individual poses.
  z=q.resize((round(q.width*scale),round(q.height*scale)),Image.Resampling.NEAREST)
  c=Image.new('RGBA',(w,h));c.alpha_composite(z,(round(pivot[0]-ax*scale),round(pivot[1]-ay*scale)))
  sheet.alpha_composite(c,((i%cols)*w,(i//cols)*h));cells.append(c)
 dest=out/(name+'.png');sheet.save(dest,optimize=True)
 masks=[np.array(c.getchannel('A'))>40 for c in cells];yy,xx=np.nonzero(np.logical_or.reduce(masks));bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
 span=max(bounds[2]-bounds[0],bounds[3]-bounds[1]) if name!='stormJet' else bounds[2]-bounds[0]
 manifest[name]={'key':'a17_'+name,'path':dest.relative_to(R).as_posix(),'w':w,'h':h,'cols':cols,'rows':rows,'n':16,'pivot':list(pivot),'span':int(span),'bounds':bounds,'fps':18}
 onion=Image.new('RGBA',(w,h))
 for j in [0,4,8,12]:
  z=cells[j].copy();z.putalpha(z.getchannel('A').point(lambda a:round(a*.25)));onion=Image.alpha_composite(onion,z)
 bg=Image.new('RGBA',(w,h),(14,24,35,255));bg.alpha_composite(onion);bg.convert('RGB').save(qa/(name+'-onion.png'))
 cells[0].save(qa/(name+'-first.png'))
 audit[name]={'source':(raw/(name+'.png')).relative_to(R).as_posix(),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'sourceSize':list(im.size),'sourceRects':rects,'sourcePivots':anchors,'commonScale':scale,'output':manifest[name],'distinctFrames':len(set(hashlib.sha256(c.tobytes()).hexdigest() for c in cells))}
(R/'assets/assault_art_1017.js').write_text('"use strict";\n/* Generated by build_assault_1017.py. */\nconst A17_ART='+json.dumps(manifest,separators=(',',':'))+';\n',newline='\n')
(raw/'manifest.json').write_text(json.dumps(audit,indent=2));print(json.dumps({k:{'size':[v['w'],v['h']],'span':v['span'],'frames':audit[k]['distinctFrames']} for k,v in manifest.items()},indent=2))
