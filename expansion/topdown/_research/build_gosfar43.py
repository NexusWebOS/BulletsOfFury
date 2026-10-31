"""Owning export for Gosfar43. Fixed canvases, hard alpha, one palette/body bank."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,urllib.request,hashlib,shutil,sys
W=Path(__file__).resolve().parent;G=W.parents[2] if W.name=='_research' else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O=G/'expansion/topdown/art/gosfar43';S=O/'source';S.mkdir(parents=True,exist_ok=True)
if not (W/'gosfar-minigun-reference.png').exists():W=S/'inputs'
JOBS={
 'hotwire/hack':('0febd270-6d92-41b1-8ab8-98030fe3e609',5,8,True,[64,120]),
 'hotwire/cover':('6df314b9-0b8b-46f7-b992-bee104215249',5,7,True,[64,120]),
 'hotwire/fire':('147e305e-aad0-4990-8a78-15001ee75c59',5,12,False,[64,120]),
 'hotwire/run':('534fdcd9-5fd6-4148-aae3-099f16819b34',9,13,True,[64,120]),
 'yuri/cover':('04d8fcae-9736-4481-ab04-efcf73ec374c',5,7,True,[64,120]),
 'gosfar/walk':('6c0278b8-967e-4b2e-a2bd-57208d7fd4fa',17,16,True,[80,152]),
 'gosfar/rev':('5ca49181-3655-4807-be7f-a834c9e209fd',9,24,True,[80,152]),
 'gosfar/fire':('c54117f1-f23f-490f-9114-70825c81cbf8',9,64,True,[80,152]),
 'gosfar/death':('fa719b2e-f1e0-4355-a5d5-743547d4f6a1',9,5,False,[80,152]),
 'gosfar/overheat':('cc1276aa-30c6-4419-a725-eac44b797405',5,8,True,[80,152]),
 'hotwire/throw':('e29f9f4c-e6d8-4961-8d70-5acefcd203ec',5,10,False,[64,120]),
 'gosfar/fire/east':('b451fab2-d3a9-4f0f-b65a-bb4717538c19',9,22,True,[80,152]),
 'gosfar/walk/east':('64041bfc-3deb-4109-bed9-d26c2859b620',9,12,True,[80,152]),
 'gosfar/fire/west':('3f4d907d-5c9c-4e64-8697-e4794df541ba',9,22,True,[80,152]),
 'gosfar/walk/west':('ea50a7ca-43bf-42f8-bc49-565de6018a1b',9,12,True,[80,152]),
 'gosfar/fire/north':('76d011a8-71aa-422d-9317-f09dcae6017c',9,22,True,[112,216]),
 'gosfar/walk/north':('093ef27e-3cdb-4de7-b579-8c75a3ba94c7',9,12,True,[80,152]),
}
def fetch():
 for name,(job,n,*_) in JOBS.items():
  d=S/name;d.mkdir(parents=True,exist_ok=True)
  receipt=d/'job.txt'
  if receipt.exists() and receipt.read_text()!=job:
   for p in d.glob('*.png'):p.rename(p.with_suffix('.replaced.png'))
  receipt.write_text(job)
  for i in range(n):
   p=d/f'{i:03}.png'
   if not p.exists():
    url=f'https://api.pixellab.ai/mcp/images/{job}/download'+(f'?index={i}' if n>1 else '')
    try: urllib.request.urlretrieve(url,p)
    except Exception as e: print('PENDING',name,i,str(e));break
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>160,255,0);return Image.fromarray(a)
assets={};banks={};review=[]
def pack(name,ims,origin,fps=10,loop=True,palette=None,provider='PixelLab'):
 ims=[clean(i) for i in ims];w,h=ims[0].size;assert w%2==h%2==0;assert all(i.size==(w,h) for i in ims)
 if name.startswith('hotwire/'):
  # One shared .75 physical unit for EVERY Hotwire action, around the same root.
  baked=[]
  for im in ims:
   c=Image.new('RGBA',(128,128));c.paste(im.resize((96,96),Image.Resampling.NEAREST),(16,30));baked.append(c)
  ims=baked
 if palette is not None:
  ref=np.array(clean(palette));visible=ref[ref[:,:,3]>0,:3]
  # Median-cut retains violet/amber material ramps from the high-detail seed;
  # most-frequent exact RGB values incorrectly discarded those low-count hues.
  quant=Image.fromarray(visible.reshape((1,len(visible),3))).quantize(colors=192,method=Image.Quantize.MEDIANCUT)
  pal=np.array(quant.getpalette(),dtype=np.int32).reshape((-1,3))[:192]
  # Fire/overheat retain hot cores and steam in addition to the approved body colours.
  pal=np.concatenate([pal,np.array([[255,255,255],[255,241,164],[255,195,74],[255,122,37],[218,51,40],[122,30,37],[158,178,196]])])
  for i,im in enumerate(ims):
   a=np.array(im);mask=a[:,:,3]>0;c,inv=np.unique(a[:,:,:3][mask],axis=0,return_inverse=True);mapped=pal[((c.astype(np.int32)[:,None,:]-pal[None,:,:])**2).sum(2).argmin(1)];a[:,:,:3][mask]=mapped[inv];ims[i]=Image.fromarray(a)
 cols=min(8,len(ims));sheet=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*h));keys=[];bounds=[]
 for i,im in enumerate(ims):
  b=im.getbbox();assert b,(name,i);bounds.append(b);r=[i%cols*w,i//cols*h,w,h];sheet.paste(im,r[:2]);k='g43_'+name.replace('/','_')+'_'+str(i);keys.append(k);assets[k]={'file':(O/(name.replace('/','_')+'.png')).relative_to(G).as_posix(),'rect':r,'size':[w,h],'anchor':origin,'bounds':b,'provider':provider,'bank':name,'phase':i,'drawScale':1}
  if name.startswith('gosfar/'):
   direction=name.split('/')[-1];assets[k]['muzzle']={'east':[147,86],'west':[13,86],'north':[93,15] if w==224 else [58,30]}.get(direction,[82,102])
   if direction in ['east','west']:
    mask=np.array(im)[:,:,3]>0;region=mask[50:112,:45] if direction=='west' else mask[50:112,115:]
    yy,xx=np.where(region)
    if len(xx):
     edge=int(xx.min()) if direction=='west' else int(xx.max()+115);band=mask[50:112,edge:edge+7] if direction=='west' else mask[50:112,edge-6:edge+1]
     assets[k]['muzzle']=[edge+(4 if direction=='west' else -4),int(np.median(np.where(band)[0])+50)]
 sheet.save(O/(name.replace('/','_')+'.png'));banks[name]={'frames':keys,'fps':fps,'loop':loop,'duration':len(keys)/fps,'origin':origin,'size':[w,h],'palette_locked':palette is not None}
 preview=Image.new('RGBA',(min(8,len(ims))*w,math.ceil(len(ims)/8)*(h+18)),(22,29,38,255));d=ImageDraw.Draw(preview)
 for i,im in enumerate(ims):
  x=i%8*w;y=i//8*(h+18);prev=ims[max(0,i-1)].copy();prev.putalpha(prev.getchannel('A').point(lambda a:a//4));preview.alpha_composite(prev,(x,y));preview.alpha_composite(im,(x,y));d.line((x+origin[0],y,x+origin[0],y+h),fill='#44c5b2');d.line((x,y+origin[1],x+w,y+origin[1]),fill='#caab72');d.text((x+3,y+h),str(i),fill='white')
 review_dir=O/'review';review_dir.mkdir(exist_ok=True);preview.convert('RGB').save(W/(name.replace('/','_')+'-onion.jpg'));preview.convert('RGB').save(review_dir/(name.replace('/','_')+'-onion.jpg'))
 review.append({'bank':name,'bounds':bounds,'size':[w,h],'root':origin,'frames':len(ims),'method':'Fixed canvas/root. One shared palette. No per-frame scaling or body transforms.'})
def build():
 boss=Image.open(W/'gosfar-minigun-reference.png');hot=Image.open(W/'hotwire-reference.png');yuri=Image.open(W/'yuri-reference.png')
 pack('gosfar/ready',[Image.open(W/'ready-corrected.png')],[80,152],palette=boss,provider='ImageGen + PixelLab exact')
 pack('hotwire/ready',[hot],[64,120],palette=hot)
 for di in ['east','west']:pack('gosfar/ready/'+di,[Image.open(W/'rotations'/(di+'.png'))],[80,152],palette=boss)
 pack('gosfar/ready/north',[Image.open(W/'north-raised-reference.png')],[112,216],palette=boss,provider='ImageGen')
 for name,(job,n,fps,loop,origin) in JOBS.items():
  files=sorted(p for p in (S/name).glob('*.png') if '.replaced.' not in p.name);assert len(files)==n,(name,len(files),n)
  pal=boss if name.startswith('gosfar') else hot if name.startswith('hotwire') else yuri
  ims=[Image.open(p) for p in files]
  if name in ['gosfar/rev','gosfar/fire','gosfar/overheat']:
   corrected=Image.open(W/(name.split('/')[1]+'-corrected.png'));ims=[corrected.crop((i%3*160,i//3*160,i%3*160+160,i//3*160+160)) for i in range(n)]
  if name=='yuri/cover':
   corrected=Image.open(W/'yuri-cover-corrected.png');ims=[corrected.crop((i%3*128,i//3*128,i%3*128+128,i//3*128+128)) for i in range(n)]
  if name=='gosfar/fire/west':
   corrected=Image.open(W/'west-fire-corrected.png');ims=[corrected.crop((i%3*160,i//3*160,i%3*160+160,i//3*160+160)) for i in range(n)]
  if name in ['gosfar/rev','gosfar/fire']:ims=ims[:8] # closure duplicate is not an extra angular phase
  if name=='hotwire/fire':ims=ims[:4] # last generated frame repeats the ignition flash
  pack(name,ims,origin,fps,loop,pal)
 src=Image.open(W/'elevator-source.png').convert('RGBA');padded=Image.new('RGBA',(1776,888));padded.paste(src,(0,0));frames=[]
 for i in range(8):frames.append(padded.crop((i%4*444,i//4*444,i%4*444+444,i//4*444+444)).resize((160,160),Image.Resampling.NEAREST))
 pack('elevator',frames,[80,152],4,False,provider='ImageGen')
 out={'build':'overdrive1018-gosfar43-r4','assets':assets,'banks':banks,'generation_jobs':JOBS,'counts':{'banks':len(banks),'frames':len(assets)}}
 (O/'manifest.json').write_text(json.dumps(out,indent=2));(O/'manifest.js').write_text('window.TD_GOSFAR43_ART='+json.dumps(out,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,window.TD_GOSFAR43_ART.assets);\n')
 (O/'review.json').write_text(json.dumps(review,indent=2));shutil.copy2(W/'gosfar-minigun-reference.png',S/'approved-minigun.png');shutil.copy2(W/'elevator-source.png',S/'elevator-source.png');print(out['counts'])
 inputs=S/'inputs';inputs.mkdir(exist_ok=True)
 if W.resolve()!=inputs.resolve():
  for name in ['gosfar-minigun-reference.png','hotwire-reference.png','yuri-reference.png','north-raised-reference.png','elevator-source.png','rev-corrected.png','fire-corrected.png','ready-corrected.png','overheat-corrected.png','yuri-cover-corrected.png','west-fire-corrected.png','muzzle-edits.json']:
   shutil.copy2(W/name,inputs/name)
  shutil.copytree(W/'rotations',inputs/'rotations',dirs_exist_ok=True)
if __name__=='__main__':
 if '--fetch' in sys.argv:fetch()
 if '--build' in sys.argv:build()
