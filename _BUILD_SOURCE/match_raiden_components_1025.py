"""Register newly generated vehicle-specific complete modules, never tint shared art."""
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects,distance_transform_edt

def extract(im,rows,columns):
 a=np.asarray(im);lab,_=label(a[:,:,3]>24);objects=[]
 for i,s in enumerate(find_objects(lab),1):
  if s is not None:
   n=np.count_nonzero(lab[s]==i)
   if n>2000:objects.append((n,i,s))
 objects=sorted(objects,reverse=True)[:rows*columns]
 assert len(objects)==rows*columns,(im.size,len(objects),rows,columns)
 objects.sort(key=lambda x:(x[2][0].start+x[2][0].stop)/2)
 objects=sum([sorted(objects[i:i+columns],key=lambda x:x[2][1].start)for i in range(0,len(objects),columns)],[])
 seeds=np.zeros(lab.shape,dtype=np.int16)
 for number,(_,i,s)in enumerate(objects,1):seeds[lab==i]=number
 _,near=distance_transform_edt(seeds==0,return_indices=True);owners=seeds[tuple(near)];crops=[]
 for number,(_,i,s)in enumerate(objects,1):
  x0,y0=max(0,s[1].start-4),max(0,s[0].start-4);x1,y1=min(im.width,s[1].stop+4),min(im.height,s[0].stop+4)
  p=a[y0:y1,x0:x1].copy();p[owners[y0:y1,x0:x1]!=number]=0
  crops.append((Image.fromarray(p),[x0,y0,x1-x0,y1-y0]))
 return crops

def apply(b,catalog):
 root=b.S/'matching';old={p['id']:p for p in catalog['components']}
 catalog['components']=[p for p in catalog['components']if p['role']=='base'or p['kit']=='running_gear']
 catalog['kits']=[dict(id='running_gear',name='Olive running gear',palette='olive',parts=[p['id']for p in catalog['components']if p['kit']=='running_gear'])]
 for p in catalog['components']:
  if p['kit']=='running_gear':p['palette']='olive'
 def register(pid,kit,key,name,crop,rect,path,scale,owner,palette):
  size=[round(v*scale)for v in crop.size];frame=Image.new('RGBA',(512,512));offset=[(512-v)//2 for v in size]
  assert min(offset)>=4,(pid,size)
  frame.paste(crop.resize(size,Image.Resampling.NEAREST),offset)
  # Solid hardware has no translucent effects. Export a crisp alpha silhouette
  # from the preserved generated alpha; leave every retained RGB pixel intact.
  a=np.array(frame);a[:,:,3]=np.where(a[:,:,3]>=200,255,0);a[a[:,:,3]==0]=0;frame=Image.fromarray(a)
  yy,xx=np.where(a[:,:,3]>128);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
  normal=f'components/{pid}.png';native=f'components/{pid}-native.png';hit=f'components/{pid}-hit.png'
  b.save(frame,b.O/normal);b.save(frame.resize((256,256),Image.Resampling.NEAREST),b.O/native)
  white=a.copy();white[:,:,:3]=255;white[a[:,:,3]==0]=0;b.save(Image.fromarray(white),b.O/hit)
  piv=b.pivot(key,bbox)
  if key=='wing_left':piv=[round(bbox[0]+.94*(bbox[2]-bbox[0])),round((bbox[1]+bbox[3])/2)]
  if key=='wing_right':piv=[round(bbox[0]+.06*(bbox[2]-bbox[0])),round((bbox[1]+bbox[3])/2)]
  if kit.startswith('gear_'):piv=[256,256]
  part=dict(id=pid,kit=kit,role=key,name=name,image=normal,native=native,hit=hit,size=[512,512],bbox=bbox,pivot=piv,source=str(path.relative_to(b.R)).replace('\\','/'),source_sha256=b.sha(path),source_rect=rect,source_scale=scale,source_offset=offset,alpha_cutoff=200,owner=owner,palette=palette,largest_central_deck_hole=0,sha256=b.sha(b.O/normal))
  catalog['components'].append(part);return part
 palettes={}
 for palette in ['sand','gunmetal']:
  parts=[]
  for filename,rows,columns,indices in [(palette+'-gear.png',4,3,range(2)),(palette+'-wheels.png',3,3,range(9))]:
   path=root/filename;crops=extract(Image.open(path).convert('RGBA'),rows,columns);common=350/max(max(c.size)for c,_ in crops)
   for i in indices:
    role,name=b.GEAR[len(parts)];crop,rect=crops[i]
    parts.append(register(f'gear_{palette}/{role}','gear_'+palette,role,palette.title()+' '+name,crop,rect,path,common,None,palette))
  palettes[palette]={p['role']:p for p in parts};catalog['kits'].append(dict(id='gear_'+palette,name=palette.title()+' running gear',palette=palette,parts=[p['id']for p in parts]))
 palettes['olive']={p['role']:p for p in catalog['components']if p['kit']=='running_gear'}
 unit_parts={}
 for kit,units in b.KITS.items():
  path=root/(kit+'-modules-clean.png');crops=extract(Image.open(path).convert('RGBA'),3,6)
  for row,(key,name,tier)in enumerate(units):
   bank=crops[row*6:row*6+6];common=350/max(max(c.size)for c,_ in bank);parts=[]
   for role,(crop,rect)in zip(b.roles(kit),bank):parts.append(register(f'matched/{key}/{role}',key,role,name+' — '+b.NAMES[role],crop,rect,path,common,key,key))
   base=old[kit+'/'+key];base['owner']=key;base['palette']=key
   unit_parts[key]={p['role']:p for p in parts};catalog['kits'].append(dict(id=key,name=name+' matched set',base=base['id'],parts=[base['id']]+[p['id']for p in parts]))
 allparts={p['id']:p for p in catalog['components']}
 for u in catalog['units']:
  key=u['id'];base=allparts[u['base']];parts=unit_parts[key];us=u['body_scale'];f=u['frame'];x0,y0,x1,y1=base['bbox'];bh=y1-y0;bw=x1-x0
  palette='sand'if key=='twin_cannon_tank'else'gunmetal'if key=='wheeled_flak'else'olive'
  mounts=b.gear_mounts(key,base,palettes[palette],f,us)
  for m in u['mounts']:
   if m['kind']=='running_gear':continue
   role=old[m['default']]['role'];m=m.copy();m['default']=parts[role]['id']
   candidates=[parts[old[c]['role']]for c in m['compatible']]
   m['compatible']=[p['id']for p in candidates];m['scales']={}
   for c in candidates:
    w,h=c['bbox'][2]-c['bbox'][0],c['bbox'][3]-c['bbox'][1]
    if c['role'].startswith('wing_'):scale=.42*bh/w*us
    elif c['role'].startswith('engine_'):scale=.28*bh/h*us
    elif c['role']in ['cannon_pod','missile_pod']:scale=(.23 if u['kit']in b.AIR else .25)*bh/h*us
    else:scale=m['scale']
    m['scales'][c['id']]=scale
   m['scale']=m['scales'][m['default']]
   if role.startswith('engine_'):m['angle']=0
   mounts.append(m)
  u['mounts']=mounts;u['matched_set']=key;u['gear_palette']=palette if key in b.GROUND else None
  assembled=Image.new('RGBA',(f,f))
  for m in mounts:
   if m.get('layer')=='under':
    c=allparts[m['default']];assembled=Image.alpha_composite(assembled,b.layer(Image.open(b.O/c['image']),f,m['position'],c['pivot'],m['scale'],m['angle']))
  body=b.layer(Image.open(b.O/base['image']),f,u['body_position'],base['pivot'],us);assembled=Image.alpha_composite(assembled,body)
  if u['running_gear']:b.save(assembled,b.O/u['running_gear'])
  for m in mounts:
   if m.get('layer')!='under':
    c=allparts[m['default']];assembled=Image.alpha_composite(assembled,b.layer(Image.open(b.O/c['image']),f,m['position'],c['pivot'],m['scale'],m['angle']))
  b.save(assembled,b.O/u['master']);b.save(assembled.resize((f//2,f//2),Image.Resampling.NEAREST),b.O/u['image'])
 catalog['version']=5;catalog['contract']='24 matched vehicle-specific hardware sets. Compatible choices preserve the hull design and paint. All ground running gear remains independent.'
 prompts=json.loads((root/'prompts.json').read_text());prompts['cleanup']=json.loads((root/'cleanup-prompts.json').read_text());(b.O/'matched-set-prompts.json').write_text(json.dumps(prompts,indent=2)+'\n')
 assert len(catalog['components'])==201
 print('MATCHED: 24 hull-specific sets, 144 matching hardware modules, 33 running-gear modules.',flush=True)

