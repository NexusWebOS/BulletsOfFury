from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,shutil,hashlib
W=Path(__file__).parent;O=W.parents[1]/'outputs/cannon-cover';R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');m=json.loads((O/'manifest.json').read_text());c=json.loads((O/'capture.json').read_text())
assert not c['errors'] and all(q['pass']for q in c['checks']);assert all(q['no_fan_visible'] and q['filled_pixels']==q['opening_pixels'] for q in m['firing_coverage'])
runtime=(R/'assets/thunderhead_reactor_1105.js').read_bytes();assert runtime==(W/'candidate/thunderhead_reactor_1105.js').read_bytes();D=O/'assets/game/shared/combat/cannon_cover_1110';D.mkdir(parents=True,exist_ok=True)
assert runtime.decode().replace('assets/game/shared/combat/cannon_cover_1110/','assets/game/shared/combat/cannon_chambers_1110/')==(W/'candidate/before.js').read_text(),'Unexpected runtime logic change'
for p in(W/'candidate/frames').glob('*.png'):
 live=R/'assets/game/shared/combat/cannon_cover_1110'/p.name;assert live.read_bytes()==p.read_bytes();shutil.copy2(live,D/p.name)
shutil.copy2(R/'assets/thunderhead_reactor_1105.js',O/'assets/thunderhead_reactor_1105.js')
v={'opaque_opening_poses':len(m['firing_coverage']),'pixels_per_opening':3715,'native_errors':c['errors'],'native_checks':c['checks'],'code_scope':'four texture paths only; normalized source is identical to the pre-edit owner','source_sha256':hashlib.sha256(runtime).hexdigest(),'syntax':'assets/game.js and assets/thunderhead_reactor_1105.js passed node --check','suite':'Not repeated for this baked-art/four-path change. Existing project baseline reports missing difficultyHealthBaseline15.'};(O/'verification.json').write_text(json.dumps(v,indent=2))
(O/'README.md').write_text('Thunderhead cannon-opening coverage\n\nBoth oval openings remain covered by opaque authored energy from the first discharge frame through the final recovery frame. The normal fan faces return after the native beam object expires. Native cancellation restores the faces immediately. The hit variant flashes the energy as well as the cannon housing.\n\nInstalled: assets/game/shared/combat/cannon_cover_1110/*.png and four matching texture paths in assets/thunderhead_reactor_1105.js.\n\n28 frames, 24 fps, 256x832 fixed cell, pivot [128,146], outlet [128,239.28]. Startup 0-5, loop 6-21, recovery 22-27. Original generated wind master retained in _ART_SOURCES/stage67_flow_1110. Editable sources in editable/.\n\nNative Chromium capture: attack-and-return.gif and opening-closeup.gif. No page or console errors. Full suite not repeated; known unrelated baseline is documented in verification.json.\n',encoding='utf-8')
with ZipFile(O.parent/'cannon-cover.zip','w',ZIP_DEFLATED)as z:
 for p in O.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(O.parent))
print(json.dumps({'native_checks':len(c['checks']),'opaque_poses':len(m['firing_coverage']),'errors':len(c['errors'])}))
