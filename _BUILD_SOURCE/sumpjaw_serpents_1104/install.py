from pathlib import Path
import shutil,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
D=R/'assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104';D.mkdir(parents=True,exist_ok=True)
S=R/'_BUILD_SOURCE/sumpjaw_serpents_1104';S.mkdir(parents=True,exist_ok=True)
for p in (W/'authored').glob('*'):
 if p.suffix in ['.png','.json']:shutil.copy2(p,D/p.name)
 else:shutil.copy2(p,S/p.name)
for n in ['sumpjaw_serpents_1104.js','sumpjaw_serpent_art_1104.js']:shutil.copy2(W/n,R/'assets'/n)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
p=R/'assets/projectile_fx_1103.js';text=p.read_bytes();text=text.replace(b'if(S.on&&S.b?._th114Owner)return rawDraw.call(this,im,...a);',b'if(S.on&&(S.b?._th114Owner||S.b?._ss116))return rawDraw.call(this,im,...a);').replace(b'h=b&&!b.dead&&!b._th114Owner?hist(b):null',b'h=b&&!b.dead&&!b._th114Owner&&!b._ss116?hist(b):null');p.write_bytes(text)
index=R/'index.html';text=index.read_bytes();needle=b'<script src="assets/sumpjaw_serpent_art_1104.js'
if needle not in text:text=text.replace(b'</body>',b'<script src="assets/sumpjaw_serpent_art_1104.js?v=serpentine-1"></script>\r\n<script src="assets/sumpjaw_serpents_1104.js?v=serpentine-1"></script>\r\n</body>');index.write_bytes(text)
print('Installed source-preserving articulated Sumpjaw owner;game.js unchanged.')
