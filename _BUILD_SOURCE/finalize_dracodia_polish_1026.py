"""Archive frame/opacity/audio/speech/body corrections and their native evidence."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_polish_1026'
native = json.loads((O / 'probe/report.json').read_text(encoding='utf8'))
latest = json.loads((O / 'video/latest.json').read_text(encoding='utf8'))
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text(encoding='utf8'))
play = json.loads((folder / 'playback.json').read_text(encoding='utf8'))
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
files = ['assets/dracodia_polish_1026.js', 'assets/dracodia_depth_1026.js',
         'assets/stage78_review_1025.js', 'assets/stage78_review_art_1025.js',
         '_BUILD_SOURCE/build_stage78_review_1025.py', 'index.html',
         '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py',
         '_BUILD_SOURCE/record_dracodia_transformation_1025.py',
         '_BUILD_SOURCE/check_dracodia_transformation_video_1025.py']
skill = Path('C:/Users/Mdogg/.codex/skills/boss-cinematics')
audio = film['events']['polish']
qa = {'scope': 'Cyclic subframes, 24-step skeleton fade, rising audible strike gain, single final speech roar, and intact first-host body after arm breaks and during its fall',
      'native': {'passed': len(native['checks']), 'checks': native['checks'],
                 'report': '_shots/dracodia_polish_1026/probe/report.json'},
      'video': {k: film[k] for k in ['video', 'checks', 'chapters', 'decodedPeakDb']},
      'seconds': film['timeline'][-1]['seconds'],
      'nativeFps': film['sound']['frames'] / film['timeline'][-1]['seconds'],
      'audio': {'beats': len(audio), 'allAccepted': all(q['played'] for q in audio),
                'firstGain': audio[0]['gain'], 'lastGain': audio[-1]['gain'],
                'strictlyIncreasing': all(z['gain'] > a['gain'] for a, z in zip(audio, audio[1:]))},
      'playback': play, 'newGenerationCredits': 0,
      'skill': {'path': str(skill), 'validated': True,
                'hashes': {p.relative_to(skill).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in skill.rglob('*') if p.is_file()}},
      'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in files},
      'syntax': {p: 0 for p in files if p.endswith('.js')},
      'requiredSuite': {'exitCode': 1, 'finalSummaryReached': False,
                        'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs',
                        'log': '_shots/dracodia_polish_1026/required-suite.log'}}
(R / 'docs/qa/dracodia_polish_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia loop, fade, sound, speech and body polish - October26

Mike requested smooth initial/download loops, a frame-based25% to100% skeleton
fade before lightning, progressively louder strike sounds, one closing speech
roar/arm lift and an intact first-host body after arm destruction.
[Current audible {qa['seconds']:.2f}s arm-break/transformation/full-speech recording]({url}).
Earlier takes are preserved.

## Runtime

`assets/dracodia_polish_1026.js` loads after RD26. It blends adjacent cyclic
authored poses at32 subframe steps, including last-to-first, using premultiplied
canvas composition. Three reusable source-sized canvases retain the actual
registered art, fixed pivots and proportional scale; no per-pose fitting or new
generated sprites. Rise and download share the existing continuous phase.
Carrier/material/wire loop seams are pixel-continuous. The24 indexed opacity
frames increase the rising carrier from25% to100% before lightning begins.

Every original and ending strike beat receives rising shared-mixer gain.
The ending reuses the approved combatBeam0927 sample/pool through the separately
gated rd27Lightning cue (25ms gate), without adding a sound per secondary bolt.
Original24 native beats remain. {len(audio)} actual recorded releases were accepted,
with strictly increasing requested gain from{audio[0]['gain']:.2f} to{audio[-1]['gain']:.2f}.
Decoded audio is audible at{film['decodedPeakDb']}dB peak; the cinematic has no new
download, synthesized audio or pending effect timers.

The earlier FEAR ME line retains its text and uses face4; only the last line
keeps face5, the authored roar bank and native scream. Native speech runs to
completion into live combat. No dialogue lines are skipped.

## First-host body and arms

The old narrow arm/core strip removed crown/shoulder/body pixels together with
the arms. The owning stage78 builder now preserves the full-width upper body
and shoulders, with a lower anatomical arm seam. The same full512 canvas and
source pixels remain. It also measures90 opaque arm target anchors across45
source poses; native non-muzzle part points use them. Claw muzzle/FOV sockets,
protected33.3/33.3/33.4 budget, actual arm debris and hit flashes remain native.

The fall had a second problem: it returned to an older core-only plate after
core exhaustion. RD27 now draws the same complete connected recovery body
during that native fall, retaining actual destroyed-arm and flash state. The
original fall clock, protected rebirth, position, explosions and progression
remain with their owners.

Rebuild masks/targets/manifests/registry through
`python _BUILD_SOURCE/build_stage78_review_1025.py`. No atlas or paid generation
work was needed. Boss Cinematics has the current recipe and evidence reference.

## Verification

- {len(native['checks'])} native Chromium checks pass: cyclic carrier/material/wire pixels,
  all24 opacity frames, increasing beat gain, exactly one closing roar, actual
  intact upper-body pixels after arm damage, matching full-body fall pixels,
  all90 opaque targets, native health/protection/reveal, real damaged pixels
  and flash expiry, no page/console errors. Native screenshots inspected.
- {len(film['checks'])} recording and {len(play['checks'])} playback checks pass. The film includes staggered
  actual arm breaks, collapse, rising/fading skeleton, download/lightning,
  whiteout, all native speech, one final roar and combat resumption. Decoded
  frames inspected; audio playback and Range seeking pass. Roughly
  {qa['nativeFps']:.1f} native frames/s and no asset errors.
- JS/Python syntax and installed skill validation pass. Required test_fl.js
  exits1 before assertions/final summary due existing missing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs`; this is not a green full suite.

Use probe, recorder and playback helpers with `--polish`. Evidence:
`docs/qa/dracodia_polish_1026.json` and `_shots/dracodia_polish_1026/`.
The film uses explicitly labelled native damage checkpoints; it is not a full
boss fight. No game.js/test_fl.js edits, commit or push.
'''
for a, b in [('based25','based 25'), ('to100','to 100'), ('at32','at 32'), ('The24','The 24'), ('from25','from 25'), ('Original24','Original 24'), ('gain from','gain from '), (' to1',' to 1'), ('at-','at -'), ('face4','face 4'), ('face5','face 5'), ('full512','full 512'), ('measures90','measures 90'), ('across45','across 45'), ('protected33','protected 33'), ('all24','all 24'), ('all90','all 90'), ('exits1','exits 1')]:
    doc = doc.replace(a, b)
(R / 'docs/DRACODIA_POLISH_1026.md').write_text(doc, encoding='utf8')
title = '## October26 - Smooth Dracodia loops, fade, rising sound and intact first host'
note = f'''{title}

Mike's loop/fade/audio/roar/body correction is live in assets/dracodia_polish_1026.js after RD26. Cyclic subframe blending removes carrier/material/wire loop snaps, with shared phase and24 indexed25%-100% intro visibility frames. Native and ending strike beats get increasing shared-mixer gain; only the final speech line owns the native roar/arm lift. The stage78 owning builder preserves full-width crown/shoulders and records90 opaque arm targets across45 poses. The native first-host fall now retains that authored body instead of an old core-only strip. Native health, attacks, flashes, protected reveal and progression remain. Boss Cinematics reference updated/validated; no new paid art.

{len(native['checks'])} native, {len(film['checks'])} recording and {len(play['checks'])} playback checks pass. Fresh audible{qa['seconds']:.2f}s clip includes staggered real arm breaks and full speech through one closing roar; native/decoded pixels and accepted increasing sound releases verified. Notes/QA: docs/DRACODIA_POLISH_1026.md and docs/qa/dracodia_polish_1026.json. Syntax passes; full suite still exits1 before summary on existing missing retired_art_archive_1022.cjs. No game.js/test_fl.js edits, commit or push.

'''.replace('and24','and 24').replace('indexed25','indexed 25').replace('records90','records 90').replace('across45','across 45').replace('audible'+f'{qa["seconds"]:.2f}', 'audible '+f'{qa["seconds"]:.2f}').replace('exits1','exits 1')
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '\n## October26 Dracodia loop/fade/speech/body polish\n\n- RD27 preserves cyclic interpolated carrier/material/wire frames and24-step25%-100% skeleton visibility before lightning. Strike beats increase shared-mixer gain; only the closing speech line owns the roar/arm lift. Keep full-width first-host body pixels after arms break and the same authored recovery body during its fall, with90 registered opaque arm targets across45 poses. Use the stage78 owning builder; preserve native budgets, hit feedback and cinematic progression. Current evidence: docs/DRACODIA_POLISH_1026.md.\n'.replace('and24','and 24').replace('step25','step 25').replace('with90','with 90').replace('across45','across 45')
if b'## October26 Dracodia loop/fade/speech/body polish' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
print(json.dumps({'native': len(native['checks']), 'recording': len(film['checks']),
                  'playback': len(play['checks']), 'audio': qa['audio'], 'video': film['video']}))
