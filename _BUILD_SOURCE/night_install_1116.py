from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];C=Path(__file__).parent
backup=R/'_ART_SOURCES/cinema_overnight_1116/night_cinema_before_boss_loading_1116.js'
if not backup.exists():backup.write_bytes((R/'assets/night_cinema_1116.js').read_bytes())
for n in ['night_cinema_1116.js']:
 (R/'assets'/n).write_text((C/n).read_text(encoding='utf8'),encoding='utf8',newline='\n')
p=R/'index.html';s=p.read_text(encoding='utf8');tag='<script src="assets/night_cinema_1116.js?v=6"></script>'
for v in[1,2,3,4,5]:s=s.replace('<script src="assets/night_cinema_1116.js?v='+str(v)+'"></script>',tag)
if tag not in s:s=s.replace('</body>',tag+'\n</body>')
p.write_text(s,encoding='utf8',newline='\n')
print('Installed scoped cinematic continuity/readability owner.')
