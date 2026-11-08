from pathlib import Path
import subprocess,sys
V=Path(r'C:/Users/Mike/Documents/New project/BOF-Furious-Boss-Videos-1104');p=V/'prepare.py';s=p.read_text()
if 'thunderhead-storm-native-final-1104'not in s:
 s=s.replace("(W/'posters').mkdir(exist_ok=True)","storm=R/'_shots/boss_comparison_1102/thunderhead-storm-native-final-1104/batch.json'\nif storm.exists():batch['jobs'].update(json.loads(storm.read_text()).get('jobs',{}))\n(W/'posters').mkdir(exist_ok=True)")
 s=s.replace('Four guns and two pressure chambers protect the hurricane reactor.','A1015 charging storm core launches cyclones, twin tornadoes, targeted thunderstrikes and a giant lightning storm. Moving clouds and rain darken the city; break all six modules to expose the core.')
 s=s.replace("'eye':'Hurricane reactor'", "'eye':'Hurricane reactor','storm-cyclone':'Core cyclone salvo','storm-tornado':'Twin tornadoes','storm-thunder':'Targeted thunderstorm','storm-tempest':'Giant core lightning storm'")
 s=s.replace("nativeFps=round(job['nativeFps'],1),peakDb=job['peakDb']", "nativeFps=round(job['nativeFps'],1),width=960 if job.get('view')=='playfield'else1280,height=1024 if job.get('view')=='playfield'else800,peakDb=job['peakDb']")
 s=s.replace("else1280", "else 1280").replace("else800", "else 800")
 s=s.replace("localRevision='prebuilt-shadow-mask-1104-2'", "localRevision='thunderhead-storm-reactor-1104'")
 s=s.replace('First 27 seconds hold fire. No enemy HP/phase/timer writes after spawn. Stage6 films were recaptured after the performance correction; Sumpjaw retains its unchanged Stage7 film.','Thunderhead uses45seconds player hold-fire, direct high-quality native-canvas H264 capture and the new authored storm reactor. Razorwake and Sumpjaw retain their prior verified movies and27seconds player hold-fire. Native allies continue acting. No enemy HP/phase/timer writes after spawn.')
 s=s.replace('The first 27 seconds demonstrate attacks before firing.','Thunderhead demonstrates attacks for45seconds before the pilot fires; the other films use27seconds. Native allies remain active. Thunderhead uses the native game canvas, including its boss health bar; cabinet side panels are outside this recording.')
 s=s.replace('Performance correction: Razorwake 26.7 to 57.7 FPS; Thunderhead 48.0 to 57.2 FPS. These are newly recorded full fights in the same high-quality mode. Sumpjaw retains its unchanged 54.7 FPS film.','Razorwake retains its57.7FPS performance-corrected film, and Sumpjaw its54.7FPS film. Thunderhead has a fresh storm-reactor recording; its actual engine FPS is shown above. The uncaptured high-quality storm profile measured59.9FPS through all four attacks.')
 s=s.replace('A1015','A 1015').replace('for45seconds','for 45 seconds').replace('use27seconds','use 27 seconds').replace('its57.7FPS','its 57.7 FPS').replace('its54.7FPS','its 54.7 FPS').replace('measured59.9FPS','measured 59.9 FPS')
 p.write_text(s)
subprocess.run([sys.executable,str(p)],check=True)
