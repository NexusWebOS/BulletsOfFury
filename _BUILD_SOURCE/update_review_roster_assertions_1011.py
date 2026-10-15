"""Migrate only explicitly superseded roster/label checks, retaining CRLF."""
from pathlib import Path
p=Path(__file__).with_name('test_fl.js');b=p.read_bytes()
pairs=[
 ("+' + INCENDIARY SHOTGUN'","+' / INCENDIARY SHOTGUN'"),
 ("+' + CHARGE DASH'","+' / CHARGE DASH'"),
 ("['s7lamprey','s7barge','s7pipe','s7walker','s7sampler','s7serpent','s7mine','s7canister','s7tank','s7skimmer']","['s7lamprey','s7barge','s7pipe','s7sampler','s7serpent','s7mine','s7canister','s7tank','s7skimmer']"),
 ("ok(_sewSeen.length===10, 'all 10 supplied toxic-sewer unit types appeared in the run","ok(_sewSeen.length===9 && !_seen.s7walker, 'all nine retained toxic-sewer units appeared without the retired walker"),
 ("'s6buoy','s6dart','s6thunder','s6turbine','s6probe'","'s6dart','s6thunder','s6turbine','s6probe'"),
 ("ok(_fleet269.every(function(k){return _plan269.indexOf(k)>=0;}),","ok(_fleet269.every(function(k){return _plan269.indexOf(k)>=0;}) && !_plan269.includes('s6buoy'),"),
 ("Stage 6 schedules all twelve supplied Heavy Turbulence airframes","Stage 6 schedules the retained storm fleet without the retired yellow buoy"),
 ("ok(_fleet270.every(function(k){return _plan270.indexOf(k)>=0;}),'Stage 7 schedules all eleven supplied toxic-sewer field units');","ok(_fleet270.every(function(k){return _plan270.indexOf(k)>=0;}) && !_plan270.includes('s7walker'),'Stage 7 schedules the retained toxic roster without the retired humanoid');")]
for old,new in pairs:
 old=old.encode();new=new.encode()
 if old not in b and new in b:continue
 assert old in b,old;b=b.replace(old,new)
p.write_bytes(b)
print('Updated five obsolete assertions; preserved CRLF.')
