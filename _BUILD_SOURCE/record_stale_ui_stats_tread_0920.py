import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
proof = {'UI-21': 'STATS_FIT_0919.md', 'S1-18': 'RAZORBACK_TREAD_RECORDING_0919.md'}
for item in data['items']:
    if item['id'] in proof:
        item['status'] = 'complete'
        item['evidence'] = proof[item['id']]
data['latestBatch'] = {
    'description': 'Reconciled already-verified Stage Clear stats fit and Razorback recorded tread audio',
    'evidence': 'STATS_FIT_0919.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
