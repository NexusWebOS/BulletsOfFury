from pathlib import Path
from PIL import Image
import json,sys,uuid,urllib.request
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');A=R/'_ART_SOURCES/performance_finish_1020';A.mkdir(exist_ok=True,parents=True);(A/'refs').mkdir(exist_ok=True)
rows={}
for pose in ['report','horror']:
 p=R/'assets/game/pilots/cole/body_frames/front_identity_1020'/('cole-'+pose+'.webp');im=Image.open(p).convert('RGBA');assert im.size==(512,1024)
 im.save(A/'refs'/('cole-'+pose+'-original.png'))
 for name,region,size in [('face',(160,0,352,192),(192,192)),('gesture',(0,0,512,512),(256,256))]:
  out=im.crop(region).resize(size,Image.Resampling.NEAREST);q=A/'refs'/('cole_'+pose+'_'+name+'.png');out.save(q)
  rows['cole_'+pose+'_'+name]={'path':str(q),'canvas':size,'source_region':region,'source_size':im.size}
for name,row in rows.items():
 p=Path(row['path']);boundary='bof-'+uuid.uuid4().hex;body=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="'+p.name+'"\r\nContent-Type: image/png\r\n\r\n').encode()+p.read_bytes()+('\r\n--'+boundary+'--\r\n').encode()
 req=urllib.request.Request(sys.argv[1],data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary},method='POST')
 with urllib.request.urlopen(req,timeout=120) as resp:row['ref']=json.load(resp)['ref']
(A/'references.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows))
