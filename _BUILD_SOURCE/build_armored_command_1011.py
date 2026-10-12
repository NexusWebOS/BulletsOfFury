"""Publish Mike's approved concept, preserving its measured, even display windows."""
from pathlib import Path
import json, hashlib, shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '_ART_SOURCES/hud_concepts_1011/armored-command.png'
OUT = ROOT / 'assets/game/shared/ui/armored_command_1011'
OUT.mkdir(parents=True, exist_ok=True)
layout = next(v for v in json.loads((ROOT/'docs/previews/hud_concepts_1011/concepts.json').read_text())['layouts'] if v['key']=='armored-command')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == layout['sha256']
shutil.copyfile(SOURCE, OUT/'frame.png')
layout.update(key='hud_armored_command_1011', path='assets/game/shared/ui/armored_command_1011/frame.png', top=92, bottom=120, approved='Mike, October 11: Armored Command')
(ROOT/'assets/armored_command_art_1011.js').write_text('"use strict";\nconst AC11_ART='+json.dumps(layout, separators=(',', ':'))+';\n', encoding='utf-8', newline='\n')
(OUT/'registration.json').write_text(json.dumps(layout,indent=2), encoding='utf-8')
print('Armored Command: approved source, 11 measured wells, proportional top and bottom strips.')
