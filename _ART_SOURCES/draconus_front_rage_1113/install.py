from pathlib import Path
import json,hashlib,shutil,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/boss_restore_1112.js','assets/boss_restore_art_1112.js','assets/boss_ship_forms_1111.js','assets/draconus_modular_1111.js','assets/overhead_slam_art_1111.js','assets/chronos_rageform_1026.js','assets/chronos_kamehameha_1026.js','assets/chronos_energy_audio_1026.js'];before={p:sha(R/p)for p in protected}
p=R/'assets/rage_palm_1110.js';old=p.read_bytes();original=b"if(b._r30.v18.donorAge>52){Q.rf1110=null;Q.action=null;Q.cool=.8;}";fixed=b"if(b._r30.v18.donorAge>52&&R.cycle>=3){Q.rf1110=null;Q.action=null;Q.cool=.8;}"
if original in old:
 assert old.count(original)==1;(W/'rage_palm_1110.before.js').write_bytes(old);new=old.replace(original,fixed);assert p.read_bytes()==old;p.write_bytes(new)
else:assert fixed in old
subprocess.run(['node','--check',str(p)],check=True);subprocess.run(['node','--check',str(W/'draconus_front_rage_1113.js')],check=True);shutil.copy2(W/'draconus_front_rage_1113.js',R/'assets/draconus_front_rage_1113.js')
p=R/'index.html';old=p.read_bytes();s=old.decode('utf-8');nl='\r\n'if'\r\n'in s else'\n'
if 'assets/draconus_front_rage_1113.js'not in s:
 (W/'index.before.html').write_bytes(old);new=s.replace('</body>','<script src="assets/draconus_front_rage_1113.js?v=1"></script>'+nl+'</body>');assert new!=s and p.read_bytes()==old;p.write_bytes(new.encode('utf-8'))
assert all(sha(R/p)==h for p,h in before.items())
(W/'installation.json').write_text(json.dumps(dict(protected=before,runtime=sha(R/'assets/draconus_front_rage_1113.js'),rageOwner=sha(R/'assets/rage_palm_1110.js'),rageChange='Only the Draconus rage-book exit now requires3 completed cycles; native HP, entry clock and attacks are unchanged.'),indent=2))
print('Installed frontal Draconus strike selection and native rage commitment/full-book recovery.')
