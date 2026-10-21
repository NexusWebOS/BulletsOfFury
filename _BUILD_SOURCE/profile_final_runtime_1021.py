from pathlib import Path
import json,sys
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'))
source=(R/'_BUILD_SOURCE/probe_edge_live_1012.py').read_text(encoding='utf-8')
for name,launch in [('Edge',"pw.chromium.launch(channel='msedge',args=['--mute-audio'])"),('Chrome',"pw.chromium.launch(channel='chrome',args=['--mute-audio'])"),('Firefox','pw.firefox.launch()')]:
 print('BEGIN '+name,flush=True)
 adapted=source.replace("pw.chromium.launch(channel='msedge',args=['--mute-audio'])",launch).replace("R=Path(__file__).resolve().parents[1]",'R=Path('+repr(str(R))+')').replace("O=R/'_shots/performance_1012/live'","O=R/'_shots/final_version_1021/performance/"+name+"'")
 # The native map is closure-owned: clear it in place instead of replacing the
 # exposed property and inadvertently simulating no movement/fire at all.
 exec(compile(adapted,name,'exec'),{'__file__':str(R/'_BUILD_SOURCE/probe_edge_live_1012.py')})
