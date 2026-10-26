"""256px PixelLab authoring canvases, fixed reactor pivot128,116.
The magenta fist registration dot is authoring-only and removed by export.
Final whole plates bake the unchanged native hammer; no runtime body sections.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_motion_1025';S=D/'seeds';S.mkdir(exist_ok=True)
motion={
'regular':[(198,258,90,368),(544,367,406,470),(901,220,730,295),(1251,395,1084,458),(226,709,42,720),(500,774,500,632),(878,853,937,968),(1255,850,1365,818)],
'chrome':[(194,267,70,388),(552,394,392,451),(897,257,727,338),(1230,404,1075,484),(231,744,44,702),(560,788,517,622),(818,823,730,935),(1244,839,1367,862)]}
power={'regular':[(330,225,165,370),(900,225,750,370),(379,814,166,948),(969,814,767,948)],'chrome':[(380,200,520,329),(1007,202,850,338),(382,800,204,930),(1050,740,868,892)]}
meta={}
for mat in ['regular','chrome']:
 for kind,points,k in [('motion',motion[mat],.40),('power',power[mat],.32 if mat=='regular' else .335)]:
  src=Image.open(D/(('keys-' if kind=='motion' else 'power-')+mat+'.png')).convert('RGBA');a=np.array(src);labs,n=label(a[:,:,3]>16);sizes=np.bincount(labs.ravel());sizes[0]=0
  for i,(cx,cy,hx,hy) in enumerate(points):
   id=int(labs[cy,cx]);assert id and sizes[id]>1000,(kind,mat,i);mask=labs==id;yy,xx=np.where(mask);box=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1);keep=binary_dilation(mask,iterations=3)
   q=a[box[1]:box[3],box[0]:box[2]].copy();q[~keep[box[1]:box[3],box[0]:box[2]]]=0;crop=Image.fromarray(q);crop=crop.resize((round(crop.width*k),round(crop.height*k)),Image.Resampling.NEAREST)
   out=Image.new('RGBA',(256,256));at=(round(128+(box[0]-cx)*k),round(116+(box[1]-cy)*k));assert at[0]>=0 and at[1]>=0 and at[0]+crop.width<=256 and at[1]+crop.height<=256,(kind,mat,i,at,crop.size);out.alpha_composite(crop,at)
   hand=[round(128+(hx-cx)*k),round(116+(hy-cy)*k)];flip=kind=='motion' and i==7 or kind=='power' and mat=='chrome' and i==0
   if flip:out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT);hand[0]=255-hand[0]
   clean=out.copy();g=ImageDraw.Draw(out);g.ellipse((hand[0]-2,hand[1]-2,hand[0]+2,hand[1]+2),fill=(255,0,255,255))
   name=f'{kind}_{mat}_{i}';out.save(S/(name+'.png'));clean.save(S/(name+'-clean.png'));meta[name]={'hand':hand,'reactor':[127 if flip else 128,116],'scale':k,'sourceBox':box,'flip':flip}
(D/'seed-manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf8')
sheet=Image.new('RGBA',(256*6,256*4),(17,25,36,255))
for i,n in enumerate(meta):sheet.alpha_composite(Image.open(S/(n+'.png')),(i%6*256,i//6*256))
sheet.save(D/'seed-contact.png');print('Prepared24 fixed256x256 authoring keys; no new weapon pixels.')
