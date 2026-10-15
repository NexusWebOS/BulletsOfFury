"""Inspect every supplied GIF and export representative original frames."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'_ART_SOURCES/portals_1011/reference';REF.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'_shots/portals_1011';OUT.mkdir(parents=True,exist_ok=True)
report=[]
for name in ['portal','void-portal','tp','tp2']:
 src=Path('C:/Users/Mdogg/Desktop')/(name+'.gif');dest=REF/src.name;shutil.copyfile(src,dest)
 im=Image.open(src);frames=[];dur=[]
 for i in range(im.n_frames):
  im.seek(i);frames.append(im.convert('RGBA').copy());dur.append(im.info.get('duration',0))
 indices=list(range(len(frames))) if len(frames)<9 else [round(i*(len(frames)-1)/7) for i in range(8)]
 sheet=Image.new('RGB',(4*256,2*292),'#10121b');d=ImageDraw.Draw(sheet)
 for n,i in enumerate(indices):
  f=frames[i];f.save(REF/f'{name}_{i:02d}.png');small=f.copy();small.thumbnail((240,256),Image.Resampling.NEAREST)
  x=(n%4)*256+(256-small.width)//2;y=(n//4)*292+24
  sheet.paste(small,(x,y),small.getchannel('A'));d.text(((n%4)*256+12,(n//4)*292+6),f'{name} / {i+1:02d}',fill='#ffffff')
 sheet.save(OUT/f'{name}-motion.png')
 report.append(dict(name=name,size=list(im.size),frames=len(frames),durations=dur,
  sampledFrames=indices,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(REF/'inspection.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report))
