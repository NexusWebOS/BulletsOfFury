from pathlib import Path
from PIL import Image,ImageFilter
import json,math,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/biome_fleet_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-BiomeFleet-1022'
D=W/'shipping';D.mkdir(exist_ok=True)
models=json.loads((W/'models.json').read_text(encoding='utf-8'));fx=json.loads((W/'effects.json').read_text(encoding='utf-8-sig'))
catalog=json.loads((R/'assets/data/AIR_MOTION_1013.json').read_text(encoding='utf-8'))['entries']
native=json.loads((W/'native-roster.json').read_text(encoding='utf-8'))
art={'models':{},'effects':{},'sheets':{},'pending':[]};audit=[]
def emit(name,frames,cell,fps):
 assert frames and all(im.size==(cell,cell) for im in frames)
 columns=min(8,len(frames));sheet=Image.new('RGBA',(columns*cell,math.ceil(len(frames)/columns)*cell));cells=[]
 for i,im in enumerate(frames):
  x=i%columns*cell;y=i//columns*cell;sheet.alpha_composite(im,(x,y));cells.append([x,y,cell,cell])
 path=D/(name+'.webp');sheet.save(path,lossless=True,method=6);key='bf22_'+name
 entry={'key':key,'path':'assets/game/shared/enemies/biome_fleet_1022/'+path.name,'frames':len(frames),'columns':columns,'cell':cell,'w':cell,'h':cell,'cells':cells,'fps':fps,'pivot':[cell//2,cell//2]}
 if cell==128:entry['modules']=[[0,0,48,128],[48,0,32,128],[80,0,48,128]]
 art['sheets'][key]={'key':key,'path':entry['path'],'w':sheet.width,'h':sheet.height};return entry
for spec in models:
 name=spec['id'];root=W/'returned'/name;bankfiles={k:sorted((root/k).glob('*.png')) for k in ['idle','attack','drift','roll','somer']};expected={'idle':5,'attack':9,'drift':9,'roll':17,'somer':17}
 # PixelLab inverted the two Cinder action prompts; select by observed motion,
 # retaining every source cell and receipt rather than trusting the job label.
 if name=='magma_dart':bankfiles['roll'],bankfiles['somer']=bankfiles['somer'],bankfiles['roll']
 if any(len(bankfiles[k]) not in ({5} if k in ['idle','drift'] else {9} if k=='attack' else {9,17}) for k in expected):art['pending'].append({'id':name,'banks':{k:len(v) for k,v in bankfiles.items()}});continue
 master=Image.open(W/'references'/(name+'-selected.png')).convert('RGBA');box=master.getbbox();span=max(box[2]-box[0],box[3]-box[1])
 palette=master.convert('RGB').quantize(colors=96,method=Image.Quantize.MEDIANCUT)
 M={'_bf22':True,'id':name,'name':spec['name'],'stages':[spec['stage']],'size':spec['size'],'aliases':spec['aliases'],'span':span,'banks':{},'sourceKeys':{},'nativeRatios':{},'pivot':[64,64]}
 for alias in spec['aliases']:
  c=next((v for v in catalog.values() if alias in v.get('aliases',[])),{})
  M['sourceKeys'][alias]=c.get('sourceKeys',{}).get(alias)
  M['nativeRatios'][alias]=c.get('nativeRatios',{}).get(alias,1)
  if spec['stage']==2 and alias in native['volcanic']:
   a=native['volcanic'][alias];M['sourceKeys'][alias]='nvl_'+a['art']+'_0';M['nativeRatios'][alias]=1.9*a['h']/max(a['w'],a['h'])
  if alias.startswith('l6x_'):M['sourceKeys'][alias]='n6x_'+alias[4:]+'_idle_0';M['nativeRatios'][alias]=1.35
  if alias.startswith('l6v_'):M['nativeRatios'][alias]={'small':1.15,'medium':1.25,'large':1.35}[spec['size']]
 # Socket measurements are recorded separately after visual inspection.
 sockets=json.loads((W/'sockets.json').read_text(encoding='utf-8')) if (W/'sockets.json').exists() else {}
 M['sockets']=sockets.get(name,{'port':[42,96],'starboard':[86,96],'centre':[64,106]})
 for kind,files in bankfiles.items():
  frames=[]
  for i,p in enumerate(files):
   im=Image.open(p).convert('RGBA');assert im.size==(128,128),(name,kind,p,im.size)
   out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(im.getchannel('A'))
   if kind in ['idle','attack','drift']:
    mask=master.getchannel('A');mask=mask if kind=='idle' else mask.filter(ImageFilter.MaxFilter(3 if kind=='attack' else 9))
    out=Image.composite(out,Image.new('RGBA',im.size),mask)
   bb=out.getbbox();assert bb and min(bb[:2])>0 and max(bb[2:])<128,(name,kind,i,bb)
   rebuilt=Image.new('RGBA',out.size)
   for x,y,w,h in [[0,0,48,128],[48,0,32,128],[80,0,48,128]]:rebuilt.paste(out.crop((x,y,x+w,y+h)),(x,y))
   assert rebuilt.tobytes()==out.tobytes()
   frames.append(out);audit.append({'model':name,'bank':kind,'frame':i,'bounds':bb,'modulesExact':True})
  M['banks'][kind]=emit(name+'_'+kind,frames,128,{'idle':8,'attack':20,'drift':12,'roll':20,'somer':20}[kind])
 art['models'][name]=M
for spec in fx:
 name=spec['id'];files=sorted((W/'returned'/name/'effect_motion').glob('*.png'))
 if len(files)!=5:art['pending'].append({'id':name,'frames':len(files)});continue
 frames=[Image.open(p).convert('RGBA') for p in files]
 if spec['form']=='muzzle':
  mask=frames[0].getchannel('A').filter(ImageFilter.MaxFilter(5));frames=[Image.composite(im,Image.new('RGBA',im.size),mask) for im in frames]
 entry=emit(name,frames,64,20)
 boxes=[im.getbbox() for im in frames if im.getbbox()];entry['ink']=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
 entry.update({'theme':spec['theme'],'form':spec['form'],'stages':[spec['stage']]});art['effects'][name]=entry
(W/'biome_fleet_art_1022.js').write_text('"use strict";\n// Owned by build_biome_fleet_1022.py; fixed cells, pivots, sockets and exact part unions.\nconst BF22_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(W/'frame-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
exports=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.glob('*.webp'))]
(W/'export-audit.json').write_text(json.dumps(exports,indent=2),encoding='utf-8')
print(json.dumps({'models':list(art['models']),'effects':list(art['effects']),'pending':art['pending'],'cells':len(audit),'bytes':sum(x['bytes'] for x in exports)}))
if '--install' in sys.argv:
 assert not art['pending'],'Do not activate incomplete animation banks or effect sets.'
 T=R/'assets/game/shared/enemies/biome_fleet_1022';T.mkdir(parents=True,exist_ok=True)
 for p in D.glob('*.webp'):shutil.copy2(p,T/p.name)
 for name in ['biome_fleet_art_1022.js','biome_fleet_1022.js']:shutil.copy2(W/name,R/'assets'/name)
 index=R/'index.html';data=index.read_bytes();tag=b'<script src="assets/biome_fleet_art_1022.js?v=biome-fleet-1022-1"></script>\n<script src="assets/biome_fleet_1022.js?v=biome-fleet-1022-1"></script>\n'
 if b'biome_fleet_1022.js' not in data:index.write_bytes(data.replace(b'</body>',tag+b'</body>'))
 print('Installed complete biome roster and effects only.')
