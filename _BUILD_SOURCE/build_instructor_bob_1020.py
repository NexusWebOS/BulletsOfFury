from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,shutil,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/instructor_bob_1020'
D=R/'assets/game/levels/tutorial/stormglass_1020/instructor_bob';P=R/'assets/game/pilots/cole/portraits/instructor_1020';Q=R/'_shots/instructor_bob_1020'
for p in [D,P,Q]:p.mkdir(exist_ok=True,parents=True)
art={'portraits':[],'parts':{},'views':{}}
def save(im,path,key,pivot):
 im=im.convert('RGBA');assert im.width%2==im.height%2==0;im.save(path,lossless=True,method=6)
 return dict(key=key,path=path.relative_to(R).as_posix(),w=im.width,h=im.height,pivot=pivot,bounds=list(im.getbbox() or [0,0,0,0]))
src=Image.open(A/'returned/instructor-portraits.png').convert('RGBA');assert src.size==(1254,1254)
palette_src=Image.open(A/'palette_black_red_1020/generated-frame-reference.png').convert('RGB').resize((256,256),Image.Resampling.NEAREST)
pr=np.array(palette_src);yy,xx=np.indices((256,256));rim=(xx<19)|(xx>236)|(yy<19)|(yy>236)
colors=np.array(Image.fromarray(pr[rim].reshape(-1,1,3)).quantize(colors=24).convert('RGB')).reshape(-1,3)
colors=np.unique(colors,axis=0).astype(int);lum=colors.mean(1)
gray=colors[(colors.max(1)-colors.min(1)<36)&(lum<150)];gray=gray[np.argsort(gray.mean(1))]
red=colors[(colors[:,0]>colors[:,1]*1.7)&(colors[:,0]>colors[:,2]*1.7)&(colors[:,0]>100)];red=red[np.argsort(red.mean(1))]
assert len(gray)>=3 and len(red)>=3
palette_audit=[]
for i,name in enumerate(['neutral','talk-small','talk-open','smile']):
 # Same627-square source cell, same shared1px padding to628, one256/628 scale.
 cell=src.crop((i%2*627,i//2*627,i%2*627+627,i//2*627+627));padded=Image.new('RGBA',(628,628));padded.paste(cell,(0,0))
 im=padded.resize((256,256),Image.Resampling.NEAREST);ar=np.array(im);old=ar.copy();rgb=ar[:,:,:3].astype(int);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 frame=(xx<24)|(xx>=234)|(yy<24)|(yy>=234)|(((xx<46)|(xx>211))&((yy<46)|(yy>211)))
 mask=frame&(g>r*1.25)&(g>b*1.25)&(g-r>12);lights=mask&(g>155);metal=mask&~lights
 ar[metal,:3]=gray[np.minimum(len(gray)-1,(g[metal]/155*(len(gray)-1)).astype(int))]
 ar[lights,:3]=red[np.minimum(len(red)-1,((g[lights]-155)/100*(len(red)-1)).astype(int))]
 assert np.array_equal(ar[25:233,48:210],old[25:233,48:210]),'Instructor likeness must remain pixel-identical'
 assert np.array_equal(ar[:,:,3],old[:,:,3])
 palette_audit.append(dict(pose=name,changed=int(mask.sum()),face_unchanged=True,alpha_unchanged=True))
 art['portraits'].append(save(Image.fromarray(ar),P/(name+'-black-red.webp'),'ic20_'+name,[128,128]))
(A/'palette_black_red_1020/export-audit.json').write_text(json.dumps(dict(palettes=dict(metal=gray.tolist(),lights=red.tolist()),portraits=palette_audit),indent=2),encoding='utf-8')
geo=json.loads((A/'parts/geometry.json').read_text(encoding='utf-8'))
for name in ['core','missile','cannon']:
 d=D/name;d.mkdir(exist_ok=True)
 a=save(Image.open(A/'parts'/(name+'-live.png')),d/'live.webp','bob20_'+name,[128,128]);a.update(target=geo[name]['target'],muzzle={'core':[128,183],'missile':[46,184],'cannon':[209,207]}[name]);art['parts'][name]=a
art['whole']=save(Image.open(A/'returned/bob.png'),D/'whole.webp','bob20_whole',[128,128])
card=Image.open(R/'expansion/topdown/art/boss_intro_1011/od_warrior_card.png').convert('RGBA');art['card']=save(card,D/'dossier-card.webp','ic20_dossier_card',[card.width//2,card.height//2])
pending=[]
for name in ['whole','core','missile','cannon']:
 paths=sorted((A/'returned'/('turn_'+name)).glob('frame_*.png'))
 if len(paths)==33:paths=paths[1:]
 if not paths:
  candidate=A/'returned'/('view_'+name)/'frame_000.png'
  if not candidate.exists():pending.append(name);continue
  paths=[candidate];pending.append(name)
 frames=[Image.open(p).convert('RGBA') for p in paths];w,h=frames[0].size;assert all(im.size==(w,h) for im in frames)
 assert w%2==h%2==0
 pad=2;strideW=w+4;strideH=h+4;cols=min(6,len(frames));rows=math.ceil(len(frames)/cols);atlas=Image.new('RGBA',(cols*strideW,rows*strideH));cells=[]
 for i,im in enumerate(frames):
  x=i%cols*strideW+pad;y=i//cols*strideH+pad;atlas.paste(im,(x,y));cells.append([x,y,w,h])
  for j in [1,2]:
   atlas.paste(im.crop((0,0,1,h)),(x-j,y));atlas.paste(im.crop((w-1,0,w,h)),(x+w-1+j,y));atlas.paste(im.crop((0,0,w,1)),(x,y-j));atlas.paste(im.crop((0,h-1,w,h)),(x,y+h-1+j))
 d=D/name;d.mkdir(exist_ok=True)
 a=save(atlas,d/('turntable-'+str(len(frames))+'.webp'),'bob20_turn_'+name,[w//2,h//2]);a.update(cell_width=w,cell_height=h,cells=cells,frames=len(frames),fps=10);art['views'][name]=a
 preview=[]
 for im in frames:
  bg=Image.new('RGBA',im.size,'#071322');bg.alpha_composite(im);preview.append(bg.convert('RGB'))
 preview[0].save(Q/('turn-'+name+'.gif'),save_all=True,append_images=preview[1:],duration=100,loop=0,optimize=False)
 contact=Image.new('RGB',(8*128,4*144),'#071322');g=ImageDraw.Draw(contact)
 for i,im in enumerate(preview):
  x=i%8*128;y=i//8*144;contact.paste(im.resize((128,128),Image.Resampling.NEAREST),(x,y));g.text((x+4,y+130),str(i),fill='white')
 contact.save(Q/('turn-'+name+'-all.png'))
art['pending_turntables']=pending
(D/'manifest.json').write_text(json.dumps(art,indent=2),encoding='utf-8')
(R/'assets/instructor_bob_art_1020.js').write_text("'use strict';\n/* Generated with the cells by build_instructor_bob_1020.py. */\nconst IC20_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'portraits':len(art['portraits']),'parts':list(art['parts']),'views':{n:a['frames'] for n,a in art['views'].items()},'pending':pending}))
