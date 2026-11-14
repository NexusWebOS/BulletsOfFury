from native import *
import numpy as np
a=json.loads((O/'art.json').read_text());m=json.loads((O/'editable/timeline.json').read_text());checks={};reps=[]
for group,banks in m.items():
 total=sum(b['count']for b in banks.values())
 for f in [1,total//2,total]:
  name,q=next((k,v)for k,v in banks.items()if v['first']<=f<v['first']+v['count']);v=a['banks'][name][f-q['first']];im=Image.open(W/'candidate/art'/(v['key']+'.png')).convert('RGBA');x,y,w,h=v['rect'];expected=Image.new('RGBA',v['logical']);expected.paste(im.crop((x,y,x+w,y+h)),(v['offset'][0]+v['pivot'][0],v['offset'][1]+v['pivot'][1]));actual=Image.open(W/'roundtrip'/(group+'-'+str(f)+'.png')).convert('RGBA');e=np.array(expected);r=np.array(actual);same=bool(np.array_equal(e[:,:,3],r[:,:,3])and np.array_equal(e[e[:,:,3]>0],r[r[:,:,3]>0]));checks[group+'-'+str(f)]=same;reps.append({'group':group,'frame':f,'bank':name,'equal':same})
checks['even_cells_rects_pivots']=all(all(x%2==0 for x in q['logical']+q['rect'])for rows in a['banks'].values()for q in rows)
checks['new_generated_effect_binary_alpha']=all(set(np.unique(np.array(Image.open(W/'candidate/art'/(q['key']+'.png')).convert('RGBA').crop((q['rect'][0],q['rect'][1],q['rect'][0]+q['w'],q['rect'][1]+q['h'])))[:,:,3])).issubset({0,255})for k,rows in a['banks'].items()if k.startswith(('wind','shield'))or k=='bolt'for q in rows)
(O/'art-verification.json').write_text(json.dumps({'checks':checks,'samples':reps,'frames':sum(map(len,a['banks'].values())),'pages':len(a['pages'])},indent=2));print(json.dumps(checks));assert all(checks.values())
