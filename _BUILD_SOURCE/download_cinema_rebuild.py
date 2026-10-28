from pathlib import Path
import json,urllib.request,re,zipfile,sys
O=Path(__file__).resolve().parents[1]/'_ART_SOURCES/cinema_story_1021' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Cinema-Rebuild';D=O/'returned';D.mkdir(exist_ok=True)
for entry in json.loads((O/(sys.argv[1] if len(sys.argv)>1 else 'job-ledger.json')).read_text(encoding='utf-8-sig')):
 text=entry.get('receipt') or '';m=re.search(r'download: (https://\S+)',text)
 if not m:continue
 count=re.search(r'frames: (\d+)',text)
 if count and int(count[1])>1:
  url=m[1].split('?')[0]
  for i in range(int(count[1])):
   target=D/(entry['id']+f'-{i:02d}.png')
   if not target.exists():urllib.request.urlretrieve(url+'?index='+str(i),target)
  print('Saved animation',entry['id'],count[1],flush=True)
  continue
 target=D/(entry['id']+'.bin')
 if not target.exists():urllib.request.urlretrieve(m[1],target)
 if zipfile.is_zipfile(target):
  with zipfile.ZipFile(target) as z:
   names=[n for n in z.namelist() if n.lower().endswith('.png')]
   for i,name in enumerate(names):(D/(entry['id']+f'-{i:02d}.png')).write_bytes(z.read(name))
 else:
  from PIL import Image
  with Image.open(target) as im:im.save(D/(entry['id']+'.png'))
 print('Saved',entry['id'],flush=True)
