from pathlib import Path
R=Path(__file__).resolve().parents[1]
for src,dst,old,new in [
 ('probe_dracodia_possession_1030.py','night_possession_1116.py',"'_shots/dracodia_possession_1030/probe'","'_shots/cinema_overnight_1116/possession'"),
 ('probe_dracodia_return_boundaries_1030.py','night_return_boundaries_1116.py',"R/'_shots/dracodia_return_1030'","R/'_shots/cinema_overnight_1116/return-boundaries'"),
 ('probe_dracodia_download_reveal_1025.py','night_rebirth_1116.py',"'_shots/dracodia_palette_1026/probe'","'_shots/cinema_overnight_1116/rebirth'")]:
 s=(R/'_BUILD_SOURCE'/src).read_text(encoding='utf8').replace(old,new)
 # Current native checkpoints only; no public score writes from developer fixtures.
 s=s.replace("p=boot(","p=boot(",1)
 anchor="initial=p.evaluate("
 if anchor in s:s=s.replace(anchor,"p.evaluate('()=>{BOFOnline.submitScore=()=>{}}');"+anchor,1)
 (R/'_BUILD_SOURCE'/dst).write_text(s,encoding='utf8',newline='\n')
print('Prepared isolated current-owner probes')
