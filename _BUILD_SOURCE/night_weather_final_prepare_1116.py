from pathlib import Path
p=Path(__file__).with_name('night_weather_probe_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("for(const camera of[0,80,160,Math.max(0,worldWidth()-VW)])", "for(const camera of[0,80,80.25,159.5,160,Math.max(0,worldWidth()-VW)])")
s=s.replace("/prototype.json'","/candidate.json'")
s=s.replace("O/'prototype.json'","O/'candidate.json'")
s=s.replace("Injected candidate only:32", "Injected candidate only:48")
(p.parent/'night_weather_final_probe_1116.py').write_text(s,encoding='utf8',newline='\n')
