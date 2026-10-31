"""Authored corridor layers for the wall-breach advance sequence.

ImageGen originals and prompts remain in source/. This builder only extracts,
normalizes alpha, applies one proportional nearest scale per bank, and pads to
even fixed canvases. Never synthesizes or paints background/sprite geometry.
"""
from pathlib import Path
import json,hashlib,statistics
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion17_environment'; SRC=OUT/'source'; FR=OUT/'frames'; QA=ROOT/'_shots/bastion17_environment'
for p in (FR,QA):p.mkdir(parents=True,exist_ok=True)
D={'version':'1013-bastion17-environment-r1','assets':{},'sequences':{},'audit':[],'sources':{},'layout':{'aperture':[170,78,300,192],'safeAperture':[184,98,272,156],'rearFloor':270,'troopDoor':[320,250]}}

def load(name):
 im=Image.open(SRC/(name+'.png')).convert('RGBA'); im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));return im

def save(key,im,anchor,src,rect,scale,extra=None):
 b=im.getchannel('A').getbbox();assert b,key
 assert all(v%2==0 for v in im.size),(key,im.size)
 if not key.startswith('pb17_stage'):assert min(b[0],b[1],im.width-b[2],im.height-b[3])>0,(key,b)
 f=FR/(key+'.png');im.save(f,optimize=True)
 D['assets'][key]={'file':f.relative_to(ROOT).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(b),'drawScale':1,**(extra or {})}
 D['audit'].append({'key':key,'source':src+'.png','crop':list(rect),'proportionalScale':scale,'pixelStep':2,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})

def grid(im,cols,rows):
 return [(round(c*im.width/cols),round(r*im.height/rows),round((c+1)*im.width/cols),round((r+1)*im.height/rows)) for r in range(rows) for c in range(cols)]

def bank(src,prefix,rects,cell,anchor,width=None,height=None,scale=None,center=False,fullwall=False):
 sheet=load(src);cuts=[sheet.crop(r) for r in rects];boxes=[q.getchannel('A').getbbox() for q in cuts]
 if scale is None:
  if width:scale=width/max(b[2]-b[0] for b in boxes)
  else:scale=height/max(b[3]-b[1] for b in boxes)
 keys=[]
 for i,(im,b,r) in enumerate(zip(cuts,boxes,rects)):
  cx=im.width/2 if fullwall else (b[0]+b[2])/2
  cy=(b[1]+b[3])/2 if center else b[3]
  root=(320,270) if fullwall else anchor
  part=im.crop(b);sm=(max(1,round(part.width*scale/2)),max(1,round(part.height*scale/2)))
  part=part.resize(sm,Image.Resampling.NEAREST).resize((sm[0]*2,sm[1]*2),Image.Resampling.NEAREST)
  pos=(round((root[0]+(b[0]-cx)*scale)/2)*2,round((root[1]+(b[1]-cy)*scale)/2)*2)
  im=Image.new('RGBA',cell);im.alpha_composite(part,pos)
  key=f'{prefix}_{i}';save(key,im,anchor,src,r,scale);keys.append(key)
 D['sequences'][prefix]={'frames':keys,'fps':12,'drawScale':1,'rootContract':{'cell':list(cell),'anchor':list(anchor),'scale':scale,'pixelStep':2,'root':'fixed wall-floor' if fullwall else 'fixed center' if center else 'bottom center'}}
 thumbscale=.5 if fullwall else 1
 contact=Image.new('RGBA',(round(cell[0]*thumbscale)*len(keys),round(cell[1]*thumbscale)+24),(16,26,37,255))
 for i,k in enumerate(keys):
  q=Image.open(FR/(k+'.png'));q=q.resize((round(q.width*thumbscale),round(q.height*thumbscale)),Image.Resampling.NEAREST);contact.alpha_composite(q,(round(cell[0]*thumbscale)*i,24));ImageDraw.Draw(contact).text((round(cell[0]*thumbscale)*i+3,3),k,fill='white')
 contact.convert('RGB').save(QA/(prefix+'_contact.png'))

for i,name in enumerate(['entry','coolant','reactor']):
 im=load(name);srcsize=im.size;im=im.resize((320,240),Image.Resampling.NEAREST).resize((640,480),Image.Resampling.NEAREST)
 save(f'pb17_stage_{i}',im,(320,240),name,(0,0,*srcsize),640/srcsize[0],{'aperture':D['layout']['aperture'],'biome':name})
D['sequences']['pb17_stage']={'frames':[f'pb17_stage_{i}' for i in range(3)],'fps':0,'drawScale':1}
im=load('backwall');rr=grid(im,2,3);b=im.crop(rr[0]).getchannel('A').getbbox()
bank('backwall','pb17_backwall',rr,(640,480),(320,240),scale=192/(b[3]-b[1]),fullwall=True)
D['layout']['wallFootprint']=D['assets']['pb17_backwall_0']['bounds']
im=load('cover');rr=grid(im,4,2)
bank('cover','pb17_enemy_cover_crate',rr[:4],(112,80),(56,68),width=80)
bank('cover','pb17_enemy_cover_wall',rr[4:],(112,80),(56,68),width=80)
im=load('blast');bank('blast','pb17_blast',grid(im,4,2),(384,256),(192,128),width=340,center=True)
for p in SRC.glob('*.png'):D['sources'][p.name]={'size':list(Image.open(p).size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_BASTION17_ENV_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
# Source-integrity review shows each separate wall state over each real stage.
contact=Image.new('RGB',(1920,1440),(16,26,37))
for room in range(3):
 for phase in range(6):
  q=Image.open(FR/f'pb17_stage_{room}.png').convert('RGBA');q.alpha_composite(Image.open(FR/f'pb17_backwall_{phase}.png'));q=q.resize((320,240),Image.Resampling.NEAREST);contact.paste(q,(phase*320,room*480))
contact.save(QA/'rooms_and_breach_contact.png')
print(json.dumps({'assets':len(D['assets']),'sequences':len(D['sequences']),'layout':D['layout'],'output':str(OUT)}))
