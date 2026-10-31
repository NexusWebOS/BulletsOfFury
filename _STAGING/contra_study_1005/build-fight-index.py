"""Index the complete numbered atlas without fabricating source timings."""
from pathlib import Path
import json, re
root = Path(__file__).resolve().parent
entries = {}
for line_number, line in enumerate((root/'BOSS_FIGHT_ATLAS.md').read_text(encoding='utf-8').splitlines(), 1):
    match = re.match(r'^## (\d{2})([a-z]?)\b(.*)', line)
    if not match:
        continue
    number = int(match[1])
    entries.setdefault(number, {'number':number, 'review':'sequential visual replay of the shown fight', 'sections':[]})['sections'].append({'id':match[1]+match[2], 'title':match[3].strip(' —'), 'atlasLine':line_number})
assert sorted(entries) == list(range(1,36)), sorted(entries)
data = {'source':{'url':'https://www.youtube.com/watch?v=iooQeqdyB8E', 'title':'Contra: Hard Corps (Genesis) All Bosses (No Damage)', 'creator':'Shadowserg'}, 'date':'2026-10-06', 'numberedEncounters':35, 'scope':'Shown attacks and responses; not exhaustive source AI or measured hitboxes/timing. Audio not analysed.', 'atlas':'BOSS_FIGHT_ATLAS.md', 'entries':list(entries.values())}
(root/'fight-index.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'Indexed {len(entries)} numbered encounters in {sum(len(e["sections"]) for e in entries.values())} sections.')
