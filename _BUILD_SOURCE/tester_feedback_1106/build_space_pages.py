"""Lossless Stage5 paging. Verify original RGBA/visible pixels per cell; retain masters."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
D=R/'assets/game/shared/combat/space_pages_1106';D.mkdir(parents=True,exist_ok=True)
s=(R/'assets/stage5_amplify_art_1101.js').read_text(encoding='utf8');A=json.loads(s[s.index('{'):s.rindex('}')+1])
banks={b['key']:b for b in [*A['banks'].values(),*(m['bank']for m in A['models'].values())]}
s=(R/'assets/enemy_flight_art_1031.js').read_text(encoding='utf8');F=json.loads(s[s.index('{'):s.rindex('}')+1])
extra=F['models']['af_s5interceptor'];banks[extra['key']]=extra
colors={'#ffffff':'white','#ff3b30':'red','#83d9ff':'ice','#000000':'shadow'}
out={'version':1,'maxPage':1536,'banks':{},'pages':{},'sourceBytes':0,'basePageBytes':0,'pixelChecks':0,'tintChecks':0}
for key,B in banks.items():
 im=Image.open(R/B['path']).convert('RGBA');c=B['cell'];cols=im.width//c;rows=im.height//c
 assert im.width%c==im.height%c==c%2==0
 records=[];unique=[];seen={}
 for y in range(rows):
  for x in range(cols):
   cell=im.crop((x*c,y*c,(x+1)*c,(y+1)*c));box=cell.getbbox()
   if not box:records.append(None);continue
   box=(box[0]//2*2,box[1]//2*2,min(c,(box[2]+1)//2*2),min(c,(box[3]+1)//2*2));crop=cell.crop(box)
   sig=(box,hashlib.sha256(crop.tobytes()).hexdigest())
   if sig not in seen:seen[sig]=len(unique);unique.append({'im':crop,'offset':box[:2]})
   records.append(seen[sig])
 pages=[];page=Image.new('RGBA',(1536,1536));x=y=2;rowH=0;usedW=usedH=2
 def save():
  k='sp116_'+key+'_'+str(len(pages));part=page.crop((0,0,(usedW+1)//2*2,(usedH+1)//2*2));entry={'key':k,'variants':{}}
  for suffix,color in [('base',None),*[(v,k)for k,v in colors.items()]]:
   image=part if color is None else Image.new('RGBA',part.size,color)
   if color:image.putalpha(part.getchannel('A'))
   name=k+'_'+suffix+'.png';image.save(D/name,optimize=True)
   pk=k+'_'+suffix;out['pages'][pk]={'path':(D/name).relative_to(R).as_posix(),'w':image.width,'h':image.height,'sha256':hashlib.sha256((D/name).read_bytes()).hexdigest()}
   entry['variants'][color or 'base']=pk
  out['basePageBytes']+=part.width*part.height*4;pages.append(entry)
 for i in sorted(range(len(unique)),key=lambda n:(-unique[n]['im'].height,-unique[n]['im'].width)):
  u=unique[i];pic=u['im'];w,h=pic.size
  if x+w+2>1536:x=2;y+=rowH+2;rowH=0
  if y+h+2>1536:save();page=Image.new('RGBA',(1536,1536));x=y=2;rowH=0;usedW=usedH=2
  page.paste(pic,(x,y));u['rect']=[len(pages),x,y,w,h,*u['offset']];x+=w+2;rowH=max(rowH,h);usedW=max(usedW,x);usedH=max(usedH,y+h+2)
 if unique:save()
 cells=[None if i is None else unique[i]['rect']for i in records];decoded={}
 for i,r in enumerate(cells):
  original=im.crop((i%cols*c,i//cols*c,(i%cols+1)*c,(i//cols+1)*c));a=np.asarray(original);visible=a[:,:,3]>0
  for color in ['base',*colors]:
   restored=Image.new('RGBA',(c,c))
   if r:
    p,sx,sy,w,h,ox,oy=r;pk=pages[p]['variants'][color]
    if pk not in decoded:decoded[pk]=Image.open(R/out['pages'][pk]['path']).convert('RGBA')
    restored.paste(decoded[pk].crop((sx,sy,sx+w,sy+h)),(ox,oy))
   z=np.asarray(restored);assert np.array_equal(a[:,:,3],z[:,:,3]),(key,i,color,'alpha')
   if color=='base':assert np.array_equal(a[:,:,:3][visible],z[:,:,:3][visible]),(key,i,'pixels');out['pixelChecks']+=1
   else:assert np.all(z[:,:,:3][visible]==np.array(tuple(int(color[j:j+2],16)for j in [1,3,5]))),(key,i,'tint');out['tintChecks']+=1
 out['banks'][key]={'cell':c,'cols':cols,'rows':rows,'pages':pages,'cells':cells,'source':B['path'],'sourceSHA':hashlib.sha256((R/B['path']).read_bytes()).hexdigest()}
 out['sourceBytes']+=im.width*im.height*4
 print('PACKED',key,len(cells),'cells',len(pages),'pages',flush=True)
(R/'assets/space_pages_art_1106.js').write_text('"use strict";\nconst SP116_ART='+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
(D/'manifest.json').write_text(json.dumps(out,separators=(',',':')),encoding='utf8')
(W/'space-pages-result.json').write_text(json.dumps({k:v for k,v in out.items()if k not in ['banks','pages']},indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items()if k not in ['banks','pages']}),flush=True)
