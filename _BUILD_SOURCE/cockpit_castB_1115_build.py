from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import numpy as np,json,hashlib,shutil,sys,struct,zlib,math
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/cockpit_castB_1115';O=R/'_shots/cockpit_castB_1115';A=R/'assets/game/shared/cinematics/cockpit_castB_1115'
for p in [S,O,A,S/'identities',S/'frames']:p.mkdir(parents=True,exist_ok=True)
jobfile=S/'generations.json'
if not jobfile.exists():jobfile=S/'generations.json'
jobs=json.loads(jobfile.read_text(encoding='utf8'))
if not (S/'generations.json').exists():shutil.copyfile(jobfile,S/'generations.json')
oldjs=R/'assets/cockpit_talk_art_1114.js'
if not (S/'previous-cockpit-registry.js').exists():shutil.copyfile(oldjs,S/'previous-cockpit-registry.js')
if not (S/'previous-city-registry.js').exists():shutil.copyfile(R/'assets/city_rescue_art_1115.js',S/'previous-city-registry.js')
olddata=json.loads((S/'previous-cockpit-registry.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
TIMES=[83,83,84,83,83,84,83,84]
old=(R/'_BUILD_SOURCE/pursuit_trace_1115_build.py').read_text(encoding='utf8');defs=old[old.index('def string('):old.index("M={'version'")].replace('16,456,256','8,544,364').replace('0,15,0,0,bytes','0,7,0,0,bytes').replace('Traced frame rim','Registered neutral cockpit').replace('Selected green-white pulse','Generated mouth and eyelids').replace('selected-green-white','speech-shapes');exec(compile(defs,'aseprite-source-functions','exec'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def align(frame,base):
 a=np.asarray(frame).astype(np.int16);b=np.asarray(base).astype(np.int16);rect=(216,30,328,122);x0,y0,x1,y1=rect;target=b[y0:y1,x0:x1,:3];best=(1e9,0,0)
 for dy in range(-3,4):
  for dx in range(-3,4):
   score=float(np.abs(a[y0-dy:y1-dy,x0-dx:x1-dx,:3]-target).mean())
   if score<best[0]:best=(score,dx,dy)
 out=Image.new('RGBA',(544,364));out.alpha_composite(frame,(best[1],best[2]));return out,list(best[1:])
banks={};minis={};stats=[];previews=[];provenance=[]
for job in jobs['jobs']:
 p=job['pilot'];rawPath=S/job['source'];identity=S/'identities'/(('juggernaut'if p=='album'else p)+'.png')
 if not rawPath.exists():shutil.copyfile(Path(job['generationOutput']),rawPath)
 if not identity.exists():shutil.copyfile(R/job['identity'],identity)
 provenance.append({**job,'sourceSha256':h(rawPath),'identitySha256':h(identity)})
 if p=='album':continue
 raw=Image.open(rawPath).convert('RGBA');assert raw.size==(2172,724),(p,raw.size)
 # Rectangular fixed-cell equivalent of the shared sprite pipeline: all
 # original543x362 source pixels retained at1:1, right/bottom padding only.
 generated=[]
 for f in range(8):
  im=raw.crop((f%4*543,f//4*362,(f%4+1)*543,(f//4+1)*362));c=Image.new('RGBA',(544,364));c.alpha_composite(im);generated.append(c)
 base=generated[0];blink=p not in ['axel','maverick','juggernaut'];mouth=[239,126,306,171];eye=[226,75,318,116]
 layers=[];frames=[];offsets=[]
 for f,im in enumerate(generated):
  aligned,offset=align(im,base);offsets.append(offset);facial=Image.new('RGBA',(544,364))
  if f>0 and(f!=7 or blink):
   box=eye if f==7 else mouth;facial.paste(aligned.crop(box),(box[0],box[1]))
  out=Image.alpha_composite(base,facial);frames.append(out);layers.append((base,facial))
 ase=S/(p+'.aseprite');author='--author'in sys.argv or not ase.exists()
 if author:aseprite(ase,base,layers)
 decoded=decode_visible(ase)
 if author:assert all(a.tobytes()==b.tobytes()for a,b in zip(decoded,frames))
 frames=decoded;dest=A/p;dest.mkdir(exist_ok=True);fd=S/'frames'/p;fd.mkdir(exist_ok=True);sheet=Image.new('RGBA',(544*4,364*2))
 for f,im in enumerate(frames):
  im.save(fd/(str(f).zfill(2)+'.png'));sheet.alpha_composite(im,(f%4*544,f//4*364));allowed=Image.new('L',(544,364));ImageDraw.Draw(allowed).rectangle(eye if f==7 else mouth,fill=255);delta=np.asarray(ImageChops.difference(im,frames[0]));outside=np.asarray(allowed)==0;assert not np.any(delta[outside]),(p,f,'body drift')
 path=dest/'cockpit.webp';sheet.save(path,lossless=True,exact=True);check=Image.open(path).convert('RGBA');assert check.tobytes()==sheet.tobytes()
 bank={'key':'cp15_'+p,'path':str(path.relative_to(R)).replace('\\','/'),'w':544,'h':364,'cols':4,'frames':8,'blink':blink,'pivot':[272,182],'mouthROI':mouth,'eyeROI':eye,'sha256':h(path),'family':'castB-1115','identity':str(identity.relative_to(R)).replace('\\','/'),'identitySha256':h(identity),'source':str(ase.relative_to(R)).replace('\\','/'),'sourceGeneration':str(rawPath.relative_to(R)).replace('\\','/')}
 assert bank['sha256']!=olddata['banks'][p]['sha256'];banks[p]=bank
 for n in [48,64,84,96]:
  mini=Image.new('RGBA',(n,n*8))
  for f,im in enumerate(frames):mini.alpha_composite(im.crop((140,0,404,264)).resize((n,n),Image.Resampling.NEAREST),(0,f*n))
  path=dest/('radio-'+str(n)+'.webp');mini.save(path,lossless=True,exact=True);minis[p+'-'+str(n)]={'key':'cp15_'+p+'_'+str(n),'path':str(path.relative_to(R)).replace('\\','/'),'w':n,'h':n,'cols':1,'frames':8,'size':n,'baselines':[n]*8,'sha256':h(path),'family':'castB-1115'}
 unique=len({hashlib.sha256(im.tobytes()).hexdigest()for im in frames});assert unique>=6,(p,unique)
 stats.append({'pilot':p,'frames':8,'unique':unique,'sourceCell':[543,362],'cell':[544,364],'sourceScale':1,'padding':[0,0,1,2],'offsets':offsets,'bodyLocked':True,'mouthROI':mouth,'eyeROI':eye,'referenceSha256':h(identity),'pageSha256':bank['sha256'],'changedFromRejectedBank':True,'asepriteRoundtrip':True});previews.append((p,frames[1]))
data={'pilots':list(banks),'banks':banks,'minis':minis,'poses':['idle','A','E','O','U','FV','small','blink'],'family':'castB-1115','authority':'User confirmed row B front-facing cast; replaces rejected CP15 1114 appearances.','generator':'built-in image_gen','normalization':'Original543x362 cells padded to544x364; no upscale/downscale. Registered upper face; neutral body/cabin locked outside generated mouth/eye regions.'}
oldjs.write_text('"use strict";\nconst CP15_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
album=Image.open(S/'album.png').convert('RGBA');k=min(912/album.width,512/album.height);size=(round(album.width*k),round(album.height*k));im=album.resize(size,Image.Resampling.NEAREST);out=Image.new('RGBA',(912,512),(0,0,0,255));out.alpha_composite(im,((912-size[0])//2,(512-size[1])//2));path=A/'album.png';out.save(path)
city=json.loads((R/'assets/city_rescue_art_1115.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'));city['images']['album']={'key':'city16_album','path':str(path.relative_to(R)).replace('\\','/'),'w':912,'h':512,'sha256':h(path),'family':'castB-1115'}
(R/'assets/city_rescue_art_1115.js').write_text('"use strict";\nconst CITY16_ART='+json.dumps(city,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(R/'_ART_SOURCES/city_rescue_1115/manifest.json').write_text(json.dumps(city,indent=2),encoding='utf8',newline='\n')
data['album']=city['images']['album']
(S/'manifest.json').write_text(json.dumps(data,indent=2),encoding='utf8',newline='\n');(S/'generation-provenance.json').write_text(json.dumps({'authority':jobs['authority'],'generator':jobs['generator'],'jobs':provenance},indent=2),encoding='utf8',newline='\n');(O/'asset-qa.json').write_text(json.dumps({'stats':stats,'frames':72,'banks':45,'album':city['images']['album'],'sourceFormat':'Layered RGBA Aseprite format, independently decoded; editor GUI/CLI unavailable and not claimed.'},indent=2),encoding='utf8')
contact=Image.new('RGB',(1632,1146),'#10151d');d=ImageDraw.Draw(contact)
for i,(p,im)in enumerate(previews):x=i%3*544;y=i//3*382;contact.paste(im.convert('RGB'),(x,y));d.text((x+12,y+364),p.upper(),fill='white')
contact.save(O/'all-nine.png');out.save(O/'new-album.png');print(json.dumps({'pilots':len(banks),'cells':72,'family':data['family'],'geometry':[544,364],'album':list(album.size)},indent=2))
