"""Save the verified accelerating/covered-reveal revision and skill receipt."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_climax_1026'
native = json.loads((O / 'probe/report.json').read_text(encoding='utf8'))
latest = json.loads((O / 'video/latest.json').read_text(encoding='utf8'))
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text(encoding='utf8'))
play = json.loads((folder / 'playback.json').read_text(encoding='utf8'))
skill = json.loads((O / 'skill-install.json').read_text(encoding='utf8'))
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
base = json.loads((O / 'baseline-hashes.json').read_text(encoding='utf8'))
assert all(hashlib.sha256((R / p).read_bytes()).hexdigest() == h for p, h in base.items())
sources = ['assets/dracodia_depth_1026.js', 'assets/dracodia_download_reveal_1025.js',
           'index.html', '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py',
           '_BUILD_SOURCE/record_dracodia_transformation_1025.py',
           '_BUILD_SOURCE/check_dracodia_transformation_video_1025.py']
seconds = film['timeline'][-1]['seconds']
qa = {
    'scope': 'Accelerating continuous depth loops, complete body concealed until peak flash, cinematic strikes across the playfield, and installed Boss Cinematics skill',
    'native': {'passed': len(native['checks']), 'failed': 0, 'checks': native['checks'],
               'report': '_shots/dracodia_climax_1026/probe/report.json'},
    'video': {'path': film['video'], 'seconds': seconds, 'decodedPeakDb': film['decodedPeakDb'],
              'nativeFps': film['sound']['frames'] / seconds, 'checks': film['checks'],
              'chapters': film['chapters'], 'report': Path(latest['report']).relative_to(R).as_posix()},
    'playback': play, 'skill': skill, 'newGenerationCredits': 0,
    'syntax': {'assets/game.js': 0, 'assets/dracodia_depth_1026.js': 0},
    'sharedSourceHashesPreserved': base,
    'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in sources},
    'requiredSuite': {'command': 'node _BUILD_SOURCE/test_fl.js', 'exitCode': 1,
                      'finalSummaryReached': False, 'log': '_shots/dracodia_climax_1026/required-suite.log',
                      'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs aborts before assertions.'},
    'method': 'Native Chromium, actual drawImage pixels, separate native-damage checkpoint, continuous audible recording with no phase/timer skips, decoded frame inspection and Chromium playback/seeking.',
}
(R / 'docs/qa/dracodia_climax_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia accelerating cinematic reveal - October26

Mike requested continuous faster loops, a complete-body reveal after the light
flashes, and additional dramatic strikes across the screen. This supersedes
the earlier preflash settling/material handoff in DRACODIA_DEPTH_1026.md.
[Current audible {seconds:.2f}s transformation recording]({url}). Earlier takes remain.

`assets/dracodia_depth_1026.js` keeps one integrated unwrapped phase from the
existing 20/24 revolutions/s carrier. Angular speed increases by 0.15 revolutions/s
each second, reaching about 2.57 revolutions/s at peak whiteout. Both banks index
that shared phase with modulo, retaining the 16 authored depth views and all
24 original carrier views. There is no late front-facing pause or deceleration.

Download percentage and visible material are separate. Visible material stays
at most 86% complete (111 of 128 scan bands); the remainder keeps the rotating
wire/carrier, including after the data reaches 100%. The actual native completed
body is never drawn before 25.6s. Only after the authored whiteout is fully opaque
does it replace the turning assembly at the same anchor and native scale. The
body becomes visible as the light clears after 25.9s and continues into native
speech at 28.5s.

Rear/front electric helices remain. Additional downward channels strike across
nine playfield lanes, away from the boss, with a quicker three-channel climax.
They reuse authored r25Bolt art and are non-damaging silent visual partners to
the existing 24 native lightning/audio beats. Native HP/form pools, portal,
protection, arena swap, speech, hit feedback and defeat/rewards remain unchanged.
This revision reuses the existing generated art and spends no generation credits.

## Boss Cinematics skill

The validated personal skill is installed at
`C:/Users/Mdogg/.codex/skills/boss-cinematics/SKILL.md` with display name
**Boss Cinematics** and invocation `$boss-cinematics`. It covers continuous
registered assembly, real depth loops and acceleration, concealed complete-body
reveals, layered surrounding electricity, distributed cinematic strikes and
native recorded visual/audio verification. A focused Bullets of Fury reference
records the actual owners, asset pivots, timings, build workflow and probe paths.
The staged source and installation hashes are under this revision's `_shots/`.

## Verification

- {len(native['checks'])} native checks pass. Actual partial rendering makes zero native complete-body
  calls at 24.7s, 25.22s and 25.59s. All 16 poses remain in the late accelerated
  loop. Actual distant-strike pixels, both helix layers and nine lanes pass.
  Native health, protection, one arena/speech handoff, damaged pixels and flash
  expiry pass, with no browser/asset errors. Native screenshots inspected.
- {len(film['checks'])} recording checks and {len(play['checks'])} playback checks pass. The film fully decodes with
  {film['decodedPeakDb']}dB sound at about {qa['video']['nativeFps']:.1f} native frames/s. Decoded preflash,
  peak-flash and clearing-light frames were inspected; play/seek works in Chromium.
- Skill validation passes for the installed files. JavaScript/Python syntax and
  scoped whitespace pass. game.js and test_fl.js hashes are preserved.
- Required `node _BUILD_SOURCE/test_fl.js` exits 1 before assertions/final summary
  on existing missing `_BUILD_SOURCE/retired_art_archive_1022.cjs`; it is not green.

Run the existing probe, recorder and playback helper with `--climax`:
`probe_dracodia_download_reveal_1025.py`, `record_dracodia_transformation_1025.py`,
`check_dracodia_transformation_video_1025.py`, all under `_BUILD_SOURCE/`.
Evidence: `docs/qa/dracodia_climax_1026.json` and `_shots/dracodia_climax_1026/`.
The film is a transformation checkpoint using explicit native arm/core damage,
not a full fight. No commit or push.
'''
(R / 'docs/DRACODIA_CLIMAX_1026.md').write_text(doc, encoding='utf8')
title = '## October26 - Accelerating Dracodia loops and flash-covered reveal'
note = f'''{title}

Mike's latest correction is live in assets/dracodia_depth_1026.js: one integrated accelerating rotation phase through peak whiteout, no late settling pause, visible scan material capped at 86% until full cover, and actual native body introduced only under the fully opaque 25.6s flash. It appears as the light clears and continues into native speech. Nine playfield lanes now receive distant downward lightning alongside the rear/front helix and core strikes; native 24-beat audio and all gameplay ownership remain. No new art generation. Boss Cinematics is installed and validated at C:/Users/Mdogg/.codex/skills/boss-cinematics/SKILL.md.

{len(native['checks'])} native, {len(film['checks'])} recording and {len(play['checks'])} playback checks pass; new audible {seconds:.2f}s clip and decoded flash/formation frames inspected. Notes/QA: docs/DRACODIA_CLIMAX_1026.md and docs/qa/dracodia_climax_1026.json. Syntax passes; required full suite exits 1 before assertions/summary due existing missing retired_art_archive_1022.cjs. game.js/test_fl.js hashes unchanged. No commit/push.

'''
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '''\n## October26 Dracodia accelerating flash reveal

- Mike's latest revision supersedes preflash settling: keep depth rotation accelerating and cyclic through peak whiteout, retain incomplete carrier/wire scan bands until full cover, and show the complete native body only as the flash clears. Preserve rear/front surrounding electricity, additional downward strikes across the playfield, all 24 native audible beats and native gameplay owners. Boss Cinematics is the personal reusable skill; current implementation/evidence: docs/DRACODIA_CLIMAX_1026.md.
'''
if b'## October26 Dracodia accelerating flash reveal' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
p = R / 'docs/DRACODIA_DEPTH_1026.md'
raw = p.read_bytes()
link = '''Latest revision: [accelerating loops, flash-covered reveal and Boss Cinematics skill](DRACODIA_CLIMAX_1026.md).
It supersedes the preflash settling described below; this earlier evidence remains archived.

'''
if b'DRACODIA_CLIMAX_1026.md' not in raw:
    end = raw.index(b'\r\n\r\n') + 4 if b'\r\n' in raw else raw.index(b'\n\n') + 2
    p.write_bytes(raw[:end] + (link.replace('\n', '\r\n') if b'\r\n' in raw else link).encode() + raw[end:])
print(json.dumps({'native': len(native['checks']), 'film': len(film['checks']),
                  'playback': len(play['checks']), 'video': film['video'], 'skill': skill['path']}))
