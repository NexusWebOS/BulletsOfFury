"""Export generated pixel divider and flat-color scrolling panel frames."""
from pathlib import Path
import argparse,json,math,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent
cli=argparse.ArgumentParser();cli.add_argument('--out',type=Path,default=W.parent if (W.parent/'overlay').is_dir() else W.parent/'outputs/BOF-Cutscenes-1103');cli.add_argument('--sources',type=Path,default=W/'comic_scroll_sources.json');cli.add_argument('--revision',type=int,default=7);args=cli.parse_args();D=args.out.resolve()
O=D/'overlay';A=O/'assets/game/shared/cinematics/story_1103';S=D/'source-art/comic_scroll_1103';S.mkdir(exist_ok=True);V=D/('verification/revision'+str(args.revision));V.mkdir(exist_ok=True)
baseline=V/'before-assets.json'
if not baseline.exists():baseline.write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in A.glob('*.webp')},indent=2))
sources={k:(Path(v)if Path(v).is_absolute()else args.sources.parent/v).resolve()for k,v in json.loads(args.sources.read_text()).items()}
provenance=[]
for name,path in sources.items():
 dest=S/(name+'-master.png')
 if path.resolve()!=dest.resolve():shutil.copy2(path,dest)
 provenance.append({'name':name,'source':dest.relative_to(D).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'tool':'built-in image_gen'})
M=json.loads((A/'manifest.json').read_text());banks=M['banks']
def put(name,frames,cols,pivot):
 w,h=frames[0].size;assert w%2==h%2==0
 sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for i,im in enumerate(frames):assert im.size==(w,h);sheet.alpha_composite(im,(i%cols*w,i//cols*h))
 path=A/(name+'.webp');sheet.save(path,lossless=True,method=4)
 banks[name]={'key':'s113_'+name,'path':path.relative_to(O).as_posix(),'w':w,'h':h,'cols':cols,'frames':len(frames),'pivot':pivot}
# Normalize the generated divider once onto a common 228 x 128 console grid.
im=Image.open(S/'divider-master.png').convert('RGBA');k=min(228/im.width,128/im.height);im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
plate=Image.new('RGBA',(228,128));plate.alpha_composite(im,((228-im.width)//2,(128-im.height)//2));a=np.array(plate)
a[:,:,3]=np.where(a[:,:,3]>=128,255,0);v=a[:,:,:3].mean(axis=2);levels=np.array([24,44,92,148,204]);gray=levels[np.abs(v[:,:,None]-levels).argmin(axis=2)].astype('uint8');a[:,:,:3]=gray[:,:,None];a[a[:,:,3]==0,:3]=0
rows=np.where((a[:,:,3]>0).sum(axis=1)>215)[0];assert len(rows)>0,'Divider needs a full horizontal footer'
dy=98-int(rows[0]);assert abs(dy)<=5,(rows.tolist(),dy)
plate=Image.new('RGBA',(228,128));plate.alpha_composite(Image.fromarray(a),(0,dy));a=np.array(plate)
for y in range(max(0,dy)):a[y]=a[max(0,dy)]
for y in range(98,128):
 xx=np.where(a[y,:,3]>0)[0]
 if len(xx)>215:a[y,:xx[0]]=a[y,xx[0]];a[y,xx[-1]+1:]=a[y,xx[-1]]
centers=[]
for y in range(98):
 xx=np.where(a[y,:,3]>0)[0];assert 5<=len(xx)<=24,(y,len(xx));centers.append(int(round(float(np.median(xx)))))
plate=Image.fromarray(a);plate.save(S/'divider-native.png');put('comic-border',[plate.resize((912,512),Image.Resampling.NEAREST)],1,[456,256])
palettes={'yellow':[(214,173,44),(242,206,86)],'blue':[(25,62,152),(43,95,192)],'red':[(169,45,57),(211,76,85)],'black':[(13,22,26),(51,94,48)],'white':[(228,223,226),(207,140,174)],'purple':[(80,49,120),(119,83,162)],'orange':[(191,101,45),(226,150,78)],'brown':[(116,82,61),(155,120,88)],'gold':[(177,139,57),(218,192,102)]}
pilot_colors={'cole':'brown','axel':'blue','decker':'gold','maverick':'black','freezer':'purple','juggernaut':'orange','yuri':'red','lizzie':'yellow','falva':'white'}
raw=Image.open(S/'tiles-master.png').convert('RGB');tiles={};tilefacts=[]
colorsheet=Image.new('RGB',(192,192));mask_left=np.indices((98,228))[1]<=np.array(centers)[:,None]
for i,(name,palette)in enumerate(palettes.items()):
 box=(round(i%3*raw.width/3),round(i//3*raw.height/3),round((i%3+1)*raw.width/3),round((i//3+1)*raw.height/3))
 im=raw.crop(box).resize((64,64),Image.Resampling.NEAREST).quantize(colors=2,dither=Image.Dither.NONE)
 labels=np.array(im);values,counts=np.unique(labels,return_counts=True);base=int(values[counts.argmax()]);fraction=float(counts.max()/4096);assert fraction>.78,(name,fraction)
 pixels=np.empty((64,64,3),dtype='uint8');pixels[labels==base]=palette[0];pixels[labels!=base]=palette[1];tiles[name]=pixels
 tile=Image.fromarray(pixels);tile.save(S/(name+'.png'));colorsheet.paste(tile,(i%3*64,i//3*64));tilefacts.append({'color':name,'palette':palette,'solid_base_fraction':fraction,'native':[64,64]})
colorsheet.save(S/'color-tiles.png')
native_frames={}
for pilot,color in pilot_colors.items():
 contact='cole'if pilot=='decker'else'decker';lc=pilot_colors[contact];frames=[];small=[]
 for phase in range(16):
  left=np.roll(tiles[lc],phase*4,axis=1);right=np.roll(tiles[color],-phase*4,axis=1)
  left=np.tile(left,(2,4,1))[:98,:228];right=np.tile(right,(2,4,1))[:98,:228]
  pixels=np.where(mask_left[:,:,None],left,right);im=Image.fromarray(pixels).convert('RGBA');small.append(im);frames.append(im.resize((912,392),Image.Resampling.NEAREST))
 native_frames[pilot]=small;put('comic-scroll-'+pilot,frames,4,[456,196])
config={'version':1,'fps':8,'phases':16,'native_grid':[228,128],'tile':[64,64],'step':4,'footer':392,'colors':pilot_colors,'palettes':palettes,'tile_facts':tilefacts,'native_divider_centers':centers,'directions':{'left':'right','right':'left'},'provenance':provenance}
M['comicScroll']=config;(A/'manifest.json').write_text(json.dumps(M,indent=2))
(O/'assets/story_campaign_art_1103.js').write_text("'use strict';\nconst S113_ART="+json.dumps({'banks':banks,'pilots':M['pilots'],'actorPoses':M['actorPoses'],'headsetMotion':M['headsetMotion'],'comicScroll':config},separators=(',',':'))+';\n')
(S/'manifest.json').write_text(json.dumps(config,indent=2));(S/'provenance.json').write_text(json.dumps(provenance,indent=2))
before=json.loads(baseline.read_text());changed=[p.stem for p in A.glob('*.webp')if p.name in before and hashlib.sha256(p.read_bytes()).hexdigest()!=before[p.name]];assert set(changed).issubset({'headset-cole','headset-panel-cole','headset-maverick','headset-panel-maverick','comic-scroll-cole','comic-scroll-maverick','comic-scroll-decker','comic-cole','comic-maverick','comic-decker'} )if args.revision>=7 else changed==['comic-border'],changed
(V/('scroll-art-report.json'if args.revision>=7 else'art-report.json')).write_text(json.dumps({'changed_prior_banks':changed,'unchanged_prior_banks':len(before)-len(changed),'new_banks':len(banks)-len(before),'banks':len(banks),'frames':sum(a['frames']for a in banks.values()),'config':config},indent=2))
font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',18);board=Image.new('RGB',(912,3*216),'#10141a');dr=ImageDraw.Draw(board)
for i,p in enumerate(pilot_colors):
 im=Image.new('RGBA',(912,512),'black');im.alpha_composite(native_frames[p][0].resize((912,392),Image.Resampling.NEAREST));contact='cole'if p=='decker'else'decker'
 for person,f,x in [(contact,8,214),(p,4,698)]:
  a=banks['headset-panel-'+person];sheet=Image.open(O/a['path']).convert('RGBA');sprite=sheet.crop((f%a['cols']*a['w'],f//a['cols']*a['h'],f%a['cols']*a['w']+a['w'],f//a['cols']*a['h']+a['h']));im.alpha_composite(sprite,(x-a['pivot'][0],398-a['pivot'][1]))
 im.alpha_composite(plate.resize((912,512),Image.Resampling.NEAREST));im=im.convert('RGB').resize((304,171),Image.Resampling.NEAREST);x=i%3*304;y=i//3*216;board.paste(im,(x,y));dr.text((x+10,y+190),p.upper()+' / '+pilot_colors[p].upper(),font=font,fill='white')
board.save(D/'Comic-color-panels.png')
print(json.dumps({'banks':len(banks),'total_frames':sum(a['frames']for a in banks.values()),'updated_prior_banks':changed,'unchanged_prior_banks':len(before)-len(changed),'colors':pilot_colors}))
