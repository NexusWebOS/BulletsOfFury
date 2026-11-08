"""Pre-author the exact existing Razorwake shadows and opaque hit masks.
Original art, cells, headings, collision threshold and sprite unit are unchanged.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np,gc
R=Path(__file__).resolve().parents[1];W=R/'_BUILD_SOURCE/furious_perf_1104';W.mkdir(exist_ok=True)
D=R/'assets/game/levels/stage_06/boss/performance_1104';D.mkdir(exist_ok=True)
s=(R/'assets/furious_encounters_art_1102.js').read_text(encoding='utf8');art=json.loads(s.split('const FB112_ART=',1)[1].rsplit(';',1)[0])
out=dict(owner='_BUILD_SOURCE/build_furious_perf_1104.py',maskPath='assets/game/levels/stage_06/boss/performance_1104/opaque_masks.bin',masks={},shadows={},pages={},sources={})
payload=bytearray();mask_seen={};unique=[];shadow_seen={};checked=0
names=['razor_roll','razor_body','thunder_body','razor_gun0','razor_gun1']+['thunder_gun'+str(i)for i in range(4)]+['thunder_pressure0','thunder_pressure1']
for name in names:
 B=art['banks'][name];path=R/B['path'];out['sources'][name]=dict(path=B['path'],sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 im=Image.open(path).convert('RGBA');alpha=im.getchannel('A');cell=B['cell'];entries=[];shadows=[]
 for n in range(B['frames']*B['dirs']):
  x=n%B['cols']*cell;y=n//B['cols']*cell;a=np.asarray(alpha.crop((x,y,x+cell,y+cell)));mask=a>24
  yy,xx=np.nonzero(mask)
  if len(xx):
   box=(int(xx.min())//2*2,int(yy.min())//2*2,min(cell,(int(xx.max())+2)//2*2),min(cell,(int(yy.max())+2)//2*2))
   x0,y0,x1,y1=box;bits=np.packbits(mask[y0:y1,x0:x1].reshape(-1),bitorder='little').tobytes();sig=(box,hashlib.sha256(bits).hexdigest())
   if sig not in mask_seen:mask_seen[sig]=[x0,y0,x1-x0,y1-y0,len(payload)];payload.extend(bits)
   entry=mask_seen[sig];restored=np.zeros_like(mask);restored[y0:y1,x0:x1]=np.unpackbits(np.frombuffer(payload,dtype=np.uint8,count=len(bits),offset=entry[4]),bitorder='little')[:(x1-x0)*(y1-y0)].reshape(y1-y0,x1-x0)
   assert np.array_equal(mask,restored),(name,n)
   entries.append(entry)
  else:entries.append(None)
  checked+=1
  if name not in ['razor_body','razor_roll']:continue
  # Canvas's rgba(...,.45) is quantized to 115/255, then source-in preserves
  # the original per-pixel alpha. Store that result rather than executing it in combat.
  sa=np.floor(a.astype(np.float32)*(115/255)+.5).astype('uint8');ys,xs=np.nonzero(sa)
  if not len(xs):shadows.append(None);continue
  box=(int(xs.min())//2*2,int(ys.min())//2*2,min(cell,(int(xs.max())+2)//2*2),min(cell,(int(ys.max())+2)//2*2));x0,y0,x1,y1=box
  rgba=np.zeros((y1-y0,x1-x0,4),dtype=np.uint8);rgba[:,:,:3]=[0,4,9];rgba[:,:,3]=sa[y0:y1,x0:x1];rgba[rgba[:,:,3]==0]=0
  sig=(box,hashlib.sha256(rgba.tobytes()).hexdigest())
  if sig not in shadow_seen:shadow_seen[sig]=len(unique);unique.append(dict(image=Image.fromarray(rgba),offset=[x0,y0]))
  shadows.append(shadow_seen[sig])
 out['masks'][name]=dict(cell=cell,dirs=B['dirs'],frames=B['frames'],cells=entries)
 if shadows:out['shadows'][name]=dict(cell=cell,cells=shadows)
 print('PREBUILT',name,len(entries),'masks',flush=True);del im,alpha;gc.collect()
page=Image.new('RGBA',(1536,1536));x=y=2;row=0;usedW=usedH=2;page_id=0
def save_page():
 key='fb114_shadow_'+str(page_id);img=page.crop((0,0,(usedW+1)//2*2,(usedH+1)//2*2));p=D/(key+'.png');img.save(p,optimize=True)
 out['pages'][key]=dict(path='assets/game/levels/stage_06/boss/performance_1104/'+p.name,w=img.width,h=img.height,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
for i in sorted(range(len(unique)),key=lambda i:(-unique[i]['image'].height,-unique[i]['image'].width)):
 u=unique[i];img=u['image'];cw,ch=img.size
 if x+cw+2>1536:x=2;y+=row+2;row=0
 if y+ch+2>1536:save_page();page_id+=1;page=Image.new('RGBA',(1536,1536));x=y=2;row=0;usedW=usedH=2
 page.paste(img,(x,y));u['rect']=['fb114_shadow_'+str(page_id),x,y,cw,ch,*u['offset']];x+=cw+2;row=max(row,ch);usedW=max(usedW,x);usedH=max(usedH,y+ch+2)
if unique:save_page()
for bank in out['shadows'].values():bank['cells']=[None if n is None else unique[n]['rect']for n in bank['cells']]
out['render']={};render_checks=0
# Small source-pixel pages avoid uploading/decoding a 300 MB roll sheet on its
# first visible pose. Deduplication retains a full common canvas in metadata.
for name in ['razor_body','razor_hit','razor_flow','razor_roll','razor_roll_hit','exhaust']:
 B=art['banks'][name];im=Image.open(R/B['path']).convert('RGBA');cell=B['cell'];tiles=[];seen={};entries=[]
 for n in range(B['frames']*B['dirs']):
  x=n%B['cols']*cell;y=n//B['cols']*cell;tile=im.crop((x,y,x+cell,y+cell));box=tile.getbbox()
  if box is None:entries.append(None);continue
  x0,y0,x1,y1=box;box=(x0//2*2,y0//2*2,min(cell,(x1+1)//2*2),min(cell,(y1+1)//2*2));crop=tile.crop(box);sig=(box,hashlib.sha256(crop.tobytes()).hexdigest())
  if sig not in seen:seen[sig]=len(tiles);tiles.append(dict(image=crop,offset=box[:2]))
  entries.append(seen[sig])
 rp=Image.new('RGBA',(1536,1536));rx=ry=2;rh=0;rw_used=rh_used=2;pn=0;render_pages=[]
 def save_render():
  key='fb114_'+name+'_'+str(pn);img=rp.crop((0,0,(rw_used+1)//2*2,(rh_used+1)//2*2));p=D/(key+'.png');img.save(p,optimize=True)
  out['pages'][key]=dict(path='assets/game/levels/stage_06/boss/performance_1104/'+p.name,w=img.width,h=img.height,sha256=hashlib.sha256(p.read_bytes()).hexdigest());render_pages.append(key)
 for i in sorted(range(len(tiles)),key=lambda i:(-tiles[i]['image'].height,-tiles[i]['image'].width)):
  u=tiles[i];tile=u['image'];cw,ch=tile.size
  if rx+cw+2>1536:rx=2;ry+=rh+2;rh=0
  if ry+ch+2>1536:save_render();pn+=1;rp=Image.new('RGBA',(1536,1536));rx=ry=2;rh=0;rw_used=rh_used=2
  rp.paste(tile,(rx,ry));u['rect']=['fb114_'+name+'_'+str(pn),rx,ry,cw,ch,*u['offset']];rx+=cw+2;rh=max(rh,ch);rw_used=max(rw_used,rx);rh_used=max(rh_used,ry+ch+2)
 if tiles:save_render()
 rects=[None if n is None else tiles[n]['rect']for n in entries];decoded={k:Image.open(D/(k+'.png')).convert('RGBA')for k in render_pages}
 for n,r in enumerate(rects):
  restored=Image.new('RGBA',(cell,cell))
  if r:restored.paste(decoded[r[0]].crop((r[1],r[2],r[1]+r[3],r[2]+r[4])),(r[5],r[6]))
  original=np.asarray(im.crop((n%B['cols']*cell,n//B['cols']*cell,n%B['cols']*cell+cell,n//B['cols']*cell+cell)));actual=np.asarray(restored);visible=original[:,:,3]>0
  assert np.array_equal(original[:,:,3],actual[:,:,3])and np.array_equal(original[:,:,:3][visible],actual[:,:,:3][visible]),(name,n)
  render_checks+=1
 out['render'][B['key']]=dict(cell=cell,cells=rects,pages=render_pages,source=B['path'],sourceSHA256=hashlib.sha256((R/B['path']).read_bytes()).hexdigest())
 print('EXACT_RENDER_PAGES',name,len(rects),len(tiles),len(render_pages),flush=True);del im,decoded;gc.collect()
out['verifiedRenderCells']=render_checks
(D/'opaque_masks.bin').write_bytes(payload);out['maskBytes']=len(payload);out['maskSHA256']=hashlib.sha256(payload).hexdigest();out['verifiedMasks']=checked;out['uniqueMasks']=len(mask_seen);out['uniqueShadows']=len(unique)
(D/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');(R/'assets/furious_perf_art_1104.js').write_text('"use strict";\nconst FB114_ART='+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
print('EXACT_MASK_CHECKS',checked,'MASK_BYTES',len(payload),'SHADOWS',len(unique),'PAGES',len(out['pages']),flush=True)
