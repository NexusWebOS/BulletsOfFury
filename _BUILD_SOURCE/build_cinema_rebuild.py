from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/cinema_story_1021' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Cinema-Rebuild';D=W/'shipping';D.mkdir(exist_ok=True)
root='assets/game/shared/cinematics/cinema_story_1021/'
art={'images':{},'banks':{}};audit=[]
banks={'data_disintegrate':('data_disintegrate',10),'data_blast_motion':('data_blast',14),'blue_portal_motion':('blue_portal',12),'void_portal_motion':('void_portal',12),'remnant_motion':('remnant',10),'code_fragment_motion':('code_fragments',12),'hq_motion':('hq_motion',8),'coast_motion':('coast_motion',12),'forge_motion':('forge_motion',12)}
patches={'hq_motion':('hq_regroup',[432,80,256,256]),'coast_motion':('coast_invasion',[218,222,256,144]),'forge_motion':('forge_upgrade',[220,210,256,144])}
source_only={'data_body','data_blast','blue_portal','dracodia_remnant','void_portal_seed','code_fragments'}
obsolete=source_only-{name for name,fps in banks.values()}
for name in obsolete:
 target=D/(name+'.webp');assert target.resolve().is_relative_to(D.resolve());target.unlink(missing_ok=True)
for p in sorted((W/'returned').glob('*.png')):
 if p.stem in source_only:continue
 if any(p.stem.startswith(s+'-') for s in banks):continue
 im=Image.open(p).convert('RGBA');assert im.width%2==0 and im.height%2==0
 target=D/(p.stem+'.webp');im.save(target,lossless=True,method=6)
 version='?v='+hashlib.sha256(target.read_bytes()).hexdigest()[:12] if p.stem in {'hq_regroup','forge_upgrade','hq_alarm','hq_river','launch_generator','power_cell'} else ''
 art['images'][p.stem]={'key':'c22_'+p.stem,'path':root+target.name+version,'w':im.width,'h':im.height}
for source,(name,fps) in banks.items():
 files=sorted((W/'returned').glob(source+'-*.png'))
 if not files:continue
 frames=[Image.open(p).convert('RGBA') for p in files];size=frames[0].size;assert all(f.size==size for f in frames) and size[0]%2==size[1]%2==0
 # Preserve the exact source boundary around animated scene-detail inserts.
 if name in patches:
  first=frames[0]
  for frame in frames[1:]:
   for box in [(0,0,size[0],4),(0,size[1]-4,size[0],size[1]),(0,0,4,size[1]),(size[0]-4,0,size[0],size[1])]:frame.paste(first.crop(box),box)
 sheet=Image.new('RGBA',(size[0]*4,size[1]*((len(frames)+3)//4)))
 for i,frame in enumerate(frames):sheet.alpha_composite(frame,(i%4*size[0],i//4*size[1]))
 target=D/(name+'.webp');sheet.save(target,lossless=True,method=6)
 art['banks'][name]={'key':'c22_bank_'+name,'path':root+target.name,'w':size[0],'h':size[1],'frames':len(frames),'columns':4,'fps':fps,'pivot':[size[0]//2,size[1]//2]}
 if name in patches:art['banks'][name]['patch']={'image':patches[name][0],'rect':patches[name][1]}
for p in D.glob('*.webp'):audit.append({'name':p.name,'bytes':p.stat().st_size,'size':Image.open(p).size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(W/'cinema_story_art_1021.js').write_text("'use strict';\n// Owned by build_cinema_rebuild.py. Fixed even canvases and common bank pivots.\nconst C22_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
(W/'export-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('Built',len(art['images']),'images and',len(art['banks']),'banks;',sum(p.stat().st_size for p in D.glob('*.webp')),'bytes')
if '--install' in sys.argv:
 T=R/root;T.mkdir(parents=True,exist_ok=True)
 for name in obsolete:
  target=T/(name+'.webp');assert target.resolve().is_relative_to(T.resolve());target.unlink(missing_ok=True)
 for p in D.glob('*.webp'):shutil.copy2(p,T/p.name)
 for name in ['cinema_story_art_1021.js','cinema_story_1021.js']:shutil.copy2(W/name,R/'assets'/name)
 index=R/'index.html';s=index.read_text(encoding='utf-8')
 for name in ['cinema_story_art_1021','cinema_story_1021']:
  tag='<script src="assets/'+name+'.js?v=cinema-story-1021-1"></script>'
  if name+'.js' not in s:s=s.replace('</body>',tag+'\n</body>')
 index.write_text(s,encoding='utf-8',newline='')
 print('Installed isolated cinematic owner and art; other files retained')
