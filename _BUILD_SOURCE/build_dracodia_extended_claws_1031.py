"""RD88: source-preserving shoulder/elbow/wrist articulation, baked offline.
The user explicitly requested generated modular poses OR authored rotations.
No new design, runtime transforms, AI API, credits or reference-video pixels.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,math,json,hashlib,subprocess
W=Path(__file__).parent;R=W.parent if W.name=='_BUILD_SOURCE'else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
installed=W.name=='_BUILD_SOURCE';O=R/'assets/game/levels/stage_08/boss/extended_claws_1031' if installed else W/'art';O.mkdir(parents=True,exist_ok=True)
REL='assets/game/levels/stage_08/boss/extended_claws_1031/'
C,H=768,640;P=np.array([384.,320.]);U=410/320;OFF=P-160*U
def data(name):
 s=(R/'assets'/name).read_text(encoding='utf-8-sig');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
V=data('stage8_identity_art_1018.js')['clips']['colossus_scythe']['frames'];src={};images={}
for id in ['left','core','right']:
 p=R/V[0]['layers'][id]['path'];images[id]=Image.open(p).convert('RGBA');src[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
def ease(u):return max(0,min(1,u))**2*(3-2*max(0,min(1,u)))
def mix(a,b,u):return np.array(a)*(1-u)+np.array(b)*u
def angle(v):return math.atan2(v[1],v[0])
def unit(a):return np.array([math.cos(a),math.sin(a)])
def pos(v):return OFF+np.array(v)*U
def blank():return Image.new('RGBA',(C,H))
def spans(im):
 a=np.array(im.getchannel('A'))>48
 return [np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1)))).tolist()for row in a]
def moved(im,srcpoint,dstpoint,degrees):
 big=blank();big.paste(im.resize((410,410),Image.Resampling.NEAREST),tuple(np.round(OFF).astype(int)))
 a=pos(srcpoint);b=pos(dstpoint);rot=big.rotate(degrees,Image.Resampling.NEAREST,center=tuple(a));out=blank();out.paste(rot,tuple(np.round(b-a).astype(int)));return out
def connected(im):
 a=np.array(im);mask=a[:,:,3]>32;seen=np.zeros(mask.shape,bool);groups=[]
 for y,x in zip(*np.where(mask)):
  if seen[y,x]:continue
  todo=[(y,x)];seen[y,x]=True;group=[]
  while todo:
   yy,xx=todo.pop();group.append((yy,xx))
   for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
    ny,nx=yy+dy,xx+dx
    if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and mask[ny,nx]and not seen[ny,nx]:seen[ny,nx]=True;todo.append((ny,nx))
  groups.append(group)
 keep=np.zeros(mask.shape,bool)
 for group in sorted(groups,key=len,reverse=True)[:1]:
  for y,x in group:keep[y,x]=True
 a[~keep]=0;return Image.fromarray(a)
def cut(im,lo,hi):
 out=Image.new('RGBA',im.size);out.paste(im.crop((0,lo,320,hi)),(0,lo));return connected(out)
# Fixed pauldrons keep their attachment to the chest. Three connected segments
# use actual source armor, tendons and blade pixels at their original unit.
S=np.array([106.,134.]);E=np.array([78.,169.]);WR=np.array([70.,198.]);TIP=np.array([88.,268.]);L1=np.linalg.norm(E-S);L2=np.linalg.norm(WR-E);L3=np.linalg.norm(TIP-WR)
pieces={id:[cut(images[id],0,140),cut(images[id],140,173),cut(images[id],173,200),cut(images[id],200,320)]for id in ['left','right']}
def arm(id,target,rest=0):
 mirror=id=='right';im=images[id];pts=[S,E,WR,TIP];T=np.array(target,dtype=float)
 if mirror:pts=[np.array([320-p[0],p[1]])for p in pts];T=np.array([320-T[0],T[1]])
 s,e,w,tip=pts;v=T-s;d=np.linalg.norm(v);T=s+v*min(1,(L1+L2+L3)*.96/max(.001,d));a=angle(T-s)
 # Choose a slightly hooked blade angle, then solve the actual elbow chain.
 phi=a+(-.08 if mirror else .08);w2=T-unit(phi)*L3;v=w2-s;dist=np.linalg.norm(v)
 if dist>L1+L2-.5:w2=s+v*(L1+L2-.5)/dist;dist=L1+L2-.5;T=w2+unit(phi)*L3
 dist=max(abs(L1-L2)+.5,dist);c=max(-1,min(1,(L1*L1+dist*dist-L2*L2)/(2*L1*dist)));theta=angle(w2-s)+(1 if mirror else -1)*math.acos(c);e2=s+unit(theta)*L1;theta2=angle(w2-e2)
 def restore(a,z):return z+math.atan2(math.sin(a-z),math.cos(a-z))*(1-rest)
 theta=restore(theta,angle(e-s));theta2=restore(theta2,angle(w-e));phi=restore(phi,angle(tip-w));e2=s+unit(theta)*L1;w2=e2+unit(theta2)*L2;T=w2+unit(phi)*L3
 shoulder,upper,fore,blade=pieces[id]
 out=blank();out.alpha_composite(moved(upper,s,s,math.degrees(angle(e-s)-theta)));out.alpha_composite(moved(fore,e,e2,math.degrees(angle(w-e)-theta2)))
 claw=moved(blade,w,w2,math.degrees(angle(tip-w)-phi));out.alpha_composite(claw)
 # Source elbow/wrist collar pixels bridge the disjoint articulation cuts.
 for at,to,deg,radius in [(e,e2,math.degrees(angle(w-e)-theta2),12),(w,w2,math.degrees(angle(tip-w)-phi),10)]:
  cap=Image.new('RGBA',im.size);box=(int(at[0]-radius),int(at[1]-radius),int(at[0]+radius),int(at[1]+radius));crop=im.crop(box);mask=Image.new('L',crop.size);ImageDraw.Draw(mask).ellipse((0,0,crop.width-1,crop.height-1),fill=255);aa=np.minimum(np.array(crop.getchannel('A')),np.array(mask));crop.putalpha(Image.fromarray(aa));cap.paste(crop,box[:2]);out.alpha_composite(moved(cap,at,to,deg))
 out.alpha_composite(moved(shoulder,s,s,0));return out,claw,{'shoulder':pos(s).tolist(),'elbow':pos(e2).tolist(),'wrist':pos(w2).tolist(),'tip':pos(T).tolist()}
def finish(im,bank,depth):
 out=im.rotate(bank,Image.Resampling.NEAREST,center=tuple(P))if bank else im
 if depth!=1:
  small=out.resize((round(C*depth),round(H*depth)),Image.Resampling.NEAREST);out=blank();out.paste(small,((C-small.width)//2,(H-small.height)//2))
 return out
def transform_point(q,bank,depth):
 a=math.radians(bank);v=np.array(q)-P;return(P+np.array([math.cos(a)*v[0]+math.sin(a)*v[1],-math.sin(a)*v[0]+math.cos(a)*v[1]])*depth).tolist()
art={'logicalCell':[C,H],'pivot':P.tolist(),'unit':410,'banks':{},'pages':{},'warnings':{},'source':src,'joints':{'left':[S.tolist(),E.tolist(),WR.tolist(),TIP.tolist()]}};poses=[];warn={}
counts={'sideL':44,'sideR':44,'coil':20,'recede':20,'approach':20,'jumpL':36,'jumpR':36,'settle':16}
for name,count in counts.items():
 art['banks'][name]=[];warn[name]=Image.new('L',(C,H))
 for f in range(count):
  u=f/(count-1);e=ease(u);depth=1;tilt=0;active=None;rest=0;targets={'left':(135,195),'right':(135,195)}
  if name.startswith('side'):
   active='left'if name=='sideL'else'right';side=-1 if active=='left'else 1
   if f<16:target=mix((135,195),(-20,220),ease(f/15));tilt=side*7*ease(f/15)
   elif f<32:
    v=(f-16)/15;target=(1-v)**2*np.array([-20,220])+2*(1-v)*v*np.array([30,306])+v*v*np.array([184,273]);tilt=side*(7-15*ease(v))
   else:target=mix((184,273),(135,195),ease((f-32)/11));tilt=-side*8*(1-ease((f-32)/11))
   targets[active]=target;targets['right'if active=='left'else'left']=(135,195)
  elif name in ['coil','recede','approach']:
   fold=e if name!='approach'else 1-e
   if name=='recede':fold=1;depth=1-.64*e
   if name=='approach':depth=.36+.64*e
   targets={id:(135,195)for id in targets};rest=1-e if name=='coil'else 0;tilt=-5*math.sin(u*math.pi)if name=='coil'else 0
  elif name.startswith('jump'):
   active='left'if name=='jumpL'else'right';side=-1 if active=='left'else 1
   if f<12:target=mix((135,195),(40,140),ease(f/11));tilt=side*10*ease(f/11)
   elif f<28:
    v=(f-12)/15;target=mix((40,140),(184,273),ease(v));tilt=side*(10-24*ease(v))
   else:target=mix((184,273),(135,195),ease((f-28)/7));tilt=-side*14*(1-ease((f-28)/7))
   targets[active]=target;targets['right'if active=='left'else'left']=(135,195)
  else:targets={id:(135,195)for id in targets};rest=e
  layers={};claws={};joints={}
  for id in ['left','right']:
   layers[id],claws[id],joints[id]=arm(id,targets[id],rest);layers[id]=finish(layers[id],tilt,depth);claws[id]=finish(claws[id],tilt,depth);joints[id]={k:transform_point(q,tilt,depth)for k,q in joints[id].items()}
  core=moved(images['core'],[160,160],[160,160],0);layers['core']=finish(core,tilt,depth)
  q={'depth':depth,'parts':{},'claws':{},'joints':joints};art['banks'][name].append(q);poses.append((name,f,layers,claws))
  if active and((name.startswith('side')and 16<=f<32)or(name.startswith('jump')and 12<=f<28)):
   warn[name]=Image.fromarray(np.maximum(np.array(warn[name]),np.array(claws[active].getchannel('A'))))
  for id in ['left','core','right']:
   b=layers[id].getbbox();assert b and min(b[:2])>2 and b[2]<C-2 and b[3]<H-2,(name,f,id,b)
page=Image.new('RGBA',(2048,2048));hit=page.copy();px=py=rh=pi=0
def flush():
 global page,hit,px,py,rh,pi
 key='rd88_page_'+str(pi);page.save(O/(key+'.png'));hit.save(O/(key+'_hit.png'));art['pages'][key]={'path':REL+key+'.png','hitKey':key+'_hit','hitPath':REL+key+'_hit.png'};pi+=1;page=Image.new('RGBA',(2048,2048));hit=page.copy();px=py=rh=0
def pack(im):
 global px,py,rh
 bb=im.getbbox();x0,y0=bb[0]//2*2,bb[1]//2*2;x1,y1=(bb[2]+1)//2*2,(bb[3]+1)//2*2;crop=im.crop((x0,y0,x1,y1));w,h=crop.size
 if px+w+2>2048:px=0;py+=rh+2;rh=0
 if py+h+2>2048:flush()
 page.paste(crop,(px,py));a=np.array(crop);white=a.copy();white[:,:,:3]=255;hit.paste(Image.fromarray(white),(px,py));mask=a[:,:,3]>48;yy,xx=np.where(mask)
 nearest=int(np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2))
 out={'key':'rd88_page_'+str(pi),'rect':[px,py,w,h],'offset':[x0-int(P[0]),y0-int(P[1])],'w':w,'h':h,'spans':spans(crop),'target':[int(xx[nearest]+x0-P[0]),int(yy[nearest]+y0-P[1])],'rupture':[[int(xx[i]+x0-P[0]),int(yy[i]+y0-P[1])]for i in np.linspace(0,len(xx)-1,5).astype(int)]}
 px+=w+2;rh=max(rh,h);return out
for name,f,layers,claws in poses:
 for id,im in layers.items():art['banks'][name][f]['parts'][id]=pack(im)
 for id,im in claws.items():
  bb=im.getbbox();x0,y0=bb[:2];art['banks'][name][f]['claws'][id]={'offset':[x0-int(P[0]),y0-int(P[1])],'w':bb[2]-x0,'h':bb[3]-y0,'spans':spans(im.crop(bb))}
flush()
# Source-alpha sweep footprints, three baked warning palette states.
for name in ['sideL','sideR','jumpL','jumpR']:
 mask=warn[name].filter(ImageFilter.MaxFilter(9));arr=np.array(mask)>48;outer=np.array(mask.filter(ImageFilter.MaxFilter(3)))>48;edge=outer&~arr;bb=mask.getbbox();states=[]
 for colour in [(84,230,73),(255,215,45),(255,65,59)]:
  a=np.zeros((H,C,4),dtype=np.uint8);a[arr]=[*colour,44];a[edge]=[*colour,160];im=Image.fromarray(a);path='warning_'+name+'_'+str(len(states))+'.png';im.save(O/path);states.append({'key':'rd88_'+path[:-4],'path':REL+path,'w':C,'h':H,'pivot':P.tolist()})
 art['warnings'][name]=states
(O/'manifest.json').write_text(json.dumps(art,separators=(',',':')))
(O/'dracodia_extended_art_1031.js').write_text("'use strict';\nconst RD88_ART="+json.dumps(art,separators=(',',':'))+';\n')
# Actual layered Aseprite animation source with pose tags and stable chest slice.
SOUR=O/'source';SOUR.mkdir(exist_ok=True);jobs=[]
for name,f,layers,claws in poses:
 paths={}
 for id in ['left','core','right']:
  path=SOUR/(name+'_'+str(f)+'_'+id+'.png');layers[id].save(path);paths[id]=str(path)
 duration=.5/counts[name]if name=='coil'else .65/counts[name]if name=='recede'else .38/counts[name]if name=='approach'else .85/counts[name]if name=='settle'else(.95/16 if f<16 else .3/16 if f<32 else .32/12)if name.startswith('side')else((.55 if name=='jumpL'else .62)/12 if f<12 else .28/16 if f<28 else .16/8)
 jobs.append({'bank':name,'paths':paths,'duration':duration})
(SOUR/'jobs.json').write_text(json.dumps(jobs));lua='''local J=json.decode(io.open(app.params.jobs):read('*a'))
local s=Sprite(768,640,ColorMode.RGB);s.layers[1].name='left';local mid=s:newLayer();mid.name='core';local right=s:newLayer();right.name='right';local layers={left=s.layers[1],core=mid,right=right};local first=1;local bank=J[1].bank
for i,q in ipairs(J) do if i>1 then s:newEmptyFrame() end;s.frames[i].duration=q.duration;for id,path in pairs(q.paths) do s:newCel(layers[id],i,Image{fromFile=path},Point(0,0)) end
 if q.bank~=bank then local tag=s:newTag(first,i-1);tag.name=bank;first=i;bank=q.bank end end
local tag=s:newTag(first,#J);tag.name=bank;local root=s:newSlice(Rectangle(384,320,1,1));root.name='chest-root';s:saveAs(app.params.out)
''';(SOUR/'author.lua').write_text(lua)
subprocess.run([r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe','--batch','--script-param','jobs='+str(SOUR/'jobs.json'),'--script-param','out='+str(O/'extended-claws.aseprite'),'--script',str(SOUR/'author.lua')],check=True)
sheet=Image.new('RGBA',(768*4,640*4),(12,19,29,255));draw=ImageDraw.Draw(sheet)
for row,name in enumerate(['sideL','sideR','coil','jumpL']):
 for col,f in enumerate([0,15 if name.startswith('side')else 10,24 if name.startswith('side')else 16,31 if name.startswith('side')else counts[name]-1]):
  q=next(x for x in poses if x[0]==name and x[1]==f);im=blank()
  for id in ['left','core','right']:im.alpha_composite(q[2][id])
  sheet.alpha_composite(im,(col*C,row*H));draw.text((col*C+16,row*H+16),name+' '+str(f),fill='white')
sheet.convert('RGB').resize((1536,1280)).save(W/'pose-review.jpg',quality=94)
print(json.dumps({'poses':len(poses),'pages':pi,'parts':len(poses)*3,'source':str(O/'extended-claws.aseprite')}))
