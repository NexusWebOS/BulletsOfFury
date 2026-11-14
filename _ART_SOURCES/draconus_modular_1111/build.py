from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True);V=W/'reviews';V.mkdir(exist_ok=True)
a=np.array(Image.open(W/'generated/draconus-empty-master.png').convert('RGBA'));mask=a[:,:,3]>180;lab,n=label(mask);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();a[:,:,3]=mask*255;a[~mask]=0;yy,xx=np.where(mask)
scale=276/(yy.max()-yy.min()+1);root=[(xx.min()+xx.max())/2,float(yy.max())];off=[round(256-root[0]*scale),round(410-root[1]*scale)];body=Image.new('RGBA',(512,512));body.alpha_composite(Image.fromarray(a).resize((round(a.shape[1]*scale),round(a.shape[0]*scale)),Image.Resampling.NEAREST),off)
def spans(mask):return[np.flatnonzero(np.diff(np.r_[False,row,False])).tolist()for row in mask]
def bounds(mask):
 y,x=np.where(mask);return[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def palette(im,mat,gun=False):
 a=np.array(im).copy();r,g,b=[a[:,:,v].astype(float)for v in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);opaque=a[:,:,3]>0
 if gun:
  blue=opaque&(b>r*1.4)&(b>95);r[blue]=np.minimum(255,b[blue]*.85);g[blue]=g[blue]*.35
 if mat=='chrome':
  neutral=opaque&(hi-lo<65)&(hi>30);v=np.minimum(255,hi*1.4+9);r[neutral]=g[neutral]=v[neutral];b[neutral]=np.minimum(255,v[neutral]+5)
 elif mat=='red':
  energy=opaque&(b>g*1.4)&(b>115);v=np.maximum(r,b);r[energy]=np.minimum(255,v[energy]*1.1);g[energy]=v[energy]*.12;b[energy]=v[energy]*.18
 elif mat=='hit':r[opaque]=g[opaque]=b[opaque]=255
 for k,v in enumerate([r,g,b]):a[:,:,k]=np.floor(v).astype('uint8')
 return Image.fromarray(a)
# Same original whole-body pixels form the foreground grip; no new limbs.
ba=np.array(body);y,x=np.indices((512,512));front=(ba[:,:,3]>0)&(((x>=196)&(x<=231)&(y>=251)&(y<=286))|((x>=282)&(x<=311)&(y>=251)&(y<=284)));hands=ba.copy();hands[~front]=0;hands=Image.fromarray(hands)
gun_at=[198,224];pivot=[54,46];muzzle=[54,180];gunmeta=[];phase=[]
for k in range(36):
 im=Image.open(W/'references'/f'rotor-{k:02}.png').convert('RGBA');phase.append(im);gm=np.zeros((512,512),bool);gm[gun_at[1]:gun_at[1]+208,gun_at[0]:gun_at[0]+104]=np.array(im)[:,:,3]>0;gm&=~front;gunmeta.append(dict(bounds=bounds(gm),spans=spans(gm)))
def export_material(im,mat,gun=False):
 if not mat.startswith('arm'):return palette(im,mat,gun)
 f=int(mat[3:])/7;a=np.array(palette(im,'regular',gun));b=np.array(palette(im,'chrome',gun));out=a.copy();out[:,:,:3]=np.rint(a[:,:,:3].astype(float)+(b[:,:,:3].astype(float)-a[:,:,:3])*f).astype('uint8');return Image.fromarray(out)
for mat in ['regular','chrome','red','hit']+['arm'+str(k)for k in range(8)]:
 export_material(body,mat).save(E/f'body_{mat}.webp',lossless=True);export_material(hands,mat).save(E/f'grip_{mat}.webp',lossless=True)
 sheet=Image.new('RGBA',(104*4,208*9))
 for k,f in enumerate(phase):sheet.alpha_composite(export_material(f,mat,True),(k%4*104,k//4*208))
 sheet.save(E/f'gun_{mat}.webp',lossless=True)
 pickup=Image.new('RGBA',(1024,256));pickup.alpha_composite(export_material(phase[0],mat,True),(74,24));pickup.save(E/f'pickup_{mat}.webp',lossless=True)
 if mat=='regular':sheet.save(E/'gun_regular.png');body.save(E/'body_regular.png');hands.save(E/'grip_regular.png')
bm=np.array(body)[:,:,3]>0
pm=np.array(Image.open(E/'pickup_regular.webp'))[:,:256,3]>0
M=dict(body=dict(cell=[512,512],pivot=[256,256],bounds=bounds(bm),spans=spans(bm)),gun=dict(cell=[104,208],pivot=pivot,at=gun_at,muzzle=muzzle,cols=4,count=36,meta=gunmeta),pickup=dict(bounds=bounds(pm),spans=spans(pm)),scale=scale,root=root,bodyHeight=276,foregroundGripIsSameSourcePixels=True)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'draconus_modular_art_1111.js').write_text("'use strict';\n/* User-approved independent rotary gun; complete fixed body and same-source grip. */\nconst DGM1111_ART="+json.dumps(M,separators=(',',':'))+';\n')
board=Image.new('RGBA',(512*4,512*2),'#101820');d=ImageDraw.Draw(board)
for k in range(8):
 mat='chrome'if k>=4 else'regular';f=[0,9,18,27][k%4];p=Image.new('RGBA',(512,512));p.alpha_composite(palette(body,mat));p.alpha_composite(palette(phase[f],mat,True),gun_at);p.alpha_composite(palette(hands,mat));board.alpha_composite(p,(k%4*512,k//4*512));d.text((k%4*512+12,k//4*512+12),mat+' / rotor '+str(f),fill='white')
board.save(V/'rig-review.png');body.save(V/'empty-body.png');print('Prepared fixed whole body and36 independent rotary phases, regular/Chromium/red/white.',flush=True)
