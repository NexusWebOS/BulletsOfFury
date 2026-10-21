"""Package the four authored PixelLab arenas, matching meshes and scan curtain."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/arena_download_1020'
D=R/'assets/game/levels/stage_08/boss/arena_download_1020';Q=R/'_shots/arena_download_1020'
for p in [D,Q]:p.mkdir(exist_ok=True,parents=True)
art={'arenas':{}};audit={'arenas':{},'bytes':0}
contact=Image.new('RGB',(1024,512),'#05050b');g=ImageDraw.Draw(contact)
for i,name in enumerate(['jungle','lava','space','sky']):
 art['arenas'][name]={}
 for kind,prefix in [('terrain',''),('wire','wire_')]:
  src=A/'returned'/(prefix+name)/'frame_000.png';im=Image.open(src).convert('RGBA');assert im.size==(512,512)
  target=D/name/(kind+'.webp');target.parent.mkdir(exist_ok=True);im.save(target,lossless=True,method=6)
  key='ad20_'+name+'_'+kind
  art['arenas'][name][kind]={'key':key,'path':target.relative_to(R).as_posix(),'w':512,'h':512,'pivot':[256,256]}
  alpha=np.array(im.getchannel('A'));audit['arenas'][name+'_'+kind]={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'size':list(im.size),'transparent_fraction':float((alpha<32).mean()),'bytes':target.stat().st_size}
  tile=Image.new('RGBA',im.size,'#0b0a18');tile.alpha_composite(im);contact.paste(tile.convert('RGB').resize((256,256),Image.Resampling.NEAREST),(i*256,0 if kind=='terrain' else 256))
  audit['bytes']+=target.stat().st_size
contact.save(Q/'arena-and-mesh.png')
paths=sorted((A/'returned/curtain').glob('frame_*.png'))
pending=not paths
if pending:paths=[A/'returned/fx/frame_000.png']
elif len(paths)==33:paths=paths[1:] # separate input0,32 genuine generated phases
assert len(paths) in [1,32],len(paths)
frames=[Image.open(p).convert('RGBA') for p in paths];assert all(im.size==(256,256) for im in frames)
# Common256 canvas and128pivot. Transparent padding is shared, never fit per pose.
W=H=256;PAD=2;stride=260;cols=6 if len(frames)>1 else 1;rows=math.ceil(len(frames)/cols)
atlas=Image.new('RGBA',(cols*stride,rows*stride));cells=[]
for i,im in enumerate(frames):
 x=i%cols*stride+PAD;y=i//cols*stride+PAD;atlas.paste(im,(x,y));cells.append([x,y,W,H])
 for j in [1,2]:
  atlas.paste(im.crop((0,0,1,H)),(x-j,y));atlas.paste(im.crop((W-1,0,W,H)),(x+W-1+j,y));atlas.paste(im.crop((0,0,W,1)),(x,y-j));atlas.paste(im.crop((0,H-1,W,H)),(x,y+H-1+j))
 for dx in [-2,-1,W,W+1]:
  for dy in [-2,-1,H,H+1]:atlas.putpixel((x+dx,y+dy),im.getpixel((0 if dx<0 else W-1,0 if dy<0 else H-1)))
target=D/('download-curtain-seed.webp' if pending else 'download-curtain-32.webp');atlas.save(target,lossless=True,method=6)
art['curtain']={'key':'ad20_download_curtain','path':target.relative_to(R).as_posix(),'w':W,'h':H,'pivot':[128,128],'frames':len(frames),'fps':20,'columns':cols,'cells':cells,'sheet_width':atlas.width,'sheet_height':atlas.height,'pending_animation':pending}
(D/'manifest.json').write_text(json.dumps(art,indent=2),encoding='utf-8')
reg="'use strict';\n/* Built with all delivered plates/cells by build_arena_download_1020.py. */\nconst AD20_ART="+json.dumps(art,separators=(',',':'))+";\n"
(R/'assets/arena_download_art_1020.js').write_text(reg,encoding='utf-8',newline='\n')
preview=[]
for im in frames:
 bg=Image.new('RGBA',(256,256),'#080713');bg.alpha_composite(im);preview.append(bg.convert('RGB'))
preview[0].save(Q/'download-curtain.gif',save_all=True,append_images=preview[1:],duration=50,loop=0,optimize=False)
contact=Image.new('RGB',(8*128,4*144),'#080713');labels=ImageDraw.Draw(contact)
for i,im in enumerate(preview):
 x=i%8*128;y=i//8*144;contact.paste(im.resize((128,128),Image.Resampling.NEAREST),(x,y));labels.text((x+4,y+130),str(i),fill='white')
contact.save(Q/'curtain-all-frames.png')
audit.update(curtain_frames=len(frames),curtain_unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames}),pending_animation=pending,curtain_sheet=list(atlas.size),runtime_bytes=audit['bytes']+target.stat().st_size+len(reg.encode()))
audit['curtain_alpha_bounds']=[list(im.getbbox() or (0,0,0,0)) for im in frames]
(A/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');print(json.dumps(audit))
