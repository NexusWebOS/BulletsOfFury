from pathlib import Path
import json,math
W=Path(__file__).resolve().parent;d=json.loads((W/'probe/report.json').read_text());p=[e for e in d['events']if e['event']=='throttle-pass'][:16];checks=[]
def ck(n,v):checks.append(dict(name=n,passed=bool(v)));print('PASS'if v else'FAIL',n)
ck('Sixteen true diagonal passes',len(p)==16 and all(abs(e['to']['x']-e['from']['x'])>800 and abs(e['to']['y']-e['from']['y'])>800 for e in p))
ck('Actual speed increases on every pass',all(a['speed']<b['speed']for a,b in zip(p,p[1:])))
ck('Final pass is at least 2.4 times faster',p[-1]['speed']>p[0]['speed']*2.4)
ck('Both lateral and vertical directions are used',{math.copysign(1,e['to']['x']-e['from']['x'])for e in p}=={-1.,1.}and{e['direction']for e in p}=={'north','south'})
ck('Heading matches the committed flight vector',all(abs(e['heading']-math.atan2(e['to']['y']-e['from']['y'],e['to']['x']-e['from']['x']))<1e-8 for e in p))
ck('Every pass enters and exits beyond the complete view',all(min(e['from']['x'],e['to']['x'])<-50 and max(e['from']['x'],e['to']['x'])>700 and min(e['from']['y'],e['to']['y'])<0 and max(e['from']['y'],e['to']['y'])>700 for e in p))
(W/'zigzag-checks.json').write_text(json.dumps(dict(checks=checks,firstSpeed=p[0]['speed'],lastSpeed=p[-1]['speed'],ratio=p[-1]['speed']/p[0]['speed'],passes=p),indent=2));assert all(c['passed']for c in checks)
