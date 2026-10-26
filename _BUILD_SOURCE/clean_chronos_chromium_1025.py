"""Palette-only chromium from clean regular plates; preserve alpha/outline/blue weapon."""
from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[1]
def chrome(im):
 a=np.array(im.convert('RGBA'));v=a[:,:,:3].astype(float);lum=v@np.array([.2126,.7152,.0722]);neutral=v.max(2)-v.min(2)<24;inside=distance_transform_edt(a[:,:,3]>0)>2
 m=neutral&inside&(lum>65)&(lum<220);z=np.minimum(235,lum*1.18+8);target=np.stack([z*.96,z*.99,z],2);mix=m*.55;a[:,:,:3]=np.clip(v*(1-mix[:,:,None])+target*mix[:,:,None],0,255).astype('uint8');return Image.fromarray(a)
def load(name):
 s=(R/name).read_text(encoding='utf8');return json.loads(s[s.index('{'):s.rindex('}')+1])
a=load('assets/hammer_correction_art_1022.js')
for k,v in a['sheets'].items():
 if k.startswith('h22_blue_') and k.endswith('_armor'):
  src=a['sheets'][k[:-6]];chrome(Image.open(R/src['path'])).save(R/v['path'],lossless=True)
a=load('assets/chronos_motion_art_1025.js')
for k,v in a['sheets'].items():
 if k.endswith('_chrome') and k[:-7]+'_regular' in a['sheets']:chrome(Image.open(R/a['sheets'][k[:-7]+'_regular']['path'])).save(R/v['path'],lossless=True)
a=load('assets/chronos_commitment_art_1025.js')
for k,v in a['sheets'].items():
 if k.endswith('_chrome') and k[:-7]+'_regular' in a['sheets']:chrome(Image.open(R/a['sheets'][k[:-7]+'_regular']['path'])).save(R/v['path'],lossless=True)
print('Chromium plates rebuilt: identical alpha, protected outer2px and saturated weapon colors')
