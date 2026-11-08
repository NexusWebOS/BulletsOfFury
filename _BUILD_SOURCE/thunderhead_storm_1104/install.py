from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
shutil.copy2(W/'thunderhead_storm_1104.js',R/'assets/thunderhead_storm_1104.js')
p=R/'assets/furious_encounters_1102.js';s=p.read_bytes().decode()
s=s.replace("if(!b.dead&&q.core.flash<=0){ctx.save();ctx.globalCompositeOperation='lighter';", "if(!b.dead&&q.core.flash<=0&&q.model!=='thunder'){ctx.save();ctx.globalCompositeOperation='lighter';")
s=s.replace("q.phase==='attack'&&q.attack==='gates'?4:0", "q.phase==='attack'&&['gates','storm-tornado'].includes(q.attack)?4:0")
p.write_bytes(s.encode())
p=R/'index.html';s=p.read_bytes().decode();tag='<script src="assets/thunderhead_storm_art_1104.js?v=weather-reactor-1"></script>\r\n<script src="assets/thunderhead_storm_1104.js?v=weather-reactor-1"></script>\r\n'
if 'assets/thunderhead_storm_1104.js'not in s:s=s.replace('</body>',tag+'</body>')
p.write_bytes(s.encode())
out=R/'_BUILD_SOURCE/thunderhead_storm_1104';out.mkdir(exist_ok=True)
shutil.copy2(W/'build_storm.py',out/'build_storm.py')
shutil.copytree(W/'authored',out/'authored',dirs_exist_ok=True)
shutil.copytree(W/'sources',out/'sources',dirs_exist_ok=True)
print('Installed Thunderhead storm module, art, fixed-size Aseprite sources and source receipts.')
