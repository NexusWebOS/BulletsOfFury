from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib, shutil

W=Path(__file__).resolve().parents[1]/'_ART_SOURCES/cinema_story_1021' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Cinema-Rebuild'
D=W/'likeness_correction'
target=W/'returned/hq_regroup.png'
original=D/'hq-regroup-before.png'
if not original.exists(): shutil.copy2(target,original)
base=Image.open(original).convert('RGBA')
crop=base.crop((40,96,296,352))
cole=Image.open(D/'cole-edit.png').convert('RGBA')
maverick=Image.open(D/'maverick-edit.png').convert('RGBA')
head=Image.open(D/'cole-head-edit.png').convert('RGBA')
assert cole.size==maverick.size==(256,256) and head.size==(80,96)
# Extract only each authored actor; all surrounding characters remain original.
mask=Image.new('L',(256,256));g=ImageDraw.Draw(mask)
g.polygon([(84,27),(108,27),(115,40),(115,61),(126,82),(130,98),
 (153,102),(153,121),(123,125),(113,146),(120,184),(114,213),
 (120,233),(139,240),(140,249),(106,251),(87,246),(90,211),
 (77,210),(70,226),(68,239),(75,243),(75,251),(51,251),
 (53,224),(55,206),(60,169),(61,144),(43,135),(44,126),
 (35,122),(30,106),(33,83),(44,66),(63,56),(79,53)],fill=255)
crop.paste(cole,(0,0),mask)
mask=Image.new('L',(80,96));ImageDraw.Draw(mask).polygon(
 [(15,7),(56,5),(59,28),(54,48),(47,59),(24,57),(18,45),(12,27)],fill=255)
crop.paste(head,(60,16),mask)
mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon(
 [(169,20),(207,20),(213,52),(223,73),(224,105),(211,111),
 (204,132),(180,127),(163,107),(147,93),(145,59),(158,46)],fill=255)
crop.paste(maverick,(0,0),mask)
# Selected authored candidate 0: one proportional 5/8 scale, stable placement.
new_head=Image.open(D/'cole-new-head-0.png').convert('RGBA').resize((60,70),Image.Resampling.NEAREST)
crop.alpha_composite(new_head,(66,20))
base.paste(crop,(40,96))
assert base.size==(688,384)
before=Image.open(original).convert('RGBA')
assert base.crop((296,0,688,384)).tobytes()==before.crop((296,0,688,384)).tobytes()
assert base.crop((432,80,688,336)).tobytes()==before.crop((432,80,688,336)).tobytes()
base.save(target)
base.resize((1376,768),Image.Resampling.NEAREST).save(D/'hq-regroup-after-zoom.png')
rgbdiff=ImageChops.difference(base.convert('RGB'),before.convert('RGB'))
report={'source_size':base.size,'changed_bbox':rgbdiff.getbbox(),
 'changed_pixels':sum(v!=(0,0,0) for v in rgbdiff.getdata()),
 'right_side_and_hq_motion_patch_pixel_identical':True,
 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'cole_head_candidate':0,'head_scale':0.625,'head_placement':[106,116],
 'jobs':['a2a3270d-6327-446a-8cb9-fdc82e32cc46','aa9111df-b328-4125-a510-575777e9e5d5','fb303c66-9460-464b-89a5-4b0af7243a41','3898463d-a4c9-4412-adac-2f78cdc37c72']}
(D/'integration-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
