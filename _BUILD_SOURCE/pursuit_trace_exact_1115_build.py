from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,struct,zlib,json,hashlib,math,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/pursuit_trace_exact_1115';A=R/'assets/game/shared/ui/pursuit_trace_exact_1115';O=R/'_shots/pursuit_trace_exact_1115'
for d in [S,A,O]:d.mkdir(parents=True,exist_ok=True)
TIMES=[62,63]*8
COLORS=[[56,204,112],[60,220,122],[70,236,138],[88,247,155],[113,255,177],[159,255,202],[211,255,232],[249,255,251],[235,255,244],[195,255,222],[146,255,196],[106,246,166],[78,231,141],[63,220,125],[53,211,114],[45,198,104]]
# Retain the established layered RGBA source format, now at the exact2x UI
# backing resolution. This evaluates definitions only, not the older builder.
old=(R/'_BUILD_SOURCE/pursuit_trace_1115_build.py').read_text(encoding='utf8');defs=old[old.index('def string('):old.index("M={'version'")].replace('456,256','912,512').replace('Traced frame rim','Original frame material').replace('Selected green-white pulse','Original frame edge accents');exec(compile(defs,'aseprite-source-functions','exec'))
SEEDS=[(125,105),(190,112),(260,115),(390,110),(67,150),(67,220),(59,320),(80,392),(105,404),(190,404),(260,403),(320,404),(392,404),(435,380),(440,320),(436,240),(431,153)]
LANDMARKS=[('raised top',125,100,True),('top recess',190,100,False),('lower side offset',58,320,True),('upper side recess',58,230,False),('bottom tab',190,408,True),('bottom notch',250,408,False)]
def frame_mask(im,side):
 a=np.asarray(im);rr=a[:,:,0].astype(float);gg=a[:,:,1].astype(float);bb=a[:,:,2].astype(float);hi=np.maximum.reduce([rr,gg,bb]);lo=np.minimum.reduce([rr,gg,bb]);metal=(rr>=18)&(gg>=22)&(bb>=26)&(rr>=gg*.64)&(rr<=gg*1.25+8)&(bb<=rr*2.1+10)&(hi-lo<66)&((rr*.2126+gg*.7152+bb*.0722)>=35)
 x0,y0,x1,y1=(50,96,450,415)if side=='left'else(462,96,863,415);domain=np.zeros_like(metal);domain[y0:y1,x0:x1]=metal[y0:y1,x0:x1];labels=np.zeros(domain.shape,dtype=np.int32);H,W=domain.shape;flat=domain.ravel();lab=labels.ravel();label=0
 for start in np.flatnonzero(flat):
  if lab[start]:continue
  label+=1;stack=[int(start)];lab[start]=label
  while stack:
   k=stack.pop();y,x=divmod(k,W)
   for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
    xx=x+dx;yy=y+dy
    if 0<=xx<W and 0<=yy<H:
     at=yy*W+xx
     if flat[at]and not lab[at]:lab[at]=label;stack.append(at)
 chosen=set();picks=[]
 for sx,sy in SEEDS:
  if side=='right':sx=912-sx
  options=[]
  for y in range(max(y0,sy-5),min(y1,sy+6)):
   for x in range(max(x0,sx-5),min(x1,sx+6)):
    if labels[y,x]:options.append(((x-sx)**2+(y-sy)**2,int(labels[y,x]),x,y))
  assert options,(side,sx,sy)
  pick=min(options);chosen.add(pick[1]);picks.append({'guide':[sx,sy],'pixel':list(pick[2:]),'component':pick[1]})
 selected=np.isin(labels,list(chosen))
 # This protected interior removes any connected technical-grid flecks. It is
 # never rendered; the visible shape remains original metal pixels only.
 if side=='left':selected[124:392,80:420]=False
 else:selected[124:392,492:832]=False
 assert not np.any(selected&~metal)
 landmarks=[]
 for name,x,y,wanted in LANDMARKS:
  if side=='right':x=912-x
  value=bool(selected[y,x]);assert value==wanted,(side,name,value);landmarks.append({'name':name,'point':[x,y],'selected':value})
 return selected,picks,landmarks
M={'version':2,'sourceCanvas':[912,512],'nativeMenu':[456,256],'pixelDensity':2,'fps':16,'frameMs':TIMES,'authorColors':COLORS,'traceMethod':'Existing metal-frame pixels, connected components and source landmarks; no polygon stroke','banks':{}}
checks=[]
for diff in ['hard','furious']:
 sourcePath=R/('assets/game/shared/cinematics/city_rescue_1115/pursuit-'+diff+'.png');reference=Image.open(sourcePath).convert('RGBA');assert reference.size==(912,512);source=np.asarray(reference);reference.save(S/(diff+'-reference.png'))
 for side in ['left','right']:
  name=diff+'-'+side;selected,picks,landmarks=frame_mask(reference,side);mask=Image.fromarray((selected*255).astype(np.uint8));mask.save(S/(name+'-frame-mask.png'));eroded=np.asarray(mask.filter(ImageFilter.MinFilter(3)))>0;edge=selected&~eroded
  lum=source[:,:,:3].astype(float)@np.array([.2126,.7152,.0722]);layers=[];frames=[]
  for phase,color in enumerate(COLORS):
   tint=np.array(color)/255;body=np.zeros_like(source);hot=np.zeros_like(source);body[:,:,:3]=np.clip((lum[:,:,None]*1.10+35)*tint,0,255).astype(np.uint8);body[:,:,3]=selected*255;hot[:,:,:3]=np.clip((lum[:,:,None]*1.15+64)*tint,0,255).astype(np.uint8);hot[:,:,3]=edge*255;body[~selected]=0;hot[~edge]=0;rim=Image.fromarray(body);core=Image.fromarray(hot);frames.append(Image.alpha_composite(rim,core));layers.append((rim,core))
  ase=S/(name+'.aseprite');author='--author'in sys.argv or not ase.exists()
  if author:aseprite(ase,reference,layers)
  decoded=decode_visible(ase)
  if author:assert all(a.tobytes()==b.tobytes()for a,b in zip(decoded,frames))
  frames=decoded
  for im in frames:assert not np.any((np.asarray(im)[:,:,3]>0)&~selected)
  bounds=[im.getbbox()for im in frames];l=(min(q[0]for q in bounds)-4)//2*2;t=(min(q[1]for q in bounds)-4)//2*2;right=math.ceil((max(q[2]for q in bounds)+4)/2)*2;bottom=math.ceil((max(q[3]for q in bounds)+4)/2)*2;cw=right-l;ch=bottom-t;sheet=Image.new('RGBA',(cw*8,ch*2))
  for f,im in enumerate(frames):sheet.alpha_composite(im.crop((l,t,right,bottom)),(f%8*cw,f//8*ch))
  path=A/(name+'.png');sheet.save(path);assert cw%2==ch%2==l%2==t%2==0 and sheet.width<=4096 and sheet.height<=4096
  M['banks'][name]={'key':'city16_trace_'+name,'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'w':cw,'h':ch,'cols':8,'frames':16,'origin':[l,t],'density':2,'sourceCanvas':[912,512],'crop':[l,t,right,bottom],'source':str(ase.relative_to(R)).replace('\\','/'),'sourceImageSha256':hashlib.sha256(sourcePath.read_bytes()).hexdigest(),'mask':str((S/(name+'-frame-mask.png')).relative_to(R)).replace('\\','/'),'selectedOriginalPixels':int(selected.sum())}
  checks.append({'name':name,'frames':16,'allFramePixelsFromOriginalMetal':True,'noAircraftOrTitlePixelsSelected':True,'landmarks':landmarks,'sourceRoundtrip':True,'sourceSha256':hashlib.sha256(ase.read_bytes()).hexdigest(),'anchors':picks})
  for f in [0,7]:
   proof=reference.copy();proof.alpha_composite(frames[f]);proof.save(O/(name+'-phase'+str(f)+'.png'));x0,y0,x1,y1=(45,94,453,420)if side=='left'else(459,94,867,420);proof.crop((x0,y0,x1,y1)).save(O/(name+'-detail-phase'+str(f)+'.png'))
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n');(R/'assets/pursuit_trace_art_1115.js').write_text('"use strict";\nconst CITY16_TRACE_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(O/'source-qa.json').write_text(json.dumps({'checks':checks,'scope':'64 layered RGBA cels decoded independently; visible support taken from the original metal frame pixels. Six raised/notched landmarks verified on each card. No editor GUI/CLI claim.'},indent=2),encoding='utf8')
print(json.dumps({'frames':64,'banks':{n:[b['w'],b['h'],b['origin'],b['selectedOriginalPixels']]for n,b in M['banks'].items()},'sourceNotchLandmarks':24},indent=2))
