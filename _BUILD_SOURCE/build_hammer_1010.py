"""Own Hammer's generated loose banks, registration and shipping manifest.

Crop/translate native RGBA only. Each bank uses one proportional scale and one
even output canvas. No per-frame fitting, synthetic tweening or atlas edits.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/hammer_1010'
DEST=ROOT/'assets/game/levels/stage_05/boss/hammer_1010'
DEST.mkdir(parents=True,exist_ok=True)
# Measured reactor and single hammer-head centers, in 384x256 / 320x320 source cells.
RIGHT_CORE=[(180,110),(208,110),(215,110),(215,103),(181,120),(211,120),(224,120),(231,102),(180,105),(211,105),(219,105),(227,98),(187,100),(220,100),(190,83),(188,81)]
RIGHT_TIP=[(90,205),(102,90),(110,102),(169,37),(118,69),(153,70),(102,83),(102,76),(106,107),(80,116),(322,105),(335,100),(346,105),(346,103),(291,169),(88,206)]
# Reactor disc centers (or its seated chest position when the hands occlude it),
# corrected against native rendered poses, rather than anchoring to a visor/LED.
LEFT_CORE=[(164,185),(165,186),(155,171),(172,192),(165,154),(160,154),(163,166),(138,166),(194,126),(175,127),(153,127),(176,131),(207,109),(177,109),(170,108),(164,105)]
LEFT_TIP=[(67,291),(259,168),(221,89),(199,67),(303,161),(286,164),(276,126),(245,100),(69,84),(217,174),(209,174),(27,136),(62,82),(58,154),(49,201),(57,202)]
# The native 1254-square left reel crosses its nominal equal-cell gutters.
# Measured rectangles retain the complete feet and
# hammer without borrowing pixels from the next subject. Export sizes stay even.
LEFT_RECTS=[(0,0,320,350),(320,0,650,350),(650,0,970,350),(970,0,1254,350),
 (0,350,358,637),(358,350,660,637),(660,350,974,637),(974,350,1254,637),
 (0,638,328,935),(328,638,613,935),(613,638,901,935),(901,638,1254,935),
 (0,938,316,1254),(316,938,634,1254),(634,938,952,1254),(952,938,1254,1254)]
CONFIG={
 'shield_form':{'size':(512,512),'pivot':(256,224),'scale':1,'core':True},
 'swing_right':{'size':(512,512),'pivot':(256,224),'scale':1.32,'core':RIGHT_CORE,'tip':RIGHT_TIP,'measure':(384,256)},
 'swing_left':{'size':(512,512),'pivot':(256,224),'scale':1.10,'core':LEFT_CORE,'tip':LEFT_TIP,'measure':(320,320),'rects':LEFT_RECTS,'order':list(range(8))+[10,9,8,11,12,13,14,15]},
 'shield_wall':{'size':(512,256),'pivot':(256,128),'scale':1},
 'core':{'size':(384,384),'pivot':(192,192),'scale':1,'core':True},
 'spike':{'size':(256,512),'pivot':(128,448),'scale':1,'foot':True},
}
def luminous_center(cell,region):
    p=np.asarray(cell);h,w=p.shape[:2];xx,yy=np.meshgrid(np.arange(w),np.arange(h))
    l,t,r,b=region
    mask=(p[:,:,0]>200)&(p[:,:,1]>215)&(p[:,:,2]>235)&(p[:,:,3]>140)&(xx>=l)&(xx<r)&(yy>=t)&(yy<b)
    if not mask.any():return ((l+r)/2,(t+b)/2)
    return (float(np.median(xx[mask])),float(np.median(yy[mask])))
manifest={};registration={}
for name,c in CONFIG.items():
    im=Image.open(SOURCE/'returned'/f'{name}.png').convert('RGBA')
    sw,sh=im.width/4,im.height/4;bank=[];regs=[]
    for i,j in enumerate(c.get('order',range(16))):
        rect=tuple(round(v*(im.width if n%2==0 else im.height)/1254) for n,v in enumerate(c['rects'][j])) if 'rects' in c else (round(j%4*sw),round(j//4*sh),round((j%4+1)*sw),round((j//4+1)*sh))
        cell=im.crop(rect);w,h=cell.size;pivot=c['pivot'];scale=c['scale'];tip=None
        if isinstance(c.get('core'),list):
            mw,mh=c['measure'];cx,cy=c['core'][j]
            dx,dy=j%4*sw-rect[0],j//4*sh-rect[1]
            point=(cx*sw/mw+dx,cy*sh/mh+dy)
            tx,ty=c['tip'][j];tip=(tx*sw/mw+dx,ty*sh/mh+dy)
        elif c.get('foot'):
            point=luminous_center(cell,(w*.25,h*.80,w*.75,h*.97))
        elif c.get('core'):
            point=luminous_center(cell,(w*.34,h*.25,w*.66,h*.65))
        else:point=(w/2,h/2)
        # Shared scale, independently measured PHYSICAL pivot translations.
        out=Image.new('RGBA',c['size']);offset=(round(pivot[0]-point[0]*scale),round(pivot[1]-point[1]*scale))
        normalized=cell.resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST)
        out.alpha_composite(normalized,offset)
        path=DEST/f'{name}_{i:02d}.png';out.save(path,optimize=True)
        a={'key':f'hm10_{name}_{i}','path':path.relative_to(ROOT).as_posix(),'w':out.width,'h':out.height,'pivot':list(pivot),
           'sourceRect':list(rect),'sourceIndex':j,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        if tip:a['tip']=[round(offset[0]+tip[0]*scale),round(offset[1]+tip[1]*scale)]
        if name=='spike':
            p=np.array(out);mask=(p[:,:,3]>140)&(p[:,:,1]>60)&(p[:,:,2]>100)
            # The shaft's central bright pixels, not the broad foot sparks, own its rise.
            yy=np.where(mask[:,108:148].any(axis=1))[0];a['height']=max(0,pivot[1]-int(yy.min())) if len(yy) else 0
        bank.append(a);regs.append({'sourceIndex':j,'reactorOrFoot':list(point),'translation':list(offset),'scale':scale})
    manifest[name]=bank;registration[name]=regs
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
(SOURCE/'registration.json').write_text(json.dumps(registration,indent=2)+'\n',encoding='utf-8',newline='\n')
(ROOT/'assets/hammer_art_1010.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_hammer_1010.py, no shared atlas edits.\nconst HM10_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Built',sum(map(len,manifest.values())),'native RGBA cells with even canvases, fixed pivots and shared scales.')
