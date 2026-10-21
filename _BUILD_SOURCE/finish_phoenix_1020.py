from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('dracodia_phoenix_art_1020.js?v=phoenix-1020','dracodia_phoenix_art_1020.js?v=phoenix-final-1020').replace('dracodia_phoenix_1020.js?v=phoenix-1020','dracodia_phoenix_1020.js?v=phoenix-final-1020')
# Revalidation of the registry brings the phoenix wireframe into existing builds.
import re
s=re.sub(r'(dracodia_download_art_1019\.js\?v=)[^"\s]+',r'\g<1>phoenix-wire-final-1020',s);p.write_text(s,encoding='utf-8',newline='\n')
p=R/'HANDOFF_CODEX.md';s=p.read_text(encoding='utf-8');header='''## 2026-10-20 Corrupted Fire Phoenix replaces Dracodia volcano copy

Mike rejected the angled robot and requested a forward-facing alien fire phoenix,
with PixelLab used for the form AND its attacks. New Pro master,17 lossless
320-square articulated components,10 independent HP owners within the original
budget. Nine coordinated wing/charge poses,16 phoenix muzzle blooms,16 clean
flowing laser frames, molten feather / feather-wall volleys, new48-pose phoenix
skull and matching16-frame hollow wireframe download. Wings tuck for roll/rotor;
every muzzle, warning, hit mask, flash and break follows actual anatomy.
Real ordinary fire caught/fixed a few cannon-lip pixels mistakenly assigned to
protected talons. Inner and outer feathers now share one wing owner, preventing
orphan wings when cannons break. Original Stage2 Furnace delegation retained.
164 PNGs/647,082bytes. Owner assets/dracodia_phoenix_1020.js, generated registry
dracodia_phoenix_art_1020.js; builder build_dracodia_phoenix_1020.py. New source
and shipping folders named dracodia_phoenix_1020 / corrupted_phoenix_1020.
Details docs/DRACODIA_PHOENIX_1020.md; native review
_shots/dracodia_phoenix_1020/review.html. Cache phoenix-final-1020.
Local only, no commit/push requested; unrelated dirty work retained.

'''
if not s.startswith('## 2026-10-20 Corrupted Fire Phoenix'):p.write_text(header+s,encoding='utf-8',newline='\n')
print('Phoenix cache versions and handoff updated')
