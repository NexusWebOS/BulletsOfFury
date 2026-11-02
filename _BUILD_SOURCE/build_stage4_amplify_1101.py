"""Stage4 replacement source sheets: true authored headings, registered hulls.
Built-in image_gen produced the original PNGs; this deterministic exporter only
normalizes their shared canvas, preserves proportions and registers real cells.
"""
from pathlib import Path
import json,hashlib,math,shutil
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage4_amplify_1101';Q=R/'_shots/stage4_amplify_1101';O=R/'assets/game/levels/stage_04/enemies/amplify_1101'
for p in[S,Q,O]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
FILES={'command':'exec-a6c709c3-3fcf-41c6-bc49-52a7cc87aed9.png','heavyjet':'exec-9ac0246e-3fbb-489c-a967-eb06c8a22320.png','missiletruck':'exec-816950e6-8ad5-441c-a36b-1652d18fd8c7.png','tanker':'exec-f13bf7fb-6d72-4635-9b9f-5dcedb7c8b6c.png','tractor':'exec-08326454-7532-4d0b-ab1d-0621e236ed99.png','sam':'exec-2b161b56-8290-49db-b01c-c47fac1bc109.png','missile':'exec-40fe715b-70a2-4f35-819a-009560d8d7a5.png','command_somer':'exec-49115433-b6a1-4f50-88aa-a33e10c15155.png','heavyjet_somer':'exec-ca715a02-cd02-4f45-ae1e-513a22f5107e.png'}
M={'owner':'_BUILD_SOURCE/build_stage4_amplify_1101.py','tool':'built-in image_gen','models':{},'banks':{},'sources':{},'promptSet':{'style':'Existing encounters_0930 tank metal/pixel style, dark outlines, olive/bronze machinery, fixed even cells, central pivots, transparent padding, no scenery/text/large baked muzzle effects.','command':'New black/burnt-orange camouflage jet with fixed twin machine guns, no modular turrets.32 authored heading/roll/attack/boost frames and8 forward somersault frames.','heavyjet':'Preserve actual heavyjet_identity.png, gray fuselage and fixed parallel missile rails.32 heading/roll/attack/boost frames and8 forward somersault frames.','missiletruck':'Six-wheel olive/bronze truck, two cream/silver missiles with orange bands and red warheads; loaded/empty/reload/rolling poses.','tanker':'Unarmed eight-wheel bronze/olive fuel truck, no weapons,8 wheel/engine animation poses.','tractor':'Tracked olive/bronze combat tractor, fixed forward twin guns at south front,8 tread/recoil poses.','sam':'Distinct mobile three-rail SAM, matching cream/silver/orange/red missiles, sequential emptying/reload and rolling poses.','missile':'Standalone matching cream/silver/orange/red rack missile in16 authored directions.'}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(name,cols,rows):
 p=S/(name+'_source.png')
 if not p.exists():shutil.copyfile(G/FILES[name],p)
 im=Image.open(p).convert('RGBA');a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=80,255,0);im=Image.fromarray(a)
 fs=[];rects=[]
 for y in range(rows):
  for x in range(cols):
   box=[round(x*im.width/cols),round(y*im.height/rows),round((x+1)*im.width/cols),round((y+1)*im.height/rows)];tile=im.crop(box);ar=np.array(tile)
   from scipy.ndimage import label
   ids,_=label(ar[:,:,3]>0);counts=np.bincount(ids.ravel());keep=counts>=max(24,counts[1:].max()*.004);keep[0]=False;ar[:,:,3]=np.where(keep[ids],255,0);fs.append(Image.fromarray(ar));rects.append(box)
 boxes=[f.getbbox()for f in fs];assert all(boxes),name
 cx=max(f.width for f in fs)/2;cy=max(f.height for f in fs)/2
 common=[min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes)];center=[(common[0]+common[2])/2,(common[1]+common[3])/2]
 M['sources'][name]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'size':im.size,'rects':rects,'commonCrop':common,'sourcePivot':center,'requestedCell':[256,256]if name!='missile'else[128,128]}
 return fs,center,max(common[2]-common[0],common[3]-common[1])
def normalized(name,cols,rows,span=154,cell=192,scale=None):
 fs,p,extent=raw(name,cols,rows);k=scale or span/extent;out=[]
 pivots=[]
 for t in fs:
  b=t.getbbox();pivot=[(b[0]+b[2])/2,(b[1]+b[3])/2]
  if name in['missiletruck','tanker','sam']:pivot[1]=b[3]-extent/2
  elif name=='tractor':pivot[1]=b[1]+extent/2
  pivots.append(pivot);t=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',(cell,cell));c.alpha_composite(t,(round(cell/2-pivot[0]*k),round(cell/2-pivot[1]*k)));out.append(c)
 M['sources'][name]['physicalPivots']=pivots
 return out,k
def bank(name,fs):
 c=fs[0].width;assert c%2==0 and all(f.size==(c,c)for f in fs);sheet=Image.new('RGBA',(c*len(fs),c))
 for i,f in enumerate(fs):sheet.alpha_composite(f,(i*c,0))
 p=O/(name+'.webp');sheet.save(p,format='WEBP',lossless=True,method=4);b={'key':'s411_'+name,'path':p.relative_to(R).as_posix(),'cell':c,'frames':len(fs),'pivot':[c//2,c//2],'cells':[[i*c,0,c,c]for i in range(len(fs))],'sha256':sha(p)};M['banks'][name]=b;return b
def preview(name,fs,cols=8):
 c=fs[0].width;rows=math.ceil(len(fs)/cols);im=Image.new('RGB',(cols*c,rows*(c+20)),(10,20,30));d=ImageDraw.Draw(im)
 for i,t in enumerate(fs):x=i%cols*c;y=i//cols*(c+20);im.paste(t,(x,y+20),t);d.text((x+3,y+3),str(i),fill='white')
 im.save(Q/(name+'-contact.jpg'),quality=93)
for name in['command','heavyjet']:
 fs,k=normalized(name,8,4);firstSpan=max(fs[0].getbbox()[2]-fs[0].getbbox()[0],fs[0].getbbox()[3]-fs[0].getbbox()[1]);sf,sp,ex=raw(name+'_somer',4,2);bb=sf[0].getbbox();ratio=firstSpan/max(bb[2]-bb[0],bb[3]-bb[1]);som,_=normalized(name+'_somer',4,2,scale=ratio)
 B={'heading':bank(name+'_heading',fs[:16]),'idle':bank(name+'_idle',[fs[0]]),'attack':bank(name+'_attack',fs[24:28]),'drift':bank(name+'_drift',[fs[1],fs[15]]),'roll':bank(name+'_roll',fs[16:24]),'somer':bank(name+'_somer',som),'boost':bank(name+'_boost',fs[28:32])}
 # Source pose0 has two fixed forward weapons. Per-heading calibration follows
 # the authored image rather than rotating its idle plate at runtime.
 guns=[[65,124],[127,124]]if name=='command'else[[51,121],[133,121]]
 tails=[[75,40],[116,40]]if name=='command'else[[80,45],[111,45]]
 poses=[]
 for d,t in enumerate(fs[:16]):
  a=d*math.tau/16;c=math.cos(a);s=math.sin(a);arr=np.array(t)[:,:,3];points=[]
  for x,y in guns:
   xx=96+(x-96)*c-(y-96)*s;yy=96+(x-96)*s+(y-96)*c;found=[]
   for py in range(max(0,round(yy)-14),min(192,round(yy)+15)):
    for px in range(max(0,round(xx)-14),min(192,round(xx)+15)):
     if arr[py,px]>80:found.append((math.hypot(px-xx,py-yy),px,py))
   _,px,py=min(found);points.append([px,py])
  poses.append(points)
 M['models'][name]={'banks':B,'side':132 if name=='command'else 160,'guns':guns,'gunPoses':poses,'tails':tails,'sourceScale':k,'ground':False,'footprint':[104,112]}
 if name=='heavyjet':
  tp=[]
  from scipy.ndimage import label,find_objects
  for d,t in enumerate(fs[:16]):
   ar=np.array(t);mask=(ar[:,:,2]>100)&(ar[:,:,1]>95)&(ar[:,:,0].astype(float)<ar[:,:,2]*.65)&(ar[:,:,3]>0);lab,_=label(mask);parts=[]
   for j,rect in enumerate(find_objects(lab),1):
    if rect is not None:
     count=int((lab[rect]==j).sum())
     if count>2:parts.append((count,[(rect[1].start+rect[1].stop)/2,(rect[0].start+rect[0].stop)/2]))
   if len(parts)>=2:points=[p for _,p in sorted(parts,reverse=True,key=lambda p:p[0])[:2]]
   else:
    a=d*math.tau/16;points=[[96+(x-96)*math.cos(a)-(y-96)*math.sin(a),96+(x-96)*math.sin(a)+(y-96)*math.cos(a)]for x,y in tails]
   tp.append(points)
  M['models'][name]['tailPoses']=tp
 preview(name,fs+som)
for name in['missiletruck','tanker','tractor','sam']:
 fs,k=normalized(name,8,1,span=160);b=bank(name,fs);bbox=fs[0].getbbox();guns=[];length=0
 if name in['missiletruck','sam']:
  a=np.array(fs[0]);mask=(a[:,:,0]>60)&(a[:,:,0]>a[:,:,1].astype(float)*2)&(a[:,:,0]>a[:,:,2].astype(float)*1.7)&(a[:,:,3]>0)
  from scipy.ndimage import label,find_objects
  lab,_=label(mask);parts=[]
  for i,s in enumerate(find_objects(lab),1):
   if s is not None and(s[0].stop-s[0].start)>4 and(s[1].stop-s[1].start)>3:parts.append((int((lab[s]==i).sum()),s))
  parts=sorted(parts,reverse=True,key=lambda p:p[0])[:2 if name=='missiletruck'else 3];assert len(parts)==(2 if name=='missiletruck'else 3),(name,parts)
  parts.sort(key=lambda p:p[1][1].start)
  # Tail fins and forward red nose delimit the actual mounted missile length.
  length=(bbox[3]-bbox[1])*.45
  for _,s in parts:guns.append([(s[1].start+s[1].stop)/2,s[0].stop-length*.47])
 elif name=='tractor':guns=[[87,174],[108,174]]
 M['models'][name]={'banks':{'sequence':b},'side':136,'guns':guns,'missileLength':length,'ground':True,'footprint':[bbox[2]-bbox[0],bbox[3]-bbox[1]],'sourceScale':k};preview(name,fs)
fs,k=normalized('missile',4,4,span=108,cell=128);angles=[]
for f in fs:
 a=np.array(f);r=(a[:,:,0]>60)&(a[:,:,0]>a[:,:,1].astype(float)*2)&(a[:,:,0]>a[:,:,2].astype(float)*1.7)&(a[:,:,3]>0);yy,xx=np.nonzero(r);angles.append(math.atan2(float(yy.mean())-64,float(xx.mean())-64))
M['projectile']={'bank':bank('rack_missile',fs),'angles':angles,'span':108};preview('missile',fs,4)
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(R/'assets/stage4_amplify_art_1101.js').write_text('"use strict";\nconst S411_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');(S/'generation.json').write_text(json.dumps({'tool':M['tool'],'promptSet':M['promptSet'],'originals':FILES,'reference':'assets/game/shared/combat/encounters_0930/tank_hull.png','identity':'_BUILD_SOURCE/stage4_amplify_1101/heavyjet_identity.png'},indent=2));print('Registered',len(M['models']),'models;',len(M['banks']),'banks;',sum(b['frames']for b in M['banks'].values()),'fixed source frames')
