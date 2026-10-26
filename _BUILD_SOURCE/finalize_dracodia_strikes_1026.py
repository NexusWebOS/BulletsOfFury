"""Archive the fixed-channel, accelerating-strikes correction."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_strikes_1026'
native = json.loads((O / 'probe/report.json').read_text(encoding='utf8'))
latest = json.loads((O / 'video/latest.json').read_text(encoding='utf8'))
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text(encoding='utf8'))
play = json.loads((folder / 'playback.json').read_text(encoding='utf8'))
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
sources = ['assets/dracodia_depth_1026.js', 'index.html',
           '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py',
           '_BUILD_SOURCE/record_dracodia_transformation_1025.py',
           '_BUILD_SOURCE/check_dracodia_transformation_video_1025.py']
skill = Path('C:/Users/Mdogg/.codex/skills/boss-cinematics')
qa = {'native': {'passed': len(native['checks']), 'checks': native['checks']},
      'video': {k: film[k] for k in ['video', 'checks', 'chapters', 'decodedPeakDb']},
      'playback': play, 'skill': str(skill),
      'skillHashes': {p.relative_to(skill).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in skill.rglob('*') if p.is_file()},
      'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in sources},
      'syntax': {'assets/game.js': 0, 'assets/dracodia_depth_1026.js': 0},
      'requiredSuite': {'exitCode': 1, 'finalSummaryReached': False,
                        'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs',
                        'log': '_shots/dracodia_strikes_1026/required-suite.log'}}
(R / 'docs/qa/dracodia_strikes_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia independent lightning strikes - October26

Mike clarified that only the surrounding lightning should spiral at the ending.
The main lightning should strike faster and faster without spinning with him.
[Current audible recording]({url}). Earlier takes remain preserved.

`assets/dracodia_depth_1026.js` now locks every downward channel's endpoints
for its strike. Core channels use fixed vertical playfield positions; distant
channels select a non-circular permutation of nine lanes with beat-locked bends.
Neither geometry uses the boss yaw or a frame-by-frame orbital clock.

The ending uses an independent integrated clock: at elapsed u after23s,
phase=5u+3u*u and rate=5+6u. Cadence accelerates from5 to20.6 strikes/s through
the25.6s flash. Each beat fades and releases for its last28%, rather than leaving
a continuously moving electrical curtain. Extra channels remain silent visual
partners to the original24 native audible beats.

Only the surrounding rear/front helix spirals, appearing during the final storm
from23s and running on its own clock. The boss keeps the already approved
accelerating depth loop and incomplete preflash assembly. Complete native form
still appears only after full whiteout cover. All health, protection, arena,
speech, hit feedback and defeat ownership remain native.

Boss Cinematics was updated and validated with the fixed-channel/independent
cadence guidance and current project reference. No new art generation or audio
routes, game.js/test_fl.js edits, commit or push.

## Verification

{len(native['checks'])} native checks pass, including actual distant-strike and helix pixels,
identical channel geometry at different boss yaws within one beat, increasing
independent cadence, release intervals, spiral absent before the final storm,
all depth poses, delayed complete-body reveal, native health/hits/flash expiry
and no page/console errors. Native screenshots inspected.

All{len(film['checks'])} recording checks and{len(play['checks'])} playback checks pass. The continuous audible
film fully decodes, and its decoded frames were inspected. Browser playback and
Range seeking pass with no asset or browser errors. Required full suite still
exits1 before assertions/final summary due existing missing
`_BUILD_SOURCE/retired_art_archive_1022.cjs`; syntax checks pass.

Use the existing probe, recorder and playback helper with `--strikes`.
Evidence: `docs/qa/dracodia_strikes_1026.json` and `_shots/dracodia_strikes_1026/`.
The film is an explicit native-damage transformation checkpoint, not a full fight.
'''
doc = doc.replace('after23','after 23').replace('from5','from 5').replace('to20','to 20').replace('the25','the 25').replace('last28','last 28').replace('original24','original 24').replace('from23','from 23').replace('exits1','exits 1').replace('All'+str(len(film['checks'])),'All '+str(len(film['checks']))).replace('and'+str(len(play['checks'])),'and '+str(len(play['checks'])))
(R / 'docs/DRACODIA_STRIKES_1026.md').write_text(doc, encoding='utf8')
title = '## October26 - Fixed downward channels and accelerating ending strikes'
note = f'''{title}

Mike clarified that only the surrounding ending electricity spirals. RD26 downward channels now lock their geometry per strike independently of boss yaw; distant channels jump across nine non-circular lanes. A separate integrated clock accelerates ending strikes from 5 to 20.6/s, with distinct pulse release intervals. The rear/front spiral appears only during the final storm. Boss acceleration, concealed final-form reveal and all native gameplay/audio ownership remain. Boss Cinematics updated/validated. {len(native['checks'])} native, {len(film['checks'])} recording and {len(play['checks'])} playback checks pass; new audible film and native/decoded frames inspected. Syntax passes; full suite still exits 1 before summary due existing missing retired_art_archive_1022.cjs. Docs/QA: docs/DRACODIA_STRIKES_1026.md and docs/qa/dracodia_strikes_1026.json. No game.js/test_fl.js edits, commit or push.

'''
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '\n## October26 independent Dracodia lightning\n\n- Only the surrounding ending lightning spirals. Downward channels remain fixed per strike, independent of boss yaw; their separate cadence accelerates through the climax with release intervals. Preserve nine distant lanes, native audible beats and the flash-covered final-body reveal. Current notes: docs/DRACODIA_STRIKES_1026.md.\n'
if b'## October26 independent Dracodia lightning' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
print(json.dumps({'native': len(native['checks']), 'recording': len(film['checks']),
                  'playback': len(play['checks']), 'video': film['video']}))
