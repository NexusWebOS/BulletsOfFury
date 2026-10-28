from pathlib import Path
from PIL import Image
from scipy.ndimage import binary_erosion
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';D=W/'armor';D.mkdir(exist_ok=True)
def art(file,var):return json.JSONDecoder().raw_decode((R/'assets'/file).read_text().split('const '+var+'=',1)[1])[0]
A=art('hammer_acting_art_1021.js','HA21_ART');F=art('hammer_furious_art_1022.js','HF22_ART');meta=json.loads((D/'manifest.json').read_text())
def chrome(im):
 a=np.array(im);v=a[:,:,:3].astype(float);lum=v@np.array([.2126,.7152,.0722]);solid=a[:,:,3]>127
 m=binary_erosion(solid)&(v.max(2)-v.min(2)<34)&(lum>56)&(lum<236)
 shine=np.interp(lum,[0,56,80,110,145,190,236,255],[0,56,125,168,202,229,249,255])
 for c,f in enumerate([.94,.98,1.]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 a[:,:,3]=np.where(solid,255,0).astype('uint8');return Image.fromarray(a)
# Rebuild the faulty activation from the approved whole-actor windup. Dark
# outlines, seams, blue sockets and canonical hammer survive in every pose.
sequence=[0,1,2,3,4,5,5,5,5,5,5,4,3,2,1,0];frames=[];rows=[];audit=[]
for i,f in enumerate(sequence):
 q=F['banks']['blue_jump'][f];sheet=Image.open(R/F['sheets'][q['sheet']]['path']).convert('RGBA');x,y,w,h=q['cell'];raw=sheet.crop((x,y,x+w,y+h));plated=chrome(raw)
 a=np.array(raw);b=np.array(plated);yy,xx=np.indices(a.shape[:2]);p=min(1,i/12);mask=(xx-224)**2+(yy-258)**2<(p*480)**2;a[mask]=b[mask];a[:,:,3]=b[:,:,3];im=Image.fromarray(a);frames.append(im)
 key='ht23_activation_'+str(i);rows.append({**q,'key':key,'sheet':'ht23_activation','cell':[i%4*w,i//4*h,w,h],'white':'ht23_activation_hit_'+str(i),'bank':'ht23_activation','frame':i,'bounds':list(im.getbbox())})
 src=np.array(raw);out=np.array(im);solid=src[:,:,3]>127;edge=solid&~binary_erosion(solid);dark=solid&(src[:,:,:3].max(2)<56)
 audit.append({'frame':i,'source':q['key'],'darkSeamsPreserved':bool(np.array_equal(src[:,:,:3][dark],out[:,:,:3][dark])),'edgeRGBPreserved':bool(np.array_equal(src[:,:,:3][edge],out[:,:,:3][edge])),'sameAlpha':bool(np.array_equal(solid,out[:,:,3]>0))})
for suffix in ['', '_hit']:
 sheet=Image.new('RGBA',(1792,1792))
 for i,im in enumerate(frames):
  if suffix:hit=Image.new('RGBA',im.size,'white');hit.putalpha(im.getchannel('A'));im=hit
  sheet.alpha_composite(im,(i%4*448,i//4*448))
 name='activation_clean'+suffix+'.webp';sheet.save(D/name,lossless=True,exact=True);key='ht23_activation'+suffix
 meta['sheets'][key]={'key':'nca_'+key,'path':'assets/game/shared/combat/hammer_tactical_1023/'+name,'sha256':hashlib.sha256((D/name).read_bytes()).hexdigest()}
meta['banks']['activation']=rows;meta['activationAudit']=audit;meta['activationSourceSequence']=sequence
# Keep the pre-existing fallback idle available at its declared baked unit.
src=A['sheets'][A['banks']['blue_idle'][0]['sheet']];im=chrome(Image.open(R/src['path']).convert('RGBA'));c=Image.new('RGBA',(384,512));c.alpha_composite(im.resize((448,448),Image.Resampling.NEAREST),(-32,34));c.save(D/'plated_idle.webp',lossless=True,exact=True);hit=Image.new('RGBA',c.size,'white');hit.putalpha(c.getchannel('A'));hit.save(D/'plated_idle_hit.webp',lossless=True,exact=True)
meta['platedIdle'].update(w=384,h=512,pivot=[192,230],tip=[122,337],bounds=list(c.getbbox()),_hf22=True)
(D/'manifest.json').write_text(json.dumps(meta,indent=2));assert all(all(q[k]for k in ['darkSeamsPreserved','edgeRGBPreserved','sameAlpha'])for q in audit)
print(json.dumps({'cleanActivationFrames':len(rows),'allOutlinesAndSeamsPreserved':True}))
