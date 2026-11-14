from pathlib import Path
from PIL import Image,ImageSequence,ImageDraw
import json,shutil,hashlib,numpy as np
PACK=Path(__file__).resolve().parents[1]
GAME=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
pilots=['cole','decker','axel','freezer','yuri','falva','lizzie','maverick','juggernaut']
mouths={'cole':[76,85,19,18],'decker':[76,83,18,16],'axel':[74,88,21,19],'freezer':[65,98,21,20],'yuri':[74,91,20,19],'falva':[77,88,19,17],'lizzie':[74,88,20,18],'maverick':[77,87,20,19],'juggernaut':[74,84,22,20]}
editor=PACK/'source/editor-input';editor.mkdir(exist_ok=True);jobs=[]
for pk in pilots:
 folder=editor/pk;folder.mkdir(exist_ok=True)
 native=Image.open(GAME/f'assets/game/shared/cinematics/story_1103/headset-{pk}.webp').convert('RGBA').crop((0,0,128,128));native.save(folder/'native.png')
 im=Image.open(PACK/'masters'/(pk+'-vowels.gif'));frames=[];at=0
 for f in ImageSequence.Iterator(im):
  duration=f.info.get('duration',100);frames.append((at,at+duration,f.convert('RGBA').copy()));at+=duration
 paths=[]
 for label,t in [('closed',at-10),('a',350),('e',550),('o',750),('u',950),('f',1150),('l',1350)]:
  frame=next(f for start,end,f in frames if start<=t<end);p=folder/(label+'.png');frame.save(p);paths.append(str(p))
 demo=PACK/'portraits'/(pk+'-talking.gif');raw=PACK/'masters'/(pk+'-demo-original.gif')
 if not raw.exists():shutil.copy2(demo,raw)
 rawim=Image.open(raw);demoFrames=[]
 for i,f in enumerate(ImageSequence.Iterator(rawim)):
  p=folder/f'demo-{i:02}.png';f.convert('RGBA').save(p);demoFrames.append(dict(path=str(p),ms=f.info.get('duration',90)))
 out=PACK/'portraits'/pk;out.mkdir(exist_ok=True)
 jobs.append(dict(pilot=pk,native=str(folder/'native.png'),poses=paths,mouth=mouths[pk],demo=demoFrames,output=str(out),gif=str(demo),aseprite=str(PACK/'portraits'/(pk+'.aseprite'))))
(PACK/'source/portrait-editor-jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')

# Inspect the generated page's actual apertures; retain native source pixels.
raw=Image.open(PACK/'masters/comic-page-kit.png').convert('RGBA');W=raw.width//2;H=raw.height//2;pages=[]
def components(binary):
 h,w=binary.shape;seen=np.zeros(binary.shape,dtype=bool);result=[]
 for sy,sx in zip(*np.where(binary)):
  if seen[sy,sx]:continue
  todo=[(int(sx),int(sy))];seen[sy,sx]=True;points=[]
  while todo:
   x,y=todo.pop();points.append((x,y))
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    nx,ny=x+dx,y+dy
    if 0<=nx<w and 0<=ny<h and binary[ny,nx]and not seen[ny,nx]:seen[ny,nx]=True;todo.append((nx,ny))
  if len(points)>800:
   xs,ys=zip(*points);result.append(dict(points=points,box=[min(xs),min(ys),max(xs)-min(xs)+1,max(ys)-min(ys)+1],area=len(points)))
 return result
for i in range(4):
 page=Image.new('RGBA',(W+W%2,H+H%2));page.paste(raw.crop((i%2*W,i//2*H,(i%2+1)*W,(i//2+1)*H)),(0,0));p=editor/f'page-{i}.png';page.save(p)
 a=np.asarray(page).astype(np.int16);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
 navy=(r<45)&(g<64)&(b<90)&(b>r+4)&(b>=21)&(g>=10)
 regions=components(navy);holes=[c for c in regions if c['box'][1]<100 and c['box'][3]>150 and c['area']>20000];holes.sort(key=lambda c:c['box'][0])
 assert len(holes)==[2,2,1,2][i],(i,[(c['box'],c['area'])for c in regions])
 mask=Image.new('RGB',page.size);draw=ImageDraw.Draw(mask)
 for c in holes:
  for x,y in c['points']:mask.putpixel((x,y),(255,255,255))
 maskPath=editor/f'page-{i}-mask.png';mask.save(maskPath)
 lower=[c for c in regions if c['box'][1]>300 and c['area']>15000];body=max(lower,key=lambda c:c['area'])['box']if lower else[35,365,770,70]
 gold=(r>145)&(g>95)&(g<210)&(b<125)&(r>g*1.1)
 tabs=[c for c in components(gold)if 300<c['box'][1]<390 and c['area']>1500];name=max(tabs,key=lambda c:c['area'])['box']if tabs else[35,332,205,22]
 pages.append(dict(id=i,input=str(p),mask=str(maskPath),w=page.width,h=page.height,panels=[c['box']for c in holes],body=body,name=name))
(PACK/'source/page-editor-jobs.json').write_text(json.dumps(pages,indent=2),encoding='utf8')
print(json.dumps(dict(portraits=len(jobs),pages=[{k:v for k,v in p.items()if k in ['id','w','h','panels','body','name']}for p in pages])))
