"""GPT whole-plate banks. Resolution chosen:576x576 RGBA, common288,328 pivot.
Source strips padded to even canvases; no segmented anatomy or per-frame scaling.
Shared bank scale, explicitly measured chest pivots and hammer-head landmarks.
"""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/chronos_frames_1025';D=R/'assets/game/shared/combat/chronos_frames_1025';D.mkdir(exist_ok=True)
# Each pair is (torso reactor/source center, physical hammer-head/source center).
points={
'activation_regular':[(250,278,142,85),(676,280,578,84),(1121,278,1015,85),(1557,278,1453,85),(251,692,149,510),(677,692,580,510),(1119,694,1018,510),(1553,694,1457,510)],
'spin_regular':[(330,218,79,232),(775,218,585,284),(1172,218,970,278),(1485,220,1697,267),(169,615,451,627),(645,613,817,536),(1185,619,998,548),(1570,620,1410,570)],
'spin_chrome':[(355,210,83,185),(787,211,580,220),(1190,227,985,259),(1488,220,1706,233),(198,612,498,595),(699,608,840,540),(1180,614,997,517),(1570,620,1662,521)],
'jump_regular':[(308,340,133,444),(766,273,589,80),(1165,248,999,92),(1535,262,1703,442),(328,700,150,790),(780,630,618,573),(1187,659,1003,584),(1570,605,1429,736)],
'jump_chrome':[(276,303,126,435),(673,264,777,70),(1027,218,1212,128),(1532,225,1685,420),(222,699,107,794),(738,633,642,550),(1175,603,1261,638),(1584,614,1418,719)],
'shield_regular':[(252,265,101,394),(649,261,783,117),(1090,260,1161,82),(1544,266,1550,65),(232,674,206,503),(650,675,639,500),(1100,674,1076,500),(1530,671,1514,502)],
'shield_chrome':[(274,234,171,370),(708,238,590,144),(1138,258,990,112),(1519,258,1474,61),(244,674,177,498),(684,670,620,502),(1100,671,1054,499),(1527,673,1485,498)],
'unfold':[(226,290,226,290),(643,257,643,257),(1109,244,956,351),(1542,193,1406,366),(226,705,226,705),(640,659,640,659),(1106,665,950,757),(1540,600,1410,780)]}
scales={'spin':.78,'jump':.78,'shield':.86,'unfold':.62,'activation':.86}
art={'resolution':[576,576],'pivot':[288,328],'banks':{},'sheets':{},'sources':{}}
contacts=[]
for source,pts in points.items():
 im=Image.open(S/('activation.png' if source=='activation_regular' else source+'.png')).convert('RGBA');src=np.array(im);labs,n=label(src[:,:,3]>16);sizes=np.bincount(labs.ravel());sizes[0]=0
 kind=source.split('_')[0];k=scales[kind];frames=[];rows=[]
 for i,(cx,cy,tx,ty) in enumerate(pts):
  # A complete connected plate, including the held hammer, is moved as one.
  id=int(labs[cy,cx]);
  if not id or sizes[id]<1000:
   yy,xx=np.indices(labs.shape);near=(xx-cx)**2+(yy-cy)**2;near[sizes[labs]<1000]=10**9;id=int(labs.flat[int(near.argmin())])
  mask=labs==id
  if source=='shield_chrome' and i in [2,6]:
   yy=np.indices(mask.shape)[0];mask&=(yy<448 if i==2 else yy>=448)
  yy,xx=np.where(mask);box=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1)
  # Preserve small authored energy pixels around the connected silhouette.
  keep=binary_dilation(mask,iterations=3);a=src[box[1]:box[3],box[0]:box[2]].copy();a[~keep[box[1]:box[3],box[0]:box[2]]]=0
  crop=Image.fromarray(a);out=Image.new('RGBA',(576,576));crop=crop.resize((round(crop.width*k),round(crop.height*k)),Image.Resampling.NEAREST)
  offset=(round(288+(box[0]-cx)*k),round(288+(box[1]-cy)*k));assert offset[0]>=0 and offset[1]>=0 and offset[0]+crop.width<=576 and offset[1]+crop.height<=576,(source,i,offset,crop.size)
  out.alpha_composite(crop,offset);frames.append(out)
  rows.append({'tip':[round(288+(tx-cx)*k),round(288+(ty-cy)*k)],'bounds':list(out.getbbox()),'sourceBounds':list(box),'sourcePivot':[cx,cy],'sourceTip':[tx,ty]})
 groups=[(source,frames,rows)] if source!='unfold' else [('unfold_regular',frames[:4],rows[:4]),('unfold_chrome',frames[4:],rows[4:])]
 for bank,fs,rs in groups:
  sheet=Image.new('RGBA',(2304,576*((len(fs)+3)//4)))
  for f,cell in enumerate(fs):sheet.alpha_composite(cell,(f%4*576,f//4*576))
  for suffix in ['', '_hit']:
   result=sheet
   if suffix:result=Image.new('RGBA',sheet.size,'white');result.putalpha(sheet.getchannel('A'))
   path=D/(bank+suffix+'.webp');result.save(path,lossless=True);art['sheets'][bank+suffix]={'key':'nca_c26_'+bank+suffix,'path':path.relative_to(R).as_posix()}
  art['banks'][bank]={'sheet':'c26_'+bank,'count':len(fs),'cols':4,'w':576,'h':576,'pivot':[288,328],'scale':k,'frames':rs}
  contacts.extend(fs)
 art['sources'][source]={'path':(S/('activation.png' if source=='activation_regular' else source+'.png')).relative_to(R).as_posix(),'sha256':hashlib.sha256((S/('activation.png' if source=='activation_regular' else source+'.png')).read_bytes()).hexdigest(),'canvas':[1774,888],'padding':[0,0,0,1]}
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf8',newline='\n')
(R/'assets/chronos_frames_art_1025.js').write_text('"use strict";\nconst C26_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
contact=Image.new('RGBA',(1024,256*((len(contacts)+3)//4)),(25,27,38,255))
for i,im in enumerate(contacts):contact.alpha_composite(im.resize((256,256),Image.Resampling.NEAREST),(i%4*256,i//4*256))
contact.save(R/'_shots/chronos_frames_1025/banks.png');print('Registered',len(contacts),'whole GPT frames')

import runpy
runpy.run_path(str(R/'_BUILD_SOURCE/build_chronos_rage_ball_1025.py'))
