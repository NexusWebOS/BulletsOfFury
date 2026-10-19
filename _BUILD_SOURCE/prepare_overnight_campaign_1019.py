"""Reuse the existing native campaign runner with an additional attack observer."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'_shots/overnight_combat_1019/campaign';D.mkdir(exist_ok=True)
s=(R/'_shots/playtest_full_1018/run.py').read_text(encoding='utf-8')
s=s.replace('ROOT=Path(__file__).resolve().parents[2]','ROOT=Path(__file__).resolve().parents[3]')
s=s.replace("OUT/'pilot.js'","ROOT/'_shots/playtest_full_1018/pilot.js'")
s=s.replace("case['startingGear']=","p.add_script_tag(path=str(ROOT/'_BUILD_SOURCE/overnight_observer_1019.js'));case['startingGear']=")
s=s.replace("case['final']=p.evaluate","case['attackAudit']=p.evaluate('ov19Summary()');case['final']=p.evaluate")
s=s.replace('len(case["captures"])<22','len(case["captures"])<12')
(D/'run.py').write_text(s,encoding='utf-8')
print('Native runner and attack observer ready.')
