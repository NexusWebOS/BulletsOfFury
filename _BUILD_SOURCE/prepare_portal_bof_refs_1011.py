"""Build a style board from actual Bullets of Fury art, not the supplied GIFs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_ART_SOURCES/portals_bof_1011/reference';OUT.mkdir(parents=True,exist_ok=True)
refs=[
 ('Electric corona','assets/game/shared/combat/arcade_finish_1010/electric_ring_10.png'),
 ('Plasma detonation','assets/game/shared/combat/arcade_finish_1010/plasma_blast_12.png'),
 ('Alien material','assets/game/levels/stage_08/stage/alien_arena_1005/void_10.png'),
 ('Armored machinery','_ART_SOURCES/playthrough_1011/references/aa5_ghost_0.png'),
 ('Wind emerald','assets/game/shared/player_weapons/wind_1011/tornado_08.png'),
 ('Chrome symbiote','_ART_SOURCES/hardcorps_1007/void_source.png')]
board=Image.new('RGB',(1152,768),'#071019');draw=ImageDraw.Draw(board);record=[]
for i,(label,path) in enumerate(refs):
 src=ROOT/path;im=Image.open(src).convert('RGBA')
 if 'void_source' in path:im=im.crop((0,0,round(im.width/4),round(im.height/4)))
 dst=OUT/(str(i)+'-'+Path(path).name);im.save(dst)
 scale=min(344/im.width,318/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
 x=i%3*384+(384-im.width)//2;y=i//3*384+48+(320-im.height)//2
 board.paste(im,(x,y),im);draw.text((i%3*384+20,i//3*384+16),label,fill='#e1edf6')
 record.append(dict(label=label,path=path,sha256=hashlib.sha256(src.read_bytes()).hexdigest(),export=dst.relative_to(ROOT).as_posix()))
board.save(OUT/'bof-style-board.png')
(OUT/'sources.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(OUT/'bof-style-board.png')
