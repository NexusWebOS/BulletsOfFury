from pathlib import Path
import json,shutil,re
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';D=R/'assets/game/shared/combat/hammer_tactical_1023';D.mkdir(parents=True,exist_ok=True)
B=W/'before';B.mkdir(exist_ok=True)
for rel in ['assets/game.js','assets/combat_pressure_1012.js','index.html','AGENTS.md','CLAUDE.md']:
 p=R/rel;dst=B/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copy2(p,dst)
for folder in ['shipping','armor']:
 for p in (W/folder).glob('*.webp'):shutil.copy2(p,D/p.name)
shutil.copy2(W/'shoot_fixed.png',R/'assets/game/shared/ui/shoot_prompt_1023.png')
art=(W/'tactical_art.js').read_text();armor=json.loads((W/'armor/manifest.json').read_text());art+='\nconst HT23_ARMOR='+json.dumps(armor,separators=(',',':'))+';\n'
(R/'assets/hammer_tactical_art_1023.js').write_text(art,encoding='utf-8',newline='\n');shutil.copy2(W/'tactical.js',R/'assets/hammer_tactical_1023.js')
p=R/'assets/game.js';s=p.read_text(encoding='utf-8')
if 'function bossShootGraphic('not in s:
 s=s.replace('let hudCallout=null;',"""/* ENGINE HEADER RULE: every boss SHOOT! objective uses Stage6's authored
   nwarn_shoot sign through bossShootGraphic. No substitute text/reticle boxes. */
function bossShootGraphic(x,y){
 const key='boss_shoot_prompt';if(!XART.rdy(key))return false;
 ctx.drawImage(XART.get(key),Math.round(x-40),Math.round(y-70));return true;
}
let hudCallout=null;""")
 marker="  X._src['pause_button_0915']="
 assert marker in s;s=s.replace(marker,"  X._src['boss_shoot_prompt']='assets/game/shared/ui/shoot_prompt_1023.png';\n"+marker)
 s=s.replace('const VW = 480, VH = 512;',"/* Boss SHOOT! headers: use bossShootGraphic / the authored Stage6 sign. */\nconst VW = 480, VH = 512;")
 s=s.replace('   single self-contained file Â· ColeForge Studios','   single self-contained file Â· ColeForge Studios\n   ENGINE ART RULE â€” every boss SHOOT! header uses Stage6\'s authored SHOOT graphic\n   through bossShootGraphic, never a substitute bitmap-text/reticle combination.')
 p.write_text(s,encoding='utf-8',newline='\n')
p=R/'assets/combat_pressure_1012.js';s=p.read_text(encoding='utf-8');old="ctx.save();ctx.globalAlpha=.55+.45*Math.sin((h.chromiumT||0)*12)**2;\n  ph8Icon(ctx,'retm_0',x,y,36);bmfDrawOn(ctx,window.BOF_UI_FACE||'game','SHOOT!',x,y-25,14,'center');ctx.restore();"
assert old in s or 'bossShootGraphic(x,y+14)'in s
s=s.replace(old,"bossShootGraphic(x,y+14);")
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'index.html';s=p.read_text(encoding='utf-8');tag='<script src="assets/hammer_tactical_art_1023.js?v=tactical-1023-1"></script>\n<script src="assets/hammer_tactical_1023.js?v=tactical-1023-1"></script>\n'
if 'assets/hammer_tactical_1023.js'not in s:s=s.replace('</body>',tag+'</body>')
s=s.replace('hammer_tactical_art_1023.js?v=tactical-1023-1','hammer_tactical_art_1023.js?v=tactical-1023-2').replace('hammer_tactical_1023.js?v=tactical-1023-1','hammer_tactical_1023.js?v=tactical-1023-2')
s=s.replace('assets/game.js?v=hq-forge-1023-1','assets/game.js?v=tactical-1023-1');s=re.sub(r'assets/combat_pressure_1012.js\?v=[^"\s]+','assets/combat_pressure_1012.js?v=tactical-1023-1',s)
s=s.replace('hammer_tactical_art_1023.js?v=tactical-1023-2','hammer_tactical_art_1023.js?v=tactical-correction-1023-3').replace('hammer_tactical_1023.js?v=tactical-1023-2','hammer_tactical_1023.js?v=tactical-correction-1023-3')
p.write_text(s,encoding='utf-8',newline='\n');print('Installed tactical actor, armor cleanup and shared Stage6 SHOOT graphic.')
