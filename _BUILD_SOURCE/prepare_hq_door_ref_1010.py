from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
im=Image.open(ROOT/'_ART_SOURCES/hq_landing_1010/background_raw.png')
W,H=im.size;front=im.crop((0,round(H/2),round(W/2),H))
front.crop((round(front.width*.415),round(front.height*.37),round(front.width*.585),round(front.height*.59))).save(ROOT/'_ART_SOURCES/hq_landing_1010/references/entrance.png')
