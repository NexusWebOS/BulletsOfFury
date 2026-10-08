"""Pack reviewed generated loose assets. Does not change any shared atlas."""
from pathlib import Path
import json, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/feedback_1002';OUT=ROOT/'assets/game/feedback_1002'
SRC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
GENERATED=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
FILES={'firejet':'exec-5bd43869-36d4-4e6d-9894-4e4b293c47e4.png','frostkit':'exec-fcbee964-b3c8-4404-bd3b-9c90ef6d34f2.png','icebreath':'exec-fa816499-319e-4f7c-ac8d-fb51cd76b485.png','chaingun':'exec-bbf3cccc-0a0c-4db5-b20c-74fbb65d9978.png','deathkit':'exec-8e56519c-b7d1-49b2-b7fa-68c5e4649813.png','electrical':'exec-47d5c554-259a-4734-ac6b-b503f5f0535c.png','lightning':'exec-55e013f5-5e3c-4a54-86e3-0c7ee77a344a.png'}
FILES['deathbody']='exec-fb760b06-1724-4bde-9dc5-6025357c426d.png'
FILES['chaingun_v2']='exec-5b223e6f-e26f-4c78-b70d-b887cd7eab4c.png'
for name,file in FILES.items():
    target=SRC/(name+'.png')
    if not target.exists():shutil.copy2(GENERATED/file,target)
art={}
def pack(name,source,rects,anchors=None,grid=False):
    im=Image.open(SRC/(source+'.png')).convert('RGBA')
    if grid:
        sx,sy=im.width/1280,im.height/1280
        rects=[[round(x*sx),round(y*sy),round((x+w)*sx)-round(x*sx),round((y+h)*sy)-round(y*sy)] for x,y,w,h in rects]
        if anchors:anchors=[[round(x*sx),round(y*sy)] for x,y in anchors]
    frames=[];cells=[];pivots=[]
    for i,rect in enumerate(rects):
        x,y,w,h=rect;c=im.crop((x,y,x+w,y+h));box=c.getchannel('A').point(lambda a:255 if a>24 else 0).getbbox()
        if not box:raise ValueError((name,rect))
        c=c.crop(box);cells.append(c)
        if anchors:pivots.append((anchors[i][0]-x-box[0],anchors[i][1]-y-box[1]))
    # Keep each frame's authored alpha and a common cell/pivot. No frame-sized rescaling.
    if anchors:
        px=max(p[0] for p in pivots)+4;py=max(p[1] for p in pivots)+4
        cw=px+max(c.width-p[0] for c,p in zip(cells,pivots))+4
        ch=py+max(c.height-p[1] for c,p in zip(cells,pivots))+4
    else:cw=max(c.width for c in cells)+8;ch=max(c.height for c in cells)+8
    sheet=Image.new('RGBA',(cw*len(cells),ch))
    for i,c in enumerate(cells):
        dx,dy=(px-pivots[i][0],py-pivots[i][1]) if anchors else ((cw-c.width)//2,(ch-c.height)//2)
        sheet.alpha_composite(c,(cw*i+dx,dy));frames.append([cw*i,0,cw,ch])
    sheet.save(OUT/(name+'.png'),optimize=True)
    art[name]={'key':'fb1002_'+name,'path':'assets/game/shared/combat/feedback_1002/'+name+'.png','frames':frames}
    if anchors:art[name]['pivot']=[px,py]
for name in ['firejet','icebreath','deathbody']:
    im=Image.open(SRC/(name+'.png'));pack(name,name,[[0,0,*im.size]])
pack('frost_hull','frostkit',[[0,0,746,700]],grid=True)
pack('frost_gun','frostkit',[[810,0,430,700]],grid=True)
pack('frost_missile','frostkit',[[140,700,440,550]],grid=True)
pack('frost_core','frostkit',[[790,800,460,440]],grid=True)
pack('chaingun','chaingun_v2',[[c*320,r*640,320,640] for r in range(2) for c in range(4)],[[c*320+160,r*640+140] for r in range(2) for c in range(4)],grid=True)
sy=Image.open(SRC/'chaingun_v2.png').height/1280
art['chaingun']['muzzle']=[art['chaingun']['pivot'][0],round(art['chaingun']['pivot'][1]+450*sy)]
# Heads are cropped ABOVE the generated shoulder/chest assembly; those are not head modules.
pack('death_head','deathkit',[[c*320+12,165,296,215] for c in range(4)],grid=True)
pack('hammer_portrait','deathkit',[[12,165,296,215]],grid=True)
pack('death_arm','deathkit',[[c*320,580,320,670] for c in range(4)],[[158,760],[409,791],[745,1003],[1052,1007]],grid=True)
pack('electrical','electrical',[[c*320,r*320,320,320] for r in range(4) for c in range(4)],grid=True)
pack('lightning_gun','lightning',[[c*320,0,320,460] for c in range(4)],grid=True)
pack('lightning_beam','lightning',[[c*320,465,320,800] for c in range(4)],grid=True)
(ROOT/'assets/feedback_art_1002.js').write_text('"use strict";\nconst FB1002_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'manifest.json').write_text(json.dumps({'generator':'built-in image_gen','assets':FILES,'art':art},indent=2),encoding='utf-8')
print('Packed',len(art),'reviewed loose asset families')
