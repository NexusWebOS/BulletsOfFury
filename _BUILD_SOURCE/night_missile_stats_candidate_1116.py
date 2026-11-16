from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_1116.py');s=p.read_text(encoding='utf8')
s=s.replace("  p.evaluate(\"()=>{BOFOnline", "  p.add_script_tag(path=str(Path(__file__).with_name('night_missile_stats_1116.js')))\n  p.evaluate(\"()=>{BOFOnline")
s=s.replace("O/'before.json'","O/'candidate.json'")
(p.parent/'night_missile_stats_after_1116.py').write_text(s,encoding='utf8',newline='\n')
