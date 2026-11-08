from pathlib import Path
import subprocess,sys
V=Path(r'C:/Users/Mike/Documents/New project/BOF-Furious-Boss-Videos-1104');p=V/'prepare.py';s=p.read_text()
if 'thunderhead-modular-mp4-1104'not in s:
 s=s.replace("(W/'posters').mkdir(exist_ok=True)","modular=R/'_shots/boss_comparison_1102/thunderhead-modular-mp4-1104/batch.json'\nif modular.exists():batch['jobs'].update(json.loads(modular.read_text()).get('jobs',{}))\n(W/'posters').mkdir(exist_ok=True)")
 s=s.replace('A 1015 charging storm core launches cyclones, twin tornadoes, targeted thunderstrikes and a giant lightning storm. Moving clouds and rain darken the city; break all six modules to expose the core.','Regenerated hull, separate reactor, four modular turrets and two cyclone cannons. Giant wind beams fire while the reactor and whole-body1015 aura charge faster and faster. Break all six weapons to expose the core; the storm attack cycle remains active.')
 s=s.replace("'storm-tempest':'Giant core lightning storm'", "'storm-tempest':'Giant core lightning storm'")
 needle="   attack=storm.get('attack')"
 extra="""   if id=='thunderhead':
    for event in storm.get('events',[]):
     key=event.get('event')
     label={'modular-core-charge':'Reactor and full-body charge','modular-wind-beam':'Giant wind cannon beams'}.get(key)
     if label and key not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.5)});seen.add(key)
"""
 s=s.replace(needle,extra+needle)
 s=s.replace("localRevision='thunderhead-storm-reactor-1104'","localRevision='thunderhead-regenerated-modular-1104'")
 s=s.replace('Thunderhead uses45seconds','Thunderhead uses55seconds').replace('for 45 seconds','for 55 seconds')
 s=s.replace('new authored storm reactor.','regenerated modular storm reactor, accelerating whole-body charge and cannon-origin wind beams.')
 s=s.replace('The uncaptured high-quality storm profile measured 59.9 FPS through all four attacks.','The regenerated kit, actual hit pixels, cannon warning lanes, beam cancellation and native defeat have been checked in the game.')
 s=s.replace('whole-body1015','whole-body 1015')
 p.write_text(s)
subprocess.run([sys.executable,str(p)],check=True)
