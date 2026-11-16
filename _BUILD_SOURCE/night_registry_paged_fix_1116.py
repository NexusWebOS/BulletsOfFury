from pathlib import Path
p=Path(__file__).with_name('night_registry_bounds_1116.py')
s=p.read_text(encoding='utf8')
old="rects:Array.from({length:count},(_,i)=>({i,...path(a.key),rect:[i%cols*W,Math.floor(i/cols)*H,W,H]}))"
new="rects:Array.from({length:count},(_,i)=>{const page=Array.isArray(a.pages)?a.pages.find(p=>typeof p.key==='string'&&Number.isFinite(p.start)&&Number.isFinite(p.frames)&&i>=p.start&&i<p.start+p.frames):null;const j=page?i-page.start:i;return {i,...path(page?page.key:a.key),rect:[j%cols*W,Math.floor(j/cols)*H,W,H]};})"
if old in s:s=s.replace(old,new)
elif new not in s:raise RuntimeError('Audit parser changed; inspect before editing')
p.write_text(s,encoding='utf8',newline='\n')
