"""Named changes against the exact prior dirty build; preserve LF and reject later edits."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/encounter_cleanup_0914/game.before.js';path=ROOT/'assets/game.js'
s=before.read_bytes().decode('utf-8')
def replace(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:90])
 s=s.replace(a,b,1)
def fn(name,body):
 global s
 a=s.index('\nfunction '+name+'(');b=s.index('\n}',a)+2;s=s[:a]+'\n'+body+s[b:]
# New definitions are embedded at the old revision's top-level source insertion point.
replace('/* Mike\'s stage 1–5 encounter corrections, 0914. Authored plates, one simulation owner. */',
 (HERE/'engine.js').read_text(encoding='utf-8')+'\n/* Mike\'s stage 1–5 encounter corrections, 0914. Authored plates, one simulation owner. */')
# Remove duplicate old function definitions; the new implementation owns each of these.
for name in ['xenoRegentGridStart','xenoRegentGridTick','xenoRegentGridDraw','spaceImpact']:
 a=s.index('\nfunction '+name+'(');b=s.index('\n}',a)+2;s=s[:a]+s[b:]
replace('  if(!e || e.dead || !ENEMY_VOLLEY[e.type]) return;',
 '  if(!e || e.dead || !ENEMY_VOLLEY[e.type]) return;\n  if(run.stage===1&&e.pattern===\'s1jet\')return;')
replace('  if(!e || e.dead) return false;\n  const V = ENEMY_VOLLEY[e.type];',
 '  if(!e || e.dead) return false;\n  if(run.stage===1&&e.pattern===\'s1jet\')return false;\n  const V = ENEMY_VOLLEY[e.type];')
# Side cannons alone emit held lasers. The central aperture charges a distinct pulse.
a=s.index('\nfunction stage3WallLaserAttack(');b=s.index('\n}',a)+2;r=s[a:b]
r=r.replace("const slots=['L','C','R'],angles=[Math.PI/2,Math.PI/2,Math.PI/2];let arc=[0,0,0],width=42", "const slots=['L','R'],angles=[Math.PI/2,Math.PI/2];let arc=[0,0],width=30")
r=r.replace('angles[2]-=.72;arc=[.22,0,-.22]', 'angles[1]-=.72;arc=[.22,-.22]')
r=r.replace("slots.splice(step&1?2:0,1);angles.splice(step&1?2:0,1);arc=[0,0];width=46", "slots.splice(step&1?1:0,1);angles.splice(step&1?1:0,1);arc=[0];width=30")
r=r.replace('angles[2]-=.95;arc=[.42,0,-.42];width=48', 'angles[1]-=.95;arc=[.42,-.42];width=34')
r=r.replace("kind:'centerBeam'", "kind:'centerPulse',released:false")
s=s[:a]+r+s[b:]
replace('    const C=S.charge;C.t+=dt;', '    const C=S.charge;C.t+=dt;stage3CentralPulse(b,C);')
replace('function stage3BossDrawOver(b){', 'function stage3BossDrawOver(b){\n  stage3CoreWarningDraw(b);')
a=s.index('  /* The promoted Stage-3 fortress uses');b=s.index('  if(!XART.rdy(key))return false;',a)
s=s[:a]+s[b:]
replace('if(!XART.rdy(key))return false;const im=XART.get(key),len=Math.max(VW,VH)*1.25;',
 "if(!XART.rdy(key))return false;const wall=B.family==='rime'&&b._s3boss&&b._s3boss.role==='wall',im=wall?(xartPalette(key,'#143ca8')||XART.get(key)):XART.get(key),len=Math.max(VW,VH)*1.25;")
replace("    ctx.globalAlpha=_ghost; ctx.drawImage(im,-B.width/2,0,B.width,len);ctx.restore();", "    if(B.released){ctx.globalAlpha=1;if(wall){const rim=xartTint(key,'#071c51',1);if(rim)ctx.drawImage(rim,-B.width/2-2,0,B.width+4,len);}ctx.drawImage(im,-B.width/2,0,B.width,len);}ctx.restore();")
# Quiet, non-overlapping native combat channels for the Regent escorts.
replace('!b._xenoGrid&&!m.tell){m.fire=', '!b._xenoGrid&&!xenoRigAnyTell(b)){m.fire=')
replace('!b._xenoGrid&&!h.tell){h.fire=', '!b._xenoGrid&&!xenoRigAnyTell(b)){h.fire=')
a=s.index("    if(b.kind==='spaceImpact'){\n      const p=");b=s.index("    if(b.kind==='mavlaser'){",a)
s=s[:a]+"    if(b.kind==='spaceImpact'){spaceImpactDraw(b);continue;}\n"+s[b:]
# Player flame draws and hits the same shorter, narrower, nozzle-anchored plume.
replace('return flameHalfW(lv,1) * (flameIsIce()?FLAME_ICE_W:1);', 'return flameHalfW(lv,1) * (flameIsIce()?FLAME_ICE_W:PLAYER_FLAME_SCALE);')
replace('return f.bot - reach*(flameIsIce()?FLAME_ICE_H:1);', 'return f.bot - reach*(flameIsIce()?FLAME_ICE_H:PLAYER_FLAME_SCALE);')
replace('const dh=reach*(_isIce?ICE_H:1), dw=flameHalfW(lv,1)*2*(_isIce?ICE_W:1);', 'const dh=reach*(_isIce?ICE_H:PLAYER_FLAME_SCALE), dw=flameHalfW(lv,1)*2*(_isIce?ICE_W:PLAYER_FLAME_SCALE);')
replace('  const src=XART.get(key);\n  const sw=src.naturalWidth, sh=src.naturalHeight;', "  const src=_isIce?XART.get(key):(xartPalette(key,'#ff6924')||XART.get(key));\n  const sw=src.naturalWidth||src.width, sh=src.naturalHeight||src.height;")
# Furnace head now locks during yellow and holds position and aim through red/release.
a=s.index("  } else if(F.phase==='head'){",s.index('\nfunction furnaceCombat('));b=s.index('\n  }\n}',a)
s=s[:a]+"  } else if(F.phase==='head'){furnaceHeadCombat(b,dt);"+s[b:]
replace('function fztTellDraw(q){', 'function fztTellDraw(q,owner){\n  if(q.kind!==\'ring\'&&owner){combatWarningDraw(owner,q);return;}')
replace('for(const q of F.tells) fztTellDraw(q);','for(const q of F.tells) fztTellDraw(q,b);')
replace("const w=q.width*2.8; ctx.drawImage(im,70,0,116,240,-w/2,-8*FZT_S,w,q.len+8*FZT_S);", "const w=q.width*2.8*1.25; ctx.drawImage(im,70,0,116,240,-w/2,-8*FZT_S,w,q.len+8*FZT_S);")
replace('for(const q of F.beams){\n      const dx=', "for(const q of F.beams){\n      const _width=q.kind==='flame'?q.width*1.25:q.width;\n      const dx=")
replace('if(d < q.width/2+6*FZT_S)', 'if(d < _width/2+6*FZT_S)')
# The complete pause menu is tracked separately; immediately remove the destructive shortcut.
fn('drawPaused',"function drawPaused(){\n  ctx.fillStyle='rgba(0,0,0,0.38)';ctx.fillRect(0,0,VW,VH);ctx.textAlign='center';\n  msgText('PAUSED',VW/2,VH/2-10,30,'#7ad63a',0,1,0.12);\n  Input.tap('backspace');if(pauseTapped())setState(GS.PLAY);\n}")
expected=s.encode('utf-8');out=ROOT/'_shots/encounter_cleanup_0914/game.expected.js' if '--dry-run' in sys.argv else path
if out==path and path.read_bytes() not in [before.read_bytes(),expected]:raise ValueError('Subsequent edits present; use --dry-run and inspect them.')
out.write_bytes(expected);print('Wrote',out,'SHA256',hashlib.sha256(expected).hexdigest())
