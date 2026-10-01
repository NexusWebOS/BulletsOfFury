"""Pack authored cinematic portraits; never redraw or overwrite old source art."""
from pathlib import Path
import json, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/cinema_0930'
OUT=ROOT/'assets/game/cinema_0930'
def build():
 OUT.mkdir(parents=True,exist_ok=True)
 data={}
 for name in ('cronos','decker','yuri'):
  im=Image.open(SOURCE/(name+'.png')).convert('RGBA')
  box=im.getchannel('A').getbbox()
  if not box: raise ValueError('Empty '+name)
  im=im.crop(box);im.thumbnail((640,560),Image.Resampling.NEAREST)
  im.save(OUT/(name+'.png'),optimize=True)
  data[name]={'path':'assets/game/cinema_0930/'+name+'.png','width':im.width,'height':im.height}
 (OUT/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
if __name__=='__main__':build()
