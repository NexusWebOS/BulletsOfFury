"""Source-preserving directional FX and twin-barrel turret bank.
FRAME FORMAT: fixed even cells, fixed emitter pivots, common proportional scale.
Existing animated exhaust/muzzles and turret pixels only. Directions are baked
offline; the revised renderer never rotates a static hull/projectile/FX canvas.
"""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'assets/game/levels/stage_01/enemies/amplify_1031';O.mkdir(parents=True,exist_ok=True);Q=R/'_shots/stage1_amplify_1031';Q.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(file,name):s=(R/file).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s.split('const '+name+'=',1)[1])[0]
S=data('assets/stage1_motion_art_1009.js','S1M_ART');A={}
def bank(name,frames,cell,pivot,source_pivot,scale,dirs,provenance):
 cols=dirs;rows=len(frames);sheet=Image.new('RGBA',(cell*cols,cell*rows))
 for f,im in enumerate(frames):
  big=Image.new('RGBA',(cell*3,cell*3));size=(round(im.width*scale),round(im.height*scale));src=im.resize(size,Image.Resampling.NEAREST);pos=(round(cell*1.5-source_pivot[0]*scale),round(cell*1.5-source_pivot[1]*scale));big.alpha_composite(src,pos)
  for d in range(dirs):
   angle=d*360/dirs;rot=big.rotate(-angle,Image.Resampling.NEAREST,center=(cell*1.5,cell*1.5));crop=rot.crop((cell,cell,cell*2,cell*2));sheet.alpha_composite(crop,(d*cell,f*cell))
 p=O/(name+'.png');sheet.save(p,optimize=True);A[name]=dict(key='s1a_'+name,path=p.relative_to(R).as_posix(),cell=cell,pivot=pivot,dirs=dirs,frames=len(frames),cols=cols,sourcePivot=source_pivot,unitScale=scale,sources=provenance,sha256=digest(p))
def reels(name,src,selection,scale,pivot,cell=64,dirs=32):
 f=[S[src][i]for i in selection];bank(name,[Image.open(R/a['path']).convert('RGBA')for a in f],cell,[cell//2,cell//2],pivot,scale,dirs,[dict(path=a['path'],sha256=digest(R/a['path']))for a in f])
reels('thruster','exhaust',range(8),.055,[128,600])
reels('muzzle','muzzle',range(4),.07,[128,24])
reels('rocket_muzzle','muzzle',range(4,8),.07,[128,24])
reels('tank_turret','turret',[3],.5,[192,192],192,64)
index=json.loads((R/'assets/game/shared/asset_index.json').read_text(encoding='utf-8'));idx={a['key']:a for a in index['assets']if isinstance(a,dict)and'key'in a}
def cell(key):
 a=idx[key];im=Image.open(R/a['path']).convert('RGBA');_,x,y,w,h,*_=a['cell'];return im.crop((x,y,x+w,y+h)),dict(path=a['path'],rect=[x,y,w,h],key=key,sha256=digest(R/a['path']))
f=[];meta=[]
for i in range(4):
 im,m=cell('mgcf_1_'+str(i+2));f.append(im);meta.append(m)
bank('slug',f,64,[32,32],[8,10],1,32,meta)
im,m=cell('lz_bomb');m['orientation']='nose south; source turned180 offline';im=im.transpose(Image.Transpose.ROTATE_180)
# Crimson/silver ordnance replaces the player-like gold bomb. Preserve alpha,
# dark outlines, neutral metal and the original luminance ordering.
for y in range(im.height):
 for x in range(im.width):
  r,g,b,a=im.getpixel((x,y))
  if a and r>g*1.12 and g>b*1.25:
   v=max(r,g,b);im.putpixel((x,y),(v,round(v*.23),round(v*.20),a))
m['palette']='crimson/silver; source neutral metal and alpha retained';bank('bomb',[im],64,[32,32],[im.width/2,im.height/2],.22,1,[m])
m=json.loads((R/'assets/game/levels/stage_01/stage/stage1_combat_fx.json').read_text());src=R/m['atlas'];atlas=Image.open(src).convert('RGBA');f=[];refs=[]
for i in range(6):
 rect=m['rects']['s1fx_jungle_missile_'+str(i)];x,y,w,h=rect;f.append(atlas.crop((x,y,x+w,y+h)));refs.append(dict(path=m['atlas'],rect=rect,sha256=digest(src)))
bank('missile',f,64,[32,32],[96,96],.25,32,refs)
for model,name in [('s1jetdelta','delta_heading'),('s1jetdelta_b','strike_heading')]:
 refit=data('assets/air_refit_art_1021.js','AF21_ART')['models'][model];f=[];refs=[];tails=[]
 for family,frame in [('idle',0),('drift',3),('drift',11)]:
  a=refit['banks'][family];path=R/a['path'];im=Image.open(path).convert('RGBA');x,y,w,h=a['cells'][frame];tile=im.crop((x,y,x+w,y+h));points=[];removed=[]
  # The current plate contains two frozen blue flames. Split only those small
  # exhaust rectangles off the hull; the animated source reel replaces them.
  for side in [-1,1]:
   blue=[]
   for yy in range(8,46):
    for xx in range(40 if side<0 else 64,64 if side<0 else 88):
     r,g,b,alpha=tile.getpixel((xx,yy))
     if alpha>80 and b>120 and b>r*1.45 and b>g*1.05:blue.append((xx,yy))
   assert blue,(family,frame,side)
   bottom=max(v for u,v in blue);mouth=[u for u,v in blue if v>=bottom-1];points.append([sum(mouth)/len(mouth),bottom+1])
   rect=[min(u for u,v in blue)-1,min(v for u,v in blue)-1,max(u for u,v in blue)+2,bottom+1];tile.paste((0,0,0,0),rect);removed.append(rect)
  f.append(tile);tails.append(points);refs.append(dict(path=a['path'],rect=[x,y,w,h],sha256=digest(path),pose=family,frame=frame,staticExhaustRemoved=removed))
 bank(name,f,128,[64,64],[64,64],1,32,refs)
 A[name]['tailSockets']=tails;A[name]['gunSockets']=[refit['sockets']['port'],refit['sockets']['starboard']]
(O/'manifest.json').write_text(json.dumps(dict(owner='_BUILD_SOURCE/build_stage1_amplify_1031.py',banks=A),indent=2)+'\n',encoding='utf-8')
(R/'assets/stage1_amplify_art_1031.js').write_text('"use strict";\nconst S1A_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
out=Image.new('RGB',(1024,len(A)*150),(7,20,28));d=ImageDraw.Draw(out)
for row,(n,a)in enumerate(A.items()):
 d.text((5,row*150+5),n,fill='white');im=Image.open(R/a['path'])
 for i in range(min(a['dirs'],8)):
  c=a['cell'];f=min(a['frames']-1,1);tile=im.crop((i*c,f*c,(i+1)*c,(f+1)*c));tile.thumbnail((110,115),Image.Resampling.NEAREST);out.paste(tile,(i*128+5,row*150+25),tile)
out.save(Q/'new-banks.png');print('Built',len(A),'banks',sum(a['frames']*a['dirs']for a in A.values()),'fixed directional frames')

