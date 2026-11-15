"""Build and integrate authored whole-character locomotion; never fit poses separately."""
from collections import deque
from pathlib import Path
from PIL import Image, ImageSequence
import hashlib, json, os, re, shutil, statistics, subprocess, zipfile

NATIVE=Path(__file__).resolve().parents[1]
PROJECT=NATIVE.parent
SRC=NATIVE/'source/fullframe-v4'
REVIEW=Path(os.environ.get('ELEMENTALIST_MOVEMENT_REVIEW',str(SRC/'review')))
CELL=(192,192);ORIGIN=(96,167)
ASE=os.environ.get('ASEPRITE_EXE') or shutil.which('aseprite') or 'aseprite'
INV=json.loads((SRC/'enemy-inventory.json').read_text(encoding='utf-8'))
ORDER=['tyler-nohood','damien','harker']+list(INV)
LABELS={'tyler-nohood':'Tyler','damien':'Damien','harker':'Harker',**{k:v['label'] for k,v in INV.items()}}
SOURCE_ID={'tyler-nohood':'tyler'}
PHASES={'walk':['Near contact','Near load','Far passing','Far swing','Far contact','Far load','Near passing','Near swing'],
 'run':['Near strike','Near compression','Far passing','Flight','Far strike','Far compression','Near passing','Flight']}

def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def block(text,action):
    m=re.search(r'(?ms)^anim '+re.escape(action)+r'\n(.*?)(?=^anim |\Z)',text)
    return m[0] if m else None
def hard(im):
    im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));return im

def clear_exterior_matte(im):
    # Some generated alpha exports contain a pale exterior. Flood only from
    # the cell border, so enclosed white eyes, shoe panels and fire cores stay.
    pix=im.load();w,h=im.size;queue=deque();seen=set()
    corner=[pix[x,y] for x,y in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]]
    needs_key=any(a>=128 and min(r,g,b)>200 and max(r,g,b)-min(r,g,b)<25 for r,g,b,a in corner)
    if not needs_key:return hard(im)
    def exterior(x,y):
        r,g,b,a=pix[x,y]
        return a<245 or (min(r,g,b)>145 and max(r,g,b)-min(r,g,b)<26)
    for x in range(w):
        for y in (0,h-1):
            if exterior(x,y):queue.append((x,y));seen.add((x,y))
    for y in range(h):
        for x in (0,w-1):
            if exterior(x,y) and (x,y) not in seen:queue.append((x,y));seen.add((x,y))
    while queue:
        x,y=queue.popleft()
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<w and 0<=yy<h and (xx,yy) not in seen and exterior(xx,yy):
                seen.add((xx,yy));queue.append((xx,yy))
    for x,y in seen:
        r,g,b,a=pix[x,y];pix[x,y]=(r,g,b,0)
    return hard(im)

def clean_components(im):
    # Drop detached export confetti, preserving nearby authored flame tongues.
    alpha=im.getchannel('A');coords={(i%384,i//384) for i,v in enumerate(alpha.tobytes()) if v}
    groups=[]
    while coords:
        p=coords.pop();group=[p];queue=deque([p])
        while queue:
            x,y=queue.popleft()
            for yy in range(y-1,y+2):
                for xx in range(x-1,x+2):
                    n=(xx,yy)
                    if n in coords:coords.remove(n);group.append(n);queue.append(n)
        groups.append(group)
    groups.sort(key=len,reverse=True)
    assert groups and len(groups[0])>1500
    main=groups[0];xs=[p[0] for p in main];ys=[p[1] for p in main]
    b=(min(xs)-10,min(ys)-10,max(xs)+10,max(ys)+10)
    keep=main[:]
    for group in groups[1:]:
        if len(group)>=3 and all(b[0]<=x<=b[2] and b[1]<=y<=b[3] for x,y in group):keep.extend(group)
    mask=Image.new('L',im.size);mask.putdata([0]*(384*384))
    pixels=mask.load()
    for x,y in keep:pixels[x,y]=255
    removed=sum(len(g) for g in groups)-len(keep)
    im.putalpha(mask)
    return im,removed

def split(path):
    im=Image.open(path).convert('RGBA')
    assert abs(im.width/im.height-2)<.005,(path,im.size)
    im=im.resize((1536,768),Image.Resampling.NEAREST)
    out=[];removed=[]
    for i in range(8):
        frame=im.crop((i%4*384,i//4*384,(i%4+1)*384,(i//4+1)*384))
        f,n=clean_components(clear_exterior_matte(frame));out.append(f);removed.append(n)
    return out,removed

def root_x(frame,char):
    b=frame.getbbox();points=[];pix=frame.load()
    for y in range(round(b[1]+.52*(b[3]-b[1])),round(b[1]+.59*(b[3]-b[1]))):
        runs=[];start=None
        for x in range(105,280):
            r,g,blue,a=pix[x,y]
            if char in ('bat','firebat') and r>120 and r>g*1.6 and g<90 and blue<90:a=0
            if a and start is None:start=x
            if not a and start is not None:runs.append((start,x));start=None
        if start is not None:runs.append((start,280))
        runs=[p for p in runs if p[1]-p[0]>=20]
        if not runs:continue
        selected=min(runs,key=lambda p:abs((p[0]+p[1])/2-192))
        if selected[1]-selected[0]<(210 if char=='fireboss' else 130):points.append(sum(selected)/2)
    assert points,(char,'pelvis registration required')
    return statistics.median(points)

def unit(text):
    paths=re.findall(r'(?m)^frame (.+)$',block(text,'idle'))
    heights=[]
    for p in paths:
        b=Image.open(NATIVE/p).convert('RGBA').getbbox();heights.append(b[3]-b[1])
    return round(statistics.median(heights))

def delays(text,action,fallback):
    content=block(text,action)
    if not content:return fallback
    current=10;values=[]
    for line in content.splitlines():
        if line.startswith('delay '):current=int(line.split()[1])
        elif line.startswith('frame '):values.append(current)
    return sum(values)

def redistribute(total):return [round((i+1)*total/8)-round(i*total/8) for i in range(8)]

def palette_for(text):
    path=re.search(r'(?m)^frame (.+)$',block(text,'idle'))[1]
    im=Image.open(NATIVE/path);assert im.mode=='P'
    colors=im.getpalette()[:768]
    q=Image.new('P',(1,1));q.putpalette(colors[3:]+colors[3:6])
    return q,colors

def encode(im,palette,colors):
    q=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE)
    result=Image.new('P',im.size);result.putpalette(colors)
    result.putdata([((v+1) if v<255 else 1) if a else 0 for v,a in zip(q.tobytes(),im.getchannel('A').tobytes())])
    result.info['transparency']=0
    return result

def gif(path,frames,ms):
    rgb=[]
    for frame in frames:
        f=frame.copy().convert('RGBA');bg=Image.new('RGB',CELL,'#17202e');bg.paste(f,mask=f.getchannel('A'));rgb.append(bg)
    rgb[0].save(path,save_all=True,append_images=rgb[1:],duration=ms,loop=0,disposal=2)
    with Image.open(path) as check:
        assert check.n_frames==8
        assert sum(f.info['duration'] for f in ImageSequence.Iterator(check))==sum(ms)

def build():
    REVIEW.mkdir(parents=True,exist_ok=True)
    backup=SRC/'pre-movement-backup.zip'
    beforefile=SRC/'pre-movement-hashes.json'
    if not backup.exists():
        paths=[NATIVE/f'data/chars/{c}/{c}.txt' for c in ORDER]+[NATIVE/'Paks/Elementalist.pak']
        with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
            for p in paths:z.write(p,p.relative_to(NATIVE).as_posix())
        write(beforefile,json.dumps({p.relative_to(NATIVE).as_posix():digest(p) for p in paths},indent=2)+'\n')
    with zipfile.ZipFile(backup) as z:
        originals={c:z.read(f'data/chars/{c}/{c}.txt').decode('utf-8').replace('\r\n','\n') for c in ORDER}
    roster={'packs':{}};report={};catalog={};changed=['data/scripts/locomotion.c']
    for char in ORDER:
        sid=SOURCE_ID.get(char,char);text=originals[char];height=unit(text)
        sheets={};confetti={}
        for a in ('walk','run'):sheets[a],confetti[a]=split(SRC/'raw'/f'{sid}-{a}.png')
        scale=height/statistics.median(f.getbbox()[3]-f.getbbox()[1] for f in sheets['walk'])
        # Calibrate each complete source sheet to the SAME body unit. The
        # validated SpriteCook run projects to 116/126 of standing height.
        # One factor applies to all eight run drawings; no per-pose fitting.
        scales={'walk':scale,'run':height*(116/126)/statistics.median(f.getbbox()[3]-f.getbbox()[1] for f in sheets['run'])}
        normalized={};recipes={};palette,colors=palette_for(text)
        walk_total=delays(text,'walk',100);run_total=delays(text,'run',max(32,round(walk_total*.72)))
        clocks={'walk':redistribute(walk_total),'run':redistribute(run_total)}
        roster['packs'][char]={};catalog[char]={'label':LABELS[char],'actions':{}}
        for action,frames in sheets.items():
            normalized[action]=[];recipes[action]=[]
            atlas=Image.new('RGBA',(1536,192));entry=[]
            flight=[0,0,0,4,0,0,0,2] if action=='run' else [0]*8
            for i,frame in enumerate(frames):
                xroot=root_x(frame,char)
                sheet_scale=scales[action]
                small=hard(frame.resize((round(384*sheet_scale),round(384*sheet_scale)),Image.Resampling.NEAREST))
                b=small.getbbox();x=ORIGIN[0]-round(xroot*sheet_scale);y=ORIGIN[1]-flight[i]-b[3]
                output=Image.new('RGBA',CELL);output.paste(small,(x,y))
                assert output.getchannel('A').histogram()[255]==small.getchannel('A').histogram()[255],(char,action,i,'clipped')
                b=output.getbbox();assert b[0]>3 and b[1]>3 and b[2]<189 and b[3]<189,(char,action,i,b)
                p=encode(output,palette,colors)
                filename=f'm1105-{action}-{i:02}.png';target=NATIVE/f'data/chars/{char}/{filename}'
                target.parent.mkdir(parents=True,exist_ok=True);p.save(target,transparency=0,bits=8)
                saved=Image.open(target);assert saved.getpalette()[:768]==colors and saved.info.get('transparency')==0
                assert set(saved.convert('RGBA').getchannel('A').tobytes())=={0,255}
                normalized[action].append(p);atlas.paste(p.copy().convert('RGBA'),(192*i,0))
                entry += [f'delay {clocks[action][i]}','offset 96 167','bbox 81 63 30 104 14',
                    'attack 0 0 0 0 0 0 0 1 0 0',f'frame data/chars/{char}/{filename}']
                recipes[action].append({'frame':i,'pelvis_x':xroot,'translation':[x,y],'bounds':b,
                    'flight_gap':flight[i],'delay_centiseconds':clocks[action][i],'removed_export_confetti':confetti[action][i]})
                changed.append(target.relative_to(NATIVE).as_posix())
            content='anim '+action+'\nloop 1\n'+'\n'.join(entry)+'\n\n'
            old=block(text,action)
            text=text.replace(old,content,1) if old else text.rstrip()+'\n\n'+content
            out=SRC/'native'/char;out.mkdir(parents=True,exist_ok=True);atlas.save(out/f'{action}.png')
            meta={'character':char,'action':action,'frame_size':CELL,'origin':ORIGIN,'body_unit':height,
                'whole_sheet_scale':scales[action],'animation':{'frames':[str(i) for i in range(8)],
                    'duration_ticks':[v*.6 for v in clocks[action]],'duration_ms':[v*10 for v in clocks[action]],'phases':PHASES[action]},
                'atlas':{'image':action+'.png','rects':[{'x':192*i,'y':0,'w':192,'h':192} for i in range(8)]},
                'method':'One complete drawn pose per frame; shared anatomical scale for walk and run; whole-frame registration',
                'motion_reference':'Smooth SpriteCook 8-frame cycle','source_reference_duration_ms':[125]*8,'flight_gaps':flight}
            write(out/f'{action}.json',json.dumps(meta,indent=2)+'\n')
            subprocess.run([ASE,'-b','--script-param','metadata='+str(out/f'{action}.json'),'--script-param','output='+str(out/f'{action}.aseprite'),
                '--script',str(NATIVE/'tools/export_animation.lua')],check=True,capture_output=True)
            checkdir=SRC/'checks';checkdir.mkdir(exist_ok=True)
            checkpng=checkdir/f'{char}-{action}.png';checkjson=checkpng.with_suffix('.json')
            subprocess.run([ASE,'-b',str(out/f'{action}.aseprite'),'--sheet-type','horizontal','--sheet',str(checkpng),
                '--format','json-array','--data',str(checkjson)],check=True,capture_output=True)
            assert Image.open(checkpng).convert('RGBA').tobytes()==atlas.tobytes(),(char,action,'Aseprite pixel round trip')
            assert [f['duration'] for f in json.loads(checkjson.read_text(encoding='utf-8'))['frames']]==[v*10 for v in clocks[action]],(char,action,'timing')
            clip={'src':f'openbor/source/fullframe-v4/native/{char}/{action}.png','cell':CELL,'origin':ORIGIN,
                'frames':8,'rects':meta['atlas']['rects'],'ticks':meta['animation']['duration_ticks'],'displayScale':1,'phases':PHASES[action]}
            roster['packs'][char][action]=clip
            preview=REVIEW/'previews';preview.mkdir(exist_ok=True)
            gif(preview/f'{char}-{action}.gif',normalized[action],[v*10 for v in clocks[action]])
            atlas.save(preview/f'{char}-{action}-strip.png')
            catalog[char]['actions'][action]={'source':'previews/SpriteCook-'+action+'-strip.png','result':f'previews/{char}-{action}-strip.png',
                'gif':f'previews/{char}-{action}.gif','aseprite':f'openbor/source/fullframe-v4/native/{char}/{action}.aseprite',
                'durations':[v*10 for v in clocks[action]],'heights':[p.copy().convert('RGBA').getbbox()[3]-p.copy().convert('RGBA').getbbox()[1] for p in normalized[action]],
                'phases':PHASES[action],'flight':flight}
        if char not in ('tyler-nohood','damien'):
            speed=float(re.search(r'(?m)^speedf ([\d.]+)',text)[1]);run=round(speed*1.6,4)
            # Keep the normal wandering option, and enable native occasional chase/run.
            # OpenBOR chooses RUN only for a long horizontal approach, then WALK nearby.
            header,tail=text.split('anim ',1)
            header=re.sub(r'(?m)^aimove .*\n','',header)
            header=re.sub(r'(?m)^run.speed.x .*\n','',header)
            header=re.sub(r'(?m)^onmovexscript .*\n','',header)
            header+=f'aimove wander chase\nrun.speed.x {run:.4f}\nonmovexscript data/scripts/locomotion.c\n\n'
            text=header+'anim '+tail
        target=NATIVE/f'data/chars/{char}/{char}.txt';write(target,text);changed.append(target.relative_to(NATIVE).as_posix())
        wh=catalog[char]['actions']['walk']['heights']
        assert max(wh)-min(wh)<=max(5,height*.05),(char,'standing scale drift',wh)
        report[char]={'label':LABELS[char],'body_unit':height,'whole_sheet_scales':scales,
            'walk_heights':wh,'run_heights':catalog[char]['actions']['run']['heights'],
            'walk_period_ms':walk_total*10,'run_period_ms':run_total*10,'recipes':recipes,
            'native_palette_preserved':True,'aseprite_roundtrips':2}
        print(char, 'unit',height,'walk',wh,'run',report[char]['run_heights'],flush=True)
    write(SRC/'roster.json',json.dumps(roster,indent=2)+'\n')
    write(SRC/'integration-checks.json',json.dumps({'characters':report,'clips':36,'frames':288,'changed_files':changed,
        'common_root':ORIGIN,'native_palette_compatibility_verified':True,'aseprite_pixel_and_timing_roundtrips':36},indent=2)+'\n')
    write(REVIEW/'viewer-data.js','window.ROSTER='+json.dumps(catalog)+';\n')
    for action in ('walk','run'):
        atlas=Image.new('RGBA',(1536,192));source_origin=(66,126) if action=='walk' else (64,116)
        with Image.open(SRC/'references'/f'tyler-{action}-spritecook.webp') as source:
            for i,f in enumerate(ImageSequence.Iterator(source)):
                atlas.alpha_composite(f.convert('RGBA'),(i*192+96-source_origin[0],167-source_origin[1]))
        atlas.save(REVIEW/'previews'/f'SpriteCook-{action}-strip.png')
    print('Integrated 36 clips / 288 frames. Native engine checks still required.')

if __name__=='__main__':build()
