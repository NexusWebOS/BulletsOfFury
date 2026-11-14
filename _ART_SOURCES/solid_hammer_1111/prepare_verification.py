from pathlib import Path
W=Path(__file__).resolve().parent; ROOT=W.parents[1]; PRIOR=W.parent/'front_hammer_1111'
for stage in [5,8]:
 s=(W.parent/f'verify_front_stage{stage}.py').read_text()
 s=s.replace("O=W.parent/'outputs/Front-facing-hammer'", "O=Path(r'"+(ROOT/'outputs/Solid-metal-hammers').as_posix()+"')")
 (W/f'verify_stage{stage}.py').write_text(s)
s=(W.parent/'front_record_loaded.py').read_text()
s=s.replace("O=Path(__file__).resolve().parent.parent/'outputs/Front-facing-hammer'", "O=Path(r'"+(ROOT/'outputs/Solid-metal-hammers').as_posix()+"')")
s=s.replace("W=Path(__file__).resolve().parent.parent/'rage_palm_1110'", "W=Path(r'"+(W.parent/'rage_palm_1110').as_posix()+"')")
s=s.replace('front-facing hammer motion','solid metal hammer motion')
(W/'front_record_loaded.py').write_text(s)
s=(PRIOR/'verify_password.py').read_text()
s=s.replace('outputs/Front-facing-hammer','outputs/Solid-metal-hammers')
(W/'verify_password.py').write_text(s)
import subprocess,sys
subprocess.run([sys.executable,str(W/'fix_capture.py')],check=True)
print('Prepared existing native checks and recordings for the corrected art.')
