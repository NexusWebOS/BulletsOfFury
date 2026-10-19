"""Own the revised Stage 8 boss art. No atlas mutation or per-pose scaling."""
from pathlib import Path
import json,math,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stage8_identity_1018';OLD=R/'_ART_SOURCES/stage8_pixellab_1018'
O=R/'assets/game/levels/stage_08/boss/identity_1018';Q=R/'_shots/stage8_identity_1018';REF=Q/'refs'
O.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
def save(key,im,pivot=None):
 assert im.width%2==im.height%2==0
 p=O/(key+'.png');im.save(p,optimize=True)
 return dict(key=key,path=p.relative_to(R).as_posix(),w=im.width,h=im.height,pivot=pivot or [im.width//2,im.height//2],bounds=list(im.getbbox() or (0,0,0,0)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def preview(name,frames):
 w,h=frames[0].size;out=Image.new('RGB',(w*4,(h+18)*math.ceil(len(frames)/4)),'#101722');d=ImageDraw.Draw(out)
 for i,im in enumerate(frames):
  x=i%4*w;y=i//4*(h+18);out.paste(im,(x,y),im);d.text((x+4,y+h),str(i),fill='white')
 out.save(Q/(name+'-sheet.png'))
 onion=Image.new('RGBA',(w,h))
 for i in sorted({0,len(frames)//4,len(frames)//2,3*len(frames)//4,len(frames)-1}):
  layer=frames[i].copy();layer.putalpha(layer.getchannel('A').point(lambda v:round(v*.22)));onion=Image.alpha_composite(onion,layer)
 bg=Image.new('RGBA',(w,h),'#101722');Image.alpha_composite(bg,onion).save(Q/(name+'-onion.png'))
 frames[0].save(Q/(name+'.gif'),save_all=True,append_images=frames[1:],duration=90,loop=0,disposal=2)
def build():
 data=dict(volcano={},hammer={},clips={})
 # Six anatomical render plates, four damage owners. All sum back to the
 # exact PixelLab master; no second pasted limb or invented armor.
 im=Image.open(OLD/'masters/volcano.png').convert('RGBA');a=np.array(im);mask=np.zeros((256,256),np.uint8)
 polygons={
  'legL':[(71,157),(122,157),(126,256),(45,256)],
  'legR':[(134,157),(180,157),(207,256),(129,256)],
  'left':[(0,97),(79,96),(88,120),(76,155),(57,182),(0,211)],
  'right':[(174,95),(256,94),(256,225),(194,225),(178,190),(168,143)],
  'head':[(101,49),(153,49),(158,99),(140,113),(111,113),(98,100)]}
 ids=['core','legL','legR','left','right','head']
 for i,k in enumerate(ids[1:],1):
  z=Image.new('L',(256,256));ImageDraw.Draw(z).polygon(polygons[k],fill=255);mask[np.asarray(z)>0]=i
 rebuild=np.zeros_like(a)
 for i,k in enumerate(ids):
  b=np.zeros_like(a);b[mask==i]=a[mask==i];rebuild[mask==i]=b[mask==i];out=Image.new('RGBA',(320,320));out.paste(Image.fromarray(b),(32,32));data['volcano'][k]=save('v19_volcano_'+k,out)
 assert np.array_equal(a,rebuild)
 data['volcanoMounts']={'core':[160,160],'legL':[120,203],'legR':[196,203],'left':[113,144],'right':[210,143],'head':[160,112]}
 data['volcanoMuzzles']={'left':[70,204],'right':[245,207]}
 meta=json.loads((REF/'meta.json').read_text())
 # These are the real Stage 5 side-swing poses; one luminance-preserving
 # blue-to-violet/red palette conversion supplies the symbiote variant.
 for bank in ['swing_left','swing_right']:
  data['hammer'][bank]=[];frames=[]
  for i,row in enumerate(meta['hm'][bank]):
   x=Image.open(REF/(row['key']+'.png')).convert('RGBA');v=np.array(x);rgb=v[:,:,:3].astype(float)
   pick=(v[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,1]*1.1)
   lum=rgb@np.array([.2126,.7152,.0722]);ramp=np.stack([lum*1.55,lum*.68,lum*1.28],2);ramp*=np.minimum(1,255/np.maximum(ramp.max(2),1))[:,:,None]
   v[pick,:3]=np.rint(ramp[pick]).astype(np.uint8);x=Image.fromarray(v);frames.append(x)
   data['hammer'][bank].append({**save('v19_hammer_'+bank+f'_{i:02}',x,row['pivot']), 'tip':row['tip']})
  preview(bank,frames)
 jobs=json.loads((S/'jobs.json').read_text())
 for name,job in jobs.items():
  paths=sorted((S/'returned'/name).glob('frame_*.png'))
  if not paths:
   if '--available' in sys.argv:continue
   raise AssertionError('Missing completed bank '+name)
  frames=[Image.open(p).convert('RGBA') for p in paths]
  if len(frames)==job['count']+1:frames=frames[1:]
  assert len(frames)==job['count'],(name,len(frames))
  if name=='colossus_death':
   # The first twenty real poses preserve the detailed boss, its agony and
   # armor fracture. Reject the model's flat clover-shaped blast tail;
   # the game's authored detailed explosions own the subsequent blast.
   frames=frames[:20]
   for i in range(20,32):
    stale=O/f'v19_colossus_death_{i:02}.png'
    if stale.exists():stale.unlink()
  rows=[];images=[]
  for i,frame in enumerate(frames):
   assert frame.size==(256,256),(name,frame.size)
   arr=np.array(frame);assert (arr[:,:,3]>200).sum()<256*256*.90,(name,i,'opaque blank')
   canvas=Image.new('RGBA',(320,320));canvas.paste(frame,(32,32));row=save('v19_'+name+f'_{i:02}',canvas)
   if name in ['colossus_roar','colossus_scythe']:
    rgba=np.array(canvas);yy,xx=np.indices((320,320));roles=np.where((xx<131)&(yy>50),1,np.where((xx>191)&(yy>50),2,0));layers={};rebuild=np.zeros_like(rgba)
    for j,part in enumerate(['core','left','right']):
     z=np.zeros_like(rgba);z[roles==j]=rgba[roles==j];rebuild[roles==j]=z[roles==j];layers[part]=save('v19_'+name+'_'+part+f'_{i:02}',Image.fromarray(z))
    assert np.array_equal(rebuild,rgba);row['layers']=layers
   rows.append(row);images.append(canvas)
  # A defeated body ends on two empty cells; those are an authored terminal
  # hold, not duplicated motion counted as additional generated poses.
  if job['count']>1:
   unique=len({x.tobytes() for x in images});assert unique>=len(images)-1 and unique>=16,(name,unique)
  data['clips'][name]={'frames':rows,'fps':12};preview(name,images)
 (R/'assets/stage8_identity_art_1018.js').write_text('"use strict";\nconst V19_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 (S/'registration.json').write_text(json.dumps({'frame':[320,320],'pivot':[160,160],'scale':1,'volcanoReconstructsMaster':True,'clips':{k:len(v['frames']) for k,v in data['clips'].items()}},indent=2))
 print(json.dumps({'files':len(list(O.glob('*.png'))),'clips':{k:len(v['frames']) for k,v in data['clips'].items()},'bytes':sum(p.stat().st_size for p in O.glob('*.png'))}))
if __name__=='__main__':build()
