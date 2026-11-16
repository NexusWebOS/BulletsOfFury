from pathlib import Path
from PIL import Image,ImageDraw
import struct,zlib,json,hashlib,math,io,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/pursuit_trace_1115';A=R/'assets/game/shared/ui/pursuit_trace_1115';O=R/'_shots/pursuit_trace_1115'
for d in [S,A,O]:d.mkdir(parents=True,exist_ok=True)
# Hand-traced source-image vertices. Even source positions map exactly onto the
# half-resolution native menu grid, following its chamfered individual frames.
PATHS={
 'hard-left':[[78,110],[410,110],[438,138],[438,374],[410,402],[78,402],[52,376],[52,138]],
 'hard-right':[[502,110],[836,110],[860,138],[860,378],[836,402],[502,402],[474,374],[474,138]],
 'furious-left':[[76,110],[410,110],[438,138],[438,374],[410,402],[76,402],[52,378],[52,138]],
 'furious-right':[[502,110],[836,110],[860,138],[860,378],[836,402],[502,402],[474,374],[474,138]]}
COLORS=[[48,147,81],[54,170,93],[64,198,113],[82,225,134],[112,246,163],[159,255,195],[210,255,228],[249,255,251],[235,255,244],[195,255,220],[146,248,187],[105,224,150],[77,199,121],[60,176,101],[48,155,87],[39,139,75]]
TIMES=[62,63]*8
def string(s):
 b=s.encode();return struct.pack('<H',len(b))+b
def chunk(kind,data):return struct.pack('<IH',len(data)+6,kind)+data
def layer(name,flags):return chunk(0x2004,struct.pack('<6HB3x',flags,0,0,0,0,0,255)+string(name))
def cel(index,im=None,linked=None):
 data=struct.pack('<HhhBHh5x',index,0,0,255,1 if linked is not None else 2,0)
 if linked is not None:data+=struct.pack('<H',linked)
 else:data+=struct.pack('<HH',*im.size)+zlib.compress(im.tobytes(),9)
 return chunk(0x2005,data)
def aseprite(path,reference,layers):
 frames=[]
 for f,(rim,core)in enumerate(layers):
  chunks=[]
  if f==0:
   chunks=[layer('Reference - hidden, locked',68),layer('Traced frame rim',3),layer('Selected green-white pulse',3)]
   chunks.append(chunk(0x2007,struct.pack('<HHI8x',1,0,0)))
   chunks.append(chunk(0x2018,struct.pack('<H8x',1)+struct.pack('<HHBH6x3sB',0,15,0,0,bytes([64,230,126]),0)+string('selected-green-white')))
  chunks +=[cel(0,reference)if f==0 else cel(0,linked=0),cel(1,rim),cel(2,core)]
  body=b''.join(chunks);frames.append(struct.pack('<IHHH2xI',16+len(body),0xF1FA,len(chunks),TIMES[f],0)+body)
 head=bytearray(128);struct.pack_into('<I5HIHII',head,0,128+sum(map(len,frames)),0xA5E0,16,456,256,32,1,62,0,0);head[34:36]=bytes([1,1]);struct.pack_into('<HH',head,40,16,16)
 path.write_bytes(bytes(head)+b''.join(frames))
def decode_visible(path):
 # Independent source reader: normal RGBA layers + compressed/linked cels.
 data=path.read_bytes();size,magic,count,w,h,depth=struct.unpack_from('<I5H',data);assert(size,magic,count,w,h,depth)==(len(data),0xA5E0,16,456,256,32)
 pos=128;visible=[];history=[];result=[];durations=[]
 for f in range(count):
  length,magic,chunks,duration=struct.unpack_from('<IHHH',data,pos);assert magic==0xF1FA;end=pos+length;pos+=16;cels={};durations.append(duration)
  for n in range(chunks):
   length,kind=struct.unpack_from('<IH',data,pos);payload=data[pos+6:pos+length]
   if kind==0x2004:visible.append(bool(struct.unpack_from('<H',payload)[0]&1))
   elif kind==0x2005:
    index,x,y,opacity,typ,z=struct.unpack_from('<HhhBHh',payload);assert(x,y,opacity,z)==(0,0,255,0)
    if typ==1:cels[index]=history[struct.unpack_from('<H',payload,16)[0]][index].copy()
    else:
     assert typ==2;ww,hh=struct.unpack_from('<HH',payload,16);raw=zlib.decompress(payload[20:]);cels[index]=Image.frombytes('RGBA',(ww,hh),raw)
   pos+=length
  assert pos==end;history.append(cels);out=Image.new('RGBA',(w,h))
  for index,vis in enumerate(visible):
   if vis and index in cels:out.alpha_composite(cels[index])
  result.append(out)
 assert pos==len(data)and durations==TIMES and visible==[False,True,True];return result
M={'version':1,'sourceCanvas':[456,256],'nativeMenu':[456,256],'sourceImageCanvas':[912,512],'frameMs':TIMES,'fps':16,'colors':COLORS,'pathsSourcePixels':PATHS,'banks':{},'sourceFormat':'layered RGBA .aseprite; hidden reference + rim + pulse; official ase-file-specs','editorAvailable':False}
sourceChecks=[]
for name,sourcePoints in PATHS.items():
 diff,side=name.split('-');path=R/('assets/game/shared/cinematics/city_rescue_1115/pursuit-'+diff+'.png');reference=Image.open(path).convert('RGBA').resize((456,256),Image.Resampling.NEAREST);points=[(x//2,y//2)for x,y in sourcePoints];reference.save(S/(diff+'-reference-native.png'))
 layers=[];frames=[]
 for f,c in enumerate(COLORS):
  rim=Image.new('RGBA',(456,256));core=Image.new('RGBA',(456,256));closed=points+[points[0]]
  ImageDraw.Draw(rim).line(closed,fill=tuple(round(v*.40)for v in c)+(255,),width=3,joint='curve')
  ImageDraw.Draw(core).line(closed,fill=tuple(c)+(255,),width=1,joint='curve');out=Image.alpha_composite(rim,core);layers.append((rim,core));frames.append(out)
 ase=S/(name+'.aseprite');author='--author'in sys.argv or not ase.exists()
 if author:aseprite(ase,reference,layers)
 decoded=decode_visible(ase)
 if author:assert all(a.tobytes()==b.tobytes()for a,b in zip(decoded,frames))
 frames=decoded;sourceChecks.append({'name':name,'frames':16,'visiblePixelsRoundtrip':True,'asepriteSha256':hashlib.sha256(ase.read_bytes()).hexdigest()})
 bounds=[p.getbbox()for p in frames];l=(min(b[0]for b in bounds)-4)//2*2;t=(min(b[1]for b in bounds)-4)//2*2;r=math.ceil((max(b[2]for b in bounds)+4)/2)*2;bottom=math.ceil((max(b[3]for b in bounds)+4)/2)*2;cw=r-l;ch=bottom-t
 sheet=Image.new('RGBA',(cw*8,ch*2))
 for f,im in enumerate(frames):sheet.alpha_composite(im.crop((l,t,r,bottom)),(f%8*cw,f//8*ch))
 out=A/(name+'.png');sheet.save(out);M['banks'][name]={'key':'city16_trace_'+name,'path':str(out.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'w':cw,'h':ch,'cols':8,'frames':16,'origin':[l,t],'sourceCanvas':[456,256],'crop':[l,t,r,bottom],'source':str(ase.relative_to(R)).replace('\\','/'),'sourceImageSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceVertices':sourcePoints}
 for f in [0,7]:
  proof=reference.copy();proof.alpha_composite(frames[f]);proof.resize((912,512),Image.Resampling.NEAREST).save(O/(name+'-phase'+str(f)+'.png'))
assert all(b['w']%2==b['h']%2==0 and b['w']*8<=4096 and b['h']*2<=4096 for b in M['banks'].values())
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n');(S/'paths.json').write_text(json.dumps(PATHS,indent=2),encoding='utf8');(R/'assets/pursuit_trace_art_1115.js').write_text('"use strict";\nconst CITY16_TRACE_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(O/'source-qa.json').write_text(json.dumps({'checks':sourceChecks,'scope':'All4 layered .aseprite sources decoded independently;64 visible RGBA frame composites match export. Aseprite executable not installed on this host; no GUI/CLI use claimed.','officialFormat':'https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md'},indent=2),encoding='utf8')
print(json.dumps({'banks':{k:[v['w'],v['h'],v['origin']]for k,v in M['banks'].items()},'frames':64,'layeredSourcesRoundtrip':True},indent=2))
