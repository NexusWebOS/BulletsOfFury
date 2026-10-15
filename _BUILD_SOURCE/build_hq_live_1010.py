"""Own live-HQ cinematic plate/sweep exports and registration together.

Only cut, pad and translate generated RGBA. No repainting or per-cell resizing.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_ART_SOURCES/hq_live_1010'
DEST=ROOT/'assets/game/shared/cinematics/hq_live_1010'
GEN=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
RAW.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def archive(name,source):
 p=RAW/(name+'_raw.png')
 if not p.exists():shutil.copy2(GEN/source,p)
 return p,Image.open(p).convert('RGBA')
banks={};sources=[]
for name,source,cols,rows,size in [
 ('background','exec-0bcc73a1-551f-422b-9e76-a1acab4759f7.png',2,2,(840,472)),
 ('radar','exec-3ad6c72d-fbf0-456a-a667-276f8bd212ee.png',8,4,(256,256))]:
 p,im=archive(name,source);bank=[];W,H=im.size
 for i in range(cols*rows):
  c,r=i%cols,i//cols
  box=[round(c*W/cols),round(r*H/rows),round((c+1)*W/cols),round((r+1)*H/rows)]
  cell=im.crop(box);pivot=[size[0]//2,size[1]//2]
  if name=='radar':
   # Bright central ignition dot: align the ring's physical origin, not its
   # moving sweep's visible bounds. Preserve the generated alpha exactly.
   cx,cy=cell.width//2,cell.height//2
   points=[]
   for y in range(cy-5,cy+6):
    for x in range(cx-5,cx+6):
     red,green,blue,alpha=cell.getpixel((x,y))
     if alpha>128 and red>105 and green>180 and blue>140:points.append((x,y))
   assert points,(name,i,'Missing fixed radar origin')
   source_pivot=[round(sum(x for x,y in points)/len(points)),round(sum(y for x,y in points)/len(points))]
  else:source_pivot=[cell.width//2,cell.height//2]
  shift=[pivot[0]-source_pivot[0],pivot[1]-source_pivot[1]]
  out=Image.new('RGBA',size,(0,0,0,255) if name=='background' else (0,0,0,0));out.alpha_composite(cell,tuple(shift))
  dest=DEST/(name+'_'+str(i).zfill(2)+'.png');out.save(dest,optimize=True)
  bank.append(dict(key='hq10_'+name+'_'+str(i).zfill(2),path=dest.relative_to(ROOT).as_posix(),w=size[0],h=size[1],pivot=pivot,source_rect=box,source_pivot=source_pivot,translation=shift,scale=1,sha256=sha(dest)))
 assert len({a['sha256'] for a in bank})==len(bank)
 banks[name]=bank
 registration=dict(raw=p.relative_to(ROOT).as_posix(),raw_sha256=sha(p),bank=bank)
 (RAW/(name+'_registration.json')).write_text(json.dumps(registration,indent=2)+'\n',encoding='utf-8')
 sources.append(dict(name=name,path=registration['raw'],sha256=registration['raw_sha256'],size=[W,H]))
(ROOT/'assets/hq_live_art_1010.js').write_text('"use strict";\nconst HQ10_ART='+json.dumps(banks,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
manifest_path=RAW/'generation_manifest.json'
prior=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
prior.update(tool='built-in image_gen',sources=sources,shipping_assets=[a for bank in banks.values() for a in bank],reference_manifest='references/manifest.json',normalization='Measured origin; crop/pad/translation only at scale 1. Runtime clips the authored acquisition field to progressively fill it; generated sweep frames animate the held scan.')
manifest_path.write_text(json.dumps(prior,indent=2)+'\n',encoding='utf-8')
print(json.dumps({name:len(bank) for name,bank in banks.items()}))
