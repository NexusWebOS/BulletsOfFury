from pathlib import Path
R=Path(__file__).resolve().parents[1];s=(R/'_BUILD_SOURCE/release_qa_1116_static.py').read_text(encoding='utf8')
s=s.replace("O=R/'_shots/release_qa_1116'","O=R/'_shots/cinema_overnight_1116'")
s=s.replace("'assets/release_entry_1116.js']", "'assets/release_entry_1116.js','assets/night_cinema_1116.js','assets/night_hq_art_1116.js','assets/night_city_atlas_1116.js','_BUILD_SOURCE/serve_nocache_1017.py']")
(R/'_BUILD_SOURCE/night_static_1116.py').write_text(s,encoding='utf8',newline='\n')
