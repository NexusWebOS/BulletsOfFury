from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
M=json.loads((W/'manifest.json').read_text(encoding='utf8'));assert set(M)=={'corrupt-overhead','corrupt-sides'}
A=R/'assets/game/shared/combat/boss_hammer_frontal_1109c';S=R/'_ART_SOURCES/boss_hammer_frontal_1109c';A.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
for n in M:
 for mat in ['regular','chrome','red','hit','red_hit']:shutil.copy2(W/'exports'/f'{n}_{mat}.webp',A/f'{n}_{mat}.webp')
 shutil.copy2(W/'exports'/f'{n}.aseprite',S/f'{n}.aseprite')
(S/'generated').mkdir(exist_ok=True)
for p in (W/'generated').glob('*.png'):shutil.copy2(p,S/'generated'/p.name)
for n in ['author.lua','build.py','jobs.json','prompts.json','audit.json']:shutil.copy2(W/n,S/n)
(A/'manifest.json').write_text(json.dumps(M,separators=(',',':')),encoding='utf8')
(R/'assets/boss_hammer_frontal_art_1109c.js').write_text('Object.assign(BA119_ART,'+json.dumps(M,separators=(',',':'))+');\n',encoding='utf8')
p=R/'index.html';s=p.read_bytes();tag=b'<script src="assets/boss_hammer_frontal_art_1109c.js?v=1"></script>'
if tag not in s:s=s.replace(b'<script src="assets/boss_animation_1109.js?v=1"></script>',tag+b'\n<script src="assets/boss_animation_1109.js?v=1"></script>')
s=s.replace(b'playtest_repairs_1108.js?v=39',b'playtest_repairs_1108.js?v=40');p.write_bytes(s)
print('Installed 32 front-facing poses with regular/chromium/rage/hit materials')
