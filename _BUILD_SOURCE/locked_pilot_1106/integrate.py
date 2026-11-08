from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');D=R/'assets/game/shared/ui/locked_pilot_1106';D.mkdir(parents=True,exist_ok=True)
for p in (W/'exports').glob('*.png'):shutil.copy2(p,D/p.name)
shutil.copy2(W/'manifest.json',D/'manifest.json')
m=json.loads((W/'manifest.json').read_text());(R/'assets/locked_pilot_art_1106.js').write_text('"use strict";\nconst LOCKED_PILOT_ART_1106='+json.dumps(m,separators=(',',':'))+';\n',encoding='utf8');shutil.copy2(W/'locked_pilot_1106.js',R/'assets/locked_pilot_1106.js')
backup=W/'before';backup.mkdir(exist_ok=True)
def edit(name,fn):
 p=R/name;raw=p.read_bytes();b=backup/Path(name).name
 if not b.exists():b.write_bytes(raw)
 s=raw.decode('utf8');new=fn(s);assert new!=s,name;p.write_bytes(new.encode('utf8'))
old="if(locked){pcFontLeft('LOCKED',bx+8,by+bh*.42,16,'#dce2ea',1);pcFontLeft('PASSWORD REQUIRED',infoX,infoY+32,10,'#ffe98a',1);return;}"
new="if(locked){if(typeof lockedPilotCard116==='function'){lockedPilotCard116(P,PX,PY,PW,PH);return;}pcFontLeft('LOCKED',bx+8,by+bh*.42,16,'#dce2ea',1);pcFontLeft('PASSWORD REQUIRED',infoX,infoY+32,10,'#ffe98a',1);return;}"
for n in ['assets/pixelmap_ui_1027.js','assets/playthrough_ui_1011.js']:edit(n,lambda s:s.replace(old,new,1))
def core(s):
 start=s.index('      /* ⚠ THE LOCKED SLOT IS A');end=s.index('\n    } else {',start)
 s=s[:start]+"      if(typeof lockedPilotMini116==='function')lockedPilotMini116('pilot',x,y0,PS_CELL);"+s[end:]
 old="      ctx.save(); ctx.globalAlpha=0.30; psBlitFit(psShipKey(Q.key,null), x+PS_CELL/2, sy+PS_CELL/2, PS_CELL-8, PS_CELL-8, 0.3); ctx.restore();"
 assert old in s;s=s.replace(old,"      if(typeof lockedPilotMini116==='function')lockedPilotMini116('ship',x,sy,PS_CELL);",1)
 s=s.replace("if(locked && pilotFlash>0){","if(locked && pilotFlash>0 && typeof lockedPilotCard116!=='function'){",1)
 s=s.replace("/* the nine-across roster: a square face over its ship, the locked slot a '?'. Returns the hit","/* the nine-across roster: a square face over its ship, authored silhouettes for locked Cole. Returns the hit",1)
 return s
edit('assets/game.js',core)
def index(s):
 s=s.replace('assets/game.js?v=desktop-controls-1106b','assets/game.js?v=locked-cole-1106c')
 s=s.replace('assets/pixelmap_ui_1027.js?', 'assets/pixelmap_ui_1027.js?locked=1106c&')
 s=s.replace('assets/playthrough_ui_1011.js?', 'assets/playthrough_ui_1011.js?locked=1106c&')
 return s.replace('</body>','<script src="assets/locked_pilot_art_1106.js?v=gray-black-1"></script>\n<script src="assets/locked_pilot_1106.js?v=gray-black-1"></script>\n</body>')
edit('index.html',index)
def taxonomy(s):
 q={'role':'locked_cole_pilot_and_actual_jet_silhouettes_with_gray_black_padlock_states','owner':'_BUILD_SOURCE/locked_pilot_1106/build_locked.lua','manifest':'assets/game/shared/ui/locked_pilot_1106/manifest.json','note':'18 fixed even two-frame Aseprite banks. Actual cole_body_0922 and ship_cole_pv2 alpha; exact #606060/#000000 states held450ms, fixed blits only. Native Cole password/save/unlock gate retained.'}
 return s.replace('{','{\n  "lp116_": '+json.dumps(q,indent=2).replace('\n','\n  ')+',',1)
edit('assets/data/ART_TAXONOMY.json',taxonomy)
json.loads((R/'assets/data/ART_TAXONOMY.json').read_text(encoding='utf8'))
print('INTEGRATED',D)
