from pathlib import Path
from PIL import Image
import numpy as np,json,urllib.request,uuid,sys
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');A=R/'_ART_SOURCES/instructor_bob_1020'
im=Image.open(A/'returned/bob.png').convert('RGBA');a=np.array(im);blue=(a[:,:,2]>170)&(a[:,:,1]>140)&(a[:,:,0]<125)&(a[:,:,3]>128);yy,xx=np.nonzero(blue);core=[round(float(xx.mean()),2),round(float(yy.mean()),2)]
rows={}
for name,x0,x1 in [('missile',0,76),('core',76,190),('cannon',190,256)]:
 part=Image.new('RGBA',(256,256));part.paste(im.crop((x0,0,x1,256)),(x0,0));part.save(A/'parts'/(name+'-live.png'));box=part.getbbox();center=core if name=='core' else [(box[0]+box[2])/2,(box[1]+box[3])/2]
 crop=part.crop(box);view=Image.new('RGBA',(192,192));view.paste(crop,(96-crop.width//2,96-crop.height//2));view.save(A/'parts'/(name+'-view.png'))
 rows[name]={'bounds':list(box),'target':center,'live_canvas':[256,256],'view_canvas':[192,192]}
(A/'parts/geometry.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
urls={}
for name in ['whole','missile','core','cannon']:
 p=A/'returned/bob.png' if name=='whole' else A/'parts'/(name+'-view.png')
 boundary='bof-'+uuid.uuid4().hex
 body=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="'+p.name+'"\r\nContent-Type: image/png\r\n\r\n').encode()+p.read_bytes()+('\r\n--'+boundary+'--\r\n').encode()
 request=urllib.request.Request(sys.argv[1],data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary},method='POST')
 with urllib.request.urlopen(request,timeout=120) as response:urls[name]=json.load(response)['ref']
(A/'parts/upload-refs.json').write_text(json.dumps(urls,indent=2),encoding='utf-8');print(json.dumps({'geometry':rows,'uploads':urls}))
