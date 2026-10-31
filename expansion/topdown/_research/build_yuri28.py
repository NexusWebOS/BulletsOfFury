"""Export reviewed PixelLab cross-steps at the existing Yuri unit/root."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,zipfile,io,hashlib
import numpy as np
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/yuri28';S=A/'source';F=A/'frames';F.mkdir(exist_ok=True,parents=True);O=R/'_shots/yuri28';O.mkdir(exist_ok=True)
assets={};sequences={};audit=[]
for direction in ['east','west']:
 for action in ['up_step','up_fire']:
  name=direction+'_'+action
  # Raw PixelLab outputs are retained as individually named PNG frames.
  paths=sorted((S/'selected'/action).glob('*.png'));assert len(paths)==17,(name,len(paths))
  images=[Image.open(p).convert('RGBA')for p in paths];images=[im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)for im in images]if direction=='east'else images;assert all(im.size==(192,224)for im in images)
  keys=[];scale=88/185;source_root=(65 if direction=='east'else 127,216);offset=(round(96-source_root[0]*scale),round(160-source_root[1]*scale))
  chosen=images[1:13]if action=='up_fire'else images[1:]
  for i,im in enumerate(chosen):
   bounds=im.getbbox();assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<192 and bounds[3]<224,(name,i,bounds)
   # One proportional scale and translation for all clips. No per-frame fitting.
   out=Image.new('RGBA',(192,224));part=im.resize((round(192*scale),round(224*scale)),Image.Resampling.NEAREST);out.alpha_composite(part,offset);out.putalpha(out.getchannel('A').point(lambda v:255 if v>=128 else 0));b=out.getbbox();assert b and b[0]>4 and b[1]>4 and b[2]<188 and b[3]<220
   # Measure the outer barrel tip in the upper-body window, excluding boots.
   ar=np.asarray(out);mask=(ar[:,:,3]>0)&(ar[:,:,0]<115)&(ar[:,:,1]<120)&(ar[:,:,2]<125);mask[:75]=False;mask[133:]=False
   yy,xx=np.where(mask);tip=int(xx.max()if direction=='east'else xx.min());near=mask[:,max(0,tip-1):min(192,tip+2)];ys=np.where(near)[0];muzzle=[tip,round(float(np.median(ys)))]
   key=f'y28_{name}_{i}';p=F/(key+'.png');out.save(p)
   assets[key]={'file':p.relative_to(R).as_posix(),'size':[192,224],'anchor':[96,160],'bounds':list(b),'drawScale':1,'muzzle':muzzle,'sourceFrame':i+1}
   keys.append(key);audit.append({'key':key,'sourceSize':[192,224],'scale':scale,'translation':list(offset),'sourceRoot':list(source_root),'mirrored':direction=='east','exportRoot':[96,160],'sourceBounds':list(bounds),'muzzle':muzzle,'hash':hashlib.sha256(p.read_bytes()).hexdigest()})
  if action=='up_step':
   out=Image.new('RGBA',(192,224));out.alpha_composite(images[0].resize((round(192*scale),round(224*scale)),Image.Resampling.NEAREST),offset);out.putalpha(out.getchannel('A').point(lambda a:255 if a>=128 else 0));key='y28_'+direction+'_setup';p=F/(key+'.png');out.save(p);assets[key]={'file':p.relative_to(R).as_posix(),'size':[192,224],'anchor':[96,160],'bounds':list(out.getbbox()),'drawScale':1,'muzzle':assets[keys[0]]['muzzle']}
  sequences['y28_'+name]={'frames':keys,'fps':24,'stride':96,'motion':True,'contacts':[0,len(keys)//2],'direction':direction,'action':action,'loop':True}
  contact=Image.new('RGB',(192*4,240*4),'#24303b');d=ImageDraw.Draw(contact)
  for i,k in enumerate(keys):
   im=Image.open(R/assets[k]['file']);x=i%4*192;y=i//4*240;contact.paste(im,(x,y),im);d.line((x,y+160,x+192,y+160),fill='#416056');d.text((x+3,y+225),str(i+1),fill='white')
  contact.save(O/(name+'_contact.png'))
  frames=[]
  for k in keys:
   bg=Image.new('RGBA',(192,224),'#24303b');bg.alpha_composite(Image.open(R/assets[k]['file']));frames.append(bg.resize((384,448),Image.Resampling.NEAREST))
  frames[0].save(O/(name+'.gif'),save_all=True,append_images=frames[1:],duration=65,loop=0,disposal=2)
pack={'assets':assets,'sequences':sequences,'audit':audit,'build':'overdrive1015-yuri28-r1','source':'PixelLab; public GitHub Yuri identity references verified byte-for-byte'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n');(A/'manifest.js').write_text('window.TD_YURI28_ART='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'frames':len(assets),'banks':len(sequences)}))
