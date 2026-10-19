"""Export PixelLab frost banks at fixed pivots; no pose fitting or synthesized frames."""
from pathlib import Path
import base64, hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/rime_effects_1019'
RAW=ROOT/'_shots/rime_defense_1019/raw'
DST=ROOT/'assets/game/shared/combat/rime_effects_1019'
OUT=ROOT/'_shots/rime_defense_1019'
JOBS={'swirl':'b7523103-745f-45f6-a289-99de8baddc1c',
      'charge':'c689aa94-a23a-45ba-92e0-3b54a6b50428',
      'mortar':'1c7580f8-cd7b-4af2-86e9-e512ba117448'}
GEOM={'swirl':((160,160),(192,192),(16,16),(96,96)),
      'charge':((160,160),(192,192),(16,16),(96,96)),
      'mortar':((64,256),(96,288),(16,16),(48,232))}
for p in [SRC,DST,OUT]:p.mkdir(parents=True,exist_ok=True)

# MCP pixels are saved locally without forwarding credentials or invoking a
# network downloader. Preserve all returned frames, including the input seed.
for f in RAW.glob('*.b64'):
    (SRC/(f.stem+'.png')).write_bytes(base64.b64decode(f.read_text()))
art={'banks':{},'fps':18,'sourceScale':1,'service':'PixelLab','jobs':JOBS,
     'bullet':{'key':'rd19_ice_slug','path':'assets/game/shared/player_weapons/player_weapons/forge_elements_0918/ice_bullet.png'}}
audit={}
for bank,job in JOBS.items():
    size,canvas,shift,pivot=GEOM[bank]
    frames=[];records=[];hashes=[]
    for i in range(1,33):
        raw=SRC/f'{bank}_{i:02}.png'
        im=Image.open(raw).convert('RGBA')
        assert im.size==size,(raw,im.size,size)
        frame=Image.new('RGBA',canvas);frame.alpha_composite(im,shift)
        ink=frame.getbbox();assert ink and min(ink)>0 and ink[2]<canvas[0] and ink[3]<canvas[1],(bank,i,ink)
        pixels=np.array(frame);assert (pixels[:,:,3]==0).sum()>canvas[0]*canvas[1]*.25
        f=DST/f'{bank}_{i-1:02}.png';frame.save(f,optimize=True)
        sha=hashlib.sha256(f.read_bytes()).hexdigest();hashes.append(sha)
        records.append({'key':f'rd19_{bank}_{i-1:02}','path':f.relative_to(ROOT).as_posix(),
                        'w':canvas[0],'h':canvas[1],'pivot':list(pivot),'sourceIndex':i,
                        'ink':list(ink),'sha256':sha})
        frames.append(frame)
    assert len(set(hashes))>=28,(bank,'too many repeated poses')
    # Contact sheets and real adjacent-pose onions, never independent resizes.
    w,h=canvas;sheet=Image.new('RGBA',(w*8,h*4),(5,13,24,255));d=ImageDraw.Draw(sheet)
    for i,frame in enumerate(frames):
        x,y=(i%8)*w,(i//8)*h;sheet.alpha_composite(frame,(x,y))
        d.line((x+pivot[0]-5,y+pivot[1],x+pivot[0]+5,y+pivot[1]),fill='#ffb04d')
        d.line((x+pivot[0],y+pivot[1]-5,x+pivot[0],y+pivot[1]+5),fill='#ffb04d')
        d.text((x+4,y+4),str(i),fill='white')
    sheet.save(OUT/f'{bank}-registration.png')
    onions=Image.new('RGBA',(w*8,h*4),(5,13,24,255))
    for i,frame in enumerate(frames):
        x,y=(i%8)*w,(i//8)*h
        prev=frames[(i-1)%len(frames)].copy();prev.putalpha(prev.getchannel('A').point(lambda a:round(a*.25)))
        nxt=frames[(i+1)%len(frames)].copy();nxt.putalpha(nxt.getchannel('A').point(lambda a:round(a*.25)))
        onions.alpha_composite(prev,(x,y));onions.alpha_composite(nxt,(x,y));onions.alpha_composite(frame,(x,y))
    onions.save(OUT/f'{bank}-onions.png')
    # WebP retains alpha and complete generated poses for the review gallery.
    frames[0].save(OUT/f'{bank}.webp',save_all=True,append_images=frames[1:],duration=56,loop=0,lossless=True)
    deltas=[]
    for i in range(32):
        a=np.array(frames[i]).astype(float);b=np.array(frames[(i+1)%32]).astype(float)
        a[:,:,:3]*=a[:,:,3,None]/255;b[:,:,:3]*=b[:,:,3,None]/255
        deltas.append(round(float(np.abs(a-b).mean()),3))
    audit[bank]={'job':job,'inputSize':list(size),'canvas':list(canvas),'pivot':list(pivot),
                 'sharedTranslation':list(shift),'proportionalScale':1,'frames':32,
                 'unique':len(set(hashes)),'adjacentMeanDelta':deltas,'loopSeamDelta':deltas[-1]}
    art['banks'][bank]=records

# Measure the real seated reactor plate, rather than extending hull collision
# into its transparent hole. Offline occupancy also works in file:// builds.
sheet=Image.open(ROOT/'assets/game/shared/combat/modular_roster_0927/rime.png').convert('RGBA')
core=sheet.crop((218,707,450,953));core.save(OUT/'actual-core.png')
alpha=np.array(core)[:,:,3];n=48;rows=[]
for y in range(n):
    bits=0
    for x in range(n):
        cell=alpha[y*core.height//n:(y+1)*core.height//n,x*core.width//n:(x+1)*core.width//n]
        bits=(bits<<1)|int(float((cell>=96).mean())>=.30)
    rows.append(f'{bits:012x}')
art['coreMask']={'n':n,'rows':rows,'sourceCell':[218,707,232,246],'alphaThreshold':96,'coverage':.30}
(DST/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/rime_effects_art_1019.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_rime_effects_1019.py.\nconst RD19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
audit['rejectedSeeds']=[{'job':'6a1ef56e-0725-42ce-aba6-46e47654f126','reason':'mechanical gear instead of organic frost'},
 {'job':'7879775e-f826-4d3b-af4e-3624a7054ada','reason':'framed snowflake icon'},
 {'job':'6f639120-efed-472d-ae73-460c2c0bc5eb','reason':'solid asteroid instead of cold vapor'}]
(SRC/'registration.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
tax=ROOT/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8-sig'));data.pop('rd19_',None)
data={'rd19_':{'role':'stage3_icy_reactor_swirl_charge_and_shoulder_laser_mortar','sheet':None,
 'note':'PixelLab:32 real frost swirl,32 reactor charge and32 laser mortar poses. Fixed192x192/pivot96,96 frost banks;96x288/pivot48,232 mortar bank, measured at the actual lower flare rather than the drifting tail. Shared16px transparent padding, constant source scale1, no per-frame fitting or generated duplicate padding. Includes measured48x48 seated-core occupancy; whole authored boss plate preserved. Owner build_rime_effects_1019.py; runtime rime_defense_1019.js.'},**data}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'frames':96,'bytes':sum(f.stat().st_size for f in DST.glob('*.png')),'audit':audit},indent=2))
