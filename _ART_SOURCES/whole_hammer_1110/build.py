from pathlib import Path
import json,math,subprocess,os
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True)
C=640;P=[320,320];FOOT=474;SCALE=.63
SOURCES={r['name']:r for r in json.loads((W/'source-index.json').read_text())if r.get('accepted')}
HEADS={
'impact_blue':[[520,402],[1140,419],[515,1025],[1133,981]],'blue-ready':[[497,429],[1105,384],[486,885],[1083,773]],'blue-wind':[[477,142],[1085,158],[484,775],[1095,742]],'blue-drive-reset':[[450,85],[1137,418],[494,1034],[793,1084]],
'blue-sidewind':[[507,381],[1083,386],[510,807],[1132,759]],'blue-sidecontact2':[[492,142],[805,161],[175,722],[755,718]],'blue-siderecover':[[116,329],[760,347],[536,904],[1117,957]],
'impact_drac':[[517,394],[1145,405],[515,1041],[1145,1004]],'drac-ready':[[525,405],[1145,383],[510,886],[1155,731]],'drac-wind':[[484,134],[1085,119],[500,710],[1085,685]],'drac-drive-reset':[[508,97],[1134,443],[511,1040],[1143,995]],
'drac-sidewind':[[526,379],[1098,402],[516,836],[1175,740]],'drac-sidecontact':[[470,99],[825,143],[166,750],[777,746]],'drac-siderecover':[[164,367],[735,370],[511,996],[1105,1002]]}
CACHE={}
def raw(name,cell):
 key=(name,cell)
 if key in CACHE:return CACHE[key]
 path=Path(SOURCES[name]['file']);path=path if path.is_absolute()else W/path;im=Image.open(path);a=np.array(im);h,w=a.shape[:2];opaque=a[:,:,3]>180
 # Raw generated groups have varying inter-row gaps. Cut in the actual blank
 # gap; never trim a raised hammer at an assumed half-height.
 counts=opaque.sum(axis=1);lo,hi=int(h*.42),int(h*.60);empty=counts[lo:hi]==0
 spans=np.flatnonzero(np.diff(np.r_[False,empty,False]));runs=[(int(spans[i]),int(spans[i+1]))for i in range(0,len(spans),2)]
 split=lo+sum(max(runs,key=lambda r:r[1]-r[0]))//2 if runs else h//2
 xs=[0,w//2,w];ys=[0,split,h];col,row=cell%2,cell//2;x0,x1=xs[col:col+2];y0,y1=ys[row:row+2];z=opaque[y0:y1,x0:x1];yy,xx=np.where(z);assert len(xx),key
 sole=int(yy.max());feet=z[max(0,sole-75):sole+1];fy,fx=np.where(feet);root=[float((fx.min()+fx.max())/2),float(sole)]
 if name.endswith('-empty'):
  centre=[(x0+root[0]),(y0+root[1])-280];out=dict(input=str(path),source=name,sourceCell=cell,crop=[x0,y0,x1-x0,y1-y0],root=root,tip=[centre[0]-x0,centre[1]-y0],headCenter=[centre[0]-x0,centre[1]-y0],grip=[centre[0]-x0,centre[1]-y0],scale=.75 if name.startswith('drac')else SCALE,mirror=False,empty=True);CACHE[key]=out;return out
 sx,sy=HEADS[name][cell];sx*=w/1254;sy*=h/1254
 purple=name.startswith('drac')or name=='impact_drac';rx,ry=(130,155)if purple else(100,110)
 xg,yg=np.meshgrid(np.arange(w),np.arange(h));near=(abs(xg-sx)<rx)&(abs(yg-sy)<ry);r,g,b=[a[:,:,i].astype(float)for i in range(3)]
 hot=opaque&near&((r>150)&(b>180)&(g<b*.75)if purple else(b>180)&(b>r*1.15))
 hy,hx=np.where(hot);assert len(hx)>30,(key,'head not found',sx,sy,len(hx))
 centre=[float(hx.mean()),float(hy.mean())]
 side=('sidecontact'in name)
 if side:tip=[float(np.quantile(hx,.01)-(33 if purple else 7)),centre[1]]
 else:tip=[centre[0],float(np.quantile(hy,.99)+(36 if purple else 4))]
 if side:grip=[centre[0],centre[1]+(145 if purple else 110)]
 else:grip=[centre[0]-(1 if centre[0]>x0+root[0]else-1)*(225 if purple else 185),centre[1]]
 out=dict(input=str(path),source=name,sourceCell=cell,crop=[x0,y0,x1-x0,y1-y0],root=root,tip=[tip[0]-x0,tip[1]-y0],headCenter=[centre[0]-x0,centre[1]-y0],grip=[grip[0]-x0,grip[1]-y0],scale=SCALE,mirror=False)
 CACHE[key]=out;return out
jobs=[]
for unit,prefix,impact,sidecontact in [('blue','blue','impact_blue','blue-sidecontact2'),('drac','drac','impact_drac','drac-sidecontact')]:
 oh=[(prefix+'-ready',i)for i in range(4)]+[(prefix+'-wind',i)for i in range(4)]+[(prefix+'-wind',3),(prefix+'-ready',3)]+[(impact,i)for i in range(4)]+[(prefix+'-drive-reset',2),(prefix+'-ready',0)]
 left=[(prefix+'-ready',0)]+[(prefix+'-sidewind',i)for i in range(1,4)]+[(sidecontact,i)for i in range(4)]+[(sidecontact,3),(prefix+'-siderecover',0)]+[(prefix+'-siderecover',1)]*6
 right=left[:9]+[(prefix+'-siderecover',0),(prefix+'-siderecover',1),(prefix+'-siderecover',2),(prefix+'-siderecover',3)]+[(prefix+'-ready',0)]*3
 for suffix,seq in [('overhead',oh),('sides',left),('right',right)]:
  bank=('blue'if unit=='blue'else'corrupt')+'-'+suffix;frames=[]
  for i,(n,f)in enumerate(seq):
   q=dict(raw(n,f));q['mirror']=suffix=='right'and i<=10;frames.append(q)
  jobs.append(dict(name=bank,unit=unit,frames=frames,cell=C,pivot=P,foot=FOOT))
for name,source in [('blue-empty','blue-empty'),('corrupt-empty','drac-empty')]:
 frames=[dict(raw(source,i//4))for i in range(16)];jobs.append(dict(name=name,unit='blue'if name.startswith('blue')else'drac',frames=frames,cell=C,pivot=P,foot=FOOT))
(W/'jobs.json').write_text(json.dumps(jobs,indent=2))
subprocess.run([os.environ.get('ASEPRITE',r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'),'--batch','--script-param','out='+W.as_posix(),'--script',str(W/'author.lua')],check=True)
M={};audit=[]
for j in jobs:
 n=j['name'];arr=np.asarray(Image.open(E/(n+'_regular.png')));meta=[]
 for i,z in enumerate(j['frames']):
  alpha=arr[i//4*C:(i//4+1)*C,i%4*C:(i%4+1)*C,3];yy,xx=np.where(alpha>96);bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
  assert bounds[0]>0 and bounds[1]>0 and bounds[2]<C and bounds[3]<C,(n,i,bounds)
  def pos(p):
   v=[P[0]+(p[0]-z['root'][0])*z['scale'],FOOT+(p[1]-z['root'][1])*z['scale']]
   if z['mirror']:v[0]=C-1-v[0]
   return v
  row=dict(tip=pos(z['tip']),headCenter=pos(z['headCenter']),grip=pos(z['grip']),bounds=bounds,spans=[np.flatnonzero(np.diff(np.r_[False,v>96,False])).tolist()for v in alpha],depth=1,wholeGenerated=True,source=z['source'],sourceCell=z['sourceCell'])
  meta.append(row);audit.append(dict(bank=n,frame=i,wholeGenerated=True,source=z['source'],cell=z['sourceCell'],mirror=z['mirror'],bounds=bounds))
 M[n]=dict(cell=[C,C],pivot=P,cols=4,count=16,folder='whole_hammer_1110',meta=meta)
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=E/(n+'_'+mat+'.png');Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'audit.json').write_text(json.dumps(dict(passed=True,cells=audit,method='Complete GPT figure/held-weapon drawings only; whole-frame registration, offline whole-frame palettes/flips. No separate body/head/hammer assembly.'),indent=2));print('Exported complete whole-character attack cells',len(audit))
