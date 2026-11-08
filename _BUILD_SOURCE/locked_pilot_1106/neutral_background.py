from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');p=R/'assets/game.js';raw=p.read_bytes();backup=W/'before/game-before-neutral.js';backup.write_bytes(raw);s=raw.decode('utf8')
old="ctx.fillStyle=PILOT_SOLID_PALETTES_1106[p.key];ctx.fillRect(0,0,v.w,v.h);"
new="ctx.fillStyle=p.key==='cole'&&isPilotLocked(p)&&typeof lp116Background==='function'?lp116Background():PILOT_SOLID_PALETTES_1106[p.key];ctx.fillRect(0,0,v.w,v.h);"
assert old in s;s=s.replace(old,new,1)
old="function psPanelBox(x,y,w,h,tint,glow){\n  ctx.save();\n  ctx.fillStyle='rgba(8,11,18,0.78)'; ctx.fillRect(x,y,w,h);\n  ctx.strokeStyle=glow?tint:'rgba(120,140,170,0.45)'; ctx.lineWidth=glow?2:1;\n  if(glow){ ctx.shadowColor=tint; ctx.shadowBlur=10; }"
new="function psPanelBox(x,y,w,h,tint,glow){\n  const lockedScreen=typeof lp116LockedScreen==='function'&&lp116LockedScreen();\n  ctx.save();\n  ctx.fillStyle=lockedScreen?lp116Panel():'rgba(8,11,18,0.78)'; ctx.fillRect(x,y,w,h);\n  ctx.strokeStyle=lockedScreen?'#b8b8b8':glow?tint:'rgba(120,140,170,0.45)'; ctx.lineWidth=glow?2:1;\n  if(glow&&!lockedScreen){ ctx.shadowColor=tint; ctx.shadowBlur=10; }"
assert old in s;s=s.replace(old,new,1)
s=s.replace("ctx.fillStyle=rgba(hx(P.tint),0.85); ctx.fillText('\\u25C0'","ctx.fillStyle=rgba(hx(locked?'#b8b8b8':P.tint),0.85); ctx.fillText('\\u25C0'",1)
p.write_bytes(s.encode('utf8'));shutil.copy2(W/'locked_pilot_1106.js',R/'assets/locked_pilot_1106.js');print('NEUTRAL LOCKED BACKDROP')
