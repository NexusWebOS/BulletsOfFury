"""Archive the local DNA palette swap and unchanged drone-conversion review."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
palette = json.loads((R / '_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json').read_text(encoding='utf8'))
native = json.loads((R / '_shots/dracodia_palette_1026/probe/report.json').read_text())
latest = json.loads((R / '_shots/drone_host_1026/latest.json').read_text())
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text())
play = json.loads((folder / 'playback.json').read_text())
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
assert all(q['decodedAlphaPreserved'] and q['decodedMaxLuminanceError'] <= .51 for q in palette['palette']['metrics'])
assert all(hashlib.sha256((R / q['path']).read_bytes()).hexdigest() == q['sha256'] for q in palette['source'])
conversion = next(q['seconds'] - q['t'] for q in film['timeline'] if q['mode'] == 'v18conversion')
fight = next(q['seconds'] for q in film['timeline'] if q['mode'] == 'fight')
skill = Path('C:/Users/Mdogg/.codex/skills/boss-cinematics')
files = ['assets/dracodia_dna_1026.js', 'assets/dracodia_dna_palette_1026.js', 'index.html',
         '_BUILD_SOURCE/build_dracodia_dna_1026.py', '_BUILD_SOURCE/record_drone_host_1026.py',
         '_BUILD_SOURCE/check_drone_host_video_1026.py', '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py']
qa = {'scope': 'DNA-only final-form violet/red-magenta palette, plus native drone-to-phase1 recording for review',
      'paletteNative': {'passed': len(native['checks']), 'checks': native['checks'],
                        'report': '_shots/dracodia_palette_1026/probe/report.json'},
      'paletteCells': {'count': 44, 'allDecodedAlphaPreserved': True,
                       'maximumLuminanceError': max(q['decodedMaxLuminanceError'] for q in palette['palette']['metrics']),
                       'banks': palette['palette']['banks'], 'originalSourcesUnchanged': True,
                       'manifest': '_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json'},
      'video': {k: film[k] for k in ['video', 'checks', 'chapters', 'decodedPeakDb', 'method']},
      'seconds': film['timeline'][-1]['seconds'], 'conversionStart': conversion, 'fightStart': fight,
      'nativeFps': film['sound']['frames'] / film['timeline'][-1]['seconds'], 'playback': play,
      'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in files},
      'skill': {'path': str(skill), 'validated': True,
                'referenceSha256': hashlib.sha256((skill / 'references/bullets-of-fury.md').read_bytes()).hexdigest()},
      'syntax': {'assets/game.js': 0, 'assets/dracodia_dna_1026.js': 0, 'assets/dracodia_dna_palette_1026.js': 0},
      'requiredSuite': {'exitCode': 1, 'finalSummaryReached': False,
                        'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs',
                        'log': '_shots/dracodia_palette_1026/required-suite.log'}}
(R / 'docs/qa/dracodia_palette_drone_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia DNA palette and drone conversion review - October26

Mike requested the DNA code match his final-form palette, then a recording of
the drone transforming into the first combat form for review.
[Current audible {qa['seconds']:.2f}s drone-to-phase1 film]({url}).
Conversion begins at {conversion:.2f}s; phase1 combat starts at {fight:.2f}s.
The existing conversion is4.3 native seconds. This pass records that entrance
as-is; it does not redesign the drone conversion.

## Palette

The DNA-only palette now matches the final form's dark violet metal,
red-magenta energy and pale highlights. The canonical final-body reference
and actual rendered palette were inspected. Green-biased pixels in the12
code and32 liquid frames are mapped through a luminance-preserving ramp.
Neutral/dark metal, source alpha, frame sizes, pivots and proportions remain.
The maximum decoded luminance error is{qa['paletteCells']['maximumLuminanceError']:.4f} on a255 scale;
all44 decoded cells preserve exact alpha. Original44 green sources remain
byte-identical for their existing arena/ending owners.

The owning DNA builder creates two isolated palette sheets and registers
`assets/dracodia_dna_palette_1026.js`. The runtime uses cached source-sized
cells only for RD28's strands, fluid and skeletal code fill. Stage8 preloads
the two palette images; no runtime pixel-color processing or green-source
replacement is needed. No shared atlas repack or paid generation.

Rebuild with `python _BUILD_SOURCE/build_dracodia_dna_1026.py`. Source hashes,
palette stops, per-cell alpha/luminance checks, sheet metadata and hashes are
in `_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json`. The builder also
owns the rd28p_ taxonomy registration. Native palette preview:
`_shots/dracodia_palette_1026/probe/native-11.5.png`.

## Drone recording and verification

`record_drone_host_1026.py` captures from native entrance time0 through portal,
drone arrival, complete conversion and six seconds of first-form combat.
No damage fixtures, phase changes or animation timer skips are used. Cole
observes with idle controls/weapons and God mode; native boss health and all
parts remain full in combat. Dialogue, conversion shriek and combat sounds
play through their original mixer routes.

- {len(native['checks'])} native cinematic checks pass, including actual violet/magenta DNA
  pixels and all prior formation, health, body, loop, fade, audio and roar checks.
- {len(film['checks'])} recording checks and {len(play['checks'])} playback checks pass. The film fully
  decodes at about {qa['nativeFps']:.1f} native frames/s with{film['decodedPeakDb']}dB sound,
  Range seeking and no page/console/asset errors. Native palette and decoded
  drone contact frames were inspected.
- JS/Python syntax and installed Boss Cinematics validation pass. The full
  test_fl suite still exits1 before assertions/final summary on existing missing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs`; it is not green.

Reproduce native palette verification with the existing cinematic probe's
`--palette` flag. Use `record_drone_host_1026.py` and
`check_drone_host_video_1026.py` for the entrance recording/playback.
QA: `docs/qa/dracodia_palette_drone_1026.json`. Earlier takes remain.
No game.js/test_fl.js edits, commit or push.
'''
for a, b in [('is4','is 4'), ('the12','the 12'), ('and32','and 32'), ('error is','error is '), ('a255','a 255'), ('all44','all 44'), ('Original44','Original 44'), ('time0','time 0'), ('with-','with -'), ('exits1','exits 1')]:
    doc = doc.replace(a, b)
(R / 'docs/DRACODIA_PALETTE_DRONE_1026.md').write_text(doc, encoding='utf8')
title = '## October26 - Final-form DNA palette and native drone conversion recording'
note = f'''{title}

Mike requested DNA in Dracodia's final-form colors and a current drone-to-phase1 review. The DNA-only violet/red-magenta/pale-metal palette uses two isolated sheets through the owning DNA builder; all44 source alpha cells and luminance are preserved, original green sources unchanged.48 native cinematic checks pass. Fresh audible{qa['seconds']:.2f}s film records native portal, drone arrival, full4.3s conversion and opening phase1 combat without damage/phase/timer writes; conversion at{conversion:.2f}s, fight at{fight:.2f}s. {len(film['checks'])} recording and{len(play['checks'])} playback checks pass; decoded frames inspected, about{qa['nativeFps']:.1f} native fps, no errors. Drone conversion itself is unchanged for review. Boss Cinematics reference updated. Docs/QA: docs/DRACODIA_PALETTE_DRONE_1026.md and docs/qa/dracodia_palette_drone_1026.json. Syntax passes; required full suite still exits1 before summary on missing retired_art_archive_1022.cjs. No game.js/test_fl.js edits, commit/push.

'''
for a, b in [('all44','all 44'), ('unchanged.48','unchanged. 48'), ('audible'+f'{qa["seconds"]:.2f}','audible '+f'{qa["seconds"]:.2f}'), ('full4','full 4'), ('at'+f'{conversion:.2f}','at '+f'{conversion:.2f}'), ('at'+f'{fight:.2f}','at '+f'{fight:.2f}'), ('and'+str(len(play['checks'])),'and '+str(len(play['checks']))), ('about'+f'{qa["nativeFps"]:.1f}','about '+f'{qa["nativeFps"]:.1f}'), ('exits1','exits 1')]:
    note = note.replace(a, b)
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '\n## October26 DNA final-form palette\n\n- RD28 DNA uses Dracodia violet/red-magenta energy and pale highlights through two local palette sheets. Preserve native luminance, alpha, outlines and original green sources; regenerate through build_dracodia_dna_1026.py. The current drone-to-phase1 film records the unchanged native conversion for review. See docs/DRACODIA_PALETTE_DRONE_1026.md.\n'
if b'## October26 DNA final-form palette' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
print(json.dumps({'native': len(native['checks']), 'recording': len(film['checks']),
                  'playback': len(play['checks']), 'video': film['video'], 'conversion': [conversion, fight]}))
