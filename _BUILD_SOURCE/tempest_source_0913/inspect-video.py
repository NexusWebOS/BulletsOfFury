from pathlib import Path
import imageio_ffmpeg,subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2];out=root/'_shots/tempest_duo_0913'
movie=out/'BulletsOfFury_Stage6_TempestBrothers.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
times=[4,7,12,18,28,36,42,54]
sheet=Image.new('RGB',(320*4,370*2),'#111820')
for i,t in enumerate(times):
    dst=out/('video_%02ds.png'%t)
    subprocess.run([ff,'-y','-loglevel','error','-ss',str(t),'-i',str(movie),'-frames:v','1',str(dst)],check=True)
    im=Image.open(dst).convert('RGB');im.thumbnail((320,342));sheet.paste(im,(i%4*320,i//4*370));ImageDraw.Draw(sheet).text((i%4*320+8,i//4*370+347),str(t)+' seconds',fill='white')
sheet.save(out/'video_contact.png')
r=subprocess.run([ff,'-hide_banner','-i',str(movie)],capture_output=True,text=True)
print(r.stderr)
r=subprocess.run([ff,'-hide_banner','-i',str(movie),'-vn','-af','volumedetect','-f','null','NUL'],capture_output=True,text=True)
print('\n'.join(s for s in r.stderr.splitlines()if 'volume:'in s))
print('movie bytes',movie.stat().st_size)
