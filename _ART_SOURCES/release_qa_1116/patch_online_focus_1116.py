from pathlib import Path
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');f=R/'assets/online.js';s=f.read_text(encoding='utf8');(R/'_ART_SOURCES/release_qa_1116/online.js.focus-before').write_bytes(f.read_bytes())
s=s.replace('let captureAudio=null,started=false;','let captureAudio=null,started=false,inputFocused=true;')
s=s.replace("const pad=padInput(),m={type:'input'};for(const a of actions)m[a]=!!keys[a]||!!pad[a];", "const focused=inputFocused&&!document.hidden,pad=focused?padInput():{},m={type:'input'};for(const a of actions)m[a]=focused&&(!!keys[a]||!!pad[a]);")
s=s.replace("window.addEventListener('blur',()=>{keys={};lastSent='';sendInput();});", "window.addEventListener('blur',()=>{inputFocused=false;keys={};lastSent='';sendInput();});\n  window.addEventListener('focus',()=>{inputFocused=true;lastSent='';sendInput();});")
s=s.replace("document.addEventListener('visibilitychange',()=>{if(document.hidden){keys={};lastSent='';sendInput();}});", "document.addEventListener('visibilitychange',()=>{inputFocused=!document.hidden&&document.hasFocus();if(!inputFocused)keys={};lastSent='';sendInput();});")
assert 'const focused=inputFocused' in s
f.write_text(s,encoding='utf8',newline='\n')
index=R/'index.html';s=index.read_text(encoding='utf8').replace('assets/online.js?v=release-1116-2','assets/online.js?v=release-1116-3');index.write_text(s,encoding='utf8',newline='\n');print('Released keyboard and raw-pad inputs on guest focus loss.')
