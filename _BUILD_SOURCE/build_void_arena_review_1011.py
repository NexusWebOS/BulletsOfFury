"""Publish the actual native captures and portable verification record."""
from pathlib import Path
from PIL import Image
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/void_arena_1011/images';OUT.mkdir(parents=True,exist_ok=True)
SHOTS=ROOT/'_shots/void_arena_1011'
for name in ['05-void-left.png','06-void-right.png','07-void-fit.png','battle-loop.webp']:
    shutil.copyfile(SHOTS/name,OUT/name)
with Image.open(SHOTS/'battle-loop.webp') as im:
    im.seek(0);im.convert('RGB').save(OUT/'battle-still.png')
arena=json.loads((SHOTS/'verification.json').read_text())
finale=json.loads((ROOT/'_shots/playthrough_1011/finale/report.json').read_text())
log=(ROOT/'_shots/void_arena_1011_regression.log').read_text(encoding='utf-8')
regression=dict(passed=len(re.findall(r'^  ok  ',log,re.M)),
    failed=len(re.findall(r'^\s*(?:FAIL|NOT OK|not ok)\b',log,re.M)),
    finalSummary='==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in log,exitCode=0)
assert not arena['failed'] and not finale['failed'] and regression['finalSummary']
paths=['assets/void_arena_1011.js','assets/void_arena_art_1011.js','index.html',
       '_ART_SOURCES/void_arena_1011/prompts.json',
       'assets/game/levels/stage_08/stage/void_arena_1011/manifest.json']
report=dict(date='2026-10-11',localOnly=True,arena=arena,finale=finale,regression=regression,
            files={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            limits='Protected bounded native encounters and camera fixtures, not a full campaign clear.')
if (SHOTS/'preview-qa.json').exists():
    report['preview']=json.loads((SHOTS/'preview-qa.json').read_text())
(ROOT/'docs/qa/void_arena_1011.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(arena=arena['passed'],finale=finale['passed'],regression=regression['passed'])))
