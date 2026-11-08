from pathlib import Path
import json,subprocess,sys
W=Path(__file__).resolve().parent;V=W.parent/'BOF-Furious-Boss-Videos-1104';p=V/'prepare.py';s=p.read_text()
s=s.replace('sumpjaw-serpents-mp4-1104/batch.json','sumpjaw-serpents-final-1104/batch.json')
if "sumpjaw-serpents-final-1104/batch.json"not in s:s=s.replace("(W/'posters').mkdir(exist_ok=True)","sump=R/'_shots/boss_comparison_1102/sumpjaw-serpents-final-1104/batch.json'\nif sump.exists():batch['jobs'].update(json.loads(sump.read_text()).get('jobs',{}))\n(W/'posters').mkdir(exist_ok=True)")
s=s.replace('Two creatures with individual health bars. Break both gills to expose each intake heart.','Two articulated toxic serpents with32-heading head turns, trailing armor bodies and airborne pounces over the player. Faster six-burst acid volleys, giant toxic orbs and circling attacks. Each keeps its own health bar; break both gills to expose its intake heart.')
s=s.replace("'bite':'Bite lunge'","'bite':'Bite lunge','leap':'Airborne pounce over the pilot','orb':'Giant toxic orb volley','acid':'Rapid acid spit volley','coil':'Coiling serpent attack'")
s=s.replace('Razorwake and Sumpjaw retain their prior verified movies and27seconds player hold-fire.','Sumpjaw has a fresh articulated-serpent recording with45seconds player hold-fire. Razorwake retains its prior verified movie and27seconds player hold-fire.')
s=s.replace('Thunderhead demonstrates attacks for 55 seconds before the pilot fires; the other films use 27 seconds.','Thunderhead demonstrates attacks for 55 seconds, Sumpjaw for45seconds and Razorwake for27seconds before the pilot fires.')
s=s.replace('Razorwake retains its 57.7 FPS performance-corrected film, and Sumpjaw its 54.7 FPS film. Thunderhead has a fresh storm-reactor recording; its actual engine FPS is shown above.','Razorwake retains its 57.7 FPS performance-corrected film. Thunderhead and Sumpjaw have fresh complete recordings; actual engine FPS is shown above.')
s=s.replace("localRevision='thunderhead-regenerated-modular-1104'","localRevision='sumpjaw-articulated-serpents-1104'")
p.write_text(s);subprocess.run([sys.executable,str(p)],check=True)
print('Prepared new Sumpjaw film with real attack chapters; prior films preserved.')
