from pathlib import Path
from PIL import Image,ImageOps,ImageFilter,ImageDraw
import numpy as np,json,math
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';O=R/'_shots/final_version_1021';cat=json.loads((R/'assets/data/AIR_MOTION_1013.json').read_text())['entries'];art={'models':{},'sheets':{},'audit':[],'pending':[]}
def read(name):return [Image.open(p).convert('RGBA') for p in sorted((S/'raw'/name).glob('*.png'))]
def emit(id,kind,ims,D):
 assert all(im.size==(128,128) for im in ims);name=f'{id}_{kind}';sid='af21_'+name;sheet=Image.new('RGBA',(min(8,len(ims))*128,math.ceil(len(ims)/8)*128));frames=[]
 for i,im in enumerate(ims):
  x=i%8*128;y=i//8*128;sheet.alpha_composite(im,(x,y));frames.append([x,y,128,128])
 D.mkdir(parents=True,exist_ok=True);p=D/(kind+'.webp');sheet.save(p,lossless=True,method=6);art['sheets'][sid]={'key':'af21_'+name,'path':p.relative_to(R).as_posix(),'w':sheet.width,'h':sheet.height}
 return{'key':'af21_'+name,'path':p.relative_to(R).as_posix(),'frames':len(ims),'cells':frames,'cell':128,'pivot':[64,64],'span':art['models'][id]['span'],'modules':[[0,0,48,128],[48,0,32,128],[80,0,48,128]]}
for folder in sorted((S/'raw').glob('air_*')):
 id=folder.name[4:]
 if id not in cat:continue
 seed=read(folder.name)
 if len(seed)!=1:continue
 master=seed[0];assert master.size==(128,128),(id,master.size)
 # PixelLab motion is geometry; the approved master owns its color palette.
 # Quantize every pose through that single palette so generated magenta/purple
 # drift never becomes an unannounced hit flash or changes a pilot's identity.
 palette=master.convert('RGB').quantize(colors=128,method=Image.Quantize.MEDIANCUT)
 raw=np.array(master).astype(float);visible=raw[:,:,3]>100;magenta=(raw[:,:,0]>raw[:,:,1]*1.2)&(raw[:,:,2]>raw[:,:,1]*1.2)&(raw[:,:,0]>50)&(raw[:,:,2]>50)&visible
 if magenta.sum()/max(1,visible.sum())<.02:
  colors=np.array(palette.getpalette(),dtype=int).reshape(-1,3);bad=(colors[:,0]>colors[:,1]*1.2)&(colors[:,2]>colors[:,1]*1.2)&(colors[:,0]>50)&(colors[:,2]>50);good=colors[~bad]
  for i in np.flatnonzero(bad):colors[i]=good[np.square(good-colors[i]).sum(1).argmin()]
  palette.putpalette(colors.reshape(-1).tolist())
 def lock_palette(im):
  out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(im.getchannel('A'));return out
 banks={'roll':read('air_'+id+'_roll'),'somer':read('air_'+id+'_somer'),'drift':read('air_'+id+'_drift'),'attack':read('air_'+id+'_attack')}
 if id=='l6v_s0':
  repair=read('air_l6v_s0_roll_repair')
  if len(repair)==16:banks['roll']=repair
 expected={'roll':16,'somer':16,'drift':16,'attack':8}
 if any(len(banks[k])!=n for k,n in expected.items()):art['pending'].append({'id':id,'banks':{k:len(v) for k,v in banks.items()}});continue
 c=cat[id];D=R/('assets/game/levels/stage_06/boss/air_refit_1021' if c.get('rebel') else f'assets/game/levels/stage_{c["stage"]:02}/enemies/air_refit_1021')/id
 bb=master.getbbox();span=max(bb[2]-bb[0],bb[3]-bb[1]);art['models'][id]={'name':c['name'],'stages':c['stages'],'aliases':c['aliases'],'sourceKeys':c.get('sourceKeys',{}),'nativeRatios':c.get('nativeRatios',{}),'referenceRatio':c.get('referenceRatio',1),'span':span,'banks':{}}
 model=art['models'][id]
 # Authored parts are disjoint rectangles of the same frame/texture. Their
 # union reconstructs the full sprite exactly without three copies in memory.
 # Existing module/weapon owners may animate them independently at these roots.
 for kind,ims in {'idle':[master],**banks}.items():
  if kind!='idle':ims=[lock_palette(im) for im in ims]
  if kind=='attack':
   # Projectiles and muzzle effects belong to native emitters. Retain physical
   # recoil while stripping any generated flame outside the approved hull.
   mask=master.getchannel('A').filter(ImageFilter.MaxFilter(7));ims=[Image.composite(im,Image.new('RGBA',im.size),mask) for im in ims]
  a=emit(id,kind,ims,D);model['banks'][kind]=a
  for i,im in enumerate(ims):
   bb=im.getbbox();assert bb and min(bb[:2])>0 and max(bb[2:])<128,(id,kind,i,bb)
   # Fixed module source rectangles must reproduce every alpha pixel exactly.
   rebuild=Image.new('RGBA',im.size)
   for x,y,w,h in a['modules']:rebuild.paste(im.crop((x,y,x+w,y+h)),(x,y))
   assert rebuild.tobytes()==im.tobytes();art['audit'].append({'id':id,'kind':kind,'frame':i,'bounds':list(bb),'modulesExact':True})
 model['sockets']={'port':[-18,21],'starboard':[18,21],'exhaustPort':[-12,-30],'exhaustStarboard':[12,-30]}
 (D/'manifest.json').write_text(json.dumps(model,indent=2))
aliases={'flight_variant_1':'s1jetdelta','flight_variant_4':'s4interceptor','flight_variant_6':'s6dart','flight_variant_8':'s8interceptor','stealth_red':'s6dart','stealth_green':'s6dart','stealth_orange':'s6dart','l6v_r0':'l6v_s0','l6v_b0':'l6v_s0','l6v_r1':'l6v_s1','l6v_b1':'l6v_s1','l6v_r2':'l6v_s2','l6v_b2':'l6v_s2'}
art['reusedFamilies']=aliases
(S/'air-export-audit.json').write_text(json.dumps(art['audit'],indent=2));(R/'assets/air_refit_art_1021.js').write_text('"use strict";\nconst AF21_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');(S/'air-production-manifest.json').write_text(json.dumps(art,indent=2));print(json.dumps({'ready':list(art['models']),'pending':art['pending'],'poses':len(art['audit'])}))
