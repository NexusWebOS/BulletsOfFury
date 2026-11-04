"""Bake BOF intro-referenced pixel shading and color sweeps into fixed frames."""
from pathlib import Path
import argparse,json,hashlib,shutil,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent
cli=argparse.ArgumentParser();cli.add_argument('--out',type=Path,default=W.parent if (W.parent/'overlay').is_dir() else W.parent/'outputs/BOF-Cutscenes-1103');cli.add_argument('--sources',type=Path,default=W/'neogeo_panels_sources.json');args=cli.parse_args();D=args.out.resolve()
O=D/'overlay';A=O/'assets/game/shared/cinematics/story_1103';S=D/'source-art/neogeo_panels_1103';S.mkdir(exist_ok=True);V=D/'verification/revision8';V.mkdir(exist_ok=True)
baseline=V/'before-assets.json'
if not baseline.exists():baseline.write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in A.glob('*.webp')},indent=2))
source=json.loads(args.sources.read_text())['master'];source=Path(source)if Path(source).is_absolute()else args.sources.parent/source
master=S/'master.png'
if source.resolve()!=master.resolve():shutil.copy2(source,master)
M=json.loads((A/'manifest.json').read_text());B=M['banks'];old=M['comicScroll'];colors=old['colors'];centers=old['native_divider_centers'];mask=np.indices((98,228))[1]<=np.array(centers)[:,None]
names=['yellow','blue','red','black','white','purple','orange','brown','gold'];raw=Image.open(master).convert('RGB');tiles={};palettes={};facts=[]
sheet=Image.new('RGB',(288,288))
for i,name in enumerate(names):
 # Inset removes provider cell separators; all tiles use one proportional scale.
 box=(round(i%3*raw.width/3)+3,round(i//3*raw.height/3)+3,round((i%3+1)*raw.width/3)-3,round((i//3+1)*raw.height/3)-3)
 im=raw.crop(box).resize((96,96),Image.Resampling.NEAREST).quantize(colors=16,dither=Image.Dither.NONE)
 rgb=np.array(im.convert('RGB'));unique,counts=np.unique(rgb.reshape(-1,3),axis=0,return_counts=True)
 order=np.argsort(unique.astype(float)@np.array([.2126,.7152,.0722]));palette=unique[order];assert len(palette)>=12,(name,len(palette))
 rank={tuple(c):j for j,c in enumerate(palette)};indices=np.array([rank[tuple(c)]for c in rgb.reshape(-1,3)],dtype='uint8').reshape(96,96)
 # Mirror repeat joins equal edge pixels, keeping the source highlight continuous.
 indices=np.pad(indices,((1,1),(0,0)),mode='edge');period=np.concatenate([indices,indices[:,::-1]],axis=1)
 tiles[name]=period;palettes[name]=palette.tolist();np.save(S/(name+'-indices.npy'),period)
 Image.fromarray(rgb).save(S/(name+'.png'));sheet.paste(Image.fromarray(rgb),(i%3*96,i//3*96))
 lum=palette.astype(float)@np.array([.2126,.7152,.0722]);facts.append({'color':name,'shades':len(palette),'luminance_min':float(lum.min()),'luminance_max':float(lum.max()),'native':[96,96],'period':192})
sheet.save(S/'color-shading-tiles.png')
phases=24;fps=12;step=8;pulse=[0,0,1,1,1,0,0,0,-1,-1,-1,0]*2
native_frames={}
def put(name,frames,cols,pivot):
 w,h=frames[0].size;assert w%2==h%2==0
 canvas=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for i,f in enumerate(frames):assert f.size==(w,h);canvas.alpha_composite(f,(i%cols*w,i//cols*h))
 path=A/(name+'.webp');canvas.save(path,lossless=True,method=4);B[name]={'key':'s113_'+name,'path':path.relative_to(O).as_posix(),'w':w,'h':h,'cols':cols,'frames':len(frames),'pivot':pivot}
for pilot,theme in colors.items():
 contact='cole'if pilot=='decker'else'decker';left_theme=colors[contact];frames=[];native=[]
 for f in range(phases):
  left=np.roll(tiles[left_theme],f*step,axis=1);right=np.roll(tiles[theme],-f*step,axis=1)
  left=np.tile(left,(1,2))[:,:228];right=np.tile(right,(1,2))[:,:228]
  lp=np.array(palettes[left_theme],dtype='uint8');rp=np.array(palettes[theme],dtype='uint8')
  left=lp[np.clip(left.astype(int)+pulse[f],0,len(lp)-1)];right=rp[np.clip(right.astype(int)+pulse[(f+6)%phases],0,len(rp)-1)]
  rgb=np.where(mask[:,:,None],left,right);im=Image.fromarray(rgb).convert('RGBA');native.append(im);frames.append(im.resize((912,392),Image.Resampling.NEAREST))
 native_frames[pilot]=native;put('comic-scroll-'+pilot,frames,4,[456,196])
# Stored fallback images use the same finished live composition.
def blit(dst,name,f,x,y):
 a=B[name];im=Image.open(O/a['path']).convert('RGBA');im=im.crop((f%a['cols']*a['w'],f//a['cols']*a['h'],f%a['cols']*a['w']+a['w'],f//a['cols']*a['h']+a['h']));dst.alpha_composite(im,(x-a['pivot'][0],y-a['pivot'][1]))
preview={}
for p in colors:
 im=Image.new('RGBA',(912,512),'black');im.alpha_composite(native_frames[p][0].resize((912,392),Image.Resampling.NEAREST));contact='cole'if p=='decker'else'decker';blit(im,'headset-panel-'+contact,8,214,398);blit(im,'headset-panel-'+p,4,698,398);blit(im,'comic-border',0,456,256);preview[p]=im;put('comic-'+p,[im],1,[456,256])
config={'version':2,'style':'Neo-Geo pilot-intro color and shading','fps':fps,'phases':phases,'native_grid':[228,128],'tile':[96,96],'period':192,'step':step,'pulse':pulse,'footer':392,'colors':colors,'palettes':palettes,'tile_facts':facts,'native_divider_centers':centers,'directions':{'left':'right','right':'left'},'source':master.relative_to(D).as_posix(),'source_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'reference':'Existing BOF pilot-intro plates and opener spotlight / stepped shade bands'}
M['comicScroll']=config;(A/'manifest.json').write_text(json.dumps(M,indent=2));(O/'assets/story_campaign_art_1103.js').write_text("'use strict';\nconst S113_ART="+json.dumps({'banks':B,'pilots':M['pilots'],'actorPoses':M['actorPoses'],'headsetMotion':M['headsetMotion'],'comicScroll':config},separators=(',',':'))+';\n');(S/'manifest.json').write_text(json.dumps(config,indent=2))
before=json.loads(baseline.read_text());changed=[p.stem for p in A.glob('*.webp')if p.name in before and hashlib.sha256(p.read_bytes()).hexdigest()!=before[p.name]];expected={prefix+p for prefix in ['comic-scroll-','comic-']for p in colors};assert set(changed)==expected,changed
(V/'art-report.json').write_text(json.dumps({'changed_banks':changed,'unchanged_banks':len(before)-len(changed),'banks':len(B),'frames':sum(a['frames']for a in B.values()),'config':config},indent=2))
board=Image.new('RGB',(912,648),'#10141a');dr=ImageDraw.Draw(board);font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',18)
for i,p in enumerate(colors):
 x=i%3*304;y=i//3*216;board.paste(preview[p].convert('RGB').resize((304,171),Image.Resampling.NEAREST),(x,y));dr.text((x+8,y+190),p.upper()+' / '+colors[p].upper(),font=font,fill='white')
board.save(D/'Comic-color-panels.png');preview['cole'].save(D/'NeoGeo-panels-preview.png')
print(json.dumps({'themes':len(colors),'shades_per_theme':[f['shades']for f in facts],'phases':phases,'fps':fps,'changed_banks':len(changed),'unchanged_banks':len(before)-len(changed),'total_frames':sum(a['frames']for a in B.values())}))
