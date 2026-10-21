from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/performance_finish_1020';O=R/'_shots/performance_finish_1020';O.mkdir(exist_ok=True,parents=True)
names=['carrier_turret','bomber_cannon','laser_terminal','dark_terminal','ice_shatter','cole_report_face','cole_horror_face','cole_report_gesture','cole_horror_gesture'];art={'banks':{},'audit':{},'pending':[]}
base_dir=R/'assets/game/pilots/cole/body_frames/performance_1020';base_dir.mkdir(parents=True,exist_ok=True)
for pose in ['report','horror']:
 im=Image.open(A/f'refs/cole-{pose}-original.png').convert('RGBA');ar=np.array(im);r,g,b=ar[:,:,0].astype(int),ar[:,:,1].astype(int),ar[:,:,2].astype(int)
 # Confirmed red matte debris to the right of the legs; no skin, uniform or head pixels.
 yy,xx=np.indices(ar.shape[:2]);debris=(yy>550)&(xx>390)&(r>20)&(r<110)&(r>4*g)&(b<20)
 ar[debris|(ar[:,:,3]<=8),3]=0;Image.fromarray(ar).save(base_dir/f'cole_{pose}_base.webp',lossless=True,method=6)
for name in names:
 paths=sorted((A/'returned'/name).glob('*.png'))
 count=24 if name.endswith('gesture') else 16
 if len(paths)!=count+1:art['pending'].append(name);continue
 frames=[Image.open(p).convert('RGBA') for p in paths[1:]];w,h=frames[0].size;assert w%2==h%2==0;assert all(im.size==(w,h) for im in frames)
 # Reuse clean physical recoil poses; the live beam/muzzle remains with its collision owner.
 if name=='carrier_turret':frames=[frames[i].copy() for i in [0,1,2,3,4,5,6,7,11,12,13,12,13,14,15,0]]
 if name=='bomber_cannon':frames=[frames[i].copy() for i in [0,1,2,3,4,5,6,7,12,13,14,12,13,14,15,0]]
 if name in ['laser_terminal','ice_shatter']:
  for im in frames:
   ar=np.array(im);rgb=ar[:,:,:3].astype(int);neutral=(rgb.max(2)-rgb.min(2)<26)&(rgb.mean(2)>30)&(rgb.mean(2)<205);ar[neutral,3]=0;im.paste(Image.fromarray(ar))
 if name.startswith('cole_') and name.endswith('face'):
  # Only eyelids/lips can change: hair, nose, jaw, beard outline remain exact source pixels.
  rects=[(50,88,86,110),(98,88,134,110),(64,123,122,148)]
  mask=Image.new('L',(w,h));g=ImageDraw.Draw(mask)
  for x0,y0,x1,y1 in rects:g.rectangle((x0,y0,x1-1,y1-1),fill=255)
  for im in frames:im.putalpha(Image.composite(im.getchannel('A'),Image.new('L',im.size),mask))
 if name.startswith('cole_') and name.endswith('gesture'):
  # Preserve original full-res head and legs. Animated region is a common upper-body band.
  mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rectangle((0,84,w-1,239),fill=255)
  for im in frames:im.putalpha(Image.composite(im.getchannel('A'),Image.new('L',im.size),mask))
  pose='horror' if 'horror' in name else 'report';seed=Image.open(A/f'returned/{name}/000.png').convert('RGBA')
  # Match the unchanged shoulder/waist at the two common band boundaries.
  for im in frames:
   for y in list(range(84,92))+list(range(232,240)):
    weight=min((y-84)/8,(239-y)/8,1);row=Image.blend(seed.crop((0,y,w,y+1)),im.crop((0,y,w,y+1)),max(0,weight));im.paste(row,(0,y))
 if name=='carrier_turret':pivot=[80,76]
 elif name=='bomber_cannon':pivot=[52,120]
 else:pivot=[w//2,h//2]
 if name.startswith('cole_'):D=R/'assets/game/pilots/cole/body_frames/performance_1020'
 elif name=='carrier_turret':D=R/'assets/game/levels/stage_06/boss/performance_1020'
 elif name=='bomber_cannon':D=R/'assets/game/levels/stage_05/miniboss/performance_1020'
 else:D=R/'assets/game/shared/player_fx/terminal_1020'
 D.mkdir(exist_ok=True,parents=True);pad=2;cw=w+4;ch=h+4;cols=min(4,count);rows=math.ceil(count/cols);sheet=Image.new('RGBA',(cols*cw,rows*ch));cells=[]
 for i,im in enumerate(frames):
  x=i%cols*cw+2;y=i//cols*ch+2;sheet.paste(im,(x,y));cells.append([x,y,w,h])
  for q in [1,2]:
   sheet.paste(im.crop((0,0,1,h)),(x-q,y));sheet.paste(im.crop((w-1,0,w,h)),(x+w-1+q,y));sheet.paste(im.crop((0,0,w,1)),(x,y-q));sheet.paste(im.crop((0,h-1,w,h)),(x,y+h-1+q))
 p=D/(name+'.webp');sheet.save(p,lossless=True,method=6)
 art['banks'][name]=dict(key='pf20_'+name,path=p.relative_to(R).as_posix(),w=w,h=h,pivot=pivot,cells=cells,frames=count,fps=12)
 hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames];boxes=[im.getbbox() for im in frames]
 art['audit'][name]=dict(size=[w,h],frames=count,unique=len(set(hashes)),bounds=boxes,bytes=p.stat().st_size,source_paths=[str(p.relative_to(R)) for p in paths])
 previews=[]
 for im in frames:
  bg=Image.new('RGBA',im.size,'#111a26');bg.alpha_composite(im);previews.append(bg.convert('RGB'))
 previews[0].save(O/(name+'.gif'),save_all=True,append_images=previews[1:],duration=83,loop=0,optimize=False)
 thumb=160;contact=Image.new('RGB',(8*thumb,math.ceil(count/8)*(thumb+20)),'#111a26');dr=ImageDraw.Draw(contact)
 for i,im in enumerate(previews):
  k=min(thumb/im.width,thumb/im.height);small=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);x=i%8*thumb;y=i//8*(thumb+20);contact.paste(small,(x+(thumb-small.width)//2,y));dr.text((x+4,y+thumb+2),str(i),fill='white')
 contact.save(O/(name+'-all.png'))
(A/'export-manifest.json').write_text(json.dumps(art,indent=2),encoding='utf-8')
(R/'assets/performance_finish_art_1020.js').write_text("'use strict';\nconst PF20_ART="+json.dumps(art['banks'],separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'banks':{n:a['frames'] for n,a in art['banks'].items()},'pending':art['pending']}))
