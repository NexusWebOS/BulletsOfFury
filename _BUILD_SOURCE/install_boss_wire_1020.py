from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=R/'_ART_SOURCES/dracodia_download_1019/jobs.json';j=json.loads(p.read_text());
for name,drawing,edit in [('volcano','cf5d6eb6-fa69-4ecc-b374-1e06397e7311','d0551d0c-5e92-49d4-ad4c-3e30e478c8e3'),('hammer','494e9e9e-bf0e-446f-93a4-8777319ae158','bba5d7ab-7e66-4c5b-9473-7f8f0559a40f')]:j[name]={**j[name],'drawing':drawing,'edit':edit,'cacheTag':'boss_redesign_1020','identity':'Whole cannon-pod Phoenix' if name=='volcano' else 'Demonic two-handed code Hammer'}
p.write_text(json.dumps(j,indent=2)+'\n');print('Download mesh jobs match native redesigns')
