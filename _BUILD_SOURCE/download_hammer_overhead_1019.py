"""Inspect the returned PixelLab candidate; no shipping export or frame fitting."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,urllib.request
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('--job',default='ef9017f2-aef2-4f32-8a9e-6c57255b0878');ap.add_argument('--bank',default='overhead');ap.add_argument('--frames',type=int,default=17);args=ap.parse_args()
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/hammer_motion_1019'/args.bank;O=R/'_shots/overnight_combat_1019'/('hammer-'+args.bank);S.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
job=args.job
def download(i):
 p=S/f'frame_{i:02}.png'
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90).read())
 im=Image.open(p).convert('RGBA');assert im.size==(256,256)
 return dict(index=i,bounds=im.getbbox(),hash=hashlib.sha256(im.tobytes()).hexdigest())
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(download,range(args.frames)))
frames=[Image.open(S/f'frame_{i:02}.png').convert('RGBA') for i in range(args.frames)]
sheet=Image.new('RGBA',(1152,((len(frames)+3)//4)*288),(8,13,23,255));onions=sheet.copy()
for i,im in enumerate(frames):
 at=(i%4*288+16,i//4*288+16);sheet.alpha_composite(im,at);ImageDraw.Draw(sheet).text((at[0],at[1]+256),str(i),fill='white')
 for j in [max(0,i-1),min(len(frames)-1,i+1)]:
  ghost=frames[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:round(a*.22)));onions.alpha_composite(ghost,at)
 onions.alpha_composite(im,at)
sheet.save(O/'candidate.png');onions.save(O/'candidate-onions.png')
frames[0].save(O/'candidate.webp',save_all=True,append_images=frames[1:],duration=90,loop=0,lossless=True)
(S/'inspection.json').write_text(json.dumps(dict(job=job,canvas=[256,256],pivot=[128,128],scale=1,records=records,status='Candidate only; pending hand/anatomy/root inspection'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(downloaded=len(frames),unique=len({r['hash'] for r in records}),bounds=[r['bounds'] for r in records])))
