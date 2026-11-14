from pathlib import Path
from PIL import Image
import json,numpy as np
W=Path(__file__).parent;O=W.parents[1]/'outputs/helicopter-death';a=json.loads((O/'art.json').read_text());m=json.loads((O/'editable/timeline.json').read_text());checks={}
for group,banks in m.items():
 total=sum(q['count']for q in banks.values())
 for f in [1,total//2,total]:
  name,q=next((k,v)for k,v in banks.items()if v['first']<=f<v['first']+v['count']);v=a['banks'][name][f-q['first']];im=Image.open(W/'candidate/art'/(v['key']+'.png')).convert('RGBA');x,y,w,h=v['rect'];expected=Image.new('RGBA',v['logical']);expected.paste(im.crop((x,y,x+w,y+h)),(v['offset'][0]+v['pivot'][0],v['offset'][1]+v['pivot'][1]));actual=Image.open(W/'roundtrip'/(group+'-'+str(f)+'.png')).convert('RGBA');e=np.array(expected);r=np.array(actual);checks[group+'-'+str(f)]=bool(np.array_equal(e[:,:,3],r[:,:,3])and np.array_equal(e[e[:,:,3]>0],r[r[:,:,3]>0]))
checks['even_source_cells_and_rectangles']=all(all(v%2==0 for v in q['rect']+q['logical'])for rows in a['banks'].values()for q in rows)
checks['uniform_bank_pivot_and_canvas']=all(all((q['logical'],q['pivot'])==(rows[0]['logical'],rows[0]['pivot'])for q in rows)for rows in a['banks'].values())
checks['all_six_hulls_have_complete_yaw_coverage']=all(len(v)==64 for k,v in a['banks'].items()if k.startswith('spin-'))
checks['all_real_pixel_chunks_have_eight_tumble_poses']=all(len(v)==8 for k,v in a['banks'].items()if k.startswith('chunk-'))
checks['explosions_finish_empty']=all(v[-1]['w']==v[-1]['h']==2 for k,v in a['banks'].items()if k.startswith('burst'))
(O/'art-verification.json').write_text(json.dumps({'checks':checks,'frames':sum(map(len,a['banks'].values())),'pages':len(a['pages'])},indent=2));print(json.dumps({'checks':len(checks),'passed':all(checks.values())}));assert all(checks.values())
