"""Normalize generated moving parts onto the live roster's shared native anchors.

Owns its loose PNG bank and stage1_motion_art_1009.js. No shared atlas changes.
Only cropping, edge cleanup and common scale/landmark registration occur here.
The hull, turret and ordnance remain independent in the actual game renderer.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/stage1_motion_1009/returned'
DEST=ROOT/'assets/game/shared/combat/stage1_motion_1009'
DEST.mkdir(parents=True,exist_ok=True)
REVIEW=ROOT/'_shots/boss_motion_1009'
REVIEW.mkdir(parents=True,exist_ok=True)
# Coordinates below are measured in each equal source cell. A whole reel shares
# one scale and target pivot, including the frames with shorter recoil/flames.
DATA={
 'hull':('s1_live_hull',8,(384,384),(192,192),1.32,[(136,357)]*8,(20,235,252,500)),
 'turret':('s1_live_turret',4,(384,384),(192,192),.778,[(262,317)]*4,(146,205,395,577)),
 'buggy_idle':('s1_buggy_idle',8,(256,384),(128,192),1.11,[(136,360)]*8,(24,198,249,523)),
 'buggy_fire':('s1_buggy_fire',4,(256,384),(128,192),.70,[(373.5,356),(305.5,356),(236.5,356),(168.5,356)],None),
 'wake':('s1_wake',8,(300,600),(150,320),1,[(131,360),(121,365),(119,365),(129,380),(147,371),(153,363),(151,356),(142,356)],None),
 'exhaust':('s1_exhaust',8,(256,640),(128,600),1,[(160,626),(147,626),(142,626),(139,626),(136,626),(125,626),(116,626),(114,626)],(25,73,244,642)),
 'muzzle':('s1_muzzles',8,(256,416),(128,24),1,[(148,140),(162,140),(180,140),(166,140),(135,140),(140,140),(127,140),(130,140)],(24,128,266,530))
}
manifest={};preview=Image.new('RGBA',(8*240,7*220),(15,22,32,255));g=ImageDraw.Draw(preview)
for row,(bank,(source,count,size,target,scale,pivots,crop)) in enumerate(DATA.items()):
    im=Image.open(SRC/(source+'.png')).convert('RGBA');frames=[]
    for i,pivot in enumerate(pivots):
        l=round(i*im.width/count);r=round((i+1)*im.width/count)
        cell=im.crop((l,0,r,im.height));pixels=np.array(cell)
        # The generator leaves sparse near-transparent ghosts well outside the
        # authored silhouettes. This is alpha cleanup, never a color-key mask.
        pixels[:,:,3][pixels[:,:,3]<64]=0
        cell=Image.fromarray(pixels)
        rect=crop
        if rect is None:
            y,x=np.where(pixels[:,:,3]>170)
            rect=(max(0,int(x.min())-8),max(0,int(y.min())-8),min(cell.width,int(x.max())+9),min(cell.height,int(y.max())+9))
        cell=cell.crop(rect)
        cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST)
        off=(round(target[0]-(pivot[0]-rect[0])*scale),round(target[1]-(pivot[1]-rect[1])*scale))
        out=Image.new('RGBA',size);out.alpha_composite(cell,off)
        path=DEST/f'{bank}_{i}.png';out.save(path,optimize=True)
        frames.append({'key':f's1m_{bank}_{i}','path':path.relative_to(ROOT).as_posix(),'w':size[0],'h':size[1],'pivot':target,'source':source+'.png','sourceRect':[l+rect[0],rect[1],l+rect[2],rect[3]],'scale':scale})
        k=min(220/out.width,180/out.height);thumb=out.resize((round(out.width*k),round(out.height*k)),Image.Resampling.NEAREST)
        preview.alpha_composite(thumb,(i*240+(240-thumb.width)//2,row*220+20+(180-thumb.height)//2));g.text((i*240+9,row*220+5),f'{bank} {i+1}/{count}',fill='#dce6ee')
    manifest[bank]=frames
(ROOT/'_ART_SOURCES/stage1_motion_1009/live-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/stage1_motion_art_1009.js').write_text('"use strict";\n// Generated only by _BUILD_SOURCE/build_stage1_motion_1009.py.\nconst S1M_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
preview.save(REVIEW/'stage1-motion-contact.png')
print('Built',sum(map(len,manifest.values())),'authored moving-part cells, independent of aiming and HP.')
