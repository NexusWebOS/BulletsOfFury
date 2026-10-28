from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageOps
import json,hashlib
W=Path(__file__).parent/'BOF-Cinema-Rebuild';D=W/'consistency_1021'
plans=json.loads((D/'palette-decisions.json').read_text(encoding='utf-8'))
integration=json.loads((D/'integration-report.json').read_text(encoding='utf-8'));byname={r['shot']:r for r in integration}
checks=[]
def ck(name,value):
 checks.append({'name':name,'ok':bool(value)});print(('PASS ' if value else 'FAIL ')+name)
 assert value,name
for name,plan in plans.items():
 before=Image.open(D/(name+'-before.png')).convert('RGBA');after=Image.open(W/'returned'/(name+'.png')).convert('RGBA')
 mask=Image.new('1',before.size)
 for op in plan['changes']:
  if op['operation']=='select_mask' and op['selector']['kind']=='polygon':ImageDraw.Draw(mask).polygon(op['selector']['points'],fill=1)
 for field in ['head','maverick_head']:
  h=byname[name].get(field)
  if not h:continue
  im=Image.open((W/'likeness_correction' if h['source'].startswith('cole-new') else D)/h['source']).convert('RGBA')
  if h.get('mirrored'):im=ImageOps.mirror(im)
  size=tuple(int(v*h['scale']) for v in im.size)
  im=im.resize(size,Image.Resampling.NEAREST);alpha=im.getchannel('A').point(lambda v:255 if v else 0)
  mask.paste(1,h['at'],alpha)
 diff=ImageChops.difference(before.convert('RGB'),after.convert('RGB'))
 outside=[px for px,m in zip(diff.get_flattened_data(),mask.get_flattened_data()) if not m]
 ck(name+' edits confined to authored actor selections',all(px==(0,0,0) for px in outside))
 ck(name+' original canvas and alpha preserved',before.size==after.size==(688,384) and before.getchannel('A').tobytes()==after.getchannel('A').tobytes())
 palette=Image.open(D/(name+'-palette.png')).convert('RGB');source=before.convert('RGB')
 lumaerrors=[]
 for old,new in zip(source.get_flattened_data(),palette.get_flattened_data()):
  if old!=new:lumaerrors.append(abs(sum(v*w for v,w in zip(old,(.2126,.7152,.0722)))-sum(v*w for v,w in zip(new,(.2126,.7152,.0722)))))
 ck(name+' palette shading luminance retained',max(lumaerrors or [0])<=.51)
for name,box,min_added in [('hq_regroup',(326,143,375,205),300),('hq_river',(195,193,226,225),100)]:
 count=lambda p:sum(b>r>g for r,g,b in Image.open(p).convert('RGB').crop(box).get_flattened_data())
 ck(name+' Freezer purple jacket replaces navy ramp',count(W/'returned'/(name+'.png'))-count(D/(name+'-before.png'))>min_added)
before={a['name']:a for a in json.loads((D/'before-export-audit.json').read_text(encoding='utf-8'))}
after={a['name']:a for a in json.loads((W/'export-audit.json').read_text(encoding='utf-8'))}
for name in ['data_disintegrate','data_blast','blue_portal','void_portal','remnant','code_fragments','hq_motion','coast_motion','forge_motion']:
 ck(name+' complete animation bank byte-identical',before[name+'.webp']['sha256']==after[name+'.webp']['sha256'])
ck('only six prior runtime exports changed',{n for n in before if before[n]['sha256']!=after[n]['sha256']}=={n+'.webp' for n in plans})
for name in ['maverick_report_pose','maverick_horror_pose','maverick_standing_pose']:
 r=byname[name];old=Image.open(D/('audit-native-'+r['native_key']+'.png')).convert('RGBA');new=Image.open(W/'returned'/(name+'.png')).convert('RGBA')
 box=r['eye_region'];mask=Image.new('1',old.size);ImageDraw.Draw(mask).rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=1)
 diff=ImageChops.difference(old,new).convert('RGB')
 ck(name+' original expression/body outside sunglasses unchanged',all(c==(0,0,0) for c,m in zip(diff.get_flattened_data(),mask.get_flattened_data()) if not m))
(D/'export-verification.json').write_text(json.dumps({'checks':checks},indent=2),encoding='utf-8')
print('ALL',len(checks),'EXPORT CHECKS PASSED')
