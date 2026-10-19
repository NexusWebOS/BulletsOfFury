"""Build the archive bank; --fixture is local-only QA using supplied old art."""
from pathlib import Path
import argparse,json,math,hashlib,shutil
from PIL import Image,ImageDraw
import numpy as np
from generate_dracodia_archive_1018 import refs
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_archive_1018';Q=R/'_shots/dracodia_archive_1018'
def build(fixture=False):
 O=Q/'fixture_art' if fixture else R/'assets/game/levels/stage_08/boss/archive_1018';O.mkdir(parents=True,exist_ok=True);(S/'refs').mkdir(parents=True,exist_ok=True)
 data={'models':{},'fx':{},'fixture':fixture};audit=[]
 selections=json.loads((S/'selections.json').read_text()) if (S/'selections.json').exists() else {}
 def save(name,im):
  assert im.width%2==im.height%2==0;p=O/(name+'.png');im.save(p,optimize=True)
  return dict(key=name,path=p.relative_to(R).as_posix(),w=im.width,h=im.height,pivot=[im.width//2,im.height//2],bounds=list(im.getbbox() or [0,0,0,0]),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 def pad(im):
  assert im.size==(256,256);out=Image.new('RGBA',(320,320));out.paste(im,(32,32));return out
 def contact(name,frames):
  w,h=frames[0].size;n=min(len(frames),32);out=Image.new('RGBA',(w*8,(h+18)*math.ceil(n/8)),'#111927');g=ImageDraw.Draw(out)
  for i,im in enumerate(frames[:n]):x=i%8*w;y=i//8*(h+18);out.alpha_composite(im,(x,y));g.text((x+3,y+h),str(i),fill='white')
  out.convert('RGB').save(Q/(name+'-sheet.png'))
  if len(frames)<8:return
  # Neighbours share the exact canvas and pivot. This is QA, never shipped art.
  onion=Image.new('RGBA',(w*8,h+18),'#111927');g=ImageDraw.Draw(onion)
  for column,index in enumerate(np.linspace(0,len(frames)-1,8).astype(int)):
   x=column*w
   for offset,color,opacity in [(-1,(50,210,255),85),(1,(255,75,185),85)]:
    neighbour=frames[max(0,min(len(frames)-1,index+offset))];alpha=neighbour.getchannel('A').point(lambda p:p*opacity//255)
    tint=Image.new('RGBA',(w,h),(*color,0));tint.putalpha(alpha);onion.alpha_composite(tint,(x,0))
   current=frames[index].copy();current.putalpha(current.getchannel('A').point(lambda p:p*185//255));onion.alpha_composite(current,(x,0))
   g.line((x+w//2-4,h//2,x+w//2+4,h//2),fill='#ffffff');g.text((x+3,h),str(index),fill='white')
  onion.convert('RGB').save(Q/(name+'-onion.png'))
  flat=[]
  for im in frames:
   bg=Image.new('RGBA',im.size,'#111927');bg.alpha_composite(im);flat.append(bg.convert('RGB'))
  flat[0].save(Q/(name+'.gif'),save_all=True,append_images=flat[1:],duration=62,loop=0,optimize=False)
 for name,source in refs.items():
  if fixture:
   shutil.copyfile(source,S/'refs'/(name+'.png'));im=Image.open(source).convert('RGBA')
   if name=='halberd':
    im=im.crop((7,14,295,152));v=np.array(im);mask=(v[:,:,0]<45)&(v[:,:,1]<52)&(v[:,:,2]<66);v[mask,3]=0;im=Image.fromarray(v)
   if max(im.size)>256:im.thumbnail((256,256),Image.Resampling.NEAREST)
   canvas=Image.new('RGBA',(256,256));canvas.paste(im,((256-im.width)//2,(256-im.height)//2));im=canvas
  else:im=Image.open(S/'returned'/name/'frame_000.png').convert('RGBA');assert im.size==(256,256)
  if not fixture:assert np.count_nonzero(np.array(im)[:,:,3]>20)<256*256*.88,(name,'opaque background')
  whole=pad(im);v=np.array(whole);owner=np.zeros((320,320),np.uint8)
  # Measured hull seams in source coordinates, then shared +32 padding.
  # Each entire battery and its mounting pod belongs to its weapon assembly.
  seams={'bastion':(106,150),'camo':(110,146),'halberd':(87,169)}[name] if not fixture else (85,171)
  owner[:,:seams[0]+32]=1;owner[:,seams[1]+32:]=2;parts={};rebuild=np.zeros_like(v)
  for i,id in enumerate(['core','left','right']):layer=np.zeros_like(v);layer[owner==i]=v[owner==i];rebuild[owner==i]=layer[owner==i];parts[id]=save('d20_'+name+'_'+id,Image.fromarray(layer))
  assert np.array_equal(v,rebuild)
  points={'halberd':{'left':[93,193],'right':[227,193],'core':[160,212]},
          'bastion':{'left':[103,215],'right':[218,215],'core':[160,225]},
          'camo':{'left':[103,214],'right':[216,214],'core':[160,230]}}[name]
  # Snap each measured fixture to a real opaque pixel in that assembly.
  fixed={}
  for id,point in points.items():
   yy,xx=np.where((v[:,:,3]>80)&(owner==['core','left','right'].index(id)));assert len(xx),(name,id)
   i=np.argmin((xx-point[0])**2+(yy-point[1])**2);fixed[id]=[int(xx[i]),int(yy[i])]
  download=[];frames=[]
  if not fixture:
   paths=sorted((S/'returned'/(name+'_download')).glob('frame_*.png'));assert len(paths)==33,(name,len(paths))
   # Frame zero is the exact seed; animation output follows it. Reverse at runtime.
   selected=selections.get(name+'_download',list(range(1,33)))
   frames=[pad(Image.open(paths[i]).convert('RGBA')) for i in selected];frames[0]=whole.copy()
   assert len(frames)>=16 and len({f.tobytes() for f in frames})>=len(frames)-1,(name,'duplicate download poses')
   assert np.count_nonzero(np.array(frames[-1])[:,:,3]>32)<np.count_nonzero(v[:,:,3]>32)*.20,(name,'download does not dissolve')
   for i,f in enumerate(frames):download.append(save('d20_'+name+'_download_'+f'{i:02}',f))
   contact(name+'-download',frames)
  mounts={'core':[160,160],'left':[sum((parts['left']['bounds'][0],parts['left']['bounds'][2]))//2,160],'right':[sum((parts['right']['bounds'][0],parts['right']['bounds'][2]))//2,160]}
  data['models'][name]=dict(full=save('d20_'+name+'_full',whole),parts=parts,mounts=mounts,muzzles=fixed,download=download)
  contact(name+'-modules',[whole,*[Image.open(O/(a['key']+'.png')).convert('RGBA') for a in parts.values()]])
  audit.append(dict(name=name,exact_module_reassembly=True,format=[320,320],pivot=[160,160],muzzles=fixed))
 if not fixture:
  for name in ['bomb_charge','bomb_burst','lightning_loop','storm_loop','transfer_loop']:
   source='bomb_burst_v2' if name=='bomb_burst' else name
   paths=sorted((S/'returned'/source).glob('frame_*.png'));assert len(paths)==33,(name,len(paths));selected=selections.get(name,list(range(1,33)));frames=[Image.open(paths[i]).convert('RGBA') for i in selected];size=frames[0].size;assert size in [(128,128),(256,256)]
   if name=='transfer_loop':
    # The service returned a neutral grey segmentation matte. Keep the actual
    # green/cyan/white VFX pixels; never ship an opaque box behind a download.
    clean=[]
    for f in frames:
     v=np.array(f);rgb=v[:,:,:3].astype(np.int16);matte=(rgb.max(2)-rgb.min(2)<=8)&(rgb.mean(2)>48)&(rgb.mean(2)<180);v[matte]=0;clean.append(Image.fromarray(v))
    frames=clean
   assert all(f.size==size for f in frames);assert len(frames)>=16 and len({f.tobytes() for f in frames})>=len(frames)-1,(name,'duplicate FX poses')
   assert all(np.count_nonzero(np.array(f)[:,:,3]>20)<f.width*f.height*.94 for f in frames),(name,'opaque FX background')
   padding=16 if name in ['bomb_charge','bomb_burst'] else 32 if name in ['storm_loop','transfer_loop'] else 0
   if padding:
    padded=[]
    for f in frames:
     c=Image.new('RGBA',(f.width+padding*2,f.height+padding*2));c.paste(f,(padding,padding));padded.append(c)
    frames=padded
   rows=[save('d20_'+name+f'_{i:02}',f) for i,f in enumerate(frames)];data['fx'][name]=dict(frames=rows,fps=24 if name=='bomb_burst' else 16,renderScale=frames[0].width/size[0],source=source,selected=selected);contact(name,frames)
 manifest=Q/'fixture_art.js' if fixture else R/'assets/dracodia_archive_art_1018.js';manifest.write_text('"use strict";\nconst D20_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 (Q/'fixture-registration.json' if fixture else S/'registration.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8');print(('QA fixture' if fixture else 'Production')+' archive art registered: '+str(len(audit))+' models')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--fixture',action='store_true');a=ap.parse_args();build(a.fixture)
