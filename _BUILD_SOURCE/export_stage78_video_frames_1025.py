"""Decode actual revised-fight frames at the observed native event times."""
from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage78_review_1025/decoded';O.mkdir(parents=True,exist_ok=True)
spec={7:[17.2,18.0,18.8,19.5,196.0],8:[15.8,78.2,113.8,120.0,135.0,151.6,164.7,168.0,172.0,176.1,177.0,710.3]}
files=[]
for stage,times in spec.items():
 q=json.loads(max((R/'_shots/stage78_review_1025/full').glob(f'stage{stage}*/verification.json'),key=lambda p:p.stat().st_mtime).read_text());video=q['video']
 for at in times:
  p=O/f'stage{stage}-{at:.1f}.png';subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-threads','2','-ss',str(at),'-i',video,'-frames:v','1',str(p)],check=True);files.append((stage,at,p))
sheet=Image.new('RGB',(4*320,((len(files)+3)//4)*222),(5,10,17));g=ImageDraw.Draw(sheet)
for i,(s,t,p)in enumerate(files):sheet.paste(Image.open(p).convert('RGB').resize((320,200)),((i%4)*320,(i//4)*222));g.text(((i%4)*320+5,(i//4)*222+203),f'Revised S{s} {int(t)//60:02}:{t%60:04.1f}',fill='white')
sheet.save(O/'contact.jpg');print(json.dumps({'decoded':len(files),'contact':str(O/'contact.jpg')}))
