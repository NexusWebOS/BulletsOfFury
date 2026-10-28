from pathlib import Path
import shutil,re
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/chronos_modular_1023';D=R/'assets/game/shared/combat/chronos_modular_1023';D.mkdir(parents=True,exist_ok=True);B=W/'before';B.mkdir(exist_ok=True)
for p in(W/'shipping').glob('*.webp'):shutil.copy2(p,D/p.name)
for source,target in [('chronos.js','chronos_modular_1023.js'),('chronos_art.js','chronos_modular_art_1023.js')]:shutil.copy2(W/source,R/'assets'/target)
paths=['assets/game.js','assets/feedback_1002.js','assets/feedback_claude_1003.js','assets/cinematic_director_0930.js','assets/cinematic_ending_1020.js','assets/cinema_story_1021.js','assets/build_integration_1003.js','assets/hammer_finale_1017.js','assets/smooth_motion_1009.js','assets/hammer_tactical_1023.js','assets/playthrough_1011.js','index.html']
for rel in paths:
 p=R/rel;dst=B/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copy2(p,dst)
 raw=p.read_bytes();s=raw.decode('utf-8')
 if rel!='index.html':
  s=s.replace("'CHROME HAMMER ARCHMAGE'","'CHRONOS'").replace("'CHROME HAMMER'","'CHRONOS'").replace("'CRONOS'","'CHRONOS'").replace('I am Cronos.','I am Chronos.').replace('Cronos is down.','Chronos is down.')
  if rel=='assets/cinematic_director_0930.js':s=s.replace("if(p==='cronos')", "if(p==='cronos'||p==='chronos')").replace("line('cronos',", "line('chronos',")
  if rel=='assets/cinematic_director_0930.js':s=s.replace("if(s.live&&b.who==='CHRONOS')fit(","if(s.live&&s.id==='cronos'&&b.who==='CHRONOS')fit(")
  if rel=='assets/playthrough_1011.js':s=s.replace('if(PT11.radio){PT11.radio.t+=dt;',"if(PT11.radio&&!BOFCinematicDirector.live){PT11.radio.t+=dt;").replace("if(q&&run.stage===5&&state===GS.PLAY)dlgBox(","if(q&&run.stage===5&&state===GS.PLAY&&!BOFCinematicDirector.live)dlgBox(")
  if rel=='assets/game.js'and'if(b._ch23Round&&'not in s:s=s.replace("    if(b._archBlaster){", "    if(b._ch23Round&&typeof ch23BulletDraw==='function'&&ch23BulletDraw(b))continue;\n    if(b._archBlaster){")
 else:
  tag='<script src="assets/chronos_modular_art_1023.js?v=chronos-modular-1023-1"></script>\n<script src="assets/chronos_modular_1023.js?v=chronos-modular-1023-1"></script>\n'
  if'assets/chronos_modular_1023.js'not in s:s=s.replace('</body>',tag+'</body>')
  for name in [Path(n).name for n in paths if n.endswith('.js')]:s=re.sub(re.escape('assets/'+name)+r'\?v=[^"\s]+','assets/'+name+'?v=chronos-modular-1023-1',s)
 p.write_bytes(s.encode('utf-8'))
# Keep the prior builder's runtime source in agreement with the visible rename.
p=R/'_ART_SOURCES/hammer_tactical_1023/tactical.js';s=p.read_text();p.write_text(s.replace("who:'CHROME HAMMER'","who:'CHRONOS'"))
print('Installed Chronos modular chaingun, native projectile route and visible name corrections.')
