"""Archive completed verification and prepend notes without rewriting history."""
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parents[1]
O = R / '_shots/campaign_controls_1004h'
reports = {name: json.loads((O / file).read_text()) for name, file in [
    ('map_storage', 'checks.json'), ('pointer_pad_hub', 'slot-checks.json')
]}
for report in reports.values():
    assert all(c['ok'] for c in report['checks']) and not report['errors']
log = (R / '_shots/campaign_controls_1004h_suite.log').read_text()
assert 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in log
count = len(re.findall(r'^\s*ok\s', log, re.M))
browser_count = sum(len(r['checks']) for r in reports.values())
assert count == 7160 and browser_count == 98
q = {
    'date': '2026-10-04',
    'scope': 'Campaign navigation, Stage VI/X travel, Start menu ownership and persistent manual/autosave load flows',
    'suite': {'assertions': count, 'exit': 0, 'final_summary': 'FALVA/LIZZIE BUILD OK, 0 ERRORS'},
    'syntax': {'assets/game.js': 'exit 0', 'assets/campaign_controls_1004h.js': 'exit 0'},
    'native': reports,
    'native_checks': browser_count,
    'review': '_shots/campaign_controls_1004h/review.html',
    'live_game': 'index.html?build=campaign-controls-1004h',
    'review_storage_namespace': 'bof_map_review_1004h_',
    'art': 'assets/game/shared/campaign/campaign_controls_1004h/manifest.json',
    'prompt': '_ART_SOURCES/campaign_controls_1004h/prompt.json',
    'screenshots_inspected': ['save-slots.png', 'load-slots.png', 'compact-save.png', 'pointer-save.png', 'auto-load.png', 'hub-save.png'],
    'limitations': 'Normalized gamepad events are injected, not physical hardware. No full campaign-clear or combat-balance claim.',
    'corrected_probe_fixtures': ['Hidden HUD canvas selector changed to #screen', 'pad_b12/13 changed to normalized pad_up/down'],
}
(R / 'docs/qa/campaign_controls_1004h.json').write_text(json.dumps(q, indent=2) + '\n', encoding='utf-8')
note = f'October 4 campaign controls and save slots: [Navigation, menu ownership and persistent saves](docs/CAMPAIGN_CONTROLS_1004H.md). Left I→VIII→VII→VI works; III→IV points down; Up VI→X / Down X→VI moves the actual ship. Start opens Save/Load/Exit before Stage X reads input; slots own Up/Down and B returns to the menu. Manual writes verify bytes, retain selected map stage/bonus/X focus and survive reload. Generated blank chrome cartridges with authored font/ships; campaign hub and autosave verified. Review demo slots persist separately from live saves. {count:,} full-suite assertions, exit 0; {browser_count} native Chromium checks, zero browser errors. Review _shots/campaign_controls_1004h/review.html; QA docs/qa/campaign_controls_1004h.json. Local only; preserve all earlier work.'
for name in ['HANDOFF_CODEX.md', 'CLAUDE.md']:
    p = R / name
    b = p.read_bytes()
    if not b.startswith(b'October 4 campaign controls and save slots:'):
        p.write_bytes((note + '\r\n\r\n').encode('utf-8') + b)
print(count, 'suite assertions;', browser_count, 'browser checks archived.')
