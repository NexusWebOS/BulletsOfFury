import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
for item in data['items']:
    if item['id'] in ('UI-19', 'UI-22'):
        item['status'] = 'complete'
        item['evidence'] = 'LOADOUT_CATALOG_0920.md'
data['latestBatch'] = {
    'description': 'Loadout weapon and element paging, selected-form glow and explicit ownership/price state',
    'evidence': 'LOADOUT_CATALOG_0920.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
