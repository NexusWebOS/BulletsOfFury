from pathlib import Path
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');p=R/'index.html';s=p.read_text(encoding='utf8')
a="scr0.style.width=Math.max(1,Math.floor(w0))+'px';scr0.style.height=Math.max(1,Math.floor(h0))+'px';"
b="scr0.style.setProperty('width',Math.max(1,Math.floor(w0))+'px','important');scr0.style.setProperty('height',Math.max(1,Math.floor(h0))+'px','important');"
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s,encoding='utf8',newline='\n')
print('Native aspect fit now overrides legacy fullscreen stretch CSS.')
