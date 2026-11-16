from pathlib import Path
import subprocess,json,sys
from PIL import Image,ImageDraw
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';F=O/'stage56/films';ff=imageio_ffmpeg.get_ffmpeg_exe()
media=[]
for name in ['chronos','hq5']:
 src=F/(name+'.webm');dest=F/(name+'.mp4')
 if not dest.exists():
  subprocess.run([ff,'-y','-i',str(src),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dest)],stdout=subprocess.DEVNULL,stderr=(F/(name+'-encode.log')).open('w'),check=True)
 frames=O/'stage56'/name;frames.mkdir(exist_ok=True)
 subprocess.run([ff,'-y','-i',str(dest),'-vf','fps=1/5,scale=456:256','-frames:v','40',str(frames/'frame-%03d.png')],stdout=subprocess.DEVNULL,stderr=(frames/'decode.log').open('w'),check=True)
 files=sorted(frames.glob('frame-*.png'));sheet=Image.new('RGB',(1368,((len(files)+2)//3)*279),(6,10,18));d=ImageDraw.Draw(sheet)
 for i,p in enumerate(files):x=i%3*456;y=i//3*279;sheet.paste(Image.open(p).convert('RGB'),(x,y));d.text((x+5,y+258),name+' '+str(i*5+2.5)+' s',fill='white')
 sheet.save(frames/'contact.jpg')
 meta=subprocess.run([ff,'-i',str(dest),'-af','astats=metadata=0:reset=0','-f','null','-'],capture_output=True,text=True).stderr
 (frames/'decoded-audio-stats.log').write_text(meta,encoding='utf8')
 media.append({'name':name,'source':'stage56/films/'+name+'.webm','file':'stage56/films/'+name+'.mp4','decodeCode':0,'frames':len(files),'audioEvidence':'stage56/'+name+'/decoded-audio-stats.log','scope':'Prepared native cinematic checkpoint, not a combat win. Native clock, scene owner, mixer audio and automatic dialogue; results/equipment menus between the two clips omitted.'})
(O/'stage56/media.json').write_text(json.dumps(media,indent=2),encoding='utf8')
print(json.dumps(media,indent=2))
