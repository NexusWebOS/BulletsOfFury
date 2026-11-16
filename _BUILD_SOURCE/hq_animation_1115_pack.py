from pathlib import Path
import json, hashlib, shutil, math
from PIL import Image, ImageDraw
import numpy as np

ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source')
OUT=ROOT/'_shots/hq_animation_1115';OUT.mkdir(parents=True,exist_ok=True)
GEN=ROOT/'_ART_SOURCES/hq_animation_1115'
INSTALL=OUT/'install';ART=INSTALL/'assets/game/shared/cinematics/hq_animation_1115';SRC=INSTALL/'_ART_SOURCES/hq_animation_1115'
ART.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True)
files={p:p+'-source.png'for p in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva','door']}
prompts=json.loads((GEN/'prompts.json').read_text(encoding='utf8'))
meta={'generator':'built-in image_gen','spritecookUsed':False,'pilots':{},'door':None,'normalization':{'alphaCutoff':192,'opaqueBody':True,'perFrameScale':False,'cell':[384,384],'pivot':[192,360],'registration':'median central waist segment and grounded boot baseline; translation only; all source RGB retained for accepted alpha pixels'}}

def savegif(cells,dest,scale=1):
    frames=[]
    for c in cells:
        bg=Image.new('RGB',c.size,'#182a39');bg.paste(c,mask=c.getchannel('A') if c.mode=='RGBA'else None)
        if scale!=1:bg=bg.resize((bg.width*scale,bg.height*scale),Image.Resampling.NEAREST)
        frames.append(bg)
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=110,loop=0,disposal=2)

for pk,filename in files.items():
    shutil.copy2(GEN/filename,SRC/(pk+'-source.png'))
    (SRC/(pk+'-prompt.txt')).write_text(prompts[pk],encoding='utf8',newline='\n')
    if pk=='door':continue
    shutil.copy2(GEN/(pk+'-reference.png'),SRC/(pk+'-reference.png'))
    im=Image.open(GEN/filename).convert('RGBA');cells=[];registration=[]
    for f in range(16):
        x0=(f%4)*im.width//4;x1=(f%4+1)*im.width//4;y0=(f//4)*im.height//4;y1=(f//4+1)*im.height//4
        a=np.array(im.crop((x0,y0,x1,y1)));a[:,:,3]=np.where(a[:,:,3]>=192,255,0);a[a[:,:,3]==0,:3]=0
        body=Image.fromarray(a);box=body.getbbox();assert box,pk
        left,top,right,bottom=box;h=bottom-top;centers=[]
        for yy in range(top+round(h*.48),top+round(h*.58)):
            xs=np.flatnonzero(a[yy,:,3]);segments=np.split(xs,np.flatnonzero(np.diff(xs)>1)+1)
            segments=[s for s in segments if len(s)>4]
            if segments:
                seg=max(segments,key=len);centers.append((int(seg[0])+int(seg[-1]))/2)
        anchorX=round(float(np.median(centers))) if centers else round((left+right)/2)
        dx,dy=192-anchorX,360-bottom
        cell=Image.new('RGBA',(384,384));cell.alpha_composite(body,(dx,dy));assert cell.getbbox() and min(cell.getbbox())>=0
        accepted=int(np.count_nonzero(a[:,:,3]));assert accepted==int(np.count_nonzero(np.array(cell)[:,:,3])),(pk,f,'clipped')
        cells.append(cell);registration.append({'sourceRect':[x0,y0,x1,y1],'sourceGroundPivot':[anchorX,bottom],'translation':[dx,dy],'visibleBounds':cell.getbbox()})
    sheet=Image.new('RGBA',(1536,1536))
    for f,c in enumerate(cells):sheet.alpha_composite(c,((f%4)*384,(f//4)*384))
    dest=ART/(pk+'.webp');sheet.save(dest,lossless=True)
    savegif(cells[:8],OUT/(pk+'-walk.gif'));savegif(cells[8:],OUT/(pk+'-cheer.gif'))
    preview=Image.new('RGB',(1536,1536),'#182a39');preview.paste(sheet,mask=sheet.getchannel('A'));preview.resize((768,768),Image.Resampling.NEAREST).save(OUT/(pk+'-contact.jpg'),quality=93)
    meta['pilots'][pk]={'key':'hq20_'+pk+'_performance','path':str(dest.relative_to(INSTALL)).replace('\\','/'),'w':384,'h':384,'cols':4,'frames':16,'walkFrames':list(range(8)),'cheerFrames':list(range(8,16)),'pivot':[192,360],'bodyHeight':300,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'registration':registration}

# Keep every approved HQ background pixel fixed. The original blue ribbed leaves
# slide physically sideways across a newly generated recessed hangar cavity.
base=Image.open(ROOT/'assets/game/shared/cinematics/hq_return_attack_1114/exterior.webp').convert('RGB').crop((0,0,418,236))
shutil.copy2(GEN/'hq-closed-reference.png',SRC/'hq-closed-reference.png')
opened=Image.open(GEN/files['door']).convert('RGB')
# Measured generated open-mouth rectangle, retaining its wall lights/floor rails.
crop=(666,350,938,477);inside=opened.crop(crop);scale=66/inside.width
inside=inside.resize((66,round(inside.height*scale)),Image.Resampling.LANCZOS)
aperture=(176,90,242,118);cavity=inside.crop((0,(inside.height-28)//2,66,(inside.height-28)//2+28))
original=base.crop(aperture);left=original.crop((0,0,33,28));right=original.crop((33,0,66,28));doors=[]
for f in range(16):
    u=f/15;u=u*u*(3-2*u);delta=round(f+18*u);mouth=cavity.copy();mouth.paste(left,(-delta,0));mouth.paste(right,(33+delta,0));c=base.copy();c.paste(mouth,aperture[:2]);doors.append(c)
sheet=Image.new('RGB',(1672,944))
for f,c in enumerate(doors):sheet.paste(c,((f%4)*418,(f//4)*236))
dest=ART/'door-slide.webp';sheet.save(dest,lossless=True)
meta['door']={'key':'hq20_hq_door','path':str(dest.relative_to(INSTALL)).replace('\\','/'),'w':418,'h':236,'cols':4,'frames':16,'aperture':list(aperture),'generatedCavityRect':list(crop),'panelTravel':33,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'_ART_SOURCES/hq_animation_1115/door-source.png','mechanism':'actual approved two leaves translate into side pockets; fixed scenery and cavity, no crossfade'}
savegif([doors[0]]*5+doors+([doors[-1]]*10)+list(reversed(doors)),OUT/'door-opening.gif',2)
contact=Image.new('RGB',(1254,472))
for i,f in enumerate([0,3,6,9,12,15]):contact.paste(doors[f],((i%3)*418,(i//3)*236))
contact.save(OUT/'doors-contact.jpg',quality=95)
(INSTALL/'assets/hq_animation_art_1115.js').write_text('"use strict";\nconst HQ20_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
(OUT/'art-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8',newline='\n')
print('Prepared nine16-frame actor banks and sixteen physical door frames;144+16 total')
