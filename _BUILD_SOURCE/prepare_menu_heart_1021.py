from pathlib import Path
from PIL import Image
import shutil, json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
G=Path(r'C:/Users/Mike/.codex/generated_images/01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f')
S=R/'_ART_SOURCES/menu_heart_1021'; S.mkdir(parents=True,exist_ok=True)
names={'menu_xl':'415ce3d5-8983-4367-8541-beba97ac20c6','menu_l':'0b1e79a8-88f0-478e-b5d2-d614c573b6d1','menu_m':'7275210d-dbfd-4ab7-a57d-43ebc2d2aff3','menu_s':'e5fdc4c8-ebcc-4e7e-a438-40b305500a89','concept_1':'7cf7a3e7-3a97-49d0-88c0-39f65bf1b804','concept_2':'48633915-d398-4a8b-8eb7-5b507118d927','concept_3':'81293d30-8214-4c92-9c41-6799374ed37f','concept_4':'a80c0743-dc87-409e-b51a-911f5e7f9007','concept_5':'9981dc4f-c291-40d7-9e3d-4640ad661c87','heart_master':'bc3fb4bd-ef35-448f-b599-76b6ff8af86e'}
for n,g in names.items():
 shutil.copy2(G/f'exec-{g}.png',S/f'{n}.png')
 im=Image.open(S/f'{n}.png').convert('RGBA')
 print(n,im.size,im.getchannel('A').getextrema(),im.getbbox())
im=Image.open(S/'heart_master.png').convert('RGBA'); im.thumbnail((212,212),Image.Resampling.NEAREST)
seed=Image.new('RGBA',(256,256));seed.alpha_composite(im,((256-im.width)//2,(256-im.height)//2));seed.save(S/'heart_seed.png')
json.dump({'generator':'built-in image_gen','sources':names,'notes':'UI generated separately for each size and concept; source artwork retained. Animation seed uses uniform scale on fixed256 transparent canvas.'},open(S/'provenance.json','w'),indent=2)
