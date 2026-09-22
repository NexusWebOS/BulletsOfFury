import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
for item in data['items']:
    if item['id'] == 'S4-16':
        item['status'] = 'complete'
        item['evidence'] = 'ESCAPE_ARROWS_0916.md'
        item['dependency'] = ''
data['latestBatch'] = {
    'description': 'Reconciled measured Stage-4 giant-strike escape arrows and synchronized alert cues',
    'evidence': 'ESCAPE_ARROWS_0916.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
