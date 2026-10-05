"""Separate generated map sheets, preserve source pixels, derive UI masks."""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
import json, shutil, hashlib
from collections import deque

R = Path(__file__).resolve().parents[1]
G = Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
A = R / '_ART_SOURCES/campaign_landscape_1004e'
O = R / 'assets/game/campaign_landscape_1004e'
A.mkdir(parents=True, exist_ok=True)
O.mkdir(parents=True, exist_ok=True)
SOURCES = [
 ('regions_north', 'exec-34046e93-8b55-4e4d-922c-c06a5f0b24ce.png', [1,2,3,4]),
 ('regions_south', 'exec-91756c1d-d83c-4ed5-a373-20c29672e019.png', [5,6,7,8]),
 ('city_hq_portal', 'exec-392e198f-d6f2-41ac-9983-9deeb93b7cec.png', ['hub','hq',9,'islets']),
 ('landscape', 'exec-c3adc370-6e6d-4a06-b609-c89b08765613.png', []),
]
records = []
for name, file, keys in SOURCES:
 src = A / (name + '.png')
 if not src.exists(): shutil.copy2(G/file, src)
 im = Image.open(src).convert('RGBA')
 assert im.getchannel('A').getextrema()[0] == 0, 'Expected genuine generated alpha'
 if not keys:
  shutil.copy2(src, O/'landscape.png')
  records.append({'key':'landscape','source':src.name,'size':im.size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
  continue
 for n, key in enumerate(keys):
  col, row = n%2, n//2
  split_y = 480 if name == 'city_hq_portal' and col == 0 else 512
  rect = (col*768, 0 if row == 0 else split_y, (col+1)*768, split_y if row == 0 else 1024)
  crop = im.crop(rect)
  if key == 9:
   # The generated city surf leaves disconnected fragments across this gutter.
   # Remove only small alpha components touching the cut's upper edge.
   w,h = crop.size
   alpha = bytearray(crop.getchannel('A').tobytes())
   seen = set()
   for x in range(w):
    if not alpha[x] or x in seen: continue
    q = deque([x]); seen.add(x); part = []
    while q:
     i=q.popleft(); part.append(i); px,py=i%w,i//w
     for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
      nx,ny=px+dx,py+dy;j=ny*w+nx
      if 0<=nx<w and 0<=ny<h and j not in seen and alpha[j]: seen.add(j);q.append(j)
    if len(part) < w*h*.025:
     for i in part: alpha[i]=0
   crop.putalpha(Image.frombytes('L',(w,h),bytes(alpha)))
  bb = crop.getbbox()
  crop = crop.crop(bb)
  crop.thumbnail((724,704), Image.Resampling.NEAREST)
  c = Image.new('RGBA',(768,768))
  c.alpha_composite(crop, ((768-crop.width)//2, (768-crop.height)//2))
  c.save(O/f'region_{key}.png')
  alpha = c.getchannel('A')
  gray = ImageOps.grayscale(c).convert('RGBA'); gray.putalpha(alpha)
  gray.save(O/f'region_{key}_lock.png')
  shadow = Image.new('RGBA',c.size,(0,8,22)); shadow.putalpha(alpha)
  shadow.save(O/f'region_{key}_shadow.png')
  glow = Image.new('RGBA',c.size,(146,230,255)); glow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)))
  glow.save(O/f'region_{key}_glow.png')
  records.append({'key':key,'source':src.name,'crop':rect,'alpha_bounds':bb,'normalized_size':c.size})
manifest = {'generator':'OpenAI built-in imagegen, October 4 2026','normalization':'Mechanical sheet separation, nearest-neighbor contain, derived grayscale and alpha UI masks; no invented terrain pixels.','sources':[{'name':n,'sha256':hashlib.sha256((A/(n+'.png')).read_bytes()).hexdigest()} for n,_,_ in SOURCES],'assets':records}
(A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
taxonomy=R/'assets/data/ART_TAXONOMY.json'
data=json.loads(taxonomy.read_text(encoding='utf-8'))
data['map4e_']={'role':'campaign_landscape','sheet':None,'note':'October 4: Mike approved the new region art and explicitly requested large landscapes underneath the stage regions. Built-in imagegen authored a connected eight-biome continent, eight larger regions, central city, HQ coast, cosmic Stage 9 portal and satellite islets. Mechanical sheet separation/derived lock-shadow-glow masks owned by _BUILD_SOURCE/build_campaign_landscape_1004e.py. Source/provenance _ART_SOURCES/campaign_landscape_1004e. Original blue ocean, stage flags, Fury HQ icon and drifting clouds retained. Runtime campaign_landscape_1004e.js. No atlas repack.'}
taxonomy.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Built 12 authored region cutouts, connected landscape and UI masks.')
