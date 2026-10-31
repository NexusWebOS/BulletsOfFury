from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
import numpy as np,json,os,shutil,subprocess
W=Path(__file__).resolve().parent;R=W.parents[1];D=W/'compiled';D.mkdir(exist_ok=True);A={}
rects=[(168,86,18,32),(200,76,22,36),(290,76,22,36),(326,86,18,32)];pivots=[(177,103),(211,94),(301,94),(335,103)]
poses=[]
for i in range(4):
 q=Image.open(R/'_ART_SOURCES/harrier_turrets_1027'/f'coloured-source-{0 if i<2 else 1}.png').convert('RGBA');p=Image.new('RGBA',(32,40));p.alpha_composite(q,(5,2));poses.append(p)
for name in ['closed','open','broken','closed_wells','open_wells','broken_wells']:
 source=R/'assets/game/levels/stage_06/boss/bosses/skycarrier'/('carrier_'+name+'.png');im=Image.open(source).convert('RGBA');raw=np.array(im);erase=np.zeros(raw.shape[:2],dtype=bool)
 for x,y,w,h in rects:erase[y:y+h,x:x+w]=True
 _,indices=distance_transform_edt(erase,return_indices=True);raw[erase]=raw[indices[0][erase],indices[1][erase]];clean=Image.fromarray(raw)
 for direction in ['south','north']if not name.endswith('wells')else['south']:
  c=clean.copy()
  for p,(x,y)in zip(poses,pivots):c.alpha_composite(p if direction=='south'else p.transpose(Image.Transpose.ROTATE_180),(x-16,y-20))
  key=name+'_'+direction;c.save(D/(key+'.png'),optimize=True);A[key]={'key':'hf28_'+key,'path':f'assets/game/levels/stage_06/boss/harrier_facing_1027/{key}.png','w':c.width,'h':c.height,'pivot':[c.width//2,c.height//2],'source':str(source.relative_to(R))}
for i,p in enumerate(poses):
 c=Image.new('RGBA',p.size,(255,255,255,0));c.putalpha(p.getchannel('A'));key=f'hit_{i}';c.save(D/(key+'.png'));A[key]={'key':'hf28_'+key,'path':f'assets/game/levels/stage_06/boss/harrier_facing_1027/{key}.png','w':32,'h':40,'pivot':[16,20]}
(W/'harrier_facing_art_1027.js').write_text('"use strict";\nconst HF28_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8');(D/'manifest.json').write_text(json.dumps({'art':A,'oldRects':rects,'pivots':pivots},indent=2),encoding='utf-8')
board=Image.new('RGBA',(1024,576),(16,27,38,255));g=ImageDraw.Draw(board)
for i,name in enumerate(['closed_south','open_south','closed_wells_south','closed_north']):board.alpha_composite(Image.open(D/(name+'.png')),(i%2*512,i//2*288));g.text((i%2*512+8,i//2*288+8),name,fill='white')
board.save(W/'whole-hull-frames.png');print('Authored9 complete hull variants and4 matching south-facing hit masks; originals preserved.')

for name,a in A.items():
 target=R/a['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/(name+'.png'),target)
shutil.copy2(W/'harrier_facing_art_1027.js',R/'assets/harrier_facing_art_1027.js')
ase=os.environ.get('ASEPRITE_EXE')or shutil.which('aseprite')
if ase:subprocess.run([ase,'--batch',str(D/'closed_wells_south.png'),'--save-as',str(W/'harrier-south.aseprite')],check=True,capture_output=True)
