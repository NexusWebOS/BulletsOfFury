"""Own PixelLab exports; never edit prior PNGs. Run from this repo's _research."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,zipfile,io,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'expansion/topdown';OUT=BASE/'art/pixel25';SOURCE=OUT/'source';FRAMES=OUT/'frames'
SOURCE.mkdir(parents=True,exist_ok=True);FRAMES.mkdir(exist_ok=True)
# Rebuild from the retained raw source by default. Optional initial import is explicit.
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--input-dir',type=Path);args=parser.parse_args()
if args.input_dir:
 INPUT=args.input_dir
 for p in (INPUT/'downloaded').glob('*.zip'):shutil.copy2(p,SOURCE/p.name)
 for p in (INPUT/'downloaded').glob('*.png'):
  if p.stem in ['wall','floor','ceiling','rearwall','door','door_open','brick','server','concrete','hud']:shutil.copy2(p,SOURCE/p.name)
 shutil.copy2(INPUT/'receipts.json',SOURCE/'receipts.json')
assets={};sequences={};audit=[]
def save(key,im,anchor,**extra):
 im=im.convert('RGBA');assert not im.width%2 and not im.height%2,(key,im.size)
 # Binary alpha keeps authored edges exact; do not touch RGB or inner lights.
 im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));q=im.getbbox();assert q,key
 file=FRAMES/(key+'.png');im.save(file)
 assets[key]={'file':file.relative_to(ROOT).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(q),'drawScale':1,**extra}
 return key
def alias(key,source):assets[key]=dict(assets[source])
def tile(im,w,h):
 cv=Image.new('RGBA',(w,h))
 for y in range(0,h,im.height):
  for x in range(0,w,im.width):cv.alpha_composite(im,(x,y))
 return cv
for name in ['wall','floor','ceiling','rearwall','door','door_open','brick','server','concrete']:
 p=SOURCE/(name+'.png');assert p.exists(),name
 save('px25_'+name,Image.open(p),(64,64),tile=name in ['wall','floor','ceiling','rearwall','brick','concrete'])
for name in ['wall','floor','ceiling','rearwall']:alias('grid21_'+name,'px25_'+name)
doorPlate=tile(Image.open(SOURCE/'rearwall.png').convert('RGBA'),128,184);doorPlate.alpha_composite(Image.open(SOURCE/'door.png').convert('RGBA'),(0,56));save('px25_door_plate',doorPlate,(64,92));alias('grid21_door_0','px25_door_plate')
# Preserve the actual frame geometry of the established UI; stretch only empty centers.
old={}
for pack in ['bastion19','bastion20']:
 s=(BASE/'art'/pack/'manifest.js').read_text(encoding='utf-8');old.update(json.JSONDecoder().raw_decode(s[s.index('{'):])[0]['assets'])
hud=Image.open(SOURCE/'hud.png').convert('RGBA')
def nine(im,size,l=28,r=28,t=6,b=6):
 q=im.getbbox();im=im.crop(q);w,h=im.size;tw,th=size;out=Image.new('RGBA',size)
 xs=[0,l,w-r,w];ys=[0,t,h-b,h];dx=[0,l,tw-r,tw];dy=[0,t,th-b,th]
 for j in range(3):
  for i in range(3):
   part=im.crop((xs[i],ys[j],xs[i+1],ys[j+1])).resize((dx[i+1]-dx[i],dy[j+1]-dy[j]),Image.Resampling.NEAREST);out.alpha_composite(part,(dx[i],dy[j]))
 return out
for role,box in [('top',(0,0,512,60)),('bottom',(0,232,512,288)),('boss',(110,58,400,106)),('dialogue',(94,108,418,224))]:
 key='pb20_hud_'+role;m=old[key];im=nine(hud.crop(box),tuple(m['size']));save('px25_hud_'+role,im,m['anchor']);alias(key,'px25_hud_'+role)
# Tile components into the existing top-down fortress footprint. Keep collision/layout unchanged.
floor=Image.open(SOURCE/'floor.png').convert('RGBA');concrete=Image.open(SOURCE/'concrete.png').convert('RGBA');wall=Image.open(SOURCE/'wall.png').convert('RGBA');brick=Image.open(SOURCE/'brick.png').convert('RGBA');rear=Image.open(SOURCE/'rearwall.png').convert('RGBA');server=Image.open(SOURCE/'server.png').convert('RGBA')
world=tile(floor,800,2400);world.alpha_composite(tile(concrete,800,640),(0,1760))
for x in [0,732]:world.alpha_composite(tile(wall,68,1760),(x,0));world.alpha_composite(tile(brick,68,640),(x,1760))
world.alpha_composite(tile(rear,664,76),(68,0))
for x in [68,635]:
 world.alpha_composite(tile(wall,97,474),(x,76))
 for y in [88,216,344]:world.alpha_composite(server.crop((16,0,112,128)),(x,y))
save('px25_fortress_ground',world,(0,0));alias('od_fortress_ground','px25_fortress_ground')
for state in ['door','door_open']:
 im=Image.open(SOURCE/(state+'.png')).convert('RGBA');box=im.getbbox();body=im.crop(box);scale=2.55;body=body.resize((round(body.width*scale),round(body.height*scale)),Image.Resampling.NEAREST);cv=Image.new('RGBA',(384,384));cv.alpha_composite(body,((384-body.width)//2,308-body.height));save('px25_fortress_'+state,cv,(192,320));alias('od_cover_'+state,'px25_fortress_'+state)
units={'rifle':1.20,'heavy':1.40,'rocket':1.20,'laser':1.30}
# South source gun sockets. Recoil stays registered around this same physical root.
muzzles={'rifle':(85,65),'heavy':(92,83),'rocket':(37,51),'laser':(91,68)}
for kind,display in units.items():
 z=zipfile.ZipFile(SOURCE/(kind+'.zip'));data=json.loads(z.read('metadata.json'))['states'][0]['frames'];rotations=data['rotations'];anims=data['animations'];bases={}
 for direction,path in rotations.items():
  im=Image.open(io.BytesIO(z.read(path))).convert('RGBA');q=im.getbbox();root=(im.width//2,q[3]);bases[direction]=(im,root)
  canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(128-root[0],224-root[1]));key=save('px25_'+kind+'_idle_'+direction,canvas,(128,224),drawScale=display,role=kind,action='idle',direction=direction)
  sequences['px25_'+kind+'_idle_'+direction]={'frames':[key],'fps':8,'loop':True}
 for name,dirs in anims.items():
  raw_action=name.removeprefix('bof25_')
  if kind=='heavy' and raw_action=='recoil_v3':dirs={**dirs,'east':dirs['west']} # Mirror the clean authored recoil, not the clipped baked effect.
  for direction,paths in dirs.items():
   if kind in ['heavy','laser','rocket'] and raw_action=='fire':continue # Rejected oversized / clipped effects.
   if raw_action=='fire_clean' and (kind in ['laser','rocket'] or (kind=='heavy' and direction in ['west','east'])):continue
   action='fire' if raw_action in ['fire_clean','recoil_v3'] else raw_action
   mirror=kind=='heavy' and raw_action=='recoil_v3' and direction=='east'
   def source_image(path):
    im=Image.open(io.BytesIO(z.read(path))).convert('RGBA');return im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if mirror else im
   ref=source_image(paths[0]);base,root=bases['west' if mirror else direction];base=base.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if mirror else base;qb=base.getbbox();qr=ref.getbbox();offset=(qr[0]-qb[0],qr[1]-qb[1]);bankroot=(root[0]+offset[0],root[1]+offset[1]);shift=(128-bankroot[0],224-bankroot[1]);keys=[];loop=action in ['walk','strafe'];chosen=paths[1:] if loop else paths
   for i,path in enumerate(chosen):
    im=source_image(path);source_bounds=im.getbbox();assert source_bounds and source_bounds[0]>0 and source_bounds[1]>0 and source_bounds[2]<im.width and source_bounds[3]<im.height,(kind,action,direction,i,'source clipping',source_bounds);assert im.size==ref.size,(kind,action,direction,im.size,ref.size);cv=Image.new('RGBA',(256,256));cv.alpha_composite(im,shift);q=cv.getbbox();assert q and q[0]>1 and q[1]>1 and q[2]<255 and q[3]<255,(kind,action,direction,i,q)
    mx,my=muzzles[kind]
    if direction=='north':mx,my=64,48
    elif direction=='east':mx,my=105,70
    elif direction=='west':mx,my=24,70
    muzzle=[128+mx-base.width//2,224+my-root[1]]
    hit=[qb[0]+128-root[0],qb[1]+224-root[1],qb[2]+128-root[0],qb[3]+224-root[1]]
    key=save(f'px25_{kind}_{action}_{direction}_{i}',cv,(128,224),drawScale=display,role=kind,action=action,direction=direction,muzzle=muzzle,hitBounds=hit,vaultLiftBaked=action=='vault');keys.append(key)
   sequences[f'px25_{kind}_{action}_{direction}']={'frames':keys,'fps':16 if action in ['walk','strafe','fire'] else 15,'loop':loop}
   audit.append({'kind':kind,'action':action,'direction':direction,'sourceAnimation':name,'mirrored':mirror,'sourceSize':list(ref.size),'sourceRoot':list(bankroot),'shift':list(shift),'frames':len(keys),'exportSize':[256,256],'exportRoot':[128,224]})
pack={'assets':assets,'sequences':sequences,'audit':audit,'service':'PixelLab','build':'overdrive1014-pixel25-r1'}
(OUT/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n');(OUT/'manifest.js').write_text('window.TD_PIXEL25_ART='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(OUT/'source/hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.iterdir() if p.is_file() and p.name!="hashes.json"},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'assets':len(assets),'banks':len(sequences),'frames':sum(len(q['frames']) for q in sequences.values()),'animations':audit},indent=2))
