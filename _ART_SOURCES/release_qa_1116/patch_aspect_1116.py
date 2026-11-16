from pathlib import Path
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');f=R/'index.html';s=f.read_text(encoding='utf8');(R/'_ART_SOURCES/release_qa_1116/index.aspect-before.html').write_bytes(f.read_bytes())
a="      if(scr0){scr0.style.width=vw+'px';scr0.style.height=vh+'px';}"
b="""      // Wide authored menus/comics keep their real backing-store aspect.
      // Filling a tall browser independently in X/Y squeezed every icon and face.
      if(scr0){var ratio0=scr0.width/Math.max(1,scr0.height),w0=Math.min(vw,vh*ratio0),h0=w0/ratio0;
        scr0.style.width=Math.max(1,Math.floor(w0))+'px';scr0.style.height=Math.max(1,Math.floor(h0))+'px';}
""".rstrip()
assert a in s;s=s.replace(a,b,1);f.write_text(s,encoding='utf8',newline='\n');print('Aspect-fit authored wide surfaces; combat canvas and HUD owner unchanged.')
