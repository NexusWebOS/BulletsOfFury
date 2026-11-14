from pathlib import Path
from PIL import Image
import json
W=Path(__file__).parent;O=W.parents[1]/'outputs/dam-impact';a=json.loads((O/'art.json').read_text());checks={}
for f in [1,9,17,25,33]:
 q=a['frames'][f-1];im=Image.open(W/'roundtrip'/('flash-'+str(f)+'.png')).convert('RGBA');expected=q['alpha'];alpha=im.getchannel('A').getextrema();rgb=im.convert('RGB').getextrema();checks['aseprite_exact_flash_'+str(f)]=alpha==(expected,expected)and(expected==0 or rgb==((255,255),(255,255),(255,255)))
checks['all_frame_cells_even_and_native_size']=all(q['rect'][2:]==[480,512]and all(n%2==0 for n in q['rect'])for q in a['frames']);checks['monotonic_alpha_with_empty_and_white_endpoints']=a['frames'][0]['alpha']==0 and a['frames'][-1]['alpha']==255 and all(b['alpha']>c['alpha']for c,b in zip(a['frames'],a['frames'][1:]));(O/'art-verification.json').write_text(json.dumps({'checks':checks},indent=2));print(json.dumps(checks));assert all(checks.values())
