from pathlib import Path
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
(W/'whole_hammer_1110.js').write_bytes((R/'assets/whole_hammer_1110.js').read_bytes()+(W/'runtime-addon.js').read_bytes())
p=W/'verify_three_way.py';s=p.read_text()
for prefix in ['blue-overhead','ba119_corrupt-overhead']:
 s=s.replace("startsWith('"+prefix+"'))seen", "startsWith('"+prefix+"')&&q.a.frame>=16)seen")
p.write_text(s)
print('Prepared live source plus scoped direction routing and grip-preserving lift.')
