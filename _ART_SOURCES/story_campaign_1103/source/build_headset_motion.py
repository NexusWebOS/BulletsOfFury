"""Export the generated headset drawings on a fixed native pixel grid."""
from pathlib import Path
import json,hashlib,shutil,math,argparse
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent
args=argparse.ArgumentParser();args.add_argument('--out',type=Path,default=W.parent if (W.parent/'overlay').is_dir() else W.parent/'outputs/BOF-Cutscenes-1103');args.add_argument('--sources',type=Path,default=W/'headset_motion_sources.json');args.add_argument('--revision',type=int,default=7);args=args.parse_args();D=args.out.resolve()
O=D/'overlay';A=O/'assets/game/shared/cinematics/story_1103'
S=D/'source-art/headset_motion_1103';S.mkdir(exist_ok=True)
V=D/('verification/revision'+str(args.revision));V.mkdir(exist_ok=True)
manifest=A/'manifest.json';M=json.loads(manifest.read_text());banks=M['banks']
baseline=V/'before-assets.json'
if not baseline.exists():baseline.write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in A.glob('*.webp')},indent=2))
sources={k:(Path(v)if Path(v).is_absolute()else args.sources.parent/v).resolve()for k,v in json.loads(args.sources.read_text()).items()}
shutil.copy2(W/'headset_motion_prompt.txt',S/'generation-contract.txt')
poses=['front-neutral','front-talk-small','front-talk-wide','front-talk-round','left-quarter','left-quarter-talk','left-profile','left-profile-talk','right-quarter','right-quarter-talk','right-profile','right-profile-talk','happy','happy-talk','sad','sad-talk','angry','angry-talk','scared','scared-talk','surprised','surprised-talk','determined','determined-talk']
clips={'front-talk':{'frames':[0,1,2,1,3,1],'ms':100},'turn-left':{'frames':[10,8,0,4,6,6,4,0,8,10],'ms':150},'turn-right':{'frames':[6,4,0,8,10,10,8,0,4,6],'ms':150},'left-talk':{'frames':[4,5,4,5],'ms':130},'right-talk':{'frames':[8,9,8,9],'ms':130},'left-profile-talk':{'frames':[6,7,6,7],'ms':130},'right-profile-talk':{'frames':[10,11,10,11],'ms':130},**{e:{'frames':[i,i+1,i,i+1],'ms':180}for e,i in [('happy',12),('sad',14),('angry',16),('scared',18),('surprised',20),('determined',22)]}}
def put(name,frames,cols,pivot):
 w,h=frames[0].size;assert w%2==h%2==0
 sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for i,im in enumerate(frames):assert im.size==(w,h);sheet.alpha_composite(im,(i%cols*w,i//cols*h))
 path=A/(name+'.webp');sheet.save(path,lossless=True,method=4)
 banks[name]={'key':'s113_'+name,'path':path.relative_to(O).as_posix(),'w':w,'h':h,'cols':cols,'frames':len(frames),'pivot':pivot}
native={};provenance=[];facts=[]
for p,path in sources.items():
 folder=S/p;folder.mkdir(exist_ok=True);master=folder/'master.png'
 if path.resolve()!=master.resolve():shutil.copy2(path,master)
 raw=Image.open(master).convert('RGBA');assert raw.width%4==0 and raw.height%6==0 and raw.width//4==raw.height//6,(p,raw.size)
 cell=raw.width//4;frames=[];alignment=[]
 for i in range(24):
  im=raw.crop((i%4*cell,i//4*cell,(i%4+1)*cell,(i//4+1)*cell)).resize((128,128),Image.Resampling.NEAREST)
  a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0
  im=Image.fromarray(a);box=im.getchannel('A').getbbox();assert box and box[3]>=120,(p,i,box)
  # Translation only: generated frame scale remains one common 1/cell factor.
  dy=125-box[3];assert abs(dy)<=8,(p,i,dy)
  fixed=Image.new('RGBA',(128,128));fixed.alpha_composite(im,(0,dy));frames.append(fixed);alignment.append({'frame':i,'dy':dy,'source_bounds':box})
 sheet=Image.new('RGBA',(512,768))
 for i,im in enumerate(frames):sheet.alpha_composite(im,(i%4*128,i//4*128))
 alpha=sheet.getchannel('A')
 if p=='cole':
  # Retain the reference's small blue iris clusters in the shared palette.
  # Median-cut alone otherwise merges these rare authored pixels into skin.
  rgb=np.array(sheet.convert('RGB'));wide=rgb.astype(int)
  blue=(wide[:,:,2]>wide[:,:,0]+18)&(wide[:,:,2]>wide[:,:,1]+5)&(wide[:,:,2]>95)&(np.array(alpha)>0)
  assert np.count_nonzero(blue)>30,'Cole reference blue eyes must survive export'
  iris=Image.fromarray(rgb[blue].reshape(-1,1,3)).quantize(colors=2,dither=Image.Dither.NONE)
  irgb=np.array(iris.convert('RGB')).reshape(-1,3);palette=np.unique(irgb,axis=0)
  normal=rgb.copy();normal[blue]=0
  mapped=np.array(Image.fromarray(normal).quantize(colors=30,dither=Image.Dither.NONE).convert('RGB'))
  closest=((rgb[blue,None,:].astype(int)-palette[None,:,:].astype(int))**2).sum(axis=2).argmin(axis=1);mapped[blue]=palette[closest]
  sheet=Image.fromarray(mapped).convert('RGBA')
 else:sheet=sheet.convert('RGB').quantize(colors=32,dither=Image.Dither.NONE).convert('RGBA')
 sheet.putalpha(alpha)
 sheet.save(folder/'frames.png');frames=[]
 for i in range(24):
  im=sheet.crop((i%4*128,i//4*128,(i%4+1)*128,(i//4+1)*128));im.save(folder/(str(i).zfill(2)+'-'+poses[i]+'.png'));frames.append(im)
 native[p]=frames;put('headset-'+p,frames,4,[64,124]);put('headset-panel-'+p,[im.resize((384,384),Image.Resampling.NEAREST)for im in frames],4,[192,372])
 arrays=[np.array(im)for im in frames];counts=[int(np.count_nonzero(a[:,:,3]))for a in arrays]
 assert min(counts)>4000 and max(counts)<16000,(p,counts)
 pairs=[]
 for x,y in [(0,1),(0,2),(0,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15),(16,17),(18,19),(20,21),(22,23)]:
  n=int(np.count_nonzero(np.any(arrays[x]!=arrays[y],axis=2)));pairs.append({'frames':[x,y],'different_pixels':n});assert n>8,(p,x,y,n)
 pal=int(len(np.unique(np.concatenate([a[a[:,:,3]>0,:3]for a in arrays]),axis=0)))
 assert pal<=32
 facts.append({'pilot':p,'source_size':raw.size,'native':[128,128],'frames':24,'palette':pal,'bounds':[im.getchannel('A').getbbox()for im in frames],'alignment':alignment,'mouth_pairs':pairs})
 provenance.append({'pilot':p,'source':master.relative_to(D).as_posix(),'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'tool':'built-in image_gen','normalization':'one proportional source-grid scale, binary alpha, shared 32-color palette; translation to chest baseline only'})
# Existing authored gray divider/footer, retained at exactly its current position.
divider=Image.open(D/'source-art/comic-divider.png').convert('RGBA')
k=min(912/divider.width,512/divider.height);divider=divider.resize((round(divider.width*k),round(divider.height*k)),Image.Resampling.NEAREST)
plate=Image.new('RGBA',(912,512));plate.alpha_composite(divider,((912-divider.width)//2,(512-divider.height)//2))
alpha=np.array(plate.getchannel('A'));footer=np.where((alpha>128).sum(axis=1)>800)[0];assert len(footer)
border=Image.new('RGBA',(912,512));border.alpha_composite(plate,(0,392-int(footer[0])))
put('comic-backdrop',[Image.new('RGBA',(912,512),(0,0,0,255))],1,[456,256]);put('comic-border',[border],1,[456,256])
motion={'version':1,'native':[128,128],'panel':[384,384],'pivot':[64,124],'poses':poses,'clips':clips,'source_art':provenance}
if (S/'identity-locks.json').exists():motion['identityOverrides']=json.loads((S/'identity-locks.json').read_text())
M['headsetMotion']=motion;manifest.write_text(json.dumps(M,indent=2))
(O/'assets/story_campaign_art_1103.js').write_text("'use strict';\nconst S113_ART="+json.dumps({'banks':banks,'pilots':M['pilots'],'actorPoses':M['actorPoses'],'headsetMotion':motion},separators=(',',':'))+';\n')
(S/'manifest.json').write_text(json.dumps(motion,indent=2));(S/'provenance.json').write_text(json.dumps(provenance,indent=2));(V/('headset-art-report.json'if args.revision>=7 else'art-report.json')).write_text(json.dumps({'headsets':facts,'banks':len(banks),'frames':sum(a['frames']for a in banks.values())},indent=2))
# Native contact sheet and frame-only motion preview; no game artwork is drawn here.
font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',17)
board=Image.new('RGB',(1136,9*152),'#15151c');draw=ImageDraw.Draw(board)
for row,p in enumerate(sources):
 draw.text((8,row*152+55),p.upper(),font=font,fill='white')
 for col,f in enumerate([0,6,10,12,14,16,18,20]):board.paste(native[p][f],(112+col*128,row*152+12),native[p][f])
board.save(D/'Headset-frames.png')
sequence=[0,1,2,1,3,0,4,6,4,0,8,10,8,0,12,13,12,13,14,15,14,15,16,17,16,17,18,19,18,19,20,21,20,21,22,23,22,23]
gif=[]
for f in sequence:
 im=Image.new('RGB',(864,960),'#15151c');dr=ImageDraw.Draw(im)
 for i,p in enumerate(sources):
  sprite=native[p][f].resize((256,256),Image.Resampling.NEAREST);x=i%3*288+16;y=i//3*320+8;im.paste(sprite,(x,y),sprite);dr.text((x,y+274),p.upper(),font=font,fill='white')
 gif.append(im)
gif[0].save(D/'Headset-Animation.gif',save_all=True,append_images=gif[1:],duration=160,loop=0,optimize=False,disposal=2)
print(json.dumps({'pilots':len(native),'authored_native_frames':len(native)*24,'banks':len(banks),'total_frames':sum(a['frames']for a in banks.values())}))
