from pathlib import Path
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;E=W/'exports';V=W/'reviews';V.mkdir(exist_ok=True)
pairs=[(15,16),(16,17),(18,19),(21,22),(22,24),(29,31)];out=Image.new('RGBA',(3072,1024),'#101820');d=ImageDraw.Draw(out)
for row,prefix in enumerate(['blue','corrupt']):
 for col,(a,b)in enumerate(pairs):
  x=Image.open(E/(prefix+'-overhead')/f'{a:02}.png').convert('RGBA');y=Image.open(E/(prefix+'-overhead')/f'{b:02}.png').convert('RGBA');out.alpha_composite(Image.blend(x,y,.5),(col*512,row*512));d.line((col*512,row*512+410,(col+1)*512,row*512+410),fill='#467684');d.text((col*512+10,row*512+10),prefix+' center '+str(a)+' / '+str(b),fill='white')
out.save(V/'center-onion-review.png')
for prefix in ['blue','corrupt']:
 out=Image.new('RGBA',(2048,4096),'#101820');d=ImageDraw.Draw(out)
 for i in range(32):out.alpha_composite(Image.open(E/(prefix+'-overhead')/f'{i:02}.png').convert('RGBA'),(i%4*512,i//4*512));d.text((i%4*512+8,i//4*512+8),str(i),fill='white')
 out.save(V/(prefix+'-center-all-poses.png'))
print('Saved complete-family pose and onion reviews.',flush=True)
