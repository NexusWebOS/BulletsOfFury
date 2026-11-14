from pathlib import Path
import json,os,subprocess
import numpy as np
from PIL import Image,ImageDraw

W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True)
C=640;P=[320,320];FOOT=474;SCALE=.63
rows=json.loads((W/'source-index.json').read_text())
provenance=json.loads((W/'blue-generation-provenance.json').read_text())
for r in rows:
 if not r.get('prompt'):
  r['prompt']=next(z['revisedPrompt'] for z in provenance if Path(z['savedPath']).name==Path(r['source']).name)
(W/'source-index.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
SOURCES={r['name']:r for r in rows if r['accepted']}
HEADS={
 'blue-cap':[[260,20,380,160],[875,235,995,400],[250,990,385,1180],[875,990,1005,1180]],
 'blue-aux':[[260,365,375,525],[885,15,1005,170],[260,815,375,970],[885,1000,1005,1165]],
 'blue-side':[[345,25,530,125],[725,80,905,180],[70,730,255,845],[695,730,885,850]],
 'drac-cap':[[250,10,390,155],[840,275,1005,530],[235,940,405,1195],[840,940,1010,1195]],
 'drac-aux':[[235,305,410,555],[860,3,1010,155],[240,825,405,1070],[860,925,1015,1185]],
 'drac-side':[[285,20,575,130],[660,100,940,205],[25,725,310,845],[655,725,930,845]],
}
CORES={
 'blue-cap':[[315,230],[940,210],[315,860],[940,885]],
 'blue-aux':[[315,260],[940,270],[315,800],[940,890]],
 'blue-side':[[330,215],[945,215],[330,850],[945,850]],
 'drac-cap':[[320,290],[920,260],[320,865],[920,900]],
 'drac-aux':[[320,270],[940,280],[315,805],[940,900]],
 'drac-side':[[325,225],[955,230],[330,840],[955,840]],
}
CACHE={};source_audit=[]

def raw(name,cell):
 key=(name,cell)
 if key in CACHE:return dict(CACHE[key])
 p=W/SOURCES[name]['file'];im=Image.open(p).convert('RGBA');a=np.asarray(im);h,w=a.shape[:2]
 alpha=a[:,:,3]>180;x0,x1=[0,w//2,w][cell%2:cell%2+2];y0,y1=[0,h//2,h][cell//2:cell//2+2]
 crop=alpha[y0:y1,x0:x1]
 assert crop.any() and not(crop[0].any()or crop[-1].any()or crop[:,0].any()or crop[:,-1].any()),('source clips',key)
 yy,xx=np.indices(alpha.shape);nom=(x0+x1)/2
 feet=alpha&(yy>y0+(y1-y0)*.63)&(yy<y1)&(abs(xx-nom)>67)&(abs(xx-nom)<240)
 fy,fx=np.where(feet);assert len(fx)>100,('feet missing',key)
 sole=int(fy.max());bottom=feet&(yy>sole-26);by,bx=np.where(bottom)
 root=[float((bx.min()+bx.max())/2)-x0,float(sole-y0)]
 cr,cg,cb=[a[:,:,i].astype(float)for i in range(3)];sx,sy=CORES[name][cell];sx*=w/1254;sy*=h/1254
 core=alpha&(abs(xx-sx)<32)&(abs(yy-sy)<24)&((cr>155)&(cr>cg*1.3)&(cr>cb*1.3)if name.startswith('drac')else(cb>160)&(cb>cr*1.25))
 ry,rx=np.where(core);assert len(rx)>8,('body registration landmark absent',key)
 root[0]=float(rx.mean())-x0
 box=HEADS[name][cell];bx0,by0,bx1,by1=[round(box[i]*(w if i%2==0 else h)/1254)for i in range(4)]
 r,g,b=[a[:,:,i].astype(float)for i in range(3)];region=(xx>=bx0)&(xx<bx1)&(yy>=by0)&(yy<by1)
 hot=alpha&region&((r>145)&(b>155)&(b>g*1.15)&(r>g*1.15)if name.startswith('drac')else(b>160)&(b>r*1.22)&(b>g*1.1))
 cy,cx=np.where(hot);assert len(cx)>40,('head absent',key)
 center=[float(cx.mean()),float(cy.mean())]
 side=name.endswith('side');axis=[-1,0]if side else[0,1]
 if side:
  cap=alpha&region&(abs(yy-center[1])<12)
  ty,tx=np.where(cap);tip=[float(tx.min()+1),center[1]]
 else:
  cap=alpha&region&(abs(xx-center[0])<12)
  ty,tx=np.where(cap);tip=[center[0],float(ty.max()-1)]
 tx,ty=map(round,tip)
 if not alpha[ty,tx]:
  cy,cx=np.where(alpha&region&(abs(xx-tx)<10)&(abs(yy-ty)<10));assert len(cx),('tip absent',key)
  j=np.argmin((cx-tx)**2+(cy-ty)**2);tip=[float(cx[j]),float(cy[j])]
 z=dict(input=str(p),source=name,sourceCell=cell,crop=[x0,y0,x1-x0,y1-y0],root=root,tip=[tip[0]-x0,tip[1]-y0],headCenter=[center[0]-x0,center[1]-y0],grip=[root[0],root[1]-205],scale=SCALE,mirror=False,capAxis=axis)
 source_audit.append(dict(source=name,cell=cell,root=root,head=center,tip=tip,capAxis=axis,sourceEdgeIssue=False));CACHE[key]=z;return dict(z)

jobs=[]
for unit,prefix in [('blue','blue'),('drac','corrupt')]:
 overhead=[('aux',0),('aux',1),('cap',0),('cap',0),('cap',0),('cap',0),('cap',0),('aux',2),('aux',2),('cap',1),('aux',3),('cap',2),('cap',3),('aux',3),('aux',0),('aux',0)]
 side=[('aux',0),('side',0),('side',0),('side',1),('side',1),('side',2),('side',2),('side',2),('side',2),('side',3),('side',3),('side',3),('side',3),('aux',0),('aux',0),('aux',0)]
 for suffix,seq in [('overhead',overhead),('sides',side),('right',side)]:
  frames=[]
  for i,(group,cell)in enumerate(seq):
   q=raw(unit+'-'+group,cell);q['mirror']=suffix=='right'and group=='side'
   q['phase']='behind-head'if suffix=='overhead'and i in[2,3,4,5,6]else'contact'if suffix=='overhead'and i in[11,12]or suffix!='overhead'and 5<=i<=8 else'downstroke'if suffix=='overhead'and 7<=i<=10 else'recovery'if i>=12 else'load'
   q['duration']=.14 if q['phase']=='behind-head'and i==5 else .055
   frames.append(q)
  jobs.append(dict(name=prefix+'-'+suffix,unit=unit,frames=frames,cell=C,pivot=P,foot=FOOT))
(W/'jobs.json').write_text(json.dumps(jobs,indent=2))
subprocess.run([os.environ.get('ASEPRITE',r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'),'--batch','--script-param','out='+W.as_posix(),'--script',str(W/'author.lua')],check=True)
M={};audit=[]
for j in jobs:
 n=j['name'];sheet=Image.open(E/(n+'_regular.png'));arr=np.asarray(sheet);meta=[]
 for i,z in enumerate(j['frames']):
  a=arr[i//4*C:(i//4+1)*C,i%4*C:(i%4+1)*C,3];y,x=np.where(a>96);bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  assert min(bounds[:2])>0 and max(bounds[2:])<C,('export clips',n,i,bounds)
  def pos(p):
   q=[P[0]+(p[0]-z['root'][0])*SCALE,FOOT+(p[1]-z['root'][1])*SCALE]
   if z['mirror']:q[0]=C-1-q[0]
   return q
  axis=[-z['capAxis'][0],z['capAxis'][1]]if z['mirror']else z['capAxis']
  m=dict(tip=pos(z['tip']),headCenter=pos(z['headCenter']),grip=pos(z['grip']),bounds=bounds,spans=[np.flatnonzero(np.diff(np.r_[False,v>96,False])).tolist()for v in a],depth=1,wholeGenerated=True,faceForward=True,source=z['source'],sourceCell=z['sourceCell'],phase=z['phase'],capAxis=axis,endCapLeads=True)
  tx,ty=map(round,m['tip'])
  if not a[ty,tx]>96:
   ay,ax=np.where(a>96);near=(abs(ax-tx)<=4)&(abs(ay-ty)<=4);assert near.any(),('contact off alpha',n,i,m['tip'])
   ax,ay=ax[near],ay[near];k=np.argmin((ax-tx)**2+(ay-ty)**2);m['tip']=[int(ax[k]),int(ay[k])]
  meta.append(m);audit.append(dict(bank=n,frame=i,source=z['source'],sourceCell=z['sourceCell'],phase=z['phase'],bounds=bounds,capAxis=axis,tip=m['tip']))
 M[n]=dict(cell=[C,C],pivot=P,cols=4,count=16,folder='cap_strikes_1111',meta=meta)
 # Palette derivatives preserve alpha and all frame coordinates exactly.
 base=np.array(sheet.convert('RGBA'));red,green,blue=[base[:,:,k].astype(float)for k in range(3)];hi=np.maximum.reduce([red,green,blue]);lo=np.minimum.reduce([red,green,blue]);opaque=base[:,:,3]>0
 for material in ['chrome','red','hit','red_hit']:
  out=base.copy();rr,gg,bb=red.copy(),green.copy(),blue.copy()
  if material in ['hit','red_hit']:
   rr[opaque]=255;gg[opaque]=255 if material=='hit' else 35;bb[opaque]=255 if material=='hit' else 42
  elif material=='chrome':
   mask=opaque&(hi-lo<65)&(hi>30);k=np.minimum(255,hi*1.4+9);rr[mask]=k[mask];gg[mask]=k[mask];bb[mask]=np.minimum(255,k[mask]+5)
  else:
   energy=opaque&(blue>green*1.4)&((blue>red*1.15)|(red>green*1.4))&(blue>115);k=np.maximum(red,blue);rr[energy]=np.minimum(255,k[energy]*1.1);gg[energy]=k[energy]*.12;bb[energy]=k[energy]*.18
   metal=opaque&~energy&(hi>40)&(hi-lo<65);rr[metal]=np.minimum(255,hi[metal]*1.2);gg[metal]=green[metal]*.48;bb[metal]=blue[metal]*.52
  for k,v in enumerate([rr,gg,bb]):out[:,:,k]=np.floor(v).astype(np.uint8)
  Image.fromarray(out).save(E/(n+'_'+material+'.png'))
 for material in ['regular','chrome','red','hit','red_hit']:
  p=E/(n+'_'+material+'.png');Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
 # Direct frame playback preview; game timings continue with native owners.
 fs=[]
 for i in range(16):
  frame=sheet.crop((i%4*C,i//4*C,(i%4+1)*C,(i//4+1)*C)).convert('RGBA');out=Image.new('RGBA',(C,C),'#101820');out.alpha_composite(frame);fs.append(out.convert('RGB'))
 fs[0].save(E/(n+'-frames.gif'),save_all=True,append_images=fs[1:],duration=[160 if i in[4,5,11]else 65 for i in range(16)],loop=0,disposal=2)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'cap_strikes_art_1111.js').write_text("'use strict';\n/* Complete end-cap-led hammer drawings. */\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\n')
(W/'audit.json').write_text(json.dumps(dict(passed=True,cells=audit,sources=source_audit,uniqueDrawings=len(CACHE),normalization='complete poses only; direct original source .63 export; common boot baseline; no body/held-weapon assembly'),indent=2))
print('Exported',len(audit),'whole-figure cells from',len(CACHE),'complete drawings.',flush=True)
