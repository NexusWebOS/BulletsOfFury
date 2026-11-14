from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label
W=Path(__file__).resolve().parent;V=W/'reviews';V.mkdir(exist_ok=True);report=[]
for name in ['draconus-gun-spin','draconus-gun-fire']:
 im=Image.open(W/'generated'/(name+'.png')).convert('RGBA');cw,ch=im.width/4,im.height/2;board=Image.new('RGBA',(1600,800),'#101820');d=ImageDraw.Draw(board)
 for k in range(8):
  box=[round(k%4*cw),round(k//4*ch),round((k%4+1)*cw),round((k//4+1)*ch)];f=im.crop(box);a=np.array(f);m=a[:,:,3]>180;l,n=label(m);sizes=np.bincount(l.ravel());sizes[0]=0;m=l==sizes.argmax();a[:,:,3]=m*255;a[~m]=0;yy,xx=np.where(m);border=bool(m[0].any()or m[-1].any()or m[:,0].any()or m[:,-1].any());h,w=m.shape
  # Enlarged unaltered source lower-center view for manual five-bore/rigidity review.
  crop=Image.fromarray(a).crop((round(w*.35),round(h*.65),round(w*.65),h));crop=crop.resize((300,350),Image.Resampling.NEAREST);board.alpha_composite(crop,(k%4*400+50,k//4*400+35));d.text((k%4*400+10,k//4*400+10),str(k)+' / clips='+str(border),fill='white')
  report.append(dict(name=name,cell=k,size=f.size,bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],clips=border))
 board.save(V/(name+'-muzzles.png'))
(W/'source-inspection.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
for p in sorted((W/'generated').glob('*transform-[abcd].png')):
 a=np.array(Image.open(p).convert('RGBA'));print(p.name,Image.open(p).size,'alpha',np.percentile(a[:,:,3],[0,25,50,75,100]).tolist(),'corner',a[5,5].tolist(),flush=True)
