"""PixelLab-only Gosfar/wall replacement; preserve approved crew/elevator banks."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, json, math, urllib.request, shutil, sys
W=Path(__file__).resolve().parent
G=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury') if W.name!='_research' else W.parents[2]
O=G/'expansion/topdown/art/gosfar44'; O.mkdir(parents=True,exist_ok=True)
if not (W/'jobs.json').exists(): W=O/'source'
jobs=json.loads((W/'jobs.json').read_text())
raw=W/'raw'; raw.mkdir(exist_ok=True)
def fetch():
 for name,j in jobs.items():
  d=raw/name; d.mkdir(parents=True,exist_ok=True)
  for i in range(j['n']):
   p=d/f'{i:03}.png'
   if not p.exists():
    url=j['states'][i] if 'states' in j else j.get('url',f"https://api.pixellab.ai/mcp/images/{j['job']}/download")
    if j['n']>1 and 'states' not in j:url+=('?index='+str(i))
    try:urllib.request.urlretrieve(url,p)
    except Exception as e:print('PENDING',name,i,str(e));break
def clean(im):
 a=np.array(im.convert('RGBA')); a[:,:,3]=np.where(a[:,:,3]>160,255,0); a[a[:,:,3]==0,:3]=0
 return Image.fromarray(a)
def build():
 old=json.loads((G/'expansion/topdown/art/gosfar43/manifest.json').read_text())
 banks={k:v for k,v in old['banks'].items() if not k.startswith('gosfar/')}
 assets={k:v for k,v in old['assets'].items() if not v['bank'].startswith('gosfar/')}
 review=[]; bp=clean(Image.open(raw/'gosfar/ready/000.png'))
 colors=np.array(bp); colors=colors[colors[:,:,3]>0,:3]
 q=Image.fromarray(colors.reshape(1,-1,3)).quantize(colors=128,method=Image.Quantize.MEDIANCUT)
 palette=np.array(q.getpalette(),dtype=np.int32).reshape(-1,3)[:128]
 palette=np.concatenate([palette,np.array([[255,255,255],[255,241,164],[255,195,74],[255,122,37],[218,51,40],[122,30,37],[158,178,196]])])
 for name,j in jobs.items():
  if j.get('source_only'):continue
  ims=[clean(Image.open(raw/name/f'{i:03}.png')) for i in range(j['n'])]
  if j.get('take'):ims=[ims[i] for i in j['take']]
  fix=W/(name.replace('/','_')+'-corrected.png')
  if fix.exists():
   sh=Image.open(fix).convert('RGBA');w,h=ims[0].size;cols=sh.width//w
   ims=[clean(sh.crop((i%cols*w,i//cols*h,i%cols*w+w,i//cols*h+h))) for i in range(len(ims))]
  w,h=ims[0].size;root=j.get('root',[80,152]);assert w%2==h%2==0 and all(i.size==(w,h) for i in ims)
  if name.startswith('gosfar/'):
   for i,im in enumerate(ims):
    a=np.array(im);m=a[:,:,3]>0;c,inv=np.unique(a[:,:,:3][m],axis=0,return_inverse=True)
    a[:,:,:3][m]=palette[((c.astype(np.int32)[:,None,:]-palette[None,:,:])**2).sum(2).argmin(1)][inv];ims[i]=Image.fromarray(a)
  cols=min(8,len(ims));sheet=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*h));keys=[];bounds=[]
  for i,im in enumerate(ims):
   box=im.getbbox();assert box;bounds.append(box);r=[i%cols*w,i//cols*h,w,h];sheet.paste(im,r[:2]);key='g44_'+name.replace('/','_')+'_'+str(i);keys.append(key)
   assets[key]={'file':(O/(name.replace('/','_')+'.png')).relative_to(G).as_posix(),'rect':r,'size':[w,h],'anchor':root,'bounds':box,'provider':'PixelLab','bank':name,'phase':i,'drawScale':1}
   if name.startswith('gosfar/'):
    assets[key]['muzzle']=j.get('muzzle',[80,103])
  sheet.save(O/(name.replace('/','_')+'.png'))
  banks[name]={'frames':keys,'fps':j.get('fps',10),'loop':j.get('loop',True),'duration':len(keys)/j.get('fps',10),'origin':root,'size':[w,h],'palette_locked':name.startswith('gosfar/'),'provider':'PixelLab'}
  p=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*(h+18)),(20,28,36,255));d=ImageDraw.Draw(p)
  for i,im in enumerate(ims):
   x=i%cols*w;y=i//cols*(h+18);ghost=ims[(i-1)%len(ims)].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:a//4));p.alpha_composite(ghost,(x,y));p.alpha_composite(im,(x,y));d.line((x+root[0],y,x+root[0],y+h),fill='#44c5b2');d.line((x,y+root[1],x+w,y+root[1]),fill='#caab72');d.text((x+3,y+h),str(i),fill='white')
  rd=O/'review';rd.mkdir(exist_ok=True);p.convert('RGB').save(rd/(name.replace('/','_')+'-onion.jpg'))
  review.append({'bank':name,'size':[w,h],'root':root,'bounds':bounds,'frames':len(ims),'provider':'PixelLab','normalization':'Fixed canvas, one common root, no frame fitting or resizing; shared armor palette.'})
 out={'build':'overdrive1018-gosfar44-r4','assets':assets,'banks':banks,'generation_jobs':jobs,'counts':{'banks':len(banks),'frames':len(assets)}}
 (O/'manifest.json').write_text(json.dumps(out,indent=2));(O/'manifest.js').write_text('window.TD_GOSFAR43_ART='+json.dumps(out,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,window.TD_GOSFAR43_ART.assets);\n')
 (O/'review.json').write_text(json.dumps(review,indent=2))
 src=O/'source';src.mkdir(exist_ok=True)
 if W!=src:
  shutil.copy2(W/'jobs.json',src/'jobs.json');shutil.copytree(raw,src/'raw',dirs_exist_ok=True)
  for p in W.glob('*-corrected.png'):shutil.copy2(p,src/p.name)
  for p in W.glob('*pixel-edits.json'):shutil.copy2(p,src/p.name)
  for name in ['provenance.json','wall-seal-edits.json','README.txt']:
   if (W/name).exists():shutil.copy2(W/name,src/name)
 print(out['counts'])
if '--fetch' in sys.argv:fetch()
if '--build' in sys.argv:build()
