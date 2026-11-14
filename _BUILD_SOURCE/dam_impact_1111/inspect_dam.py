from pathlib import Path
from PIL import Image,ImageChops
import json
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/dam-impact';O.mkdir(parents=True,exist_ok=True)
a=Image.open(R/'assets/game/levels/stage_01/stage/bg_stage01_intact.png').convert('RGBA');b=Image.open(R/'assets/game/levels/stage_01/stage/bg_stage01_destroyed.png').convert('RGBA');diff=ImageChops.difference(a,b);bbox=diff.convert('RGB').getbbox();out=Image.new('RGB',(1360,850),(6,25,30));out.paste(a.crop((0,0,680,850)),(0,0),a.crop((0,0,680,850)));out.paste(b.crop((0,0,680,850)),(680,0),b.crop((0,0,680,850)));out.save(W/'dam-reference.png');(W/'source-measurements.json').write_text(json.dumps({'size':a.size,'changed_bounds':bbox},indent=2));print(json.dumps({'size':a.size,'changed_bounds':bbox}))
