from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,re
from scipy.ndimage import distance_transform_edt,binary_dilation
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True)
O=W if W.parent.name=='_ART_SOURCES' else W.parents[1]/'outputs/chronus-core-loop';O.mkdir(parents=True,exist_ok=True)
runtime=R/'assets/hammer_finale_1017.js';before=(W/'before.js').read_bytes() if (W/'before.js').exists() else runtime.read_bytes();(C/'before.js').write_bytes(before);code=before.decode()
S=R/'_ART_SOURCES/hammer_finale_1017';src=Image.open(S/'references/stunned.png').convert('RGBA');a=np.array(src);rgb=a[:,:,:3].astype(float)
r,g,b=rgb.transpose(2,0,1);blue=(a[:,:,3]>200)&(b>75)&(b>r*1.16)&(b>g*1.05)
Y,X=np.mgrid[:256,:256];core=(X>=116)&(X<=139)&(Y>=134)&(Y<=157)
blue|=core&(a[:,:,3]>0)&(b>95)&(b>r*1.03)
hot=(a[:,:,3]>200)&(rgb.min(2)>190)&binary_dilation(blue,iterations=2)
mask=blue|hot;dist,idx=distance_transform_edt(~mask,return_indices=True);near=rgb[idx[0],idx[1]]
steps=[0,.16,.32,.52,.74,.95];glow=np.zeros_like(rgb);glow[mask]=rgb[mask]*.48
for lo,hi,amount in [(0,1,.28),(1,2,.15),(2,3,.07)]:
 edge=(dist>lo)&(dist<=hi)&~mask;glow[edge]=near[edge]*amount
for level,u in enumerate(steps):
 q=a.copy();q[:,:,:3]=np.clip(rgb+glow*u,0,255).astype('uint8')
 # Partial local illumination is baked onto existing armor around every emitter.
 # Preserve source core ring detail, source alpha and the rest of the armor.
 for white in [0,1]:
  v=q.copy()
  if white:v[:,:,:3]=(v[:,:,:3]*.12+255*.88).astype('uint8')
  Image.fromarray(v).resize((296,296),Image.Resampling.NEAREST).save(D/f'body-{level}-{white}.png')
raw=sorted((S/'returned/drain').glob('frame_*.png'))[1:];assert len(raw)==32
sheet=Image.new('RGBA',(320*32,320));counts=[];hashes=[]
for i,p in enumerate(raw):
 im=Image.open(p).convert('RGBA');v=np.array(im);t=v[:,:,:3].astype(float);rr,gg,bb=t.transpose(2,0,1)
 # Restore actual PixelLab blue-white discharge, including arcs crossing armor.
 # Do not retain generated armor or duplicate source core/ring graphics.
 bluefx=(v[:,:,3]>0)&(bb>85)&(bb>rr*1.18)&(bb>gg*1.08)
 white=(v[:,:,3]>0)&(t.min(2)>185)&binary_dilation(bluefx,iterations=2)
 keep=(bluefx|white)&~binary_dilation(mask,iterations=1)
 v[:,:,3]=np.where(keep,v[:,:,3],0);v[v[:,:,3]==0]=0
 cell=Image.new('RGBA',(320,320));cell.alpha_composite(Image.fromarray(v).resize((296,296),Image.Resampling.NEAREST),(12,12));sheet.paste(cell,(320*i,0))
 counts.append(int(keep.sum()));hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
sheet.save(D/'aura.png',optimize=True)
old="for(const key of CE110.keys)XART._src['ce110_'+key]='assets/game/levels/stage_05/boss/chronus_electric_1110/'+key+'.png';"
assert old in code
code=code.replace(old,"for(const key of CE110.keys)XART._src['ce110_'+key]='assets/game/levels/stage_05/boss/'+(key==='aura'||key.startsWith('body-')?'chronus_core_loop_1110/':'chronus_electric_1110/')+key+'.png';")
start=code.index('function ce110Body(e)');end=code.index('function ce110Emit(',start)
code=code[:start]+'''// Integrated frame clock: 8fps rising continuously to40fps, without phase resets.
function ce110Loop(age){const t=Math.min(10,age);return 8*t+1.6*t*t+Math.max(0,age-10)*40;}
function ce110Body(e){const F=e.hf17,q=ce110Offset(F),clock=ce110Loop(F.age),frame=Math.floor(clock)%32;
 const floor=Math.min(3,Math.floor(F.age/2)),level=Math.min(5,floor+Math.floor((Math.sin(clock/32*Math.PI*2)*.5+.5)*(5-floor)+.001)),white=e.boss.flash>0||Math.floor(F.age*16)%3===0?1:0;
 const im=XART.get('ce110_body-'+level+'-'+white);if(im)ctx.drawImage(im,Math.round(F.anchor.x+q[0]-148),Math.round(F.anchor.y+q[1]-148));
 CE110.stats[white?'white':'normal']++;ce110Blit('aura',frame,320,F.anchor.x+q[0],F.anchor.y+q[1]);
 CE110.stats.aura[frame]=(CE110.stats.aura[frame]||0)+1;CE110.stats.coreLevels||={};CE110.stats.coreLevels[level]=(CE110.stats.coreLevels[level]||0)+1;CE110.stats.loopFps=8+3.2*Math.min(10,F.age);
}
'''+code[end:]
code=code.replace('// CE110: source-pixel 1015 lighting, authored electrical aura and exact source-piece breakup.','// CE110: actual core-pixel 1015 steps, preserved PixelLab discharge and source-piece breakup.')
(C/'hammer_finale_1017.js').write_text(code,encoding='utf-8',newline='\n')
meta={'expected_source_hash':hashlib.sha256(before).hexdigest(),'body':{'source':'_ART_SOURCES/hammer_finale_1017/references/stunned.png','cell':[296,296],'pivot':[148,148],'emissive_pixels':int(mask.sum()),'steps':steps,'local_spill_pixels':3,'alpha_preserved':True},'aura':{'source':'_ART_SOURCES/hammer_finale_1017/returned/drain/frame_001.png through frame_032.png','pixellab_job':'66542724-a05b-4f41-aa33-21f0a8748020','frames':32,'cell':[320,320],'pivot':[160,160],'energy_pixels':counts,'source_sha256':hashes,'frame_clock':'8*t+1.6*t*t for t<=10; then40fps','fps':[8,40]},'explosions_and_shatter':'previously selected three families and original armor trajectories retained'}
(O/'manifest.json').write_text(json.dumps(meta,indent=2))
contact=Image.new('RGB',(960,640),'#10192b');d=ImageDraw.Draw(contact)
for j,i in enumerate([3,7,11,15,23,27]):
 tile=Image.new('RGBA',(320,320),'#10192b');tile.alpha_composite(Image.open(D/'body-5-0.png'),(12,12));tile.alpha_composite(sheet.crop((320*i,0,320*(i+1),320)));contact.paste(tile.convert('RGB'),(j%3*320,j//3*320));d.text((j%3*320+4,j//3*320+4),str(i),fill='white')
contact.save(W/'core-loop-contact.png')
print(json.dumps({'corePixels':int(mask.sum()),'auraFrames':32,'energyRange':[min(counts),max(counts)],'files':len(list(D.glob('*.png')))}))
