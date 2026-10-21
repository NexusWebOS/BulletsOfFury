from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'index.html';s=p.read_text(encoding='utf-8');marker='<script src="assets/combat_audio_1015.js';assert marker in s
if 'assets/boss_download_1020.js' not in s:s=s.replace(marker,'<script src="assets/boss_download_1020.js?v=inventory-1020"></script>\n'+marker,1)
s=s.replace('v=whole-wings-1020"','v=whole-wings-1020-final"').replace('v=actors-1020"','v=actors-1020-final"').replace('v=routes-1020"','v=routes-1020-final"').replace('v=bosses-1020"','v=bosses-1020-final"');p.write_text(s,encoding='utf-8',newline='\n');print('Damaged-form download variants registered')
