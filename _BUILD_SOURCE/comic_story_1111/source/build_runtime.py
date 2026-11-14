from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
story=json.loads((P/'source/human-story.json').read_text(encoding='utf8'))
runtime=(P/'source/comic_story_1111.js').read_text(encoding='utf8').replace('__STORY__',json.dumps(story,separators=(',',':')))
(P/'overlay/assets/comic_story_1111.js').write_text(runtime,encoding='utf8')
print('Built human comic runtime')
