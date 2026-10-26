"""Palette-only derivatives of approved whole plates. Fixed even cells/pivots."""
from pathlib import Path
import json, copy
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
P=R/'assets/game/shared/combat/chronos_motion_1025/manifest.json'
a=json.loads(P.read_text())
for name,bank in list(a['banks'].items()):
 if not (name.endswith('_chrome') or name=='activation'):continue
 new=name.replace('_chrome','_red') if name!='activation' else 'rage_charge'
 source=R/a['sheets'][name]['path'];im=Image.open(source).convert('RGBA');v=np.array(im);rgb=v[:,:,:3].astype(float)
 hi=rgb.max(2);lo=rgb.min(2);lum=rgb@np.array([.2126,.7152,.0722]);sat=hi-lo
 # Preserve black outlines and white metallic highlights. Authored saturated
 # energy and midtone steel become crimson, without altering any silhouettes.
 warm=(rgb[:,:,0]>rgb[:,:,2]*1.3)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(sat>25)
 amount=np.where(warm,1,np.where(sat>25,0,.72)*np.clip((245-hi)/65,0,1))*np.clip((lum-12)/30,0,1)
 red=np.stack([np.minimum(255,np.maximum(hi,lum*1.8)),lum*.22,lum*.28],2)
 v[:,:,:3]=np.clip(rgb*(1-amount[:,:,None])+red*amount[:,:,None],0,255).astype('uint8')
 dest=source.with_name(new+'.webp');Image.fromarray(v).save(dest,lossless=True)
 a['sheets'][new]={'key':'nca_c27_'+new,'path':dest.relative_to(R).as_posix()}
 a['sheets'][new+'_hit']={**a['sheets'][name+'_hit'],'key':'nca_c27_'+new+'_hit'}
 b=copy.deepcopy(bank);b['sheet']='c27_'+new;a['banks'][new]=b
P.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8')
(R/'assets/chronos_motion_art_1025.js').write_text('"use strict";\nconst C27_ART='+json.dumps(a,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Registered',len(a['banks']),'whole-plate banks')
