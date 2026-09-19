from pathlib import Path
from PIL import Image
D=Path('assets/game/pilot_portraits')
S=Image.open(D/'yuri_expression_sheet_0919.png').convert('RGBA')
F=Image.open(D/'axel-idle.png').convert('RGBA')
N=['idle','anger','crash','happy','laugh','sad','victory','talk-closed','talk-small','talk-medium','talk-o','talk-wide']
assert S.size==(1448,1086) and F.size==(256,256)
for i,n in enumerate(N):
 x=(i%4)*362;y=(i//4)*362
 tile=S.crop((x,y,x+362,y+362)).resize((240,240),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(256,256),(7,11,19,255));out.alpha_composite(tile,(8,8))
 for box in [(0,0,256,17),(0,239,256,256),(0,17,17,239),(239,17,256,239)]:out.paste(F.crop(box),box[:2])
 out.save(D/('yuri-'+n+'.png'))
