"""Normalize real PixelLab poses; split complementary depth plates, never invent VFX."""
from pathlib import Path
import hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/lightning_depth_1018'
O=R/'assets/game/shared/combat/lightning_1018'
Q=R/'_shots/lightning_depth_1018/art'

def clean(path):
    v=np.array(Image.open(path).convert('RGBA'))
    # Transparent pixels can retain a blue segmentation RGB. Clear only their
    # invisible channels, leaving every authored visible RGBA pixel untouched.
    v[v[:,:,3]==0]=0
    return Image.fromarray(v)

def padded(im,pad):
    c=Image.new('RGBA',(im.width+pad*2,im.height+pad*2))
    c.paste(im,(pad,pad))
    return c

def contact(name,frames):
    size=128;sheet=Image.new('RGBA',(size*4,(size+18)*math.ceil(len(frames)/4)),'#0c1420');g=ImageDraw.Draw(sheet)
    for i,im in enumerate(frames):
        preview=im.copy();preview.thumbnail((size,size),Image.Resampling.NEAREST)
        x=(i%4)*size+(size-preview.width)//2;y=(i//4)*(size+18)+(size-preview.height)//2
        sheet.alpha_composite(preview,(x,y));g.text(((i%4)*size+4,(i//4)*(size+18)+size+2),str(i),fill='white')
    sheet.convert('RGB').save(Q/(name+'-sheet.png'))
    onions=Image.new('RGBA',(128*8,146),'#0c1420')
    for j,i in enumerate(np.linspace(0,len(frames)-1,8).astype(int)):
        for offset,color,alpha in [(-1,(40,210,255),80),(1,(255,50,180),80),(0,(255,255,255),220)]:
            im=frames[(i+offset)%len(frames)].copy();im.thumbnail((128,128),Image.Resampling.NEAREST)
            if offset:
                tint=Image.new('RGBA',im.size,(*color,0));tint.putalpha(im.getchannel('A').point(lambda p:p*alpha//255));im=tint
            else:im.putalpha(im.getchannel('A').point(lambda p:p*alpha//255))
            onions.alpha_composite(im,(j*128+(128-im.width)//2,(128-im.height)//2))
        ImageDraw.Draw(onions).text((j*128+4,130),str(i),fill='white')
    onions.convert('RGB').save(Q/(name+'-onion.png'))
    gif=[]
    for im in frames:
        c=Image.new('RGBA',im.size,'#0c1420');c.alpha_composite(im);gif.append(c.convert('RGB'))
    gif[0].save(Q/(name+'.gif'),save_all=True,append_images=gif[1:],duration=62,loop=0,optimize=False)

def build():
    O.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
    data={'banks':{},'source':'PixelLab Pro seeds + PixMiniMax generated animation','owner':'_BUILD_SOURCE/build_lightning_depth_1018.py'}
    selections=json.loads((S/'selections.json').read_text(encoding='utf-8'))
    audit=[]
    def save(name,frames,raw,pad,**extra):
        w,h=frames[0].size;assert w%2==0 and h%2==0
        n=len(frames);assert 16<=n<=32 and len({f.tobytes() for f in frames})>=n-2,(name,'duplicate animation poses')
        rows=[]
        for i,im in enumerate(frames):
            assert im.size==(w,h) and im.getbbox(),(name,i,'empty or mismatched canvas')
            v=np.array(im);assert not v[0,:,3].any() and not v[-1,:,3].any() and not v[:,0,3].any() and not v[:,-1,3].any(),(name,i,'ink on export border')
            key=f'l21_{name}_{i:02}';path=O/(key+'.png');im.save(path,optimize=True)
            rows.append({'key':key,'path':path.relative_to(R).as_posix(),'w':w,'h':h,'pivot':[w//2,h//2],'bounds':list(im.getbbox()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        data['banks'][name]={'frames':rows,'w':w,'h':h,'pivot':[w//2,h//2],'fps':16,'source_size':list(raw),'padding':pad,'renderScale':h/raw[1],**extra}
        values=[np.array(f) for f in frames]
        diffs=[float(np.mean(np.abs(values[i].astype(float)-values[(i+1)%n].astype(float)))) for i in range(n)]
        audit.append({'bank':name,'poses':n,'size':[w,h],'pivot':[w//2,h//2],'unique':len({f.tobytes() for f in frames}),'loop_difference':diffs[-1],'median_adjacent_difference':float(np.median(diffs))})
        contact(name,frames)
    master={}
    for name,raw,pad in [('wrap',(256,256),32),('bolt',(128,128),16),('orb',(96,96),16),('tether',(256,128),16)]:
        files=sorted((S/'returned'/(name+'_loop')).glob('frame_*.png'));assert len(files)==33,(name,'expected input plus32 generated frames',len(files))
        selected=selections.get(name,list(range(1,33)));original=[clean(files[i]) for i in selected];assert all(im.size==raw for im in original),(name,'source geometry')
        assert all(np.count_nonzero(np.array(im)[:,:,3]>32)<im.width*im.height*.90 for im in original),(name,'opaque background')
        frames=[padded(im,pad) for im in original];master[name]=frames
        if name!='wrap':save(name,frames,raw,pad,axis=math.pi*.75 if name=='bolt' else 0)
    frames=master['wrap'];w,h=frames[0].size;yy,xx=np.mgrid[:h,:w];phi=np.arctan2((yy-h/2)/.9,xx-w/2)
    back=[];front=[]
    for i,im in enumerate(frames):
        v=np.array(im);near=np.sin(phi+i/32*math.tau*2)>0
        a=v.copy();b=v.copy();a[near]=0;b[~near]=0
        far=Image.fromarray(a);close=Image.fromarray(b)
        assert np.array_equal(np.array(Image.alpha_composite(far,close)),v),(i,'depth plates do not recompose exactly')
        back.append(far);front.append(close)
        im.save(Q/('wrap-reference-'+f'{i:02}.png'))
    save('wrap_back',back,(256,256),32);save('wrap_front',front,(256,256),32)
    contact('wrap-complete',frames)
    (R/'assets/lightning_art_1018.js').write_text('"use strict";\nconst L21_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    taxonomy=R/'assets/data/ART_TAXONOMY.json';old=json.loads(taxonomy.read_text(encoding='utf-8'))
    entry={'role':'boss_lightning_effects','sheet':None,'note':'PixelLab-generated branching lightning:32 paired exact-recomposing front/back wrap poses,32 forked bolt poses,24 selected crackling storm-orb poses and32 core-tether poses. Plain filled-circle orb returns excluded. Even fixed canvases/common pivots and proportional bank scale. Owner build_lightning_depth_1018.py; runtime lightning_depth_1018.js. Replaces crescent chains for Dracodia and upgrades Storm Sovereign electrical effects.'}
    taxonomy.write_text(json.dumps({'l21_':entry,**{k:v for k,v in old.items() if k!='l21_'}},indent=2)+'\n',encoding='utf-8',newline='\n')
    (S/'registration.json').write_text(json.dumps({'banks':audit,'exact_depth_reassembly':True,'source_indices':selections},indent=2)+'\n',encoding='utf-8')
    registered={a['key']+'.png' for b in data['banks'].values() for a in b['frames']}
    archive=S/'excluded_exports';archive.mkdir(exist_ok=True)
    for path in O.glob('l21_*.png'):
        if path.name in registered:continue
        dest=archive/path.name
        assert path.resolve().is_relative_to(R.resolve()) and dest.resolve().is_relative_to(R.resolve())
        if not dest.exists():path.rename(dest)
    print('Registered'+str(sum(len(b['frames']) for b in data['banks'].values()))+' real generated lightning poses in5 banks',flush=True)

if __name__=='__main__':build()
