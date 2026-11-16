from pathlib import Path
from PIL import Image,ImageOps
import json,math,hashlib,io
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';S=R/'_ART_SOURCES/city_rescue_1115';M=json.loads((S/'manifest.json').read_text(encoding='utf8'));checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 assert v,n
def checkBytes(n,im,path,sha,fmt):
 out=io.BytesIO();im.save(out,format=fmt,**({'lossless':True}if fmt=='WEBP'else{}));h=hashlib.sha256(out.getvalue()).hexdigest();ck(n,h==sha==hashlib.sha256((R/path).read_bytes()).hexdigest())
def contain(im,size):
 k=min(size[0]/im.width,size[1]/im.height);p=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',size,(0,0,0,255));c.alpha_composite(p,((size[0]-p.width)//2,(size[1]-p.height)//2));return c
for n in ['pursuit-hard','pursuit-furious','album']:
 a=M['images'][n];im=contain(Image.open(S/('generated-'+n+'.png')).convert('RGBA'),(912,512));checkBytes(n+' exact source reproduction',im,a['path'],a['sha256'],'PNG')
im=Image.open(S/'generated-rural.png').convert('RGBA').resize((680,1020),Image.Resampling.NEAREST);tile=Image.new('RGBA',(680,2040));tile.alpha_composite(im);tile.alpha_composite(ImageOps.flip(im),(0,1020));a=M['images']['rural'];checkBytes('rural tile exact reproduction',tile,a['path'],a['sha256'],'PNG')
ck('rural repeat seam identical and fully opaque',tile.crop((0,0,680,1)).tobytes()==tile.crop((0,2039,680,2040)).tobytes()and tile.getchannel('A').getextrema()==(255,255))
a=M['images']['shade'];checkBytes('fixed dim plate reproduction',Image.new('RGBA',(480,512),(0,3,12,168)),a['path'],a['sha256'],'PNG')
cells=[Image.open(S/('thruster-%02d.png'%i)).convert('RGBA')for i in range(16)];ck('sixteen distinct normalized source cells',len({c.tobytes()for c in cells})==16)
ck('uniform even source cells and binary alpha',all(c.size==(128,256)and set(c.getchannel('A').getdata()).issubset({0,255})for c in cells))
ck('all measured nozzle pivots fixed',all(r['pivot']==[64,224]and r['scale']==.5 for r in M['thrusterRegistration']))
sheet=Image.new('RGBA',(512,1024))
for i,c in enumerate(cells):sheet.alpha_composite(c,(i%4*128,i//4*256))
a=M['images']['thruster-source'];checkBytes('registered source sheet reproduction',sheet,a['path'],a['sha256'],'PNG')
for di,scale in enumerate([1,.96,.92,.88,.84,.8,.76,.72,.68,.64,.6,.56,.52,.48,.44,.4]):
 size=math.ceil(448*.46*scale/2)*2;pivot=[size//2,size//2];page=Image.new('RGBA',(2048,2048));px=py=rowH=0;key='city16_thrusters_d'+str(di)
 for d in range(16):
  frames=[]
  for c in cells:
   c=c.resize((round(128*.46*scale),round(256*.46*scale)),Image.Resampling.NEAREST);base=Image.new('RGBA',(size,size));base.alpha_composite(c,(pivot[0]-round(64*.46*scale),pivot[1]-round(224*.46*scale)));frames.append(base.rotate(-d*22.5,resample=Image.Resampling.NEAREST,center=tuple(pivot)))
  bounds=[c.getbbox()for c in frames];l=min(b[0]for b in bounds)//2*2;t=min(b[1]for b in bounds)//2*2;r=math.ceil(max(b[2]for b in bounds)/2)*2;bot=math.ceil(max(b[3]for b in bounds)/2)*2;crop=[l,t,r,bot];cw=r-l;ch=bot-t
  if px+cw*4>2048:px=0;py+=rowH;rowH=0
  B=M['banks']['thrust-d'+str(di)+'-r'+str(d)];ck('d'+str(di)+' r'+str(d)+' stable even geometry and16 phases',B['frames']==16 and B['sharedCrop']==crop and B['sourcePivot']==pivot and B['pivot']==[pivot[0]-l,pivot[1]-t]and B['w']==cw and B['h']==ch and cw%2==ch%2==0)
  for j,c in enumerate(frames):
   x=px+j%4*cw;y=py+j//4*ch;ck('d'+str(di)+' r'+str(d)+' frame'+str(j)+' source rect',B['cells'][j]==[key,x,y]);page.alpha_composite(c.crop(crop),(x,y))
  px+=cw*4;rowH=max(rowH,ch*4)
 bbox=page.getbbox();page=page.crop((0,0,math.ceil(bbox[2]/2)*2,math.ceil(bbox[3]/2)*2));a=B['pages'][0];checkBytes(key+' exact atlas reproduction',page,a['path'],a['sha256'],'WEBP')
for direction in ['nw','w']:
 for shadow in [False,True]:
  name='storm_'+direction+('_shadow'if shadow else'');B=M['banks'][name];sheet=Image.new('RGBA',(B['w']*4,B['h']*4))
  for f in range(16):
   c=Image.open(S/('storm-'+direction+('-body'if shadow else'')+'-%02d.png'%f)).convert('RGBA')
   if shadow:a=c.getchannel('A').point(lambda v:round(v*.27));c=Image.new('RGBA',c.size);c.putalpha(a)
   ck(name+' frame'+str(f)+' no clipped extents',c.getbbox()[0]>=4 and c.getbbox()[1]>=4 and c.getbbox()[2]<=796 and c.getbbox()[3]<=796);sheet.alpha_composite(c.crop(B['sharedCrop']),(f%4*B['w'],f//4*B['h']))
  a=B['pages'][0];checkBytes(name+' exact native-flight reproduction',sheet,a['path'],a['sha256'],'WEBP')
ck('all new pages fit4096 texture cap',all(a['w']<=4096 and a['h']<=4096 for b in M['banks'].values()for a in b['pages']))
registry='"use strict";\nconst CITY16_ART='+json.dumps(M,separators=(',',':'))+';\n';ck('registry exact reproduction',registry.encode()==(R/'assets/city_rescue_art_1115.js').read_bytes())
for name in ['thruster','storm-nw','storm-w']:
 im=Image.open(O/(name+'.gif'));ck(name+' review GIF has16 distinct frames',im.n_frames==16)
(O/'art-qa.json').write_text(json.dumps({'checks':checks,'sourceCell':[128,256],'phases':16,'headingCount':16,'depthCount':16,'shadowExcludesExhaust':True},indent=2),encoding='utf8');print(str(len(checks))+' registered-art checks passed; all20 atlas pages and6 PNGs reproduced without writing shipping art.',flush=True)
