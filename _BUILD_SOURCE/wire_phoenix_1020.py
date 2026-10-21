from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=R/'_ART_SOURCES/dracodia_download_1019/jobs.json';jobs=json.loads(p.read_text());jobs['volcano']={**jobs['volcano'],'drawing':'5519d03c-45cc-43fc-b5fd-2586fe76d6af','edit':'f56bc2ca-fccf-496c-98e7-a817c63444af','cacheTag':'phoenix_1020','identity':'Corrupted Fire Phoenix'};p.write_text(json.dumps(jobs,indent=2)+'\n')
p=R/'_BUILD_SOURCE/build_dracodia_download_1019.py';s=p.read_text();s=s.replace("name,j=row;d=S/name;d.mkdir(exist_ok=True)","name,j=row;d=S/name/j.get('cacheTag','');d.mkdir(parents=True,exist_ok=True)")
s=s.replace("im=Image.open(S/name/'full.png').convert('RGBA')","im=Image.open(S/name/j.get('cacheTag','')/'full.png').convert('RGBA')")
p.write_text(s,encoding='utf-8',newline='\n');print('Phoenix replaces the volcano wireframe through the owning builder; old sources retained')
