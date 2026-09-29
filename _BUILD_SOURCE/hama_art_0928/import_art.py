"""Slice/pad/pack authored image_gen frames; no sprite drawing or engine edits."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, math, shutil

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'_ART_SOURCES/hama_art_0928'
OUT=ROOT/'assets/game/hama_art_0928'
INPUTS=json.loads((SOURCE/'inputs.json').read_text(encoding='utf-8-sig'))
FAMILIES={}; QA=[]
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'review').mkdir(exist_ok=True)

def bounds(im):
    return im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox()

def grid(key,cols,rows):
    src=Path(INPUTS['paths'][key]);dst=SOURCE/(key+'.png')
    if src.exists() and src.resolve()!=dst.resolve(): shutil.copy2(src,dst)
    im=Image.open(dst).convert('RGBA')
    layout=INPUTS.get('layouts',{}).get(key,{})
    xs=layout.get('xs',[round(i*im.width/cols) for i in range(cols+1)])
    ys=layout.get('ys',[round(i*im.height/rows) for i in range(rows+1)])
    cells=[]
    for r in range(rows):
        xx=layout.get('rowXs',{}).get(str(r),xs)
        for c in range(cols):
            yy=layout.get('colYs',{}).get(str(c),ys)
            rect=[xx[c],yy[r],xx[c+1],yy[r+1]]
            cells.append((im.crop(rect),rect))
    return cells

def add(name,key,cells,size,fps,group,mode='feet',loop=True,events=None,notes='',body_height=None,anchors=None,offsets=None):
    boxes=[bounds(im) for im,_ in cells]
    if any(b is None for b in boxes):raise ValueError('Empty '+name)
    margin=16
    scale=min((size[0]-margin*2)/max(b[2]-b[0] for b in boxes),
              (size[1]-margin*2)/max(b[3]-b[1] for b in boxes))
    if body_height: scale=min(scale,280/body_height)
    frames=[];records=[]
    anchor=[size[0]//2,size[1]//2 if mode=='center' else size[1]-margin]
    # Asymmetric held-helper poses must fit around BOSS root, not pair centroid.
    if anchors:
        for i,((im,rect),b) in enumerate(zip(cells,boxes)):
            aa=[anchors[i][0]-rect[0],anchors[i][1]-rect[1]]
            oy=offsets[i] if offsets else 0
            for available,extent in [(anchor[0]-12,aa[0]-b[0]),(size[0]-12-anchor[0],b[2]-aa[0]),
                                     (anchor[1]+oy-12,aa[1]-b[1]),(size[1]-12-anchor[1]-oy,b[3]-aa[1])]:
                if extent>0:scale=min(scale,available/extent)
    folder=OUT/name;folder.mkdir(exist_ok=True)
    columns=min(8,len(cells));padding=2
    atlas=Image.new('RGBA',(columns*(size[0]+4),math.ceil(len(cells)/columns)*(size[1]+4)))
    for i,((im,rect),b) in enumerate(zip(cells,boxes)):
        alpha=im.getchannel('A');sw,sh=im.size
        source_edge=sum(sum(alpha.crop(v).histogram()[32:]) for v in [(0,0,sw,1),(0,sh-1,sw,sh),(0,0,1,sh),(sw-1,0,sw,sh)])
        if source_edge:raise ValueError((name,i,'source frame cut touches visible pixels',source_edge))
        part=im.crop(b); dims=[round(part.width*scale),round(part.height*scale)]
        part=part.resize(dims,Image.Resampling.NEAREST)
        source_anchor=[(b[0]+b[2])/2,(b[1]+b[3])/2 if mode=='center' else b[3]]
        if mode=='feet':
            foot=im.getchannel('A').crop((0,max(0,b[3]-12),im.width,b[3]))
            f=foot.point(lambda a:255 if a>=64 else 0).getbbox()
            source_anchor[0]=(f[0]+f[2])/2
        if anchors:source_anchor=[anchors[i][0]-rect[0],anchors[i][1]-rect[1]]
        x=round(anchor[0]-(source_anchor[0]-b[0])*scale)
        y=round(anchor[1]-(source_anchor[1]-b[1])*scale)
        if offsets:y+=offsets[i]
        if x<8 or x+part.width>size[0]-8 or y<8 or y+part.height>size[1]-8:
            raise ValueError((name,i,'frame exceeds padded canvas',x,y,dims,source_anchor))
        canvas=Image.new('RGBA',size);canvas.alpha_composite(part,(x,y));frames.append(canvas)
        canvas.save(folder/f'{i:02d}.png',optimize=True)
        ax=(i%columns)*(size[0]+4)+2;ay=(i//columns)*(size[1]+4)+2
        atlas.alpha_composite(canvas,(ax,ay))
        records.append({'file':f'{name}/{i:02d}.png','rect':[ax,ay,*size],
                        'sourceRect':rect,'sourceAlphaBounds':list(b),'sourceAnchor':source_anchor,
                        'sharedScale':scale,'offset':[x,y],'sourceCutEdgePixelsAlpha32':source_edge})
    atlas.save(folder/'atlas.png',optimize=True)
    unique=len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames})
    edge=sum(sum(f.getchannel('A').crop(box).histogram()[32:]) for f in frames
             for box in [(0,0,size[0],1),(0,size[1]-1,size[0],size[1]),(0,0,1,size[1]),(size[0]-1,0,size[0],size[1])])
    assert edge==0 and unique>1,(name,edge,unique)
    QA.append({'name':name,'frames':len(frames),'uniqueFrames':unique,'outerEdgePixelsAlpha32':edge,
               'sourceCutEdgePixelsAlpha32':sum(f['sourceCutEdgePixelsAlpha32'] for f in records),
               'allCornersTransparent':all(f.getpixel((0,0))[3]==0 for f in frames)})
    fam={'atlas':f'{name}/atlas.png','size':list(size),'anchor':anchor,'fps':fps,'loop':loop,
         'group':group,'source':key,'events':events or {},'notes':notes,'frames':records}
    FAMILIES[name]=fam
    (folder/'reel.json').write_text(json.dumps(fam,indent=2)+'\n',encoding='utf-8')
    previews=[]
    for f in frames:
        bg=Image.new('RGBA',size,(15,24,34,255));bg.alpha_composite(f);previews.append(bg.convert('RGB'))
    previews[0].save(OUT/'review'/f'{name}.gif',save_all=True,append_images=previews[1:],
                    duration=round(1000/fps),loop=0,disposal=2)

for key,prefix in [('boss_moonwalk_profile','boss_moonwalk'),('boss_moonwalk_armored_profile','armored_moonwalk')]:
    cells=grid(key,4,4)
    for j,direction in enumerate(['left','right']):
        add(prefix+'_'+direction,key,cells[j*8:(j+1)*8],(448,480),10,'boss',body_height=240,
            notes='Backward heel/toe glide. Translate actor '+direction+' while facing opposite direction. Eight authored frames; no canvas rotation.')

add('boss_lasso_360','boss_lasso',grid('boss_lasso',4,3),(448,480),12,'boss',body_height=276,
    offsets=[0,-5,-12,-7,-4,-12,0,-10,-13,-4,-12,-5],
    notes='Twelve authored front/side/back/side turn views. Review uses small hop offsets; synchronize jump/turn cadence to music in runtime.')
add('helper_lasso_360','helper_lasso',grid('helper_lasso',4,3),(176,200),12,'helper',
    offsets=[0,-3,-6,-4,-3,-6,0,-5,-6,-3,-6,-3],
    notes='One complete lasso turn. Authored poses, no HTML rotation. Hop timing may be tuned independently.')
add('double_hammer_slam','double_slam_padded',grid('double_slam_padded',4,3),(448,480),12,'boss',loop=False,
    body_height=INPUTS.get('bodyHeights',{}).get('double_slam_padded'),events={'2':'slam_first','7':'slam_second'},
    notes='Two separate impacts for the two-word musical cue. Impact FX, camera shake and sound remain separate engine layers.')
add('hammer_toss_helper_throw','toss_helper_padded',grid('toss_helper_padded',4,4),(448,480),12,'boss',loop=False,
    body_height=INPUTS.get('bodyHeights',{}).get('toss_helper_padded'),anchors=INPUTS.get('anchors',{}).get('toss_helper_padded'),
    events={'3':'detach_hammer','6':'attach_helper','10':'release_helper','13':'beckon_helper','14':'summon_helper'},
    notes='Boss+helper composite during pickup/carry. Hide standalone helper for attached frames; use separate airborne reel on release.')
add('helper_airborne_tumble','helper_flight',grid('helper_flight',4,2),(176,200),14,'helper','center',
    notes='Eight authored tumbling views. Position/velocity/scale follow projectile trajectory; mouth layer on front-visible views only.')
for key,prefix,group in [('boss_singing','boss_speaker','head'),('helper_singing','helper_speaker','head')]:
    cells=grid(key,4,2)
    for j,cycle in enumerate(['sing','chant']):
        add(prefix+'_'+cycle,key,cells[j*4:(j+1)*4],(128,144),12,group,'bottom',
            notes='Neck anchor bottom center; modular replacement head, not a floating duplicate. No baked text. Match body-view/head scale at integration.')
hc=grid('hammer_flight_corrected',4,2)
single_path=Path(INPUTS['paths']['hammer_up_left']);single_saved=SOURCE/'hammer_up_left.png'
if single_path.exists() and single_path.resolve()!=single_saved.resolve():shutil.copy2(single_path,single_saved)
single=Image.open(single_saved).convert('RGBA');sb=bounds(single);single=single.crop(sb)
prescale=378/single.height;single=single.resize((round(single.width*prescale),378),Image.Resampling.NEAREST)
up_cell=Image.new('RGBA',(444,443));up_cell.alpha_composite(single,((444-single.width)//2,32))
# New generated up-left view completes the missing quadrant. No image rotation.
spin=[hc[0],hc[1],hc[2],(up_cell,[0,0,444,443]),hc[4],hc[5],hc[6],hc[3]]
add('hammer_airborne_spin','hammer_flight_corrected',spin,(224,224),14,'prop','center',body_height=900,
    notes='Detached canonical cylindrical hammer. Full end-over-end turn; common drum-center pivot. Use authored poses, not CSS rotation.',
    anchors=[[240,135],[630,170],[1180,250],[281,330],[240,740],[625,720],[958,676],[1465,147]])
FAMILIES['hammer_airborne_spin']['frames'][3]['sourceOverride']={'file':'hammer_up_left.png','originalAlphaBounds':list(sb),'preScale':prescale,'cellPadding':[(444-single.width)//2,32]}
(OUT/'hammer_airborne_spin/reel.json').write_text(json.dumps(FAMILIES['hammer_airborne_spin'],indent=2)+'\n',encoding='utf-8')
add('boss_vocal_leap','boss_vocal_leap',grid('boss_vocal_leap',4,3),(448,520),12,'boss',loop=False,
    body_height=INPUTS.get('bodyHeights',{}).get('boss_vocal_leap'),anchors=INPUTS.get('anchors',{}).get('boss_vocal_leap'),
    offsets=[0,0,0,-25,-60,-80,-55,-20,0,0,0,0],
    events={'3':'takeoff','5':'apex','8':'slam_impact','11':'recovered'},
    notes='Vocal grille on torso; modular speaker head can provide mouth animation. Preserve airborne root offsets; captions/audio remain separate layers.')

manifest={'version':1,'date':'2026-09-28','scope':'Hama art-only pack; not wired to gameplay',
          'method':'built-in image_gen; Pillow import only crops/scales/pads/packs pixels',
          'families':FAMILIES,'timing':'Preview FPS and frame cues only. No song recording or verified timestamps supplied.'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(OUT/'qa.json').write_text(json.dumps({'families':len(FAMILIES),'frames':sum(len(f['frames']) for f in FAMILIES.values()),'checks':QA},indent=2)+'\n',encoding='utf-8')

tiles=[]
for name,fam in FAMILIES.items():
    tile=Image.new('RGB',(300,340),(15,24,34));d=ImageDraw.Draw(tile)
    d.text((12,10),name,fill=(217,232,246))
    im=Image.open(OUT/fam['frames'][len(fam['frames'])//2]['file']).convert('RGBA')
    im.thumbnail((280,295),Image.Resampling.NEAREST)
    tile.paste(im,((300-im.width)//2,36),im);tiles.append(tile)
contact=Image.new('RGB',(1500,math.ceil(len(tiles)/5)*340),(15,24,34))
for i,tile in enumerate(tiles):contact.paste(tile,((i%5)*300,(i//5)*340))
contact.save(OUT/'review/contact.png')
duet=[]
for i in range(12):
    stage=Image.new('RGBA',(960,520),(15,24,34,255))
    boss=Image.open(OUT/FAMILIES['boss_lasso_360']['frames'][i]['file']).convert('RGBA')
    helper=Image.open(OUT/FAMILIES['helper_lasso_360']['frames'][i]['file']).convert('RGBA')
    stage.alpha_composite(boss,(256,20))
    stage.alpha_composite(helper,(152,300))
    stage.alpha_composite(helper,(632,300))
    duet.append(stage.convert('RGB'))
duet[0].save(OUT/'review/lasso_breakdown.gif',save_all=True,append_images=duet[1:],duration=90,loop=0,disposal=2)
print(json.dumps({'families':len(FAMILIES),'frames':sum(len(f['frames']) for f in FAMILIES.values()),'sizeBytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())}))
