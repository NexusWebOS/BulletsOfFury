from pathlib import Path
from PIL import Image
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
OUT=ROOT/'expansion/topdown/art/grid21'
for p in [OUT/'source',OUT/'frames']:p.mkdir(parents=True,exist_ok=True)
candidate=Path(r'C:\Users\Mike\Documents\New project\.tooling\grid21_sources_final.json')
inputs=json.loads((candidate if candidate.is_file() else OUT/'source/prompts.json').read_text(encoding='utf-8'))
assets={};seq={};sources={}
def hard(im):
 im=im.convert('RGBA');a=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 rgb=im.convert('RGB').quantize(colors=48,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(a);return rgb
def save(k,im,anchor,extra=None):
 assert im.width%2==0 and im.height%2==0
 im.save(OUT/'frames'/f'{k}.png');assets[k]={'file':f'expansion/topdown/art/grid21/frames/{k}.png','size':list(im.size),'anchor':anchor,'bounds':list(im.getchannel('A').getbbox()),'drawScale':1,**(extra or {})}
def load(name):
 q=inputs[name];p=OUT/'source'/f'{name}.png';source=Path(q['file']);source=source if source.is_absolute() else OUT/source
 if source.resolve()!=p.resolve():shutil.copy2(source,p)
 sources[name]={'file':f'source/{name}.png','prompt':q['prompt'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};return Image.open(p).convert('RGBA')
for name in ['wall','floor','ceiling','rearwall']:
 im=load(name);n=256 if name in ['wall','rearwall'] else 128;im=hard(im.resize((n,n),Image.Resampling.NEAREST));save('grid21_'+name,im,[n//2,n//2],{'tile':True})
def bank(name,cols,rows,target,canvas,anchor,center=False):
 im=load(name);cw=im.width/cols;ch=im.height/rows;cells=[];rects=[]
 for i in range(cols*rows):
  rect=(round(i%cols*cw),round(i//cols*ch),round((i%cols+1)*cw),round((i//cols+1)*ch));cell=im.crop(rect);cell.putalpha(cell.getchannel('A').point(lambda v:255 if v>=128 else 0));bbox=cell.getchannel('A').getbbox();assert bbox;cells.append(cell.crop(bbox));rects.append({'cell':list(rect),'alphaBounds':list(bbox)})
 ref=cells[0];sc=min(target[0]/ref.width,target[1]/ref.height);sources[name]['export']={'canvas':list(canvas),'anchor':list(anchor),'uniformScale':sc,'nativeTarget':list(target),'sourceCells':rects,'alphaThreshold':128,'resample':'nearest','paletteColors':48,'dither':False}
 frames=[]
 for i,cell in enumerate(cells):
  cell=hard(cell.resize((max(1,round(cell.width*sc)),max(1,round(cell.height*sc))),Image.Resampling.NEAREST));cv=Image.new('RGBA',canvas);x=anchor[0]-cell.width//2;y=anchor[1]-cell.height//2 if center else anchor[1]-cell.height
  assert x>=0 and y>=0 and x+cell.width<=cv.width and y+cell.height<=cv.height,(name,i,cell.size,x,y)
  cv.alpha_composite(cell,(x,y));k=f'grid21_{name}_{i}';save(k,cv,list(anchor));frames.append(k)
 seq['grid21_'+name]={'frames':frames,'fps':8,'loop':True}
 return frames
bank('door',1,1,(96,144),(112,160),(56,152))
bank('cover',2,2,(156,78),(192,112),(96,104))
bank('crate',2,2,(72,52),(96,80),(48,72))
bank('barrel',2,2,(36,48),(64,64),(32,58))
bank('turret_gun',2,2,(40,40),(56,56),(28,28),True)
bank('turret_laser',2,2,(40,40),(56,56),(28,28),True)
bank('core',4,2,(40,40),(56,56),(28,28),True)
reactor=bank('reactor',4,2,(96,144),(128,176),(64,88),True)
for old,new in [('pb18_door_core','core'),('pb18_turret_gun','turret_gun'),('pb18_turret_laser','turret_laser'),('pb18_barrel','barrel'),('pb18_enemy_crate','crate'),('pb18_armored_crate','crate'),('pb17_enemy_cover_wall','cover')]:
 seq[old]={**seq['grid21_'+new]}
 if old=='pb17_enemy_cover_wall':
  frames=[]
  for i,k in enumerate(seq[old]['frames']):
   m=assets[k];alias='grid21_enemywall_'+str(i);assets[alias]={**m,'drawScale':72/156};frames.append(alias)
  seq[old]['frames']=frames
seq['pb18_master']={'frames':[reactor[i%4] for i in range(8)]+[reactor[4],reactor[4],reactor[5],reactor[5]]+[reactor[6],reactor[6],reactor[7],reactor[7]],'fps':8}
manifest={'version':'grid21-1014-r1','assets':assets,'sequences':seq,'sources':sources,'notes':'Separate component generations; native nearest-neighbor exports; characters and enemies retained.'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(OUT/'manifest.js').write_text('window.TD_GRID21_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8');(OUT/'source/prompts.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
print(json.dumps({'assets':len(assets),'sources':len(sources),'sequences':len(seq)}))
