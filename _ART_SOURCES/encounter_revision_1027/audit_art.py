from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
W=Path(__file__).resolve().parent;A=json.loads((W/'compiled/manifest.json').read_text());checks=[];clipped=[]
board=Image.new('RGBA',(1200,840),(10,17,26,255));draw=ImageDraw.Draw(board)
names=['carrier_turret','rook_pod','tank_gun','warden_gun','rearL_fixed','frontL_swat','core','canister','head_rage','head_grin','death_ball','pentagram','tornado','nuke','lightning','code_round']
for name,a in A.items():
 im=Image.open(W/'compiled'/(name+'.png')).convert('RGBA');ok=True
 for f in range(a['frames']):
  x=f%a['cols']*a['cw'];y=f//a['cols']*a['ch'];q=im.crop((x,y,x+a['cw'],y+a['ch']));b=q.getbbox()
  if b and (name.startswith(('herald_','rear','front'))and not name.startswith('head'))and(b[0]==0 or b[1]==0 or b[2]==q.width or b[3]==q.height):clipped.append({'name':name,'frame':f,'bounds':b});ok=False
 checks.append({'name':name,'frames':a['frames'],'fixedEvenCells':a['cw']%2==a['ch']%2==0,'unclipped':ok,'decodedBytes':im.width*im.height*4,'sha256':hashlib.sha256((W/'compiled'/(name+'.png')).read_bytes()).hexdigest()})
for i,name in enumerate(names):
 a=A[name];im=Image.open(W/'compiled'/(name+'.png')).convert('RGBA');f=min(8,a['frames']-1);x=f%a['cols']*a['cw'];y=f//a['cols']*a['ch'];q=im.crop((x,y,x+a['cw'],y+a['ch']));q.thumbnail((220,160),Image.Resampling.NEAREST);px=i%4*300;py=i//4*210;board.alpha_composite(q,(px+(300-q.width)//2,py+20+(160-q.height)//2));draw.text((px+16,py+185),name,fill='white')
board.save(W/'authored-banks-preview.png');report={'banks':checks,'clippedFrames':clipped,'totalDecodedMiB':sum(q['decodedBytes']for q in checks)/1024**2,'sourceHashes':{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (W/'source').glob('*.png')}}
(W/'art-audit.json').write_text(json.dumps(report,indent=2));print('Banks',len(A),'clipped component frames',len(clipped),'decoded MiB',round(report['totalDecodedMiB'],1))
