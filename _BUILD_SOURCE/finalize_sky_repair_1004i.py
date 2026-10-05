"""Archive actual verification and preserve previous drop notes byte-for-byte."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/sky_repair_1004i'
report=json.loads((O/'checks.json').read_text())
assert all(c['ok'] for c in report['checks']) and not report['errors']
log=(O/'suite.log').read_text();assert 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in log
count=len(re.findall(r'^\s*ok\s',log,re.M));assert count==7177
stealth=(O/'stealth.log').read_text();assert "errors []" in stealth and "PASS []" in stealth
art=json.loads((R/'assets/game/sky_repair_1004i/manifest.json').read_text())
assert all(s['alpha_identical'] and s['max_luminance_rounding_error']<.51 for s in art['sources'])
qa={'date':'2026-10-04','scope':'Stage X password/campaign arenas, consistent blue larger ace and white hits, arcade bomber durability',
    'suite':{'assertions':count,'exit':0,'final_summary':'FALVA/LIZZIE BUILD OK, 0 ERRORS'},
    'native':report,'stealth_regression':{'difficulty':'furious','result':'PASS []','errors':[],'log':'_shots/sky_repair_1004i/stealth.log'},
    'art_manifest':art,'review':'_shots/sky_repair_1004i/review.html',
    'limitations':'Controlled encounters and native pixels, not a full campaign clear or a human balance pass.'}
(R/'docs/qa/sky_repair_1004i.json').write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
note=f'October 4 sky encounter corrections: [Stage X arena, blue ace and arcade bombers](docs/SKY_REPAIR_1004I.md). XHARR/XREBEL and campaign rematches use the authored mountain/water arena; HARR6/REBEL6 retain Stage VI. Current larger giant fighter has twenty blue poses, six matching module plates and exact-alpha white hits; simulation owns part flash expiry. Bombing passes have six HP on every difficulty and can die to one lethal missile. {count:,} full-suite assertions, exit 0; {len(report["checks"])} native Chromium checks and existing Furious stealth-flight regression pass, zero browser errors. Review _shots/sky_repair_1004i/review.html; QA docs/qa/sky_repair_1004i.json. Local only; preserve all earlier work.'
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;b=p.read_bytes()
 if not b.startswith(b'October 4 sky encounter corrections:'):p.write_bytes((note+'\r\n\r\n').encode('utf-8')+b)
print(count,'suite assertions;',len(report['checks']),'native browser checks archived.')
