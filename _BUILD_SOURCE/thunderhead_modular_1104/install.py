from pathlib import Path
import shutil,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_BUILD_SOURCE/thunderhead_modular_1104';S.mkdir(exist_ok=True)
subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','root='+str(W/'authored'),'--script',str(W/'authored/author.lua')],check=True)
shutil.copy2(W/'thunderhead_modular_1104.js',R/'assets/thunderhead_modular_1104.js')
for n in ['thunderhead-modular-generated.png','wind-beam-generated.png','build_modular.py']:
 shutil.copy2(W/n,S/n)
shutil.copytree(W/'authored',S/'authored',dirs_exist_ok=True)
p=R/'index.html';s=p.read_bytes().decode();tag='<script src="assets/thunderhead_modular_art_1104.js?v=reactor-beam-kit-1"></script>\r\n<script src="assets/thunderhead_modular_1104.js?v=reactor-beam-kit-1"></script>\r\n'
if 'assets/thunderhead_modular_1104.js'not in s:s=s.replace('</body>',tag+'</body>')
p.write_bytes(s.encode());print('Installed regenerated modular Thunderhead and authored giant wind beams.')
