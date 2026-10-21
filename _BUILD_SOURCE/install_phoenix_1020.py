from pathlib import Path
import urllib.request
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_phoenix_1020'
for name,job,index in [('feather','ac817c6c-04a2-4b0d-9731-b259ed949e24',0),('plume','6b1ca499-cabc-492f-9ba3-006b3c6cc2d5',0)]:
 p=S/(name+'.png')
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={index}',timeout=90).read())
p=R/'index.html';s=p.read_text(encoding='utf-8');marker='<script src="assets/combat_audio_1015.js';assert marker in s
if 'assets/dracodia_phoenix_1020.js' not in s:s=s.replace(marker,'<script src="assets/dracodia_phoenix_art_1020.js?v=phoenix-1020"></script>\n<script src="assets/dracodia_phoenix_1020.js?v=phoenix-1020"></script>\n'+marker,1)
p.write_text(s,encoding='utf-8',newline='\n');print('Phoenix art and runtime registered')
