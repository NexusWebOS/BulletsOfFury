from pathlib import Path
import imageio_ffmpeg
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent; O=W.parents[1]/'outputs/Solid-metal-hammers'
for unit in ['chronos','dracodia']:
 p=O/(unit+'-hammer.mp4')
 if not p.exists()or p.stat().st_size<100:continue
 selections=[8,12,15,18,25,40,55,75,148,155,160,180]
 g=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24'); meta=next(g); sz=meta['size']; board=Image.new('RGB',(1200,960),'#101820'); d=ImageDraw.Draw(board); j=0
 for i,b in enumerate(g):
  if i not in selections:continue
  im=Image.frombytes('RGB',sz,b).crop((265,0,1015,800)).resize((300,320),Image.Resampling.NEAREST); board.paste(im,(j%4*300,j//4*320));d.text((j%4*300+5,j//4*320+8),f'{i/20:.2f}s',fill='white');j+=1
  if j==len(selections):break
 g.close();board.save(W/'reviews'/(unit+'-native-strip.png'));print('Saved native review strip',unit,flush=True)
