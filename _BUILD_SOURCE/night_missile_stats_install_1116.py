from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=Path(__file__).parent;O=R/'_shots/cinema_overnight_1116/missile-stats';A=R/'_ART_SOURCES/cinema_overnight_1116'
q=json.loads((O/'contracts-shipping.json').read_text());assert len(q['rows'])==7 and not q['errors']and all(all(a['checks'].values())and all(a.get('edge',{}).values())for a in q['rows'])
before=json.loads((O/'before.json').read_text())['rows'][0];after=json.loads((O/'candidate.json').read_text())['rows'][0];assert before['setup']['hp']-before['hp']==after['setup']['hp']-after['hp']==34 and before['stats']['mslHits']==0 and after['stats']['mslHits']==1
p=R/'assets/night_missile_stats_1116.js';p.write_text((S/p.name).read_text(),encoding='utf8',newline='\n');(A/p.name).write_bytes(p.read_bytes());p=R/'index.html';raw=p.read_bytes();backup=A/'index-before-missile-stats.html'
if not backup.exists():backup.write_bytes(raw)
s=raw.decode('utf8');eol='\r\n'if b'\r\n'in raw else'\n';tag='<script src="assets/night_missile_stats_1116.js?v=1"></script>'
if tag not in s:s=s.replace('</body>',tag+eol+'</body>')
p.write_bytes(s.encode('utf8'));print('Installed player missile hit accounting; no damage/phase/reward changes')
