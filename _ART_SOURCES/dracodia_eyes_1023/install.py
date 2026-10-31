from pathlib import Path
import shutil,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_ART_SOURCES/dracodia_brain_1023';D=R/'assets/game/levels/stage_08/boss/neural_archon_1023';C=R/'_ART_SOURCES/dracodia_eyes_1023';C.mkdir(parents=True,exist_ok=True)
assert not json.loads((W/'shipping/manifest.json').read_text()).get('PROVISIONAL_SINGLE_FRAME_COMBAT_SMOKE')
for p in(W/'shipping').glob('*.webp'):shutil.copy2(p,D/p.name)
for folder in ['raw','shipping']:shutil.copytree(W/folder,C/folder,dirs_exist_ok=True)
for folder in ['charge','laser_new']:shutil.copytree(W/'raw'/folder,S/'raw'/folder,dirs_exist_ok=True)
for name in ['brain.js','brain_art.js','asset-audit.json','requests.json','jobs.json','brain-review.png','charge-review.png','cloud-review.png','geyser-review.png','morph-review.png']:
 shutil.copy2(W/name,C/name)
for name in ['brain.js','brain_art.js','asset-audit.json','brain-review.png','charge-review.png']:shutil.copy2(W/name,S/name)
shutil.copytree(W/'shipping',S/'shipping',dirs_exist_ok=True)
p=S/'jobs.json';j=json.loads(p.read_text());j.update(json.loads((W/'jobs.json').read_text()));p.write_text(json.dumps(j,indent=2))
p=S/'generation-prompts.json';j=json.loads(p.read_text());j['eye_correction_1023']=json.loads((W/'requests.json').read_text());p.write_text(json.dumps(j,indent=2))
shutil.copy2(W/'brain.js',R/'assets/dracodia_brain_1023.js');shutil.copy2(W/'brain_art.js',R/'assets/dracodia_brain_art_1023.js')
# Exact explicit paths; never string-rewrite a builder's own replacement rules.
s=(W/'build.py').read_text(encoding='utf-8').replace("R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');B=R/'_ART_SOURCES/dracodia_brain_1023';W=Path(__file__).resolve().parent;O=W/'shipping';O.mkdir(exist_ok=True)","R=Path(__file__).resolve().parents[1];B=R/'_ART_SOURCES/dracodia_brain_1023';W=B;O=W/'shipping';O.mkdir(exist_ok=True)")
(R/'_BUILD_SOURCE/build_dracodia_brain_1023.py').write_text(s,encoding='utf-8');shutil.copy2(R/'_BUILD_SOURCE/build_dracodia_brain_1023.py',S/'build.py')
# Repair the previous self-rewriting installer so rebuild/install is repeatable.
legacy='''from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_brain_1023';D=R/'assets/game/levels/stage_08/boss/neural_archon_1023'
for p in(S/'shipping').glob('*.webp'):shutil.copy2(p,D/p.name)
for name in ['brain.js','brain_art.js']:shutil.copy2(S/name,R/'assets'/('dracodia_brain_1023.js'if name=='brain.js'else'dracodia_brain_art_1023.js'))
print('Installed current Neural Archon frames and runtime.')
'''
(R/'_BUILD_SOURCE/install_dracodia_brain_1023.py').write_text(legacy,encoding='utf-8');shutil.copy2(R/'_BUILD_SOURCE/install_dracodia_brain_1023.py',S/'install.py')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('neural-archon-1023-2','neural-eyes-1023-1');p.write_text(s,encoding='utf-8',newline='\n')
p=R/'assets/data/asset_catalog.json';a=json.loads(p.read_text(encoding='utf-8'));a['assets']=[v for v in a['assets']if not v['key'].startswith(('nb23_','nca_nb23_'))];m=json.loads((W/'shipping/manifest.json').read_text())
for v in m['sheets'].values():a['assets'].append({'key':v['key'],'root':v['key'],'path':v['path'],'owner':'levels/stage_08/boss/neural_archon_1023','cell':None})
for rows in m['banks'].values():
 for cell in rows:
  root=m['sheets'][cell['sheet']];a['assets'].append({'key':cell['key'],'root':root['key'],'path':root['path'],'owner':'levels/stage_08/boss/neural_archon_1023','cell':cell['cell']})
p.write_text(json.dumps(a,indent=2),encoding='utf-8')
p=R/'assets/data/ART_TAXONOMY.json';a=json.loads(p.read_text(encoding='utf-8'));a['nb23_']['note']='Whole-frame PixelLab idle/charge/focus preserve moving face; each body cell has measured eyes. New16-frame laser flow at6 baked expansion widths. Authored white hit partners and progressive eye/brow glow; no live visual effects. Sources _ART_SOURCES/dracodia_brain_1023 and dracodia_eyes_1023.';p.write_text(json.dumps(a,indent=2),encoding='utf-8')
for name in ['install.py','build.py','download.py','probe.py']:shutil.copy2(W/name,C/name)
print('Installed whole-frame moving eyes, authored charge and16-frame PixelLab beams.')
