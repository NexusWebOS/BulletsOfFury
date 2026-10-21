from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'index.html';s=p.read_text(encoding='utf-8');marker='<script src="assets/combat_audio_1015.js';assert marker in s
if 'assets/hammer_redesign_1020.js' not in s:s=s.replace(marker,'<script src="assets/hammer_redesign_art_1020.js?v=actors-1020"></script>\n<script src="assets/hammer_redesign_1020.js?v=actors-1020"></script>\n'+marker,1)
p.write_text(s,encoding='utf-8',newline='\n');print('Hammer rewrite registered')
