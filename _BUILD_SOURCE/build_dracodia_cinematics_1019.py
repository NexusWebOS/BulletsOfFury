from pathlib import Path
from PIL import Image,ImageOps
import json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_demon_1019/cinematics';D=R/'assets/game/shared/cinematics/dracodia_demon_1019';D.mkdir(parents=True,exist_ok=True)
for name in ['emergence','contact']:
 im=Image.open(S/(name+'.png')).convert('RGB');out=ImageOps.fit(im,(960,540),Image.Resampling.LANCZOS);out.save(D/(name+'.webp'),quality=92,method=6)
(S/'provenance.json').write_text(json.dumps({'generator':'built-in GPT imagegen','referenceIdentity':'_ART_SOURCES/stage8_pixellab_1018/masters/colossus.png','composition':'authored orbital emergence and first contact; no aircraft','frames':['emergence.png','contact.png'],'shippingCanvas':[960,540],'palette':'charcoal chromium, purple, white','prompt':'Remake the orbital symbiote emergence and first-contact scenes as a demonic artificial intelligence parasite with Dracodia skull, metallic wire tendrils, chromium armor and violet circuit corruption entering the satellite; Earth below, purple rift, sharp mid90s arcade pixel illustration. No text or aircraft.'},indent=2))
