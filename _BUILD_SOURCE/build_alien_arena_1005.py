"""Deploy authored arena/components without repainting native image pixels."""
from pathlib import Path
from PIL import Image
import hashlib, json, shutil
R=Path(__file__).resolve().parents[1]
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
S=R/'_ART_SOURCES/alien_arena_1005'; O=R/'assets/game/alien_arena_1005'
S.mkdir(parents=True,exist_ok=True); O.mkdir(parents=True,exist_ok=True)
sources={
 'back':('exec-54a878a9-e1cf-4367-966c-c17a91b2d9bd.png',1,1,'Edit the alien cathedral perimeter; central 60 percent pitch-black void. Preserve black chrome, skull pillars and crimson lava at edges. Remove purple haze and crossing bridges from center. Opaque, no characters or UI.'),
 'front':('exec-60016014-1366-47d0-8f48-22c0857c1386.png',1,1,'Transparent portrait black chrome biomechanical ribs and skull pillars at far edges only. Central 75 percent empty alpha. Near-black, restrained silver/crimson/green ports, no floor, characters or UI.'),
 'code':('exec-37ddd385-ae49-41e6-9059-c1593af91ded.png',4,3,'Twelve equal ordered frames of the same narrow five-column emerald binary bank. Alternating columns scroll down/up, moving lime heads and dim trails, anchored chrome rib, genuine transparency, detailed arcade pixels.'),
 'void':('exec-f41f6e0d-0d92-46e0-96d8-543165742d3f.png',4,3,'Twelve equal ordered black oily symbiote gather/iris/open/rotating void frames, steel glints and crimson/violet fissures, fixed pivot, native transparent outer alpha, no download, bubble or UI.'),
 'ghost':('exec-48981847-cee4-4218-bc3c-03896824fd0f.png',3,3,'Nine isolated modular ghost components: reactor torso, complete crowned head, tail, left and right upper arms, left and right claws, eye satellite, cannon. Black oil/violet plasma/ivory eyes/red fissures, native alpha, equal cells and visible joint sockets.')}
art={}; manifest={'generator':'built-in image_gen','alpha':'native, unmodified','sources':{}}
for name,(file,cols,rows,prompt) in sources.items():
 src=S/(name+'.png')
 if not src.exists(): shutil.copyfile(G/file,src)
 im=Image.open(src); assert im.width%cols==0 and im.height%rows==0
 cw,ch=im.width//cols,im.height//rows; cells=[]
 for f in range(cols*rows):
  cell=im.crop((f%cols*cw,f//cols*ch,(f%cols+1)*cw,(f//cols+1)*ch))
  # Crop only the transparent padding for modular joint placement. Pixels and
  # original source are retained exactly; runtime registers measured bounds.
  box=cell.getbbox() if name=='ghost' else (0,0,cw,ch)
  cell=cell.crop(box); path=O/(name+'_'+str(f)+'.png'); cell.save(path)
  cells.append({'key':'aa5_'+name+'_'+str(f),'path':path.relative_to(R).as_posix(),'w':cell.width,'h':cell.height,'sourceBox':box})
 art[name]=cells
 manifest['sources'][name]={'path':src.relative_to(R).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prompt':prompt,'columns':cols,'rows':rows}
(R/'assets/alien_arena_art_1005.js').write_text('"use strict";\nconst AA5_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Deployed 35 authored cells: deep-black arena, transparent ribs, code/void loops and ghost modules.')
