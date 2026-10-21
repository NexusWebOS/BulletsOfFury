from pathlib import Path
from PIL import Image
import hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/cinematic_finish_1020';S=R/'_ART_SOURCES/cinematic_finish_1020';D=R/'assets/game/shared/cinematics/cinematic_finish_1020';D.mkdir(parents=True,exist_ok=True);S.mkdir(exist_ok=True)
sources={name:str(S/(name+'-master.png')) for name in ['debrief','relay']}
art={};records=[]
for name,source in sources.items():
 raw=Path(source);im=Image.open(raw).convert('RGB');w,h=im.size;out=Image.new('RGB',(w+w%2,h+h%2),'black');out.paste(im);p=D/(name+'.webp');out.save(p,lossless=True,method=6)
 art[name]=dict(key='ce20_'+name,path=p.relative_to(R).as_posix(),w=out.width,h=out.height,content_rect=[0,0,w,h]);records.append(dict(name=name,master=(S/(name+'-master.png')).relative_to(R).as_posix(),sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),sourceSize=[w,h],exportSize=list(out.size),bytes=p.stat().st_size,policy='Original generated pixels preserved; even transparent-free bottom padding only; no resampling. Environment has no pilots or aircraft.'))
(D/'manifest.json').write_text(json.dumps(dict(art=art,sources=records),indent=2)+'\n');(R/'assets/cinematic_ending_art_1020.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_cinematic_finish_1020.py.\nconst CE20_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(plates=len(art),bytes=sum(v['bytes'] for v in records))))
