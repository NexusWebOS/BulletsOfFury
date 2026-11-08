from pathlib import Path
import json,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;V=W.parent/'BOF-Furious-Boss-Videos-1104';R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
clip=next(c for c in json.loads((V/'manifest.json').read_text())if c['id']=='sumpjaw');routes=json.loads((V/'routes.json').read_text());movie=routes[clip['url']];sheet=Image.new('RGB',(960,560),(7,15,22));d=ImageDraw.Draw(sheet)
for i,label in enumerate(['Airborne pounce over the pilot','Giant toxic orb volley','Rapid acid spit volley','Coiling serpent attack']):
 ch=next(c for c in clip['chapters']if c['label']==label);time=ch['time']+1.8;out=W/('film-'+str(i)+'.png')
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-ss',str(time),'-i',movie,'-frames:v','1','-y',str(out)],check=True)
 im=Image.open(out).convert('RGB');im.thumbnail((240,520));sheet.paste(im,(i*240,25));d.text((i*240+5,5),label,fill='white')
sheet.save(W/'live-fight-review.jpg');print('Inspected four actual decoded fight chapters.')
