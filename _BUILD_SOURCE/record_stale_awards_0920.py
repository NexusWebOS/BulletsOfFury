import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'docs/REQUEST_CHECKLIST_0914.json'
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
data = json.loads(raw.decode('utf-8'))
for item in data['items']:
    if item['id'] == 'ACH-02':
        item['status'] = 'complete'
        item['request'] = ('Achievement title button and gallery, plus a queued unlock card that rises, '
            'holds, then slides/fades down at lower left, per Mike\'s later 0916 placement.')
        item['evidence'] = 'AWARDS_0916.md'
        item['dependency'] = ''
data['latestBatch'] = {
    'description': 'Reconciled completed achievement gallery and the later-approved lower-left unlock card',
    'evidence': 'AWARDS_0916.md',
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8').replace(b'\n', newline))
