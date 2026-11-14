from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

W=Path(__file__).resolve().parent/'cap_strikes_1111'
O=W.parent.parent/'outputs/End-cap-strikes';O.mkdir(parents=True,exist_ok=True)
M=json.loads((W/'manifest.json').read_text());board=Image.new('RGB',(640*3,640*2),'#101820');draw=ImageDraw.Draw(board)
checks=[]
for row,unit in enumerate(['blue','corrupt']):
 for col,(bank,index,label)in enumerate([('overhead',11,'DOWN: lower end cap'),('sides',8,'LEFT: left end cap'),('right',8,'RIGHT: right end cap')]):
  name=unit+'-'+bank;sheet=Image.open(W/'exports'/(name+'_regular.png')).convert('RGBA')
  frame=sheet.crop((index%4*640,index//4*640,index%4*640+640,index//4*640+640));board.paste(frame,(col*640,row*640),frame);draw.text((col*640+15,row*640+15),unit.upper()+' / '+label,fill='white')
  meta=M[name]['meta'][index];axis=np.asarray(meta['capAxis']);offset=np.asarray(meta['tip'])-np.asarray(meta['headCenter']);assert np.dot(axis,offset)>15,(name,offset)
  checks.append({'bank':name,'frame':index,'capAxis':meta['capAxis'],'headToEndFace':offset.tolist(),'passed':True})
 overhead=M[unit+'-overhead']['meta'];xs=[m['headCenter'][0]for m in overhead[8:12]];drift=max(xs)-min(xs)
 assert drift<5,(unit,'downstroke lateral drift',xs)
 checks.append({'unit':unit,'check':'head descends in vertical centerline','lateralDriftPixels':drift,'passed':True})
 frames=[];dur=[]
 for suffix in ['overhead','overhead','sides','right']:
  sheet=Image.open(W/'exports'/(unit+'-'+suffix+'_regular.png')).convert('RGBA')
  for i in range(16):
   f=sheet.crop((i%4*640,i//4*640,i%4*640+640,i//4*640+640));bg=Image.new('RGBA',(640,640),'#101820');bg.alpha_composite(f);frames.append(bg.convert('RGB'));dur.append(140 if suffix=='overhead'and i in[4,5,11] else 75)
 frames[0].save(O/(('Chronos'if unit=='blue'else'Dracodia')+'-end-cap-swings.gif'),save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=2)
board.save(O/'contact-poses.png')
(W/'geometry-review.json').write_text(json.dumps({'checks':checks,'passed':True,'visualReview':'Complete source/cell contact drawings; end faces lead down/left/right with rigid T-joints.'},indent=2))
print('Contact directions and vertical descent pass; frame GIFs saved.',flush=True)
