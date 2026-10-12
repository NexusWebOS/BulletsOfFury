"""Publish bounded native evidence for the October 11 recording pass."""
from pathlib import Path
import hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / '_shots/playthrough_1011'
PREVIEW = ROOT / 'docs/previews/playthrough_1011'
CAPTURES = PREVIEW / 'captures'
CAPTURES.mkdir(parents=True, exist_ok=True)

files = {
    'runtime': ['armored-command-stage6.png'],
    'ui': ['armored-coop.png', 'cockpit-live.png', 'title-flight.png'],
    'encounters': ['ice-carrier-modular.png', 'hammer-new-reactor.png',
                   'storm-northbound-pursuit.png'],
    'routes': ['chaos-harrier.png', 'toxic-pressure-salvo.png'],
    'finale': ['host-shoulder-beam.png', 'drone-raised-takeover.png',
               'heart-beating.png', 'ghost-multilock.png'],
    'weapons': ['fire-forge-comparison.png', 'sonic-forge-preview.png', 'fire-live-contact.png'],
}
for folder, names in files.items():
    for name in names:
        shutil.copy2(SHOTS / folder / name, CAPTURES / name)

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

suites = {name: read(SHOTS / name / 'report.json')
          for name in ('runtime', 'ui', 'routes', 'encounters', 'finale', 'weapons')}
copied = read(ROOT / 'docs/qa/hardcorps_finale_patterns_1007.json')
checks = copied['checks']
passed = sum(x['passed'] for x in suites.values())
failed = sum(x['failed'] for x in suites.values())
copied_pass = sum(bool(c['ok']) for c in checks)
log = (SHOTS / 'final-regression.log').read_text(encoding='utf-8-sig')
assertions = len(re.findall(r'^  ok ', log, re.M))
assert '==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in log
assert not failed and copied_pass == len(checks)
assert all(not s['errors'] for s in suites.values()) and not copied['errors']

launch = read(SHOTS / 'launchscale.json')['1']
rec = launch['rec']
heights = [h for r in rec for _, h in r['ship']]
play_heights = [h for r in rec if r['st'] == 'play' for _, h in r['ship']]
manifest = read(ROOT / 'assets/game/shared/combat/playthrough_1011/manifest.json')
owners = ['assets/game.js', 'assets/playthrough_1011.js', 'assets/playthrough_finale_1011.js',
          'assets/playthrough_ui_1011.js', 'assets/armored_command_1011.js',
          'assets/part2_motion_1011.js', 'assets/hardcorps_finale_patterns_1007.js',
          'assets/game/shared/combat/playthrough_1011/manifest.json']
report = {
    'date': '2026-10-11',
    'summary': (f'{assertions:,} regression assertions pass (exit 0). '
                f'{passed} recording-specific native checks and {copied_pass} copied-form '
                'native checks pass with no browser errors. '
                'The review is based on bounded encounters and rendering fixtures; '
                'a human campaign clear and the open ledger items remain.'),
    'source': {'file': '2026-10-11 12-24-48.mp4', 'durationSeconds': 3954.367,
               'sha256': '23bd7a46942a982c4f42ad4047fc187f4adce3f429b30c41e6dfa77e9bb49a1f',
               'method': 'Local full-audio transcription, targeted redecodes, 198 overview captures and targeted action captures.'},
    'regression': {'command': 'node _BUILD_SOURCE/test_fl.js', 'assertions': assertions,
                   'failures': 0, 'exitCode': 0, 'finalSummary': True,
                   'baselineAssertions': 8670, 'baselineFailures': 0,
                   'log': '_shots/playthrough_1011/final-regression.log',
                   'testMaintenance': 'Superseded Walker/buoy roster and renamed pilot special expectations updated; no gameplay failures excluded.'},
    'native': suites,
    'copiedForms': {'passed': copied_pass, 'failed': len(checks)-copied_pass,
                    'errors': copied['errors'], 'report': 'docs/qa/hardcorps_finale_patterns_1007.json'},
    'launch': {'stage': 1, 'pilot': 'maverick', 'firstPlayFrame': next(i for i, r in enumerate(rec) if r['st']=='play'),
               'measuredFrames': len(rec), 'minShipHeight': min(heights), 'maxShipHeight': max(heights),
               'firstPlayHeight': play_heights[0], 'offScaleBlits': sum(h != 60 for h in heights),
               'errors': launch['errors']},
    'generatedArt': {'bankCounts': {k: len(v) for k, v in manifest.items()},
                     'totalCells': sum(map(len, manifest.values())), 'cinematicPlates': 2,
                     'build': '_BUILD_SOURCE/build_playthrough_art_1011.py',
                     'provenance': '_ART_SOURCES/playthrough_1011/'},
    'openItems': [
        'The two small green shapes at 41:34-41:43 strongly match loose Maverick missile-ammo drops (msl_2_2), not an enemy owner. Mike is being asked whether to replace their pickup art or remove those loose Stage 6 ammo drops. Other aircraft remain.',
        'The reported 09:58-10:12 firing/scroll interruption has not been reproduced in the current build; ordinary pellets remain unshootable.',
        'Full human campaign balance/clear, including Stage 6 encounter progression and all final copied forms, remains.'
    ],
    'hashes': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in owners},
    'captures': [str((CAPTURES / n).relative_to(ROOT)).replace('\\','/') for names in files.values() for n in names],
    'publication': 'Local working tree only. No commit or push.',
}
matrix=read(ROOT/'_shots/element_arsenal_1011/live/checks.json')
assert not matrix['errors'] and all(c['passed'] for c in matrix['checks'])
report['elementMatrix']={'cases':len(matrix['rows']),'passed':len(matrix['checks']),'failed':0,'errors':[],
                        'report':'_shots/element_arsenal_1011/live/checks.json'}
preview_report = SHOTS / 'review/report.json'
if preview_report.exists():
    report['reviewPage'] = read(preview_report)
(ROOT / 'docs/qa/playthrough_1011.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'assertions': assertions, 'native': passed, 'copiedForms': copied_pass,
                  'cells': report['generatedArt']['totalCells'], 'captures': len(report['captures'])}))
