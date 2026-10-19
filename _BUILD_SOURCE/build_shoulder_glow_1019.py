"""Clip authored PixelLab frost motion to the actual Rime shoulder cavities.

No generated hull, procedural sprite, blur or runtime pixel read. All poses use
the same source-space socket mask, 80x80 canvas and pivot (40,40).
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/rime_effects_1019'
D=R/'assets/game/shared/combat/shoulder_glow_1019'
O=R/'_shots/overnight_combat_1019'
D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
plate=Image.open(R/'assets/game/shared/combat/modular_roster_0927/rime.png').convert('RGBA')
art={'canvas':[80,80],'pivot':[40,40],'fps':18,'sourceScale':1,
     'sourcePlate':'assets/game/shared/combat/modular_roster_0927/rime.png',
     'sourceChargeJob':'c689aa94-a23a-45ba-92e0-3b54a6b50428','banks':{}}
audit={}
for side,cx in [('L',201),('R',491)]:
    cy=184;box=(cx-40,cy-40,cx+40,cy+40)
    source=plate.crop(box);a=np.array(source)
    yy,xx=np.mgrid[:80,:80]
    # The connected dark cavity is inside the original blue inner bevel. The
    # measured ellipse bounds the selection so neighboring dark hull cannot light.
    allowed=(((xx-40)/26)**2+((yy-40)/25)**2<1)&(a[:,:,:3].max(2)<70)&(a[:,:,3]>128)
    seen=np.zeros((80,80),bool);todo=[(40,40)]
    while todo:
        y,x=todo.pop()
        if x<0 or y<0 or x>=80 or y>=80 or seen[y,x] or not allowed[y,x]:continue
        seen[y,x]=True;todo.extend([(y-1,x),(y+1,x),(y,x-1),(y,x+1)])
    assert 1200<int(seen.sum())<2100,(side,int(seen.sum()))
    mask=Image.fromarray((seen*255).astype('uint8'))
    mask.save(O/f'shoulder-{side}-cavity-mask.png')
    records=[];poses=[]
    for i in range(32):
        raw=Image.open(S/f'charge_{i+1:02}.png').convert('RGBA')
        assert raw.size==(160,160)
        # One constant proportional resize, centered by the source pivot. No
        # per-pose crop, fitting, rotation or synthetic intermediate frames.
        texture=raw.resize((64,64),Image.Resampling.NEAREST)
        frame=Image.new('RGBA',(80,80));frame.alpha_composite(texture,(8,8))
        pixels=np.array(frame);pixels[:,:,3]=np.minimum(pixels[:,:,3],np.array(mask))
        frame=Image.fromarray(pixels);f=D/f'{side.lower()}_{i:02}.png';frame.save(f,optimize=True)
        records.append({'key':f'sg19_{side}_{i:02}','path':f.relative_to(R).as_posix(),
                        'w':80,'h':80,'pivot':[40,40]})
        poses.append(frame)
        assert not np.any((pixels[:,:,3]>0)&~seen)
    sheet=Image.new('RGBA',(80*8,80*4),(8,14,24,255))
    onions=sheet.copy()
    for i,frame in enumerate(poses):
        at=(i%8*80,i//8*80)
        for image in [sheet,onions]:image.alpha_composite(source,at)
        for j in [(i-1)%32,(i+1)%32]:
            ghost=poses[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:round(a*.20)))
            onions.alpha_composite(ghost,at)
        sheet.alpha_composite(frame,at);onions.alpha_composite(frame,at)
    sheet.resize((1280,640),Image.Resampling.NEAREST).save(O/f'shoulder-{side}-registration.png')
    onions.save(O/f'shoulder-{side}-onions.png')
    art['banks'][side]=records
    audit[side]={'sourceBox':box,'center':[cx,cy],'maskPixels':int(seen.sum()),
                 'frameCount':32,'unique':len({hashlib.sha256(p.tobytes()).hexdigest() for p in poses}),
                 'proportionalScale':.4,'translation':[8,8],'canvas':[80,80],'pivot':[40,40]}
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(R/'assets/shoulder_glow_art_1019.js').write_text('"use strict";\n// Owned by build_shoulder_glow_1019.py.\nconst SG19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(O/'shoulder-registration.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit,indent=2))
