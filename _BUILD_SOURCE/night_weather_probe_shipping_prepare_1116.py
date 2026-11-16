from pathlib import Path
for name in ['night_weather_probe_1116.py','night_weather_final_probe_1116.py','night_weather_fallback_probe_1116.py']:
 p=Path(__file__).with_name(name);s=p.read_text(encoding='utf8');old=" p.add_script_tag(path=str(Path(__file__).with_name('night_weather_1116.js')))"
 if old in s:s=s.replace(old," if not p.evaluate(\"typeof NW16!=='undefined'\"):p.add_script_tag(path=str(Path(__file__).with_name('night_weather_1116.js')))")
 p.write_text(s,encoding='utf8',newline='\n')
