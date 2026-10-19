"""Record completed native evidence without altering source or prior notes."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'_shots/stage8_identity_1018'
reports={name:json.loads((Q/name/'results.json').read_text()) for name in ['native','sequences','review']}
assert all(r['failed']==0 and not r['errors'] for r in reports.values())
log=(Q/'test_fl.log').read_text(encoding='utf-8');passed=sum(x.startswith('  ok ') for x in log.splitlines())
assert passed==8791 and 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in log
pre={'assets/game.js':'ae206b3d6ec874412cc76f5a65e6bfd4722a21f35e907a1ba0e90934e9009265','_BUILD_SOURCE/test_fl.js':'c5e63b5162e6301f26b67fd8e9ea3b4d192d766367a49d84d3028a1d5506269b'}
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in pre};assert hashes==pre
data=dict(core=dict(passed=passed,failed=0,exit=0,banner=True),native_total=sum(r['passed'] for r in reports.values()),reports={k:dict(passed=v['passed'],failed=v['failed'],errors=v['errors'],evidence=f'_shots/stage8_identity_1018/{k}/results.json') for k,v in reports.items()},art=json.loads((R/'_ART_SOURCES/stage8_identity_1018/registration.json').read_text()),preserved_preexisting_source_sha256=hashes)
(R/'docs/qa/stage8_identity_1018.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
heading='# 2026-10-18 - Stage8 native identities, Dracodia avatar and new defeats\n\n'
note=heading+'''Mike rejected the generic Stage8 attack books and the Hammer's extra arm.
The latest owner is assets/stage8_identity_1018.js, loaded after V18 and its
new art registry. Hammer uses native Stage5 combat and two-arm HK5 poses,
plus the real16-pose left/right swings and depth/plane rules. Volcano uses
the real Furnace arms/body/head pools, independent arm poses, continuous
flamethrower, magma/firewave cannon and full360-degree eye-laser head phase.
The explicitly approved old six-part Harrier uses its actual controller.
Dracodia/host/Ghost use organic limbs, core spores and purple-black wells;
no generic arm missiles or arm gun lasers. Main Colossus has24 real roar
and24 scythe poses, a new avatar plus16 speech poses. New host/Ghost deaths
precede full-black arena swaps; final death uses20 selected detailed poses,
opaque80x80 armor fragments, repeated explosions and a last-copy reform.
The established red portal/reunion still awards one campaign clear.

315 loose PNGs/8.94MiB; fixed320x320/pivot160,160, common proportional scale.
Owner build_stage8_identity_1018.py; exact refs/prompts/jobs and selections
under _ART_SOURCES/stage8_identity_1018. No shared atlas edit. Native full-
FOV review remains docs/previews/stage8_pixellab_1018/index.html; it now has
avatar, roar, final death, detached-head and correct native onion controls.

QA:121 native Chromium checks passed across Normal/Hard/Furious, sequences
and delivered preview; zero page/console/draw/asset errors. Core8791/0,
exit0 and final BUILD OK banner. The initial Harrier lookup and Furnace
rounding failures were fixed and retested. Detailed evidence:
docs/STAGE8_IDENTITIES_1018.md and docs/qa/stage8_identity_1018.json.
game.js and test_fl.js match their pre-correction hashes, preserving all
earlier local changes and their line endings. No commit or push in this pass.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;s=p.read_text(encoding='utf-8')
 if not s.startswith(heading):p.write_text(note+s,encoding='utf-8',newline='\n')
print(json.dumps(dict(core=passed,native=data['native_total'],errors=0)))
