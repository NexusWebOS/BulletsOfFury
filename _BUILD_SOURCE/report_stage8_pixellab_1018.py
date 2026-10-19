"""Save the measured Stage8 asset and native verification handoff."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'_shots/stage8_pixellab_1018'
reports={n:json.loads((Q/p/'results.json').read_text()) for n,p in [('combat','native'),('transitions','transitions'),('review','review')]}
assert all(d['failed']==0 and not d['errors'] for d in reports.values())
suite=(Q/'test_fl.log').read_text();assert 'BUILD OK, 0 ERRORS' in suite
passed=sum(l.startswith('  ok ') for l in suite.splitlines());assert passed==8791
art=json.loads((R/'assets/stage8_pixellab_art_1018.js').read_text().split('const V18_ART=',1)[1].strip().removesuffix(';'))
assert len(art['models'])==7 and len(art['clips'])==7
assert sum(len(m['frames']) for m in art['models'].values())==112
assert sum(len(c['frames']) for c in art['clips'].values())==144
files=[a for m in art['models'].values() for f in m['frames'] for a in f.values()]+[a for c in art['clips'].values() for a in c['frames']]+[art['drone']]
assert len(files)==481
for a in files:
 p=R/a['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
assert hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='ae206b3d6ec874412cc76f5a65e6bfd4722a21f35e907a1ba0e90934e9009265'
assert hashlib.sha256((R/'_BUILD_SOURCE/test_fl.js').read_bytes()).hexdigest()=='c5e63b5162e6301f26b67fd8e9ea3b4d192d766367a49d84d3028a1d5506269b'
count=sum(d['passed'] for d in reports.values());size=sum((R/a['path']).stat().st_size for a in files)
payload=dict(core=dict(passed=passed,failed=0,exit=0,banner=True),native_total=count,reports=reports,
 asset=dict(models=7,modelPoses=112,transformationPoses=144,shippingPngs=len(files),bytes=size,canvas=[320,320],pivot=[160,160],droneCanvas=[256,256]),
 review='docs/previews/stage8_pixellab_1018/index.html',invulnerableBot=True,
 limits='Invulnerable native observations verify behavior, pixels and finite completion; they do not establish human balance. Broad combat pass232 and review12 precede the final cinematic-protection repair; focused transition pass13 verifies that repair and the preserved campaign ending.',
 source_sha256={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['assets/game.js','_BUILD_SOURCE/test_fl.js','assets/stage8_pixellab_1018.js','assets/stage8_pixellab_art_1018.js']})
(R/'docs/qa/stage8_pixellab_1018.json').write_text(json.dumps(payload,indent=2)+'\n')
note=f'''# 2026-10-18 - Stage8 PixelLab takeover and five-form modular finale

Mike explicitly requested modular replacements for Stage8 phases1–3. This is
a named Stage8 exception to the whole-plate rule, recorded in AGENTS.md and
the standing creative rules below. Phase3 has exactly main Colossus + Hammer,
helicopter, Harrier and volcano. No knight, cryo, Storm or Warden transformation
can enter this encounter. Their old art stays on disk for other authored uses.

PixelLab uses inspected native identity exports. Seven16-pose model banks have
three disjoint anatomical layers each: core / left weapon / right weapon.
32 actual drone-takeover poses,24 Ghost emergence,24 Colossus emergence and
four16-pose morphs complete256 poses.481 shipping PNGs total{size/1048576:.2f}MiB;
boss/effect cells320x320/pivot160,160 and actual drone256x256. No per-pose fitting
or warped duplicate frames. The gray-blank volcano idle was rejected wholesale;
the clean176x176 standard-model replacement has one proportional normalization.
Own build_stage8_pixellab_1018.py; selection/prompts/source registrations in
_ART_SOURCES/stage8_pixellab_1018. No shared atlas repack.

stage8_pixellab_1018.js is loaded last after its generated manifest. Render,
alpha hit testing, Retina, gun ports, flashes and breakups share the same
animated module rig. Primary fire damages cores. Broken weapons lose pixels,
locks, shots and their own active beams. Five finite final pools and module
damage persist across visits; dead forms never heal or re-enter. Normal/Hard/
Furious tells1.10/.96/.82s, recovery1.15/.85/.60s and increasing gun/fan pressure.
The actual approved fire-column root/body/tip renders the volcano flamethrower.

The old arena fades fully to black before the next plate swaps, then the new
generated emergence plays into its proper biome. Full-height FOV and side HUD
remain consistent. Existing PixelLab arenas/code parallax and Stage8 red portals
remain; Dracodia's monologue, final death, portal, reunion and one clear reward
are preserved. Cinematic180-second protection is capped to.5s when combat resumes
and then expires normally. Review bot invulnerability is test/preview-only.

Verification: core8791/0, exit0 and final BUILD OK; native{count}/0
({reports['combat']['passed']} combat/animation/five-pool checks,
{reports['transitions']['passed']} focused transition/protection/ending checks,
{reports['review']['passed']} delivered review checks). No page, console, draw or
asset errors. All PNG hashes and uniform canvases verified. game.js and test_fl.js
bytes and LF/CRLF remain unchanged from the start of this task. The broad combat
pass precedes the final protection-only fix; the focused transition pass tests
that fix. These invulnerable observations do not certify human balance.

Review: docs/previews/stage8_pixellab_1018/index.html (actual game iframe,
isolated saves, scene/difficulty selectors, onion overlay and native weapon/
form destruction). Report docs/STAGE8_PIXEL_LAB_1018.md; QA
docs/qa/stage8_pixellab_1018.json; captures/logs _shots/stage8_pixellab_1018.
No commit or push. Existing work preserved.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;raw=p.read_bytes();first=b'# 2026-10-18 - Stage8 PixelLab takeover and five-form modular finale'
 assert not raw.startswith(first),'handoff already saved'
 p.write_bytes(note.replace('\n','\r\n').encode()+raw)
print(json.dumps(dict(native=count,core=passed,shippingPngs=len(files),bytes=size,qa='docs/qa/stage8_pixellab_1018.json')))
