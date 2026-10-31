"""Export authored 16-bit Bastion environment, machinery, boss and ordnance.

Only measured source crops, binary-alpha cleanup, proportional nearest scaling
and transparent padding. One scale per bank; no procedural replacement art.
"""
from pathlib import Path
import json, hashlib, statistics, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion16_environment'
SRC=OUT/'source'; FR=OUT/'frames'; QA=ROOT/'_shots/bastion16_environment'
for d in (SRC,FR,QA): d.mkdir(parents=True,exist_ok=True)
D={'version':'1013-bastion16-environment-r1','assets':{},'sequences':{},'audit':[], 'sources':{}}

def load(name):
    im=Image.open(SRC/(name+'.png')).convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
    return im

def save(key,im,anchor,src,rect,scale):
    b=im.getchannel('A').getbbox(); assert b, key
    assert im.width%2==0 and im.height%2==0,(key,im.size)
    if key!='pb16_stage': assert min(b[0],b[1],im.width-b[2],im.height-b[3])>=2,(key,b)
    f=FR/(key+'.png'); im.save(f,optimize=True)
    D['assets'][key]={'file':f.relative_to(ROOT).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(b),'drawScale':1}
    D['audit'].append({'key':key,'source':src+'.png','crop':list(rect),'proportionalScale':scale,'pixelStep':1 if key.startswith('pb16_reticle') else 2,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})

def bank(src,prefix,rects,target,cell=(192,192),center=False,largest=False,scale=None,baseline=None,fps=10):
    sheet=load(src); cuts=[]
    for rect in rects:
        cut=sheet.crop(rect)
        if largest:
            a=np.array(cut.getchannel('A')); labels,n=ndimage.label(a>0)
            counts=np.bincount(labels.ravel()); counts[0]=0
            a=np.where(labels==int(np.argmax(counts)),255,0).astype('uint8'); cut.putalpha(Image.fromarray(a))
        cuts.append(cut)
    boxes=[im.getchannel('A').getbbox() for im in cuts]
    assert all(boxes),prefix
    if scale is None:
        if target[0]: scale=target[0]/max(b[2]-b[0] for b in boxes)
        else: scale=target[1]/max(b[3]-b[1] for b in boxes)
    anchor=(cell[0]//2,cell[1]//2 if center else baseline or cell[1]-12)
    keys=[]
    for i,(cut,b,rect) in enumerate(zip(cuts,boxes,rects)):
        # A stable physical foot/base center, not independent per-frame fitting.
        cx=(b[0]+b[2])/2 if not prefix.startswith('pb16_helios') else cut.width/2
        cy=(b[1]+b[3])/2 if center else b[3]
        image=cut.crop(b)
        step=1 if prefix=='pb16_reticle' else 2
        small=(max(1,round(image.width*scale/step)),max(1,round(image.height*scale/step)))
        image=image.resize(small,Image.Resampling.NEAREST).resize((small[0]*step,small[1]*step),Image.Resampling.NEAREST)
        pos=(round((anchor[0]+(b[0]-cx)*scale)/2)*2,round((anchor[1]+(b[1]-cy)*scale)/2)*2)
        canvas=Image.new('RGBA',cell);canvas.alpha_composite(image,pos)
        key=f'{prefix}_{i}';save(key,canvas,anchor,src,rect,scale);keys.append(key)
    D['sequences'][prefix]={'frames':keys,'fps':fps,'drawScale':1,'scale':scale,'rootContract':{'cell':list(cell),'anchor':list(anchor),'method':'fixed proportional bank scale; bottom-center physical root; binary alpha; nearest two-pixel clusters'}}
    contact=Image.new('RGBA',(len(keys)*cell[0],cell[1]+24),(16,26,37,255))
    for i,k in enumerate(keys):
        contact.alpha_composite(Image.open(FR/(k+'.png')),(i*cell[0],24));ImageDraw.Draw(contact).text((i*cell[0]+4,4),k,fill='white')
    contact.convert('RGB').save(QA/(prefix+'_contact.png'))
    onion=Image.new('RGBA',(len(keys)*cell[0],cell[1]),(16,26,37,255))
    for i,k in enumerate(keys):
        for j,a in [((i-1)%len(keys),65),((i+1)%len(keys),65),(i,200)]:
            q=Image.open(FR/(keys[j]+'.png'));q.putalpha(q.getchannel('A').point(lambda v:v*a//255));onion.alpha_composite(q,(i*cell[0],0))
    onion.convert('RGB').save(QA/(prefix+'_onion.png'))

def rects(src,columns,y0,y1):
    w=load(src).width
    return [(round(i*w/columns),y0,round((i+1)*w/columns),y1) for i in range(columns)]

stage=load('stage'); stage=stage.resize((320,240),Image.Resampling.NEAREST).resize((640,480),Image.Resampling.NEAREST)
save('pb16_stage',stage,(320,240),'stage',(0,0,1448,1086),640/1448)
bank('props','pb16_wall',rects('props',4,80,300),(160,0),(192,112),largest=True)
bank('props','pb16_barrel',rects('props',4,301,660),(0,60),(96,112),largest=True)
bank('props','pb16_door',rects('props',4,660,1008),(0,130),(160,160),largest=True)
for prefix,y0,y1 in [('pb16_turret_gun',0,350),('pb16_turret_laser',365,690)]:
    bank('machinery',prefix,rects('machinery',4,y0,y1),(64,0),(96,96),center=True,largest=False)
bank('machinery','pb16_core',rects('machinery',4,700,1086),(140,0),(176,176),center=True)
hel=load('helios'); hh=hel.height/4
for row,action in enumerate(['run','throw','jump','lightning']):
    bank('helios','pb16_helios_'+action,rects('helios',4,round(row*hh),round((row+1)*hh)),(0,180),(256,256),scale=.58,baseline=232,fps=12,largest=action=='lightning')
bank('effects','pb16_orb',rects('effects',4,0,360),(32,0),(64,64),center=True)
bank('effects','pb16_geyser',rects('effects',4,638,1086),(0,130),(160,160))
bolt=load('bolts');bw,bh=bolt.size
bank('bolts','pb16_lightning',[(round(c*bw/2),round(r*bh/2),round((c+1)*bw/2),round((r+1)*bh/2)) for r in range(2) for c in range(2)],(140,0),(176,96),center=True)
wall=load('wallLow');ww,wh=wall.size
bank('wallLow','pb16_wall_low',[(round(c*ww/2),round(r*wh/2),round((c+1)*ww/2),round((r+1)*wh/2)) for r in range(2) for c in range(2)],(160,0),(192,80),largest=True)
shot=load('shots');sw,sh=shot.size
for name,row,start,target,cell in [('mg',0,0,12,(24,24)),('laser',0,2,14,(24,24)),('rocket',1,0,22,(36,36))]:
    rr=[(round((start+i)*sw/4),round(row*sh/2),round((start+i+1)*sw/4),round((row+1)*sh/2)) for i in range(2)]
    bank('shots','pb16_reticle' if name=='reticle' else 'pb16_projectile_'+name,rr,(target,0),cell,center=True)
reticle=load('reticle');rw,rh=reticle.size
bank('reticle','pb16_reticle',[(round(i*rw/2),0,round((i+1)*rw/2),round(rh/2)) for i in range(2)],(16,0),(24,24),center=True)

for p in SRC.glob('*.png'): D['sources'][p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(Image.open(p).size)}
(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_BASTION16_ENV_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
# Reviewer contact at actual gameplay resolution, all frames from all banks.
names=list(D['sequences']); montage=Image.new('RGB',(1024,len(names)*280),(16,26,37))
for row,name in enumerate(names):
    contact=Image.open(QA/(name+'_contact.png')).convert('RGB');montage.paste(contact,(0,row*280))
montage.save(QA/'all_frames.png')
print(json.dumps({'assets':len(D['assets']),'sequences':len(D['sequences']),'output':str(OUT),'review':str(QA),'wall':D['assets']['pb16_wall_0'],'core':D['assets']['pb16_core_0'],'helios':D['assets']['pb16_helios_run_0']}))
