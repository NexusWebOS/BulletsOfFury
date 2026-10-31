"""Export reviewed PixelLab frames with one canvas, one scale and palette per bank."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
G=Path(__file__).resolve().parents[3];O=G/'expansion/topdown/art/combat42';W=O/'source';O.mkdir(exist_ok=True)
assets={};banks={};reviews=[]
def pack(name,files,origin,fps=12,loop=True,palette_source=None):
 if not files:return
 ims=[Image.open(p).convert('RGBA') for p in files];size=ims[0].size;assert all(im.size==size for im in ims);assert not size[0]%2 and not size[1]%2
 ref=Image.open(palette_source or files[0]).convert('RGBA');a=np.array(ref);colors,counts=np.unique(a[a[:,:,3]>180,:3],axis=0,return_counts=True);pal=colors[np.argsort(-counts)[:192]].astype(np.int32)
 norm=[];bounds=[];keys=[];w,h=size;cols=min(8,len(ims));sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(ims)/cols)))
 for i,im in enumerate(ims):
  a=np.array(im);mask=a[:,:,3]>160;rgb=a[:,:,:3][mask];uniq,inv=np.unique(rgb,axis=0,return_inverse=True);nearest=pal[((uniq.astype(np.int32)[:,None,:]-pal[None,:,:])**2).sum(2).argmin(1)];a[:,:,:3][mask]=nearest[inv];a[:,:,3]=np.where(mask,255,0);im=Image.fromarray(a);b=im.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<w and b[3]<h,(name,i,b);norm.append(im);bounds.append(b)
  rect=[i%cols*w,i//cols*h,w,h];sheet.paste(im,rect[:2]);k='od42_'+name.replace('/','_')+'_'+str(i);keys.append(k);assets[k]={'file':(O/(name.replace('/','_')+'.png')).relative_to(G).as_posix(),'rect':rect,'size':[w,h],'anchor':origin,'bounds':list(b),'provider':'PixelLab','drawScale':1,'bank':name,'phase':i}
 path=O/(name.replace('/','_')+'.png');sheet.save(path);banks[name]={'frames':keys,'fps':fps,'loop':loop,'duration':len(ims)/fps,'origin':origin,'size':[w,h],'palette_locked':True}
 # Fixed-root previous/current/next onion contact; no individual frame fitting.
 contact=Image.new('RGBA',(w*min(8,len(ims)),(h+22)*math.ceil(len(ims)/8)),(29,38,49,255));pen=ImageDraw.Draw(contact)
 for i,im in enumerate(norm):
  x=i%8*w;y=i//8*(h+22);prev=norm[max(0,i-1)].copy();prev.putalpha(prev.getchannel('A').point(lambda v:v//4));contact.alpha_composite(prev,(x,y));contact.alpha_composite(im,(x,y));pen.line((x+origin[0],y,x+origin[0],y+h),fill='#3bc6b5');pen.line((x,y+origin[1],x+w,y+origin[1]),fill='#d4ac65');pen.text((x+4,y+h+4),str(i),fill='white')
 contact.convert('RGB').save(O/(name.replace('/','_')+'-onion.jpg'))
 reviews.append({'bank':name,'frames':len(ims),'canvas':size,'origin':origin,'bounds':bounds,'heightRange':[min(b[3]-b[1] for b in bounds),max(b[3]-b[1] for b in bounds)],'method':'Common fixed canvas/root; nearest seed palette; hard alpha; no per-frame resizing.','source_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in files]})
pack('yuri_back42/traverse/east',sorted((W/'yuri-traverse').glob('*.png')),[80,136],24,False,W/'yuri-back-clean.png')
# Recoil takes are quarantined: raised hands / invented handheld guns fail the fixed-grip contract.
# The approved rear traverse remains active; do not disguise those takes with code transforms.
for name in ['phoenix','hotwire','neil']:
 folder=W/(name+'-drive-retry');folder=folder if folder.exists() else W/(name+'-drive')
 # First Phoenix/Neil takes were rejected (unrequested effects / pistol shape loss).
 if name!='hotwire' and not folder.name.endswith('retry'):continue
 pack(name+'/sit/east',sorted(folder.glob('*.png')),[64,120],8 if name!='neil' else 14,True,W/(name+'-drive.png'))
out={'build':'overdrive1018-combat42-r5','assets':assets,'banks':banks,'counts':{'banks':len(banks),'frames':len(assets)}}
(O/'manifest.json').write_text(json.dumps(out,indent=2));(O/'manifest.js').write_text('window.TD_COMBAT42_ART='+json.dumps(out,separators=(',',':'))+';Object.assign(window.TD_NIGHT39_ART.assets,window.TD_COMBAT42_ART.assets);Object.assign(window.TD_NIGHT39_ART.banks,window.TD_COMBAT42_ART.banks);Object.assign(window.TD_ASSAULT_ART.assets,window.TD_COMBAT42_ART.assets);\n')
(O/'review.json').write_text(json.dumps(reviews,indent=2));print(out['counts'])
