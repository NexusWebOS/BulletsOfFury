from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'_BUILD_SOURCE/night_warning_matrix_1116.py'
s=p.read_text(encoding='utf8').replace("/warning-matrix-current'","/warning-matrix-final'")
needle="    ident=f'{diff}-s{stage}-{role}';"
replacement="    if diff!='hard' or stage<4 or (stage==4 and role=='mini'):continue\n    p.goto('http://127.0.0.1:8765/index.html?night-matrix-isolated=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')\n    ident=f'{diff}-s{stage}-{role}';"
assert needle in s
s=s.replace(needle,replacement)
(R/'_BUILD_SOURCE/night_warning_matrix_final_1116.py').write_text(s,encoding='utf8',newline='\n')
