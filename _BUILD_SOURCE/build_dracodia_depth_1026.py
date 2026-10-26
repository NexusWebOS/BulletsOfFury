"""Normalize one SpriteCook turntable with one scale and shared reference pivot.

Keep the generated source untouched. Use its clean front-to-back half plus the
reflected matching half for a continuous full turn; no per-pose fitting/warping.
"""
from pathlib import Path
from PIL import Image,ImageSequence,ImageFilter,ImageDraw
from scipy.ndimage import label
import json,hashlib,numpy as np

R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/dracodia_depth_1026';O=R/'assets/game/levels/stage_08/boss/dracodia_depth_1026';Q=R/'_shots/dracodia_depth_1026'
O.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
raw=Image.open(S/'turntable-source.webp');source=[f.copy().convert('RGBA')for f in ImageSequence.Iterator(raw)]
assert len(source)==12 and all(f.size==(286,286)for f in source)
def heart(im):
 a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);y,x=np.indices(a.shape[:2]);m=(r>140)&(r>g*1.6)&(r>b*1.4)&(a[:,:,3]>120)&(y>70)&(y<210)
 labs,n=label(m);counts=np.bincount(labs.ravel());counts[0]=0;yy,xx=np.where(labs==counts.argmax());return [float(xx.mean()),float(yy.mean())]
anchor=heart(source[0]);target=[255.52,253.02];offset=[round(target[i]-anchor[i])for i in range(2)]
selection=[(i,False)for i in range(9)]+[(i,True)for i in range(7,0,-1)]
sheet=Image.new('RGBA',(2048,2048));wire=Image.new('RGBA',sheet.size);frames=[];contact=Image.new('RGB',(1280,4*340),(7,12,21));g=ImageDraw.Draw(contact)
for f,(i,flip)in enumerate(selection):
 im=source[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT)if flip else source[i]
 # Mirror around the measured frontal chest axis, not a per-frame crop centre.
 dx=round(2*anchor[0]-(im.width-1))+offset[0] if flip else offset[0]
 c=Image.new('RGBA',(512,512));c.alpha_composite(im,(dx,offset[1]));a=np.array(c);alpha=c.getchannel('A');edge=np.array(alpha).astype(np.int16)>np.array(alpha.filter(ImageFilter.MinFilter(3))).astype(np.int16)+24
 lum=a[:,:,:3].astype(float)@np.array([.2126,.7152,.0722]);crease=np.zeros(lum.shape,dtype=bool)
 for axis in [0,1]:crease|=np.abs(lum-np.roll(lum,1,axis))>65
 ink=(a[:,:,3]>80);out=np.zeros_like(a);out[:,:,:3]=[138,206,255];out[:,:,3]=np.where(edge,195,np.where(crease&ink,115,0))
 cell=Image.fromarray(out);xy=(f%4*512,f//4*512);sheet.alpha_composite(c,xy);wire.alpha_composite(cell,xy)
 frames.append({'cell':[xy[0],xy[1],512,512],'source_frame':i,'mirrored':flip,'pivot':[256,256],'bounds':list(c.getbbox())})
 small=c.resize((320,320),Image.Resampling.NEAREST);contact.paste(small,((f%4)*320,(f//4)*340),small);g.text(((f%4)*320+4,(f//4)*340+321),f'{f}: source{i}'+(' reflected'if flip else''),fill='white')
sheet.save(O/'forming-turntable.webp',lossless=True,method=6);wire.save(O/'forming-wire.webp',lossless=True,method=6);contact.save(Q/'normalized-turntable.jpg')
art={'w':512,'h':512,'logicalSize':320,'pivot':[256,256],'frames':len(frames),'fps':16/1.2,'cells':[f['cell']for f in frames],
 'body':{'key':'rd26_body','path':(O/'forming-turntable.webp').relative_to(R).as_posix()},'wire':{'key':'rd26_wire','path':(O/'forming-wire.webp').relative_to(R).as_posix()}}
(R/'assets/dracodia_depth_art_1026.js').write_text("'use strict';\nconst RD26_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'source_asset_id':'f2f2d956-f64b-444c-8bb3-c495f7b43e74','animation_asset_id':'f6a6647c-3094-4e1d-a634-7c4af5598e80','job_id':'b86c6abb-b05f-4e57-9679-e77e16c59fab',
 'model':'pixel-engine-v1.5','requested_frames':12,'generated_frames':12,'runtime_frames':16,'credits_used':26,'credits_remaining_after_job':4,
 'source':'_BUILD_SOURCE/dracodia_depth_1026/turntable-source.webp','source_sha256':sha(S/'turntable-source.webp'),'reference':'_BUILD_SOURCE/dracodia_depth_1026/native-reference.png','reference_sha256':sha(S/'native-reference.png'),
 'source_chest':anchor,'common_translation':offset,'uniform_scale':1,'normalization':'One fixed512 canvas and shared chest pivot. Source0..8 front-to-back; reflected7..1 forms the opposite half, avoiding the generated late back-to-front jump. No per-frame scale or bounding-box fitting.',
 'frame_details':frames,'art':art,'files':{p.name:sha(p)for p in [O/'forming-turntable.webp',O/'forming-wire.webp']}}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');(S/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
tax=R/'assets/data/ART_TAXONOMY.json';raw=tax.read_bytes()
if 'rd26_'not in json.loads(raw.decode('utf8')):
 entry={'rd26_':{'role':'dracodia_forming_depth_turntable','sheet':None,'owner':'_BUILD_SOURCE/build_dracodia_depth_1026.py','manifest':(O/'manifest.json').relative_to(R).as_posix(),
  'note':'Mike October26: one referenced SpriteCook depth animation;16 selected/reflected upright whole-body views on fixed512 cells, common chest pivot and one proportional scale. Matching source-derived wire. Protected rebirth only; settles into actual native final form before the unchanged whiteout/speech. Native HP, hit feedback and24 lightning beats remain. Runtime dracodia_depth_1026.js separates overhead strikes and front/rear helical lightning.'}}
 block=json.dumps(entry,indent=2,ensure_ascii=False)[1:-2]+','
 if b'\r\n'in raw:block=block.replace('\n','\r\n')
 pos=raw.index(b'{')+1;new=raw[:pos]+block.encode('utf8')+raw[pos:];json.loads(new.decode('utf8'));tax.write_bytes(new)
print(json.dumps({'generated':12,'runtime':16,'sourceChest':anchor,'offset':offset,'frameSize':[512,512],'path':str(O)}),flush=True)
