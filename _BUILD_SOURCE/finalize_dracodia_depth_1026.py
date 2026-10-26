"""Archive the verified depth-download release without replacing earlier evidence."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_depth_1026'
native = json.loads((O / 'probe/report.json').read_text())
latest = json.loads((O / 'video/latest.json').read_text())
folder = Path(latest['folder'])
film = json.loads(Path(latest['report']).read_text())
play = json.loads((folder / 'playback.json').read_text())
manifest = json.loads((R / '_BUILD_SOURCE/dracodia_depth_1026/manifest.json').read_text())
assert all(q['passed'] for q in native['checks'])
assert all(film['checks'].values()) and all(play['checks'].values())
sources = [
    'assets/dracodia_depth_1026.js', 'assets/dracodia_depth_art_1026.js',
    'assets/dracodia_download_reveal_1025.js', 'index.html',
    '_BUILD_SOURCE/build_dracodia_depth_1026.py',
    '_BUILD_SOURCE/probe_dracodia_download_reveal_1025.py',
    '_BUILD_SOURCE/record_dracodia_transformation_1025.py',
    '_BUILD_SOURCE/check_dracodia_transformation_video_1025.py',
]
seconds = film['timeline'][-1]['seconds']
qa = {
    'scope': 'Upright depth-turning Dracodia download, overhead lightning strikes and front/rear electrical helices',
    'native': {'passed': len(native['checks']), 'failed': 0,
               'report': '_shots/dracodia_depth_1026/probe/report.json',
               'checks': native['checks']},
    'video': {'path': film['video'], 'seconds': seconds,
              'decodedPeakDb': film['decodedPeakDb'],
              'nativeFps': film['sound']['frames'] / seconds,
              'checks': film['checks'], 'chapters': film['chapters'],
              'report': Path(latest['report']).relative_to(R).as_posix()},
    'playback': play,
    'art': {'manifest': '_BUILD_SOURCE/dracodia_depth_1026/manifest.json',
            **{k: manifest[k] for k in ['source_asset_id', 'animation_asset_id', 'job_id',
                                        'model', 'generated_frames', 'runtime_frames',
                                        'credits_used', 'source_sha256', 'reference_sha256']}},
    'syntax': {p: 0 for p in ['assets/game.js', 'assets/dracodia_download_reveal_1025.js',
                              'assets/dracodia_depth_1026.js', 'assets/dracodia_depth_art_1026.js']},
    'requiredSuite': {'command': 'node _BUILD_SOURCE/test_fl.js', 'exitCode': 1,
                      'finalSummaryReached': False,
                      'reason': 'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs aborts before assertions.'},
    'sourceHashes': {p: hashlib.sha256((R / p).read_bytes()).hexdigest() for p in sources},
    'method': 'Real Chromium native loop and actual drawImage pixels. Explicit native damage starts the recorded checkpoint; no transformation timers or phases are skipped. Native speech finishes before a separate real damage/hit-expiry fixture.',
}
(R / 'docs/qa/dracodia_depth_1026.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf8')
url = 'http://127.0.0.1:53746/' + film['video']
doc = f'''# Dracodia depth download — October26

Mike requested downward lightning strikes, electricity swirling around the body,
and new forming views that turn in depth like the floating skeletal carrier.
[Current audible 36-second recording]({url}). Earlier recordings are preserved.

`assets/dracodia_depth_1026.js` loads after the existing download owner and its
new art registry. The body remains upright while front, profile and armored-back
poses rotate around its vertical axis. The original 24-pose skeletal carrier
stays visible inside unbuilt bands. Completed bands reveal the matching material
view; the final front view blends into the actual native ce20Body renderer before
the whiteout. A shared chest anchor, native scale and continuous position carry
the completed body into speech.

The electrical wrap uses separate rear and foreground helix passes around the
body. Main strikes start above the playfield and travel downward through and
below the assembly. Both use the existing authored blue lightning art. Native
24-beat timing and shared-mixer lightning cues remain; there are no extra queued
sounds or new damage owners. Five form pools, protection, the 25.6s arena reveal,
28.5s speech handoff, native combat hits and defeat remain with their existing
owners. The fusion cue remains combatEnergy0927.

## Art and rebuild

SpriteCook pixel-engine-v1.5 generated 12 transparent 286x286 poses from the
exported actual 320x320 final-body reference. The paid job used 26 credits.
Reference asset: `{manifest['source_asset_id']}`.
Animation asset: `{manifest['animation_asset_id']}`.
Job: `{manifest['job_id']}`.

The compiler selects source poses 0–8 from front to back, then reflects 7–1 for
the opposite half. This produces 16 continuous depth views without the generated
late back-to-front jump. Every cell uses the same 512x512 canvas, 256,256 pivot,
one scale of 1 and fixed 113,117 source translation. There is no per-frame fitting.
The wire layer comes from the source alpha edges/material creases. Original and
normalized contact sheets were inspected before native activation.

Run `python _BUILD_SOURCE/build_dracodia_depth_1026.py` to reproduce the two
2048x2048 sheets, art registry and registered taxonomy entry. Source files,
generation settings, hashes, source selection and runtime cells are in
`_BUILD_SOURCE/dracodia_depth_1026/`; runtime copies and manifest are under
`assets/game/levels/stage_08/boss/dracodia_depth_1026/`. No signed URLs, new atlas
edits or generated player aircraft are involved.

## Verification

- {len(native['checks'])} native Chromium checks pass, including actual depth-view pixels,
  narrower profiles, different back art, upright orientation, visible rear/front
  swirl pixels, downward strikes, all 24 native beats, preserved health pools,
  continuous speech position, actual white hit pixels and normal flash expiry.
  The first carrier matches exactly; the completed renderer comparison differs
  by 62 pixels on its 245760-pixel capture, within the existing render tolerance.
- All {len(film['checks'])} recording checks and {len(play['checks'])} playback checks pass. The {seconds:.2f}s film
  fully decodes, has {film['decodedPeakDb']}dB audible sound, runs at roughly
  {qa['video']['nativeFps']:.1f} native frames/s, and plays/seeks with audio in Chromium.
  The decoded film contact sheet was inspected. No page, console or asset errors.
- JavaScript syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits 1
  before assertions/final summary because the existing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs` helper is missing.

Reproduce with the existing probe, recorder and playback helper, each with
`--depth`: `probe_dracodia_download_reveal_1025.py`,
`record_dracodia_transformation_1025.py`, and
`check_dracodia_transformation_video_1025.py` under `_BUILD_SOURCE/`.
Evidence: `docs/qa/dracodia_depth_1026.json` and `_shots/dracodia_depth_1026/`.
The video is a native-damage transformation checkpoint, not a full boss fight.
This pass did not edit game.js/test_fl.js, commit or push.
'''
(R / 'docs/DRACODIA_DEPTH_1026.md').write_text(doc, encoding='utf8')
title = '## October26 — Upright Dracodia depth download and surrounding lightning'
note = f'''{title}

Mike requested real depth rotation during formation, overhead strikes and surrounding electricity. assets/dracodia_depth_1026.js now uses 16 normalized front/profile/back poses from a SpriteCook turntable while the original skeletal carrier remains inside unbuilt bands. Separate rear/front authored-lightning helices wrap the upright body; main bolts strike downward. Final front material blends into the native body before whiteout and continues into speech. All 24 native beats, health pools, audio, protection and defeat remain. Source assets/settings, 26-credit job, fixed 512 cells/pivot and rebuild ownership are archived; see docs/DRACODIA_DEPTH_1026.md.

{len(native['checks'])} native checks, {len(film['checks'])} recording checks and {len(play['checks'])} playback checks pass; fresh {seconds:.2f}s audible film inspected. Actual damaged pixels/expiry and continuous handoff verified, no browser/asset errors. QA: docs/qa/dracodia_depth_1026.json. Syntax passes; required full suite exits 1 before assertions/summary on existing missing retired_art_archive_1022.cjs. No game.js/test_fl.js edits, commit or push.

'''
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    raw = p.read_bytes()
    if title.encode() not in raw:
        p.write_bytes((note.replace('\n', '\r\n') if b'\r\n' in raw else note).encode() + raw)
p = R / 'AGENTS.md'
raw = p.read_bytes()
rule = '''\n## October26 Dracodia depth download

- assets/dracodia_depth_1026.js supersedes flat rolling during the protected download: upright front/profile/back poses, one shared chest pivot/scale, native final-body handoff. Keep the skeletal carrier in unbuilt bands, separate rear/front electric helices and overhead downward strikes, all 24 native beats/audio and native health/reveal/death owners. Rebuild the source-derived 512-cell art through _BUILD_SOURCE/build_dracodia_depth_1026.py. See docs/DRACODIA_DEPTH_1026.md.
'''
if b'## October26 Dracodia depth download' not in raw:
    p.write_bytes(raw + (rule.replace('\n', '\r\n') if b'\r\n' in raw else rule).encode())
p = R / 'docs/DRACODIA_DOWNLOAD_REVEAL_1025.md'
raw = p.read_bytes()
link = '''Current October26 revision adds upright front/profile/back formation, overhead
strikes and surrounding lightning. See [depth download and current recording](DRACODIA_DEPTH_1026.md).
The October25 notes and film below preserve the earlier revision.

'''
if b'DRACODIA_DEPTH_1026.md' not in raw:
    end = raw.index(b'\n\n') + 2 if b'\r\n' not in raw else raw.index(b'\r\n\r\n') + 4
    p.write_bytes(raw[:end] + (link.replace('\n', '\r\n') if b'\r\n' in raw else link).encode() + raw[end:])
print(json.dumps({'native': len(native['checks']), 'film': len(film['checks']),
                  'playback': len(play['checks']), 'video': film['video']}))
