from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;work=W.parent.resolve();data=json.loads((W/'working-cache-cleanup.json').read_text())
for q in data['files']:
 p=Path(q['temporary']).resolve();source=Path(q['canonical']);assert p.is_relative_to(work)and hashlib.sha256(source.read_bytes()).hexdigest()==q['sha256'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(source,p)
print('Restored verified historical working exports from canonical source archives.')
