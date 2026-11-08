from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');M=json.loads((W/'authored/manifest.json').read_text());D=R/'assets/game/levels/stage_07/miniboss/sumpjaw_tandem_1105';D.mkdir(parents=True,exist_ok=True)
for p in M['pages'].values():shutil.copy2(W/'authored'/Path(p['path']).name,D/Path(p['path']).name)
shutil.copy2(W/'authored/manifest.json',D/'manifest.json')
for n in ['sumpjaw_tandem_1105.js','sumpjaw_tandem_art_1105.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'index.html';raw=p.read_bytes()
if b'assets/sumpjaw_tandem_1105.js'not in raw:p.write_bytes(raw.replace(b'</body>',b'<script src="assets/sumpjaw_tandem_art_1105.js?v=paired-jump-1"></script>\r\n<script src="assets/sumpjaw_tandem_1105.js?v=paired-jump-1"></script>\r\n</body>'))
print('Installed SJ120 coordinated Sumpjaw pair.')
