from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=R/'_shots/cinematic_invasion_1020';movie=O/'invasion-ending-native.webm';shots=[]
for t in [1.5,11.5,29,42,50,67,77,88,100,108,114,117,122,131,148]:
 p=O/f'film-{t:g}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1',str(p)],check=True);im=Image.open(p).convert('RGB');assert im.getbbox();shots.append((t,im))
sheet=Image.new('RGB',(5*384,3*238),'#101522');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):im.thumbnail((384,216));sheet.paste(im,((i%5)*384,(i//5)*238));d.text(((i%5)*384+5,(i//5)*238+218),str(t)+'s decoded movie',fill='white')
sheet.save(O/'recorded-film-contact-sheet.jpg',quality=94);(O/'film-report.json').write_text(json.dumps({'passed':15,'checks':15,'errors':[],'decodedFrames':[t for t,_ in shots]},indent=2));print('15 native movie frames decoded')
