"""Import authored image_gen art; no sprite drawing or runtime modifications.

Slicing, nearest-neighbor scale, padding, atlas packing and review composites only.
Run from any folder. Sources/prompts are preserved beside inputs.json.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import hashlib, json, math, shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '_ART_SOURCES/weapon_animation_0928'
OUT = ROOT / 'assets/game/weapon_animation_0928'
INPUTS = json.loads((SOURCE / 'inputs.json').read_text(encoding='utf-8'))
ELEMENTS = ['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water']
PILOTS = ['axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva','cole']
FAMILIES, QA = {}, []
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'review').mkdir(exist_ok=True)

def bounds(im, threshold=32):
    return im.getchannel('A').point(lambda a:255 if a>=threshold else 0).getbbox()

def source(key):
    src = Path(INPUTS['paths'][key])
    dst = SOURCE / (key + '.png')
    if src.exists() and src.resolve()!=dst.resolve():
        shutil.copy2(src, dst)
    elif not dst.exists():
        raise FileNotFoundError(f'Neither generation cache nor saved source exists: {key}')
    return Image.open(dst).convert('RGBA')

def grid(im, cols, rows, xs=None, ys=None):
    xs = xs or [round(x*im.width/cols) for x in range(cols+1)]
    ys = ys or [round(y*im.height/rows) for y in range(rows+1)]
    return [(im.crop((xs[c],ys[r],xs[c+1],ys[r+1])),
             [xs[c],ys[r],xs[c+1]-xs[c],ys[r+1]-ys[r]])
            for r in range(rows) for c in range(cols)]

def normalize(cells, size, mode='center', margin=8):
    # One shared scale for a whole reel. Cropping/padding never changes pixel colors.
    boxes = [bounds(im) for im,_ in cells]
    if any(b is None for b in boxes): raise ValueError('Empty source frame')
    mw = max(b[2]-b[0] for b in boxes)
    mh = max(b[3]-b[1] for b in boxes)
    scale = min((size[0]-margin*2)/mw,(size[1]-margin*2)/mh)
    frames, info = [], []
    for (im,rect),box in zip(cells,boxes):
        part = im.crop(box)
        dims = (max(1,round(part.width*scale)),max(1,round(part.height*scale)))
        part = part.resize(dims,Image.Resampling.NEAREST)
        x = (size[0]-part.width)//2
        if mode=='boss':
            foot = im.getchannel('A').crop((0,max(0,box[3]-16),im.width,box[3]))
            foot_box = foot.point(lambda a:255 if a>=64 else 0).getbbox()
            foot_x = (foot_box[0]+foot_box[2])/2
            x = round(size[0]/2-(foot_x-box[0])*scale)
        y = (size[1]-part.height)//2 if mode=='center' else (margin if mode=='top' else size[1]-margin-part.height)
        canvas = Image.new('RGBA',size)
        canvas.alpha_composite(part,(x,y))
        frames.append(canvas)
        info.append({'sourceCell':rect,'sourceAlphaBounds':list(box),'scale':scale,'offset':[x,y]})
    anchor = [size[0]//2, size[1]//2 if mode=='center' else (margin if mode=='top' else size[1]-margin)]
    return frames, info, anchor

def add(name,cells,size,fps,loop=True,mode='center',source_key=None,notes='',margin=8):
    frames, provenance, anchor = normalize(cells,size,mode,margin)
    folder=OUT/name
    folder.mkdir(exist_ok=True)
    cols=min(8,len(frames)); rows=math.ceil(len(frames)/cols)
    pad=2
    atlas=Image.new('RGBA',(cols*(size[0]+pad*2),rows*(size[1]+pad*2)))
    records=[]
    for i,(im,prov) in enumerate(zip(frames,provenance)):
        path=folder/f'{i:02d}.png'; im.save(path,optimize=True)
        x=(i%cols)*(size[0]+pad*2)+pad; y=(i//cols)*(size[1]+pad*2)+pad
        atlas.alpha_composite(im,(x,y))
        records.append({'file':f'{name}/{i:02d}.png','rect':[x,y,*size],**prov})
    atlas.save(folder/'atlas.png',optimize=True)
    unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames})
    edge=sum(sum(im.getchannel('A').crop(rect).histogram()[32:]) for im in frames
             for rect in [(0,0,size[0],1),(0,size[1]-1,size[0],size[1]),(0,0,1,size[1]),(size[0]-1,0,size[0],size[1])])
    qa={'name':name,'frames':len(frames),'uniqueFrames':unique,'outerEdgePixelsAlpha32':edge,
        'transparentCanvas':all(im.getpixel((0,0))[3]==0 for im in frames)}
    if edge or (len(frames)>1 and unique!=len(frames)): raise ValueError(qa)
    QA.append(qa)
    family={'atlas':f'{name}/atlas.png','size':list(size),'fps':fps,'loop':loop,
            'anchor':anchor,'source':source_key,'notes':notes,'frames':records}
    FAMILIES[name]=family
    (folder/'reel.json').write_text(json.dumps(family,indent=2)+'\n',encoding='utf-8')
    # GIF is a review composite over solid slate; runtime PNGs retain original alpha.
    previews=[]
    for im in frames:
        bg=Image.new('RGBA',size,(15,24,34,255)); bg.alpha_composite(im)
        previews.append(bg.convert('RGB'))
    if len(frames)>1:
        previews[0].save(OUT/'review'/f'{name}.gif',save_all=True,append_images=previews[1:],
                         duration=round(1000/fps),loop=0 if loop else 1,disposal=2)
    return frames

# Fixed housings are separate from rotating barrels; never rotate a finished gun plate.
housing_cells=grid(source('mounts'),6,3)
for i,pilot in enumerate(PILOTS):
    for j,side in enumerate(['left','right']):
        name=f'chaingun_mount_{pilot}_{side}'
        add(name,[housing_cells[i*2+j]],(64,96),1,False,'bottom','mounts',
            'Fixed armored housing. Rear mount anchor; barrel couples to front socket.')
        FAMILIES[name]['barrelSocket']=[32,18]

# Actual generated layout is eight columns, six rows (sixteen frames per view).
barrel_im=source('barrels')
barrel_cells=grid(barrel_im,8,6,xs=[0,186,346,501,648,797,946,1094,barrel_im.width],
                  ys=[0,229,436,650,855,1040,barrel_im.height])
for i,view in enumerate(['top','bank','underside']):
    add('chaingun_barrel_'+view,barrel_cells[i*16:(i+1)*16],(64,112),20,True,'bottom','barrels',
        'Axial rotation frames. Rear coupling anchor. Bank/underside are authored views, not yaw rotation.')

for kind,prefix,size,fps,mode in [('orb','orbs',(96,96),10,'center'),
                                ('beam','beams',(128,320),12,'bottom'),
                                ('cast','casts',(160,320),12,'bottom'),
                                ('orb_hit','orb_hits',(160,160),16,'center')]:
    for group,letter in enumerate(['a','b','c']):
        key=prefix+'_'+letter+('_padded' if kind=='orb_hit' else '')
        if key not in INPUTS['paths']: continue
        rows=6 if kind=='orb' else 3
        im=source(key)
        cut_rows={'beams_a':[0,510,1021,im.height], 'beams_b':[0,507,1008,im.height],
                  'beams_c':[0,516,1024,im.height], 'casts_a':[0,514,1020,im.height],
                  'casts_b':[0,515,1021,im.height], 'casts_c':[0,504,1015,im.height]}
        ys=cut_rows.get(key)
        cells=grid(im,4,rows,ys=ys)
        count=8 if kind=='orb' else 4
        for j in range(3):
            element=ELEMENTS[group*3+j]
            add(kind+'_'+element,cells[j*count:(j+1)*count],size,fps,kind!='orb_hit',mode,key,
                'Authored elemental frame reel. Fixed center/origin; do not canvas-rotate or independently rescale frames.')

ballistic=grid(source('ballistic'),4,5)
add('chaingun_round',ballistic[:4],(48,80),16,True,'top','ballistic','Projectile tip anchor; short animated tracer.',6)
add('chaingun_muzzle',ballistic[4:12],(96,144),24,False,'bottom','ballistic','Directional flash with firing origin at bottom.',8)
add('chaingun_impact',ballistic[12:20],(160,160),24,False,'center','ballistic','Metal shrapnel and penetrating impact.',8)
element_im=source('round_elements')
rounds=grid(element_im,3,3,xs=[0,475,768,element_im.width],ys=[0,432,824,element_im.height])
for i,el in enumerate(ELEMENTS):
    add('chaingun_round_'+el,[rounds[i]],(48,96),1,False,'top','round_elements',
        'Single directional infused ballistic round; inherits MG element in runtime.',6)

# Correct hammer-only body. Excludes rejected old back-chaingun character entirely.
boss=source('chromium_corrected')
cells=grid(boss,4,3,ys=[0,373,805,boss.height])
add('chromium_activation_hammer_only',cells,(320,480),10,False,'boss','chromium_corrected',
    'Correct current hammer-only boss. Neutral, hand rise, silver lightning, armor coating, armored settle. No back chaingun.',12)

manifest={'version':1,'date':'2026-09-28','status':'graphics-only; not installed in game runtime',
          'method':'built-in image_gen; import uses Pillow only to slice/pad/pack authored pixels',
          'elements':ELEMENTS,'pilots':PILOTS,'families':FAMILIES}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(OUT/'qa.json').write_text(json.dumps({'families':len(FAMILIES),'frames':sum(len(v['frames']) for v in FAMILIES.values()),
                                   'checks':QA},indent=2)+'\n',encoding='utf-8')

def contact(names,file,tile=(180,210),cols=6):
    img=Image.new('RGB',(cols*tile[0],math.ceil(len(names)/cols)*tile[1]),(15,24,34))
    d=ImageDraw.Draw(img)
    for i,name in enumerate(names):
        f=FAMILIES[name]; rec=f['frames'][len(f['frames'])//2]
        im=Image.open(OUT/rec['file']).convert('RGBA')
        im.thumbnail((tile[0]-16,tile[1]-40),Image.Resampling.NEAREST)
        x=(i%cols)*tile[0]; y=(i//cols)*tile[1]
        img.paste(im,(x+(tile[0]-im.width)//2,y+25),im)
        d.text((x+8,y+5),name.replace('chaingun_','cg ').replace('_',' '),fill=(221,230,244))
    img.save(OUT/'review'/file)

contact([k for k in FAMILIES if k.startswith(('orb_','beam_','cast_'))],'elemental_contact.png')
contact([k for k in FAMILIES if k.startswith('chaingun_')],'chaingun_contact.png')
contact(['chromium_activation_hammer_only'],'chromium_contact.png',tile=(360,520),cols=1)
print(json.dumps({'families':len(FAMILIES),'frames':sum(len(v['frames']) for v in FAMILIES.values()),
                  'output':str(OUT),'qa':'All frames unique, nonempty, transparent and padded.'}))
