from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';ff=imageio_ffmpeg.get_ffmpeg_exe()
for folder,parts in [('stage3-current',['lead-in','arrival','hq']),('stage45-current',['post4','assembly'])]:
 for name in parts:
  src=O/folder/(name+'.webm');dest=src.with_suffix('.mp4')
  if not src.exists():continue
  if not dest.exists():subprocess.run([ff,'-y','-i',str(src),'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dest)],stdout=subprocess.DEVNULL,stderr=(O/folder/(name+'-encode.log')).open('w'),check=True)
  D=O/folder/name;D.mkdir(exist_ok=True);subprocess.run([ff,'-y','-i',str(dest),'-vf','fps=1/10,scale=456:256','-frames:v','40',str(D/'frame-%03d.png')],stdout=subprocess.DEVNULL,stderr=(D/'decode.log').open('w'),check=True);files=sorted(D.glob('frame-*.png'));sheet=Image.new('RGB',(1368,((len(files)+2)//3)*280),(7,13,22));d=ImageDraw.Draw(sheet)
  for i,p in enumerate(files):x=i%3*456;y=i//3*280;sheet.paste(Image.open(p).convert('RGB'),(x,y));d.text((x+4,y+259),folder+' '+name+' '+str(i*10+5)+'s',fill='white')
  sheet.save(D/'contact.jpg',quality=90);print(folder,name,len(files),'decoded frames',flush=True)
