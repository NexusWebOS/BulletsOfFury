from pathlib import Path
from PIL import Image,ImageOps,ImageChops,ImageDraw
import json,hashlib,shutil
W=Path(__file__).resolve().parents[1]/'_ART_SOURCES/cinema_story_1021' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Cinema-Rebuild'
D=W/'consistency_1021';H=W/'likeness_correction';report=[]
heads={
 'forge_upgrade':('cole-new-head-0.png',H,0.625,(63,130),False),
 'hq_alarm':('cole-new-head-0.png',H,0.375,(197,142),False),
 'launch_generator':('cole-new-head-2.png',H,0.375,(160,55),False),
 'hq_river':('cole-rear-1.png',D,0.875,(66,133),False),
 'power_cell':('cole-rear-1.png',D,0.5,(516,185),True)
}
maverick_heads={'hq_regroup':(0.625,(198,117)),'hq_alarm':(0.25,(412,155)),'hq_river':(0.375,(536,168))}
names=['hq_regroup','forge_upgrade','hq_alarm','hq_river','launch_generator','power_cell']
contact=Image.new('RGB',(1376,1242),'#0a0e15');g=ImageDraw.Draw(contact)
for i,name in enumerate(names):
 before=Image.open(D/(name+'-before.png')).convert('RGBA')
 im=Image.open(D/(name+'-palette.png')).convert('RGBA')
 assert before.size==im.size==(688,384)
 if name in heads:
  file,folder,scale,at,mirror=heads[name];head=Image.open(folder/file).convert('RGBA')
  if mirror:head=ImageOps.mirror(head)
  size=tuple(int(n*scale) for n in head.size)
  assert all(n%2==0 for n in size) and size[0]/head.width==size[1]/head.height
  head=head.resize(size,Image.Resampling.NEAREST);im.alpha_composite(head,at)
 if name in maverick_heads:
  scale,at=maverick_heads[name];head=Image.open(D/'maverick-head-0.png').convert('RGBA')
  size=tuple(int(n*scale) for n in head.size)
  assert all(n%2==0 for n in size) and size[0]/head.width==size[1]/head.height
  im.alpha_composite(head.resize(size,Image.Resampling.NEAREST),at)
 target=W/'returned'/(name+'.png');im.save(target);im.save(D/(name+'-after.png'))
 diff=ImageChops.difference(before.convert('RGB'),im.convert('RGB'))
 report.append({'shot':name,'size':im.size,'changed_bbox':diff.getbbox(),
  'changed_pixels':sum(x!=(0,0,0) for x in diff.get_flattened_data()),
  'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
  'head':{'source':heads[name][0],'scale':heads[name][2],'at':heads[name][3],'mirrored':heads[name][4]} if name in heads else None,
  'maverick_head':{'source':'maverick-head-0.png','scale':maverick_heads[name][0],'at':maverick_heads[name][1]} if name in maverick_heads else None})
 contact.paste(im.convert('RGB'),((i%2)*688,(i//2)*414));g.text(((i%2)*688+4,(i//2)*414+386),name,fill='white')
 # Existing scene-motion patches do not include any corrected actor.
 if name=='hq_regroup':assert im.crop((432,80,688,336)).tobytes()==before.crop((432,80,688,336)).tobytes()
 if name=='forge_upgrade':assert im.crop((220,210,476,354)).tobytes()==before.crop((220,210,476,354)).tobytes()
contact.save(D/'final-contact.png')
# Preserve the original report / alarm expressions and body geometry; carry over
# only the authored sunglasses region from the three-frame PixelLab repair.
legacy=[('inv20_maverick','maverick_report_pose',(20,45,108,84)),
 ('inv20_maverick_horror','maverick_horror_pose',(20,45,108,84)),
 ('pose_maverick_0','maverick_standing_pose',(40,20,88,46))]
for i,(key,name,box) in enumerate(legacy):
 before=Image.open(D/('audit-native-'+key+'.png')).convert('RGBA')
 im=before.copy();patch=Image.open(D/('maverick-legacy-edit-'+str(i)+'.png')).convert('RGBA')
 im.paste(patch.crop(box),(80+box[0],box[1]))
 assert im.size==before.size and all(n%2==0 for n in im.size)
 assert im.crop((0,84,im.width,im.height)).tobytes()==before.crop((0,84,im.width,im.height)).tobytes()
 im.save(W/'returned'/(name+'.png'));im.save(D/(name+'-after.png'))
 report.append({'shot':name,'native_key':key,'size':im.size,'eye_region':[80+box[0],box[1],80+box[2],box[3]],'original_body_and_mouth_preserved':True})
(D/'integration-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
