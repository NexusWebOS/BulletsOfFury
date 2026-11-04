"""Reproducible offline export of generated scenes and existing cast pixels.
Runtime uses source rectangles and integer placement only.
"""
from pathlib import Path
import json, math, shutil, hashlib, argparse
import numpy as np
from PIL import Image
WORK=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--game',type=Path,default=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury'));p.add_argument('--out',type=Path,default=WORK.parent/'outputs/BOF-Cutscenes-1103');p.add_argument('--refs',type=Path,default=WORK/'references');p.add_argument('--sources',type=Path,default=WORK/'generated.json');p.add_argument('--headsets-only',action='store_true');args=p.parse_args()
ROOT=args.game;OUT=args.out;REF=args.refs
OV=OUT/'overlay'
ART=OV/'assets/game/shared/cinematics/story_1103'
SRC=OUT/'source-art'
ART.mkdir(parents=True,exist_ok=True);SRC.mkdir(exist_ok=True)
M={k:(Path(v)if Path(v).is_absolute()else args.sources.parent/v).resolve()for k,v in json.loads(args.sources.read_text()).items()}
N=json.loads((REF/'native.json').read_text())
pilots=list(N['cast']['pilots'])
registry=json.loads((ART/'manifest.json').read_text())['banks'] if args.headsets_only else {};provenance=[]
def put(name,frames,cols=None,pivot=None):
    if args.headsets_only and not name.startswith(('headset-','comic-')):return frames
    cols=cols or min(8,len(frames));w,h=frames[0].size
    assert w%2==h%2==0 and all(f.size==(w,h) for f in frames)
    sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
    for i,f in enumerate(frames):sheet.alpha_composite(f,(i%cols*w,i//cols*h))
    path=ART/(name+'.webp');sheet.save(path,lossless=True,method=4)
    registry[name]={'key':'s113_'+name,'path':path.relative_to(OV).as_posix(),'w':w,'h':h,'cols':cols,'frames':len(frames),'pivot':pivot or [w//2,h//2]}
    return frames
def grid(path,cols,rows):
    im=Image.open(path).convert('RGBA');w,h=im.size
    return [im.crop((round(i%cols*w/cols),round(i//cols*h/rows),round((i%cols+1)*w/cols),round((i//cols+1)*h/rows))) for i in range(cols*rows)]
def fit(im,w,h):
    k=min(w/im.width,h/im.height);out=Image.new('RGBA',(w,h))
    im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
    out.alpha_composite(im,((w-im.width)//2,(h-im.height)//2));return out
for name,path in M.items():
    dest=SRC/(name+'.png')
    if path.resolve()!=dest.resolve():shutil.copy2(path,dest)
    provenance.append({'name':name,'source':dest.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'tool':'built-in image_gen'})
    if name.startswith(('flight-','headset16-')) or name in ['decker-shock','headsets','lounge-empty','forge-empty','comic-divider','clean-sky']:continue
    if name.endswith('-exit'):
        im=Image.open(path).convert('RGBA');height=round(im.height*680/im.width)//2*2
        put(name,[im.resize((680,height),Image.Resampling.NEAREST)],1);continue
    frames=grid(path,2,2)
    put(name,[fit(f,912,512) for f in frames],2)
# Empty room/still plates are authored source art; no browser decoration.
for name,old in [('hangar','hq_hangar'),('lounge','hq_regroup'),('forge','forge_upgrade'),('earth','orbital_return'),('river','hq_river'),('sewer','river_sewer'),('sky','air_invasion')]:
    source=M[name+'-empty'] if name in ['lounge','forge'] else M['clean-sky'] if name=='sky' else ROOT/N['images'][old]['path'].split('?')[0]
    im=Image.open(source).convert('RGBA');put(name,[fit(im,912,512)],1)
# Small full-body cast for staging; preserve a single source scale and pivot.
for p in pilots:
    poses={**N['cast']['pilots'][p],**N['performance']['pilots'][p]}
    chosen=['neutral','speaking','salute','walk_0','walk_1','walk_2','walk_3','run_0','run_1','run_2','run_3','sit_idle','sit_speaking','dispatch_typing','happy','ecstatic','jump_cheer','angry','sad']
    fs=[]
    for pose in chosen:
        key=poses[pose]
        # Metadata source paths are registered in the owning art file.
        text=(ROOT/('assets/cast_performance_art_1102.js' if key.startswith('cp112_') else 'assets/cast_cinematics_art_1102.js')).read_text()
        import re
        source=re.search('"'+re.escape(key)+'":"([^"]+\\.(?:png|webp))"',text).group(1)
        im=Image.open(ROOT/source).convert('RGBA')
        if pose.startswith('run_') and p in ['yuri','lizzie']:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        m=N['performance']['metadata'].get(key,{'cell':[512,1024],'pivot':[256,976]})
        k=.25;im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
        frame=Image.new('RGBA',(224,272));frame.alpha_composite(im,(112-round(m['pivot'][0]*k),256-round(m['pivot'][1]*k)));fs.append(frame)
    put('actor-'+p,fs,5,[112,256])
    # Native cockpit identity retained for the first relay observation shot.
    path=REF/('cin_pilot_'+p+'_open.png')
    if path.exists():put('cockpit-'+p,[fit(Image.open(path).convert('RGBA'),912,512)],1)
    front=Image.open(REF/('ship_'+p+'_so6.png')).convert('RGBA')
    put('return-'+p,[fit(front.resize((round(front.width*(48+i*5)/front.height),48+i*5),Image.Resampling.NEAREST),256,256) for i in range(32)],8)
    raw=Image.open(REF/('ship_'+p+'.png')).convert('RGBA')
    assert raw.getchannel('A').getextrema()==(0,255),(p,'native ship export must retain transparent background')
    fs=[]
    for i in range(32):
        height=round(64-40*i/31);small=raw.resize((max(2,round(raw.width*height/raw.height)),height),Image.Resampling.NEAREST)
        f=Image.new('RGBA',(128,128));f.alpha_composite(small,((128-small.width)//2,64-small.height//2));fs.append(f)
    put('landing-'+p,fs,8,[64,64])
# Four genuinely redrawn viewpoints per aircraft; depth and lighting are baked.
groups=[['cole','axel','decker'],['maverick','freezer','juggernaut'],['yuri','lizzie','falva']]
for g,ps in enumerate(groups):
    cells=grid(M['flight-'+str(g)],4,3)
    for row,p in enumerate(ps):
        source=cells[row*4:row*4+4]
        source=[fit(im,256,256) for im in source]
        put('flight-'+p,source,4)
        # 48 fixed 256px launch cells, common fuselage pivot; frame-only recession.
        fs=[]
        for i in range(48):
            pose=0 if i<8 else 1 if i<34 else 2
            im=source[pose].copy();a=np.array(im)
            # Authored own-pixel exhaust pulse. Hull dark seams stay unchanged.
            rgb=a[:,:,:3].astype(float);bright=(rgb.max(2)>170)&(rgb.max(2)-rgb.min(2)>65)&(np.indices(a.shape[:2])[0]>128)
            gain=1+(.06,.13,.23,.13)[i%4]
            rgb[bright]=np.minimum(255,rgb[bright]*gain);a[:,:,:3]=rgb.astype('uint8');im=Image.fromarray(a)
            size=round(236*(1-i/52)**1.3);fs.append(fit(im.resize((size,size),Image.Resampling.NEAREST),256,256))
        put('launch-'+p,fs,8)
# Decker's keyboard/recoil/recovery/duck poses remain a source-authored bank.
put('decker-shock',[fit(f,384,384) for f in grid(M['decker-shock'],3,2)],3,[192,368])
put('decker-room',[fit(f,208,208) for f in grid(M['decker-shock'],3,2)],3,[104,200])
harrier=REF/'whv_closed.png'
if harrier.exists():put('harrier',[fit(Image.open(harrier).convert('RGBA'),320,320)],1)
extra=REF/'extras.json'
if extra.exists():
    E=json.loads(extra.read_text())['rebels']
    for p in ['voss','nyx','rook','kaia','jace']:
        b=E['banks']['flight-'+p] if 'flight-'+p in E['banks'] else E['banks']['flight_'+p]
        im=Image.open(ROOT/b['path'].split('?')[0]).convert('RGBA');cells=[]
        for i in range(b['frames']):
            cell=im.crop((i%b['cols']*b['cw'],i//b['cols']*b['ch'],i%b['cols']*b['cw']+b['cw'],i//b['cols']*b['ch']+b['ch']))
            cells.append(fit(cell,128,128))
        put('rebel-'+p,cells,8)
head_order=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
headmap={}
native_heads=SRC/'headsets-16bit';native_heads.mkdir(exist_ok=True)
for p in head_order:
    # Newly generated console drawings, normalized once to their native pixel grid.
    # Hard alpha and no-dither palette export keep the drawn clusters crisp.
    im=Image.open(M['headset16-'+p]).convert('RGBA')
    assert im.width==im.height,(p,'headset source must have a square canvas')
    im=im.resize((128,128),Image.Resampling.NEAREST)
    alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
    im=im.convert('RGB').quantize(colors=32,dither=Image.Dither.NONE).convert('RGBA')
    im.putalpha(alpha);im.save(native_heads/(p+'.png'));headmap[p]=im
    portrait=Image.new('RGBA',(288,288))
    portrait.alpha_composite(im.resize((256,256),Image.Resampling.NEAREST),(16,16))
    put('headset-'+p,[portrait],1)
# Full authored comic panels: chest edges end behind the gray footer, never float.
divider=fit(Image.open(M['comic-divider']).convert('RGBA'),912,512)
alpha=np.array(divider.getchannel('A'))
footer=np.where((alpha>128).sum(axis=1)>800)[0]
assert len(footer)>0,'gray comic footer must span both panels'
footer_top=int(footer[0]);dy=392-footer_top
framing=Image.new('RGBA',(912,512));framing.alpha_composite(divider,(0,dy))
for p in pilots:
    frame=Image.new('RGBA',(912,512),(0,0,0,255))
    contact='cole' if p=='decker' else 'decker'
    for person,x in [(contact,14),(p,498)]:
        native=headmap[person]
        if person==p:native=native.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        portrait=Image.new('RGBA',(400,400))
        portrait.alpha_composite(native.resize((384,384),Image.Resampling.NEAREST),(8,8))
        # Lower anatomical cut is covered by the authored gray comic footer.
        bounds=portrait.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
        frame.alpha_composite(portrait,(x,398-bounds[3]))
    frame.alpha_composite(framing)
    put('comic-'+p,[frame],1)
# Source-authored fade ladder; Bayer alpha coverage is stored in the atlas.
bayer=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])
pattern=np.tile(bayer,(128,228));fs=[]
for i in range(17):
    a=np.zeros((512,912,4),dtype='uint8');a[:,:,3]=(pattern<i).astype('uint8')*255;fs.append(Image.fromarray(a))
put('fade',fs,4)
(ART/'manifest.json').write_text(json.dumps({'version':'story-1103','pilots':pilots,'banks':registry,'source_art':provenance,'actorPoses':chosen},indent=2))
(OV/'assets/story_campaign_art_1103.js').write_text("'use strict';\nconst S113_ART="+json.dumps({'banks':registry,'pilots':pilots,'actorPoses':chosen},separators=(',',':'))+';\n')
(SRC/'provenance.json').write_text(json.dumps(provenance,indent=2))
print(f'Exported {len(registry)} banks, {sum(a["frames"] for a in registry.values())} even fixed frames to {OUT}')
