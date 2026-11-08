from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
D=R/'assets/game/levels/stage_06/miniboss/razorwake_tempest_1105';D.mkdir(parents=True,exist_ok=True)
S=R/'_BUILD_SOURCE/razorwake_tempest_1105';S.mkdir(parents=True,exist_ok=True)
for p in(W/'authored').glob('*'):
 if p.suffix in['.png','.json','.bin']:shutil.copy2(p,D/p.name)
 elif p.is_file():shutil.copy2(p,S/p.name)
shutil.copytree(W/'authored/strips',S/'strips',dirs_exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
for n in ['wind-orb-generated.png','thruster-generated.png','helix-reference.png','PROMPTS.json','SPEC.md']:shutil.copy2(W/n,S/n)
for n in ['razorwake_tempest_1105.js','razorwake_tempest_art_1105.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'index.html';s=p.read_bytes()
if b'assets/razorwake_tempest_1105.js'not in s:s=s.replace(b'</body>',b'<script src="assets/razorwake_tempest_art_1105.js?v=aggressive-wind-1"></script>\r\n<script src="assets/razorwake_tempest_1105.js?v=aggressive-wind-1"></script>\r\n</body>');p.write_bytes(s)
print('Installed RW118 aggressive modular wind encounter.')
