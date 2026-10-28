from pathlib import Path
from PIL import Image
from scipy.ndimage import binary_erosion
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';O=W/'armor';O.mkdir(exist_ok=True)
def load_js(name,var):
 s=(R/'assets'/name).read_text();start=s.index('const '+var+'=')+len('const '+var+'=');return json.JSONDecoder().raw_decode(s[start:])[0]
A=load_js('hammer_acting_art_1021.js','HA21_ART');F=load_js('hammer_furious_art_1022.js','HF22_ART');H=load_js('hammer_correction_art_1022.js','H22_ART')
meta={'sheets':{},'banks':{},'owner':'_BUILD_SOURCE/build_hammer_tactical_1023.py','outlinePolicy':'Original alpha and boundary-connected dark linework retained; interior chromium ramp only.'};audit=[]
def chrome(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);hi=rgb.max(2);lo=rgb.min(2);solid=a[:,:,3]>127
 # Preserve the silhouette rim and every dark armor seam. No whitening outlines.
 interior=binary_erosion(solid,iterations=1);m=interior&(hi-lo<34)&(lum>56)&(lum<236)
 levels=np.interp(lum,[0,56,80,110,145,190,236,255],[0,56,105,145,181,222,247,255])
 for c,f in enumerate([.94,.98,1.0]):a[:,:,c][m]=np.clip(levels[m]*f,0,255).astype('uint8')
 a[:,:,3]=np.where(solid,255,0).astype('uint8');return Image.fromarray(a)
for art,label in [(A,'ha'),(F,'hf'),(H,'h22')]:
 for bank,rows in art['banks'].items():
  if not bank.startswith('blue_')or not bank.endswith('_armor'):continue
  base=bank[:-6];original=art['banks'].get(base)
  if not original:continue
  for row in rows:
   src=art['sheets'][original[0]['sheet']];sid=row['sheet']
   if sid in meta['sheets']:continue
   im=Image.open(R/src['path']).convert('RGBA');out=chrome(im);name=label+'_'+bank+'.webp';out.save(O/name,lossless=True,exact=True);meta['sheets'][sid]={'key':art['sheets'][sid]['key'],'path':'assets/game/shared/combat/hammer_tactical_1023/'+name,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()}
   before=np.asarray(im);after=np.asarray(out);solid=before[:,:,3]>127;edge=solid&~binary_erosion(solid);dark=solid&(before[:,:,:3].max(2)<=56)
   audit.append({'bank':bank,'family':label,'size':list(out.size),'sameAlpha':bool(np.array_equal(solid,after[:,:,3]>0)),'edgeDarkKept':bool(np.array_equal(before[:,:,:3][edge],after[:,:,:3][edge])),'darkSeamsPreserved':bool(np.array_equal(before[:,:,:3][dark],after[:,:,:3][dark]))})
# The resting plated actor must use this same coherent metal ramp, not the old white outline.
src=A['sheets'][A['banks']['blue_idle'][0]['sheet']];im=Image.open(R/src['path']).convert('RGBA');out=chrome(im);out.save(O/'plated_idle.webp',lossless=True,exact=True)
meta['platedIdle']={**A['banks']['blue_idle'][0],'key':'ht23_plated_idle','white':'ht23_plated_idle_hit','path':'assets/game/shared/combat/hammer_tactical_1023/plated_idle.webp'}
hit=Image.new('RGBA',out.size,'white');hit.putalpha(out.getchannel('A'));hit.save(O/'plated_idle_hit.webp',lossless=True,exact=True)
meta['audit']=audit;(O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'armorSheets':len(audit),'allAlphaPreserved':all(a['sameAlpha']for a in audit)}))
