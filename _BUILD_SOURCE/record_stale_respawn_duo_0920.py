import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
proof = {'ENG-19': 'RESPAWN_SAFETY_0919.md', 'S1-14': 'RAZORBACK_HANDOFF_0919.md'}
for item in data['items']:
    if item['id'] in proof:
        item['status'] = 'complete'
        item['evidence'] = proof[item['id']]
data['latestBatch'] = {
    'description': 'Reconciled verified respawn safety and Hard Razorback Duo heavy-attack handoff',
    'evidence': 'RESPAWN_SAFETY_0919.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
