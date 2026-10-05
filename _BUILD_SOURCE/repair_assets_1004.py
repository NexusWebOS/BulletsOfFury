"""Normalize the authored island kit; preserve original and exact crop provenance."""
from pathlib import Path
from PIL import Image,ImageFilter,ImageOps
import json,shutil
from collections import deque
R=Path(__file__).resolve().parents[1]
S=Path(r'C:\Users\Mdogg\.codex\generated_images\01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c\exec-1d678880-c09a-40ef-906c-31faf2148873.png')
A=R/'_ART_SOURCES/gameplay_1004';A.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/gameplay_1004';O.mkdir(parents=True,exist_ok=True)
source=A/'campaign_islands.png'
if not source.exists():shutil.copy2(S,source)
im=Image.open(source).convert('RGBA')
xs=[0,411,849,1254];ys=[0,378,818,1254];keys=[1,2,3,4,'hub',5,7,6,8];records=[]
def main_piece(crop):
 # Mechanical sheet separation: discard adjacent cells' stray alpha fragments.
 w,h=crop.size;alpha=bytearray(crop.getchannel('A').tobytes());seen=bytearray(w*h);largest=[]
 for start in range(w*h):
  if seen[start] or alpha[start]<16:continue
  seen[start]=1;q=deque([start]);part=[]
  while q:
   i=q.popleft();part.append(i);x=i%w;y=i//w
   for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
    nx=x+dx;ny=y+dy;j=ny*w+nx
    if 0<=nx<w and 0<=ny<h and not seen[j] and alpha[j]>=16:seen[j]=1;q.append(j)
  if len(part)>len(largest):largest=part
 mask=bytearray(w*h)
 for i in largest:mask[i]=alpha[i]
 crop.putalpha(Image.frombytes('L',(w,h),bytes(mask)));return crop
for n,key in enumerate(keys):
 x,y=n%3,n//3;rect=(xs[x],ys[y],xs[x+1],ys[y+1]);crop=main_piece(im.crop(rect));bb=crop.getbbox();crop=crop.crop(bb)
 crop.thumbnail((496,464),Image.Resampling.NEAREST);c=Image.new('RGBA',(512,512));c.alpha_composite(crop,((512-crop.width)//2,(512-crop.height)//2))
 c.save(O/f'island_{key}.png');alpha=c.getchannel('A')
 gray=ImageOps.grayscale(c).convert('RGBA');gray.putalpha(alpha);gray.save(O/f'island_{key}_lock.png')
 shadow=Image.new('RGBA',c.size,(0,8,22,255));shadow.putalpha(alpha);shadow.save(O/f'island_{key}_shadow.png')
 glow=Image.new('RGBA',c.size,(110,230,255,255));glow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)));glow.save(O/f'island_{key}_glow.png')
 records.append({'key':key,'crop':rect,'opaque_bounds':bb,'output':str(O/f'island_{key}.png')})
im.crop((9,177,49,199)).save(O/'bridge.png')
(A/'manifest.json').write_text(json.dumps({'source':'OpenAI imagegen, 2026-10-04','normalization':'separate largest connected alpha component per cell, nearest-neighbor contain on 512px transparent canvas; derived grayscale/shadow/glow UI masks','bridge_crop':[9,177,49,199],'islands':records},indent=2))

