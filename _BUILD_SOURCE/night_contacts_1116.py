from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116'
for folder in [O/'native-boss/stage8',O/'native-sweep/stage7']:
 if not(folder/'report.json').exists():continue
 d=json.loads((folder/'report.json').read_text());seen=set();files=[]
 for i,q in enumerate(d['timeline'],1):
  tag=(q.get('mode'),q.get('phase'),q.get('form'))
  f=folder/('phase-%05d.png'%i)
  if f.exists()and tag not in seen:seen.add(tag);files.append((f,str(round(q['seconds'],1))+'s '+str(tag)))
 for start in range(0,len(files),12):
  batch=files[start:start+12];sheet=Image.new('RGB',(1280,((len(batch)+2)//3)*290),(5,10,17));dr=ImageDraw.Draw(sheet)
  for j,(p,caption)in enumerate(batch):
   im=Image.open(p).convert('RGB');im.thumbnail((426,266));x=j%3*426;y=j//3*290;sheet.paste(im,(x,y));dr.text((x+3,y+268),caption,fill='white')
  sheet.save(folder/('contact-%02d.jpg'%(start//12)))
 print(folder.name,'unique actual phase frames',len(files))
