from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/encounter_cleanup_0914/test.before.js';path=ROOT/'_BUILD_SOURCE/test_fl.js'
s=before.read_bytes().decode('utf-8').replace('\r\n','\n')
s=s.replace('impact299.visual===2&&impact299.generic===0&&impact299.hit===1','impact299.visual===0&&impact299.generic===0&&impact299.hit===1')
s=s.replace('Volley impact keeps both authored explosion layers with one warhead report and no duplicate generic explosion sounds','Volley impact uses one bounded authored reel with one warhead report and no stacked generic explosions')
# Generic volley coverage belongs to an armed stage, not stage-1 jets' dedicated guns.
a=s.index('// ===== 213a.')
z=s.index('// ===== 213b.',a)
fixture=s[a:z].replace('run.stage=1; curStage=STAGES[0];','run.stage=4; curStage=STAGES[3];').replace('beginStage(1); setState(GS.PLAY);','beginStage(4); setState(GS.PLAY);')
s=s[:a]+fixture+s[z:]
old="ok(/-4\\.0\\*dt,4\\.0\\*dt/.test(_cb) && /-0\\.85\\*dt,0\\.85\\*dt/.test(_cb),\n     'THE EYE LASERS TRACK - they slew onto the player through the charge and keep a slow slew while burning');"
new="ok(/furnaceHeadCombat/.test(_cb) && /cycle<lock/.test(_fn287('furnaceHeadCombat')),\n     'Furnace head delegates to a charge that stops aiming before its warning completes');"
assert old in s
s=s.replace(old,new)
anchor="console.log('\\n============================================');"
assert s.count(anchor)==1
s=s.replace(anchor,(HERE/'tests.js').read_text(encoding='utf-8')+'\n'+anchor)
expected=s.replace('\n','\r\n').encode('utf-8')
if path.read_bytes() not in [before.read_bytes(),expected] and hashlib.sha256(path.read_bytes()).hexdigest()!='4b5d032efb16b846d49f17b3ed8a4fb8126c5d0566b9b916640c3d736a1f7089':raise ValueError('Subsequent suite edits present.')
path.write_bytes(expected);print('Installed nine meaningful section-300 checks; CRLF preserved.')
