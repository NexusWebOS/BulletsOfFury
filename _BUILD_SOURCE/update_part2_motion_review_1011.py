"""Apply the motion review additions inside the existing owning page builder."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/'_BUILD_SOURCE/build_part2_review_1010.py'
s=f.read_text(encoding='utf-8')
if 'drawn_motion_1011' in s:
    print('Owning builder already contains the motion review');raise SystemExit(0)
s=s.replace('October 11 animation corrections','October 11 animation corrections').replace('revision=20261011','revision=20261011-motion')
s=s.replace('Authored effects · corrected crops and fixed anchors','Drawn rotations and complete effects')
s=s.replace('Atomic: 28 original poses plus 4 drawn in-betweens. Each bank uses one fixed preview scale that fits its entire union of visible pixels. Onion mode overlays the neighboring poses at the same physical anchor.',
 'Four fighter variants each have 16 rigid barrel-roll views and 16 somersault views. The cloud has 32 progressive drawings. Maverick shares Jace’s sphere motion in green and overdrive colors. Furnace shows the same complete beam as the game. Onion overlays neighboring poses at their physical anchor.')
s=s.replace('<option value="atom">Atomic cloud · 32 corrected poses</option>', '<option value="atom">Atomic cloud · 32 smooth stages</option>')
s=s.replace('<option value="jace">Jace molten helix · 32 poses</option>', '<option value="jace">Jace molten helix · 32 poses</option><option value="maverick">Maverick green helix · 32 poses</option><option value="maverick_full">Maverick overdrive helix · 32 poses</option>')
s=s.replace('<option value="fire">Furnace fire column · 32 poses</option>', '<option value="fire">Furnace complete fire beam · 32 poses</option><option value="fire_tip">Furnace flame crown · 16 poses</option>')
s=s.replace('<option value="stealth">Actual opening stealth fighter</option>', '<option value="stealth_roll">Stealth barrel roll · 16 views</option><option value="stealth_somer">Stealth somersault · 16 views</option><option value="stealth">Stealth fighter · idle</option>')
s=s.replace('<option value="blue">Original blue</option>', '<option value="blue">Blue</option><option value="orange">Orange heavy</option>')
s=s.replace("<script>\n'use strict';let data", "<script src=\"../../../assets/part2_fire_renderer_1011.js\"></script>\n<script>\n'use strict';let data")
s=s.replace("function artList(){return bank.value==='stealth'?data.banks.stealth.filter(a=>a.role===airRole.value):data.banks[bank.value];}",
 "function artList(){return bank.value.startsWith('stealth')?data.banks[bank.value].filter(a=>a.role===airRole.value&&(bank.value!=='stealth'||a.pose==='idle')):data.banks[bank.value];}")
s=s.replace('function fitBank(){const bounds=', "function fitBank(){if(bank.value==='fire')return {k:1,cx:216,cy:378};const bounds=")
s=s.replace("const paint=(q,alpha)=>{const im=loaded[q.key];if(im?.complete){g.globalAlpha=alpha;g.drawImage(im,cx-q.pivot[0]*k,cy-q.pivot[1]*k,q.w*k,q.h*k);g.globalAlpha=1;}};",
 "const paint=(q,alpha)=>{if(bank.value==='fire'){p2RenderFireColumn(g,data.banks,key=>loaded[key]?.complete?loaded[key]:null,cx,cy,-Math.PI/2,300,64,data.banks.fire.indexOf(q)/32,alpha,true);return;}const im=loaded[q.key];if(im?.complete){const p=(data.banks.atom.indexOf(q)+.5)/32;g.globalAlpha=alpha*(bank.value==='atom'&&p>.875?(1-p)/.125:1);g.drawImage(im,cx-q.pivot[0]*k,cy-q.pivot[1]*k,q.w*k,q.h*k);g.globalAlpha=1;}};")
s=s.replace("bank.value!=='stealth'", "!bank.value.startsWith('stealth')")
s=s.replace("(bank.value==='shield'?800:1000/24)", "(bank.value==='shield'?800:bank.value==='atom'&&index===31?700:1000/24)")
# New evidence is read only when it exists, keeping earlier reports independent.
s=s.replace("log=ROOT/'_shots/part2_motion_1011/full-tests.log'", "f=ROOT/'_shots/part2_motion_1011/report.json'\nif f.exists():reports['drawn_motion_1011']=json.loads(f.read_text())\nlog=ROOT/'_shots/part2_motion_1011/full-tests.log'")
f.write_text(s,encoding='utf-8',newline='\n')
print('Updated owning motion preview builder')
