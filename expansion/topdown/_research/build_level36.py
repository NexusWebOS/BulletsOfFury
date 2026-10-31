"""Export generated Base36 materials as registered, independent game assets."""
from pathlib import Path
from PIL import Image
import json, shutil, hashlib
R=Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
D=R/'expansion/topdown/art/level36';D.mkdir(parents=True,exist_ok=True);(D/'source').mkdir(exist_ok=True)
I=Path('C:/Users/Mike/.codex/generated_images/01a0f036-546a-7e23-9f3a-463bc4985c5c')
P={'build':'overdrive1016-base36-r1','assets':{},'sequences':{},'sources':[]}
def source(name):
 p=D/'source'/name
 if not p.exists():shutil.copy2(I/name,p)
 P['sources'].append({'file':'source/'+name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'Built-in ImageGen; crop, shared proportional nearest-neighbor export, transparent padding only'})
 return Image.open(p).convert('RGBA')
def save(k,im,anchor,**meta):
 assert im.width%2==0 and im.height%2==0
 im.save(D/(k+'.png'));P['assets'][k]={'file':(D/(k+'.png')).relative_to(R).as_posix(),'size':list(im.size),'anchor':anchor,'bounds':list(im.getbbox()),**meta}
def plate(k,im,rect,scale=.5,cell=(256,256),anchor=(128,240),**meta):
 a=im.crop(rect);a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.NEAREST)
 # Register the physical opaque material, not faint exported shadow/alpha dust.
 # All source alpha is retained; only canvas placement and collision width use this bound.
 b=a.getchannel('A').point(lambda v:255 if v>=96 else 0).getbbox()
 out=Image.new('RGBA',cell);out.alpha_composite(a,(anchor[0]-(b[0]+b[2])//2,anchor[1]-b[3]));save(k,out,list(anchor),bodyWidth=b[2]-b[0],sourceCell=list(rect),sourceScale=scale,**meta)
props=source('exec-1b6959ef-64c2-4305-80ff-44e273f63fda.png');ys=[0,380,610,953,1254]
for row,name in enumerate(['column','lowwall','relay','chest']):
 for col in range(4):plate(f'l36_{name}_{col}',props,(round(col*props.width/4),ys[row],round((col+1)*props.width/4),ys[row+1]),damageState=col)
env=source('exec-c2b3be90-7486-4235-9978-3bb6b8e8a341.png')
for name,x0,x1 in [('outer_h',0,370),('outer_v',370,620),('outer_down',620,940),('outer_up',940,1254)]:plate('l36_'+name,env,(x0,0,x1,365))
for name,y0,y1 in [('field',375,600),('door',615,895)]:
 for col in range(4):plate(f'l36_{name}_{col}',env,(round(col*env.width/4),y0,round((col+1)*env.width/4),y1))
 P['sequences']['l36_'+name]={'frames':[f'l36_{name}_{c}' for c in range(4)],'fps':10 if name=='field' else 6,'loop':name=='field'}
for name,x0,x1 in [('machine',370,635),('barrel',665,925),('crate',940,1254)]:plate('l36_'+name,env,(x0,915,x1,1254))
floor=source('exec-6707f216-5c83-4062-aa08-149da37e2dbf.png').resize((256,256),Image.Resampling.NEAREST);save('l36_floor',floor,[0,0])
ground=Image.new('RGBA',(800,2800))
for y in range(0,2800,256):
 for x in range(0,800,256):ground.alpha_composite(floor,(x,y))
save('l36_ground',ground,[0,0])
source('exec-4119dfa0-15fc-42c7-b9c1-8343fdbbe999.png')
arena=source('exec-ca8d97ee-ab48-446a-98f8-556afc27837f.png');plate('l36_arena',arena,(0,0,*arena.size),.4,(512,512),(256,506))
(D/'manifest.json').write_text(json.dumps(P,indent=2)+'\n',encoding='utf-8')
(D/'manifest.js').write_text('window.TD_LEVEL36_ART='+json.dumps(P,separators=(',',':'))+';Object.assign(TD_ASSAULT_ART.assets,TD_LEVEL36_ART.assets);Object.assign(TD_ASSAULT_ART.sequences,TD_LEVEL36_ART.sequences);\n',encoding='utf-8')
print(json.dumps({'assets':len(P['assets']),'sources':len(P['sources'])}))
