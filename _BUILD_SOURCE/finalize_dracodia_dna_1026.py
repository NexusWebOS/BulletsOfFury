"""Archive the authored living-code formation and its native/rendered proof."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_dna_1026'
native = json.loads((O / 'probe/report.json').read_text(encoding='utf8'))
latest = json.loads((O / 'video/latest.json').read_text(encoding='utf8'))
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text(encoding='utf8'))
play = json.loads((folder / 'playback.json').read_text(encoding='utf8'))
sources = json.loads((R / '_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json').read_text(encoding='utf8'))
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
assert all(hashlib.sha256((R / q['path']).read_bytes()).hexdigest() == q['sha256'] for q in sources['source'])
files = ['assets/dracodia_dna_1026.js', 'index.html', '_BUILD_SOURCE/build_dracodia_dna_1026.py',
         '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py',
         '_BUILD_SOURCE/record_dracodia_transformation_1025.py',
         '_BUILD_SOURCE/check_dracodia_transformation_video_1025.py']
frames = [q for q in film['timeline'] if q['mode'] == 'dr5er23rebirth' and 8 < q['sceneTime'] < 13.5]
fps = (frames[-1]['frames'] - frames[0]['frames']) / (frames[-1]['seconds'] - frames[0]['seconds'])
skill = Path('C:/Users/Mdogg/.codex/skills/boss-cinematics')
qa = {'scope': 'Glowing synthetic/symbiotic DNA-code strands and liquid lobes rise into the fading skeleton during Coles reaction, then converge into the native download',
      'native': {'passed': len(native['checks']), 'checks': native['checks'],
                 'report': '_shots/dracodia_dna_1026/probe/report.json'},
      'video': {k: film[k] for k in ['video', 'checks', 'chapters', 'decodedPeakDb']},
      'seconds': film['timeline'][-1]['seconds'], 'formationFps': fps,
      'playback': play, 'sourceManifest': '_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json',
      'unchangedSourceAssets': len(sources['source']), 'newGenerationCredits': 0,
      'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in files},
      'skill': {'path': str(skill), 'validated': True,
                'referenceSha256': hashlib.sha256((skill / 'references/bullets-of-fury.md').read_bytes()).hexdigest()},
      'syntax': {'assets/game.js': 0, 'assets/dracodia_dna_1026.js': 0},
      'requiredSuite': {'exitCode': 1, 'finalSummaryReached': False,
                        'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs',
                        'log': '_shots/dracodia_dna_1026/required-suite.log'}}
(R / 'docs/qa/dracodia_dna_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia living DNA-code formation - October26

Mike requested glowing synthetic/symbiotic DNA-code strands that rise with
lava-lamp motion, form the fading skeleton while Cole reacts, then lead into
the established transition. [Current audible {qa['seconds']:.2f}s recording]({url}).
The new formation starts around 0:09; earlier recordings remain preserved.

`assets/dracodia_dna_1026.js` loads after RD27. It reuses the inspected authored
AA5 binary-code12 and SV10 liquid-symbiote32 banks. Twin glowing code strands,
cross-links and pulsating liquid lobes spiral in separate rear/foreground
passes. The lobes rise along the helix and fade in/out at their flow endpoints
instead of popping when recycled. Code characters move upward, and animated
code is clipped inside the actual turning carrier silhouette with the same
phase and native registration.

Material begins appearing at scene6.2s during Cole's confused reaction, before
the7s skeleton rise. It wraps the existing24-step25%-100% opacity ramp. From13.8s,
the helix contracts and is absorbed into the native download; it is gone by15.8s,
before lightning. This green living-material spiral is distinct from the blue
ending electrical helix. Native dialogue, movement, protection, health pools,
arm/body fixes, smooth depth loops, rising thunder, complete-body flash reveal,
single closing roar and final combat handoff remain with their existing owners.

## Sources and ownership

No new raster sprites, atlas changes or paid generation.44 existing source files
keep their original palettes, even362/384 canvases and hashes. Fixed64x64 source
fragments use proportional transforms along the strands. The silhouette fill
uses one256x256 canvas and the actual carrier mask. Source availability is
preloaded with Stage8; all effect motion reads the native simulation clock.
No new attack, collision owner, warning, timer queue or sound route was added.

`python _BUILD_SOURCE/build_dracodia_dna_1026.py` verifies the even source cells
and crop, and owns `_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json`.
The manifest records all44 unchanged authored source hashes, keys, dimensions,
the common crop and timings. Boss Cinematics has the current formation recipe.

## Verification

- {len(native['checks'])} native Chromium checks pass. Isolated actual-pixel comparisons detect
  the strands/fluid lobes and the code inside the true skeletal silhouette.
  All12 code and32 liquid frames animate; front/back cross-links and14 lobes,
  early appearance with Cole, absorption and cleanup before lightning pass.
  The previous health, arm/body, frame seams, opacity, audio, closing roar,
  actual hit pixels/expiry and protected reveal checks remain green.
- {len(film['checks'])} recording and {len(play['checks'])} playback checks pass, including sound, Range
  seeking and playback of the new formation. Actual native/decoded screenshots
  were inspected. Formation runs at about {fps:.1f} native frames/s. The whole film
  decodes with{film['decodedPeakDb']}dB audible peak and no page/console/asset errors.
- JavaScript/Python syntax and installed skill validation pass. Required
  test_fl.js still exits1 before assertions/final summary on existing missing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs`; the full suite is not green.

Use the existing probe, recorder and playback helper with `--dna`.
Evidence: `docs/qa/dracodia_dna_1026.json` and `_shots/dracodia_dna_1026/`.
The film uses explicit native arm/core-damage checkpoints and includes the
complete speech. It is not a complete boss fight. No game.js/test_fl.js edits,
commit or push.
'''
for a, b in [('code12','code 12'), ('symbiote32','symbiote 32'), ('scene6','scene 6'), ('the7','the 7'), ('existing24','existing 24'), ('step25','step 25'), ('From13','From 13'), ('by15','by 15'), ('generation.44','generation. 44'), ('even362','even 362'), ('Fixed64','Fixed 64'), ('one256','one 256'), ('all44','all 44'), ('All12','All 12'), ('and32','and 32'), ('and14','and 14'), ('with-','with -'), ('exits1','exits 1')]:
    doc = doc.replace(a, b)
(R / 'docs/DRACODIA_DNA_1026.md').write_text(doc, encoding='utf8')
title = '## October26 - Living DNA-code builds the rising Dracodia skeleton'
note = f'''{title}

Mike requested living synthetic/symbiotic DNA-code formation during Cole's reaction. assets/dracodia_dna_1026.js reuses inspected AA5 code12 and SV10 liquid32 art: paired glowing code helices/cross-links, rising pulsing lobes, and animated code clipped inside the actual turning skeleton. It appears from6.2s, wraps the25%-100% skeletal rise and converges into download from13.8 to15.8s, before lightning. Rear/front depth, native clocks, all previous cinematic/combat/body/audio fixes remain.44 original source files retained; no new raster generation or atlas edits. Builder/source manifest and Boss Cinematics reference record the recipe.

{len(native['checks'])} native, {len(film['checks'])} recording and {len(play['checks'])} playback checks pass. New audible{qa['seconds']:.2f}s film and actual native/decoded DNA pixels inspected, about{fps:.1f} fps during formation, no browser/asset errors. Notes/QA: docs/DRACODIA_DNA_1026.md and docs/qa/dracodia_dna_1026.json. Syntax passes; required full suite exits1 before summary due existing missing retired_art_archive_1022.cjs. No game.js/test_fl.js edits, commit or push.

'''
for a, b in [('code12','code 12'), ('liquid32','liquid 32'), ('from6','from 6'), ('the25','the 25'), ('from13','from 13'), ('to15','to 15'), ('remain.44','remain. 44'), ('audible'+f'{qa["seconds"]:.2f}','audible '+f'{qa["seconds"]:.2f}'), ('about'+f'{fps:.1f}','about '+f'{fps:.1f}'), ('exits1','exits 1')]:
    note = note.replace(a, b)
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '\n## October26 Dracodia living DNA-code formation\n\n- The initial skeletal rise has its own living green DNA-code formation from6.2 to15.8s: authored code/liquid lobes, rear/front helix, binary cross-links and code inside the actual carrier mask. It wraps the stepped skeletal fade, then converges into download before lightning. This material spiral is separate from the blue ending electricity. Preserve native dialogue, protection and all later fixes. Current owner/evidence: docs/DRACODIA_DNA_1026.md; source manifest owner build_dracodia_dna_1026.py.\n'.replace('from6','from 6').replace('to15','to 15')
if b'## October26 Dracodia living DNA-code formation' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
print(json.dumps({'native': len(native['checks']), 'recording': len(film['checks']),
                  'playback': len(play['checks']), 'video': film['video'], 'formationFps': fps}))
