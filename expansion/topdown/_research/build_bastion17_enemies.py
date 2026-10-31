"""Own Level 7 authored elite, enemy cover poses and flying gun pickups.

Only isolate, scale proportionally and register original generated pixels.
Every bank keeps its body unit and even canvas. No synthetic inbetween drawings.
"""
from pathlib import Path
import json,hashlib,statistics
import numpy as np
from scipy.ndimage import label,find_objects
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion17_enemies';SRC=OUT/'source';FR=OUT/'frames';QA=ROOT/'_shots/bastion17_enemies'
FR.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
PREV=json.loads((ROOT/'expansion/topdown/art/bastion16_enemies/manifest.json').read_text())
D={'version':'1013-bastion17-enemies-r1','generator':'built-in image_gen','assets':{},'sequences':{},'audit':[],'sources':{},
   'contract':{'actorCell':[192,256],'actorAnchor':[96,224],'pickupCell':[96,96],'pickupAnchor':[48,48],
       'method':'connected authored figure extraction; shared per-bank proportional nearest scale, integer head root/ground registration; binary alpha128',
       'notes':'Ordinary crouch matches existing approved idle unit height. Original source pixels/prompts retained.'}}

def source(name,cols,rows):
    path=SRC/(name+'.png');sheet=Image.open(path).convert('RGBA');rgba=np.asarray(sheet)
    labs,count=label(rgba[:,:,3]>=128,np.ones((3,3),bool));objects=find_objects(labs);result={}
    for number,sl in enumerate(objects,1):
        yy,xx=np.where(labs[sl]==number)
        if len(xx)<400:continue
        col=min(cols-1,int((np.mean(xx)+sl[1].start)*cols/sheet.width));row=min(rows-1,int((np.mean(yy)+sl[0].start)*rows/sheet.height));idx=row*cols+col
        if idx not in result or len(xx)>result[idx]['pixels']:
            result[idx]={'id':number,'pixels':len(xx),'box':(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop),'col':col,'row':row}
    assert len(result)==cols*rows,(name,len(result),cols*rows)
    D['sources'][name]={'file':path.relative_to(ROOT).as_posix(),'size':sheet.size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'prompt':(SRC/(name+'_prompt.txt')).relative_to(ROOT).as_posix()}
    return {'name':name,'rgba':rgba,'labs':labs,'objects':result,'size':sheet.size,'cols':cols,'rows':rows}

def bank(src,prefix,indices,fps,scale,draw_scale,action,role=None):
    actor=action!='pickup';cell=(192,256) if actor else (96,96);anchor=(96,224) if actor else (48,48)
    keys=[];objects=src['objects'];h=src['size'][1];w=src['size'][0]
    base=statistics.median(objects[i]['box'][3]-round(objects[i]['row']*h/src['rows']) for i in range(min(16,len(objects))))
    for phase,index in enumerate(indices):
        ob=objects[index];b=ob['box'];px=src['rgba'][b[1]:b[3],b[0]:b[2]].copy()
        mask=src['labs'][b[1]:b[3],b[0]:b[2]]==ob['id'];px[:,:,3]=np.where(mask,255,0).astype(np.uint8);px[:,:,:3][~mask]=0
        cut=Image.fromarray(px,'RGBA')
        if actor:
            top=mask[:max(8,round(mask.shape[0]*.18))];_,xx=np.where(top);rx=b[0]+float(np.median(xx))
            ry=b[3]
            if action in ('death','vault'):
                ry=round(ob['row']*h/src['rows'])+base
                if action=='death':rx=(ob['col']+.5)*w/src['cols']
        else:rx=(b[0]+b[2])/2;ry=(b[1]+b[3])/2
        size=(round(cut.width*scale),round(cut.height*scale));offset=(round(anchor[0]+(b[0]-rx)*scale),round(anchor[1]+(b[1]-ry)*scale))
        assert min(offset)>0 and offset[0]+size[0]<cell[0] and offset[1]+size[1]<cell[1],(prefix,phase,offset,size)
        im=Image.new('RGBA',cell);im.alpha_composite(cut.resize(size,Image.Resampling.NEAREST),offset)
        key=f'{prefix}_{phase}';dest=FR/(key+'.png');im.save(dest,optimize=True);bounds=im.getchannel('A').getbbox()
        meta={'file':dest.relative_to(ROOT).as_posix(),'size':cell,'anchor':anchor,'bounds':bounds,'drawScale':draw_scale,'action':action,'phase':phase}
        if actor:
            meta['role']=role;meta['muzzle']=[anchor[0],round(offset[1]+cut.height*.4*scale)]
            meta['vaultLiftBaked']=action=='vault'
        D['assets'][key]=meta;keys.append(key)
        D['audit'].append({'key':key,'source':src['name']+'.png','sourceComponent':ob['id'],'sourceRect':b,'sourceRoot':[rx,ry],
            'sourceScale':scale,'offset':offset,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    D['sequences'][prefix]={'frames':keys,'fps':fps,'loop':action in ('idle','walk','fire','pickup'),'drawScale':draw_scale,
      'rootContract':{'cell':cell,'anchor':anchor,'commonSourceScale':scale}}
    contact=Image.new('RGBA',(cell[0]*len(keys),cell[1]),(24,31,43,255));onion=contact.copy()
    for i,key in enumerate(keys):
        im=Image.open(FR/(key+'.png'));contact.alpha_composite(im,(i*cell[0],0))
        for neighbor,opacity in (((i-1)%len(keys),65),((i+1)%len(keys),65),(i,210)):
            q=Image.open(FR/(keys[neighbor]+'.png'));q.putalpha(q.getchannel('A').point(lambda a:a*opacity//255));onion.alpha_composite(q,(i*cell[0],0))
        draw=ImageDraw.Draw(onion);draw.line((i*cell[0]+anchor[0],0,i*cell[0]+anchor[0],cell[1]),fill=(60,150,150,255));draw.line((i*cell[0],anchor[1],(i+1)*cell[0],anchor[1]),fill=(60,150,150,255))
    contact.convert('RGB').save(QA/(prefix+'_contact.png'));onion.convert('RGB').save(QA/(prefix+'_onion.png'))
    return keys

elite=source('elite',4,8)
eh=statistics.median(elite['objects'][i]['box'][3]-elite['objects'][i]['box'][1] for i in range(4))
es=.5;ed=125/(round(eh*es));start=0
for action,n,fps in [('idle',4,6),('walk',8,12),('fire',4,14),('crouch',4,12),('vault',6,10),('death',6,9)]:
    bank(elite,'pb17_elite_'+action,range(start,start+n),fps,es,ed,action,'elite');start+=n

# Targeted built-in image edit repaired a misplaced source muzzle flash.
# Preserve the edit's complete192x256 canvas using its uniform upscale ratio,
# then apply only an integer baseline nudge. Never stretch or fit its actor.
fix_path=SRC/'elite_firefix.png'
fix=Image.open(fix_path).convert('RGBA')
assert fix.width/192==fix.height/256
native=fix.resize((192,256),Image.Resampling.NEAREST)
native.putalpha(native.getchannel('A').point(lambda a:255 if a>=128 else 0))
bb=native.getchannel('A').getbbox();delta=224-bb[3]
fixed=Image.new('RGBA',(192,256));fixed.alpha_composite(native,(0,delta))
key='pb17_elite_fire_1';dest=FR/(key+'.png');fixed.save(dest,optimize=True)
D['assets'][key]['bounds']=fixed.getchannel('A').getbbox()
D['sources']['elite_firefix']={'file':fix_path.relative_to(ROOT).as_posix(),'size':fix.size,'sha256':hashlib.sha256(fix_path.read_bytes()).hexdigest(),
     'prompt':(SRC/'elite_firefix_prompt.txt').relative_to(ROOT).as_posix()}
D['audit'].append({'key':key,'source':'elite_firefix.png','sourceRect':[0,0,fix.width,fix.height],'sourceScale':192/fix.width,
     'offset':[0,delta],'reason':'builtin image edit moves flash onto actual forward barrel; baseline nudge only','sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
for i,muzzle in enumerate(((96,166),(96,168),(96,165),(96,165))):D['assets'][f'pb17_elite_fire_{i}']['muzzle']=muzzle
firekeys=D['sequences']['pb17_elite_fire']['frames'];contact=Image.new('RGBA',(768,256),(24,31,43,255));onion=contact.copy()
for i,k in enumerate(firekeys):
    contact.alpha_composite(Image.open(FR/(k+'.png')),(i*192,0))
    for n,a in (((i-1)%4,65),((i+1)%4,65),(i,210)):
        q=Image.open(FR/(firekeys[n]+'.png'));q.putalpha(q.getchannel('A').point(lambda v:v*a//255));onion.alpha_composite(q,(i*192,0))
    dr=ImageDraw.Draw(onion);dr.line((i*192+96,0,i*192+96,256),fill=(60,150,150,255));dr.line((i*192,224,(i+1)*192,224),fill=(60,150,150,255))
contact.convert('RGB').save(QA/'pb17_elite_fire_contact.png')
onion.convert('RGB').save(QA/'pb17_elite_fire_onion.png')

crouch=source('crouch',4,4)
for row,role in enumerate(('rifle','heavy','rocket','laser')):
    prev=PREV['assets']['pb16_'+role+'_idle_0'];b=crouch['objects'][row*4]['box'];height=b[3]-b[1]
    scale=(prev['bounds'][3]-prev['bounds'][1])/height
    bank(crouch,'pb17_'+role+'_crouch',range(row*4,row*4+4),12,scale,prev['drawScale'],'crouch',role)

pickup=source('pickup',4,3)
for row,weapon in enumerate(('shotgun','laser','minigun')):
    width=statistics.median(pickup['objects'][row*4+i]['box'][2]-pickup['objects'][row*4+i]['box'][0] for i in range(4))
    scale=.2;draw_scale=40/round(width*scale)
    bank(pickup,'pb17_pickup_'+weapon,range(row*4,row*4+4),8,scale,draw_scale,'pickup',weapon)

assert len(D['assets'])==60 and len(D['sequences'])==13
for key,m in D['assets'].items():
    im=Image.open(ROOT/m['file']);a=np.asarray(im)[:,:,3];b=im.getchannel('A').getbbox()
    assert all(n%2==0 for n in im.size)
    assert set(np.unique(a)).issubset({0,255})
    assert b[0]>0 and b[1]>0 and b[2]<im.width and b[3]<im.height
(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_BASTION17_ENEMY_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({'assets':len(D['assets']),'sequences':len(D['sequences']),'eliteDrawScale':ed,'sources':D['sources']}))
