from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent; PRIOR=W.parent/'front_hammer_1111'; OLD=W.parent/'heavy_hammer_1111'; E=W/'exports'; O=W.parents[1]/'outputs/Solid-metal-hammers'; C=512
M=json.loads((W/'manifest.json').read_text()); O.mkdir(exist_ok=True)
for move in ['overhead','sides','right']:
 fs=[]; count=M['blue-'+move]['count']; source=E if move=='overhead'else PRIOR/'exports'
 for i in range(count):
  out=Image.new('RGBA',(1024,1056),'#101820'); d=ImageDraw.Draw(out)
  for col,n,title in [(0,'blue','CHRONOS'),(1,'corrupt','DRACODIA')]:
   for row,mat in [(0,'regular'),(1,'chrome')]:
    sheet=Image.open(source/(n+'-'+move+'_'+mat+'.webp')).convert('RGBA'); f=sheet.crop((i%4*C,i//4*C,(i%4+1)*C,(i//4+1)*C)); out.alpha_composite(f,(col*C,32+row*C)); d.text((col*C+12,row*C+12),title+' / '+('CHROMIUM'if row else'NORMAL'),fill='white')
  fs.append(out.convert('RGB'))
 ds=([30]*8+[55]*8+[60,55,45,40,35,30,100,65]+[50]*8)if move=='overhead'else[55]*16
 fs[0].save(O/('all-four-'+move+'.gif'),save_all=True,append_images=fs[1:],duration=ds,loop=0,disposal=2)
 fs[22 if move=='overhead'else 6].save(O/('all-four-'+move+'.png'))
 if move=='overhead':
  for prefix in ['blue','corrupt']:
   board=Image.new('RGBA',(2048,4096),'#101820'); draw=ImageDraw.Draw(board)
   for i in range(32):
    f=Image.open(E/(prefix+'-overhead')/f'{i:02}.png').convert('RGBA'); board.alpha_composite(f,(i%4*C,i//4*C)); draw.text((i%4*C+10,i//4*C+10),str(i),fill='white')
   board.convert('RGB').save(O/(prefix+'-all-poses.png'))
 # Explicitly use alpha compositing above; hidden RGB in transparent pixels is not artwork.
data={}
for n,a in M.items():
 data[n]=dict(count=a['count'],sheets={})
 source=OLD/'exports'if n.endswith('whirl')else E if n.endswith('overhead')else PRIOR/'exports'
 for mat in ['regular','chrome','red']: data[n]['sheets'][mat]='data:image/webp;base64,'+base64.b64encode((source/(n+'_'+mat+'.webp')).read_bytes()).decode()
template=(W/'player-template.html').read_text(encoding='utf8').replace('__DATA__',json.dumps(data,separators=(',',':')))
template=template.replace('Forward-facing hammer attacks','Solid metal hammer attacks').replace('Forward-facing hammer attacks — both forms','Solid metal hammer attacks — all four forms')
template=template.replace('Solid metal hammer attacks — both forms','Solid metal hammer attacks — all four forms')
(O/'playback.html').write_text(template,encoding='utf8')
print('Saved all-four-form GIF, contact comparisons, pose boards and frame player.',flush=True)
