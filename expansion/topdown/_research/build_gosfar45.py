from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,shutil
W=Path(__file__).resolve().parent;G=W.parents[2]if W.name=='_research'else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=G/'expansion/topdown/art/gosfar45';O.mkdir(parents=True,exist_ok=True)
if not(W/'jobs.json').exists():W=O/'source'
J=json.loads((W/'jobs.json').read_text(encoding='utf-8'));raw=W/'raw'
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>160,255,0);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def images(k):return [clean(Image.open(raw/k/f'{i:03}.png'))for i in range(J[k]['n'])]
def muzzle_for(k,im,root,default):
 if not k.startswith('hotwire/'):return default
 _,weapon,action,di=k.split('/');ax,ay=root
 if action.startswith('prone')or action=='crawl':
  p=raw/f'hotwire/{weapon}/prone/{di}/000.png'
  if p.exists():
   a=np.array(clean(Image.open(p)));yy,xx=np.where(a[:,:,3]>0)
   if di in ['north','south']:
    y=yy.min()if di=='north'else yy.max();return[int(np.median(xx[yy==y])),int(y)]
   if di in ['east','west']:
    x=xx.max()if di=='east'else xx.min();return[int(x),int(np.median(yy[xx==x]))]
 if action in ['fire','run_fire','crouch_fire','draw_forward']or(action=='jump'and di in ['east','west']):
  a=np.array(im);rgb=a[:,:,:3].astype(int);lum=rgb.mean(2);neutral=(rgb.max(2)-rgb.min(2)<32)&(lum>24)&(lum<216)&(a[:,:,3]>0);yy,xx=np.indices(neutral.shape)
  if di=='north':neutral&=(yy<ay-(42 if action=='crouch_fire' else 75))&(abs(xx-ax)<25)
  elif di in ['east','west']:neutral&=(xx>ax+14 if di=='east'else xx<ax-14)&(yy<ay-24)&(yy>(0 if action=='jump'else ay-90))
  else:return default
  ys,xs=np.where(neutral)
  if len(xs):
   if di=='north':y=ys.min();return[int(np.median(xs[ys==y])),int(y)]
   x=xs.max()if di=='east'else xs.min();return[int(x),int(np.median(ys[xs==x]))]
 return default
assets={};banks={};review=[]
palettes={}
for family,keys in {'hotwire':['hotwire/rifle/ready/south','hotwire/eagle/ready/south','hotwire/rifle/ready/north'],'gosfar':['gosfar/ready/south','gosfar/ready/east','gosfar/ready/west']}.items():
 col=np.concatenate([np.array(images(k)[0]).reshape(-1,4)for k in keys]);col=col[col[:,3]>0,:3]
 q=Image.fromarray(col.reshape(1,-1,3)).quantize(colors=192,method=Image.Quantize.MEDIANCUT);pal=np.array(q.getpalette(),dtype=np.int32).reshape(-1,3)[:192]
 palettes[family]=np.concatenate([pal,[[255,255,255],[255,241,164],[255,195,74],[255,122,37]]])
def pack(k,ims,root,fps=12,loop=True,muzzle=None,palette=None):
 if palette is not None:
  for n,im in enumerate(ims):
   a=np.array(im);m=a[:,:,3]>0;c,inv=np.unique(a[:,:,:3][m],axis=0,return_inverse=True);a[:,:,:3][m]=palette[((c.astype(np.int32)[:,None,:]-palette[None,:,:])**2).sum(2).argmin(1)][inv];ims[n]=Image.fromarray(a)
 w,h=ims[0].size;assert w%2==h%2==0 and all(im.size==(w,h)for im in ims),k
 cols=min(8,len(ims));rows=math.ceil(len(ims)/cols);sheet=Image.new('RGBA',(w*cols,h*rows));onion=Image.new('RGBA',(w*cols,(h+18)*rows),(24,34,44,255));d=ImageDraw.Draw(onion);keys=[];bounds=[]
 for i,im in enumerate(ims):
  box=im.getbbox();assert box,k;bounds.append(box);x=i%cols*w;y=i//cols*h;sheet.paste(im,(x,y));key='g45_'+k.replace('/','_')+'_'+str(i);keys.append(key)
  meta={'file':(O/(k.replace('/','_')+'.png')).relative_to(G).as_posix(),'rect':[x,y,w,h],'size':[w,h],'anchor':root,'bounds':list(box),'bank':k,'provider':'PixelLab','phase':i,'drawScale':1}
  socket=muzzle_for(k,im,root,muzzle)
  if socket:meta['muzzle']=socket
  assets[key]=meta;y=i//cols*(h+18);ghost=ims[(i-1)%len(ims)].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:a//4));onion.alpha_composite(ghost,(x,y));onion.alpha_composite(im,(x,y));d.line((x+root[0],y,x+root[0],y+h),fill='#39c4ad');d.line((x,y+root[1],x+w,y+root[1]),fill='#c8a65b');d.text((x+2,y+h),str(i),fill='white')
  if socket:d.line((x+socket[0]-3,y+socket[1],x+socket[0]+3,y+socket[1]),fill='#ff59df');d.line((x+socket[0],y+socket[1]-3,x+socket[0],y+socket[1]+3),fill='#ff59df')
 sheet.save(O/(k.replace('/','_')+'.png'));rd=O/'review';rd.mkdir(exist_ok=True);onion.convert('RGB').save(rd/(k.replace('/','_')+'-onion.jpg'))
 banks[k]={'frames':keys,'fps':fps,'loop':loop,'duration':len(keys)/fps,'origin':root,'size':[w,h],'palette_locked':palette is not None,'provider':'PixelLab'};review.append({'bank':k,'frames':len(keys),'root':root,'bounds':bounds,'size':[w,h],'normalization':'Common physical body unit, fixed canvas/root per bank, binary alpha and shared identity palette; no frame resizing.'})
for k,j in J.items():
 if j.get('source_only')or k.startswith('env/'):continue
 mark=raw/k/'_job.txt'
 if j.get('replace')and(not mark.exists()or mark.read_text()!=j['job']):print('PENDING replacement',k);continue
 if not all((raw/k/f'{i:03}.png').exists()for i in range(j['n'])):print('PENDING',k);continue
 ims=images(k)
 if j.get('replace_frames'):
  source=ims[:]
  for dst,src in j['replace_frames'].items():ims[int(dst)]=source[src].copy()
 if j.get('take'):ims=[ims[i]for i in j['take']]
 root=j.get('root',[64,120]);mu=j.get('muzzle')
 if k=='gosfar/rev/south':continue # Rejected white gun. Approved rotating-barrel firing plates supply the rev below.
 if k=='gosfar/ready/north':ims=[clean(Image.open(raw/'gosfar/north-raised/000.png'))];root=[112,216]
 if k.startswith('gosfar/'):
  di=k.split('/')[-1];rel={'south':[52,-36],'east':[56,-46],'west':[-52,-42],'north':[38,-194]}[di];mu=[root[0]+rel[0],root[1]+rel[1]]
 if k.startswith('hotwire/'):
  di=k.split('/')[-1];action=k.split('/')[2]
  if action=='fire'and len(ims)>5:
   # Keep the authored raise as a separate action. Repeated shots use the aimed portion.
   pack(k.replace('/fire/','/draw_forward/'),ims[:5],root,12,False,palette=palettes['hotwire']);ims=ims[5:]
  dx,dy={'south':(11,-24),'north':(0,-99),'east':(35,-57),'west':(-36,-57),'north-east':(27,-82),'north-west':(-27,-82),'south-east':(32,-33),'south-west':(-32,-33)}[di]
  if action.startswith('prone')or action=='crawl':dy=-13;dx=dx*1.35
  elif action.startswith('crouch'):dy+=27
  mu=[round(root[0]+dx),round(root[1]+dy)]
 fps=j.get('fps',12)
 if '/roll/'in k or '/prone_roll/'in k:fps=len(ims)/.5
 if '/grenade/'in k:fps=len(ims)/.6
 if '/jump/'in k:fps=len(ims)/.65
 if '/reload/'in k:fps=len(ims)/1.1
 pack(k,ims,root,fps,j.get('loop',True),mu,palettes.get(k.split('/')[0]))
# Grey fortress modular pieces share their source crop and baseline.
if all((raw/k/'000.png').exists()for k in ['env/cover-master','env/cover-cracked','env/cover-rubble']):pack('env/cover',[images(k)[0].crop((8,0,88,96))for k in ['env/cover-master','env/cover-cracked','env/cover-rubble']],[40,76],1,False)
if all((raw/k/'000.png').exists()for k in ['env/side-master','env/side-cracked','env/side-open']):pack('env/side',[images(k)[0]for k in ['env/side-master','env/side-cracked','env/side-open']],[48,136],1,False)
if all((raw/k/'000.png').exists()for k in ['env/return-master','env/return-cracked','env/return-rubble']):pack('env/return',[images(k)[0]for k in ['env/return-master','env/return-cracked','env/return-rubble']],[48,136],1,False)
# Retain approved PixelLab hacking and Yuri wall/prone transition plates.
old=json.loads((G/'expansion/topdown/art/gosfar43/manifest.json').read_text(encoding='utf-8'));crew={'hotwire/hack':'hotwire/hack'}
for new,oldkey in crew.items():
 b=old['banks'][oldkey];banks[new]=b
 for key in b['frames']:assets[key]=old['assets'][key]
for w,di in [('rifle','south')]+[('eagle',d)for d in ['north','south','east','west']]:
 b=banks['hotwire/'+w+'/crouch/'+di];banks['hotwire/'+w+'/crouch_walk/'+di]={**b,'note':'Available-art quiet crouch hold; replacement gait intentionally deferred.','held_pose':True}
for di in ['south','east','west','north']:
 k='gosfar/fire/'+di
 if k in banks:
  # Rev uses generated rigid barrel phases that contain no exterior discharge.
  b=banks[k];safe=[]
  for i,key in enumerate(b['frames']):
   im=images(k)[i];a=np.array(im);yy,xx=np.indices(a.shape[:2]);mu=assets[key]['muzzle'];root=assets[key]['anchor'];vx=mu[0]-root[0];vy=mu[1]-(root[1]-70);norm=max(1,math.hypot(vx,vy));projection=(xx-mu[0])*vx/norm+(yy-mu[1])*vy/norm
   fire=(a[:,:,0].astype(int)>180)&(a[:,:,1].astype(int)>60)&(a[:,:,0].astype(int)>a[:,:,1].astype(int)*1.2)&(a[:,:,1].astype(int)>a[:,:,2].astype(int)*1.2)&(a[:,:,3]>0)&(projection>8)&((xx-mu[0])**2+(yy-mu[1])**2<50**2)
   if fire.sum()<3:safe.append(key)
  if len(safe)<2:safe=[b['frames'][0],b['frames'][1]]
  banks['gosfar/rev/'+di]={**b,'frames':safe,'fps':16,'duration':len(safe)/16,'note':'Generated no-discharge barrel phases; exact same whole-body plates.'}
required=['yuri/cover/east','yuri/drop/north','env/cover','env/side','env/return','lift/open','lift/depart','lift/shaft']+['gosfar/fire/'+d for d in ['south','north','east','west']]
missing=[k for k in required if k not in banks]
if missing:raise SystemExit('Not installing incomplete pack: '+', '.join(missing))
out={'build':'overdrive1018-gosfar45-r2','assets':assets,'banks':banks,'generation_jobs':J,'counts':{'banks':len(banks),'frames':len(assets)},'art_limitations':[k for k,b in banks.items()if b.get('held_pose')]}
(O/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8');(O/'manifest.js').write_text('window.TD_GOSFAR45_ART='+json.dumps(out,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,window.TD_GOSFAR45_ART.assets);\n',encoding='utf-8');(O/'review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
print(out['counts'])
