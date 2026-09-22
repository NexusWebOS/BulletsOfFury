import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
for item in data['items']:
    if item['id'] == 'ENG-23':
        item['request'] = ('Audit and repair the Forge/weapon upgrade loop. The Stage-1-to-2 boss reward, '
            'two combines, re-spec, Loadout swap, death persistence, audible UI cues, campaign manual-slot '
            'and autosave round-trips, and Stage-3 entry have Chromium proof. Later boss rewards and full '
            'natural-play combinations still need review.')
        item['evidence'] = 'FORGE_REWARD_AUDIT_0920.md'
data['latestBatch'] = {
    'description': 'Forge manual-slot and autosave persistence with Stage-3 entry reapplication',
    'evidence': 'FORGE_REWARD_AUDIT_0920.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
