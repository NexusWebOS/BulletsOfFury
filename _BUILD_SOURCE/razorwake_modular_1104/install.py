from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');D=R/'assets/game/levels/stage_06/miniboss/razorwake_modular_1104';D.mkdir(parents=True,exist_ok=True);S=R/'_BUILD_SOURCE/razorwake_modular_1104';S.mkdir(parents=True,exist_ok=True)
for p in(W/'authored').glob('*'):
 if p.suffix in['.png','.json','.bin']:shutil.copy2(p,D/p.name)
 elif p.is_file():shutil.copy2(p,S/p.name)
shutil.copytree(W/'authored/strips',S/'strips',dirs_exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
for n in ['razorwake-modular-generated.png','wind-tornado-generated.png','PROMPTS.md']:shutil.copy2(W/n,S/n)
for n in ['razorwake_modular_1104.js','razorwake_modular_art_1104.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'assets/projectile_fx_1103.js';s=p.read_bytes()
if b'||S.b?._rw117Owner'not in s:s=s.replace(b'S.b?._ss116)',b'S.b?._ss116||S.b?._rw117Owner)')
while b'||S.b?._rw117Owner||S.b?._rw117Owner'in s:s=s.replace(b'||S.b?._rw117Owner||S.b?._rw117Owner',b'||S.b?._rw117Owner')
s=s.replace(b'!b._th114Owner&&!b._ss116?hist(b)',b'!b._th114Owner&&!b._ss116&&!b._rw117Owner?hist(b)');p.write_bytes(s)
p=R/'index.html';s=p.read_bytes()
if b'assets/razorwake_modular_1104.js'not in s:s=s.replace(b'</body>',b'<script src="assets/razorwake_modular_art_1104.js?v=wind-chains-1"></script>\r\n<script src="assets/razorwake_modular_1104.js?v=wind-chains-1"></script>\r\n</body>');p.write_bytes(s)
print('Installed Razorwake hinged wings, independent miniguns and wind attack owner.')
