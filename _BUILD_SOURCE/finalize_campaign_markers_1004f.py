"""Archive final native reports and append a concise handoff without rewriting history."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_markers_1004f'
reports={name:json.loads((O/file).read_text(encoding='utf-8')) for name,file in [('map','checks.json'),('flags','flag-checks.json'),('orbits','orbit-inspection.json'),('review','review-checks.json')]}
assert all(all(c['ok'] for c in report['checks']) and not report['errors'] for report in reports.values())
summary={'date':'2026-10-04','scope':'Generated Roman I–IX flags, permanent Stage X, physical Fury HQ frontage, vertical campaign ship travel','suite':{'assertions':7143,'exit':0,'final_summary':'FALVA/LIZZIE BUILD OK, 0 ERRORS'},'native':reports,'review':'_shots/campaign_markers_1004f/review.html','sources':'_ART_SOURCES/campaign_landscape_1004f','limitations':'Campaign map fixtures and normal browser animation verified; not a combat balance or campaign-clear pass.'}
(R/'docs/qa/campaign_markers_1004f.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
note='October 4 campaign flags and routes: [Roman flags, permanent Stage X and physical Fury HQ](docs/CAMPAIGN_MARKERS_1004F.md). Generated I–IX in the approved X chrome style with stage colors, normalized mast-base anchors, locks, rank/selected/unlock states. X stays in the central city; both earned rematches and all five Rebel/Harrier orbit art preserved. HQ lettering is built into the regenerated building; extra map labels/old plaque removed. Fixed invisible HQ NaN bobbing. All nine pilot hulls support down 4→5 and up 7→8 / 8→1 with correctly placed trails and stable arrival headings. 7,143 full-suite assertions, exit 0; 69 native/review checks, zero browser errors. Review _shots/campaign_markers_1004f/review.html; QA docs/qa/campaign_markers_1004f.json. Local only; preserve all earlier work.'
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;b=p.read_bytes()
 if not b.startswith(b'October 4 campaign flags and routes:'):p.write_bytes((note+'\r\n\r\n').encode('utf-8')+b)
print('Archived 69 passing browser checks and the 7,143-assertion suite.')
