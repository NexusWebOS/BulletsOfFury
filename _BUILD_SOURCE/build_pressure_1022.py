from pathlib import Path
from PIL import Image,ImageFilter
import json,math,hashlib,shutil,sys,colorsys
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/pressure_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Pressure-1022'
D=W/'shipping';D.mkdir(exist_ok=True);art={'models':{},'effects':{},'herald':{},'sheets':{},'pending':[]};audit=[]
def emit(name,frames,fps):
 assert frames and all(im.size==frames[0].size for im in frames)
 w,h=frames[0].size;columns=min(8,len(frames));sheet=Image.new('RGBA',(columns*w,math.ceil(len(frames)/columns)*h));cells=[]
 for i,im in enumerate(frames):
  x=i%columns*w;y=i//columns*h;sheet.alpha_composite(im,(x,y));cells.append([x,y,w,h]);bb=im.getbbox();assert bb,(name,i)
  assert bb[0]>0 and bb[1]>0 and bb[2]<w and bb[3]<h,(name,i,bb)
  audit.append({'name':name,'frame':i,'bounds':bb,'canvas':[w,h]})
 p=D/(name+'.webp');sheet.save(p,lossless=True,method=6);key='cp22_'+name
 B={'key':key,'path':'assets/game/shared/enemies/pressure_1022/'+p.name,'frames':len(frames),'columns':columns,'cell':w,'w':w,'h':h,'cells':cells,'fps':fps,'pivot':[w//2,h//2]}
 art['sheets'][key]={'key':key,'path':B['path'],'w':sheet.width,'h':sheet.height};return B
for spec in json.loads((W/'models.json').read_text(encoding='utf-8')):
 name=spec['id'];root=W/'returned'/name;files={k:sorted((root/k).glob('*.png')) for k in ['idle','attack','drift','roll','somer']}
 if any(len(files[k]) not in ([5] if k in ['idle','drift'] else [9]) for k in files):art['pending'].append({'id':name,'banks':{k:len(v) for k,v in files.items()}});continue
 # The unarmed Dasher's generated recoil incorrectly pitched the entire hull.
 # Its attack uses the approved rigid accelerator pulse, with a separate turbo
 # wake. The rejected source is retained for review, never silently substituted.
 if name=='dasher':files['attack']=files['idle']
 master=Image.open(W/'references'/(name+'-selected.png')).convert('RGBA');box=master.getbbox();span=max(box[2]-box[0],box[3]-box[1]);palette=master.convert('RGB').quantize(colors=96)
 alias={'dasher':'cp22dasher','slimejet':'cp22slime','sewerdrone':'cp22drone','sewerheavy':'cp22relay'}[name]
 M={'_bf22':True,'id':name,'name':spec['name'],'stages':[spec['stage']],'size':spec['size'],'aliases':[alias],'span':span,'banks':{},'sourceKeys':{},'nativeRatios':{alias:1.45},'pivot':[64,64],
 'sockets':{'slimejet':{'port':[40,103],'starboard':[88,103],'centre':[64,105]},'sewerdrone':{'port':[30,91],'starboard':[98,91],'centre':[64,107]},'sewerheavy':{'port':[29,109],'starboard':[99,109],'centre':[64,109]},'dasher':{'port':[44,95],'starboard':[84,95],'centre':[64,110]}}[name]}
 for kind,paths in files.items():
  frames=[]
  for p in paths:
   im=Image.open(p).convert('RGBA');assert im.size==(128,128)
   out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(im.getchannel('A'))
   if kind=='idle':out=Image.composite(out,Image.new('RGBA',im.size),master.getchannel('A').filter(ImageFilter.MaxFilter(3)))
   elif kind=='attack':out=Image.composite(out,Image.new('RGBA',im.size),master.getchannel('A').filter(ImageFilter.MaxFilter(7)))
   frames.append(out)
  B=emit(name+'_'+kind,frames,{'idle':8,'attack':20,'drift':12,'roll':18,'somer':18}[kind]);B['modules']=[[0,0,48,128],[48,0,32,128],[80,0,48,128]]
  for im in frames:
   rebuilt=Image.new('RGBA',im.size)
   for x,y,w,h in B['modules']:rebuilt.paste(im.crop((x,y,x+w,y+h)),(x,y))
   assert rebuilt.tobytes()==im.tobytes()
  M['banks'][kind]=B
 art['models'][name]=M
norm=json.loads((W/'herald-normalization.json').read_text(encoding='utf-8'))
for part in ['wingL','wingR','head']:
 paths=sorted((W/'returned'/('herald_'+part)/'motion').glob('*.png'))
 if len(paths)!=9:art['pending'].append({'part':part,'frames':len(paths)});continue
 frames=[Image.open(p).convert('RGBA') for p in paths];B=emit('herald_'+part,frames,12);B['pivot']=norm[part]['pivot'];B['sourceScale']=norm[part]['scale'];art['herald'][part]=B
for name,stage in [('toxic_orb',7),('toxic_muzzle',7),('dasher_turbo',6),('soul_feather',8)]:
 paths=sorted((W/'returned'/name/'effect_motion').glob('*.png'))
 if len(paths)!=5:art['pending'].append({'effect':name,'frames':len(paths)});continue
 frames=[Image.open(p).convert('RGBA') for p in paths]
 if name=='toxic_muzzle':
  mask=frames[0].getchannel('A').filter(ImageFilter.MaxFilter(7));frames=[Image.composite(im,Image.new('RGBA',im.size),mask) for im in frames]
 B=emit(name,frames,20);boxes=[im.getbbox() for im in frames if im.getbbox()];B['ink']=[min(x[0] for x in boxes),min(x[1] for x in boxes),max(x[2] for x in boxes),max(x[3] for x in boxes)];B['stages']=[stage];art['effects'][name]=B
# Reuse approved PixelLab water needle/wave motion with a lime hue; alpha and
# original luminance remain exact. These are derivatives, not additional bills.
for form in ['needle','wave']:
 source=R/'assets/game/shared/enemies/biome_fleet_1022'/('water_'+form+'.webp')
 if not source.exists():art['pending'].append({'derived':str(source)});continue
 sheet=Image.open(source).convert('RGBA');frames=[]
 for i in range(5):
  im=sheet.crop((i*64,0,(i+1)*64,64));pixels=[]
  for red,green,blue,a in im.getdata():
   h,s,v=colorsys.rgb_to_hsv(red/255,green/255,blue/255);r,g,b=colorsys.hsv_to_rgb(.23,s,v);pixels.append((round(r*255),round(g*255),round(b*255),a))
  im.putdata(pixels);frames.append(im)
 B=emit('toxic_'+form,frames,20);boxes=[im.getbbox() for im in frames];B['ink']=[min(x[0] for x in boxes),min(x[1] for x in boxes),max(x[2] for x in boxes),max(x[3] for x in boxes)];B['stages']=[7];B['derivedFrom']=str(source.relative_to(R));art['effects']['toxic_'+form]=B
(W/'pressure_art_1022.js').write_text('"use strict";\n// Owned by build_pressure_1022.py. Fixed cells, pivots and launcher sockets.\nconst CP22_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(W/'frame-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');exports=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.glob('*.webp'))];(W/'export-audit.json').write_text(json.dumps(exports,indent=2),encoding='utf-8')
print(json.dumps({'models':list(art['models']),'effects':list(art['effects']),'herald':list(art['herald']),'pending':art['pending'],'cells':len(audit),'bytes':sum(x['bytes'] for x in exports)}))
if '--install' in sys.argv:
 assert not art['pending'],'Incomplete banks cannot activate.'
 T=R/'assets/game/shared/enemies/pressure_1022';T.mkdir(parents=True,exist_ok=True)
 for p in D.glob('*.webp'):shutil.copy2(p,T/p.name)
 names=['pressure_art_1022.js','air_pressure_1022.js','sewer_pressure_1022.js','herald_predator_1022.js']
 for name in names:shutil.copy2(W/name,R/'assets'/name)
 index=R/'index.html';data=index.read_bytes();tag=''.join('<script src="assets/'+name+'?v=pressure-1022-1"></script>\n' for name in names).encode()
 if b'pressure_art_1022.js' not in data:index.write_bytes(data.replace(b'</body>',tag+b'</body>'))
 print('Installed complete pressure art and stage-scoped combat owners.')
