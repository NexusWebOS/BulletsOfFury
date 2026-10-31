"""Import generated authored 16-bit Yuri banks, with crop/pivot provenance.
No synthetic body poses. Single proportional scale per source, binary alpha,
connected alpha spans isolate complete figures instead of uniform grid guesses.
"""
from pathlib import Path
import json, hashlib, statistics
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion16_yuri'
SRC=OUT/'source';FR=OUT/'frames';QA=ROOT/'_shots/bastion16_yuri'
FR.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
D={'version':'1013-bastion16-r1','generator':'built-in image_gen','assets':{},'sequences':{},'audit':[]}
CELL=(192,192);ANCHOR=(96,172)
def spans(values,gap=10):
    indices=np.where(values)[0]
    if not len(indices):return []
    groups=np.split(indices,np.where(np.diff(indices)>gap)[0]+1)
    return [(int(g[0]),int(g[-1])+1) for g in groups]
def getrow(name,y0,y1,n):
    src=Image.open(SRC/(name+'.png')).convert('RGBA')
    row=src.crop((0,y0,src.width,y1));a=np.array(row.getchannel('A'))
    xs=spans((a>=128).sum(axis=0)>3,12)
    assert len(xs)==n,(name,y0,xs)
    out=[]
    for x0,x1 in xs:
        im=row.crop((max(0,x0-2),0,min(src.width,x1+2),row.height))
        im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
        b=im.getbbox();im=im.crop(b)
        rect=[max(0,x0-2)+b[0],y0+b[1],max(0,x0-2)+b[2],y0+b[3]]
        out.append((im,rect))
    return out
def emit(key,item,source,s,sector=2,kind='normal',center=None):
    im,rect=item;a=np.array(im).astype(float)
    # Physical root follows the brown hair center, not the protruding rifle.
    brown=(a[:,:,0]>30)&(a[:,:,0]>a[:,:,1]*1.24)&(a[:,:,1]>a[:,:,2]*1.16)&(a[:,:,1]>18)&(a[:,:,0]<140)&(a[:,:,3]>0)
    if kind!='death':brown[int(im.height*.55):]=False
    yy,xx=np.where(brown)
    cx=float(np.median(xx)) if len(xx)>10 and kind!='death' else im.width/2
    if center is not None:cx=center
    sz=(round(im.width*s),round(im.height*s))
    origin=(round(ANCHOR[0]-cx*s),round(ANCHOR[1]-im.height*s))
    assert min(origin)>1 and origin[0]+sz[0]<CELL[0]-1 and origin[1]+sz[1]<CELL[1]-1,(key,origin,sz)
    frame=Image.new('RGBA',CELL);frame.alpha_composite(im.resize(sz,Image.Resampling.NEAREST),origin)
    b=frame.getbbox();file=FR/(key+'.png');frame.save(file,optimize=True)
    meta={'file':file.relative_to(ROOT).as_posix(),'size':list(CELL),'anchor':list(ANCHOR),'bounds':b,'drawScale':1}
    # Authored gun socket: dark pixels in the upper gun region, directional extreme.
    ar=np.array(im).astype(float);mx=ar[:,:,:3].max(axis=2);mn=ar[:,:,:3].min(axis=2)
    gun=(ar[:,:,3]>0)&((mx-mn)<55)&(mx>10)&(mx<155)
    gun[int(im.height*(.28 if kind=='blind' else .34)):]=False
    gy,gx=np.where(gun)
    if len(gx)>5:
        if sector<2:tx=float(np.percentile(gx,3))
        elif sector>2:tx=float(np.percentile(gx,97))
        else:tx=float(np.median(gx))
        near=np.abs(gx-tx)<5
        ty=float(np.median(gy[near])) if near.any() else float(np.median(gy))
    else:tx,ty=cx,im.height*.15
    meta['muzzle']=[round(origin[0]+tx*s,2),round(origin[1]+ty*s,2)]
    D['assets'][key]=meta
    D['audit'].append({'key':key,'source':source+'.png','crop':rect,'scale':s,'rootX':cx,'sourceFootY':im.height,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    return key
def sequence(name,keys,fps=12,loop=True):
    D['sequences'][name]={'frames':keys,'fps':fps,'loop':loop,'rootContract':{'cell':CELL,'anchor':ANCHOR,'scale':'one proportional scale per source','physicalRoot':'feet baseline and head/pelvis axis'}}
    contact=Image.new('RGBA',(len(keys)*192,192),(16,25,36,255))
    onion=Image.new('RGBA',contact.size,(16,25,36,255))
    for j,key in enumerate(keys):
        im=Image.open(FR/(key+'.png'));contact.alpha_composite(im,(j*192,0))
        for idx,alpha in [((j-1)%len(keys),60),((j+1)%len(keys),60),(j,210)]:
            q=Image.open(FR/(keys[idx]+'.png'));q.putalpha(q.getchannel('A').point(lambda a:a*alpha//255));onion.alpha_composite(q,(j*192,0))
        dr=ImageDraw.Draw(onion);dr.line((j*192+96,0,j*192+96,192),fill=(80,170,210));dr.line((j*192,172,(j+1)*192,172),fill=(80,170,210))
    contact.convert('RGB').save(QA/(name+'_contact.png'));onion.convert('RGB').save(QA/(name+'_onion.png'))
    return keys
aimrows=[getrow('aim',a,b,5) for a,b in [(0,320),(320,595),(595,885),(885,1122)]]
perm=[0,3,2,1,4] # Generated oblique columns point opposite their nominal positions.
for row,name in [(0,'aim'),(3,'crouch')]:
    sequence('pb16_yuri_'+name,[emit(f'pb16_yuri_{name}_{d}',aimrows[row][c],'aim',.435,d) for d,c in enumerate(perm)],8)
for d,c in enumerate(perm):
    keys=[f'pb16_yuri_aim_{d}']
    keys += [emit(f'pb16_yuri_fire_{d}_{i}',aimrows[r][c],'aim',.435,d) for i,r in enumerate([1,2])]
    sequence(f'pb16_yuri_fire_{d}',keys+[keys[0]],20)
forward_fire=getrow('forward_fire',0,756,4)
sequence('pb16_yuri_fire_2',[emit(f'pb16_yuri_fire_forward_{i}',item,'forward_fire',.18,2) for i,item in enumerate(forward_fire)],20)
for name,ys,s in [('forward_motion',[(0,231),(231,420),(420,644),(644,887)],.55),('left_motion',[(0,240),(240,433),(433,669),(669,887)],.55)]:
    for r,bank in enumerate(['strafe','crouch_strafe','rise','advance']):
        if name=='left_motion' and r>1:continue
        suffix=('_0' if name=='left_motion' else '')
        keys=[emit(f'pb16_yuri_{bank}{suffix}_{i}',item,name,s,0 if suffix else 2) for i,item in enumerate(getrow(name,*ys[r],8))]
        sequence('pb16_yuri_'+bank+suffix,keys,12,bank not in ['rise'])
for d in range(5):
    items=[getrow('blindfire',a,b,5)[d] for a,b in [(0,307),(307,600),(600,854),(854,1122)]]
    sequence(f'pb16_yuri_blindfire_{d}',[emit(f'pb16_yuri_blindfire_{d}_{i}',item,'blindfire',.435,d,'blind') for i,item in enumerate(items)],14)
for bank,ys in [('death',(0,415)),('revive',(415,724))]:
    items=getrow('death_revive',*ys,8)
    sequence('pb16_yuri_'+bank,[emit(f'pb16_yuri_{bank}_{i}',item,'death_revive',.41 if bank=='revive' else .34,2,'death') for i,item in enumerate(items)],10,False)
D['sources']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.png')}
D['promptSet']='source/prompts.json'
for k,m in D['assets'].items():
    im=Image.open(ROOT/m['file']);assert all(n%2==0 for n in im.size)
    assert set(im.getchannel('A').getdata()).issubset({0,255})
(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_BASTION16_YURI_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({'frames':len(D['assets']),'banks':len(D['sequences']),'canvas':CELL,'alpha':'binary','sources':len(D['sources'])}))

