from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];S=Path(__file__).parent;A=R/'_ART_SOURCES/cinema_overnight_1116';A.mkdir(parents=True,exist_ok=True)
q=json.loads((R/'_shots/cinema_overnight_1116/weather/candidate.json').read_text());assert len(q['results'])==48 and all(r['different']==0 for r in q['results'])and not q['errors'];assert len(q['fallbacks'])==5 and all(r['different']==0 and r['skipped']==0 for r in q['fallbacks'])
code=(S/'night_weather_1116.js').read_text();(R/'assets/night_weather_1116.js').write_text(code,encoding='utf8',newline='\n');(A/'night_weather_1116.js').write_text(code,encoding='utf8',newline='\n')
p=R/'index.html';raw=p.read_bytes();backup=A/'index-before-weather.html'
if not backup.exists():backup.write_bytes(raw)
s=raw.decode('utf8');eol='\r\n'if b'\r\n'in raw else'\n';tag='<script src="assets/night_weather_1116.js?v=1"></script>'
if tag not in s:s=s.replace('</body>',tag+eol+'</body>')
p.write_bytes(s.encode('utf8'));print('Installed conservative authored weather culling; unchanged native clocks/art/HP')
s=(R/'_BUILD_SOURCE/night_diagnostic_1116.py').read_text();s=s.replace("native-diagnostic'","native-weather'")
(R/'_BUILD_SOURCE/night_weather_record_1116.py').write_text(s,encoding='utf8',newline='\n')
