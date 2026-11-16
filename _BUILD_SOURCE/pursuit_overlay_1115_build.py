from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,struct,zlib,json,hashlib,math,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/pursuit_overlay_1115';A=R/'assets/game/shared/ui/pursuit_overlay_1115';O=R/'_shots/pursuit_overlay_1115'
for p in [S,A,O]:p.mkdir(parents=True,exist_ok=True)
TIMES=[62,63]*8
old=(R/'_BUILD_SOURCE/pursuit_trace_1115_build.py').read_text(encoding='utf8');defs=old[old.index('def string('):old.index("M={'version'")].replace('456,256','912,512').replace('Traced frame rim','Interior color wash').replace('Selected green-white pulse','Exact original-frame pulse');exec(compile(defs,'aseprite-source-functions','exec'))
base=json.loads((R/'_ART_SOURCES/pursuit_trace_exact_1115/manifest.json').read_text(encoding='utf8'))
COLORS=base['authorColors'];STRENGTH=[.18,.19,.21,.23,.25,.27,.29,.31,.30,.28,.26,.24,.22,.20,.19,.18]
M={k:v for k,v in base.items()if k!='banks'};M.update({'version':3,'banks':{},'interiorStrength':STRENGTH,'interiorMethod':'Enclosed center component of original metal frame after offline 3px gap closure; exact approved frame pixels retained byte-for-byte.'})
checks=[]
def interior(mask,side):
 wall=np.asarray(mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)))>0
 H,W=wall.shape;outside=np.zeros_like(wall);outside[0,0]=True;stack=[0]
 while stack:
  k=stack.pop();y,x=divmod(k,W)
  for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
   if 0<=xx<W and 0<=yy<H and not wall[yy,xx]and not outside[yy,xx]:outside[yy,xx]=True;stack.append(yy*W+xx)
 holes=(~outside)&(~wall);selected=np.zeros_like(holes);y,x=200,250 if side=='left'else 650;assert holes[y,x];selected[y,x]=True;stack=[y*W+x]
 while stack:
  k=stack.pop();y,x=divmod(k,W)
  for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
   if 0<=xx<W and 0<=yy<H and holes[yy,xx]and not selected[yy,xx]:selected[yy,xx]=True;stack.append(yy*W+xx)
 assert selected.sum()>95000 and not np.any(selected&(np.asarray(mask)>0))
 return selected
for name,B in base['banks'].items():
 diff,side=name.split('-');reference=Image.open(R/('assets/game/shared/cinematics/city_rescue_1115/pursuit-'+diff+'.png')).convert('RGBA');source=np.asarray(reference);mask=Image.open(R/B['mask']);fill=interior(mask,side);fillIm=Image.fromarray(np.uint8(fill)*255);fillIm.save(S/(name+'-interior-mask.png'));mask.save(S/(name+'-frame-mask.png'));reference.save(S/(diff+'-reference.png'))
 border=decode_visible(R/B['source']);layers=[];frames=[]
 for f,color in enumerate(COLORS):
  a=np.zeros_like(source);a[fill,:3]=np.round(source[fill,:3]*(1-STRENGTH[f])+np.array(color)*STRENGTH[f]).astype(np.uint8);a[fill,3]=255;wash=Image.fromarray(a);layers.append((wash,border[f]));frames.append(Image.alpha_composite(wash,border[f]))
 ase=S/(name+'.aseprite');author='--author'in sys.argv or not ase.exists()
 if author:aseprite(ase,reference,layers)
 decoded=decode_visible(ase)
 if author:assert all(a.tobytes()==b.tobytes()for a,b in zip(frames,decoded))
 frames=decoded;framePixels=np.asarray(mask)>0;support=fill|framePixels;Image.fromarray(np.uint8(support)*255).save(S/(name+'-combined-mask.png'))
 for f,im in enumerate(frames):
  pix=np.asarray(im);assert np.array_equal(pix[framePixels],np.asarray(border[f])[framePixels]);assert not np.any((pix[:,:,3]>0)&~support);assert np.all(pix[fill,3]==255)
 l,t,right,bottom=B['crop'];cw,ch=B['w'],B['h'];sheet=Image.new('RGBA',(cw*8,ch*2))
 for f,im in enumerate(frames):sheet.alpha_composite(im.crop((l,t,right,bottom)),(f%8*cw,f//8*ch))
 path=A/(name+'.png');sheet.save(path);assert cw%2==ch%2==l%2==t%2==0 and sheet.width<=4096 and sheet.height<=4096
 M['banks'][name]={**B,'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':str(ase.relative_to(R)).replace('\\','/'),'mask':str((S/(name+'-combined-mask.png')).relative_to(R)).replace('\\','/'),'frameMask':str((S/(name+'-frame-mask.png')).relative_to(R)).replace('\\','/'),'interiorMask':str((S/(name+'-interior-mask.png')).relative_to(R)).replace('\\','/'),'interiorPixels':int(fill.sum())}
 checks.append({'name':name,'frames':16,'approvedFramePixelsIdentical':True,'noPixelsOutsideSelectedCard':True,'opaqueBakedInterior':True,'interiorPixels':int(fill.sum()),'sourceRoundtrip':True,'sourceSha256':hashlib.sha256(ase.read_bytes()).hexdigest()})
 for f in [0,4,7]:
  proof=reference.copy();proof.alpha_composite(frames[f]);proof.save(O/(name+'-phase'+str(f)+'.png'))
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n');(R/'assets/pursuit_trace_art_1115.js').write_text('"use strict";\nconst CITY16_TRACE_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(O/'source-qa.json').write_text(json.dumps({'checks':checks,'scope':'64 retained layered RGBA cels; approved exact border unchanged, same-color interior wash baked into opaque source pixels. No runtime opacity/filter/blend effect. No editor GUI/CLI claim.'},indent=2),encoding='utf8')
print(json.dumps({'frames':64,'interiorPixels':{c['name']:c['interiorPixels']for c in checks}},indent=2))
