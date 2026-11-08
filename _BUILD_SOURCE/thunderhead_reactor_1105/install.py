from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
M=json.loads((W/'authored/manifest.json').read_text());D=R/'assets/game/levels/stage_06/boss/thunderhead_reactor_1105';D.mkdir(parents=True,exist_ok=True)
for p in M['pages'].values():shutil.copy2(W/'authored'/Path(p['path']).name,D/Path(p['path']).name)
for n in ['manifest.json','opaque_masks.bin']:shutil.copy2(W/'authored'/n,D/n)
for n in ['thunderhead_reactor_art_1105.js','thunderhead_reactor_1105.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'index.html';raw=p.read_bytes()
if b'assets/thunderhead_reactor_1105.js'not in raw:p.write_bytes(raw.replace(b'</body>',b'<script src="assets/thunderhead_reactor_art_1105.js?v=reactor-depth-1"></script>\r\n<script src="assets/thunderhead_reactor_1105.js?v=reactor-depth-1"></script>\r\n</body>'))
print('Installed TC119 Thunderhead reactor pass.')
