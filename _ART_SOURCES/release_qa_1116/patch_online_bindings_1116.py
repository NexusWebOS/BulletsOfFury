from pathlib import Path
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');f=R/'assets/online.js';s=f.read_text(encoding='utf8');(R/'_ART_SOURCES/release_qa_1116/online.js.binding-before').write_bytes(f.read_bytes())
s=s.replace("    const a=keyAction[e.key];if(!a)return;e.preventDefault();e.stopImmediatePropagation();keys[a]=on;sendInput();", "    const native=typeof keybindFor==='function'?actions.find(a=>(keybindFor(1)[a]||[]).includes(String(e.key).toLowerCase())):null;\n    const a=native||keyAction[e.key];if(!a)return;e.preventDefault();e.stopImmediatePropagation();keys[a]=on;sendInput();")
s=s.replace("  function padInput(){\n    const gp=", """  function padInput(){
    // Guest pads use the same saved raw-button assignments as local gameplay.
    if(typeof Input!=='undefined'&&typeof keybindFor==='function'){
      Input.pollGamepad();const kb=keybindFor(1);
      return Object.fromEntries(actions.map(a=>[a,(kb[a]||[]).some(k=>k.startsWith('pad_')&&!!Input.keys[k])]));
    }
    const gp=""")
f.write_text(s,encoding='utf8',newline='\n')
index=R/'index.html';s=index.read_text(encoding='utf8').replace('assets/online.js?v=release-1116-1','assets/online.js?v=release-1116-2');index.write_text(s,encoding='utf8',newline='\r\n');print('Online guest now honors native saved bindings.')
