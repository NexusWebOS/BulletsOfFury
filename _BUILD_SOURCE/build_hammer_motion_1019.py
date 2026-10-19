"""Export inspected PixelLab Hammer poses. Fixed 256-square cells, no fitting."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/hammer_motion_1019'
D=R/'assets/game/levels/stage_08/boss/hammer_motion_1019'
O=R/'_shots/overnight_combat_1019'
D.mkdir(parents=True,exist_ok=True)
directions=['south','south-east','east','north-east','north','north-west','west','south-west']
# Physical hammer-head centres annotated against each actual generated view.
heads=[(215,120),(206,103),(165,90),(95,91),(65,114),(48,128),(72,143),(177,145)]
art={'canvas':[256,256],'pivot':[128,128],'banks':{}}
audit={'canvas':[256,256],'pivot':[128,128],'normalization':'Identity: common scale 1, no frame fitting or generated intermediates.','banks':{}}
for bank,scale in [('ball',.85),('twirl',.55)]:
    # The last ball frame is an off-palette source hold. Omit it; never
    # manufacture an interpolation or duplicate an end pose to pad the count.
    sources=[S/f'hammer_ball_{i:02}.png' for i in range(1,32)] if bank=='ball' else [S/(n+'.png') for n in directions]
    records=[];poses=[];hashes=[]
    sheet=Image.new('RGBA',(256*8,256*((len(sources)+7)//8)),(7,12,22,255))
    onions=sheet.copy()
    for i,source in enumerate(sources):
        im=Image.open(source).convert('RGBA');assert im.size==(256,256)
        box=im.getbbox();assert box and min(box[:2])>8 and max(box[2:])<248,(bank,i,box)
        path=D/f'{bank}_{i:02}.png';im.save(path,optimize=True)
        a={'key':f'hm19_{bank}_{i:02}','path':path.relative_to(R).as_posix(),'w':256,'h':256,'pivot':[128,128],'bounds':list(box),'referenceScale':scale,'source':source.relative_to(R).as_posix()}
        if bank=='twirl':a.update(direction=directions[i],head=list(heads[i]))
        records.append(a);poses.append(im);hashes.append(hashlib.sha256(im.tobytes()).hexdigest())
    assert len(set(hashes))==len(hashes)
    for i,im in enumerate(poses):
        xy=(i%8*256,i//8*256);sheet.alpha_composite(im,xy)
        for j in [(i-1)%len(poses),(i+1)%len(poses)]:
            ghost=poses[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda v:round(v*.2)));onions.alpha_composite(ghost,xy)
        onions.alpha_composite(im,xy)
        pen=ImageDraw.Draw(sheet);pen.text((xy[0]+5,xy[1]+5),str(i),fill='#dddddd')
        if bank=='twirl':
            x,y=heads[i];pen.ellipse((xy[0]+x-5,xy[1]+y-5,xy[0]+x+5,xy[1]+y+5),outline='#40ff80',width=1)
    sheet.save(O/f'hammer-{bank}-accepted.png');onions.save(O/f'hammer-{bank}-onions.png')
    poses[0].save(O/f'hammer-{bank}-accepted.webp',save_all=True,append_images=poses[1:],duration=65 if bank=='ball' else 95,loop=0,lossless=True)
    art['banks'][bank]=records
    audit['banks'][bank]={'frames':len(records),'unique':len(set(hashes)),'referenceScale':scale,'sources':[p.relative_to(R).as_posix() for p in sources],'hashes':hashes,'bounds':[a['bounds'] for a in records]}
audit['jobs']={'ball':'74c4e4fd-d2a5-4534-9126-9419cffe2380','twirlEightViews':'b793015d-b907-4de5-bd16-ef424892ddbc'}
audit['rejected']=[{'source':'hammer_ball_32.png','reason':'Off-palette source hold causes a brown flash at the loop seam.'},{'job':'25b41064-98fa-48d6-8314-7769b2c054e9','reason':'Idle front poses did not perform the requested turn.'},{'source':'hammer_twirl_01..32.png','reason':'Generated 45-degree segments jump through incorrect directions and mirror the weapon hand. Use the eight actual directional views.'}]
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(S/'accepted-registration.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
(R/'assets/hammer_motion_art_1019.js').write_text('"use strict";\n// Owned by build_hammer_motion_1019.py.\nconst HM19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
tax=R/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8-sig'))
data['hm19_']={'role':'stage8_native_hammer_rolling_and_turning','sheet':None,'note':'31 inspected real PixelLab rolling poses and eight proper directional views.256x256/pivot128,128. Actual live Hammer reference; no generated interpolation, per-frame fitting, extra arm or flat rotation over the rolling bank. Runtime hammer_motion_1019.js; owner build_hammer_motion_1019.py.'}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:dict(frames=v['frames'],unique=v['unique']) for k,v in audit['banks'].items()}))
