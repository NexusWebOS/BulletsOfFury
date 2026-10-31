from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_brain_1023';D=R/'assets/game/levels/stage_08/boss/neural_archon_1023'
for p in(S/'shipping').glob('*.webp'):shutil.copy2(p,D/p.name)
for name in ['brain.js','brain_art.js']:shutil.copy2(S/name,R/'assets'/('dracodia_brain_1023.js'if name=='brain.js'else'dracodia_brain_art_1023.js'))
print('Installed current Neural Archon frames and runtime.')
