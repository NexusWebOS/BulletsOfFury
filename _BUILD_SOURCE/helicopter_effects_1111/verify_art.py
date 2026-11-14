from pathlib import Path
from PIL import Image
import json,numpy as np
W=Path(__file__).parent;O=W.parents[1]/'outputs/dracodia-helicopter';a=json.loads((O/'art.json').read_text());m=json.loads((O/'editable/timeline.json').read_text());checks={}
for name,mapping in m.items():
 total=len(mapping['native'])
 for f in [1,total//2,total]:
  q=a['banks'][name][mapping['native'][f-1]-1];im=Image.open(W/'candidate/art'/(q['key']+'.png')).convert('RGBA');x,y,w,h=q['rect'];expected=Image.new('RGBA',q['logical']);expected.paste(im.crop((x,y,x+w,y+h)),(q['offset'][0]+q['pivot'][0],q['offset'][1]+q['pivot'][1]));actual=Image.open(W/'roundtrip'/(name+'-'+str(f)+'.png')).convert('RGBA');e=np.array(expected);r=np.array(actual);checks[name+'-'+str(f)]=bool(np.array_equal(e[:,:,3],r[:,:,3])and np.array_equal(e[e[:,:,3]>0],r[r[:,:,3]>0]))
checks['all_cells_rectangles_even']=all(all(v%2==0 for v in q['logical']+q['rect'])for rows in a['banks'].values()for q in rows)
checks['uniform_bank_canvas_and_pivot']=all(all((q['logical'],q['pivot'])==(rows[0]['logical'],rows[0]['pivot'])for q in rows)for rows in a['banks'].values())
checks['binary_alpha']=all(set(np.unique(np.array(Image.open(p).convert('RGBA'))[:,:,3])).issubset({0,255})for p in(W/'candidate/art').glob('*.png'))
checks['complete_direction_coverage']=all(len(a['banks'][n])==8*64 for n in ['muzzle','launch','tracer','missile'])
checks['finite_explosion_empty_end_frames']=all(a['banks'][n][-1]['w']==2 and a['banks'][n][-1]['h']==2 for n in ['burst72','burst112','burst160'])
(O/'art-verification.json').write_text(json.dumps({'checks':checks,'frames':sum(map(len,a['banks'].values())),'pages':len(a['pages'])},indent=2));print(json.dumps(checks));assert all(checks.values())
