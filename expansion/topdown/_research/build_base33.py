"""Base33 authored environment exporter. Crop/pad/nearest only; no painted art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
R=Path(__file__).resolve().parents[3]
A=R/'expansion/topdown/art/base33';S=A/'source';F=A/'frames';F.mkdir(parents=True,exist_ok=True)
assets={};sequences={};audit=[]
def src(n):return Image.open(S/(n+'.png')).convert('RGBA')
def put(name,im,anchor,**meta):
 im=im.convert('RGBA');assert im.width%2==0 and im.height%2==0
 p=F/(name+'.png');im.save(p);b=im.getbbox();assert b
 assets[name]={'file':p.relative_to(R).as_posix(),'size':list(im.size),'anchor':anchor,'bounds':list(b),'bodyWidth':b[2]-b[0],'bodyHeight':b[3]-b[1],'drawScale':1,**meta};audit.append({'key':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
def crop(n,rect,scale,cell=None,anchor=None,root=None):
 im=src(n).crop(rect);w=max(1,round(im.width*scale));h=max(1,round(im.height*scale));im=im.resize((w,h),Image.Resampling.NEAREST)
 if not cell:cell=(w+(w%2),h+(h%2))
 out=Image.new('RGBA',cell)
 if root and anchor:pos=(round(anchor[0]-root[0]*scale),round(anchor[1]-root[1]*scale))
 else:pos=((cell[0]-w)//2,(cell[1]-h)//2)
 out.alpha_composite(im,pos);return out
for i in range(4):
 x=i%2*627;y=i//2*627;rect=[x,y,x+627,y+627];put('b33_wall_'+str(i),crop('wall',rect,256/627),[0,0],source='wall',sourceRect=rect)
# Generated strips use observed row boundaries, not guessed uniform grid cuts.
rows=[0,358,634,938,1254]
names=['floor_a','floor_b','ceiling_a','ceiling_b','chute_a','chute_b','pipes','service']
for i,n in enumerate(names):
 x=i%2*627;rect=[x,rows[i//2],x+627,rows[i//2+1]];put('b33_'+n,crop('strips',rect,256/627),[0,0],source='strips',sourceRect=rect)
props=[('crate',[0,0,310,318]),('stack',[318,0,625,318]),('barrier',[635,0,984,318]),('barrel',[990,0,1254,318]),('pillar',[0,318,280,638]),('slide_pipe',[280,318,644,638]),('crawl_duct',[644,318,984,638]),('door',[984,318,1254,638]),('vent_closed',[0,638,320,938]),('vent_damaged',[320,638,640,938]),('vent_open',[640,638,980,938]),('door_open',[980,638,1254,938]),('drone_hatch',[0,938,340,1254]),('siren',[340,938,625,1254]),('locker',[625,938,928,1254]),('barrier_broken',[928,938,1254,1254])]
for n,rect in props:
 im=src('props').crop(rect);b=im.getbbox();root=[(b[0]+b[2])/2,b[3]]
 # All vent damage states share the same 320x300 source unit and root.
 if n.startswith('vent_'):root=[160,286]
 canvas=(128,128);anchor=[64,120];scale=.25
 source='props'
 if n in ['slide_pipe','crawl_duct']:
  source='pipe_v2' if n=='slide_pipe' else 'duct_v2';raw=src(source);bb=raw.getchannel('A').point(lambda a:255 if a>127 else 0).getbbox();rect=[bb[0]-4,bb[1]-4,bb[2]+4,bb[3]+4];root=[(bb[2]-bb[0])/2+4,bb[3]-bb[1]+4];scale=(90 if n=='slide_pipe' else 83)/(bb[2]-bb[0])
 out=crop(source,rect,scale,canvas,anchor,root);put('b33_'+n,out,anchor,source=source,sourceRect=rect,sourceRoot=root,scale=scale)
for i in range(4):
 x=i%2*627;y=i//2*627;rect=[x,y,x+627,y+627];im=src('recess').crop(rect);b=im.getbbox();root=[(b[0]+b[2])/2,b[3]];out=crop('recess',rect,.35,(224,224),[112,212],root)
 put('b33_recess_'+str(i),out,[112,212],source='recess',sourceRect=rect,sourceRoot=root,scale=.35)
 # The actual opaque near piers are separate render layers; never fake cover with player alpha.
 bb=out.getbbox();cuts=[bb[0],bb[0]+44,bb[2]-44,bb[2]]
 for side,l,r in [('left',cuts[0],cuts[1]),('right',cuts[2],cuts[3])]:
  layer=Image.new('RGBA',out.size);layer.alpha_composite(out.crop((l,0,r,out.height)),(l,0));put(f'b33_recess_{i}_{side}',layer,[112,212],sourceKey='b33_recess_'+str(i),crop=[l,0,r,out.height])
fxrows=[0,314,604,928,1254];cols=[0,314,628,942,1254]
for j,bank in enumerate(['impact','ventburst','steam','blast']):
 keys=[]
 for i in range(4):
  rect=[cols[i],fxrows[j],cols[i+1],fxrows[j+1]];root=[157,290 if bank=='steam'else(160 if bank=='blast'else 147)];anchor=[48,88 if bank=='steam'else 48]
  out=crop('fx',rect,.25,(96,96),anchor,root);k=f'b33_{bank}_{i}';put(k,out,anchor,source='fx',sourceRect=rect,sourceRoot=root,scale=.25);keys.append(k)
 sequences['b33_'+bank]={'frames':keys,'fps':12 if bank!='steam'else 8,'loop':False}
icons=['slide','crawl','cover','vent','right','down','ammo','danger','secret','bullets','alarm','exit','grenade','shield','explosion','vault']
# Measured cell centers preserve the icon frame rather than clipping the generated outer trim.
cx=[174,477,779,1082];cy=[184,474,760,1044]
for i,n in enumerate(icons):
 rect=[cx[i%4]-150,cy[i//4]-145,cx[i%4]+150,cy[i//4]+145];out=crop('icons',rect,.16,(48,48));put('b33_icon_'+n,out,[24,24],source='icons',sourceRect=rect,scale=.16)
pack={'build':'overdrive1015-base33-r1','assets':assets,'sequences':sequences,'audit':audit,'source':'Six image_gen sheets; measured source rectangles, proportional nearest-neighbor exports; no character/enemy regeneration.'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
(A/'manifest.js').write_text('window.TD_BASE33_ART='+json.dumps(pack,separators=(',',':'))+';Object.assign(window.TD_ESCAPE29_ART.assets,TD_BASE33_ART.assets);Object.assign(window.TD_ESCAPE29_ART.sequences,TD_BASE33_ART.sequences);\n',encoding='utf-8')
O=R/'_shots/base33';O.mkdir(parents=True,exist_ok=True)
for group,keys in [('props',[k for k in assets if k.startswith('b33_') and assets[k].get('source')=='props']),('icons',[k for k in assets if '_icon_'in k]),('effects',[k for k in assets if assets[k].get('source')=='fx'])]:
 out=Image.new('RGB',(768,768),'#24313b');d=ImageDraw.Draw(out)
 for i,k in enumerate(keys):
  im=Image.open(R/assets[k]['file']);sc=1 if group=='props'else 2;im=im.resize((im.width*sc,im.height*sc),Image.Resampling.NEAREST);x=i%4*192;y=i//4*192;out.paste(im,(x+(192-im.width)//2,y),im);d.text((x+5,y+174),k,fill='white')
 out.save(O/('contact_'+group+'.png'))
print(json.dumps({'assets':len(assets),'effects':len(sequences),'files':str(F)}))

