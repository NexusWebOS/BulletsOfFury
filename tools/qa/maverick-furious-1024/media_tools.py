from pathlib import Path
import sys,subprocess,json
import imageio_ffmpeg
from PIL import Image,ImageOps,ImageDraw
W=Path(__file__).resolve().parent;O=W/'review';FF=imageio_ffmpeg.get_ffmpeg_exe()
if sys.argv[1]=='sample-audio':
 p=O/'maverick-furious-full-campaign.webm'
 r=subprocess.run([FF,'-hide_banner','-ss',sys.argv[2]if len(sys.argv)>2 else'25','-i',str(p),'-t','6','-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
 print('\n'.join(x for x in r.stderr.splitlines()if any(k in x for k in ['Audio:','mean_volume','max_volume','Duration:'])))
if sys.argv[1]=='sheet':
 images=sorted(O.glob('screen-*.png'));start=int(sys.argv[2])if len(sys.argv)>2 else 0;images=images[start:start+16]
 out=Image.new('RGB',(1280,4*205),(12,16,24));d=ImageDraw.Draw(out)
 for n,p in enumerate(images):
  im=Image.open(p).convert('RGB');im.thumbnail((320,180));x=n%4*320;y=n//4*205;out.paste(im,(x,y));d.text((x+5,y+184),p.stem,fill='white')
 path=O/f'sheet-{start:03}.jpg';out.save(path,quality=91);print(path)
if sys.argv[1]=='convert':
 p=O/'maverick-furious-full-campaign.webm';out=O/'Maverick-Furious-Beta-Playthrough.mp4'
 cmd=[FF,'-hide_banner','-y','-i',str(p),'-c:v','libx264','-preset','veryfast','-crf','21','-maxrate','3500k','-bufsize','7000k','-threads','2','-pix_fmt','yuv420p','-fps_mode','vfr','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)]
 with (O/'conversion.log').open('w')as f:r=subprocess.run(cmd,stdout=f,stderr=f)
 if r.returncode:raise RuntimeError('Video conversion failed')
 print(out,out.stat().st_size)
if sys.argv[1]=='frames':
 start=float(sys.argv[2]);count=int(sys.argv[3])if len(sys.argv)>3 else 8;step=float(sys.argv[4])if len(sys.argv)>4 else 2
 folder=O/f'frames-{int(start):05}';folder.mkdir(exist_ok=True)
 subprocess.run([FF,'-v','error','-ss',str(start),'-i',str(O/'maverick-furious-full-campaign.webm'),'-t',str(count*step),'-vf',f'fps=1/{step}','-frames:v',str(count),str(folder/'frame-%02d.png')],check=True)
 ims=sorted(folder.glob('frame-*.png'));sheet=Image.new('RGB',(1280,((len(ims)+3)//4)*205),(12,16,24));d=ImageDraw.Draw(sheet)
 for n,p in enumerate(ims):
  im=Image.open(p);im.thumbnail((320,180));x=n%4*320;y=n//4*205;sheet.paste(im,(x,y));d.text((x+5,y+183),f'{start+n*step:.1f}s',fill='white')
 dest=folder/'sheet.jpg';sheet.save(dest,quality=93);print(dest)
