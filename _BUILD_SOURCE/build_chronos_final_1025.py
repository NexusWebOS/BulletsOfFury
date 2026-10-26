"""Export corrected whole-body turns and raised chromium activation, fixed448 cells.
Sources: GPT keys + PixelLab motion. No runtime body parts; same common actor
registration and one proportional scale. Head sockets measured on actual pixels.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,numpy as np,ast
from scipy.ndimage import label,distance_transform_edt
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_final_1025';O=R/'assets/game/shared/combat/chronos_motion_1025';P=O/'manifest.json';art=json.loads(P.read_text());WORLD=512/342
# The existing compiler's immutable, canonical held weapon and tracked-fist bake.
s=ast.parse((R/'_BUILD_SOURCE/build_chronos_motion_1025.py').read_text())
for n in s.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['bake','marker']:exec(compile(ast.Module(body=[n],type_ignores=[]),'canonical-bake','exec'))
tool=Image.open(R/'_ART_SOURCES/chronos_motion_1025/refs/hammer-canonical.png').convert('RGBA').resize((342,342),Image.Resampling.NEAREST);wide=Image.new('RGBA',(512,512));wide.alpha_composite(tool,(85,85));tool=wide;GRIP=(256,85+382*342/512);HEAD=(256,256)

def steel(im,chrome=False):
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);lum=rgb@np.array([.2126,.7152,.0722]);warm=(rgb[:,:,0]>rgb[:,:,2]*1.3)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(hi-lo>25)
 if chrome:
  neutral=(hi-lo<35)&(lum>35)&(lum<230);amount=np.where(neutral,.80,0);v=np.minimum(240,lum*1.65+10);target=np.stack([v*.96,v*.99,v],2);rgb=rgb*(1-amount[:,:,None])+target*amount[:,:,None]
 rgb[warm]=np.stack([lum*.94,lum,lum*1.03],2)[warm]
 a[:,:,:3]=np.clip(rgb,0,255).astype('uint8');return Image.fromarray(a)

def red(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);lum=rgb@np.array([.2126,.7152,.0722]);amount=np.where(hi-lo>25,0,.72)*np.clip((245-hi)/65,0,1)*np.clip((lum-12)/30,0,1);target=np.stack([np.minimum(255,np.maximum(hi,lum*1.8)),lum*.22,lum*.28],2);a[:,:,:3]=np.clip(rgb*(1-amount[:,:,None])+target*amount[:,:,None],0,255).astype('uint8');return Image.fromarray(a)

def export(name,frames):
 sheet=Image.new('RGBA',(448*4,448*math.ceil(len(frames)/4)));meta=[]
 for i,(im,m) in enumerate(frames):sheet.alpha_composite(im,(i%4*448,i//4*448));meta.append(m)
 for suffix in ['', '_hit']:
  im=sheet
  if suffix:im=Image.new('RGBA',sheet.size,'white');im.putalpha(sheet.getchannel('A'))
  path=O/(name+suffix+'.webp');im.save(path,lossless=True);art['sheets'][name+suffix]={'key':'nca_c27_'+name+suffix,'path':path.relative_to(R).as_posix()}
 art['banks'][name]={'sheet':'c27_'+name,'count':len(frames),'cols':4,'cell':[448,448],'frames':meta}

# Explicit center estimates only select the real luminous head component. The
# emitted anchor/bounds come from that component, never an abstract hand offset.
expectA=[(25,140),(36,140),(56,140),(75,140),(91,140),(131,140),(165,140),(188,141),(215,141),(225,141),(225,141),(225,141)]
expectB=[(225,141),(214,141),(198,141),(184,143),(171,143),(150,146),(140,146),(111,146),(99,146),(78,144),(59,143),(38,141),(25,141)]
turns={};anchors=[]
for name,expected in [('spin_a',expectA),('spin_b',expectB)]:
 rows=[]
 for i,estimate in enumerate(expected):
  im=Image.open(D/f'frames/{name}/{i:02}.png').convert('RGBA');v=np.array(im);rgb=v[:,:,:3].astype(float);yy,xx=np.indices(v.shape[:2]);mask=(rgb[:,:,2]>150)&(rgb[:,:,1]>80)&(rgb[:,:,2]>rgb[:,:,0]*1.18)&(v[:,:,3]>80)&((xx-estimate[0])**2+(yy-estimate[1])**2<26**2)
  labs,n=label(mask);parts=[]
  for j in range(1,n+1):
   ys,xs=np.where(labs==j)
   if len(xs)>8:parts.append((len(xs),[float(xs.mean()),float(ys.mean())],[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
  assert parts,(name,i);_,point,box=max(parts,key=lambda v:v[0]);k=326/256;offset=[round(224-128*k),round(227-116*k)];base=Image.new('RGBA',(448,448));base.alpha_composite(im.resize((326,326),Image.Resampling.NEAREST),tuple(offset));tip=[(point[j]*k+offset[j])*WORLD for j in [0,1]];bounds=[(box[j]*k+offset[j%2])*WORLD for j in range(4)]
  meta={'tip':tip,'grip':[((point[0]+128)*.5*k+offset[0])*WORLD,(point[1]*k+offset[1])*WORLD],'headBounds':bounds,'bounds':[x*WORLD for x in base.getbbox()],'angle':0,'empty':False}
  rows.append((base,meta));anchors.append({'bank':name,'frame':i,'head':point,'headBox':box})
 turns[name]=rows
spin=turns['spin_a'][:-1]+turns['spin_b'][:-1]
# Side attacks are complete, authored torso/hip turns through a horizontal arc.
# All17 samples retain the fixed source scale and actual weapon head landmarks.
sides={'left':[turns['spin_b'][round(i/16*(len(turns['spin_b'])-1))] for i in range(17)],'right':[turns['spin_a'][round(i/16*(len(turns['spin_a'])-1))] for i in range(17)]}
for mat in ['regular','chrome','red']:
 for bank,rows in [('spin',spin),*sides.items()]:
  processed=[]
  for im,m in rows:
   im=steel(im,mat!='regular');im=red(im) if mat=='red' else im;processed.append((im,m))
  export(bank+'_'+mat,processed)
frames=[]
for i,p in enumerate(sorted((D/'frames/overhead_activation').glob('*.png'))):
 im=steel(Image.open(p).convert('RGBA'));a=np.array(im)
 # Inspectable fist centers for the few energy-occluded markers.
 expected=[(128,59),(126,48),(126,39),(126,36),(124,36),(125,36),(126,36),(122,38),(123,38),(122,39),(122,39),(121,39),(115,43),(114,44),(111,45),(111,44),(110,45),(109,45),(112,51),(111,50),(112,50),(111,50),(111,50),(112,51),(111,50)][i]
 measured,mask=marker(a,expected);hand=list(expected)
 if mask is not None and math.dist(measured,expected)>10:mask=None
 if mask is not None:
  _,idx=distance_transform_edt(mask,return_indices=True);a[mask]=a[idx[0][mask],idx[1][mask]]
 frames.append(bake(Image.fromarray(a),hand,-.4));anchors.append({'bank':'activation','frame':i,'hand':hand,'marker':mask is not None})
export('activation',frames)
art['weapon']['note']='Canonical fixed-scale bitmap baked for overhead/depth/guard/charge. Complete authored GPT-PixelLab turns retain the cylindrical plasma weapon and measured per-pose head sockets. Detached flight uses the unchanged native tool.'
P.write_text(json.dumps(art,indent=2)+'\n',encoding='utf8');(R/'assets/chronos_motion_art_1025.js').write_text('"use strict";\nconst C27_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'anchors.json').write_text(json.dumps(anchors,indent=2)+'\n')
preview=Image.new('RGBA',(448*5,472*3),(20,30,42,255));draw=ImageDraw.Draw(preview)
for j,(label_,row) in enumerate([(f'spin {i}',spin[i]) for i in [0,5,10,16,22]]+[(f'activation {i}',frames[i]) for i in [0,4,8,12,16,20,24]]):
 x=j%5*448;y=j//5*472;preview.alpha_composite(row[0],(x,y+24));draw.text((x+12,y+6),label_,fill='white')
preview.save(R/'_shots/chronos_final_1025/final-plates.png');print('Exported3 whole-body material variants, left/right sweeps, overhead activation')

# Mike's original HAMMER/HAMA two-handed spin is the final authority. Keep the
# newer one-handed candidate archived in its source pack, never activate it.
import runpy
runpy.run_path(str(R/'_BUILD_SOURCE/restore_chronos_original_spin_1025.py'))

runpy.run_path(str(R/'_BUILD_SOURCE/restore_chronos_twohand_attacks_1025.py'))

runpy.run_path(str(R/'_BUILD_SOURCE/clean_chronos_chromium_1025.py'))
