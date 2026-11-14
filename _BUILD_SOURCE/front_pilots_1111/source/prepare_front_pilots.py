from pathlib import Path
from PIL import Image,ImageSequence
import json
P=Path(__file__).resolve().parents[1]
Y={'cole':120,'axel':111,'freezer':116,'yuri':119,'maverick':118,'falva':121,'lizzie':121,'decker':119,'juggernaut':106}
LINES={'cole':"Everybody gets home. That's the deal.",'axel':"I'll take point.",'freezer':"Then I'll watch your tail.",'yuri':"I should call my parents.",'maverick':"Try to leave something for the rest of us.",'falva':"We got Granddad's bomber flying.",'lizzie':"Granddad's bomber had air outside it.",'decker':"Ours. You wound half the coils.",'juggernaut':"I've got a song for this."}
jobs=[]
for pk,cy in Y.items():
 folder=P/'portraits'/pk
 raw=Image.open(P/f'masters/{pk}-master.png').convert('RGBA').resize((320,320),Image.Resampling.NEAREST)
 alpha=raw.getchannel('A').point(lambda a:255 if a>=128 else 0)
 native=raw.convert('RGB').quantize(colors=176,method=Image.Quantize.MEDIANCUT).convert('RGBA');native.putalpha(alpha)
 for y in range(320):
  for x in range(320):
   if not native.getpixel((x,y))[3]:native.putpixel((x,y),(0,0,0,0))
 native.save(folder/'native.png');native.save(folder/'0.png')
 frames=[f.convert('RGBA').copy()for f in ImageSequence.Iterator(Image.open(P/f'masters/{pk}-vowels.gif'))]
 assert len(frames)==13 and frames[0].size==(192,192)
 poses=[]
 for i,rawIndex in enumerate([0,1,3,5,7,9,11]):
  f=folder/f'raw-{i}.png';frames[rawIndex].save(f);poses.append(str(f))
 def pose(c):
  c=c.lower()
  if c in 'mbp .,!?:;':return 0
  if c in 'fv':return 5
  if c=='l':return 6
  if c=='u':return 4
  if c=='o':return 3
  if c in 'eiy':return 2
  return 1
 plan=[{'pose':0,'ms':250}]+[{'pose':pose(c),'ms':150 if c in '.!?' else 80 if c!=' ' else 100}for c in LINES[pk]]+[{'pose':0,'ms':650}]
 jobs.append(dict(pilot=pk,native=str(folder/'native.png'),poses=poses,offset=[64,0],mouth=[160,cy+5,28 if pk not in ['falva','lizzie']else 24,17],minY=cy-5,maxY=cy+22,output=str(folder),aseprite=str(P/'portraits'/(pk+'.aseprite')),gif=str(P/'portraits'/(pk+'-front-talking.gif')),line=LINES[pk],plan=plan))
(P/'source/portrait-editor-jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
print('Prepared nine fixed 320px masters and seven mouth poses each.')
