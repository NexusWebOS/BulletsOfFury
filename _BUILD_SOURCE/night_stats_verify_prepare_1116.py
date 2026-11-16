from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'_BUILD_SOURCE/night_static_1116.py';s=p.read_text(encoding='utf8')
if "'assets/night_missile_stats_1116.js'"not in s:s=s.replace("'assets/night_weather_1116.js'","'assets/night_weather_1116.js','assets/night_missile_stats_1116.js'")
p.write_text(s,encoding='utf8',newline='\n')
