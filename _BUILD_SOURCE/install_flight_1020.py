from pathlib import Path
from PIL import Image
import urllib.request
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/boss_redesign_1020';p=S/'corner-warning-sheet.png'
if not p.exists():p.write_bytes(urllib.request.urlopen('https://api.pixellab.ai/mcp/pixel-tools/8eed4c09-d9a5-4cc3-b0c9-0479dbb40877/assets/south/full.png',timeout=90).read())
Image.open(p).crop((0,0,64,64)).save(S/'corner-warning.png')
p=R/'index.html';s=p.read_text(encoding='utf-8');marker='<script src="assets/combat_audio_1015.js';assert marker in s
if 'assets/phoenix_swoon_1020.js' not in s:s=s.replace(marker,'<script src="assets/phoenix_swoon_art_1020.js?v=whole-wings-1020"></script>\n<script src="assets/boss_shared_1020.js?v=bosses-1020"></script>\n<script src="assets/phoenix_swoon_1020.js?v=whole-wings-1020"></script>\n<script src="assets/helicopter_assault_1020.js?v=routes-1020"></script>\n'+marker,1)
p.write_text(s,encoding='utf-8',newline='\n');print('Whole-module flight encounters registered')
