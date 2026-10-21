from pathlib import Path
from PIL import Image
import urllib.request,json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_phoenix_1020';D=S/'beam-motion-clean';D.mkdir(exist_ok=True)
job='344bdb15-4628-4260-8190-438a67737b3f';p=S/'beam-clean-sheet.png'
if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/pixel-tools/{job}/assets/south/full.png',timeout=90).read())
sheet=Image.open(p).convert('RGBA');assert sheet.size==(256,512)
for i in range(16):
 im=sheet.crop((i%4*64,i//4*128,i%4*64+64,i//4*128+128));im.save(D/f'{i+1:02}.png',optimize=True)
 if i==0:
  old=S/'beam-rejected-feather.png'
  if not old.exists():old.write_bytes((S/'beam.png').read_bytes())
  im.save(S/'beam.png',optimize=True)
(S/'beam-clean-provenance.json').write_text(json.dumps(dict(sourceEdit='76edd3fb-baae-4a18-a4f0-34131edbd8ea',drawing=job,frame=[64,128],frames=16,commonCrop=[20,0,44,127],rejected='Arrowhead and large spike texture was visually too coarse when enlarged; replaced by a continuous plasma column.'),indent=2)+'\n');print('Clean continuous PixelLab beam installed')
