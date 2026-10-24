from pathlib import Path
import shutil,re,os
W=Path(__file__).resolve().parent
candidate=W.parents[1]
R=Path(os.environ.get('BOF_GAME_ROOT',str(candidate if(candidate/'assets/game.js').exists() else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'))))
O=R/'assets/game/shared/combat/encounter_revision_1023';O.mkdir(exist_ok=True)
for f in (W/'art').glob('*'):shutil.copy2(f,O/f.name)
for n in ['encounter_revision_1023.js','encounter_revision_art_1023.js','dracodia_rebirth_1023.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'index.html';s=p.read_text(encoding='utf-8')
for name in ['encounter_revision_art_1023.js','encounter_revision_1023.js','dracodia_rebirth_1023.js','cinematic_director_0930.js','feedback_claude_1003.js','feedback_1002.js','hammer_tactical_1023.js','siege_tanks_1010.js','hammer_furious_1022.js']:
 pattern=r'<script src="assets/'+re.escape(name)+r'(?:\?[^"]*)?"></script>'
 matches=list(re.finditer(pattern,s))
 tag='<script src="assets/'+name+'?v=encounter-review-1024-1"></script>'
 if matches:
  seen=[False]
  def replace_tag(m):
   if seen[0]:return ''
   seen[0]=True;return tag
  s=re.sub(pattern,replace_tag,s)
 else:s=s.replace('</body>',tag+'\n</body>')
p.write_bytes(s.encode('utf-8'));print('Installed authored banks and encounter correction cache versions')
