"""Rebuild the campaign-map runtime art from the reviewed, preserved RGBA sources."""
from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/campaign_0930';O=R/'assets/game/campaign_0930'
O.mkdir(parents=True,exist_ok=True)
for name,edge in [('fury_hq',256),('eastern_ruins',1100),('solar_frontier',1024),('solar_curtain_v2',1152),('northern_coast',1600)]:
 im=Image.open(S/(name+'.png')).convert('RGBA');alpha=im.getchannel('A')
 assert alpha.getextrema()[0]==0,(name,'Expected genuine transparency')
 if name not in ('solar_frontier','solar_curtain_v2'):im=im.crop(alpha.getbbox())
 im.thumbnail((edge,edge),Image.Resampling.NEAREST);im.save(O/(name+'.png'))
 print(name,im.size)
# Three existing expansion scenery assets were copied once into this runtime
# folder. Their source paths/provenance are recorded; expansion gameplay stays
# separate and this build never imports its manifest, stages or unlocks.
