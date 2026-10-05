"""Record successful checks without rewriting previous handoff history."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_stagex_1004g'
report=json.loads((O/'checks.json').read_text());log=(R/'_shots/campaign_stagex_1004g_suite.log').read_text()
assert all(c['ok'] for c in report['checks']) and not report['errors']
assert 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in log
count=len(re.findall(r'^\s*ok\s',log,re.M))
q={'date':'2026-10-04','scope':'Floating central Stage X city island; shared flag/orbit/pointer pose and focused camera','suite':{'assertions':count,'exit':0,'final_summary':'FALVA/LIZZIE BUILD OK, 0 ERRORS'},'native':report,'review':'_shots/campaign_stagex_1004g/review.html','art':'assets/game/campaign_stagex_1004g/region_hub.png','prompt':'_ART_SOURCES/campaign_stagex_1004g/prompt.json','limitations':'Campaign map and both route launches verified; no combat balance or full campaign-clear claim.'}
(R/'docs/qa/campaign_stagex_1004g.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
note=f'October 4 floating Stage X correction: [Central floating city island](docs/CAMPAIGN_STAGEX_1004G.md). Generated deep rock underside, permanent elevation, ground shadow and hover/bob. City, X flag, whole-island pointer and both encounter orbits share one pose. Camera exposes the complete skyline; locked briefing no longer resets its letters. Locked viewing grants no fight; earned Harrier and five-Rebel launches preserved. {count:,} full-suite assertions, exit 0; {len(report["checks"])} native/review checks, zero browser errors. Review _shots/campaign_stagex_1004g/review.html; QA docs/qa/campaign_stagex_1004g.json. Local only; preserve all earlier work.'
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;b=p.read_bytes()
 if not b.startswith(b'October 4 floating Stage X correction:'):p.write_bytes((note+'\r\n\r\n').encode('utf-8')+b)
print(count,'suite assertions;',len(report['checks']),'browser checks archived.')
