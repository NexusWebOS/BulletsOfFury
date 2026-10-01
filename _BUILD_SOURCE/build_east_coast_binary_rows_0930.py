"""Build the East Coast binary-row barrier from its preserved generated art."""
from pathlib import Path
from PIL import Image
import hashlib,json

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/campaign_0930/east_coast_binary_rows_v6.png'
O=R/'assets/game/campaign_0930'
source=Image.open(S).convert('RGBA')
assert source.size==(887,1774),source.size
base=source.resize((512,1024),Image.Resampling.LANCZOS)
sheet=Image.new('RGBA',(2048,1024),(0,0,0,0))
frames=[]
for i,(light,cyan) in enumerate([(0.95,1.00),(1.00,1.02),(1.04,1.08),(0.98,1.01)]):
    r,g,b,a=base.split()
    def lut(factor):return [min(255,round(v*factor)) for v in range(256)]
    frame=Image.merge('RGBA',(r.point(lut(light)),g.point(lut(cyan)),b.point(lut(cyan)),a))
    assert frame.getchannel('A').getextrema()==(0,255)
    sheet.paste(frame,(i*512,0))
    frames.append({'index':i,'rect':[i*512,0,512,1024],
                   'light':light,'cyan':cyan,
                   'sha256':hashlib.sha256(frame.tobytes()).hexdigest()})
assert len({f['sha256'] for f in frames})==4
O.mkdir(parents=True,exist_ok=True)
sheet.save(O/'east_coast_binary_rows_v6.png',optimize=True)
(O/'east_coast_binary_rows_v6.json').write_text(json.dumps({
    'image':'east_coast_binary_rows_v6.png','columns':4,'rows':1,
    'frame_width':512,'frame_height':1024,'fps':3,'count':4,
    'motion':'fixed-position subtle palette flicker of generated binary rows',
    'transparent_edge':True,'frames':frames},indent=2)+'\n',encoding='utf-8')
print('Built four fixed-position binary-row wall frames.')
